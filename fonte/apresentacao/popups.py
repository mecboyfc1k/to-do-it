from tkinter import *
from tkinter import Tk, font
from fonte.apresentacao.fontes import Fontes
from tkcalendar import DateEntry
from fonte.apresentacao.listas import *
from PIL import Image, ImageTk
from pathlib import Path
from fonte.dominio.excecoes import DescrInvalida
from datetime import date 

class PopUpCriar(Toplevel):

    def __init__(self, bg, width, height, gap_r, gap_c, lista:Lista):
        super().__init__(bg=bg, takefocus=True, )
        self.geometry(f"{width}x{height}")
        self.rowconfigure((0, 1, 2),pad=gap_r)
        self.columnconfigure((0, 1),pad=gap_c)
        self.resizable(False, False)
        self._lista = lista
        self._campos = []
        

    def inicializar(self):

        fonte = font.Font(family=Fontes.ITENS_LISTA[0], size=Fontes.ITENS_LISTA[1])

        Label(self, text="Descrição:", font=fonte, foreground="black", bg=self["bg"]).grid(column=0, row=0)
        self._campos.append(Entry(self,width=30))
        self._campos[0].grid(column=1, row=0)

        Label(self, text="Prazo final:", font=fonte, foreground="black", bg=self["bg"]).grid(column=0, row=1)
        self._campos.append(DateEntry(self))
        self._campos[1].grid(column=1, row=1)

        Button(self, text="Criar", command=self._criar, font=fonte, width=20).grid(row=2, column=1,)
        Button(self, text="Cancelar", command=self._destruir, font=fonte).grid(row=2, column=0,)

        self.grab_set()

    def _destruir(self):
        self.destroy()

    def _criar(self):
        descr=self._campos[0].get()
        data_prev=self._campos[1].get_date()
        try:
            self._lista.adicionar_item(descr, data_prev)
        except DescrInvalida:
            pass

        self._campos[0].delete(0, END)
        self._campos[1].set_date(date.today())

    

class PopUpExc(Toplevel):

    def __init__(self, bg, width, height, gap_r, gap_c, lista:Lista, app):
        super().__init__(bg=bg, takefocus=True, )
        self.geometry(f"{width}x{height}")
        self.rowconfigure((0, 1, 2),pad=gap_r)
        self.columnconfigure((0, 1),pad=gap_c)
        self.resizable(False, False)
        self._lista = lista
        self._campos = []
        self._app=app
        self._width=width
        self._height=height

    def inicializar(self):

        self._item_selecionado = self._app.ITEM_SELECIONADO

        if not self._item_selecionado:
            self.destroy()

        else:

            fonte = font.Font(family=Fontes.ITENS_LISTA[0], size=Fontes.ITENS_LISTA[1])
            
            Label(self, text="Tem certeza que deseja excluir este item?", font=fonte, foreground="black", bg=self["bg"]).grid(column=0, row=0, columnspan=2)

            icone_path=Path("fonte/apresentacao/recursos/excluir_aviso.png")
            icone=Image.open(icone_path)
            self._icone=ImageTk.PhotoImage(icone)
            canvas=Canvas(self, bg=self["bg"], highlightthickness=0, height=100)
            canvas.grid(column=0, row=1, columnspan=2, sticky=NSEW)
            canvas.create_image(self._width//2,64,image=self._icone, anchor=CENTER)
            Button(self, text="Excluir", command=self._excluir, font=fonte).grid(row=2, column=1,)
            Button(self, text="Cancelar", command=self._destruir, font=fonte).grid(row=2, column=0,)

            self.update()
            self.grab_set()

    def _excluir(self):
        self._lista.excluir_item()
        self.destroy()
        self._app.ITEM_SELECIONADO=None

    def _destruir(self):
        self.destroy()

class PopUpAlt(Toplevel):

    def __init__(self, bg, width, height, gap_r, gap_c, lista:Lista, app):
        super().__init__(bg=bg, takefocus=True, )
        self.geometry(f"{width}x{height}")
        self.rowconfigure((0, 1, 2),pad=gap_r)
        self.columnconfigure((0, 1),pad=gap_c)
        self.resizable(False, False)
        self._lista = lista
        self._campos = []
        self._app=app
        

    def inicializar(self):

        self._item_selecionado = self._app.ITEM_SELECIONADO

        if not self._item_selecionado:
            self.destroy()

        else:

            descr_orig=self._item_selecionado.get_descr()
            data_prev_orig=self._item_selecionado.get_data_prev()

            fonte = font.Font(family=Fontes.ITENS_LISTA[0], size=Fontes.ITENS_LISTA[1])

            Label(self, text="Descrição:", font=fonte, foreground="black", bg=self["bg"]).grid(column=0, row=0)
            self._campos.append(Entry(self,width=30))
            self._campos[0].insert(0, descr_orig)
            self._campos[0].grid(column=1, row=0)

            Label(self, text="Prazo final:", font=fonte, foreground="black", bg=self["bg"]).grid(column=0, row=1)
            self._campos.append(DateEntry(self, textvariable=""))
            self._campos[1].set_date(data_prev_orig)
            self._campos[1].grid(column=1, row=1)


            Button(self, text="Alterar", command=self._alterar, font=fonte, width=20).grid(row=2, column=1,)
            Button(self, text="Cancelar", command=self._destruir, font=fonte).grid(row=2, column=0,)

            self.grab_set()

    def _alterar(self):
        descr=self._campos[0].get()
        data_prev=self._campos[1].get_date()
        self._lista.alterar_item(descr, data_prev)
        self._app.ITEM_SELECIONADO=None
        self.destroy()

    def _destruir(self):
        self.destroy()