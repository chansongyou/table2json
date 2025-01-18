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

### Excel format

#### Supported types

- str
- int
- float
- enum(declared in C# files)
    - e.g., `EnumName` if declared like `public enum EnumName`

#### Format

As shown the below table, the first line must be one of the supported types.

Empty type is not allowed.

| ID  | Name   | Value | Race      | FloatValue |
|-----|--------|-------|-----------|------------|
| int | str    | int   | EnumName  | float      |
| 0   | asdfad | 12    | Human     | 1.2        |
| 1   | agas   | 24    | Human     | 1.354      |
| 2   | dfd    | 5     | Orc       | 2.3        |
| 3   | dd     | 65    | Elf       | 5.3        |
| 4   | sdafa  | 6     | Elf       | 2.4        |


### Before running script

1. Put excel files in `input` directory
2. Check output directory (if there is something important) since all the files will be overwritten at the end of the script if there is the same file name.
3. Fullfill enum_files.txt with paths of C# files where enum is declared. Each path must be at a line.

### Run script

```shell
uv run table2json
```
