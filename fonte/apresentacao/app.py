from tkinter import *
from tkinter import Tk
from fonte.apresentacao.paleta import Cores as cor
from fonte.apresentacao.barra_superior import BarraSuperior
from fonte.apresentacao.painel_botoes import PainelBotoes
from fonte.apresentacao.listas import *
from fonte.apresentacao.popups import *
from fonte.aplicacao import operacoes
from PIL import Image, ImageTk
from fonte.dominio.tarefa import Tarefa


class App(Tk):

    BARRA_SUP_CR = cor.VERDE_EUCALIPTO
    BG_CR = cor.VERDE_CHA_VERDE
    BOTAO_CR1 = cor.AZUL_HORTENSIA
    PAINEL_BT_BG = cor.VERDE_LIMAO
    LISTA_BG_CR = cor.VERDE_LIMAO
    LISTA_IT_BG_CR = cor.VERDE_LIMAO
    LISTA_IT_HV_CR = cor.VERDE_CHA_VERDE
    LISTA_IT_CK_CR = cor.VERDE_EUCALIPTO
    LISTA_IT_RL_CR = cor.VERDE_OLIVA
    POPUP_BG = cor.VERDE_EUCALIPTO

    ITEM_SELECIONADO=None


    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.configure(bg=App.BG_CR, height=900, width=1000)
    

    def _construir(self):

        operacoes.inicializar_bd()

        BarraSuperior(self, App.BARRA_SUP_CR).inicializar()

        l_e=ListaE(self, App.LISTA_BG_CR, App.LISTA_IT_BG_CR, self, hover_bg=App.LISTA_IT_HV_CR, cr_press=App.LISTA_IT_CK_CR, cr_release=App.LISTA_IT_RL_CR)
        l_d=ListaD(self, App.LISTA_BG_CR, App.LISTA_IT_BG_CR, self, hover_bg=App.LISTA_IT_HV_CR, cr_press=App.LISTA_IT_CK_CR, cr_release=App.LISTA_IT_RL_CR)

        l_e.ligar_lista_vizinha(l_d)
        l_d.ligar_lista_vizinha(l_e)


        icon_bt_add=Image.open(Path("./fonte/apresentacao/recursos/botoes/criar.png").absolute())
        icon_bt_add=ImageTk.PhotoImage(icon_bt_add)

        icon_bt_alt=Image.open(Path("./fonte/apresentacao/recursos/botoes/editar.png").absolute())
        icon_bt_alt=ImageTk.PhotoImage(icon_bt_alt)

        icon_bt_exc=Image.open(Path("./fonte/apresentacao/recursos/botoes/apagar.png").absolute())
        icon_bt_exc=ImageTk.PhotoImage(icon_bt_exc)

        botoes=((App.BOTAO_CR1, icon_bt_add, self._criar_popup_criar, (App.POPUP_BG, 400, 150, 20, 20, l_e)),
                (App.BOTAO_CR1, icon_bt_alt, self._criar_popup_alterar, (App.POPUP_BG, 400, 150, 20, 20, l_e, self)),
                (App.BOTAO_CR1, icon_bt_exc, self._criar_popup_excluir, (App.POPUP_BG, 400, 250, 20, 20, l_e, self)))

        PainelBotoes(self, 50, 10, App.PAINEL_BT_BG, 100, *botoes).inicializar()

        l_e.inicializar()
        l_d.inicializar()

        self._recuperar(l_e, l_d)

        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)

    def _ao_fechar(self):
        operacoes.salvar_tarefas()
        self.destroy()

    def _recuperar(self, lista_andamento:Lista, lista_concluidas:Lista):
        tarefas = operacoes.recuperar_tarefas()

        if tarefas:
            for tarefa in tarefas:
                if tarefa.concluida:
                    lista_concluidas.adicionar_item(tarefa=tarefa, marcado=True)
                else:
                    lista_andamento.adicionar_item(tarefa=tarefa, marcado=False)

    def _criar_popup_criar(self, bg, width, height, gap_r, gap_c, lista):
        pop=PopUpCriar(bg, width, height, gap_r, gap_c, lista)
        pop.inicializar()

    def _criar_popup_alterar(self, bg, width, height, gap_r, gap_c, lista, app):
        pop=PopUpAlt(bg, width, height, gap_r, gap_c, lista, app)
        pop.inicializar()

    def _criar_popup_excluir(self, bg, width, height, gap_r, gap_c, lista, app):
        pop=PopUpExc(bg, width, height, gap_r, gap_c, lista, app)
        pop.inicializar()

    def iniciar(self):
        self.update()
        self._construir()
        self.mainloop()