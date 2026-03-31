from tkinter import *
from tkinter import Tk
from fonte.apresentacao.botao_arrendodado import BotaoArredondado

class PainelBotoes(Frame):

    PAINEL_PAD=20

    def __init__(self, master, raio_bt, gap, bg, altura, *args, bt_ck_cr, bt_hv_cr):
        super().__init__(master)

        self._bt_ck_cr = bt_ck_cr
        self._bt_hv_cr = bt_hv_cr
        self._espacamento=gap
        self._bt_descr=args
        self._bt_raio=raio_bt
        self._botoes=[]
        self.configure(height=altura, width=20, padx=PainelBotoes.PAINEL_PAD, pady=PainelBotoes.PAINEL_PAD, bg=bg)

    def inicializar(self):

        self.pack(anchor='center', side='bottom', padx=PainelBotoes.PAINEL_PAD, pady=PainelBotoes.PAINEL_PAD)

        i=0

        for botao in self._bt_descr:
            self._botoes.append(BotaoArredondado(self, self._bt_raio, botao[0], botao[1], botao[2], *botao[3], bt_hv_cr=self._bt_hv_cr, bt_ck_cr=self._bt_ck_cr))
            self._botoes[i].inicializar()
            i+=1
            