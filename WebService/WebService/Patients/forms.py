#################
#### imports ####
#################

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from ..models import User , Patient, db
from WebService import app
from flask_wtf import Form
from wtforms import DateField, TextField, DecimalField, validators
from wtforms.validators import DataRequired, Length, EqualTo, Email
from datetime import date, datetime

class DateForm(Form):
    dt = DateField('Pick a Date', format="%d-%m-%Y", validators=[DataRequired()])
    firstname = TextField('firstname', validators=[DataRequired()])
    lastname = TextField('lastname', validators=[DataRequired()])
    address = TextField('address')
    city = TextField('city')
    email = TextField('email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    phone = DecimalField('phone')