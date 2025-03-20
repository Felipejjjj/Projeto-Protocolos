Descrição do Projeto

O nosso programa é um sistema de gerenciamento de produtos desenvolvido com a API de sockets em Python. O cliente, ao se conectar ao servidor, pode cadastrar produtos, consultar produtos, remover produtos e encerrar a conexão. O servidor gerencia os produtos utilizando uma árvore binária de busca (BST) para organização eficiente dos dados.

Arquivos do Projeto

servidor.py: Contém o código do servidor do sistema de gerenciamento de produtos. Ele é responsável por aceitar conexões de clientes, processar os comandos enviados e manipular os dados dos produtos usando uma estrutura de árvore binária de busca (BST). Ele também registra logs das operações realizadas.

cliente.py: Contém o código do cliente que se conecta ao servidor. O cliente pode enviar comandos para cadastrar produtos, consultar produtos, remover produtos e encerrar a conexão. As respostas do servidor são exibidas ao usuário.

bst.py: Implementa a estrutura de árvore binária de busca (BST) para armazenar e gerenciar os produtos no servidor. Fornece funções para inserção, busca e remoção de produtos.

Pré-requisitos para Execução

Python 3.x: Linguagem de programação usada para desenvolver o projeto. Pode ser instalado a partir do site oficial do Python.

Biblioteca socket: Biblioteca padrão do Python para criação de conexões de rede. Já está disponível no Python.

Biblioteca logging: Biblioteca padrão do Python usada para registrar logs do servidor.

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

Execute o arquivo servidor.py para iniciar o servidor.

Em um terminal separado, execute o arquivo cliente.py para iniciar o cliente.

Utilize os comandos suportados para interagir com o sistema.

Comandos disponíveis:

CADASTRAR|codigo|nome|preco → Cadastra um novo produto.

CONSULTAR|codigo → Consulta um produto pelo código.

REMOVER|codigo → Remove um produto pelo código.

O servidor responderá com mensagens indicando o sucesso ou erro das operações.

Bibliotecas Utilizadas

socket: Permite a comunicação entre o cliente e o servidor via conexões TCP.

logging: Usada para registrar eventos e atividades do servidor.

sys: Usada para acessar argumentos passados na linha de comando.

### Responsáveis pelo projeto
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/107876857?v=4" width=115><br><sub>Felipe Oliveira</sub>](https://github.com/Felipejjjj) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/149403389?v=4" width=115><br><sub>Francisco Viana</sub>](https://github.com/franciscovmn)
| :---: | :---: | :---: |