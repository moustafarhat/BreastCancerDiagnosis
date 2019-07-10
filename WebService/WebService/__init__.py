#################
#### imports ####
#################

from flask import Flask, redirect, url_for
from flask_login import LoginManager

import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

#import WebService.main
#import WebService.auth


####################
#### extensions ####
####################
login = LoginManager()
login.init_app(app)

####################
#### flask-login ####
####################

from  .models import User


@login.user_loader
def load_user(user_id):
     return User.query.filter(User.user_id == int(user_id)).first()

@login.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login_post'))


####################
#### blueprints ####
####################
#Register blueprints here

from .Auth.views import users_blueprint
from .ML_Predictor.views import Predictor_blueprint
from .Patients.views import Patients_blueprint
from .Foundations.views import Foundations_blueprint