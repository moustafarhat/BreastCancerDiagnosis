#################
#### imports ####
#################
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from ..models import User , Patient, db,Patient_Informations
from WebService import app
from flask_wtf import Form
from wtforms import DateField, TextField, DecimalField, HiddenField, validators
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from datetime import date, datetime


class PredictionForm(Form):
    clump_thickness = TextField('clump_thickness', validators=[DataRequired()])
    uniformity_cell_size = TextField('uniformity_cell_size', validators=[DataRequired()])
    uniformity_cell_shape = TextField('uniformity_cell_shape', validators=[DataRequired()])
    marginal_adhesion = TextField('marginal_adhesion', validators=[DataRequired()])
    single_epithelial_cell_size = TextField('single_epithelial_cell_size', validators=[DataRequired()])
    bare_nuclei = TextField('bare_nuclei', validators=[DataRequired()])
    bland_chromatin = TextField('bland_chromatin', validators=[DataRequired()])
    normal_nucleoli = TextField('normal_nucleoli', validators=[DataRequired()])
    mitoses = TextField('mitoses', validators=[DataRequired()])

class ResultForm(Form):
    result1_id = HiddenField('result1_id')
    result2_id = HiddenField('result2_id')