class Producto:
    def __init__(self, id_producto=None, nombre="", precio=0.0, stock=0, id_categoria=None, id_proveedor=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.id_categoria = id_categoria
        self.id_proveedor = id_proveedor