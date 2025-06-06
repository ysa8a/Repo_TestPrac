import sqlite3
import os
import bcrypt
 
DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'db')
USERS_DB = os.path.join(DB_DIR, 'users.db')
DATA_DB = os.path.join(DB_DIR, 'data.db')
 
# Hash seguro con bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode('utf-8')
 
def verify_password(stored_hash, password):
    return bcrypt.checkpw(password.encode(), stored_hash.encode())
 
def ensure_users_db():
    ensure_data_db()
 
    if not os.path.exists(USERS_DB):
        os.makedirs(DB_DIR, exist_ok=True)
        conn = sqlite3.connect(USERS_DB)
        c = conn.cursor()
        c.execute("""CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            company_id INTEGER
        )""")
        users = [
            ('alice', hash_password('password1'), 'user', None),
            ('bob', hash_password('password2'), 'owner', 1),
            ('admin', hash_password('admin123'), 'admin', None)
        ]
        c.executemany("INSERT INTO users (username, password, role, company_id) VALUES (?, ?, ?, ?)", users)
        conn.commit()
        conn.close()
 
def ensure_data_db():
    if not os.path.exists(DATA_DB):
        os.makedirs(DB_DIR, exist_ok=True)
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute("""CREATE TABLE companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            owner TEXT
        )""")
        c.execute("""CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            user TEXT,
            comment TEXT
        )""")
 
        # Empresas y comentarios
        c.execute("INSERT INTO companies (name, description, owner) VALUES ('Insegura Corp', 'A very insecure company.', 'bob')")
        c.execute("INSERT INTO comments (company_id, user, comment) VALUES (1, 'alice', 'This company is extremely insecure!')")
        c.execute("INSERT INTO comments (company_id, user, comment) VALUES (1, 'admin', 'I agree, there are many vulnerabilities here.')")
        c.execute("INSERT INTO comments (company_id, user, comment) VALUES (1, 'bob', 'We need to improve security immediately.')")
 
        c.execute("INSERT INTO companies (name, description, owner) VALUES ('Flameera', 'A cutting-edge company with top security measures.', 'bob')")
        c.execute("INSERT INTO comments (company_id, user, comment) VALUES (2, 'alice', 'Flameera is doing great with security!')")
        c.execute("INSERT INTO comments (company_id, user, comment) VALUES (2, 'admin', 'Top-tier measures! I recommend this company for security.')")
        c.execute("INSERT INTO comments (company_id, user, comment) VALUES (2, 'bob', 'Our security is state-of-the-art! Flameera is the future.')")
 
        conn.commit()
        conn.close()
 
def get_users_connection():
    ensure_users_db()
    conn = sqlite3.connect(USERS_DB)
    conn.row_factory = sqlite3.Row
    return conn
 
def get_data_connection():
    ensure_data_db()
    conn = sqlite3.connect(DATA_DB)
    conn.row_factory = sqlite3.Row
    return conn
