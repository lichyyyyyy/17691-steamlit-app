import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from dagshub import dagshub_logger


global e_value
e_value = 0

def preprocess():
    df = pd.read_csv('data/raw.csv')

    df['DATE'] = pd.to_datetime(df['DATE'])
    df = df.groupby([pd.Grouper(key='DATE', freq='W-MON')]).agg({'PRCP':'sum', 'TMAX':'max'}).reset_index().sort_values('DATE')
    df.drop(df[(df.DATE.dt.isocalendar().week < 35) | (df.DATE.dt.isocalendar().week > 40)].index, inplace=True)
    df[["IS_STORM"]] = df.apply(lambda row: pd.Series((row.PRCP >=0.35) & (row.TMAX <= 80)), axis=1)
    df["IS_STORM"] = df["IS_STORM"].astype(float)
    df = df.drop(columns = ["DATE"])
    df.to_csv('data/processed.csv')

    # Create numpy array
    array = df.to_numpy()
    array = array/array.max(axis = 0)

    return manupilate(array)


def manupilate(array):
    # Manupilate data
    x, y = np.shape(array)
    x = int(x / 6)
    y = y * 5
    print(x, y)
    X = []
    Y = []
    for i in range(x):
        block = array[i * 6: i * 6 + 5]
        block = block.reshape(1, y)
        X.append(block)
        Y.append(array[i * 6 + 5][2])
    X = np.concatenate(X, 0)
    Y = np.array(Y)

    return X, Y


def train(X, Y):
    # Split the train set and test set
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

    # Fit the model
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 1), random_state=1)
    clf.fit(X_train, Y_train)

    # Prediction
    Y_pred = clf.predict(X_test)
    # calculation(Y_test, Y_pred)
    return confusion_matrix(Y_test, Y_pred)



def calculation(cm, Y_test, Y_pred):
    # Calculate metrix
    acc = accuracy_score(Y_test, Y_pred)
    prec = precision_score(Y_test, Y_pred)
    rec = recall_score(Y_test, Y_pred)

    print ('Precision: {}\nRecall: {}\nAccuracy: {}'.format(acc, prec, rec))

    sensitivity = cm[0][0] / (cm[0][0] + cm[1][0])
    specificity = cm[1][1] / (cm[0][1] + cm[1][1])

    print ('Sensitivity: {}\nSpecificity: {}'.format(sensitivity, specificity))


def process():
    X, Y = preprocess()
    cm = train(X, Y)
    return cm


if __name__ == '__main__':
    process()
