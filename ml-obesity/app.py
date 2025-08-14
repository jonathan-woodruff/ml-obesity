from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from dotenv import load_dotenv
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from forms import Obesity
import os
import pandas as pd

load_dotenv()  #load environment variables from .env

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

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
    X_test = scaler.transform(X_test)

    #Fit the model
    classifier = SVC(kernel="linear")
    classifier.fit(X_train, y_train)
    return classifier

@app.route('/', methods=["GET", "POST"])
def index():
    form = Obesity(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "prediction", 
            gender=form.gender.data,
            age=form.age.data,
            height=form.height.data,
            weight=form.weight.data,
            family=form.family.data
        ))
    #else:
        #print(form.errors)
    genderOptions = {"male": "Male", "female": "Female"}
    yesno = {"yes": "Yes", "no": "No"}
    return render_template(
        'gender.html', 
        genderOptions=genderOptions, 
        yesno=yesno,
        template_form=form
    )

@app.route('/prediction/<gender>/<int:age>/<float:height>/<float:weight>/<family>', methods=["GET"])
def prediction(gender, age, height, weight, family):
    return render_template(
        'prediction.html',
        template_gender=gender,
        template_age=age,
        template_height=height,
        template_weight=weight,
        template_family=family
    )
