class ProductoForm:
    def __init__(self, nombre="", precio="", stock="", id_categoria="", id_proveedor=""):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.id_categoria = id_categoria
        self.id_proveedor = id_proveedor

    def validar(self):
        errores = []

        if not self.nombre.strip():
            errores.append("El nombre es obligatorio.")

        try:
            if float(self.precio) <= 0:
                errores.append("El precio debe ser mayor a 0.")
        except:
            errores.append("El precio no es válido.")

        try:
            if int(self.stock) < 0:
                errores.append("El stock no puede ser negativo.")
        except:
            errores.append("El stock no es válido.")

        if not str(self.id_categoria).strip():
            errores.append("Debe seleccionar una categoría.")

        if not str(self.id_proveedor).strip():
            errores.append("Debe seleccionar un proveedor.")

        return errores