from pytest import fixture
from datetime import date

@fixture
def valores_validos_testes():
    
    return {
        "descr": ["Uma tarefa que preciso fazer", "outra tarefa que preciso fazer"],
        "data_tarefa": {"data_futura": [(2026, date.today().month+1, 30), (2026, date.today().month+2, 15)], "data_passada": [(2020, 1, 1), (2020, 2, 1)]}
    }

@fixture
def valores_invalidos_testes():

    return {
        "descr": {"vazio": "", "estouro": "a" * 61},
        "data_tarefa": {}
    }