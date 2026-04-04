from flask import Flask, render_template, flash, redirect, url_for, request, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF

import os
import importlib.util

from inventario.inventario import inventario_bp
from Conexion.conexion import obtener_conexion
from services.producto_service import (
    listar_productos,
    obtener_producto_por_id,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
    listar_categorias,
    listar_proveedores
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave_segura_123"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debe iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"

app.register_blueprint(inventario_bp)


# =========================================================
# CARGAR forms.py y models.py DE LA RAÍZ
# Esto evita conflicto con las carpetas nuevas forms/ y models/
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def cargar_modulo_local(nombre_modulo, archivo):
    ruta_archivo = os.path.join(BASE_DIR, archivo)
    spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_archivo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

forms_raiz = cargar_modulo_local("forms_raiz", "forms.py")
models_raiz = cargar_modulo_local("models_raiz", "models.py")

FormularioNombre = forms_raiz.FormularioNombre
FormularioRegistro = forms_raiz.FormularioRegistro
FormularioLogin = forms_raiz.FormularioLogin
Usuario = models_raiz.Usuario


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
def validar_datos_producto(nombre, precio, stock, id_categoria, id_proveedor):
    errores = []

    if not nombre.strip():
        errores.append("El nombre es obligatorio.")

    try:
        if float(precio) <= 0:
            errores.append("El precio debe ser mayor a 0.")
    except:
        errores.append("El precio no es válido.")

    try:
        if int(stock) < 0:
            errores.append("El stock no puede ser negativo.")
    except:
        errores.append("El stock no es válido.")

    if not str(id_categoria).strip():
        errores.append("Debe seleccionar una categoría.")

    if not str(id_proveedor).strip():
        errores.append("Debe seleccionar un proveedor.")

    return errores


def limpiar_texto_pdf(texto):
    return str(texto).encode("latin-1", "replace").decode("latin-1")


# =========================================================
# LOGIN MANAGER
# =========================================================
@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id_usuario, nombre, mail, password FROM usuarios WHERE id_usuario = %s",
        (user_id,)
    )
    fila = cursor.fetchone()
    cursor.close()
    conexion.close()

    if fila:
        return Usuario(fila[0], fila[1], fila[2], fila[3])
    return None


# =========================================================
# RUTAS PRINCIPALES
# =========================================================
@app.route("/")
def home():
    return render_template("index.html", titulo="Inicio")


@app.route("/about")
def about():
    return render_template("about.html", titulo="Acerca de")


@app.route("/usuario/<nombre>")
def usuario(nombre):
    return render_template("usuario.html", titulo="Usuario", nombre=nombre)


@app.route("/edad/<int:edad>")
def edad(edad):
    return render_template("edad.html", titulo="Edad", edad=edad)


@app.route("/formulario", methods=["GET", "POST"])
def formulario():
    form = FormularioNombre()

    if form.validate_on_submit():
        nombre = form.nombre.data.strip()
        flash(f"POST recibido con éxito ✅ (Nombre: {nombre})", "success")
        return redirect(url_for("formulario"))

    return render_template("formulario.html", titulo="Formulario", form=form)


# =========================================================
# REGISTRO Y LOGIN
# =========================================================
@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = FormularioRegistro()

    if form.validate_on_submit():
        nombre = form.nombre.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id_usuario FROM usuarios WHERE mail = %s", (email,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            flash("Ese correo ya está registrado.", "danger")
            cursor.close()
            conexion.close()
            return redirect(url_for("registro"))

        password_hash = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
            (nombre, email, password_hash)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

        flash("Usuario registrado correctamente. Ahora puede iniciar sesión.", "success")
        return redirect(url_for("login"))

    return render_template("registro.html", titulo="Registro", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = FormularioLogin()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, mail, password FROM usuarios WHERE mail = %s",
            (email,)
        )
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()

        if fila and check_password_hash(fila[3], password):
            usuario = Usuario(fila[0], fila[1], fila[2], fila[3])
            login_user(usuario)
            flash("Inicio de sesión correcto.", "success")
            return redirect(url_for("panel"))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("login.html", titulo="Login", form=form)


@app.route("/panel")
@login_required
def panel():
    return render_template("panel.html", titulo="Panel", usuario=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("login"))


# =========================================================
# CRUD DE PRODUCTOS
# Uso ruta /crud/productos para no chocar con rutas viejas
# =========================================================
@app.route("/crud/productos")
def listar_productos_web():
    productos = listar_productos()
    return render_template("productos/listar.html", productos=productos, titulo="Productos")


@app.route("/crud/productos/nuevo")
def nuevo_producto_web():
    categorias = listar_categorias()
    proveedores = listar_proveedores()
    return render_template(
        "productos/crear.html",
        categorias=categorias,
        proveedores=proveedores,
        errores=[],
        datos={},
        titulo="Nuevo producto"
    )


@app.route("/crud/productos/guardar", methods=["POST"])
def guardar_producto_web():
    nombre = request.form.get("nombre", "").strip()
    precio = request.form.get("precio", "").strip()
    stock = request.form.get("stock", "").strip()
    id_categoria = request.form.get("id_categoria", "").strip()
    id_proveedor = request.form.get("id_proveedor", "").strip()

    errores = validar_datos_producto(nombre, precio, stock, id_categoria, id_proveedor)

    if errores:
        categorias = listar_categorias()
        proveedores = listar_proveedores()
        return render_template(
            "productos/crear.html",
            categorias=categorias,
            proveedores=proveedores,
            errores=errores,
            datos=request.form,
            titulo="Nuevo producto"
        )

    crear_producto(nombre, precio, stock, id_categoria, id_proveedor)
    flash("Producto registrado correctamente.", "success")
    return redirect(url_for("listar_productos_web"))


@app.route("/crud/productos/editar/<int:id_producto>")
def editar_producto_web(id_producto):
    producto = obtener_producto_por_id(id_producto)

    if not producto:
        flash("El producto no existe.", "warning")
        return redirect(url_for("listar_productos_web"))

    categorias = listar_categorias()
    proveedores = listar_proveedores()

    return render_template(
        "productos/editar.html",
        producto=producto,
        categorias=categorias,
        proveedores=proveedores,
        errores=[],
        titulo="Editar producto"
    )


@app.route("/crud/productos/actualizar/<int:id_producto>", methods=["POST"])
def actualizar_producto_web(id_producto):
    nombre = request.form.get("nombre", "").strip()
    precio = request.form.get("precio", "").strip()
    stock = request.form.get("stock", "").strip()
    id_categoria = request.form.get("id_categoria", "").strip()
    id_proveedor = request.form.get("id_proveedor", "").strip()

    errores = validar_datos_producto(nombre, precio, stock, id_categoria, id_proveedor)

    if errores:
        categorias = listar_categorias()
        proveedores = listar_proveedores()

        producto = (
            id_producto,
            nombre,
            precio,
            stock,
            int(id_categoria) if id_categoria.isdigit() else 0,
            int(id_proveedor) if id_proveedor.isdigit() else 0
        )

        return render_template(
            "productos/editar.html",
            producto=producto,
            categorias=categorias,
            proveedores=proveedores,
            errores=errores,
            titulo="Editar producto"
        )

    actualizar_producto(id_producto, nombre, precio, stock, id_categoria, id_proveedor)
    flash("Producto actualizado correctamente.", "success")
    return redirect(url_for("listar_productos_web"))


@app.route("/crud/productos/eliminar/<int:id_producto>")
def confirmar_eliminar_producto_web(id_producto):
    producto = obtener_producto_por_id(id_producto)

    if not producto:
        flash("El producto no existe.", "warning")
        return redirect(url_for("listar_productos_web"))

    return render_template("productos/eliminar.html", producto=producto, titulo="Eliminar producto")


@app.route("/crud/productos/borrar/<int:id_producto>", methods=["POST"])
def borrar_producto_web(id_producto):
    eliminar_producto(id_producto)
    flash("Producto eliminado correctamente.", "info")
    return redirect(url_for("listar_productos_web"))


@app.route("/crud/productos/pdf")
def reporte_productos_pdf():
    productos = listar_productos()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reporte de productos", new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.ln(5)

    pdf.set_font("Arial", "B", 9)
    pdf.cell(12, 8, "ID", border=1)
    pdf.cell(45, 8, "Nombre", border=1)
    pdf.cell(25, 8, "Precio", border=1)
    pdf.cell(20, 8, "Stock", border=1)
    pdf.cell(40, 8, "Categoria", border=1)
    pdf.cell(40, 8, "Proveedor", border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Arial", "", 8)

    for producto in productos:
        pdf.cell(12, 8, limpiar_texto_pdf(producto[0]), border=1)
        pdf.cell(45, 8, limpiar_texto_pdf(producto[1]), border=1)
        pdf.cell(25, 8, limpiar_texto_pdf(producto[2]), border=1)
        pdf.cell(20, 8, limpiar_texto_pdf(producto[3]), border=1)
        pdf.cell(40, 8, limpiar_texto_pdf(producto[4]), border=1)
        pdf.cell(40, 8, limpiar_texto_pdf(producto[5]), border=1, new_x="LMARGIN", new_y="NEXT")

    pdf_bytes = bytes(pdf.output(dest="S"))

    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": "inline; filename=reporte_productos.pdf"}
    )


# =========================================================
# PRUEBA DE CONEXIÓN
# =========================================================
try:
    conexion = obtener_conexion()
    print("Conexión exitosa a MySQL")
    conexion.close()
except Exception as e:
    print("Error de conexion:", e)


if __name__ == "__main__":
    app.run(debug=True)