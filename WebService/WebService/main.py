# main.py

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from .models import User , Patient, db
from WebService import app
from flask_wtf import Form
from wtforms import DateField
from datetime import date, datetime

class DateForm(Form):
    dt = DateField('Pick a Date', format="%d-%m-%Y")

@app.route('/')
def index():
    return redirect(url_for('get_patients'))

@app.route('/patients')
def get_patients():
    all_patients = Patient.query.all()
    return render_template('index.html', allpatients = all_patients)

@app.route('/profile')
def profile():
    return 'Profile'

@app.route('/addpatient')
def addpatient():
    form = DateForm()
    return render_template('addpatient.html', form=form)


@app.route('/addpatient', methods=["POST"])
def addpatient_post():
    form = DateForm(request.form)
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    birthdate = request.form.get('dt')
    address = request.form.get('address')
    city = request.form.get('city')
    email = request.form.get('email')
    phone = request.form.get('phone')

    patient = Patient.query.filter_by(email=email).first()

    if patient:
        error = "The patient already exists"
        return render_template('addpatient.html', form=form, error=error)
    
    datetime_object = datetime.strptime(birthdate,'%d-%m-%Y')
    birth = date(datetime_object.year, datetime_object.month, datetime_object.day)
    new_patient = Patient(first_name = firstname, last_name = lastname, birth_date = birth, address = address, city = city, email = email, phone = phone)
    db.session.add(new_patient)
    db.session.commit()

    return redirect(url_for('get_patients'))