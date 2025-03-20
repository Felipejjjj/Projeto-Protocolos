# Classe que representa um nó da árvore
class Node:
    def __init__(self, codigo, nome, preco):
        self.codigo = codigo  # Código do produto (chave de busca na árvore)
        self.produto = {"nome": nome, "preco": preco}  # Armazena os dados do produto em um dicionário
        self.left = None  # Ponteiro para o filho esquerdo
        self.right = None  # Ponteiro para o filho direito

# Classe que implementa a Árvore Binária de Busca (BST)
class BST:
    def __init__(self):
        self.root = None  # Começa com a árvore vazia

    # Função pública para inserir um produto na árvore
    def insert(self, codigo, nome, preco):
        """Insere um novo produto na árvore"""
        self.root = self._insert(self.root, codigo, nome, preco)

    # Função interna recursiva para inserir um produto na posição correta
    def _insert(self, node, codigo, nome, preco):
        if not node:  # Se chegou em um nó vazio, cria um novo nó aqui
            return Node(codigo, nome, preco)

        if codigo < node.codigo:  # Se o código for menor, vai para a esquerda
            node.left = self._insert(node.left, codigo, nome, preco)
        else:  # Se for maior ou igual, vai para a direita
            node.right = self._insert(node.right, codigo, nome, preco)

        return node  # Retorna o nó atualizado

    # Função pública para buscar um produto pelo código
    def search(self, codigo):
        """Busca um produto pelo código"""
        node = self._search(self.root, codigo)  # Chama a função recursiva
        return node.produto if node else None  # Retorna o produto se encontrou, senão retorna None

    # Função interna recursiva para buscar um nó na árvore
    def _search(self, node, codigo):
        if not node or node.codigo == codigo:  # Se encontrou ou chegou ao final sem achar
            return node

        # Se o código for menor, busca na subárvore esquerda, senão busca na direita
        return self._search(node.left, codigo) if codigo < node.codigo else self._search(node.right, codigo)

    # Função pública para remover um produto pelo código
    def remove(self, codigo):
        """Remove um produto pelo código"""
        self.root, deleted = self._remove(self.root, codigo)  # Chama a função recursiva
        return deleted  # Retorna se a remoção foi bem-sucedida

    # Função interna recursiva para remover um nó da árvore
    def _remove(self, node, codigo):
        if not node:  # Se não encontrou o nó, retorna sem alteração
            return node, False

        if codigo < node.codigo:  # Se o código for menor, procura na esquerda
            node.left, deleted = self._remove(node.left, codigo)
        elif codigo > node.codigo:  # Se for maior, procura na direita
            node.right, deleted = self._remove(node.right, codigo)
        else:
            deleted = True  # Marcamos que encontramos o nó para remover

            # Caso 1: Nó sem filho à esquerda
            if not node.left:
                return node.right, deleted  # Retorna o filho direito para ocupar o lugar do nó removido
            
            # Caso 2: Nó sem filho à direita
            if not node.right:
                return node.left, deleted  # Retorna o filho esquerdo para ocupar o lugar do nó removido
            
            # Caso 3: Nó com dois filhos -> Encontramos o menor valor da subárvore direita
            temp = self._min_value_node(node.right)
            node.codigo, node.produto = temp.codigo, temp.produto  # Substituímos os dados pelo sucessor
            node.right, _ = self._remove(node.right, temp.codigo)  # Removemos o nó sucessor na subárvore direita

        return node, deleted  # Retorna o nó atualizado e se houve remoção

    # Função auxiliar para encontrar o menor nó na subárvore direita (usado na remoção)
    def _min_value_node(self, node):
        """Encontra o menor nó na subárvore direita"""
        current = node
        while current.left:  # O menor valor sempre está na extremidade esquerda
            current = current.left
        return current  # Retorna o nó com o menor valor
