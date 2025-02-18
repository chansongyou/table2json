import pandas as pd

from table2json.csharp_enum import CSharpEnumData


def to_bool(value: int | str | bool):
    if isinstance(value, bool):
        return value
    elif isinstance(value, int):
        return bool(value)
    elif isinstance(value, str):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        else:
            raise ValueError("Only 1, 0, true, and false are allowed!")
    else:
        raise ValueError("Only string or integer value is allowed for boolean")



def parse_sheet(
    file_name: str, sheet_name: str, df_sheet: pd.DataFrame, enum_data: CSharpEnumData = None
) -> dict:
    series_column_types = df_sheet.iloc[0]
    if any(series_column_types.isna()):
        raise ValueError(f"{file_name}.{sheet_name} has empty type. Please enter types")

    column_types = series_column_types.to_dict()

    df_rows = df_sheet.iloc[1:]

    for i in range(len(df_rows)):
        row = df_rows.iloc[i]

        keys = row.keys()
        for key in keys:
            column_type = column_types[key]
            value = row[key]

            if column_type == "str":
                row[key] = str(value)
            elif column_type == "int":
                row[key] = int(value)
            elif column_type == "float":
                row[key] = float(value)
            elif column_type == "bool":
                row[key] = to_bool(value)
            else:
                row[key] = enum_data.get_int_value_by_enum(column_type, str(value))

    return df_rows.to_dict(orient="list")
