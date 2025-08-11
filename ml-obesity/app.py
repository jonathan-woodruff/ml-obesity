from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from dotenv import load_dotenv
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

load_dotenv()  #load environment variables from .env

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

### STEP 1: ETL
df = pd.read_csv('obesity-data.csv')

### STEP 2: DATA CLEANING
#Get familiar with the data
print(df.head())
print(df.info())

### STEP 3: EXPLORATORY DATA ANALYSIS
#show histograms for Age, Height, Weight
#sns.histplot(x='Weight', data=df)
#plt.show()
#plt.close()

#show value counts for categorical data
#print(df['Gender'].value_counts())
#print(df['family_history_with_overweight'].value_counts())
#print(df['FAVC'].value_counts())
#print(df['CAEC'].value_counts())
#print(df['SMOKE'].value_counts())
#print(df['SCC'].value_counts())
#print(df['CALC'].value_counts())
#print(df['MTRANS'].value_counts())
#print(df['NObeyesdad'].value_counts())

### Step 4: MODEL SELECTION
# We'll start with linear SVC

### STEP 5: FEATURE ENGINEERING
#Provide an order to the ordinal variables
df['CAEC'] = pd.Categorical(df['CAEC'], ['no', 'Sometimes', 'Frequently', 'Always'], ordered=True)
df['CALC'] = pd.Categorical(df['CALC'], ['no', 'Sometimes', 'Frequently', 'Always'], ordered=True)
# numerically encode categorical features
for feature in ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS']:
    df[feature] = df[feature].astype('category').cat.codes

### STEP 6: DATA SPLIT
X = df.drop(columns=['NObeyesdad'])
y = df['NObeyesdad']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

### STEP 7: NORMALIZE THE FEATURES
#Z-score normalize the features
scaler = preprocessing.StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

### STEP 8: FIT THE MODEL
classifier = SVC(kernel="linear")
classifier.fit(X_train, y_train)
score_train = classifier.score(X_train, y_train)
score_test = classifier.score(X_test, y_test)
print(score_train)
print(score_test)

### STEP 9: HYPERPARAMETER TUNING USING GRID SEARCH
# Initialize hyperparameters
parameters = {
    'kernel': ['linear', 'rbf'], 
    'C': [.01, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1],
    'gamma': np.logspace(-9, 3, 13)
}

#Set up Grid Search
gs = GridSearchCV(classifier, parameters)

#fit the grid search classifier to the training data
gs.fit(X_train, y_train)
print(gs.best_estimator_)
print(gs.best_params_)

#compare scores between how the model does on training data (gs.best_score_) and test data
best_score = gs.best_score_
test_score = gs.score(X_test, y_test)
print(best_score)
print(test_score)

#get a nice view of the hyperparameter configurations and their scores
hyperparameter_grid = pd.DataFrame(gs.cv_results_['params'])
grid_scores = pd.DataFrame(gs.cv_results_['mean_test_score'], columns=['score'])
scores = pd.concat([hyperparameter_grid, grid_scores], axis = 1)
print(scores) 

@app.route('/', methods=["GET", "POST"])
def index():
    return "Hello, World!"