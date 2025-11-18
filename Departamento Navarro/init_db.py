import sqlite3

# Crear conexión y cursor
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Crear tabla de usuarios
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Insertar un usuario de prueba (puedes quitar esto luego)
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', '1234'))

# Guardar cambios y cerrar
conn.commit()
conn.close()

print("Base de datos creada con usuario 'admin' y contraseña '1234'")
