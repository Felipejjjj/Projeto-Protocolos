import sys
import socket

class Node:
    def __init__(self, codigo, nome, preco):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.next = None

class ListaEncadeada:
    def __init__(self):
        self.head = None
    
    def adicionar(self, codigo, nome, preco):
        novo_no = Node(codigo, nome, preco)
        novo_no.next = self.head
        self.head = novo_no
    
    def remover(self, codigo):
        atual = self.head
        anterior = None
        while atual and atual.codigo != codigo:
            anterior = atual
            atual = atual.next
        
        if not atual:
            return False
        
        if not anterior:
            self.head = atual.next
        else:
            anterior.next = atual.next
        
        return True
    
    def buscar(self, codigo):
        atual = self.head
        while atual:
            if atual.codigo == codigo:
                return atual
            atual = atual.next
        return None

def testar_conexao(host, port=12345):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.settimeout(1)
            cliente.connect((host, port))
        return True
    except (socket.error, socket.timeout):
        return False

def enviar_requisicao(host, mensagem):
    PORT = 12345
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((host, PORT))
        cliente.send(mensagem.encode())
        resposta = cliente.recv(1024).decode()
        return resposta

def main():
    # Verificando se foi passado um IP como argumento na linha de comando
    if len(sys.argv) > 1:
        host = sys.argv[1]
        if not testar_conexao(host):
            print(f"Não foi possível conectar ao IP fornecido: {host}")
            return
        print(f"Conectado com sucesso ao IP: {host}")
    else:
        host = "0.0.0.0" if testar_conexao("0.0.0.0") else input("Digite o IP do servidor: ")

    lista_produtos = ListaEncadeada()
    
    while True:
        print("\n1. Cadastrar Produto")
        print("2. Consultar Produto")
        print("3. Remover Produto")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            codigo = input("Código: ")
            nome = input("Nome: ")
            preco = input("Preço: ")
            resposta = enviar_requisicao(host, f"CADASTRAR|{codigo}|{nome}|{preco}")
            print(resposta)
            if resposta.startswith("OK"):
                lista_produtos.adicionar(int(codigo), nome, float(preco))
        
        elif opcao == '2':
            codigo = input("Código: ")
            resposta = enviar_requisicao(host, f"CONSULTAR|{codigo}")
            print(resposta)
            if resposta.startswith("OK"):
                partes = resposta.split('|')
                print(f"Produto: {partes[1]}, Preço: R$ {partes[2]}")
        
        elif opcao == '3':
            codigo = input("Código: ")
            resposta = enviar_requisicao(host, f"REMOVER|{codigo}")
            print(resposta)
            if resposta.startswith("OK"):
                lista_produtos.remover(int(codigo))
        
        elif opcao == '4':
            print("Encerrando aplicação...")
            break
        else:
            print("Opção inválida!")

# Verifique se o script está sendo executado diretamente
if __name__ == "__main__":
    main()
