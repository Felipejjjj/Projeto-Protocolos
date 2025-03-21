import socket  # Para criar a comunicação de rede (clientes e servidor)
import logging  # Para registrar mensagens de log, como erros e informações
import threading  # Para permitir que o servidor atenda múltiplos clientes ao mesmo tempo
from bst import BST  # Importa a classe BST (Árvore Binária de Busca), usada para armazenar os produtos de forma eficiente

class Server:
    def __init__(self, host="0.0.0.0", port=8080):
        # Inicializa o servidor com o endereço IP e porta definidos
        self.host = host  # O servidor aceitará conexões de qualquer IP
        self.port = port  # Porta que o servidor vai escutar
        self.produtos = BST()  # Usando a BST para armazenar os produtos cadastrados
        self.lock = threading.Semaphore(1)  # Semáforo para garantir que apenas uma thread por vez modifique a lista de produtos
        self.setup_logging()  # Configura o sistema de logs

    def setup_logging(self):
        # Configura como as mensagens de log serão exibidas
        logging.basicConfig(
            level=logging.INFO,  # Nível de log (informações gerais)
            format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log com data e hora
            datefmt="%Y-%m-%d %H:%M:%S",  # Formato de data e hora
        )

    def start(self):
        # Cria o socket do servidor e começa a escutar por conexões
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Define o tipo de comunicação (TCP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar o endereço
        server.bind((self.host, self.port))  # Faz o bind do servidor ao IP e à porta
        server.listen(5)  # Permite até 5 conexões simultâneas
        logging.info(f"Servidor iniciado na porta {self.port}...")  # Log da inicialização do servidor

        while True:
            # Espera por novos clientes
            client, addr = server.accept()  # Quando um cliente se conecta, aceita a conexão
            logging.info(f"Nova conexão de {addr}")  # Log da nova conexão
            client_thread = threading.Thread(target=self.handle_client, args=(client,))  # Cria uma nova thread para lidar com o cliente
            client_thread.start()  # Inicia a thread que vai atender o cliente

    def handle_client(self, client):
        # Função que lida com as requisições de um cliente
        try:
            data = client.recv(1024).decode().strip()  # Recebe dados do cliente e decodifica
            logging.info(f"Recebido: {data}")  # Log da requisição recebida

            response_full = self.process_request(data)  # Processa a requisição e gera a resposta
            client.sendall(response_full.encode())  # Envia a resposta de volta ao cliente

        except Exception as e:
            # Se houver algum erro no processamento, envia uma mensagem de erro
            logging.error(f"Erro ao processar requisição: {e}")
            client.sendall("ERRO|Falha interna do servidor".encode())  # Envia erro ao cliente

        finally:
            client.close()  # Fecha a conexão com o cliente, independentemente de ter dado certo ou não

    def process_request(self, request):
        # Função que processa a requisição e chama a ação apropriada
        partes = request.split("|")  # Divide a requisição em partes usando "|" como separador
        acao = partes[0]  # A primeira parte da requisição indica a ação

        if acao == "CADASTRAR":
            return self.cadastrar(partes)  # Chama a função de cadastro
        elif acao == "CONSULTAR":
            return self.consultar(partes)  # Chama a função de consulta
        elif acao == "REMOVER":
            return self.remover(partes)  # Chama a função de remoção
        else:
            return "ERRO|Ação desconhecida"  # Retorna erro caso a ação seja inválida

    def cadastrar(self, partes):
        # Função para cadastrar um novo produto
        if len(partes) < 4:  # Verifica se a quantidade de dados é suficiente
            return "ERRO|Dados incompletos"  # Retorna erro se faltar dados

        try:
            codigo, nome, preco = int(partes[1]), partes[2], float(partes[3])  # Tenta extrair os dados (código, nome e preço)
            if not nome.replace(" ", "").isalpha():  # Verifica se o nome contém apenas letras e espaços
                return "ERRO|Nome inválido. Use apenas letras e espaços"

            with self.lock:  # Garante que apenas uma thread acesse a lista de produtos por vez
                self.produtos.insert(codigo, nome, preco)  # Insere o novo produto na árvore

            logging.info(f"Produto cadastrado: {codigo} - {nome} (R$ {preco})")  # Log do produto cadastrado
            return "200 OK\n------\nProduto cadastrado com sucesso!"  # Resposta de sucesso

        except ValueError:
            return "ERRO|Formato inválido dos dados"  # Caso os dados não tenham o formato correto

    def consultar(self, partes):
        # Função para consultar um produto pelo código
        if len(partes) < 2:  # Verifica se o código foi fornecido
            return "ERRO|Código não fornecido"  # Retorna erro se o código não for fornecido

        try:
            codigo = int(partes[1])  # Tenta converter o código para inteiro

            with self.lock:  # Garante que a consulta ao banco de dados seja feita de forma segura
                produto = self.produtos.search(codigo)  # Tenta buscar o produto pelo código

            if produto:
                # Se o produto for encontrado, retorna as informações
                return f"200 OK\n------\ncodigo: {codigo} | nome: {produto['nome']} | valor: R${produto['preco']}"
            return "404 NOT FOUND\n------\nProduto não encontrado"  # Se o produto não for encontrado, retorna erro

        except ValueError:
            return "ERRO|Código inválido"  # Caso o código não seja um número válido

    def remover(self, partes):
        # Função para remover um produto pelo código
        if len(partes) < 2:  # Verifica se o código foi fornecido
            return "ERRO|Código não fornecido"  # Retorna erro se o código não for fornecido

        try:
            codigo = int(partes[1])  # Tenta converter o código para inteiro

            with self.lock:  # Garante que a remoção seja feita de forma segura
                sucesso = self.produtos.remove(codigo)  # Tenta remover o produto pelo código

            if sucesso:
                logging.info(f"Produto {codigo} removido")  # Log da remoção
                return "200 OK\n------\nProduto removido com sucesso"  # Retorna sucesso
            return "404 NOT FOUND\n------\nProduto não encontrado"  # Retorna erro caso o produto não seja encontrado

        except ValueError:
            return "ERRO|Código inválido"  # Caso o código não seja um número válido

if __name__ == "__main__":
    # Esse bloco inicia o servidor se o script for executado diretamente
    server = Server()  # Cria uma instância do servidor
    server.start()  # Inicia o servidor, fazendo-o começar a escutar por conexões
