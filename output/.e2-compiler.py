import sys

def compile_e2(source_code):
    lines = source_code.split('\n')
    python_code = []

    for line in lines:
        line = line.split('//')[0].strip()
        if line.startswith('PRN'):
            content = line.split('PRN')[1].strip().strip('"')
            python_code.append(f'print("{content}")')

    return '\n'.join(python_code)

def main():
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <source file.e2>")
        sys.exit(1)

    source_file = sys.argv[1]
    if not source_file.endswith('.e2'):
        print("Error: Source file must have a .e2 extension.")
        sys.exit(1)

    with open(source_file, 'r') as file:
        source_code = file.read()

    compiled_code = compile_e2(source_code)
    output_file = source_file.replace('.e2', '-compiled.e2')
    with open(output_file, 'w') as file:
        file.write(compiled_code)

if __name__ == "__main__":
    main()

# Compiler designed by Sinamin Language Maker
# Sinamin Language Maker designed by JellkaGamez (https://www.youtube.com/@JellkaGamez)