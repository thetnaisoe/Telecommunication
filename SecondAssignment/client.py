import struct
import sys

def read_and_print_first_record(file_path, struct_format):
    with open(file_path, 'rb') as f:
        data = f.read(struct.calcsize(struct_format))
        unpacked_data = struct.unpack(struct_format, data)
        print(unpacked_data)

def pack_and_print(struct_format, *values):
    packed_data = struct.pack(struct_format, *values)
    print(packed_data)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 client.py <file1> <file2> <file3> <file4>")
        exit(1)

    # Define the structures
    structures = {
        'file1': '?c9s',
        'file2': '9sif',
        'file3': 'fc?',
        'file4': '9s?i'
    }

    # Task 1: Read and print the first record of each file
    for i in range(1, 5):
        file_path = sys.argv[i]
        struct_format = structures[f'file{i}']
        read_and_print_first_record(file_path, struct_format)

    # Task 2: Pack and print the given values in binary format
    values_to_pack = [
        ('18s i ?', b'elso', 48, True),
        ('f ? c', 51.5, False, b'X'),
        ('i 16s f', 39, b'masodik', 58.9),
        ('c i 19s', b'Z', 70, b'harmadik')
    ]

    for struct_format, *values in values_to_pack:
        pack_and_print(struct_format, *values)