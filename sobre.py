#                           PLATAFORMA SANDBOX 3/3 2022
#
# Conjunto de abas que permite ao usuario ter acesso às  informações do sistema através da interface gráfica. 
from tkinter import*
import sys
from tkinter.scrolledtext import ScrolledText

class sob(object):
    def __init__(self, **kw):                    
        self.sob = Toplevel()
        self.sob.title("SANDBOX")
        self.sob.geometry('930x455')
        self.sob.configure(bg='white')
        self.sob.resizable(width=0, height=0)
        self.create_text()   
       
        
    def create_text(self):
        atex = ScrolledText(self.sob,width = 90, 
                            height = 20, 
                            font = ("Times New Roman",
                                    15,))
        atex.grid(column = 0, pady = 10, padx = 10)
        atex.insert(INSERT,
                                    """\
            This is a scrolledtext widget to make tkinter text read only.
                                    Hi
                                    Geeks !!!
                                    Geeks !!!
                                    Geeks !!! 
                                    Geeks !!!










                escreva o texto                    
                                    Geeks !!!
                                    Geeks !!!
                                    Geeks !!!
                                    """)
        atex.configure(state ='disabled') 