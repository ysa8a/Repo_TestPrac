from flask import Flask
from dotenv import load_dotenv
import os
from flask_wtf import CSRFProtect

# Load environment variables
load_dotenv()

# Configurar la app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = 99999999
csrf = CSRFProtect(app)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

# 📌 Importa y registra el Blueprint de auth
from routes.auth import auth_bp
app.register_blueprint(auth_bp)
# 📌 Importa y registra el Blueprint de companies   
from routes.companies import companies_bp
app.register_blueprint(companies_bp)
# 📌 Importa y registra el Blueprint de user

