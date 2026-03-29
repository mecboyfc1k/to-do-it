import pytest
from fonte.dominio.tarefa import Tarefa
from fonte.dominio.excecoes import *
from fonte.dominio.tipos import *

class TestCriacaoTarefa:

    def test_criar_tarefa_com_valores_validos(self, valores_validos_testes):
        try:
            data = date(*valores_validos_testes["data_tarefa"]["data_futura"][0])
            Tarefa(descr=valores_validos_testes["descr"][0], data_prev=data)
        except Exception as e:
            pytest.fail(f"Tipos válidos lançaram uma exceção: {e}")

        try:
            data = date(*valores_validos_testes["data_tarefa"]["data_futura"][0])
            Tarefa(descr=valores_validos_testes["descr"][0], data_prev=data)
        except Exception as e:
            pytest.fail(f"Tipos válidos lançaram uma exceção: {e}")

    def test_criar_tarefa_com_valores_invalidos(self, valores_invalidos_testes, valores_validos_testes):
        with pytest.raises(TarefaInvalida):
            data = date(*valores_validos_testes["data_tarefa"]["data_futura"][0])
            Tarefa(descr=valores_invalidos_testes["descr"]["vazio"], data_prev=data)

        with pytest.raises(TarefaInvalida):
            data = date(*valores_validos_testes["data_tarefa"]["data_futura"][0])
            Tarefa(descr=valores_invalidos_testes["descr"]["estouro"], data_prev=data)



class TestSettersTarefa:

    def test_setters_invalidos(self, valores_invalidos_testes, valores_validos_testes):
        
        tarefa = Tarefa(descr=valores_validos_testes["descr"][0], data_prev=date(*valores_validos_testes["data_tarefa"]["data_futura"][0]))

        with pytest.raises(TarefaInvalida):
            tarefa.descr = valores_invalidos_testes["descr"]["vazio"]

        with pytest.raises(TarefaInvalida):
            tarefa.descr = valores_invalidos_testes["descr"]["estouro"]

    def test_setters_validos(self, valores_validos_testes):

        tarefa = Tarefa(descr=valores_validos_testes["descr"][0], data_prev=date(*valores_validos_testes["data_tarefa"]["data_futura"][0]))

        try:
            tarefa.descr = valores_validos_testes["descr"][1]
        except Exception as e:
            pytest.fail(f"Setter descr com valor válido lançou uma exceção: {e}")

        try:
            tarefa.data_prev = date(*valores_validos_testes["data_tarefa"]["data_futura"][1])
        except Exception as e:
            pytest.fail(f"Setter data_prev com valor válido lançou uma exceção: {e}")

class TestMetodosTarefa:
    
    def test_marcar_desmarcar(self, valores_validos_testes):
        tarefa = Tarefa(descr=valores_validos_testes["descr"][0], data_prev=date(*valores_validos_testes["data_tarefa"]["data_futura"][0]))

        tarefa.marcar()
        assert tarefa.concluida == True, "O método marcar() não marcou a tarefa como concluída."

        tarefa.desmarcar()
        assert tarefa.concluida == False, "O método desmarcar() não desmarcou a tarefa como concluída."

    def test_atrasada(self, valores_validos_testes):
        tarefa = Tarefa(descr=valores_validos_testes["descr"][0], data_prev=date(*valores_validos_testes["data_tarefa"]["data_passada"][0]))
        assert tarefa.atrasada == True, "Tarefa com data passada não foi marcada como atrasada."

        tarefa = Tarefa(descr=valores_validos_testes["descr"][0], data_prev=date(*valores_validos_testes["data_tarefa"]["data_futura"][0]))
        assert tarefa.atrasada == False, "Tarefa com data futura foi marcada como atrasada."

