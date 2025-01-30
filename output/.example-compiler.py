import sys

def compile_example_to_python(source_code):
    lines = source_code.split('\n')
    python_code = []

    for line in lines:
        if '//' in line:
            comment_index = line.find('//')
            line = line[:comment_index]
        python_code.append(line)

    return '\n'.join(python_code)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]
    try:
        with open(source_file, 'r') as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Error: The file {source_file} does not exist.")
        sys.exit(1)

    compiled_code = compile_example_to_python(source_code)
    output_file = source_file.replace('.example', '-compiled.py')

    with open(output_file, 'w') as file:
        file.write(compiled_code)

# Compiler designed by Sinamin Superset Maker
# Sinamin Superset Maker designed by JellkaGamez (https://www.youtube.com/@JellkaGamez)