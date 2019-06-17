#################
#### imports ####
#################
from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired()])

