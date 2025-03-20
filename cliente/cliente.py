import sys
import socket
import logging
import re

# Configuração dos logs para registrar erros e eventos importantes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Classe que representa um nó da lista encadeada (cada nó é um produto)
class Node:
    def __init__(self, codigo, nome, preco):
        self.codigo = codigo  # Código do produto
        self.nome = nome  # Nome do produto
        self.preco = preco  # Preço do produto
        self.next = None  # Ponteiro para o próximo nó na lista

# Classe para gerenciar a lista encadeada de produtos
class ListaEncadeada:
    def __init__(self):
        self.head = None  # Inicializa a lista vazia
    
    # Adiciona um novo produto à lista
    def adicionar(self, codigo, nome, preco):
        novo_no = Node(codigo, nome, preco)
        novo_no.next = self.head  # O novo nó aponta para o antigo primeiro nó
        self.head = novo_no  # Agora ele é o primeiro da lista
    
    # Remove um produto pelo código
    def remover(self, codigo):
        atual = self.head  # Começa do primeiro nó
        anterior = None  # Mantém o nó anterior para ajustar os ponteiros
        
        # Percorre a lista até encontrar o código ou chegar ao final
        while atual and atual.codigo != codigo:
            anterior = atual
            atual = atual.next
        
        if not atual:  # Se não encontrou, retorna falso
            return False
        
        if not anterior:  # Se for o primeiro da lista, basta mudar o head
            self.head = atual.next
        else:  # Se for um nó do meio ou final, ajusta os ponteiros
            anterior.next = atual.next
        
        return True  # Produto removido com sucesso
    
    # Busca um produto pelo código
    def buscar(self, codigo):
        atual = self.head
        while atual:
            if atual.codigo == codigo:
                return atual  # Produto encontrado!
            atual = atual.next
        return None  # Produto não encontrado

# Testa se o cliente consegue conectar ao servidor
def testar_conexao(host, port=12345):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.settimeout(1)  # Define um tempo limite para a conexão
            cliente.connect((host, port))  # Tenta conectar
        return True  # Conseguiu conectar
    except (socket.error, socket.timeout) as e:
        logging.error(f"Erro ao conectar ao servidor: {e}")
        return False  # Deu erro na conexão

# Envia uma requisição para o servidor e recebe a resposta
def enviar_requisicao(host, mensagem):
    PORT = 12345  # Porta do servidor
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((host, PORT))  # Conecta ao servidor
            cliente.send(mensagem.encode())  # Envia a mensagem codificada
            resposta = cliente.recv(1024).decode()  # Recebe a resposta do servidor
            return resposta  # Retorna a resposta
    except socket.error as e:
        logging.error(f"Erro ao enviar requisição: {e}")
        return "ERRO|Falha na comunicação com o servidor"  # Retorna erro

# Função principal do cliente

def main():
    # Verifica se foi passado um IP como argumento na linha de comando
    if len(sys.argv) > 1:
        host = sys.argv[1]
        if not testar_conexao(host):
            print(f"Não foi possível conectar ao IP fornecido: {host}")
            return
        print(f"Conectado com sucesso ao IP: {host}")
    else:
        # Se não passou um IP, tenta conectar no padrão ou pede ao usuário
        host = "0.0.0.0" if testar_conexao("0.0.0.0") else input("Digite o IP do servidor: ")

    lista_produtos = ListaEncadeada()  # Cria uma lista para guardar os produtos localmente
    
    while True:
        # Menu de opções para o usuário
        print("\n1. Cadastrar Produto")
        print("2. Consultar Produto")
        print("3. Remover Produto")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':  # Cadastrar produto
            try:
                codigo = int(input("Código: "))
                nome = input("Nome: ")
                if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ ]+$", nome):
                    print("Erro: O nome deve conter apenas letras e espaços!")
                    continue
                preco = float(input("Preço: "))
                resposta = enviar_requisicao(host, f"CADASTRAR|{codigo}|{nome}|{preco}")
                print(resposta)
                if resposta.startswith("OK"):
                    lista_produtos.adicionar(codigo, nome, preco)
            except ValueError:
                print("Erro: Código e preço devem ser numéricos!")
        
        elif opcao == '2':  # Consultar produto
            try:
                codigo = int(input("Código: "))
                resposta = enviar_requisicao(host, f"CONSULTAR|{codigo}")
                print(resposta)
                if resposta.startswith("OK"):
                    partes = resposta.split('|')
                    print(f"Produto: {partes[1]}, Preço: R$ {partes[2]}")
            except ValueError:
                print("Erro: Código inválido!")
        
        elif opcao == '3':  # Remover produto
            try:
                codigo = int(input("Código: "))
                resposta = enviar_requisicao(host, f"REMOVER|{codigo}")
                print(resposta)
                if resposta.startswith("OK"):
                    lista_produtos.remover(codigo)
            except ValueError:
                print("Erro: Código inválido!")
        
        elif opcao == '4':  # Sair do programa
            print("Encerrando aplicação...")
            break
        else:
            print("Opção inválida!")  # Se o usuário digitou algo errado

# Executa a função main se o script for rodado diretamente
if __name__ == "__main__":
    main()
