import os
import json
import csv
from flask import Blueprint, render_template, request, redirect, url_for

from Conexion.conexion import obtener_conexion

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

    # TXT
    if not os.path.exists(TXT_PATH):
        open(TXT_PATH, "w", encoding="utf-8").close()

    # JSON
    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    else:
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                json.load(f)
        except Exception:
            with open(JSON_PATH, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    # CSV
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nombre", "precio", "cantidad"])
            writer.writeheader()
    else:
        if os.path.getsize(CSV_PATH) == 0:
            with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["nombre", "precio", "cantidad"])
                writer.writeheader()


# --------------------------
# Funciones TXT
# --------------------------
def guardar_en_txt(d: dict):
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
                datos.append(
                    {
                        "nombre": partes[0],
                        "precio": partes[1],
                        "cantidad": partes[2]
                    }
                )
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
    Guarda y muestra datos en TXT, JSON y CSV.
    """
    asegurar_data_dir()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        precio_txt = request.form.get("precio", "").strip()
        cantidad_txt = request.form.get("cantidad", "").strip()

        if nombre and precio_txt and cantidad_txt:
            registro_archivo = {
                "nombre": nombre,
                "precio": precio_txt,
                "cantidad": cantidad_txt
            }

            guardar_en_txt(registro_archivo)
            guardar_en_json(registro_archivo)
            guardar_en_csv(registro_archivo)

        return redirect(url_for("inventario.datos"))

    return render_template(
        "datos.html",
        datos_txt=leer_txt(),
        datos_json=leer_json(),
        datos_csv=leer_csv()
    )


@inventario_bp.route("/productos")
def productos():
    """Lista productos desde MySQL."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos ORDER BY id_producto DESC")
    lista = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("productos.html", productos=lista)


@inventario_bp.route("/productos/nuevo", methods=["GET", "POST"])
def producto_nuevo():
    """Formulario para crear producto en MySQL."""
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        precio_txt = request.form.get("precio", "").strip().replace(",", ".")
        stock_txt = request.form.get("stock", "").strip()

        if nombre and precio_txt and stock_txt:
            try:
                precio_num = float(precio_txt)
                stock_num = int(stock_txt)

                conexion = obtener_conexion()
                cursor = conexion.cursor()

                sql = """
                    INSERT INTO productos (nombre, descripcion, precio, stock)
                    VALUES (%s, %s, %s, %s)
                """
                valores = (nombre, descripcion, precio_num, stock_num)

                cursor.execute(sql, valores)
                conexion.commit()

                cursor.close()
                conexion.close()

            except ValueError:
                pass

        return redirect(url_for("inventario.productos"))

    return render_template("producto_form.html", producto=None, editar=False)


@inventario_bp.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
def producto_editar(id_producto):
    """Edita un producto en MySQL."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        precio_txt = request.form.get("precio", "").strip().replace(",", ".")
        stock_txt = request.form.get("stock", "").strip()

        if nombre and precio_txt and stock_txt:
            try:
                precio_num = float(precio_txt)
                stock_num = int(stock_txt)

                sql = """
                    UPDATE productos
                    SET nombre = %s, descripcion = %s, precio = %s, stock = %s
                    WHERE id_producto = %s
                """
                valores = (nombre, descripcion, precio_num, stock_num, id_producto)

                cursor.execute(sql, valores)
                conexion.commit()

                cursor.close()
                conexion.close()

                return redirect(url_for("inventario.productos"))
            except ValueError:
                pass

    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template("producto_form.html", producto=producto, editar=True)


@inventario_bp.route("/productos/eliminar/<int:id_producto>")
def producto_eliminar(id_producto):
    """Elimina un producto en MySQL."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect(url_for("inventario.productos"))