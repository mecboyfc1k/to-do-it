class DescrInvalida(Exception):
    def __init__(self, erro:str, valor_recebido:str):
        mensagem = f"{erro} Valor recebido: '{valor_recebido}'"
        super().__init__(mensagem)

    def __str__(self):
        return super().__str__()


class TarefaInvalida(Exception):
    def __init__(self, mensagem=None):
        mensagem = f"Tarefa inválida. {mensagem}" if mensagem else "Tarefa inválida."
        super().__init__(mensagem)

    def __str__(self):
        return super().__str__()
    
class BufferVazio(Exception):
    def __init__(self, mensagem=None):
        mensagem = f"O buffer já está vazio. {mensagem}" if mensagem else "O buffer já está vazio"
        super().__init__(mensagem)

    def __str__(self):
        return super().__str__()
    
class BufferCheio(Exception):
    def __init__(self, mensagem=None):
        mensagem = f"O buffer já está cheio. {mensagem}" if mensagem else "O buffer já está cheio"
        super().__init__(mensagem)

    def __str__(self):
        return super().__str__()