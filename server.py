from flask import Flask
from dotenv import load_dotenv
import os
from flask_wtf import CSRFProtect

# Load environment variables from .env file
load_dotenv()
# Set the Flask app configuration

def create_app():
    """
    Create and configure the Flask application.
    """
    # Load environment variables
    load_dotenv()

    # Initialize the Flask app
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')  # Cargada de forma segura
    app.permanent_session_lifetime = 99999999
    csrf = CSRFProtect(app)
    from routes.home import register_home
    register_home(app)
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=True,  # ✅ Solo si estás usando HTTPS
        SESSION_COOKIE_SAMESITE='Lax'
    )

    return app