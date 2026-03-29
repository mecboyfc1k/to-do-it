from tkinter import *
from tkinter import Tk
from fonte.apresentacao.paleta import Cores as cor

class BarraSuperior(Frame):

    W=300

    def __init__(self, master, bg):
        super().__init__(master)

        self.configure(bg=bg,
                       height=self.master.winfo_screenheight()//8,
                       width=BarraSuperior.W)
        
    def inicializar(self):
        self.pack(anchor="n",side='top', fill='x', expand=False)