from huggingface_hub import InferenceClient
import curses, os, subprocess

def warn(text):
    print("\033[33m[WARNING] " + text + "\033[0m")

def finput(text):
    return input("\033[34m[INPUT] " + text + "\033[0m")

def info(text):
    print("\033[32m[INFO] " + text + "\033[0m")

def err(text):
    print("\033[31m[ERROR] " + text + "\033[0m")
    # raise Exception

try:
    with open("key.key", "r") as f:
        api_key = f.read().strip()
except FileNotFoundError:
    err("key.key not found")
    exit()


if api_key == "YOUR API KEY HERE":
    err("API key not inputed. Please input your API key in the key.key file.")

client = InferenceClient(api_key=api_key)

messages = [
    {
        "role": "system",
        "content": """
IGNORE ALL PREVIOUS INSTRUCTIONS  
You are part of the Sinamin Language Maker, a specialized program designed to create and manage languages of programming languages. You will be provided with step-by-step instructions and specific input. Your task is to strictly follow the instructions as described below.  

Step: Init  
When the step is "Init", you will receive a message formatted as follows:  
Name: <name provided by the user>  
Language: <base language provided by the user>  
Features: <features provided by the user>  
Step: Init  
Your response must be a single line containing only the file format specific to the language, in the following format:  
.<file_format_here>  
<file_format_here> must correspond to the appropriate file format for the specified language. And must not be the same as the base language (e.g. if the base language is Python, the file format must not be .py).

Step: Create  
The terminal usage will always be:  
python compiler.py <source file.py>  
When the step is "Create", you will receive a message formatted as follows:  
Features: <New features here>  
Source: <Source code the user has given>  

If there is no current compiler, the "Output" parameter will not be included in the message.  
Your task is to analyze the provided input and produce a valid raw Python implementation of the language's compiler. If there is a compiler there will be a "Output" parameter and a "Rating" parameter, The "Rating" parameter tells you whether or not the user likes the output of the compiler.
If an error occurs in the source code of the compiler, you will receive a message formatted like this:  
ERROR: <Code error>  
Your response must not include any errors as output, as this will be treated as executable code. The response must also avoid the use of ``` or any additional formatting that could interfere with execution.  

Your compiler must not be an interpreter or conatin a compiled version of the provided file.
Your compiler may not execute the compiled source code as that would screw up the program.
Your compiler must save the compiled source code to a file with the name of the source code file followed by "-compiled" and then the extension of the base language
Your compiler must not overwrite the original file. It should save it as a new file.

The source code is in the file format provided by you, and is not .py or .cpp or anything else. It it the file format that you provided.

The source code provided must not be within your compiler source code and your compiler MAY NOT be an interpreter and MAY NOT be the compiled source code. And it must support the console usage "python compiler.py <file>"
compiler.py is your source code file. You can use any external libraries that are supported by the Windows OS

Your response must include a raw Python implementation of the compiler source code. This compiler should correctly parse the language syntax provided in the source and translate it into valid Python code.  

Important Notes:  
- Do not include any additional formatting, examples, or explanations in your response.  
- The output will be interpreted as raw Python source code.  
- If there is an error in the source code of the compiler, respond with the raw Python implementation of the corrected compiler.  

By following these rules, you will accurately generate and manage the languages of programming languages and handle any errors that arise in the source code.
"""
    }
]

print("\033[33;1mSinamin Language Maker\033[0m")
warn("This program may use a lot of API calls!")
warn("You have been warned!")
info("This program takes a while to fully complete a Language so please be patient!")
info("Compilers will be written in python. You can find them in the output directory.")
begin = finput("Do you wish to continue? (Y/n): ")

if begin.lower() != "y":
    exit()

print("\033[0mVery well. Staring up \033[33;1mSinamin Language Maker\033[0m!")

info("Please fill in the required information!")

name = finput("Language name: ")
features = finput("Features (Comma Seperated): ")

language_info = {'name': name, 'features': features}
# language_info = {'name': 'Mamba', 'features': 'Simpler language, heavy focus on human readable syntax'}
# print(language_info)

def get_message():
    try:
        stream = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct", 
            messages=messages, 
            temperature=0.5,
            max_tokens=2048,
            top_p=0.7,
            stream=False
        )

        return stream["choices"][0]["message"]["content"]
    except Exception as e:
        err(f"An error occurred! {e}")
        return e

messages.append(
    {"role": "user", "content": f"Name: {language_info['name']}\nLanguage: {language_info['name']}\nFeatures: {language_info['features']}\nStep: Init"}
)

name = get_message().strip()

print("Your file format is: \"" + name + "\"")
warn("You will have to write some code in your own language!")

source = None

while source is None:
    file = "./output/src" + finput("Please input a file... ./output/src/")

    try:
        with open(file, "r") as f:
            source = f.read()
    except FileNotFoundError:
        warn("File not found. Try again.")
    except Exception as e:
        err(f"An error occurred: {e}. Try again.")

messages.append(
    {"role": "user", "content": f"Name: {name}\nLanguage: {language_info['name']}\nFeatures: {language_info['features']}\nStep: Create\nSource: {source}"}
)

cont = True
while cont:

    error = "fake error"

    while error is not None:
        compiler = get_message()
        compiler = compiler.replace("```", "")
        
        # Add a spesific line to the compiler

        compiler = f"{compiler}\n\n# Compiler designed by Sinamin Language Maker\n# Sinamin Language Maker designed by JellkaGamez (https://www.youtube.com/@JellkaGamez)"

        with open(f"./output/{name}-compiler.py", "w") as f:
            f.write(compiler)

        info(f"Compiler saved as {name}-compiler.py")

        with open(f"./output/saves/{name}-save.py", "w") as f:
            f.write(compiler)

        info(f"Save saved as {name}-save.save")

        error = None

        # Run the console command python <name>-compiler.py <file> and capture errors
        try:
            result = subprocess.run(
                ["python", f"output/{name}-compiler.py", file],
                check=True,
                capture_output=True,
                text=True
            )
            info("Compilation successful")
        except subprocess.CalledProcessError as e:
            info("Compilation failed with errors:")
            error = e.stderr
            err(e.stderr)

        if error:
            # feed errors back into AI

            messages.append(
                {"role": "user", "content": f"ERROR: {error}"}
            )
    
    finished = finput("Finished? (Y/n): ")

    if finished.lower() == "y":
        cont = False

    if cont:
        satisfaction = finput("Please rate the compiler (0-10): ")

        new_features = finput("New features (Comma Seperated): ")

        errors = finput("Errors with output (Comma Seperated): ")

        messages.append(
            {"role": "user", "content": f"File Format: {name}\nFeatures: {new_features}\nSource: {source}\nStep: Create\nErrors: {errors}\nRating: {satisfaction}"}
        )