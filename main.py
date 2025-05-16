from fastapi import FastAPI
import psycopg2
from typing import Optional

def get_connection():
    try:
        connection = psycopg2.connect(
            dbname="sistema_recargas_viajes",
            user="admin",
            password="Pass!__2025!",
            host="149.130.169.172",
            port="33333"
        )
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

app = FastAPI()

@app.get("/users/count")
def get_user_count():
    conn = get_connection()
    if conn is None:
        return {"error": "Failed to connect to the database"}
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios;")
    total_users = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"total_users": total_users}

@app.get("/users/active/count")
def get_active_user_count():
    conn = get_connection()
    if conn is None:
        return {"error": "Failed to connect to the database"}
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT u.usuario_id) FROM usuarios u INNER JOIN tarjetas t ON u.usuario_id = t.usuario_id WHERE t.estado = 'Activa';")
    total_active_users = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"total_active_users": total_active_users}

@app.get("/users/latest")
def get_latest_user():
    conn = get_connection()
    if conn is None:
        return {"error": "Failed to connect to the database"}
    cursor = conn.cursor()
    cursor.execute("SELECT usuario_id, nombre, apellido FROM usuarios ORDER BY fecha_registro DESC LIMIT 1;")
    latest_user = cursor.fetchone()
    cursor.close()
    conn.close()
    if latest_user:
        return {"usuario_id": latest_user[0], "nombre_completo": f"{latest_user[1]} {latest_user[2]}"}
    else:
        return {"message": "No users found"}

@app.get("/trips/total")
def get_total_trips():
    conn = get_connection()
    if conn is None:
        return {"error": "Failed to connect to the database"}
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM viajes;")
    total_trips = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"total_trips": total_trips}

@app.get("/finance/revenue")
def get_total_revenue():
    conn = get_connection()
    if conn is None:
        return {"error": "Failed to connect to the database"}
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(t.valor) FROM viajes v INNER JOIN tarifas t ON v.tarifa_id = t.tarifa_id;")
    total_revenue = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if total_revenue is not None:
        return {"total_revenue": total_revenue}
    else:
        return {"total_revenue": 0}
 
