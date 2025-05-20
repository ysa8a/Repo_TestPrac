from flask import request, redirect, render_template, session
from db import get_connection, verify_password  # Asegúrate de tener estas funciones en db/__init__.py
from server import app

@app.route('/login', methods=['GET', 'POST'])  # ✅ Acepta POST
def login():
    if 'username' in session:
        return redirect('/companies')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cur = conn.cursor()

        # Consulta segura
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        # Verificación segura
        if user and verify_password(user['password'], password):
            session['username'] = user['username']
            session['role'] = user['role']
            session['company_id'] = user['company_id']
            return redirect('/companies')
        else:
            return render_template('auth/login.html', error="Invalid username or password")

    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
