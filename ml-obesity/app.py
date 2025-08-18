from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from dotenv import load_dotenv
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from forms import GenderForm, AgeForm, HeightForm, WeightForm, FamilyForm
import os
import pandas as pd

load_dotenv()  #load environment variables from .env

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

yesno = {1: "Yes", 0: "No"}

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

@app.route('/', methods=["GET", "POST"])
def index():
    form = GenderForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "age", 
            gender=form.gender.data,
        ))

    return render_template(
        'gender.html',
        genderOptions={0: "Female", 1: "Male"},
        template_form=form
    )

@app.route('/age/<int:gender>', methods=["GET", "POST"])
def age(gender):
    form = AgeForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "height", 
            gender=gender,
            age=form.age.data
        ))
    #else:
        #print(form.errors)

    return render_template(
        'age.html',
        template_form=form
    )

@app.route('/height/<int:gender>/<int:age>', methods=["GET", "POST"])
def height(gender, age):
    form = HeightForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "weight", 
            gender=gender,
            age=age,
            height=form.height.data,
            heightUnit=form.heightUnit.data,
        ))

    return render_template(
        'height.html',
        template_form=form
    )

@app.route('/weight/<int:gender>/<int:age>/<float:height>/<heightUnit>', methods=["GET", "POST"])
def weight(gender, age, height, heightUnit):
    form = WeightForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "family", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=form.weight.data,
            weightUnit=form.weightUnit.data,
        ))

    return render_template(
        'weight.html',
        template_form=form
    )

@app.route('/family/<int:gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>', methods=["GET", "POST"])
def family(gender, age, height, heightUnit, weight, weightUnit):
    form = FamilyForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "favc", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=form.family.data,
        ))

    return render_template(
        'family.html',
        yesno=yesno,
        template_form=form
    )

@app.route('/favc/<int:gender>/<int:age>/<float:height>/<heightUnit>', methods=["GET", "POST"])
def favc(gender, age, height, heightUnit, weight, weightUnit):
    form = HeightForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "prediction", 
            gender=form.gender.data,
            age=form.age.data,
            height=form.height.data,
            heightUnit=form.heightUnit.data,
            weight=form.weight.data,
            weightUnit=form.weightUnit.data,
            family=form.family.data,
            favc=form.favc.data,
            fcvc=form.fcvc.data,
            ncp=form.ncp.data,
            caec=form.caec.data,
            smoke=form.smoke.data,
            ch2o=form.ch2o.data,
            scc=form.scc.data,
            faf=form.faf.data,
            tue=form.tue.data,
            calc=form.calc.data,
            mtrans=form.mtrans.data
        ))

    yesno = {1: "Yes", 0: "No"}
    return render_template(
        'gender.html',
        genderOptions={0: "Female", 1: "Male"}, 
        yesno=yesno,
        fcvcOptions={3: "Always", 2: "Sometimes", 1: "Never"},
        ncpOptions={1: "Between one and two meals", 3: "Three meals", 4: "More than three meals"},
        caecOptions={3: "Always", 2: "Frequently", 1: "Sometimes", 0: "No"},
        ch2oOptions={1: "Less than a liter", 2: "Between one and two liters", 3: "More than two liters"},
        fafOptions={3: "4 or 5 days", 2: "2 or 4 days", 1: "1 or 2 days", 0: "I do not have"},
        tueOptions={0: "0 - 1 hours", 1: "2 - 5 hours", 2: "more than 5 hours"},
        calcOptions={3: "Always", 2: "Frequently", 1: "Sometimes", 0: "I do not drink"},
        mtransOptions={0: "Automobile", 2: "Motorbike", 1: "Bike", 3: "Public Transportation", 4: "Walking"},
        template_form=form
    )

@app.route('/prediction/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>/<fcvc>/<ncp>/<caec>/<smoke>/<ch2o>/<scc>/<faf>/<tue>/<calc>/<mtrans>', methods=["GET"])
def prediction(gender, age, height, heightUnit, weight, weightUnit, family, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf, tue, calc, mtrans):
    classifier = fit_model()
    prediction = classifier.predict([[
        gender,
        age,
        height_to_meters(height,heightUnit),
        weight_to_kg(weight,weightUnit),
        family,
        favc,
        fcvc,
        ncp,
        caec,
        smoke,
        ch2o,
        scc,
        faf,
        tue,
        calc,
        mtrans
    ]])
    
    return render_template(
        'prediction.html',
        template_prediction=prediction
    )