from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pandas as pd

#Machine learning logic
def fit_model():
    df = pd.read_csv('obesity-data.csv')

    #Provide an order to the ordinal variables
    df['CAEC'] = pd.Categorical(df['CAEC'], ['no', 'Sometimes', 'Frequently', 'Always'], ordered=True)
    df['CALC'] = pd.Categorical(df['CALC'], ['no', 'Sometimes', 'Frequently', 'Always'], ordered=True)
    # numerically encode categorical features
    for feature in ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS']:
        df[feature] = df[feature].astype('category').cat.codes

    X = df.drop(columns=['NObeyesdad'])
    y = df['NObeyesdad']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    #Z-score normalize the features
    scaler = preprocessing.StandardScaler()
    X_train = scaler.fit_transform(X_train)

    #Fit the model
    classifier = SVC(kernel="linear")
    classifier.fit(X_train, y_train)
    return [classifier, scaler]

def height_to_meters(height, unit):
    if unit == 'cm':
        return height / 100
    elif unit == 'in':
        return height / 39.3701
    else:
        raise Exception('Unexpected unit argument')

def weight_to_kg(weight, unit):
    if unit == 'kg':
        return weight
    elif unit == 'lbs':
        return weight / 2.20462
    else:
        raise Exception('Unexpected unit argument')