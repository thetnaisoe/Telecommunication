# Input File Generator: `protkollInputGenerator.py`

This project involves generating and processing binary files with specific formats. It consists of two main tasks where you read and write binary data according to predefined formats and parameters.

## Tasks

### Task 1: Read the Binary Files and Output First Record

The program reads binary files passed as command-line arguments and writes the contents of the first record to the standard output. Each binary file contains multiple records, and the first one is unpacked and printed using the following formats:

- **Parameter 1:** `bool`, `character`, `9 long string`
- **Parameter 2:** `9 long string`, `integer`, `float`
- **Parameter 3:** `float`, `character`, `bool`
- **Parameter 4:** `9 long string`, `bool`, `integer`

### Task 2: Print Values in Binary Format

The program generates binary data and prints it to stdout. The values are packed using the `struct` module, and the following formats are used for packing the data:

- `f` for `float`
- `i` for `integer`
- `c` for `character`
- `?` for `bool`
- `Xs` for strings (where X is the length of the string, e.g., `3s`)

Values to be packed and printed include:
1. `"first"` (18 characters), 48, `True`
2. `51.5`, `False`, `'X'`
3. `39`, `"second"` (16 characters), 58.9
4. `'Z'`, 70, `"third"` (19 characters)

### Script Usage

The program accepts four binary files as command-line arguments and processes them in sequence. Run the script as follows:

```bash
python3 client.py <file1> <file2> <file3> <file4>
