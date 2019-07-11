
#################
#### imports ####
#################

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_login import LoginManager
from ..models import User, Foundations
from WebService import app
from ..models import db
from .forms import LoginForm

################
#### config ####
################

users_blueprint = Blueprint('users', __name__)


################
#### routes ####
################



@app.route('/login', methods=["GET", "POST"])
def login_post():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(email=email).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            flash('Thanks for logging in, {}'.format(user.email))
            return redirect(url_for('result'))
        else:
            flash('ERROR! Incorrect login credentials.')
    return render_template('login.html', form=form)


@app.route('/signup')
@login_required
def signup():
    all_groups = Foundations.query.all()
    return render_template('signup.html', allgroups = all_groups)

@app.route('/signup', methods=['POST'])
@login_required
def signup_post():

    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    group_id = request.form.get('group')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(first_name = first_name, last_name = last_name, email=email, password=generate_password_hash(password, method='sha256'),foundation_id = group_id)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('get_patients'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye!', 'info')
    return redirect(url_for('login_post'))

