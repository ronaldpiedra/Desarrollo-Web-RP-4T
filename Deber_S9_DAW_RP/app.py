from flask import Flask, render_template, flash, redirect, url_for
from forms import FormularioNombre

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave_segura_123"

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

if __name__ == "__main__":
    app.run(debug=True)