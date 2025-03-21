import socket
import logging
import threading  # Importa o módulo threading
from bst import BST  # Importa a árvore binária de busca (BST) para armazenar os produtos

# Classe que representa o servidor
class Server:
    def __init__(self, host="0.0.0.0", port=8080):
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
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Evita erro de "endereço já em uso"
        server.bind((self.host, self.port))  # Associa o socket ao IP e porta
        server.listen(5)  # Define um limite de 5 conexões simultâneas na fila
        logging.info(f"Servidor iniciado na porta {self.port}...")  # Log de início do servidor

        while True:
            client, addr = server.accept()  # Aceita uma nova conexão
            logging.info(f"Nova conexão de {addr}")  # Log da conexão recebida
            # Cria uma nova thread para processar a requisição do cliente
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()  # Inicia a thread

    # Processa a requisição recebida do cliente
    def handle_client(self, client):
        try:
            data = client.recv(1024).decode().strip()
            logging.info(f"Recebido: {data}")

            response_full = self.process_request(data)  # Obtém a resposta completa
            client.send(response_full.encode())  # Envia a resposta completa para o cliente

        except Exception as e:
            logging.error(f"Erro ao processar requisição: {e}")
            client.send("ERRO|Falha interna do servidor".encode())
        finally:
            client.close()

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

    # Cadastra um novo produto na BST
    def cadastrar(self, partes):
        if len(partes) < 4:
            return "ERRO|Dados incompletos"

        try:
            codigo, nome, preco = int(partes[1]), partes[2], float(partes[3])
            if not nome.replace(" ", "").isalpha():
                return "ERRO|Nome inválido. Use apenas letras e espaços"

            if self.produtos is None:
                return "ERRO|Estrutura de dados não inicializada"

            self.produtos.insert(codigo, nome, preco)
            logging.info(f"Produto cadastrado: {codigo} - {nome} (R$ {preco})")

            return "200 OK\n------\nProduto cadastrado com sucesso!"

        except ValueError:
            return "ERRO|Formato inválido dos dados"

    # Consulta um produto pelo código na BST
    def consultar(self, partes):
        if len(partes) < 2:
            return "ERRO|Código não fornecido"

        try:
            codigo = int(partes[1])
            produto = self.produtos.search(codigo)

            if produto:
                return f"200 OK\n------\ncodigo: {codigo} | nome: {produto['nome']} | valor: R${produto['preco']}"
            return "404 NOT FOUND\n------\nProduto não encontrado"

        except ValueError:
            return "ERRO|Código inválido"

    # Remove um produto da BST pelo código
    def remover(self, partes):
        if len(partes) < 2:
            return "ERRO|Código não fornecido"

        try:
            codigo = int(partes[1])
            sucesso = self.produtos.remove(codigo)

            if sucesso:
                logging.info(f"Produto {codigo} removido")
                return "200 OK\n------\nProduto removido com sucesso"
            return "404 NOT FOUND\n------\nProduto não encontrado"

        except ValueError:
            return "ERRO|Código inválido"

# Inicia o servidor quando o script for executado diretamente
if __name__ == "__main__":
    server = Server()  # Cria uma instância do servidor
    server.start()  # Inicia o servidor
