Descrição do Projeto

O nosso programa é um sistema de gerenciamento de produtos desenvolvido com a API de sockets em Python. O cliente, ao se conectar ao servidor, pode cadastrar produtos, consultar produtos, remover produtos e encerrar a conexão. O servidor gerencia os produtos utilizando uma árvore binária de busca (BST) para organização eficiente dos dados. Além disso, o servidor utiliza threading para atender múltiplos clientes simultaneamente, garantindo que o processamento de requisições de diferentes clientes não interfira uns com os outros.
Arquivos do Projeto

    servidor.py: Contém o código do servidor do sistema de gerenciamento de produtos. O servidor agora utiliza threading, permitindo que ele crie uma nova thread para cada cliente que se conecta. Cada thread é responsável por processar a requisição de um cliente, permitindo que o servidor atenda múltiplos clientes simultaneamente sem bloqueios. Além disso, o servidor registra logs das operações realizadas.

    cliente.py: Contém o código do cliente que se conecta ao servidor. O cliente pode enviar comandos para cadastrar produtos, consultar produtos, remover produtos e encerrar a conexão.

    bst.py: Implementa a estrutura de árvore binária de busca (BST) para armazenar e gerenciar os produtos no servidor. Fornece funções para inserção, busca e remoção de produtos.

Pré-requisitos para Execução

    Python 3.x: Linguagem de programação usada para desenvolver o projeto. Pode ser instalado a partir do site oficial do Python.
    Biblioteca socket: Biblioteca padrão do Python para criação de conexões de rede. Já está disponível no Python.
    Biblioteca logging: Biblioteca padrão do Python usada para registrar logs do servidor.
    Biblioteca threading: Biblioteca padrão do Python usada para criar múltiplas threads, permitindo o atendimento simultâneo de várias conexões.
    Biblioteca sys: Biblioteca padrão do Python usada para acessar argumentos da linha de comando.

Protocolo da Aplicação

O protocolo da aplicação consiste em uma série de comandos que o cliente pode enviar ao servidor:

    CADASTRAR: Registra um novo produto.
        Argumentos:
            codigo: O código numérico do produto.
            nome: O nome do produto.
            preco: O preço do produto.

    CONSULTAR: Consulta um produto pelo código.
        Argumentos:
            codigo: O código numérico do produto a ser consultado.

    REMOVER: Remove um produto pelo código.
        Argumentos:
            codigo: O código numérico do produto a ser removido.

Instruções para Execução

    Iniciar o servidor:
        Execute o arquivo servidor.py para iniciar o servidor.

    Iniciar o cliente:
        Em um terminal separado, execute o arquivo cliente.py para iniciar o cliente.

    Interagir com o servidor:

        Utilize os seguintes comandos para interagir com o sistema:
            CADASTRAR|codigo|nome|preco → Cadastra um novo produto.
            CONSULTAR|codigo → Consulta um produto pelo código.
            REMOVER|codigo → Remove um produto pelo código.

    O servidor responderá com mensagens indicando o sucesso ou erro das operações.

Como Funciona o Servidor com Threading

O servidor foi modificado para usar o módulo threading do Python, permitindo que ele atenda múltiplos clientes simultaneamente. Quando um cliente se conecta, o servidor cria uma nova thread para tratar a requisição desse cliente. Isso significa que o servidor não fica bloqueado esperando a resposta de um cliente, e pode atender a outros clientes enquanto processa os dados.
Fluxo de Execução:

    O servidor escuta conexões em uma porta definida.
    Quando um cliente se conecta, o servidor cria uma nova thread com a função handle_client(), que é responsável por processar a requisição e enviar a resposta.
    Cada thread lida com um cliente de forma independente, permitindo que o servidor atenda múltiplas requisições de diferentes clientes simultaneamente.

Bibliotecas Utilizadas

    socket: Permite a comunicação entre o cliente e o servidor via conexões TCP.
    logging: Usada para registrar eventos e atividades do servidor.
    threading: Usada para criar novas threads que permitem o atendimento simultâneo de múltiplos clientes.
    sys: Usada para acessar argumentos passados na linha de comando.

### Responsáveis pelo projeto
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/107876857?v=4" width=115><br><sub>Felipe Oliveira</sub><br><sub>matricula 20241370007</sub><br><sub>raimundo.felipe@academico.ifpb.edu.br</sub>](https://github.com/Felipejjjj) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/149403389?v=4" width=115><br><sub>Francisco Viana</sub><br><sub>matricula 20232370011</sub><br><sub>francisco.viana@academico.ifpb.edu.br</sub>](https://github.com/franciscovmn) |
| :---: | :---: | 
