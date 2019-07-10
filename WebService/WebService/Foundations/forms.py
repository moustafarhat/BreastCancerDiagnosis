#################
#### imports ####
#################

from flask import Blueprint, render_template, redirect, url_for, request, flash
from WebService import app
from flask_wtf import Form
from wtforms import DateField, TextField, DecimalField, HiddenField, validators
from wtforms.validators import DataRequired

class FoundationForm(Form):
    fnd_id = HiddenField('fnd_id')
    name = TextField('name', validators=[DataRequired()])