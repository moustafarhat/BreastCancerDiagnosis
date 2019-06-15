# main.py

from flask import Blueprint, render_template
#from . import db
from WebService import app

main = Blueprint('main', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

#prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,12)
    loaded_model = pickle.load(open("SerializedModel/model.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

#Get result from serialized Model 
@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
        
        if int(result)==2:
            prediction='Cancer'
        else:
            prediction='No Cancer'
   
    return render_template("result.html",prediction=prediction)