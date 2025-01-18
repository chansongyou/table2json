"""Read C# files and find enum classes"""

import re
from dataclasses import dataclass
from pathlib import Path

from tree_sitter import Language, Parser, Query
from tree_sitter_c_sharp import language


class CSharpEnum:
    def __init__(self, name: str, start_row: int, end_row: int):
        self.name: str = name
        self.start_row: int = start_row
        self.end_row: int = end_row
        self.values: dict = {}


class CSharpEnumData:
    def __init__(self):
        self.enums: list[CSharpEnum] = []

    def find_enum_class(self, enum_name: str) -> CSharpEnum | None:
        for enum_class in self.enums:
            if enum_class.name == enum_name:
                return enum_class

    def get_int_value_by_enum(self, enum_class_name: str, enum_value: str):
        if not (enum_class := self.find_enum_class(enum_class_name)):
            raise ValueError(f"Unknown enum class: {enum_class_name}")

        return enum_class.values[enum_value]


def find_enums(file_path: Path) -> CSharpEnumData:
    """
    Find and parse all enums in the given C# source code.
    """

    if not file_path.exists():
        raise FileNotFoundError

    if file_path.suffix != ".cs":
        raise ValueError("Please enter c# file only")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    csharp = Language(language())
    parser = Parser(csharp)
    tree = parser.parse(bytes(content, "utf8"))

    enum_data = CSharpEnumData()

    query = Query(
        csharp,
        """
        (enum_declaration 
            name: (identifier)
            body: (_)
        ) @enum_class
        """,
    )
    nodes_captured = query.captures(tree.root_node)
    for node_type, nodes in nodes_captured.items():
        if node_type != "enum_class":
            continue

        for node in nodes:
            enum_class_name = None
            for child in node.children:
                if child.type != "identifier":
                    continue

                enum_class_name = child.text.decode().strip()
                break

            if enum_class_name is None:
                raise ValueError("Enum class name not found!")

            enum_class = CSharpEnum(enum_class_name, node.start_point.row, node.end_point.row)
            enum_data.enums.append(enum_class)

            for child in node.children:
                if child.type != "enum_member_declaration_list":
                    continue

                index = 0
                for enum_member in child.children:
                    if enum_member.type != "enum_member_declaration":
                        continue

                    line = lines[enum_member.start_point.row]

                    if match := re.match(
                        r"\s*(?P<name>[a-zA-Z0-9_]+)\s*=\s*(?P<value>-?\d+)", line
                    ):
                        index = int(match.group("value"))
                        enum_class.values[match.group("name")] = index
                    else:
                        enum_class.values[enum_member.text.decode().strip()] = index

                    index += 1

    return enum_data
