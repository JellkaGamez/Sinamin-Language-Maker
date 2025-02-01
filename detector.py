def warn(text):
    print("\033[33m[WARNING] " + text + "\033[0m")

def finput(text):
    return input("\033[34m[INPUT] " + text + "\033[0m")

def info(text):
    print("\033[32m[INFO] " + text + "\033[0m")

def err(text):
    print("\033[31m[ERROR] " + text + "\033[0m")
    # raise Exception

compiler = None

while compiler is None:
    file = finput("Please input a file to continue... ")

    try:
        with open(file, "r") as f:
            compiler = f.read()
    except FileNotFoundError:
        warn("File not found. Try again.")
    except Exception as e:
        err(f"An error occurred: {e}. Try again.")

warn("This detector is not always acturate as scammers can modify the file in a way that makes it impossible to detect")

if compiler.__contains__("# Compiler designed by Sinamin Language Maker\n# Sinamin Language Maker designed by JellkaGamez (https://www.youtube.com/@JellkaGamez)"):
    info("Compiler is designed by Sinamin Language Maker")
else:
    info("Compiler is not designed by Sinamin Language Maker")