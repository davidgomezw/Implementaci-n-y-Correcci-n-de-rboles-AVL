import sys 

#aqui se crea la clase nodo, almacenando el valor, los hijos y su altura
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1 

#función para obtener la altura de un nodo
def getHeight(node):
    if not node:
        return 0
    return node.height

#función para obtener el balance de un nodo
def getBalance(node):
    if not node:
        return 0
    return getHeight(node.left) - getHeight(node.right)

#función para actualizar la altura de un nodo
def updateHeight(node):
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))

#función para rotar a la derecha
def rotate_right(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    updateHeight(y)
    updateHeight(x)
    return x

#función para rotar a la izquierda
def rotate_left(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    updateHeight(x)
    updateHeight(y)
    return y

#clase para el árbol AVL
class AVLTree:
    def __init__(self):
        self.root = None

    #función para insertar un valor
    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if not node:
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node 
        
        updateHeight(node)
        balance = getBalance(node)

        # Corrección de rotaciones con return
        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node) 
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node) 
        elif balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node) 
        
        return node 

    #función para eliminar 
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if not node:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if not node.left: return node.right
            elif not node.right: return node.left
            
            temp = self._get_min_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)

        if not node: return node

        updateHeight(node)
        balance = getBalance(node)

        if balance > 1 and getBalance(node.left) >= 0: return rotate_right(node)
        if balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)
        if balance < -1 and getBalance(node.right) <= 0: return rotate_left(node)
        if balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)
        return node

    def _get_min_node(self, node):
        current = node
        while current.left: current = current.left
        return current

    #recorrido in-order 
    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    #visualización 
    def visualize(self):
        print("\n── Estructura del árbol AVL ──")
        if not self.root:
            print("  (árbol vacío)")
        else:
            self._visualize_recursive(self.root, "", False)
        print()

    def _visualize_recursive(self, node, prefix, is_left):
        if node is None:
            return
        self._visualize_recursive(node.right, prefix + ("│    " if is_left else "     "), False)
        connector = "└── " if is_left else "┌── "
        print(f"{prefix}{connector}[{node.value}] h={node.height} b={getBalance(node)}")
        self._visualize_recursive(node.left, prefix + ("     " if is_left else "│    "), True)

# Menú Interactivo
avl = AVLTree()

while True:
    print("--- MENU ÁRBOL AVL ---")
    print("1. Insertar")
    print("2. Eliminar")
    print("3. Mostrar árbol")
    print("4. Mostrar recorrido in-orden")
    print("5. Salir")
    
    try:
        opcion = int(input("Opcion: "))
        if opcion == 1:
            val = int(input("Valor a insertar: "))
            avl.insert(val)
        elif opcion == 2:
            val = int(input("Valor a eliminar: "))
            avl.delete(val)
        elif opcion == 3:
            avl.visualize()
        elif opcion == 4:
            print("Recorrido in-order:", avl.inorder())
        elif opcion == 5:
            print("Saliendo...")
            break
        else:
            print("Opción inválida")
    except ValueError:
        print("Error: Ingresa un número válido")