import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import bcrypt

# Cargar las variables de entorno (funciona en local si usas .env)
load_dotenv()

# 🔗 Conexión general
def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)

# ✅ Hash seguro con bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode('utf-8')

def verify_password(stored_hash, password):
    return bcrypt.checkpw(password.encode(), stored_hash.encode())

# ✅ Crear tabla users si no existe
def ensure_users_table():
    conn = get_connection()
    cur = conn.cursor()

    # Crear tabla si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT,
            company_id INTEGER
        );
    """)

    # Insertar datos solo si está vacía
    cur.execute("SELECT COUNT(*) FROM users;")
    if cur.fetchone()['count'] == 0:
        users = [
            ('alice', hash_password('password1'), 'user', None),
            ('bob', hash_password('password2'), 'owner', 1),
            ('admin', hash_password('admin123'), 'admin', None)
        ]
        for u in users:
            cur.execute("INSERT INTO users (username, password, role, company_id) VALUES (%s, %s, %s, %s)", u)

    conn.commit()
    cur.close()
    conn.close()

# ✅ Crear tabla companies y comments si no existen
def ensure_data_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name TEXT,
            description TEXT,
            owner TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            company_id INTEGER,
            "user" TEXT,
            comment TEXT
        );
    """)

    # Verificar si hay datos ya insertados
    cur.execute("SELECT COUNT(*) FROM companies;")
    if cur.fetchone()['count'] == 0:
        # Insertar empresas
        cur.execute("INSERT INTO companies (name, description, owner) VALUES ('Insegura Corp', 'A very insecure company.', 'bob') RETURNING id;")
        c1_id = cur.fetchone()['id']

        cur.execute("INSERT INTO companies (name, description, owner) VALUES ('Flameera', 'Top security company.', 'bob') RETURNING id;")
        c2_id = cur.fetchone()['id']

        # Comentarios
        cur.execute("INSERT INTO comments (company_id, user, comment) VALUES (%s, %s, %s)", (c1_id, 'alice', 'This company is extremely insecure!'))
        cur.execute("INSERT INTO comments (company_id, user, comment) VALUES (%s, %s, %s)", (c1_id, 'admin', 'Agreed, very vulnerable.'))
        cur.execute("INSERT INTO comments (company_id, user, comment) VALUES (%s, %s, %s)", (c1_id, 'bob', 'Improvement needed.'))

        cur.execute("INSERT INTO comments (company_id, user, comment) VALUES (%s, %s, %s)", (c2_id, 'alice', 'Excellent security.'))
        cur.execute("INSERT INTO comments (company_id, user, comment) VALUES (%s, %s, %s)", (c2_id, 'admin', 'Highly recommended.'))
        cur.execute("INSERT INTO comments (company_id, user, comment) VALUES (%s, %s, %s)", (c2_id, 'bob', 'Flameera is the future.'))

    conn.commit()
    cur.close()
    conn.close()
