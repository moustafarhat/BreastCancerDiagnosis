#################
#### imports ####
#################

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from ..models import User , Patient, Foundations, db
from WebService import app
from flask_wtf import Form
from wtforms import DateField, TextField
from datetime import date, datetime
from .forms import *

################
#### config ####
################

Foundations_blueprint = Blueprint('Foundations', __name__)


################
#### routes ####
################

@app.route('/groups', methods=['GET', 'POST'])
@login_required
def get_groups():
    if request.method == "POST":
        form = FoundationForm(request.form)
        id = request.form.get('fnd_id')
        name = request.form.get('name')
        permission = request.form.get('permission')
        
        if id:
            fnd = Foundations.query.get(id)
            fnd.name = name
            fnd.permission = permission
            db.session.commit()
        else:
            new_fnd = Foundations(name = name, role = permission)
            db.session.add(new_fnd)
            db.session.commit()

        return redirect(url_for('get_groups'))
    else:
        form = FoundationForm()
        select_val = ''
        if 'id' in request.args:
            foundation_id = request.args.get('id')
            fnd = Foundations.query.get(foundation_id)
            form.fnd_id.data = fnd.foundation_id
            form.name.data = fnd.name
            select_val = fnd.role

        all_groups = Foundations.query.all()
        return render_template('groups.html', allgroups = all_groups, form=form, select_val = select_val)

@app.route('/deletegroup')
@login_required
def deletegroup():
    if 'id' in request.args:
        foundation_id = request.args.get('id')
        fnd = Foundations.query.get(foundation_id)
        db.session.delete(fnd)
        db.session.commit()
    return redirect(url_for('get_groups'))
