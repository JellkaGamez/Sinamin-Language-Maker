import sys

def compile_exm(source_code, output_file):
    lines = source_code.split('\n')
    compiled_code = []

    for line in lines:
        # Remove comments
        comment_index = line.find('//')
        if comment_index != -1:
            line = line[:comment_index]
        # Strip whitespace
        line = line.strip()
        if line:
            # Convert PRN to print
            if line.startswith('PRN '):
                line = 'print(' + line[4:] + ')'
            compiled_code.append(line)

    with open(output_file, 'w') as f:
        f.write('\n'.join(compiled_code))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <source file.exm>")
        sys.exit(1)

    source_file = sys.argv[1]
    if not source_file.endswith('.exm'):
        print("Source file must have .exm extension")
        sys.exit(1)

    output_file = source_file[:-4] + '-compiled.py'
    with open(source_file, 'r') as f:
        source_code = f.read()

    compile_exm(source_code, output_file)

# Compiler designed by Sinamin Language Maker
# Sinamin Language Maker designed by JellkaGamez (https://www.youtube.com/@JellkaGamez)