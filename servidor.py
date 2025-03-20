import socket
import logging
from bst import BST

class Server:
    def __init__(self, host="0.0.0.0", port=12345):
        self.host = host
        self.port = port
        self.produtos = BST()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        logging.info(f"Servidor iniciado na porta {self.port}...")

        while True:
            client, addr = server.accept()
            logging.info(f"Nova conexão de {addr}")
            self.handle_client(client)

    def handle_client(self, client):
        try:
            data = client.recv(1024)
            data = data.decode().strip()
            
            response = self.process_request(data)

            client.send(response.encode())

        except Exception as e:
            logging.error(f"Erro ao processar requisição: {e}")
        finally:
            client.close()

    def process_request(self, request):
        partes = request.split("|")
        acao = partes[0]

        if acao == "CADASTRAR":
            return self.cadastrar(partes)
        elif acao == "CONSULTAR":
            return self.consultar(partes)
        elif acao == "REMOVER":
            return self.remover(partes)
        else:
            return "ERRO|Ação desconhecida"

    def cadastrar(self, partes):
        if len(partes) < 4:
            return "ERRO|Dados incompletos"

        try:
            codigo, nome, preco = int(partes[1]), partes[2], float(partes[3])
            self.produtos.insert(codigo, nome, preco)
            logging.info(f"Produto cadastrado: {codigo} - {nome} (R$ {preco})")
            return f"200 OK\n------\nProduto {nome} cadastrado com sucesso!"
        except ValueError:
            return "ERRO|Formato inválido dos dados"

    def consultar(self, partes):
        if len(partes) < 2:
            return "ERRO|Código não fornecido"

        try:
            codigo = int(partes[1])
            produto = self.produtos.search(codigo)
            if produto:
                return f"OK|{produto['nome']}|{produto['preco']}"
            return "404 NOT FOUND\n-------------\nProduto não encontrado"
        except ValueError:
            return "ERRO|Código inválido"

    def remover(self, partes):
        if len(partes) < 2:
            return "ERRO|Código não fornecido"

        try:
            codigo = int(partes[1])
            sucesso = self.produtos.remove(codigo)
            if sucesso:
                logging.info(f"Produto {codigo} removido")
                return "200 OK\n------\nProduto removido com sucesso"
            return "ERRO|Produto não encontrado"
        except ValueError:
            return "ERRO|Código inválido"

if __name__ == "__main__":
    server = Server()
    server.start()
