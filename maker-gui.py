print("\033[33m[WARNING] " + "This is a TODO file. Exitting..." + "\033[0m")
print("\033[33m[WARNING] " + "To see why please open the file and read the comments" + "\033[0m")

# ================= TODO =================
# Use the maker_function file to implement 
# a gui interface
# ========================================

# exit() <- removed while developing

# Import Module
from tkinter import *
import os
import libraries.maker_function as mf

gui_data = os.listdir(os.path.join(os.path.dirname(__file__), "data/gui"))
print(gui_data)

if gui_data == []:
    mf.warn("No GUI data found.")
    with open("./data/gui/saves.json", "w") as f:
        f.writelines(
            """
{
    'saves': []
}
"""
        )
    mf.info("Created saves.json")
    mf.info("Please restart the program.")
    exit()

class Window():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("900x500")
        self.root.title("Sinamin Language Maker")
        self.root.resizable(False, False)
    
    def generateGUI(self):
        self.languages = Frame(master=self.root, width=250, height=500, highlightbackground="black", highlightthickness=1)
        self.languages.place(width=250, height=500)
    
        self.label = Label(master=self.languages, text="Saved Languages")
        self.label.place(relx=0.5, rely=0.02, anchor=CENTER)


    def run(self):
        self.root.mainloop()

window = Window()
window.generateGUI()
window.run()