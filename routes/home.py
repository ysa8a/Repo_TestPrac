from flask import redirect
from flask import current_app as app

@app.route('/')
def index():
    return redirect('/login')
