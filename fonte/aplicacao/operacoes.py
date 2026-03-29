from fonte.dominio.tarefa import Tarefa
from fonte.dominio.tipos import *
from datetime import date, datetime
from pathlib import Path
from fonte.infraestrutura import operacoes_bd
from fonte.infraestrutura.buffer import Buffer

path = Path("fonte/infraestrutura/tarefas.db").absolute()
caminho_ut = None
BUFFER = Buffer(8)

def inicializar_bd(caminho:Path=None):

    global caminho_ut

    if not(caminho):
        caminho_ut = path
    else:
        caminho_ut = caminho

    conn=_criar_conexao()
    operacoes_bd.criar_tabela(conn)

    _fechar_conexao(conn)



def _criar_conexao():
    return operacoes_bd.conectar_bd(caminho_ut)


def _fechar_conexao(conn):
    operacoes_bd.fechar_conexao(conn)


def criar_tarefa(descr, data_prev):

    conn=_criar_conexao()

    if isinstance(data_prev, date):
        data_prevista=data_prev

    else:
        data_prevista=date(*data_prev)

    descricao=Descr(descr)

    tarefa=Tarefa(descricao, data_prevista)

    BUFFER.add(operacoes_bd.inserir_tarefa, conn, tarefa.id, tarefa.descr, tarefa.data_prev, tarefa.concluida)

    _fechar_conexao(conn)

    return tarefa



def marcar_tarefa(tarefa:Tarefa):
    tarefa.marcar()
    with _criar_conexao() as conn:
        BUFFER.add(operacoes_bd.alterar_tarefa, conn, tarefa.id, nova_concluida=True)



def desmarcar_tarefa(tarefa:Tarefa):
    tarefa.desmarcar()
    with _criar_conexao() as conn:
        BUFFER.add(operacoes_bd.alterar_tarefa, conn, tarefa.id, nova_concluida=False)
        

def alterar_tarefa(tarefa:Tarefa, descr=None, data_prev=None):
    tarefa.descr=descr
    tarefa.data_prev=data_prev

    with _criar_conexao() as conn:
        BUFFER.add(operacoes_bd.alterar_tarefa, conn, tarefa.id, descr, data_prev)

def recuperar_tarefas() -> list[Tarefa]:

    with _criar_conexao() as conn:

        if BUFFER.get(0):
            BUFFER.esvaziar_buffer(conn)

        resultados_consulta=operacoes_bd.consultar_tudo(conn, "Tarefas")
        resultados=[]

    for resultado in resultados_consulta:
        excluir_tarefa(resultado[0])

    with _criar_conexao() as conn:

        if BUFFER.get(0):
            BUFFER.esvaziar_buffer(conn)

    for i in range(len(resultados_consulta)):
        data_dt=datetime.strptime(resultados_consulta[i][2],"%Y-%m-%d")
        data = date(data_dt.year, data_dt.month, data_dt.day)
        resultados.append(criar_tarefa(resultados_consulta[i][1], data))
        if resultados_consulta[i][3]:
            marcar_tarefa(resultados[i])

    return resultados

def excluir_tarefa(id):
    with _criar_conexao() as conn:
        BUFFER.add(operacoes_bd.excluir_tarefa, conn, id)

def salvar_tarefas():

    with _criar_conexao() as conn:
        if BUFFER.get(0):
            BUFFER.esvaziar_buffer(conn)