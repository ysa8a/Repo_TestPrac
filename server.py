from flask import Flask
from dotenv import load_dotenv
import os
from flask_wtf import CSRFProtect

from db import ensure_users_table, ensure_data_tables
from routes.home import home_bp
from routes.auth import auth_bp
from routes.companies import companies_bp
from routes.companies_admin import companies_admin_bp
from routes.users_admin import users_admin_bp

# Cargar variables de entorno
load_dotenv()

# Crear instancia de la aplicación
app = Flask(__name__)

# Configuración de seguridad y sesión
app.secret_key = os.getenv('SECRET_KEY', 'supersecret')
app.permanent_session_lifetime = 99999999

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,  # ✅ Solo si usas HTTPS (Render lo usa)
    SESSION_COOKIE_SAMESITE='Lax'
)

# Protección CSRF
csrf = CSRFProtect(app)

# Inicializar base de datos (usuarios y datos)
with app.app_context():
    ensure_users_table()
    ensure_data_tables()

# Registrar Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(companies_bp)
app.register_blueprint(companies_admin_bp)
app.register_blueprint(users_admin_bp)