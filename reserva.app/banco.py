import sqlite3

def conectar():
    return sqlite3.connect("reservas.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        sala TEXT,
        data TEXT,
        hora_inicio TEXT,
        hora_fim TEXT,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)
    
    conn.commit()
    conn.close()
