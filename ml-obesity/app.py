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
    #else:
        #print(form.errors)
    yesno = {"yes": "Yes", "no": "No"}
    return render_template(
        'gender.html',
        genderOptions={"male": "Male", "female": "Female"}, 
        yesno=yesno,
        fcvcOptions={"always": "Always", "sometimes": "Sometimes", "never": "Never"},
        ncpOptions={"one": "Between one and two meals", "two": "Three meals", "three": "More than three meals"},
        caecOptions={"always": "Always", "frequently": "Frequently", "sometimes": "Sometimes", "no": "No"},
        ch2oOptions={"one": "Less than a liter", "two": "Between one and two liters", "three": "More than two liters"},
        fafOptions={"one": "4 or 5 days", "two": "2 or 4 days", "three": "1 or 2 days", "four": "I do not have"},
        tueOptions={"one": "0 - 1 hours", "two": "2 - 5 hours", "three": "more than 5 hours"},
        calcOptions={"always": "Always", "frequently": "Frequently", "sometimes": "Sometimes", "no": "I do not drink"},
        mtransOptions={"automobile": "Automobile", "motorbike": "Motorbike", "bike": "Bike", "public": "Public Transportation", "walking": "Walking"},
        template_form=form
    )

@app.route('/prediction/<gender>/<int:age>/<float:height>/<float:weight>/<family>/<favc>/<fcvc>/<ncp>/<caec>/<smoke>/<ch2o>/<scc>/<faf>/<tue>/<calc>/<mtrans>', methods=["GET"])
def prediction(gender, age, height, weight, family, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf, tue, calc, mtrans):
    return render_template(
        'prediction.html',
        template_gender=gender,
        template_age=age,
        template_height=height,
        template_weight=weight,
        template_family=family,
        template_favc=favc,
        template_fcvc=fcvc,
        template_ncp=ncp,
        template_caec=caec,
        template_smoke=smoke,
        template_ch2o=ch2o,
        template_scc=scc,
        template_faf=faf,
        template_tue=tue,
        template_calc=calc,
        template_mtrans=mtrans
    )
