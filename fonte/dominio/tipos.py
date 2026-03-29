from fonte.dominio.excecoes import *
from datetime import date

class Descr(str):
    def __new__(cls, string_descr:str):
        if not string_descr:
            raise DescrInvalida("A descrição não pode ser vazia.", string_descr)
        elif len(string_descr) > 60:
            raise DescrInvalida("A descrição não pode exceder 60 caracteres.", string_descr)
        return super().__new__(cls, string_descr)