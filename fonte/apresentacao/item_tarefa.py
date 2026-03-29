from tkinter import *
from fonte.apresentacao.listas import *
from tkinter import Tk, font
from fonte.aplicacao import operacoes
from fonte.apresentacao.fontes import Fontes
from pathlib import Path
from PIL import Image, ImageTk
from fonte.dominio.tarefa import Tarefa


class ItemTarefa(Frame):

    H=50
    PADX = 2
    PADY=2

    def __init__(self, master, app, bg, l_2, marcado=False):
        super().__init__(master=master)
        self._bg_cr=bg

        if marcado:
            self._tarefa_concluida=IntVar(value=1)
        else:
            self._tarefa_concluida=IntVar(value=0)

        self._lista_vizinha = l_2

        self.bind("<Button-1>", self._ao_clicar)

        self._app=app


    def criar_tarefa(self, descr = None, data_prev = None, tarefa:Tarefa = None):
        if not tarefa:
            self._tarefa = operacoes.criar_tarefa(descr, data_prev)
        else:
            self._tarefa = tarefa

        self.configure(bg=self._bg_cr, height=ItemTarefa.H, width=20)

        self._descr_label = Label(self,text=self._tarefa.descr, font=font.Font(family=Fontes.ITENS_LISTA[0], size=Fontes.ITENS_LISTA[1]), fg="black", bg=self["bg"])
        self._descr_label.bind("<Button-1>", self._ao_clicar)
        data = str(self._tarefa.data_prev)

        if self._tarefa.atrasada:
            self._data_label=Label(self,text=data, font=font.Font(family=Fontes.ITENS_LISTA[0], size=Fontes.ITENS_LISTA[1]), fg="red", bg=self["bg"])
        else:
            self._data_label=Label(self,text=data, font=font.Font(family=Fontes.ITENS_LISTA[0], size=Fontes.ITENS_LISTA[1]), fg="black", bg=self["bg"])

        self._data_label.bind("<Button-1>", self._ao_clicar)

        path_marcado = Path("fonte/apresentacao/recursos/botoes/check.png").absolute()
        path_desmarcado = Path("fonte/apresentacao/recursos/botoes/uncheck.png").absolute()

        self._marcado_ic = Image.open(path_marcado)
        self._marcado_ic = ImageTk.PhotoImage(self._marcado_ic)

        self._desmarcado_ic = Image.open(path_desmarcado)
        self._desmarcado_ic = ImageTk.PhotoImage(self._desmarcado_ic)


        marcador = Checkbutton(self, command=self._marcacao_tarefa, indicatoron=0, image=self._desmarcado_ic, selectimage=self._marcado_ic, selectcolor=self["bg"], borderwidth=0, relief="flat", bg=self["bg"], highlightthickness=0,variable=self._tarefa_concluida,offvalue=0, onvalue=1)

        marcador.grid(column=0, row=0)
        self._descr_label.grid(column=1, row=0)
        self._data_label.grid(column=2, row=0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=8)
        self.columnconfigure(2, weight=2)

        self.pack(anchor="nw", side="top", fill="x")

    def destruir_tarefa(self):
        operacoes.excluir_tarefa(self._tarefa.id)
        self.destroy()
        


    def alterar_tarefa(self, descr, data_prev):

        operacoes.alterar_tarefa(self._tarefa, descr, data_prev)

        data = str(self._tarefa.data_prev)

        if self._tarefa.atrasada:
            self._data_label.configure(text=data, fg="red")
        else:
            self._data_label.configure(text=data, fg="black")

        self._descr_label.configure(text=self._tarefa.descr)


    def _marcacao_tarefa(self):

        if self._tarefa_concluida.get()==1:
            self._lista_vizinha.adicionar_item(tarefa=self._tarefa, marcado=True)
            operacoes.marcar_tarefa(self._tarefa)
        else:
            self._lista_vizinha.adicionar_item(tarefa=self._tarefa, marcado=False)
            operacoes.desmarcar_tarefa(self._tarefa)

        if self._app.ITEM_SELECIONADO == self:
            self._app.ITEM_SELECIONADO = None
        self.destruir_tarefa()

    def _ao_clicar(self, event):
        self._app.ITEM_SELECIONADO = self
        print(self._app.ITEM_SELECIONADO)

    def get_descr(self):
        return self._tarefa.descr
    
    def get_data_prev(self):
        return self._tarefa.data_prev