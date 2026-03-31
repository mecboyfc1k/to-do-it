from tkinter import *
from tkinter import Tk
from typing import Callable
from math import *
from PIL import Image, ImageTk

class BotaoArredondado(Canvas):

    PADX=10
    PADY=10

    def __init__(self, master, raio:int, botao_bg_cr, icone:PhotoImage, call:Callable, *args, bt_ck_cr = "", bt_hv_cr = "", **kwargs):
        super().__init__(master, width=raio, height=raio,highlightthickness=0,bg=master["bg"])
        self._raio=raio
        self._botao_bg_cr=botao_bg_cr
        self._icone = icone
        self._chamavel=call
        self._argumentos=args
        self._argumentos_chave=kwargs
        self._bt_hv_cr = bt_hv_cr
        self._bt_ck_cr = bt_ck_cr
        self.bind("<Button-1>", self._ao_clicar, "+")
        self.bind("<ButtonRelease-1>", self._ao_desclicar, "+")
        self.bind("<Enter>", self._on_enter, "+")
        self.bind("<Leave>",self._on_leave, "+")

    def inicializar(self):
        
        self.pack(anchor="se", side="right",padx=BotaoArredondado.PADX,pady=BotaoArredondado.PADY)

        self._bt_bg = self.create_oval(0,0,self._raio,self._raio,fill=self._botao_bg_cr, outline="")

        pad = self._raio//2
        self.create_image(pad, pad, image=self._icone)

    def _ao_clicar(self, event):
        self.itemconfigure(self._bt_bg, fill=self._bt_ck_cr)

    def _ao_desclicar(self, event):
        self.itemconfigure(self._bt_bg, fill=self._botao_bg_cr)
        self._chamavel(*self._argumentos, **self._argumentos_chave)

    def _on_enter(self, event):
        self.itemconfigure(self._bt_bg, fill=self._bt_hv_cr)

    def _on_leave(self, event):
        self.itemconfigure(self._bt_bg, fill=self._botao_bg_cr)