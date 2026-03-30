from Conexion.conexion import obtener_conexion

def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.id_producto, p.nombre, p.precio, p.stock,
               c.nombre AS categoria,
               pr.nombre AS proveedor
        FROM productos p
        INNER JOIN categorias c ON p.id_categoria = c.id_categoria
        INNER JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto ASC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos

def obtener_producto_por_id(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_producto, nombre, precio, stock, id_categoria, id_proveedor
        FROM productos
        WHERE id_producto = %s
    """, (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto

def crear_producto(nombre, precio, stock, id_categoria, id_proveedor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, precio, stock, id_categoria, id_proveedor)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, precio, stock, id_categoria, id_proveedor))
    conexion.commit()
    cursor.close()
    conexion.close()

def actualizar_producto(id_producto, nombre, precio, stock, id_categoria, id_proveedor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE productos
        SET nombre = %s, precio = %s, stock = %s, id_categoria = %s, id_proveedor = %s
        WHERE id_producto = %s
    """, (nombre, precio, stock, id_categoria, id_proveedor, id_producto))
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_producto(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conexion.commit()
    cursor.close()
    conexion.close()

def listar_categorias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_categoria, nombre FROM categorias ORDER BY nombre ASC")
    categorias = cursor.fetchall()
    cursor.close()
    conexion.close()
    return categorias

def listar_proveedores():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_proveedor, nombre FROM proveedores ORDER BY nombre ASC")
    proveedores = cursor.fetchall()
    cursor.close()
    conexion.close()
    return proveedores