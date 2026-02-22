from flask import Flask, render_template, request

app = Flask(__name__)

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
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        return render_template("formulario.html", titulo="Formulario", mensaje=f"POST recibido con éxito ✅ (Nombre: {nombre})")
    return render_template("formulario.html", titulo="Formulario")

if __name__ == "__main__":
    app.run(debug=True)