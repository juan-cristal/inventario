import sqlite3
from pathlib import Path

DB_FOLDER = Path(__file__).parent / "database"
DB_FOLDER.mkdir(exist_ok=True)   # Ensures folder exists

DB_PATH = DB_FOLDER / "inventario.db"


# ---------------------------------------------
# Database Utilities
# ---------------------------------------------

def get_conn():
    """Return a new SQLite connection using the project DB path."""
    return sqlite3.connect(DB_PATH)


def crear_base():
    """Create the database and table if they don’t exist."""
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
        """)


# ---------------------------------------------
# CRUD Operations
# ---------------------------------------------

def agregar_producto(nombre, descripcion, cantidad, precio, categoria):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, descripcion, cantidad, precio, categoria))


def obtener_todos():
    with get_conn() as conn:
        return conn.execute("SELECT * FROM productos").fetchall()


def buscar_por_id(pid):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM productos WHERE id = ?",
            (pid,)
        ).fetchone()


def actualizar_producto(pid, nombre, descripcion, cantidad, precio, categoria):
    with get_conn() as conn:
        conn.execute("""
            UPDATE productos
            SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
            WHERE id = ?
        """, (nombre, descripcion, cantidad, precio, categoria, pid))


def eliminar_producto(pid):
    with get_conn() as conn:
        conn.execute("DELETE FROM productos WHERE id = ?", (pid,))


def obtener_bajo_stock(limite):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM productos WHERE cantidad <= ?",
            (limite,)
        ).fetchall()


# ---------------------------------------------
# Initialize DB automatically
# ---------------------------------------------

crear_base()
18