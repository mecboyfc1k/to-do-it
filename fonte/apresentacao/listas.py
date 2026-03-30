from tkinter import *
from tkinter import Tk
from apresentacao.item_tarefa import ItemTarefa
from fonte.apresentacao.botao_arrendodado import *
from fonte.dominio.tarefa import Tarefa
from PIL import Image, ImageTk
from pathlib import Path

class Lista(Frame):

    H = 300
    PADX=20
    PADY=20

    def __init__(self, master, bg, it_bg, app, hover_bg="", cr_press="", cr_release=""):
        super().__init__(master)
        self.configure(bg=bg, width=self.master.winfo_width()//2-Lista.PADX*2, height=Lista.H, padx=0, pady=0)
        self.pack_propagate(False)
        self._it_bg = it_bg
        self._hover_bg=hover_bg
        self._cr_press = cr_press
        self._cr_release = cr_release

        self.canvas = Canvas(self, bg=bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, side="left")

        self.scrollbar=Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(fill=Y, side=RIGHT)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollabe_frame=Frame(self.canvas, bg=bg, pady=5)

        self.canvas_window=self.canvas.create_window((0,0), window=self.scrollabe_frame,anchor=NW)

        self.scrollabe_frame.bind("<Configure>", self._ao_mudar_conteudo)
        self.canvas.bind("<Configure>", self._ao_mudar_canvas)

        self._app=app

    def ligar_lista_vizinha(self, l_v):
        self._lista_vizinha = l_v
        

    def _ao_mudar_canvas(self,event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _ao_mudar_conteudo(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def inicializar():
        pass

    def _ao_redimensionar(self, event):
        self.configure(width=self.master.winfo_width()//2-Lista.PADX*2)

    def adicionar_item(self, descr=None, data_prev=None, tarefa:Tarefa=None, marcado=False):
        if not tarefa:
            ItemTarefa(self.scrollabe_frame, self._app, self._it_bg, self._lista_vizinha, marcado=marcado, hover_bg=self._hover_bg, cr_press=self._cr_press, cr_release=self._cr_release).criar_tarefa(descr, data_prev)
        else:
            ItemTarefa(self.scrollabe_frame, self._app, self._it_bg, self._lista_vizinha, marcado=marcado, hover_bg=self._hover_bg, cr_press=self._cr_press, cr_release=self._cr_release).criar_tarefa(tarefa=tarefa)
    def alterar_item(self, descr, data_prev):
        self._app.ITEM_SELECIONADO.alterar_tarefa(descr, data_prev)

    def excluir_item(self):
        self._app.ITEM_SELECIONADO.destruir_tarefa()

class ListaE(Lista):

    def __init__(self, master, bg, it_bg, app, hover_bg="", cr_press="", cr_release=""):
        super().__init__(master,bg, it_bg, app, hover_bg=hover_bg, cr_press=cr_press, cr_release=cr_release)

    def inicializar(self):
        self.pack(anchor="w", side="left", fill="y", expand=True, padx=Lista.PADX, pady=Lista.PADY)
        self.master.bind("<Configure>", self._ao_redimensionar, "+")


class ListaD(Lista):

    def __init__(self, master, bg, it_bg, app, hover_bg="", cr_press="", cr_release=""):
        super().__init__(master, bg, it_bg, app, hover_bg=hover_bg, cr_press=cr_press, cr_release=cr_release)

    def inicializar(self):
        self.pack(anchor="e", side="right", fill="y", expand=True, padx=Lista.PADX, pady=Lista.PADY)
        self.master.bind("<Configure>", self._ao_redimensionar, "+")