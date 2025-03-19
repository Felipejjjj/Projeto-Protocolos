class Node:
    def __init__(self, codigo, nome, preco):
        self.codigo = codigo
        self.produto = {"nome": nome, "preco": preco}
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, codigo, nome, preco):
        """Insere um novo produto na árvore, evitando duplicação de código"""
        if self.search(codigo):
            return False  # Produto com o mesmo código já existe
        self.root = self._insert(self.root, codigo, nome, preco)
        return True  # Produto cadastrado com sucesso

    def _insert(self, node, codigo, nome, preco):
        if not node:
            return Node(codigo, nome, preco)
        if codigo < node.codigo:
            node.left = self._insert(node.left, codigo, nome, preco)
        else:
            node.right = self._insert(node.right, codigo, nome, preco)
        return node

    def search(self, codigo):
        """Busca um produto pelo código"""
        node = self._search(self.root, codigo)
        return node.produto if node else None

    def _search(self, node, codigo):
        if not node or node.codigo == codigo:
            return node
        return self._search(node.left, codigo) if codigo < node.codigo else self._search(node.right, codigo)

    def remove(self, codigo):
        """Remove um produto pelo código"""
        self.root, deleted = self._remove(self.root, codigo)
        return deleted

    def _remove(self, node, codigo):
        if not node:
            return node, False

        if codigo < node.codigo:
            node.left, deleted = self._remove(node.left, codigo)
        elif codigo > node.codigo:
            node.right, deleted = self._remove(node.right, codigo)
        else:
            deleted = True
            if not node.left:
                return node.right, deleted
            if not node.right:
                return node.left, deleted
            
            # Substituir pelo menor valor da subárvore direita
            temp = self._min_value_node(node.right)
            node.codigo, node.produto = temp.codigo, temp.produto
            node.right, _ = self._remove(node.right, temp.codigo)

        return node, deleted

    def _min_value_node(self, node):
        """Encontra o menor nó na subárvore direita"""
        while node.left:
            node = node.left
        return node

    def inorder(self):
        """Retorna a lista de produtos ordenados por código"""
        produtos = []
        self._inorder(self.root, produtos)
        return produtos

    def _inorder(self, node, produtos):
        if node:
            self._inorder(node.left, produtos)
            produtos.append({"codigo": node.codigo, "nome": node.produto["nome"], "preco": node.produto["preco"]})
            self._inorder(node.right, produtos)