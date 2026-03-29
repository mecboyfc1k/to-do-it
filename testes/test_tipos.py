import pytest
from fonte.dominio.tipos import *
from fonte.dominio.excecoes import *

def test_excecoes_tipos(valores_invalidos_testes):
    
    with pytest.raises(DescrInvalida):
        Descr(valores_invalidos_testes["descr"]["vazio"])

    with pytest.raises(DescrInvalida):
        Descr(valores_invalidos_testes["descr"]["estouro"])

def test_tipos_validos(valores_validos_testes):

    try:
        descr = Descr(valores_validos_testes["descr"][0])
        valores_teste_data = valores_validos_testes["data_tarefa"]["data_futura"][0]
    except Exception as e:
        pytest.fail(f"Tipos válidos lançaram uma exceção: {e}")