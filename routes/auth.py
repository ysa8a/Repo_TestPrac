# routes/auth.py

from flask import Blueprint, request, render_template, redirect, session
from db import get_users_connection, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/companies')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_users_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and verify_password(user['password'], password):
            session['username'] = user['username']
            session['role'] = user['role']
            session['company_id'] = user['company_id']
            return redirect('/companies')

        return render_template('auth/login.html', error="Invalid username or password")
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
