# main.py

from flask import Blueprint
#from . import db
from WebService import app

main = Blueprint('main', __name__)

@app.route('/')
def index():
    return 'Index'

@app.route('/profile')
def profile():
    return 'Profile'