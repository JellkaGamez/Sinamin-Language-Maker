print("\033[33m[WARNING] " + "This is a TODO file. Exitting..." + "\033[0m")
print("\033[33m[WARNING] " + "To see why please open the file and read the comments" + "\033[0m")

# ================= TODO =================
# Use the maker_function file to implement 
# a gui interface
# ========================================

# exit() <- removed while developing

# Import Module
from tkinter import *
import os, json, time
import subprocess
import libraries.maker_function as mf

gui_data = os.listdir(os.path.join(os.path.dirname(__file__), "data/gui"))
print(gui_data)

if gui_data == []:
    mf.warn("No GUI data found.")
    with open("./data/gui/saves.json", "w") as f:
        f.writelines(
            """
{
    "langs": []
}
"""
        )
    mf.info("Created saves.json")
    mf.info("Please restart the program.")
    exit()

saves = None
with open("./data/gui/saves.json", "r") as f:
    saves = f.read()
saves = json.loads(saves)
class Window():
    def __init__(self):
        self.languages = []
        self.lang_buttons = []
        self.lang_labels = []
        self.lang_dat = []
        self.root = Tk()
        self.root.geometry("900x500")
        self.root.title("Sinamin Language Maker")
        self.root.resizable(False, False)
    
    def generateGUI(self):
        self.languages = Frame(master=self.root, width=250, height=500, highlightbackground="black", highlightthickness=1)
        self.languages.place(width=250, height=500)

        self.project = Frame(master=self.root, width=650, height=500, highlightbackground="black", highlightthickness=1)
        self.project.place(width=650, height=500, x=250)

        label = Label(master=self.languages, text="Saved Languages")
        label.place(relx=0.5, rely=0.02, anchor=CENTER)
        self.lang_labels.append(label)

        if saves['langs'] == []:
            label = Label(master=self.languages, text="No saves found.")
            label.place(relx=0.5, rely=0.1, anchor=CENTER)
            self.lang_labels.append(label)
        else:
            i = 0
            for save in saves['langs']:
                lang_dat = save
                button = Button(master=self.languages, text=f"{lang_dat['name']} ({lang_dat['format']})", command=lambda lang=lang_dat: self.load_language(lang))
                button.place(relx=0.5, rely=0.1 + (i * 0.05), anchor=CENTER)
                self.lang_buttons.append(button)
                i += 1

    def LANG_new(self, name):
        # make a new blank language save
        with open(f"./data/gui/saves/{name}.json", "w") as f:
            f.write()

    def save(self, lang_dat):
        with open(lang_dat['source_code_file'], "w") as f:
            f.write(self.source_area.get("0.0", END))

        lang_dat['language_info']['features'] = self.features.get()

    def cont(self, lang, lang_dat):
        self.compile_area.delete("1.0", END)
        self.compile_area.insert(0.5, "GENERATING CODE...\nThis may freeze or be very slow...\nPlease wait...")
        time.sleep(1)
        mf.continue_create(lang['name'], lang_dat['source_code_file'], -1, lang_dat['language_info']['features'], '(You may ignore these errors as this is a TODO GUI message) Test Error')
        mf.create(lang['name'], lang_dat['language_info'], lang_dat['source_code_file'])

    def compile(self, lang, lang_dat):
        try:
            result = subprocess.run(
                ["python", f"output/{lang['format']}-compiler.py", f"{lang_dat['source_code_file']}"],
                check=True,
                capture_output=True,
                text=True
            )
            mf.info("Compilation successful")
            with open(f'{lang_dat['source_code_file'].replace(lang['format'], '')}-compiled.py', 'r') as f:
                self.compile_area.delete("1.0", END)
                self.compile_area.insert(0.5, f.read())

        except subprocess.CalledProcessError as e:
            mf.info("Compilation failed with errors:")
            mf.err(e)

    def projectUI(self, project, data, lang_dat):
        if data is None:
            # empty the project frame without destryoing it
            for widget in project.winfo_children():
                widget.destroy()
            
            return
        label = Label(master=project, text=f"{data['name']} ({data['format']})")
        label.place(relx=0.5, rely=0.02, anchor=CENTER)

        label = Label(master=project, text=f"Features")
        label.place(relx=0.5, rely=0.08, anchor=CENTER)

        self.features = Entry(master=project, text='Features', width=100)
        self.features.insert(0, lang_dat['language_info']['features'])
        self.features.place(relx=0.5, rely=0.12, anchor=CENTER)

        label = Label(master=project, text=f"Example Source Code")
        label.place(relx=0.5, rely=0.18, anchor=CENTER)

        compile = Button(master=project, text="Compile", command=lambda: self.compile(data, lang_dat))
        compile.place(relx=0.4, rely=0.58, anchor=CENTER)

        save = Button(master=project, text="Save", command=lambda: self.save(lang_dat))
        save.place(relx=0.6, rely=0.58, anchor=CENTER)

        cont = Button(master=project, text="Continue", command=lambda: self.cont(data, lang_dat))
        cont.place(relx=0.5, rely=0.84, anchor=CENTER)

        self.source_code = None
        with open(lang_dat['source_code_file'], "r") as f:
            self.source_code = f.read()

        self.source_area = Text(master=project, width=50, height=10)
        self.source_area.insert(0.5, self.source_code)
        self.source_area.place(relx=0.5, rely=0.36, anchor=CENTER)

        self.compile_area = Text(master=project, width=50, height=5)
        self.compile_area.place(relx=0.5, rely=0.7, anchor=CENTER)


    def load_language(self, lang):
        self.lang_dat = mf.load_save(f'./data/gui/saves/{lang['format']}-save.json')
        self.projectUI(self.project, lang, self.lang_dat)

    def run(self):
        self.root.mainloop()

window = Window()
window.generateGUI()
window.projectUI(window.project, None, None)
window.run()