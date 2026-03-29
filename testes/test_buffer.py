import pytest
from infraestrutura.buffer import Buffer
from fonte.dominio.excecoes import BufferVazio

def test_buffer_vazio():

    buffer = Buffer(4)

    def funcao_de_teste(conn):
        pass

    for i in range(3):
        if not(buffer.get(i)):
            assert True


    for i in range(3):
        buffer.add(funcao_de_teste, 1)

    buffer.esvaziar_buffer(1)

    for i in range(3):

        if not(buffer.get(i)):
            assert True

def test_add():

    buffer = Buffer(4)

    def funcao_de_teste(argumento_1, argumento_2):
        pass

    for i in range(3):
        buffer.add(funcao_de_teste, 1, 1)

    for i in range(3):
        if buffer.get(i):
            assert True

def test_esvaziar_buffer():

    buffer = Buffer(4)

    def funcao_de_teste(argumento_1, argumento_2):
        assert (argumento_1+argumento_2)==5

    buffer.add(funcao_de_teste, 1, 2, 3)
    buffer.add(funcao_de_teste, 1, 1, 4)
    buffer.add(funcao_de_teste, 1, argumento_1=5, argumento_2=0)

def test_esvaziar_vazio():

    buffer = Buffer(4)

    with pytest.raises(BufferVazio):
        buffer.esvaziar_buffer(1)

    def funcao_de_teste(conn):
        pass

    for i in range(3):
        buffer.add(funcao_de_teste,1)

    buffer.esvaziar_buffer(1)

    with pytest.raises(BufferVazio):
        buffer.esvaziar_buffer(1)

    for i in range(4):
        buffer.add(funcao_de_teste,1)

    with pytest.raises(BufferVazio):
        buffer.esvaziar_buffer(1)
