#################
#### imports ####
#################

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from ..models import User , Patient, db
from WebService import app
from flask_wtf import Form
from wtforms import DateField, TextField
from datetime import date, datetime

class DateForm(Form):
    dt = DateField('Pick a Date', format="%d-%m-%Y")
    firstname = TextField()
    lastname = TextField()
    address = TextField()
    city = TextField()
    email = TextField()
    phone = TextField()