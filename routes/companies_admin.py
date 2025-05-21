from flask import request, redirect, render_template, session, Blueprint
from flask_wtf.csrf import generate_csrf
from db import get_connection

companies_admin_bp = Blueprint('companies_admin', __name__)

@companies_admin_bp.route('/admin/companies')
def admin_list_companies():
    if session.get('role') != 'admin':
        return "Access denied", 403

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies")
    companies = cur.fetchall()
    cur.close()
    conn.close()

    csrf_token = generate_csrf()
    return render_template('admin/admin_companies.html', companies=companies, csrf_token=csrf_token)

@companies_admin_bp.route('/admin/companies/add', methods=['GET', 'POST'])
def admin_add_company():
    if session.get('role') != 'admin':
        return "Access denied", 403

    if request.method == 'POST':
        company_name = request.form['company_name']
        owner = request.form['owner']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO companies (name, owner) VALUES (%s, %s)", (company_name, owner))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/admin/companies')

    return render_template('admin/admin_companies.html')

@companies_admin_bp.route('/admin/companies/delete', methods=['POST'])
def delete_company():
    if session.get('role') != 'admin':
        return "Access denied", 403

    company_id = request.form['company']

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM companies WHERE id = %s", (company_id,))
    cur.execute("DELETE FROM comments WHERE company_id = %s", (company_id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect('/admin/companies')
