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

def enviar_requisicao(mensagem):
    HOST = '0.0.0.0'
    PORT = 12345
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        cliente.send(mensagem.encode())
        resposta = cliente.recv(1024).decode()
        return resposta

def main():
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
            resposta = enviar_requisicao(f"CADASTRAR|{codigo}|{nome}|{preco}")
            print(resposta)
            if resposta.startswith("OK"):
                lista_produtos.adicionar(int(codigo), nome, float(preco))
        
        elif opcao == '2':
            codigo = input("Código: ")
            resposta = enviar_requisicao(f"CONSULTAR|{codigo}")
            print(resposta)
            if resposta.startswith("OK"):
                partes = resposta.split('|')
                print(f"Produto: {partes[1]}, Preço: R$ {partes[2]}")
        
        elif opcao == '3':
            codigo = input("Código: ")
            resposta = enviar_requisicao(f"REMOVER|{codigo}")
            print(resposta)
            if resposta.startswith("OK"):
                lista_produtos.remover(int(codigo))
        
        elif opcao == '4':
            print("Encerrando aplicação...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
