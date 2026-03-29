# MY-TD

Olá! Seja bem vindo ao meu projeto, o MY-TD

## Contexto

Movido pela necessidade de superar o desafio de um processo seletivo para uma vaga de tutor, me propus a fazer um app de to-do-it próprio. Reaproveitando um pouco dos conhecimentos que adquiri em projetos anteriores, me desafiei a fazer este app em 3 dias. Claro que não se trata de algo em sua versão final, mas se trata apenas de uma versão funcional, logo, em versões posteriores pretendo lançar uma release mais adequada em um pacote mais bem estruturado.

## Execução

Ao baixar os arquivos, o mais adequado é que se crie um venv na raiz do projeto. Para isso, digite `python -m venv caminho/para/a/raiz/do/projeto/venv` lembre-se de que a parte do 'venv' realmente é 'venv'.

Se preferir, pode navegar até a raiz do projeto usando o comando "cd" e executar `python -m venv ./venv`

Após isso, para instalar as dependências, preferi usar um pyproject.toml ao invés de requirements.txt, mas caso prefira assim, deixarei os dois.

Para instalar, basta executar `pip install -e .` na raiz do projeto, até prefiro assim para resolver as dependências de arquivos criados dentro do projeto mais facilmente.

Por fim, basta executar `python -m fonte`e aproveitar o app.

## Utilidade

Basicamente, é um app em que podemos criar tarefas com descrições curtas e datas. As operações suportadas são criação, alteração e exclusão de tarefas. Ao clicar no botão de seleção, podemos marcar como concluída (ou desmarcar). O conceito de lista to-do-it é amplamente usado para retirar da memória a carga que podemos atribuir ao computador.