from tkinter import *
from fonte.apresentacao.listas import *
from tkinter import Tk, font
from fonte.aplicacao import operacoes
from fonte.apresentacao.fontes import Fontes
from pathlib import Path
from PIL import Image, ImageTk
from fonte.dominio.tarefa import Tarefa


class ItemTarefa(Frame):

    H=30
    PADX = 2
    PADY=2

    def __init__(self, master, app, bg, l_2, hover_bg="", marcado=False, cr_press = "", cr_release = ""):
        super().__init__(master=master)
        self.pack_propagate(False)
        self.grid_propagate(False)

        self._bg_cr=bg

        if marcado:
            self._tarefa_concluida=IntVar(value=1)
        else:
            self._tarefa_concluida=IntVar(value=0)

        self._lista_vizinha = l_2

        self.bind("<Button-1>", self._ao_clicar, "+")
        self.bind("<ButtonRelease-1>", self._ao_desclicar, "+")
        self.bind("<Enter>", self._on_enter, "+")
        self.bind("<Leave>", self._on_leave, "+")

        self._app=app
        self._selecionado=False
        self._hover_ativo=False
        self._hover_bg = hover_bg
        self._bg = bg
        self._cr_press = cr_press
        self._cr_release = cr_release


    def criar_tarefa(self, descr = None, data_prev = None, tarefa:Tarefa = None):
        if not tarefa:
            self._tarefa = operacoes.criar_tarefa(descr, data_prev)
        else:
            self._tarefa = tarefa

        self.configure(bg=self._bg_cr, height=ItemTarefa.H, width=20)
        self.pack_propagate(False)

        if self._tarefa.concluida:
            self._descr_label = Label(self,text=self._tarefa.descr, font=font.Font(family=Fontes.ITENS_LISTA[0], size=Fontes.ITENS_LISTA[1]), fg="gray", bg=self["bg"], height=1)

        else:

            self._descr_label = Label(self,text=self._tarefa.descr, font=font.Font(family=Fontes.ITENS_LISTA[0], size=Fontes.ITENS_LISTA[1]), fg="black", bg=self["bg"], height=1)

        self._descr_label.bind("<Button-1>", self._ao_clicar,"+")
        self._descr_label.bind("<ButtonRelease-1>", self._ao_desclicar, "+")
        self._descr_label.bind("<Enter>", self._on_enter, "+")
        self._descr_label.bind("<Leave>", self._on_leave, "+")
        data = str(self._tarefa.data_prev)

        if self._tarefa.atrasada:
            self._data_label=Label(self,text=data, font=font.Font(family=Fontes.ITENS_LISTA[0], size=Fontes.ITENS_LISTA[1]), fg="red", bg=self["bg"])
        elif self._tarefa.concluida:
            self._data_label=Label(self,text=data, font=font.Font(family=Fontes.ITENS_LISTA[0], size=Fontes.ITENS_LISTA[1]), fg="gray", bg=self["bg"])
        else:
            self._data_label=Label(self,text=data, font=font.Font(family=Fontes.ITENS_LISTA[0], size=Fontes.ITENS_LISTA[1]), fg="black", bg=self["bg"])

        self._data_label.bind("<Button-1>", self._ao_clicar, "+")
        self._data_label.bind("<ButtonRelease-1>", self._ao_desclicar, "+")
        self._data_label.bind("<Enter>", self._on_enter, "+")
        self._data_label.bind("<Leave>", self._on_leave, "+")

        path_marcado = Path("fonte/apresentacao/recursos/botoes/check.png").absolute()
        path_desmarcado = Path("fonte/apresentacao/recursos/botoes/uncheck.png").absolute()

        self._marcado_ic = Image.open(path_marcado)
        self._marcado_ic = ImageTk.PhotoImage(self._marcado_ic)

        self._desmarcado_ic = Image.open(path_desmarcado)
        self._desmarcado_ic = ImageTk.PhotoImage(self._desmarcado_ic)


        self._marcador = Checkbutton(self, command=self._marcacao_tarefa, indicatoron=0, image=self._desmarcado_ic, selectimage=self._marcado_ic, selectcolor=self["bg"], borderwidth=0, relief="flat", bg=self["bg"], highlightthickness=0,variable=self._tarefa_concluida,offvalue=0, onvalue=1)

        self._marcador.grid(column=0, row=0)
        self._descr_label.grid(column=1, row=0)
        self._data_label.grid(column=2, row=0)

        self.columnconfigure(1, weight=8)
        self.columnconfigure(2, weight=2)

        self.pack(anchor="nw", side="top", fill="x")

    def destruir_tarefa(self):
        operacoes.excluir_tarefa(self._tarefa.id)
        self.resetar_selecao()
        self.destroy()
        
    def destruir_item(self):
        self.destroy()

    def alterar_tarefa(self, descr, data_prev):

        operacoes.alterar_tarefa(self._tarefa, descr, data_prev)

        data = str(self._tarefa.data_prev)

        if self._tarefa.atrasada:
            self._data_label.configure(text=data, fg="red")
        else:
            self._data_label.configure(text=data, fg="black")

        self._descr_label.configure(text=self._tarefa.descr)
        self.resetar_selecao()


    def _marcacao_tarefa(self):

        if self._tarefa_concluida.get()==1:
            operacoes.marcar_tarefa(self._tarefa)
            self._lista_vizinha.adicionar_item(tarefa=self._tarefa, marcado=True)
            
        else:
            operacoes.desmarcar_tarefa(self._tarefa)
            self._lista_vizinha.adicionar_item(tarefa=self._tarefa, marcado=False)
            

        if self._app.ITEM_SELECIONADO == self:
            self.resetar_selecao()
            self._app.ITEM_SELECIONADO = None
        self.destruir_item()

    def _ao_clicar(self, event):
        if self._app.ITEM_SELECIONADO != self:
            self.configure(bg=self._cr_press)
            self._data_label.configure(bg=self._cr_press)
            self._descr_label.configure(bg=self._cr_press)
            self._marcador.configure(bg=self._cr_press, selectcolor=self._cr_press)
            if self._app.ITEM_SELECIONADO:
                self._app.ITEM_SELECIONADO.resetar_selecao()

    def _ao_desclicar(self, event):
        if self._app.ITEM_SELECIONADO != self:
            self.configure(bg=self._cr_release)
            self._data_label.configure(bg=self._cr_release)
            self._descr_label.configure(bg=self._cr_release)
            self._marcador.configure(bg=self._cr_release, selectcolor=self._cr_release)
            self._app.ITEM_SELECIONADO = self
            self._selecionado=True

    def get_descr(self):
        return self._tarefa.descr
    
    def get_data_prev(self):
        return self._tarefa.data_prev
    
    def _on_enter(self, event):
        if not(self._selecionado) and self._hover_bg:
            self.configure(bg=self._hover_bg)
            self._data_label.configure(bg=self._hover_bg)
            self._descr_label.configure(bg=self._hover_bg)
            self._marcador.configure(bg=self._hover_bg, selectcolor=self._hover_bg)

    def _on_leave(self, event):
        if not(self._selecionado):
            self.configure(bg=self._bg)
            self._data_label.configure(bg=self._bg)
            self._descr_label.configure(bg=self._bg)
            self._marcador.configure(bg=self._bg, selectcolor=self._bg)

    def resetar_selecao(self):
        self._selecionado=False
        self.configure(bg=self._bg_cr)
        self._data_label.configure(bg=self._bg_cr)
        self._descr_label.configure(bg=self._bg_cr)
        self._marcador.configure(bg=self._bg_cr, selectcolor=self._bg_cr)