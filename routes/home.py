from flask import render_template

def register_home(app):
    @app.route('/')
    def index():
        return render_template('auth/login.html')
