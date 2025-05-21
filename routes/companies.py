from flask import request, redirect, render_template, session, Blueprint
from db import get_connection

companies_bp = Blueprint('companies', __name__)

@companies_bp.route('/')
def index():
    return redirect('/login')

@companies_bp.route('/companies')
def list_companies():
    if 'username' not in session:
        return redirect('/login')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies")
    companies = cur.fetchall()

    companies_list = []
    for company in companies:
        company_dict = dict(company)
        cur.execute("SELECT COUNT(*) FROM comments WHERE company_id = %s", (company_dict['id'],))
        company_dict['comment_count'] = int(cur.fetchone()['count'])
        companies_list.append(company_dict)

    cur.close()
    conn.close()
    return render_template('companies/home.html', companies=companies_list)

@companies_bp.route('/companies/<int:company_id>', methods=['GET', 'POST'])
def company_detail(company_id):
    if 'username' not in session:
        return redirect('/login')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies WHERE id = %s", (company_id,))
    company = cur.fetchone()

    cur.execute("SELECT * FROM comments WHERE company_id = %s", (company_id,))
    comments = cur.fetchall()

    if request.method == 'POST':
        comment = request.form['comment']
        user = session.get('username')
        cur.execute('INSERT INTO comments (company_id, "user", comment) VALUES (%s, %s, %s)', (company_id, user, comment))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(f'/companies/{company_id}')

    cur.close()
    conn.close()
    if not company:
        return "Company not found", 404
    return render_template('companies/company.html', company=company, comments=comments)

@companies_bp.route('/companies/register', methods=['GET', 'POST'])
def register_company():
    if session.get('role') != 'owner':
        return "Access denied", 403

    if request.method == 'POST':
        company_name = request.form['company_name']
        description = request.form['description']
        owner = session.get('username')

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO companies (name, description, owner) VALUES (%s, %s, %s)", (company_name, description, owner))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/companies')

    return render_template('companies/register_company.html')

@companies_bp.route('/companies/<int:company_id>/edit', methods=['GET', 'POST'])
def edit_company(company_id):
    if 'username' not in session:
        return redirect('/')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies WHERE id = %s", (company_id,))
    company = cur.fetchone()

    if not company:
        cur.close()
        conn.close()
        return "Company not found", 404

    if session.get('role') != 'admin' and session.get('username') != company['owner']:
        cur.close()
        conn.close()
        return "Access denied", 403

    if request.method == 'POST':
        new_name = request.form['company_name']
        new_description = request.form['description']
        cur.execute("UPDATE companies SET name = %s, description = %s WHERE id = %s", (new_name, new_description, company_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/companies')

    cur.close()
    conn.close()
    return render_template('companies/edit_company.html', company=company)
