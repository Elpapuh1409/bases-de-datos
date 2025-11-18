import sqlite3
from contextlib import closing

DB_PATH = 'inventario.db'

# Estructura de la base de datos (puedes modificar según tus necesidades)
TABLES = {
    'inventario': '''
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            responsable TEXT NOT NULL,
            marca TEXT NOT NULL,
            equipo TEXT NOT NULL,
            serie TEXT,
            fecha_ingreso TEXT,
            fecha_salida TEXT,
            proceso TEXT,
            valor REAL,
            observaciones TEXT,
            estado TEXT,
            progreso INTEGER
        );
    '''
}

def inicializar_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        for table_sql in TABLES.values():
            c.execute(table_sql)
        conn.commit()

def agregar_item(responsable, marca, equipo, serie, fecha_ingreso, fecha_salida, proceso, valor, observaciones, estado, progreso):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO inventario (responsable, marca, equipo, serie, fecha_ingreso, fecha_salida, proceso, valor, observaciones, estado, progreso)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (responsable, marca, equipo, serie, fecha_ingreso, fecha_salida, proceso, valor, observaciones, estado, progreso))
        conn.commit()
        return c.lastrowid

def obtener_items():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM inventario')
        return c.fetchall()

def buscar_item_por_id(item_id):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM inventario WHERE id = ?', (item_id,))
        return c.fetchone()

def actualizar_item(item_id, **kwargs):
    campos = ', '.join([f"{k} = ?" for k in kwargs.keys()])
    valores = list(kwargs.values())
    valores.append(item_id)
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute(f'UPDATE inventario SET {campos} WHERE id = ?', valores)
        conn.commit()

def eliminar_item(item_id):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM inventario WHERE id = ?', (item_id,))
        conn.commit()

# Inicializa la base de datos al importar el módulo
inicializar_db()
