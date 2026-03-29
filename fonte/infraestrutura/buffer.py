from typing import Callable
from fonte.dominio.excecoes import BufferVazio


class Buffer:

    def __init__(self, tamanho, ticks_esvaziamento=None):
        self._tamanho = tamanho
        self._buffer = [None for i in range(tamanho)]

    def add(self, chamavel:Callable, conn, *args, **kwargs):
        funcao = (chamavel, (args, kwargs,),)

        for i in range(self._tamanho):
            if not(self._buffer[i]):
                self._buffer[i] = funcao
                break

        if not(None in self._buffer):
            self.esvaziar_buffer(conn)
            


    def esvaziar_buffer(self, conn):

        if not(self._buffer[0]):

            raise(BufferVazio)
        
        for i in range(self._tamanho):

            if not self._buffer[i]:
                break

            self._buffer[i][0](conn, *self._buffer[i][1][0], **self._buffer[i][1][1])
            self._buffer[i] = None

    def get(self, indice):
        return self._buffer[indice]