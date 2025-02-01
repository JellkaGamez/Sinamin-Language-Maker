print("\033[33m[WARNING] " + "This is a TODO file. Exitting..." + "\033[0m")
print("\033[33m[WARNING] " + "To see why please open the file and read the comments" + "\033[0m")

# ================= TODO =================
# Use the maker_function file to implement 
# a propper command-line based interface
# ========================================

exit()

from huggingface_hub import InferenceClient
import curses, os, subprocess, json

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
You are part of the Sinamin Language Maker, a specialized program designed to create and manage programming languages. You will be provided with step-by-step instructions and specific input. Your task is to strictly follow the instructions as described below.  

Step: Init  
When the step is "Init", you will receive a message formatted as follows:  

Name: <name provided by the user>  
Features: <features provided by the user>  
Step: Init  

Your response must be a single line containing only the file extension for the new language, in this format:  

.<file_format_here>  

<file_format_here> must be a new, unique file extension related to the language's name. It must not be an existing programming language extension (e.g., .py, .cpp, .js, etc.). No explanations, comments, or extra text are allowed.  

Step: Create  
The terminal usage will always be:  

python compiler.py <source file.ext>  

When the step is "Create", you will receive a message formatted as follows:  

Features: <new features here>  
Source: <source code the user has given>  

If a compiler already exists, you will also receive:  

Output: <previous compiled output>  
Rating: <user feedback rating>  

The "Rating" parameter indicates user satisfaction with the compiler’s output.  

If an error occurs in the compiler, you will receive:  

ERROR: <code error>  

You must return a valid, functional Python compiler implementation that processes the custom language and converts it into valid Python code.  

Your compiler must:  
- Be written in Python only  
- Strictly follow the features specified by the user  
- Parse the provided source code and generate valid Python output  
- Save the compiled output in a new file named <original_filename>-compiled.<file_format> (where <file_format> is the generated extension)  
- Support command-line execution using python compiler.py <file>  
- Use only Windows-supported Python libraries  

Your compiler must not:  
- Be an interpreter (it must convert code, not execute it)  
- Contain a pre-written program (e.g., print("Hello World"))  
- Execute the compiled source code  
- Overwrite the original file  
- Include placeholder or default code  
- Start with the name of the compiler's language (e.g., Python)  

Strict Output Format:  
- Your response must contain only raw Python source code  
- No markdown, formatting, explanations, comments, or examples are allowed  
- Do not include any additional text other than the required Python code  
- Only return the corrected compiler code if an error occurs

If you make a mistake and add markdown formatting in your response, the program will automatically remove it.
You must still avoid markdown fomatting in your response.
"""
# prompt V1.1
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

save = finput("Do you want to load a save? (Y/n): ")

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

if save.lower() == "y":
    save = None

    save_file = None

    while save is None:
        file = "./output/saves/" + finput("Please input a save file... ./output/saves/")
        try:
            with open(file, "r") as f:
                save = f.read()
                save_file = file
        except FileNotFoundError:
            warn("File not found. Try again.")
        except Exception as e:
            err(f"An error occurred: {e}. Try again.")

    save_JSON = json.loads(save)

    language_info = save_JSON["language_info"]
    messages = save_JSON["messages"]

    source_file = save_JSON["source_code_file"]
    with open(source_file, "r") as f:
        source = f.read()
    compiler_file = save_JSON["compiler_code_file"]

    name = language_info["name"]
    features = language_info["features"]

else:
    info("Please fill in the required information!")

    name = finput("Language name: ")
    features = finput("Features (Comma Seperated): ")

    language_info = {'name': name, 'features': features}



    messages.append(
        {"role": "user", "content": f"Name: {language_info['name']}\nFeatures: {language_info['features']}\nStep: Init"}
    )

    name = get_message().strip()

    print("Your file format is: \"" + name + "\"")
    warn("You will have to write some code in your own language!")

    source = None

    source_file = None

    while source is None:
        file = "./output/src/" + finput("Please input a file... ./output/src/")
        try:
            with open(file, "r") as f:
                source = f.read()
                source_file = file
        except FileNotFoundError:
            warn("File not found. Try again.")
        except Exception as e:
            err(f"An error occurred: {e}. Try again.")

messages.append(
    {"role": "user", "content": f"Name: {name}\nLanguage: {language_info['name']}\nFeatures: {language_info['features']}\nStep: Create\nSource: {source}"}
)

if compiler_file:
    with open(compiler_file, "r") as f:
        compiler = f.read()

cont = True
while cont:

    error = "fake error"

    while error is not None:
        compiler = get_message()
        compiler = compiler.replace("```", "")
        
        # Add a spesific line to the compiler

        compiler = f"{compiler}\n\n# Compiler designed by Sinamin Language Maker\n# Sinamin Language Maker designed by JellkaGamez (https://www.youtube.com/@JellkaGamez)"

        if compiler.startswith('python'):
            compiler.replace('python', '')

        if compiler.__contains__('```'):
            compiler.replace('```', '')

        with open(f"./output/{name}-compiler.py", "w") as f:
            f.write(compiler)

        info(f"Compiler saved as {name}-compiler.py")

        with open(f"./output/saves/{name}-save.json", "w") as f:
            f.write(json.dumps({
                "language_info": language_info,
                "source_code_file": source_file,
                "compiler_code_file": f"./output/{name}-compiler.py",
                "messages": messages
            }))

        info(f"Save saved as {name}-save.json")

        error = None

        # Run the console command python <name>-compiler.py <file> and capture errors
        try:
            result = subprocess.run(
                ["python", f"output/{name}-compiler.py", source_file],
                check=True,
                capture_output=True,
                text=True
            )
            info("Compilation successful")
        except subprocess.CalledProcessError as e:
            info("Compilation failed with errors:")
            error = e
            err(e)

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