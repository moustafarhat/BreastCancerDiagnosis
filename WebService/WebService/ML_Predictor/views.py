#################
#### imports ####
#################

from flask import render_template, Blueprint
from WebService import app
from .forms import *
import pickle

################
#### config ####
################

Predictor_blueprint = Blueprint('Predictor', __name__)


#ML_Model_Cancer_Predictor 1  function
def M_ValuePredictor1(to_predict_list):
    loaded_model = pickle.load(open("SerializedModel/model.pkl","rb"))
    result = loaded_model.predict(to_predict_list)

    # creating and training a model
    # serializing our model to a file called model.pkl

    pickle.dump(lr, open('model.pkl', "wb"))

    # load the model from disk
    loaded_model = pickle.load(open('model.pkl', 'rb'))
    #result = loaded_model.predict(data_df[predictor_lst])
    result2= loaded_model.predict([[1, 1, 2, 5,
                       1, 1, 5]])
    print(result2)

    return result[0]

#ML_Model_Cancer_Predictor 2  function
def M_ValuePredictor2(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,12)
    loaded_model = load_model('save_model/my_net.model')
    result = loaded_model.predict(to_predict)
    return result[0]


#Get result from serialized Models
@app.route('/index',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))

        #Get the predicted value from the first Model
        predictor1 = M_ValuePredictor1(to_predict_list)

        #Get the predicted value from the Second  Model
        predictor2 = M_ValuePredictor1(to_predict_list)

        #Compare results to get more Accuracy
        if predictor1==prepredictor2:
                    if int(result)==2:
                        prediction='Cancer'
                    else:
                        prediction='No Cancer'

        else:
            #Do something else
            pass
   
    return render_template("index.html",prediction=prediction)