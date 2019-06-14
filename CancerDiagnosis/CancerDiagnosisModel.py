"""
this script is used to analyze breast cancer data from from the University of Wisconsin Hospitals.
This data will also be user to create predictions against the class column
"""
import pickle
import sys
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score


def calculate_correlations(df, target_column):
    """
    Used to create a series of correlations
    :param df: pandas data frame
    :param target_column: the column running the correlations against
    :return: a series with correlations against target_column
    """
    corr_series = df.corr()
    corr_series = corr_series[target_column]
    return corr_series


def predic(Values):
    # TODO make a prediction here
    pass


def draw_scatter(df):
    fig = plt.figure(figsize=(10, 12))

    ax1 = fig.add_subplot(8, 2, 1)
    ax2 = fig.add_subplot(8, 2, 2)
    ax3 = fig.add_subplot(8, 2, 3)
    ax4 = fig.add_subplot(8, 2, 4)
    ax5 = fig.add_subplot(8, 2, 5)
    ax6 = fig.add_subplot(8, 2, 6)
    ax7 = fig.add_subplot(8, 2, 7)
    ax8 = fig.add_subplot(8, 2, 8)

    ax1.scatter(df["clump_thickness"], df["class"], color="green")
    ax2.scatter(df["uniformity_cell_size"], df["class"], color="green")
    ax3.scatter(df["uniformity_cell_shape"], df["class"], color="green")
    ax4.scatter(df["marginal_adhesion"], df["class"], color="green")
    ax5.scatter(df["single_epithelial_cell_size"], df["class"], color="green")
    ax6.scatter(df["bland_chromatin"], df["class"], color="green")
    ax7.scatter(df["normal_nucleoli"], df["class"], color="green")
    ax8.scatter(df["mitoses"], df["class"], color="green")

    ax1.set_ylabel("Class")
    ax2.set_ylabel("Class")
    ax3.set_ylabel("Class")
    ax4.set_ylabel("Class")
    ax5.set_ylabel("Class")
    ax6.set_ylabel("Class")
    ax7.set_ylabel("Class")
    ax8.set_ylabel("Class")

    ax1.set_xlabel("Clump Thickness")
    ax2.set_xlabel("Uniformity Cell Size")
    ax3.set_xlabel("Uniformity Cell Shape")
    ax4.set_xlabel("Marginal Adhesion")
    ax5.set_xlabel("Single Epithelial Cell Size")
    ax6.set_xlabel("Bland Chromatin")
    ax7.set_xlabel("Normal Nucleoli")
    ax8.set_xlabel("Mitoses")

    plt.tight_layout(pad=1.0, w_pad=0.5, h_pad=2.5)
    plt.show()


def main():
    try:
        # import the data
        data_df = pd.read_csv("Data/breast-cancer-wisconsin.data")

        draw_scatter(data_df)

    except Exception as e:
        print(e)
        sys.exit(1)

    print("# of rows: {0}".format(len(data_df)))
    print(data_df.head())
    print(data_df.describe())

    # remove sample_code_number column
    del data_df['sample_code_number']

    print("*** CORRELATIONS WITH CLASS ***")
    print(calculate_correlations(data_df, "class"))

    # scatter plot for each of the attributes against class
    print("scatter plot for each of the attributes against class")
    draw_scatter(data_df)

    # there are 16 rows where the value of 'bare_nuclei' is '?'. Let's remove these rows
    print(len(data_df[data_df["bare_nuclei"] == "?"]))

    data_df = data_df[data_df["bare_nuclei"] != "?"]

    predictor_lst = ["clump_thickness", "uniformity_cell_size", "uniformity_cell_shape", "marginal_adhesion",
                     "single_epithelial_cell_size", "bland_chromatin", "normal_nucleoli"]

    # fit the logistic regression model
    lr = LogisticRegression()

    lr.fit(data_df[predictor_lst], data_df["class"])

    print("*** Accuracy (Score) ***")
    print(lr.score(data_df[predictor_lst], data_df["class"]))

    # creating and training a model
    # serializing our model to a file called model.pkl

    pickle.dump(lr, open('./SerializedModel/model.pkl', "wb"))

    # create predictions
    predictions = lr.predict(data_df[predictor_lst])
    print("*** Predictions ***")

    # eingeben = [5, 1, 1, 1, 3, 1, 1]
    # ausgeben = lr.predict(array.reshape(eingeben))
    # print("Ausgeben" + ausgeben)

    data_df["class_predictions"] = predictions
    print(data_df.head())

    # predictions count
    print("*** Predictions Value Count ***")
    print(data_df["class_predictions"].value_counts())

    # *** calculate accuracy ***

    # get the rows where the actual and the predicted labels match
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

    print("*** Lets see the accuracr using K FOLD ***")
    kf = KFold(len(data_df), 10, shuffle=True, random_state=8)

    accuracies = cross_val_score(lr, data_df[predictor_lst], data_df["class"], scoring="accuracy", cv=kf)
    average_accuracy = sum(accuracies) / len(accuracies)

    print("Accurcies using 10 K-Folds: {0}".format(accuracies))
    print("Average Accuracies after 10 K-Foldsl: {0})".format(average_accuracy))




if __name__ == "__main__":
    sys.exit(0 if main() else 1)
