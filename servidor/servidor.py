import socket
import logging
from arvore_bst.bst import BST  # Importa a árvore binária de busca (BST) para armazenar os produtos

# Classe que representa o servidor
class Server:
    def __init__(self, host="0.0.0.0", port=12345):
        self.host = host  # IP no qual o servidor vai rodar (0.0.0.0 aceita conexões de qualquer IP)
        self.port = port  # Porta onde o servidor escuta as conexões
        self.produtos = BST()  # Estrutura para armazenar os produtos na forma de uma árvore binária
        self.setup_logging()  # Configuração do sistema de logs

    # Configura os logs para registrar eventos do servidor
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,  # Define o nível de log como INFO
            format="%(asctime)s - %(levelname)s - %(message)s",  # Formato da mensagem de log
            datefmt="%Y-%m-%d %H:%M:%S",  # Formato da data e hora
        )

    # Inicia o servidor e começa a escutar conexões
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
        server.bind((self.host, self.port))  # Associa o socket ao IP e porta
        server.listen(5)  # Define um limite de 5 conexões simultâneas na fila
        logging.info(f"Servidor iniciado na porta {self.port}...")  # Log de início do servidor

        while True:
            client, addr = server.accept()  # Aceita uma nova conexão
            logging.info(f"Nova conexão de {addr}")  # Log da conexão recebida
            self.handle_client(client)  # Processa a requisição do cliente

    # Processa a requisição recebida do cliente
    def handle_client(self, client):
        try:
            data = client.recv(1024)  # Recebe até 1024 bytes de dados do cliente
            data = data.decode().strip()  # Decodifica e remove espaços extras

            response = self.process_request(data)  # Processa a requisição recebida

            client.send(response.encode())  # Envia a resposta de volta para o cliente

        except Exception as e:
            logging.error(f"Erro ao processar requisição: {e}")  # Log de erro
        finally:
            client.close()  # Fecha a conexão com o cliente

    # Interpreta a requisição do cliente e direciona para a ação correta
    def process_request(self, request):
        partes = request.split("|")  # Divide a mensagem recebida pelo delimitador "|"
        acao = partes[0]  # A primeira parte indica a ação desejada

        # Executa a ação com base no comando recebido
        if acao == "CADASTRAR":
            return self.cadastrar(partes)
        elif acao == "CONSULTAR":
            return self.consultar(partes)
        elif acao == "REMOVER":
            return self.remover(partes)
        else:
            return "ERRO|Ação desconhecida"  # Responde com erro se o comando for inválido

    # Cadastra um novo produto na BST (árvore binária de busca)
    def cadastrar(self, partes):
        if len(partes) < 4:
            return "ERRO|Dados incompletos"  # Retorna erro se não tiver todos os campos necessários

        try:
            codigo, nome, preco = int(partes[1]), partes[2], float(partes[3])  # Converte os valores recebidos
            self.produtos.insert(codigo, nome, preco)  # Insere o produto na árvore BST
            logging.info(f"Produto cadastrado: {codigo} - {nome} (R$ {preco})")  # Log do cadastro
            return f"200 OK\n------\nProduto {nome} cadastrado com sucesso!"  # Responde ao cliente com sucesso
        except ValueError:
            return "ERRO|Formato inválido dos dados"  # Retorna erro se os dados não forem válidos

    # Consulta um produto pelo código na BST
    def consultar(self, partes):
        if len(partes) < 2:
            return "ERRO|Código não fornecido"  # Retorna erro se não informar o código

        try:
            codigo = int(partes[1])  # Converte o código para inteiro
            produto = self.produtos.search(codigo)  # Procura o produto na árvore BST
            if produto:
                return f"OK|{produto['nome']}|{produto['preco']}"  # Retorna os dados do produto
            return "404 NOT FOUND\n-------------\nProduto não encontrado"  # Retorna erro se não encontrar
        except ValueError:
            return "ERRO|Código inválido"  # Retorna erro se o código não for um número

    # Remove um produto da BST pelo código
    def remover(self, partes):
        if len(partes) < 2:
            return "ERRO|Código não fornecido"  # Retorna erro se não informar o código

        try:
            codigo = int(partes[1])  # Converte o código para inteiro
            sucesso = self.produtos.remove(codigo)  # Tenta remover o produto da árvore BST
            if sucesso:
                logging.info(f"Produto {codigo} removido")  # Log da remoção
                return "200 OK\n------\nProduto removido com sucesso"  # Retorna sucesso
            return "ERRO|Produto não encontrado"  # Retorna erro se o produto não existir
        except ValueError:
            return "ERRO|Código inválido"  # Retorna erro se o código não for um número

# Inicia o servidor quando o script for executado diretamente
if __name__ == "__main__":
    server = Server()  # Cria uma instância do servidor
    server.start()  # Inicia o servidor
