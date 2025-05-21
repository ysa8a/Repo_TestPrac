from flask import request, redirect, render_template, session, Blueprint
from db import get_users_connection, get_data_connection, hash_password
from flask_wtf.csrf import generate_csrf

users_admin_bp = Blueprint('users_admin', __name__)

@users_admin_bp.route('/admin/users')
def admin_users():
    if session.get('role') != 'admin':
        return "Access denied", 403

    conn_u = get_users_connection()
    cur_u = conn_u.cursor()
    cur_u.execute("SELECT * FROM users")
    users = cur_u.fetchall()
    cur_u.close()
    conn_u.close()

    conn_d = get_data_connection()
    cur_d = conn_d.cursor()
    cur_d.execute("SELECT * FROM companies")
    companies = cur_d.fetchall()
    cur_d.close()
    conn_d.close()

    csrf_token = generate_csrf()
    return render_template("admin/admin_users.html", users=users, companies=companies, csrf_token=csrf_token)

@users_admin_bp.route('/admin/users/add', methods=['POST'])
def add_user():
    if session.get('role') != 'admin':
        return "Access denied", 403

    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    company_id = request.form.get('company_id') if role == 'owner' else None

    conn = get_users_connection()
    cur = conn.cursor()

    if company_id:
        cur.execute(
            "INSERT INTO users (username, password, role, company_id) VALUES (%s, %s, %s, %s)",
            (username, hash_password(password), role, company_id)
        )
    else:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hash_password(password), role)
        )

    conn.commit()
    cur.close()
    conn.close()
    return redirect('/admin/users')

@users_admin_bp.route('/admin/users/edit', methods=['POST'])
def edit_user():
    if session.get('role') != 'admin':
        return "Access denied", 403

    username = request.form['username']
    new_role = request.form['role']
    company_id = request.form.get('company_id') if new_role == 'owner' else None

    conn = get_users_connection()
    cur = conn.cursor()

    if company_id:
        cur.execute("UPDATE users SET role = %s, company_id = %s WHERE username = %s", (new_role, company_id, username))
    else:
        cur.execute("UPDATE users SET role = %s, company_id = NULL WHERE username = %s", (new_role, username))

    conn.commit()
    cur.close()
    conn.close()
    return redirect('/admin/users')

@users_admin_bp.route('/admin/users/delete', methods=['POST'])
def delete_user():
    if session.get('role') != 'admin':
        return "Access denied", 403

    username = request.form['username']
    conn = get_users_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = %s", (username,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/admin/users')
