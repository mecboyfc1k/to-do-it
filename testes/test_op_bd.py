import pytest
from fonte.infraestrutura import operacoes_bd as op_bd

from fonte.dominio.tarefa import Tarefa
from pathlib import Path
from datetime import date,datetime
import sqlite3


class TestCriacaoDoBD:

    def test_criar_arq_bd(self, tmp_path):

        from fonte.aplicacao import operacoes

        caminho_bd = tmp_path/"tarefas.db"
        with op_bd.conectar_bd(caminho_bd):
            assert caminho_bd.exists()


    def test_criar_tabela_tarefas(self, tmp_path):

        from fonte.aplicacao import operacoes

        caminho_bd = Path(tmp_path/"tarefas.db")

        conn = op_bd.conectar_bd(caminho_bd)
        op_bd.criar_tabela(conn)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Tarefas'")
        tabela = cursor.fetchone()

        conn.close()

        assert tabela is not None

    def test_dominio_da_tabela_tarefas(self, tmp_path):

        from fonte.aplicacao import operacoes

        caminho_bd = tmp_path/"tarefas.db"

        conn = op_bd.conectar_bd(caminho_bd)
        op_bd.criar_tabela(conn)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(Tarefas)")
        colunas = cursor.fetchall()
        nomes_colunas = [coluna[1] for coluna in colunas]
        constraints = [colunas[0][5]] + [coluna[3] for coluna in colunas[1:]]
        
        conn.close()

        assert nomes_colunas == ["id", "descr", "data_prev", "concluida"], f"Colunas incorretas: {nomes_colunas}"

        assert constraints == [1, 1, 1, 1], f"Constraints incorretas: {constraints}"


class TestOperacoesDoBD:


    def test_inserir_tarefa(self, tmp_path, valores_validos_testes):

        from fonte.aplicacao import operacoes

        caminho_bd = Path(tmp_path/"tarefas.db").absolute()

        operacoes.inicializar_bd(caminho_bd)
        conn=operacoes._criar_conexao()

        tarefa=Tarefa(valores_validos_testes["descr"][0], date(*valores_validos_testes["data_tarefa"]["data_futura"][0]))

        op_bd.inserir_tarefa(conn, tarefa.id, tarefa.descr, tarefa.data_prev, tarefa.concluida)

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tarefas WHERE id=?", (tarefa.id,))
        resultado = cursor.fetchone()
        data_prev_dt = datetime.strptime(resultado[2], "%Y-%m-%d")
        data_prev = date(data_prev_dt.year, data_prev_dt.month, data_prev_dt.day)
        conn.close()

        assert resultado is not None
        assert resultado[0] == tarefa.id
        assert resultado[1] == tarefa.descr
        assert data_prev == tarefa.data_prev
        assert resultado[3] == tarefa.concluida


    def test_consulta_tudo_valida(self,tmp_path, valores_validos_testes):

        from fonte.aplicacao import operacoes
        
        caminho_bd = tmp_path/"tarefa.db"
        operacoes.inicializar_bd(caminho_bd)
        conn = operacoes._criar_conexao()

        tarefa_1=operacoes.criar_tarefa(valores_validos_testes["descr"][0], date(*valores_validos_testes["data_tarefa"]["data_futura"][0]))
        tarefa_2=operacoes.criar_tarefa(valores_validos_testes["descr"][1], date(*valores_validos_testes["data_tarefa"]["data_futura"][1]))

        operacoes.BUFFER.esvaziar_buffer(conn)

        resultados = op_bd.consultar_tudo(conn, "Tarefas")

        data_prev_dt_1 = datetime.strptime(resultados[0][2], "%Y-%m-%d")
        data_prev_1 = date(data_prev_dt_1.year, data_prev_dt_1.month, data_prev_dt_1.day)

        data_prev_dt_2 = datetime.strptime(resultados[1][2], "%Y-%m-%d")
        data_prev_2 = date(data_prev_dt_2.year, data_prev_dt_2.month, data_prev_dt_2.day)
        conn.close()

        assert tarefa_1.id == resultados[0][0], "id de tarefa_1 apresenta inconsistências"
        assert tarefa_1.descr == resultados[0][1], "descr de tarefa_1 apresenta inconsistências"
        assert tarefa_1.data_prev == data_prev_1, "data_prev de tarefa_1 apresenta inconsistências"
        assert tarefa_1.concluida == resultados[0][3], "concluida de tarefa_1 apresenta inconsistências"

        assert tarefa_2.id == resultados[1][0], "id de tarefa_2 apresenta inconsistências"
        assert tarefa_2.descr == resultados[1][1], "descr de tarefa_2 apresenta inconsistências"
        assert tarefa_2.data_prev == data_prev_2, "data_prev de tarefa_2 apresenta inconsistências"
        assert tarefa_2.concluida == resultados[1][3], "concluida de tarefa_2 apresenta inconsistências"

    
    def test_detector_sql_injection(self, tmp_path, valores_validos_testes):

        from fonte.aplicacao import operacoes

        caminho_bd = tmp_path/"tarefas.db"

        operacoes.inicializar_bd(caminho=Path(caminho_bd).resolve())
        conn = operacoes._criar_conexao()
        operacoes.criar_tarefa(valores_validos_testes["descr"][0], date(*valores_validos_testes["data_tarefa"]["data_futura"][0]))

        with pytest.raises(ValueError,match="Nome de tabela inválido"):
            op_bd.consultar_tudo(conn, "nome-invalido")


    def test_alteracao_valida(self,tmp_path,valores_validos_testes):

        from fonte.aplicacao import operacoes
        
        caminho_bd = tmp_path/"tarefa.db"
        operacoes.inicializar_bd(caminho=Path(caminho_bd).resolve())
        conn = operacoes._criar_conexao()

        tarefa_1 = operacoes.criar_tarefa(valores_validos_testes["descr"][0], valores_validos_testes["data_tarefa"]["data_futura"][0])

        tarefa_2 = operacoes.criar_tarefa(valores_validos_testes["descr"][1], valores_validos_testes["data_tarefa"]["data_futura"][1])


        operacoes.BUFFER.esvaziar_buffer(conn)

        op_bd.alterar_tarefa(conn, tarefa_1.id, tarefa_2.descr, tarefa_2.data_prev, tarefa_2.concluida)

        resultados = operacoes.recuperar_tarefas()
        
        assert resultados[1].descr == tarefa_2.descr, "A alteração do nome não foi realizada corretamente."
        assert resultados[1].data_prev == tarefa_2.data_prev, "A alteração da data não foi realizada corretamente."


    def valores_validos_testes(self,tmp_path,valores_validos_testes):

        from fonte.aplicacao import operacoes

        caminho_bd = tmp_path/"tarefas.db"
        conn = operacoes.criar_conexao(caminho_bd=Path(caminho_bd).resolve())
       
        tarefa_1 = Tarefa(valores_validos_testes["descr"][0], valores_validos_testes["data_tarefa"]["data_futura"][0])

        operacoes.criar_tarefa(tarefa_1)

        op_bd.excluir_tarefa(conn, tarefa_1.id)

        resultados = operacoes.recuperar_tarefas("Tarefas")

        assert len(resultados) == 0, "A exclusão da tarefa não foi realizada corretamente."