import os
import json
import csv
from flask import Blueprint, render_template, request, redirect, url_for

from .bd import init_db, get_session
from .productos import Producto

inventario_bp = Blueprint("inventario", __name__)

# --------------------------
# Rutas de archivos (data/)
# --------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

TXT_PATH = os.path.join(DATA_DIR, "datos.txt")
JSON_PATH = os.path.join(DATA_DIR, "datos.json")
CSV_PATH = os.path.join(DATA_DIR, "datos.csv")


def asegurar_data_dir():
    """Crea carpeta data/ y archivos base si no existen."""
    os.makedirs(DATA_DIR, exist_ok=True)

    # TXT: puede estar vacío sin problema
    if not os.path.exists(TXT_PATH):
        open(TXT_PATH, "w", encoding="utf-8").close()

    # JSON: debe iniciar con [] para poder json.load sin error
    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    else:
        # Si existe pero está vacío/corrupto, lo reparamos a []
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                json.load(f)
        except Exception:
            with open(JSON_PATH, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    # CSV: debe tener encabezado
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nombre", "precio", "cantidad"])
            writer.writeheader()
    else:
        # Si existe pero está vacío, ponemos encabezado
        if os.path.getsize(CSV_PATH) == 0:
            with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["nombre", "precio", "cantidad"])
                writer.writeheader()


# --------------------------
# Funciones TXT
# --------------------------
def guardar_en_txt(d: dict):
    """Guarda una línea con formato: nombre|precio|cantidad"""
    with open(TXT_PATH, "a", encoding="utf-8") as f:
        f.write(f"{d['nombre']}|{d['precio']}|{d['cantidad']}\n")


def leer_txt():
    datos = []
    with open(TXT_PATH, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split("|")
            if len(partes) == 3:
                datos.append({"nombre": partes[0], "precio": partes[1], "cantidad": partes[2]})
    return datos


# --------------------------
# Funciones JSON
# --------------------------
def guardar_en_json(d: dict):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        lista = json.load(f)
    lista.append(d)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)


def leer_json():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------
# Funciones CSV
# --------------------------
def guardar_en_csv(d: dict):
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nombre", "precio", "cantidad"])
        writer.writerow(d)


def leer_csv():
    datos = []
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            datos.append(row)
    return datos


# --------------------------
# Rutas Flask
# --------------------------
@inventario_bp.route("/datos", methods=["GET", "POST"])
def datos():
    """
    - Recibe datos de formulario
    - Guarda en TXT/JSON/CSV
    - Guarda también en SQLite con SQLAlchemy
    - Muestra lectura de cada formato en datos.html
    """
    asegurar_data_dir()
    init_db()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        precio_txt = request.form.get("precio", "").strip()
        cantidad_txt = request.form.get("cantidad", "").strip()

        # Validación mínima
        if nombre and precio_txt and cantidad_txt:
            # Guardado en archivos tal cual (texto)
            registro_archivo = {"nombre": nombre, "precio": precio_txt, "cantidad": cantidad_txt}
            guardar_en_txt(registro_archivo)
            guardar_en_json(registro_archivo)
            guardar_en_csv(registro_archivo)

            # Guardado en DB (numérico) - acepta coma o punto
            precio_norm = precio_txt.replace(",", ".")
            try:
                precio_num = float(precio_norm)
                cantidad_num = int(cantidad_txt)

                session = get_session()
                p = Producto(nombre=nombre, precio=precio_num, cantidad=cantidad_num)
                session.add(p)
                session.commit()
                session.close()
            except ValueError:
                # Si meten "0,9a" o algo inválido: igual quedan archivos guardados,
                # pero no se inserta en DB para no romper la app.
                pass

        return redirect(url_for("inventario.datos"))

    return render_template(
        "datos.html",
        datos_txt=leer_txt(),
        datos_json=leer_json(),
        datos_csv=leer_csv()
    )


@inventario_bp.route("/productos")
def productos():
    """Lista productos desde SQLite (SQLAlchemy ORM)."""
    init_db()
    session = get_session()
    lista = session.query(Producto).order_by(Producto.id.desc()).all()
    session.close()
    return render_template("productos.html", productos=lista)


@inventario_bp.route("/productos/nuevo", methods=["GET", "POST"])
def producto_nuevo():
    """Formulario para crear producto directo en SQLite (ORM)."""
    init_db()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        precio_txt = request.form.get("precio", "").strip().replace(",", ".")
        cantidad_txt = request.form.get("cantidad", "").strip()

        if nombre and precio_txt and cantidad_txt:
            try:
                precio_num = float(precio_txt)
                cantidad_num = int(cantidad_txt)

                session = get_session()
                p = Producto(nombre=nombre, precio=precio_num, cantidad=cantidad_num)
                session.add(p)
                session.commit()
                session.close()
            except ValueError:
                pass

        return redirect(url_for("inventario.productos"))

    return render_template("producto_form.html")