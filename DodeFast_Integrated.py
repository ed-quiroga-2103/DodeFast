from DodeFast import *
from GUI import *
from tkinter import *

env = {}

DFInterpreter = BasicExecute(env)

root = Tk()
app  = Window(root, DFInterpreter)

root.config(bg = "black")

root.mainloop()
        
