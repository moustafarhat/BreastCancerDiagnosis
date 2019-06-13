import pandas as pd
import sys
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import numpy as np
import random
import copy
import csv
try:

        # import the data
        data_df = pd.read_csv('CancerDiagnosis/Data/breast-cancer-wisconsin.data')
except Exception as e: 
        print(e)
        sys.exit(1)
print("# of rows: {0}".format(len(data_df)))
    #print(data_df.head())


    # remove sample_code_number column
del data_df['sample_code_number']
predictor_lst = ["clump_thickness", "uniformity_cell_size", "uniformity_cell_shape", "marginal_adhesion",
                     "single_epithelial_cell_size", "bland_chromatin", "normal_nucleoli","mitoses"]
# there are 16 rows where the value of 'bare_nuclei' is '?'. Let's remove these rows
print(len(data_df[data_df["bare_nuclei"] == "?"]))
data_df = data_df[data_df["bare_nuclei"] != "?"]
Y=np.array(data_df["class"])
for i in range(0,len(Y)):
    if Y[i] == 2:
        Y[i] = 0
    else :
        Y[i] = 1
X = np.array(data_df[predictor_lst])
V= np.array([[0.1,0.2,0.3,0.4,0.4,0.6,0.2,0.7],
    [0.8,0.9,0.4,0.6,0.1,0.8,0.3,0.5],
    [0.2,0.4,0.1,0.5,0.7,0.9,0.3,0.2],
    [0.8,0.1,0.1,0.2,0.4,0.6,0.3,0.9],
    [0.9,0.9,0.4,0.2,0.5,0.1,0.6,0.7],
    [0.1,0.2,0.1,0.4,0.7,0.6,0.3,0.1],
    [0.3,0.2,0.5,0.3,0.8,0.2,0.9,0.7],
    [0.4,0.6,0.8,0.9,0.2,0.3,0.6,0.9]])
W=np.array([[0.2,0.1,0.3,0.4,0.6,0.7,0.8,0.9]])  
lr = 0.5
def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_daoshu(x):
    return x*(1-x)

def  updateW(): 
    global X,Y,V,W,lr
    W_C = np.array([0,0,0,0,0,0,0,0])
    V_C = np.array([[0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0]])

    for i in range(0,len(X)):
         #8*1
        layer_1_input = np.dot(V,np.array([X[i]]).T)  ## V*X 
        layer_1_output = sigmoid(layer_1_input)  ## a=f(V*X)

         #1*1
        layer_2_input = np.dot(W,layer_1_output)  
        layer_2_output = sigmoid(layer_2_input)
        #1*1
        E_2 = Y[i] - layer_2_output.T   
        ## 1*1
        layer_2_detal = E_2*sigmoid_daoshu(layer_2_output)
        ##8*1
        E_1 = np.dot(W.T,layer_2_detal)
        
        ## 8*1)
        layer_1_detal = E_1*sigmoid_daoshu(layer_1_output)

 
        W_C = W_C + np.dot(layer_2_detal, layer_1_output.T)
      
        V_C = V_C + np.dot(layer_1_detal, np.array([X[i]]))

    
    W_d = W_C/len(X)
    V_d = V_C/len(X)

    W = W + lr*W_d
    V = V + lr*V_d
def train():
    train_n_mal =1000
    output = [0 for i in range(len(X))]; 
    
    for index in range (train_n_mal):
        updateW()
        if index==0 or index==(train_n_mal-1):
           
            for i in range(0,len(X)):
                layer_1_input = np.dot(V,np.array([X[i]]).T)
                layer_1_output = sigmoid(layer_1_input)  
                layer_2_input = np.dot(W,layer_1_output)  
                layer_2_output = sigmoid(layer_2_input)
                output[i] = layer_2_output[0][0]
            for j in range(0,len(X)):
                if output[j] < 0.5 :
                    output[j] = 2
                else :
                    output[j] = 4
            print(output)
    #df = pd.DataFrame(V)
    #df.to_csv('V.data')
    #df1 = pd.DataFrame(W)
    #df1.to_csv('W.data')
    data_df["class_predictions"] = output
    print(data_df.head())
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

    #print("*** Lets see the accuracr using K FOLD ***")
    #kf = KFold( 10, shuffle=True, random_state=8)#len(data_df),#https://blog.csdn.net/weixin_40283816/article/details/83242777

    #accuracies = cross_val_score(data_df, data_df[predictor_lst], data_df["class"], scoring="accuracy", cv=kf)
    #average_accuracy = sum(accuracies) / len(accuracies)

    #print("Accurcies using 10 K-Folds: {0}".format(accuracies))
    #print("Average Accuracies after 10 K-Foldsl: {0})".format(average_accuracy))
def schatzen(eingeben):
    V =  pd.read_csv("CancerDiagnosis/Data/V.data")
    del V["Unnamed: 0"]
    W =  pd.read_csv("CancerDiagnosis/Data/W.data")
    del W["Unnamed: 0"]
    layer_1_input = np.dot(V,np.array([eingeben]).T)
    layer_1_output = sigmoid(layer_1_input)  
    layer_2_input = np.dot(W,layer_1_output)  
    layer_2_output = sigmoid(layer_2_input)
    output1 = layer_2_output[0][0]
    if output1 > 0.5 :      
        output1 = 4
    else :
        output1 = 2
    print(output1)
def main():       
    #train()
    eingeben =[5,1,1,1,2,3,1,1]
    schatzen(eingeben)        
if __name__ == '__main__':
   sys.exit(0 if main() else 1) 
            