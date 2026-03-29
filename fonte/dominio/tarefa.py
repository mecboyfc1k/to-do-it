from fonte.dominio.excecoes import *
from fonte.dominio.tipos import *
from datetime import date
import uuid

class Tarefa:

    def __init__(self, descr:Descr, data_prev:date=None):

        if not data_prev:
            self._data_prev = date.today()
        elif not isinstance(data_prev, date):
            raise TarefaInvalida("data_prev deve ser do tipo date.")
        else:
            self._data_prev = data_prev

        try:
            self._descr = Descr(descr)
        except DescrInvalida as e:
            raise TarefaInvalida(f"descr inválida. {e}")
        
        if self._data_prev < date.today():
            self._atrasada = True
        else:
            self._atrasada = False
        
        self._concluida = False

        self._id = str(uuid.uuid4())
    
    @property
    def id(self):
        return self._id

    @property
    def descr(self):
        return self._descr
    
    @descr.setter
    def descr(self, value):
        try:
            self._descr = Descr(value)
        except DescrInvalida as e:
            raise TarefaInvalida(f"descr inválida. {e}")
        
    @property
    def data_prev(self):
        return self._data_prev
    
    @data_prev.setter
    def data_prev(self, value:date):
        if not isinstance(value, date):
            raise TarefaInvalida("data_prev deve ser do tipo date.")
        self._data_prev = value

        if self._data_prev < date.today():
            self._atrasada = True
        else:
            self._atrasada = False

    @property
    def atrasada(self):
        return self._atrasada
    
    @property
    def concluida(self):
        return self._concluida

    def marcar(self):
        self._concluida = True

    def desmarcar(self):
        self._concluida = False