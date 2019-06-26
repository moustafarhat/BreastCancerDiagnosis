#################
#### imports ####
#################
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from WebService import app
from flask_login import LoginManager


################
#### config ####
################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'DB\DataBase.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


#login = LoginManager(app)





