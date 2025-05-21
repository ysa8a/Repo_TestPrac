from flask import Blueprint, redirect

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return redirect('/login')
