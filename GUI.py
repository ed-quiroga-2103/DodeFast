from tkinter import *

#-----------------CONSTANTS---------------------

WIDTH = 500
HEIGHT = 600


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master, background = "black")
        self.master = master
        self.init_window()

    def init_window(self):

        # changing the title of our master widget
        self.master.title("DodeFast")
        self.txt = ""
        # allowing the widget to take the full space of the root window
        self.grid()

        self.text=Text(self.master, bg = "black" , fg = "white")

        self.scroll = Scrollbar(self.master, command= self.text.yview)
        self.scroll.grid(column = 1 , row = 0,sticky = E)

        self.text.config(state=DISABLED, yscroll = self.scroll.set)
        self.text.grid(column = 0 ,row = 0,sticky = W)

        self.scroll.config(command=self.text.yview)



        self.e = Entry(self.master)
        self.e.grid(column = 0 , row = 1,sticky = W+E+N+S)



        # creating a menu instance
        menu = Menu(self.master, background='black', foreground='white',
               activebackground='black', activeforeground='white')
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu, background='black', foreground='white',
               activebackground='black', activeforeground='white')

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # create the file object)
        edit = Menu(menu, background='black', foreground='white',
               activebackground='black', activeforeground='white')

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="Undo")
        edit.add_command(label="Redo")
        edit.add_command(label="Show Text")

        root.bind('<Return>', self.showText)


        #added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)


    def client_exit(self):
        exit()

    def showText(self, event):
        self.txt += ">>> " + self.e.get() + "\n"

        self.e.delete(0,END)

        """
        self.myWidget.configure(yscrollcommand=None, state=NORMAL)
        self.myWidget.delete(1.0, END)
        self.myWidget.insert(END, data)
        self.myWidget.configure(yscrollcommand=self.myWidgetScrollbar.set, state=DISABLED)
        """
        self.text.config(state = NORMAL)

        self.text.delete(1.0, END)

        self.text.insert(END, self.txt)

        self.text.config(state = DISABLED)

        self.text.yview(END)

root = Tk()
app  = Window(root)

root.config(bg = "black")

root.mainloop()
