import sys
import socket

# Classe que representa um nó na lista encadeada (basicamente um produto)
class Node:
    def __init__(self, codigo, nome, preco):
        self.codigo = codigo  # Código do produto
        self.nome = nome  # Nome do produto
        self.preco = preco  # Preço do produto
        self.next = None  # Ponteiro para o próximo nó

# Classe que gerencia a lista encadeada dos produtos
class ListaEncadeada:
    def __init__(self):
        self.head = None  # Começa sem nenhum item na lista

    # Adiciona um novo produto à lista (insere no início)
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

        # Se não encontrou, retorna falso
        if not atual:
            return False

        # Se for o primeiro item da lista, só precisa mudar o head
        if not anterior:
            self.head = atual.next
        else:
            anterior.next = atual.next  # Remove o nó ajustando o ponteiro do anterior

        return True

    # Busca um produto pelo código e retorna o nó correspondente
    def buscar(self, codigo):
        atual = self.head
        while atual:
            if atual.codigo == codigo:
                return atual  # Achou!
            atual = atual.next
        return None  # Não achou

# Testa se consegue conectar ao servidor na porta 12345
def testar_conexao(host, port=12345):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.settimeout(1)  # Espera no máximo 1 segundo
            cliente.connect((host, port))  # Tenta conectar
        return True  # Conseguiu conectar
    except (socket.error, socket.timeout):
        return False  # Deu ruim

# Envia uma mensagem para o servidor e recebe a resposta
def enviar_requisicao(host, mensagem):
    PORT = 12345  # Porta do servidor

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((host, PORT))  # Conecta ao servidor
        cliente.send(mensagem.encode())  # Envia a mensagem
        resposta = cliente.recv(1024).decode()  # Espera e recebe a resposta
        return resposta  # Retorna a resposta recebida

# Função principal do programa
def main():
    # Verifica se um IP foi passado como argumento ao rodar o script
    if len(sys.argv) > 1:
        host = sys.argv[1]
        if not testar_conexao(host):
            print(f"Não foi possível conectar ao IP fornecido: {host}")
            return
        print(f"Conectado com sucesso ao IP: {host}")
    else:
        # Se não passou um IP, tenta conectar no IP padrão ou pede para o usuário informar um
        host = "0.0.0.0" if testar_conexao("0.0.0.0") else input("Digite o IP do servidor: ")

    lista_produtos = ListaEncadeada()  # Cria uma lista para guardar os produtos localmente

    while True:
        print("\n1. Cadastrar Produto")
        print("2. Consultar Produto")
        print("3. Remover Produto")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':  # Cadastrar produto
            codigo = input("Código: ")
            nome = input("Nome: ")
            preco = input("Preço: ")
            resposta = enviar_requisicao(host, f"CADASTRAR|{codigo}|{nome}|{preco}")  # Envia ao servidor
            print(resposta)
            if resposta.startswith("OK"):  # Se o servidor confirmou, adiciona na lista local
                lista_produtos.adicionar(int(codigo), nome, float(preco))

        elif opcao == '2':  # Consultar produto
            codigo = input("Código: ")
            resposta = enviar_requisicao(host, f"CONSULTAR|{codigo}")  # Pergunta ao servidor
            print(resposta)
            if resposta.startswith("OK"):  # Se encontrou, exibe os detalhes
                partes = resposta.split('|')
                print(f"Produto: {partes[1]}, Preço: R$ {partes[2]}")

        elif opcao == '3':  # Remover produto
            codigo = input("Código: ")
            resposta = enviar_requisicao(host, f"REMOVER|{codigo}")  # Pede ao servidor para remover
            print(resposta)
            if resposta.startswith("OK"):  # Se removeu no servidor, remove localmente também
                lista_produtos.remover(int(codigo))

        elif opcao == '4':  # Sair do programa
            print("Encerrando aplicação...")
            break

        else:
            print("Opção inválida!")  # Se o usuário digitou algo errado

# Executa a função main se o script for rodado diretamente
if __name__ == "__main__":
    main()
