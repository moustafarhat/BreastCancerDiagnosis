#################
#### imports ####
#################
from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(Form):
    email = StringField('email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('password', validators=[DataRequired()])

