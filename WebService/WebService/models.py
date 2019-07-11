#################
#### imports ####
#################
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import UserMixin , LoginManager
import os
from WebService import app
from .Config import *

#@login.user_loader
#def load_user(user_id):
#    try:
#        return User.query.get(user_id)
#    except:
#        return None


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    token = db.Column(db.String(100))
    foundation_id = db.Column(db.Integer, db.ForeignKey('foundations.foundation_id'))
    foundation = db.relationship("Foundations", backref='users')

    def __init__(self, first_name, last_name, email, password, foundation):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.foundation = foundation

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True
 
    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True
 
    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False
 
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.user_id)
 
    def __repr__(self):
        return '<User {0}>'.format(self.name)


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    address = db.Column(db.String(75))
    city = db.Column(db.String(50))
    email = db.Column(db.String(75), unique = True, nullable = False)
    phone = db.Column(db.String(25))
    access_permission = db.Column(db.Boolean, unique = False)
    informations = db.relationship('Patient_Informations', backref='patients', lazy=True)

    def __init__(self, first_name, last_name, birth_date, address, city, email, phone, access_permission):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.address = address
        self.city = city
        self.email = email
        self.phone = phone
        self.access_permission = access_permission

class Patient_Informations(db.Model):
    __tablename__ = 'patient_informations'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    clump_thickness = db.Column(db.Integer)
    uniformity_cell_size = db.Column(db.Integer)
    uniformity_cell_shape = db.Column(db.Integer)
    marginal_adhesion = db.Column(db.Integer)
    single_epithelial_cell_size = db.Column(db.Integer)
    bare_nuclei = db.Column(db.Integer)
    bland_chromatin = db.Column(db.Integer)
    normal_nucleoli = db.Column(db.Integer)
    mitoses = db.Column(db.Integer)
    result = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    diagnosis_date = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    model = db.Column(db.Integer)
    user = db.relationship("User", backref="patient_informations")
    patient = db.relationship("Patient", backref="patient_informations")

    def __init__(self, patient_id, clump_thickness, uniformity_cell_size, uniformity_cell_shape, marginal_adhesion,
     single_epithelial_cell_size, bare_nuclei, bland_chromatin, normal_nucleoli, mitoses, result, user_id,diagnosis_date, status, model):
        self.patient_id = patient_id
        self.clump_thickness = clump_thickness
        self.uniformity_cell_size = uniformity_cell_size
        self.uniformity_cell_shape = uniformity_cell_shape
        self.marginal_adhesion = marginal_adhesion
        self.single_epithelial_cell_size = single_epithelial_cell_size
        self.bare_nuclei = bare_nuclei
        self.bland_chromatin = bland_chromatin
        self.normal_nucleoli = normal_nucleoli
        self.mitoses = mitoses
        self.result = result
        self.user_id = user_id
        self.diagnosis_date = diagnosis_date
        self.status = status
        self.model = model

class Foundations(db.Model):
    __tablename__ = 'foundations'
    foundation_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))
    role = db.Column(db.Integer)
    members = db.relationship('User', backref='foundations', lazy=True)

    def __init__(self, name, role):
        self.name = name
        self.role = role