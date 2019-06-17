#################
#### imports ####
#################
from flask_wtf import Form
from flask_wtf import Form
from wtforms import DateField, TextField

class PredictionForm(Form):
    result = TextField()