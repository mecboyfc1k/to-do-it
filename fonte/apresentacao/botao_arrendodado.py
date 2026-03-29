from tkinter import *
from tkinter import Tk
from typing import Callable
from math import *
from PIL import Image, ImageTk

class BotaoArredondado(Canvas):

    PADX=10
    PADY=10

    def __init__(self, master, raio:int, botao_bg_cr, icone:PhotoImage, call:Callable, *args, **kwargs):
        super().__init__(master, width=raio, height=raio,highlightthickness=0,bg=master["bg"])
        self._raio=raio
        self._botao_bg_cr=botao_bg_cr
        self._icone = icone
        self._chamavel=call
        self._argumentos=args
        self._argumentos_chave=kwargs

    def inicializar(self):
        
        self.pack(anchor="se", side="right",padx=BotaoArredondado.PADX,pady=BotaoArredondado.PADY)

        self.create_oval(0,0,self._raio,self._raio,fill=self._botao_bg_cr, outline="")

        pad = self._raio//2
        self.create_image(pad, pad, image=self._icone)

        self.bind("<Button-1>", self._ao_clicar, "+")

    def _ao_clicar(self, event):
        self._chamavel(*self._argumentos, **self._argumentos_chave)