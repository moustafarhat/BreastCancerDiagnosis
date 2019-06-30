#################
#### imports ####
#################
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from WebService import app
from flask_login import LoginManager
from enum import Enum

################
#### config ####
################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'DB\DataBase.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Permission(Enum):
    Admin = 0
    Doctor = 1
    Other = 2

#login = LoginManager(app)





