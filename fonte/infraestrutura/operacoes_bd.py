import sqlite3 as conector
from datetime import date
from pathlib import Path


def conectar_bd(caminho:Path):

    return conector.connect(caminho)

def criar_tabela(conn:conector.Connection):
    
    cursor = conn.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Tarefas (id TEXT PRIMARY KEY,
                    descr TEXT NOT NULL,
                    data_prev TEXT NOT NULL,
                    concluida BOOLEAN NOT NULL)
                    ''')
    
    conn.commit()

def consultar_tudo(conn:conector.Connection, tabela: str):
    if not tabela.isidentifier():
        raise ValueError("Nome de tabela inválido")

    comando_sql = f"SELECT * FROM {tabela}"
    cursor = conn.cursor()
    resultado = cursor.execute(comando_sql)

    return resultado.fetchall()

def alterar_tarefa(conn:conector.Connection, id, novo_descr=None, nova_data:date=None, nova_concluida=None):
    campos_alterar=[]
    valores=[]

    if novo_descr:
        campos_alterar.append("descr = ?")
        valores.append(novo_descr)
    if nova_data:
        campos_alterar.append("data_prev = ?")
        nova_data=nova_data.strftime("%Y-%m-%d")
        valores.append(nova_data)
    if nova_concluida is not None:
        campos_alterar.append("concluida = ?")
        valores.append(nova_concluida)

    if not campos_alterar:
        return
    
    valores.append(id)
    comando_sql = f"UPDATE Tarefas SET {', '.join(campos_alterar)} WHERE id = ?"

    cursor = conn.cursor()
    cursor.execute(comando_sql, tuple(valores))
    conn.commit()

def excluir_tarefa(conn, id):
    cursor = conn.cursor()
    cursor.execute('''
                   DELETE FROM Tarefas WHERE id = ?
                    ''',
                    (id,))
    conn.commit()

def inserir_tarefa(conn, id, descr, data_prev:date, concluida):
    cursor = conn.cursor()
    data_prev=data_prev.strftime("%Y-%m-%d")
    cursor.execute('''
                    INSERT INTO Tarefas (id, descr, data_prev, concluida)
                    VALUES (?, ?, ?, ?)
                    ''', (id, descr, data_prev, concluida))
    conn.commit()

def fechar_conexao(conn:conector.Connection):
    conn.close()