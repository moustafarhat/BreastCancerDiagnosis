import pandas as pd
import sys
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import numpy as np
import csv
import sqlite3
import time
from sklearn.externals import joblib
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.models import load_model
def train():
    try:

        # import the data
        data_df = pd.read_csv('CancerDiagnosis/Data/breast-cancer-wisconsin.data')
    except Exception as e: 
        print(e)
        sys.exit(1)
#print("# of rows: {0}".format(len(data_df)))
    #print(data_df.head())


    # remove sample_code_number column
    del data_df['sample_code_number']
    predictor_lst = ["clump_thickness", "uniformity_cell_size", "uniformity_cell_shape", "marginal_adhesion",
                     "single_epithelial_cell_size", "bland_chromatin", "normal_nucleoli","mitoses"]
# there are 16 rows where the value of 'bare_nuclei' is '?'. Let's remove these rows
#print(len(data_df[data_df["bare_nuclei"] == "?"]))
    data_df = data_df[data_df["bare_nuclei"] != "?"]
    #y_train = np.array(data_df["class"])    
    #x_train = np.array(data_df[predictor_lst])
    #model = Sequential() 
    #model.add(Dense(input_dim = 8,output_dim = 12))
    #model.add(Activation('relu')) 
    #model.add(Dense(input_dim = 12,output_dim = 1))
    #model.compile(loss='mean_squared_error', optimizer='adam') 
    #model.fit(x_train, y_train, nb_epoch = 10000, batch_size = 16) 

    #model.save('my_net.model')

    model = load_model('save_model/my_net.model')
    vermutung = model.predict(data_df[predictor_lst])
    for i in range(len(vermutung )):
        if vermutung[i] < 3 :
            vermutung[i]= 2
        else :
            vermutung[i] = 4
    data_df["class_predictions"] = vermutung
 
    # predictions count
    print("*** Predictions Value Count ***")
    print(data_df["class_predictions"].value_counts())
    matched_df = data_df[data_df["class"] == data_df["class_predictions"]]
    accuracy = float(len(matched_df)) / float(len(data_df))
    print("Accuracy is {0}".format(accuracy))

    # *** calculate the outcomes of the binary classification
    true_positives = len(data_df[(data_df["class"] == 4) & (data_df["class_predictions"] == 4)])
    true_negatives = len(data_df[(data_df["class"] == 2) & (data_df["class_predictions"] == 2)])
    false_positives = len(data_df[(data_df["class"] == 2) & (data_df["class_predictions"] == 4)])
    false_negatives = len(data_df[(data_df["class"] == 4) & (data_df["class_predictions"] == 2)])

    print("True Positives is {0}".format(true_positives))
    print("True Negatives is {0}".format(true_negatives))
    print("False Positives is {0}".format(false_positives))
    print("False Negatives is {0}".format(false_negatives))

    sensitivity = float(true_positives) / float((true_positives + false_negatives))
    print("Sensitivity is {0}".format(sensitivity))

    specificity = float(true_negatives) / float(true_negatives + false_positives)
    print("Specificity is {0}".format(specificity))
    '''
    print("*** Lets see the accuracr using K FOLD ***")
    kf = KFold( 10, shuffle=True, random_state=8)

    accuracies = cross_val_score(model, data_df[predictor_lst], data_df["class"], scoring="accuracy", cv=kf)
    average_accuracy = sum(accuracies) / len(accuracies)

    print("Accurcies using 10 K-Folds: {0}".format(accuracies))
    print("Average Accuracies after 10 K-Foldsl: {0})".format(average_accuracy))
    '''
def main():
   train()
   
   with sqlite3.connect('WebService/WebService/datenbank.sqlite') as con:
        data_patient_informations = pd.read_sql_query("SELECT * FROM patient_informations", con=con)
   del data_patient_informations['id']
   del data_patient_informations['patient_id']
   del data_patient_informations['bare_nuclei']
   del data_patient_informations['result']
   data_patient_informations =np.array(data_patient_informations)
   model = load_model('save_model/my_net.model')
   ergibnis  = model.predict(data_patient_informations)
   print(ergibnis)
if __name__ == '__main__':
   sys.exit(0 if main() else 1) 
  
            