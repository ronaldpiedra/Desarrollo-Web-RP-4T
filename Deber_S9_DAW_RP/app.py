from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from forms import FormularioNombre, FormularioRegistro, FormularioLogin
from inventario.inventario import inventario_bp
from Conexion.conexion import obtener_conexion
from models import Usuario

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave_segura_123"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debe iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"

app.register_blueprint(inventario_bp)

@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id_usuario, nombre, mail, pasword FROM usuarios WHERE id_usuario = %s",
        (user_id,)
    )
    fila = cursor.fetchone()
    cursor.close()
    conexion.close()

    if fila:
        return Usuario(fila[0], fila[1], fila[2], fila[3])
    return None

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
            "INSERT INTO usuarios (nombre, mail, pasword) VALUES (%s, %s, %s)",
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
            "SELECT id_usuario, nombre, mail, pasword FROM usuarios WHERE mail = %s",
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

try:
    conexion = obtener_conexion()
    print("Conexión exitosa a MySQL")
    conexion.close()
except Exception as e:
    print("Error de conexion:", e)

if __name__ == "__main__":
    app.run(debug=True)