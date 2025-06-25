from flask import Flask, request
import pyodbc
import os
from datetime import datetime

app = Flask(__name__)

# 🔒 Conexión usando variables de entorno
def conectar_sql():
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.environ['SQL_SERVER']};"
        f"DATABASE={os.environ['SQL_DATABASE']};"
        f"UID={os.environ['SQL_USER']};"
        f"PWD={os.environ['SQL_PASSWORD']}"
    )

# 📥 Endpoint para registrar un nuevo discípulo
@app.route('/nuevo-discipulo', methods=['POST'])
def nuevo_discipulo():
    data = request.get_json()
    print("📦 JSON recibido:", data)

    if not data:
        return "No se recibió JSON válido", 400

    print("🧾 Campos recibidos:")
    print("🔹 idDiscipulo:", data.get("idDiscipulo"))
    print("🔹 nombre_completo:", data.get("nombre_completo"))
    print("🔹 fecha_nacimiento:", data.get("fecha_nacimiento"))
    print("🔹 fecha_ingreso:", data.get("fecha_ingreso"))

    conn = None
    try:
        conn = conectar_sql()
        cursor = conn.cursor()

        id_discipulo = str(data.get("idDiscipulo"))
        nombre = str(data.get("nombre_completo"))
        fecha_nacimiento = datetime.strptime(data.get("fecha_nacimiento"), "%Y-%m-%d").date()
        fecha = datetime.strptime(data.get("fecha_ingreso"), "%Y-%m-%d").date()

        cursor.execute("""
            INSERT INTO Discipulo (idDiscipulo, nombrecompleto, fecha_nacimiento, fechaingreso)
            VALUES (?, ?, ?, ?)
        """, id_discipulo, nombre, fecha_nacimiento, fecha)

        conn.commit()
        print("✅ Inserción en tabla Discipulo completada")
        return 'Discípulo registrado correctamente', 200

    except Exception as e:
        if conn:
            conn.rollback()
        print("❌ Error al registrar discípulo:", e)
        return f'Error al registrar discípulo: {e}', 400

    finally:
        if conn:
            conn.close()

# 📅 Endpoint para registrar asistencia
@app.route('/registrar-asistencia', methods=['POST'])
def registrar_asistencia():
    data = request.get_json()
    print("📅 JSON de asistencia recibido:", data)

    if not data:
        return "No se recibió JSON válido", 400

    print("🧾 Campos recibidos:")
    print("🔹 idDiscipulo:", data.get("idDiscipulo"))
    print("🔹 fecha_asistencia:", data.get("fecha_asistencia"))

    conn = None
    try:
        conn = conectar_sql()
        cursor = conn.cursor()

        id_discipulo = str(data.get("idDiscipulo"))
        fecha_asistencia = datetime.strptime(data.get("fecha_asistencia"), "%Y-%m-%d").date()

        cursor.execute("""
            INSERT INTO Asistencia (idDiscipulo, fecha_asistencia)
            VALUES (?, ?)
        """, id_discipulo, fecha_asistencia)

        conn.commit()
        print("✅ Inserción en tabla Asistencia completada")
        return 'Asistencia registrada correctamente', 200

    except Exception as e:
        if conn:
            conn.rollback()
        print("❌ Error al registrar asistencia:", e)
        return f'Error al registrar asistencia: {e}', 400

    finally:
        if conn:
            conn.close()

# 🌐 Habilitar host 0.0.0.0 en caso de que Render lo requiera
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
