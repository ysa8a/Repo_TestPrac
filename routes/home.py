from flask import redirect
from server import app

@app.route('/')
def index():
    return redirect('/login')
