from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Semana 9 ok ✅"

@app.route("/about")
def about():
    return "Acerca de (ruta simple)"

@app.route("/usuario/<nombre>")
def usuario(nombre):
    return f"Hola, {nombre} (ruta dinámica)"

@app.route("/edad/<int:edad>")
def edad(edad):
    return f"Tienes {edad} años"

@app.route("/formulario", methods=["GET", "POST"])
def formulario():
    if request.method == "POST":
        return "POST recibido con éxito ✅"
    return "GET (solo visita)"

if __name__ == "__main__":
    app.run(debug=True)
