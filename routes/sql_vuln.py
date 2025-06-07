# routes/sql_vuln.py
import sqlite3
from flask import Blueprint, request

sql_vuln = Blueprint('sql_vuln', __name__)

@sql_vuln.route('/vulnerable_login', methods=['POST'])
def vulnerable_login():
    username = request.form.get('username')
    password = request.form.get('password')

    #  VULNERABLE: SQL concatenation sin parámetros seguros
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(query)  # 💥 vulnerable a inyecciones SQL
    user = cursor.fetchone()
    conn.close()

    if user:
        return "Login exitoso"
    else:
        return "Credenciales inválidas"
