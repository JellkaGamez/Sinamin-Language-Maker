.e2

import sys

def compile_example2_to_python(source_code, output_file):
    lines = source_code.split('\n')
    python_code = []

    for line in lines:
        # Remove comments
        comment_index = line.find('//')
        if comment_index != -1:
            line = line[:comment_index]
        line = line.strip()
        if line.startswith('PRN'):
            print_statement = line.replace('PRN', 'print', 1)
            python_code.append(print_statement)

    with open(output_file, 'w') as f:
        f.write('\n'.join(python_code))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <source file.e2>")
        sys.exit(1)

    source_file = sys.argv[1]
    if not source_file.endswith('.e2'):
        print("Source file must have .e2 extension")
        sys.exit(1)

    with open(source_file, 'r') as f:
        source_code = f.read()

    output_file = source_file.replace('.e2', '-compiled.e2')
    compile_example2_to_python(source_code, output_file)

# Compiler designed by Sinamin Language Maker
# Sinamin Language Maker designed by JellkaGamez (https://www.youtube.com/@JellkaGamez)