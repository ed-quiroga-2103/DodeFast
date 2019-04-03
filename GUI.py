from tkinter import *
from DodeFast import *
from CodeManager import *

#-----------------CONSTANTS---------------------

WIDTH = 500
HEIGHT = 600

#-----------------------------------------------

class Window(Frame):

    def __init__(self, master, DFInterpreter):
        Frame.__init__(self, master, background = "black")
        self.master = master
        self.init_window()
        self.DFInterpreter = DFInterpreter
        self.lexer = BasicLexer()
        self.parser = BasicParser()

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
        file.add_command(label= "New File", command = self.newFile)
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

        self.master.bind('<Return>', self.showText)


        #added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)


    def client_exit(self):
        exit()


    def runCodeA(self, textInput):

        self.DFInterpreter.env = {}


        self.txt += ">>> ------------------Code block executed!------------------" + "\n"

        text = textInput.get("1.0",END)

        if text:

            lines = manageCode(text)

            print(lines)
            try:
                for line in lines:
                    if line:
                        try:
                            lex = self.lexer.tokenize(line)
                            tree = self.parser.parse(lex)
                        except AttributeError:
                            self.txt += ">>> Syntax Error! Expression in code block not found!" + "\n"
                            break
                        except:
                            self.txt += ">>> Illegal token in code block!" + "\n"
                            break


                        print(tree)
                        result = self.DFInterpreter.walkTree(tree)

                        try:
                            if result[0] == "print":
                                self.txt += str(result[1]) + "\n"
                                print("here")
                        except:
                            pass


            except:
                self.txt += ">>> Semantic error on code block!\nCheck your code because something is not right." + "\n"


            self.e.delete(0,END)

            self.text.config(state = NORMAL)

            self.text.delete(1.0, END)

            self.text.insert(END, self.txt)

            self.text.config(state = DISABLED)

            self.text.yview(END)

    def runCode(self, event, textInput):

        self.DFInterpreter.env = {}


        self.txt += ">>> ------------------Code block executed!------------------" + "\n"

        text = textInput.get("1.0",END)

        if text:

            lines = manageCode(text)

            print(lines)
            try:
                for line in lines:
                    if line:
                        try:
                            lex = self.lexer.tokenize(line)
                            tree = self.parser.parse(lex)
                        except AttributeError:
                            self.txt += ">>> Syntax Error! Expression in code block not found!" + "\n"
                            break
                        except:
                            self.txt += ">>> Illegal token in code block!" + "\n"
                            break



                        result = self.DFInterpreter.walkTree(tree)
                        print("Resultado " +str(result))

                        try:
                            if isinstance(result, list):
                                self.txt += str(result) + "\n"

                            if result[0] == "print":
                                self.txt += str(result[1]) + "\n"
                                print("here")
                        except:
                            pass


            except:
                self.txt += ">>> Semantic error on code block!\nCheck your code because something is not right." + "\n"


            self.e.delete(0,END)

            self.text.config(state = NORMAL)

            self.text.delete(1.0, END)

            self.text.insert(END, self.txt)

            self.text.config(state = DISABLED)

            self.text.yview(END)



    def newFile(self):
        newWindow = Toplevel(self)


        newWindow.config(bg = "black")

        text = Text(newWindow, bg = "black", fg = "white", insertbackground = "white")

        scroll = Scrollbar(newWindow, command= text.yview)
        scroll.grid(column = 1 , row = 0,sticky = E)

        text.config(yscroll = scroll.set)
        text.grid(column = 0 ,row = 0,sticky = W)

        scroll.config(command= text.yview)

        menu = Menu(newWindow, background='black', foreground='white',
               activebackground='black', activeforeground='white')
        newWindow.config(menu=menu)

        file = Menu(menu, background='black', foreground='white',
               activebackground='black', activeforeground='white')

        file.add_command(label= "Run", command = lambda: self.runCodeA(text))

        newWindow.bind('<Control-F5>', lambda event : self.runCode(event, text))

        menu.add_cascade(label = "File", menu = file)

    def showText(self, event):

        text = self.e.get()

        self.txt += ">>> " + self.e.get() + "\n"


        if text:

            lines = manageCode(text)

            for line in lines:
                if line:
                    try:
                        lex = self.lexer.tokenize(line)
                        tree = self.parser.parse(lex)

                        print(tree)
                        
                    except AttributeError:
                        self.txt += ">>> Syntax Error! Expression not found! \nCheck if everything is written correctly" + "\n"
                        break
                    except:
                        self.txt += ">>> Illegal token!" + "\n"
                        break

                    result = self.DFInterpreter.walkTree(tree)
                    print(result)
                    if isinstance(result, list):
                        self.txt += str(result) + "\n"

                    if result != None:
                        self.txt += str(result) + "\n"


        self.e.delete(0,END)

        self.text.config(state = NORMAL)

        self.text.delete(1.0, END)

        self.text.insert(END, self.txt)

        self.text.config(state = DISABLED)

        self.text.yview(END)
