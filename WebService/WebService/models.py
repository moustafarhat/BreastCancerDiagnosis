from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from WebService import app

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'datenbank.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    token = db.Column(db.String(100))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

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
    informations = db.relationship('Patient_Informations', backref='patients', lazy=True)

    def __init__(self, first_name, last_name, birth_date, address, city, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.address = address
        self.city = city
        self.email = email
        self.phone = phone

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
    patient = db.relationship("Patient", backref="patient_informations")

    def __init__(self, patient_id, clump_thickness, uniformity_cell_size, uniformity_cell_shape, marginal_adhesion,
     single_epithelial_cell_size, bare_nuclei, bland_chromatin, normal_nucleoli, mitoses):
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