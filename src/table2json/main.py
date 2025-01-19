import os
import json
import logging
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

from table2json.csharp_enum import find_enums
from table2json.parser import parse_sheet
from table2json.encrypt import AESUtility

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_dir_path(input_dir: Path, output_dir: Path, excel_file_path: Path):
    dir_path = output_dir / excel_file_path.relative_to(input_dir).parent

    if not dir_path.exists():
        dir_path.mkdir(parents=True)

    return dir_path


def create_json_file(
    input_dir: Path, output_dir: Path, excel_file_path: Path, sheet_name: str, data: dict
) -> Path:
    dir_path = _get_dir_path(input_dir, output_dir, excel_file_path)

    json_file_name = dir_path / f"{sheet_name}.json"
    with open(json_file_name, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return json_file_name


def create_encrypted_dat_file(
    input_dir: Path, output_dir: Path, excel_file_path: Path, sheet_name: str, data: dict
) -> Path:
    dir_path = _get_dir_path(input_dir, output_dir, excel_file_path)

    dat_file_name = dir_path / f"{sheet_name}.dat"
    data_json = json.dumps(data, indent=4, ensure_ascii=False)

    encrypted_data = AESUtility.encrypt(data_json, os.environ["KEY"], os.environ["IV"])
    with open(dat_file_name, "w") as f:
        f.write(encrypted_data)

    return dat_file_name


def _read_enum_files(enum_files_path: Path) -> list[Path]:
    with open(enum_files_path, "r") as f:
        files = f.readlines()

    return [Path(file.strip()) for file in files if file.strip()]


def main():
    parser = ArgumentParser(description="generate json files from excel files")

    parser.add_argument(
        "--input-dir",
        type=str,
        default="./input",
        help="Please enter path of directory where excel files reside.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="Please enter path of directory where json files will be populated.",
    )
    parser.add_argument(
        "--output-dir-encrypt",
        type=str,
        default="./output_encrypted",
        help="Please enter path of directory where encrypted json files will be populated.",
    )
    parser.add_argument(
        "--enum_files",
        type=str,
        default="./enum_files.txt",
        help="Please provide a file that contains paths of *.cs files with new lines",
    )
    parser.add_argument(
        "--encrypt",
        action="store_true",
        help="If this arg is given, json files will be encrypted further",
    )

    args = parser.parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    enum_files_path = Path(args.enum_files)
    encrypt = args.encrypt

    load_dotenv()

    if not input_dir.is_dir() or not output_dir.is_dir() or not enum_files_path.is_file():
        logger.error("Please check if input arguments are correct")
        raise ValueError

    excel_files = [file_path for file_path in input_dir.rglob("*.xlsx")]

    logger.info("Finding all the enums in c# files...")
    enum_data = find_enums(_read_enum_files(enum_files_path))
    logger.info(f"Found {len(enum_data.enums)} enums!")

    logger.info("Processing excel files...")
    result_files = set()
    for excel_file in tqdm(excel_files):
        sheets = pd.read_excel(excel_file, sheet_name=None)
        for sheet_name, df_sheet in sheets.items():
            sheet_data = parse_sheet(excel_file.stem, sheet_name, df_sheet, enum_data)
            if encrypt:
                file_generated = create_encrypted_dat_file(
                    input_dir, output_dir, excel_file, sheet_name, sheet_data
                )
            else:
                file_generated = create_json_file(
                    input_dir, output_dir, excel_file, sheet_name, sheet_data
                )

            if file_generated in result_files:
                raise KeyError(f"{str(file_generated)} already exists!")

            result_files.add(file_generated)

    logger.info(f"{len(result_files)} files are generated!")
