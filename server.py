from flask import Flask
from dotenv import load_dotenv
import os
from flask_wtf import CSRFProtect

def create_app():
    """
    Create and configure the Flask application.
    """
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    app.permanent_session_lifetime = 99999999
    CSRFProtect(app)

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_SAMESITE='Lax'
    )

    # 📌 Importa rutas para registrarlas
    from routes import home, auth, companies, companies_admin, users_admin

    return app

