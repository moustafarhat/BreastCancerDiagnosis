#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, redirect
from flask_login import login_required, current_user
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn import model_selection
from keras.models import load_model
import os
from ..models import Patient_Informations, db
from WebService import app
from .forms import *
import pickle
import sys
from datetime import datetime


################
#### config ####
################

Predictor_blueprint = Blueprint('Predictor', __name__)

##########################
#### helper functions ####
##########################

#ML_Model_Cancer_Predictor 1  function
def M_ValuePredictor1(to_predict_list):
   path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\SerializedModels\ML_Model_Cancer_Predictor1.pkl"
   loaded_model = pickle.load(open(path,"rb"))
   # load the model from disk

   result = loaded_model.predict([to_predict_list])

   # creating and training a model
   # serializing our model to a file called model.pkl

   #result = loaded_model.predict(data_df[predictor_lst])
   #result2= loaded_model.predict([[1, 1, 2, 5,1, 1, 5]])


   #print(result2)
   return result

#ML_Model_Cancer_Predictor 2  function
def M_ValuePredictor2(to_predict_list):

   finalresult=0

   path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\SerializedModels\ML_Model_Cancer_Predictor2.model"
   
   model = load_model(path)

   data_patient_informations =np.array([to_predict_list])

   result  = model.predict(data_patient_informations)

   if result[len(result)-1] < 3:
       finalresult = 2
   else :
       finalresult = 4

   return finalresult


#Get result from serialized Models
@app.route('/', methods=["GET", "POST"])
@login_required
def result():
       
   # Data that we need for Model (it is important to follow this order!)
   #[0] clump_thickness
   #[1] uniformity_cell_size
   #[2] uniformity_cell_shape
   #[3] marginal_adhesion
   #[4] single_epithelial_cell_size
   #[5] bland_chromatin
   #[6] normal_nucleoli
   if request.method == "GET":
      form = PredictionForm()
      all_patients = Patient.query.all()
      return render_template('index.html', allpatients = all_patients, form = form)
   
   if request.method == "POST":
      form = PredictionForm(request.form)
      
      clump_thickness = request.form.get('clump_thickness')
      uniformity_cell_size = request.form.get('uniformity_cell_size')
      uniformity_cell_shape = request.form.get('uniformity_cell_shape')
      marginal_adhesion = request.form.get('marginal_adhesion')
      single_epithelial_cell_size = request.form.get('single_epithelial_cell_size')
      bare_nuclei = request.form.get('bare_nuclei')
      bland_chromatin = request.form.get('bland_chromatin')
      normal_nucleoli = request.form.get('normal_nucleoli')
      mitoses = request.form.get('mitoses')
      patient_id = request.form.get('patient')
      user_id = current_user.user_id

      ValuesList=[float(clump_thickness),float(uniformity_cell_size),float(uniformity_cell_shape),float(marginal_adhesion),float(single_epithelial_cell_size),float(bland_chromatin),float(normal_nucleoli)]
      
      try:
         result_list = M_ValuePredictor1(ValuesList)
         result1 = int(result_list[0])
         result2 = M_ValuePredictor2(ValuesList)

         p_info1 = Patient_Informations(patient_id = patient_id, 
                                       clump_thickness = clump_thickness, 
                                       uniformity_cell_size = uniformity_cell_size,
                                       uniformity_cell_shape = uniformity_cell_shape, 
                                       marginal_adhesion = marginal_adhesion,
                                       single_epithelial_cell_size = single_epithelial_cell_size,
                                       bare_nuclei = bare_nuclei, 
                                       bland_chromatin = bland_chromatin, 
                                       normal_nucleoli = normal_nucleoli, 
                                       mitoses = mitoses,
                                       result = result1, 
                                       user_id = user_id,
                                       diagnosis_date = datetime.now(), 
                                       status = 0,
                                       model = 1)
         db.session.add(p_info1)
         db.session.commit()
         p_info2 = Patient_Informations(patient_id = patient_id, 
                                       clump_thickness = clump_thickness, 
                                       uniformity_cell_size = uniformity_cell_size,
                                       uniformity_cell_shape = uniformity_cell_shape, 
                                       marginal_adhesion = marginal_adhesion,
                                       single_epithelial_cell_size = single_epithelial_cell_size,
                                       bare_nuclei = bare_nuclei, 
                                       bland_chromatin = bland_chromatin, 
                                       normal_nucleoli = normal_nucleoli, 
                                       mitoses = mitoses,
                                       result = result2, 
                                       user_id = user_id,
                                       diagnosis_date = datetime.now(), 
                                       status = 0,
                                       model = 2)
         db.session.add(p_info2)
         db.session.commit()
         return redirect(url_for('result_detail', id_model1=p_info1.id, id_model2=p_info2.id))
      except Exception as e: 
         print(e)

        #TODO::In future we will compare result from differents Models
        #to_predict_list = request.form.to_dict()
        #to_predict_list=list(to_predict_list.values())
        #to_predict_list = list(map(int, to_predict_list))

        #Get the predicted value from the first Model
        #predictor1 = M_ValuePredictor1(to_predict_list)

        #Get the predicted value from the Second  Model
        #predictor2 = M_ValuePredictor1(to_predict_list)

        #Compare results to get more Accuracy
        #if predictor1==prepredictor2:
       #             if int(result)==2:
      #                  prediction='Cancer'
      #              else:
      #                  prediction='No Cancer'

     #   else:
            #Do something else
     #       pass
   
      return render_template("index.html",form =form)

@app.route('/result', methods=["GET", "POST"])
@login_required
def result_detail():
   if request.method == "GET":
      if 'id_model1' in request.args and 'id_model2' in request.args:
         id_model1 = request.args.get('id_model1')
         id_model2 = request.args.get('id_model2')
         result1 = Patient_Informations.query.filter_by(id=id_model1).first()
         result2 = Patient_Informations.query.filter_by(id=id_model2).first()
         result = result2
         form = ResultForm()
         form.result1_id.data = id_model1
         form.result2_id.data = id_model2
         return render_template("result.html",result = result, result1 = result1, result2 = result2, form =form, id_model1 = id_model1, id_model2 = id_model2)
      if 'id_model1' in request.args:
         id_model1 = request.args.get('id_model1')
         result1 = Patient_Informations.query.filter_by(id=id_model1).first()
         result = result1
         form = ResultForm()
         form.result1_id.data = id_model1
         return render_template("result.html",result = result, result1 = result1, form =form, id_model1 = id_model1)
      if 'id_model2' in request.args:
         id_model2 = request.args.get('id_model2')
         result2 = Patient_Informations.query.filter_by(id=id_model2).first()
         result = result2
         form = ResultForm()
         form.result2_id.data = id_model2
         return render_template("result.html",result = result, result2 = result2, form =form, id_model2 = id_model2)
   if request.method == "POST":
      form = ResultForm(request.form)
      id1 = form.result1_id.data
      id2 = form.result2_id.data
      if id1:
         p_info1 = Patient_Informations.query.get(id1)
         p_info1.status = request.form.get('status1')
      if id2:
         p_info1 = Patient_Informations.query.get(id2)
         p_info1.status = request.form.get('status2')
      db.session.commit()
      if id1 and id2:
         return redirect(url_for('result_detail', id_model1=id1, id_model2=id2))
      if id1:
         return redirect(url_for('result_detail', id_model1=id1))
      if id2:
         return redirect(url_for('result_detail', id_model2=id2))