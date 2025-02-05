import sys

def compile_source(source_code):
    lines = source_code.split('\n')
    compiled_code = []
    for line in lines:
        if '//' in line:
            line = line[:line.index('//')]
        compiled_code.append(line.strip())
    return '\n'.join(compiled_code)

def main():
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <source file.e2>")
        return
    source_file = sys.argv[1]
    if not source_file.endswith('.e2'):
        print("Error: Source file must have .e2 extension")
        return
    with open(source_file, 'r') as file:
        source_code = file.read()
    compiled_code = compile_source(source_code)
    output_file = source_file.replace('.e2', '-compiled.e2')
    with open(output_file, 'w') as file:
        file.write(compiled_code)

if __name__ == "__main__":
    main()

# Compiler designed by Sinamin Language Maker
# Sinamin Language Maker designed by JellkaGamez (https://www.youtube.com/@JellkaGamez)