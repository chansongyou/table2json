# table2json
Convert excel sheets to json files. It may utilizes C# enum classes to convert string into int.


## Installation

### Prerequisite

Install uv

```shell
pip install uv
```

### Create virtual environment

```shell
uv venv
```

### Install dependencies and package

```shell
uv sync
```

## How-to

### Before running script

1. Put excel files in `input` directory
2. Check output directory (if there is something important) since all the files will be overwritten at the end of the script if there is the same file name.
3. Fullfill enum_files.txt with paths of C# files where enum is declared. Each path must be at a line.

### Run script

```shell
uv run table2json
```