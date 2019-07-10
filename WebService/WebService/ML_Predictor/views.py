#################
#### imports ####
#################

from flask import render_template, Blueprint
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn import model_selection
from ..models import Patient_Informations, db
from WebService import app
from .forms import *
import pickle
import sys


################
#### config ####
################

Predictor_blueprint = Blueprint('Predictor', __name__)

##########################
#### helper functions ####
##########################

#ML_Model_Cancer_Predictor 1  function
def M_ValuePredictor1(to_predict_list):

    loaded_model = pickle.load(open("SerializedModel/ML_Model_Cancer_Predictor1.pkl","rb"))
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
    to_predict = np.array(to_predict_list).reshape(1,12)
    loaded_model = load_model('save_model/my_net.model')
    result = loaded_model.predict(to_predict)
    return result[0]


#Get result from serialized Models
@app.route('/index', methods=["GET", "POST"])
def result(data):

    # Data that we need for Model (it is important to follow this order!)
    #[0] clump_thickness
    #[1] uniformity_cell_size
    #[2] uniformity_cell_shape
    #[3] marginal_adhesion
    #[4] single_epithelial_cell_size
    #[5] bland_chromatin
    #[6] normal_nucleoli

     if request.method == "POST":

        form = PredictionForm(request.form)

        clump_thickness = request.form.get('clump_thickness')
        uniformity_cell_size = request.form.get('uniformity_cell_size')
        uniformity_cell_shape = request.form.get('uniformity_cell_shape')
        marginal_adhesion = request.form.get('marginal_adhesion')
        single_epithelial_cell_size = request.form.get('single_epithelial_cell_size')
        bland_chromatin = request.form.get('bland_chromatin')
        normal_nucleoli = request.form.get('normal_nucleoli')

        try:

           result = M_ValuePredictor1([clump_thickness,uniformity_cell_size,uniformity_cell_shape,marginal_adhesion,single_epithelial_cell_size,bland_chromatin,normal_nucleoli])

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
   
     return render_template("index.html",form =Form)