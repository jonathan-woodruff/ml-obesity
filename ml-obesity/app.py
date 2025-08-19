from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from dotenv import load_dotenv
from forms import GenderForm, AgeForm, HeightForm, WeightForm, FamilyForm, FAVCForm, FCVCForm, NCPForm, CAECForm, SmokeForm, CH2OForm, SCCForm, FAFForm, TUEForm, CALCForm, MTRANSForm
from utilities.index import fit_model, height_to_meters, weight_to_kg
import numpy as np
import os

load_dotenv()  #load environment variables from .env

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

yesno = {1: "Yes", 0: "No"}

@app.route('/', methods=["GET", "POST"])
def index():
    form = GenderForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "age", 
            gender=form.gender.data
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
            heightUnit=form.heightUnit.data
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
            weightUnit=form.weightUnit.data
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
            family=form.family.data
        ))

    return render_template(
        'family.html',
        yesno=yesno,
        template_form=form
    )

@app.route('/favc/<int:gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>', methods=["GET", "POST"])
def favc(gender, age, height, heightUnit, weight, weightUnit, family):
    form = FAVCForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "fcvc", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=family,
            favc=form.favc.data
        ))

    return render_template(
        'favc.html',
        yesno=yesno,
        template_form=form
    )

@app.route('/fcvc/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>', methods=["GET", "POST"])
def fcvc(gender, age, height, heightUnit, weight, weightUnit, family, favc):
    form = FCVCForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "ncp", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=family,
            favc=favc,
            fcvc=form.fcvc.data
        ))

    return render_template(
        'fcvc.html',
        fcvcOptions={3: "Always", 2: "Sometimes", 1: "Never"},
        template_form=form
    )

@app.route('/ncp/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>/<fcvc>', methods=["GET", "POST"])
def ncp(gender, age, height, heightUnit, weight, weightUnit, family, favc, fcvc):
    form = NCPForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "caec", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=family,
            favc=favc,
            fcvc=fcvc,
            ncp=form.ncp.data
        ))

    return render_template(
        'ncp.html',
        ncpOptions={1: "Between one and two meals", 3: "Three meals", 4: "More than three meals"},
        template_form=form
    )

@app.route('/caec/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>/<fcvc>/<ncp>', methods=["GET", "POST"])
def caec(gender, age, height, heightUnit, weight, weightUnit, family, favc, fcvc, ncp):
    form = CAECForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "smoke", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=family,
            favc=favc,
            fcvc=fcvc,
            ncp=ncp,
            caec=form.caec.data
        ))

    return render_template(
        'caec.html',
        caecOptions={3: "Always", 2: "Frequently", 1: "Sometimes", 0: "No"},
        template_form=form
    )

@app.route('/smoke/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>/<fcvc>/<ncp>/<caec>', methods=["GET", "POST"])
def smoke(gender, age, height, heightUnit, weight, weightUnit, family, favc, fcvc, ncp, caec):
    form = SmokeForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "ch2o", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=family,
            favc=favc,
            fcvc=fcvc,
            ncp=ncp,
            caec=caec,
            smoke=form.smoke.data
        ))

    return render_template(
        'smoke.html',
        yesno=yesno,
        template_form=form
    )

@app.route('/ch2o/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>/<fcvc>/<ncp>/<caec>/<smoke>', methods=["GET", "POST"])
def ch2o(gender, age, height, heightUnit, weight, weightUnit, family, favc, fcvc, ncp, caec, smoke):
    form = CH2OForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "scc", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=family,
            favc=favc,
            fcvc=fcvc,
            ncp=ncp,
            caec=caec,
            smoke=smoke,
            ch2o=form.ch2o.data
        ))

    return render_template(
        'ch2o.html',
        ch2oOptions={1: "Less than a liter", 2: "Between one and two liters", 3: "More than two liters"},
        template_form=form
    )

@app.route('/scc/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>/<fcvc>/<ncp>/<caec>/<smoke>/<ch2o>', methods=["GET", "POST"])
def scc(gender, age, height, heightUnit, weight, weightUnit, family, favc, fcvc, ncp, caec, smoke, ch2o):
    form = SCCForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "faf", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=family,
            favc=favc,
            fcvc=fcvc,
            ncp=ncp,
            caec=caec,
            smoke=smoke,
            ch2o=ch2o,
            scc=form.scc.data
        ))

    return render_template(
        'scc.html',
        yesno=yesno,
        template_form=form
    )

@app.route('/faf/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>/<fcvc>/<ncp>/<caec>/<smoke>/<ch2o>/<scc>', methods=["GET", "POST"])
def faf(gender, age, height, heightUnit, weight, weightUnit, family, favc, fcvc, ncp, caec, smoke, ch2o, scc):
    form = FAFForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "tue", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=family,
            favc=favc,
            fcvc=fcvc,
            ncp=ncp,
            caec=caec,
            smoke=smoke,
            ch2o=ch2o,
            scc=scc,
            faf=form.faf.data
        ))

    return render_template(
        'faf.html',
        fafOptions={3: "4 or 5 days", 2: "2 or 4 days", 1: "1 or 2 days", 0: "I do not have"},
        template_form=form
    )

@app.route('/tue/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>/<fcvc>/<ncp>/<caec>/<smoke>/<ch2o>/<scc>/<faf>', methods=["GET", "POST"])
def tue(gender, age, height, heightUnit, weight, weightUnit, family, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf):
    form = TUEForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "calc", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=family,
            favc=favc,
            fcvc=fcvc,
            ncp=ncp,
            caec=caec,
            smoke=smoke,
            ch2o=ch2o,
            scc=scc,
            faf=faf,
            tue=form.tue.data
        ))

    return render_template(
        'tue.html',
        tueOptions={0: "0 - 1 hours", 1: "2 - 5 hours", 2: "more than 5 hours"},
        template_form=form
    )

@app.route('/calc/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>/<fcvc>/<ncp>/<caec>/<smoke>/<ch2o>/<scc>/<faf>/<tue>', methods=["GET", "POST"])
def calc(gender, age, height, heightUnit, weight, weightUnit, family, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf, tue):
    form = CALCForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "mtrans", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=family,
            favc=favc,
            fcvc=fcvc,
            ncp=ncp,
            caec=caec,
            smoke=smoke,
            ch2o=ch2o,
            scc=scc,
            faf=faf,
            tue=tue,
            calc=form.calc.data
        ))

    return render_template(
        'calc.html',
        calcOptions={3: "Always", 2: "Frequently", 1: "Sometimes", 0: "I do not drink"},
        template_form=form
    )

@app.route('/mtrans/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>/<fcvc>/<ncp>/<caec>/<smoke>/<ch2o>/<scc>/<faf>/<tue>/<calc>', methods=["GET", "POST"])
def mtrans(gender, age, height, heightUnit, weight, weightUnit, family, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf, tue, calc):
    form = MTRANSForm(csrf_enabled=False)
    if form.validate_on_submit(): #if valid submission
        return redirect(url_for(
            "prediction", 
            gender=gender,
            age=age,
            height=height,
            heightUnit=heightUnit,
            weight=weight,
            weightUnit=weightUnit,
            family=family,
            favc=favc,
            fcvc=fcvc,
            ncp=ncp,
            caec=caec,
            smoke=smoke,
            ch2o=ch2o,
            scc=scc,
            faf=faf,
            tue=tue,
            calc=calc,
            mtrans=form.mtrans.data
        ))

    return render_template(
        'mtrans.html',
        mtransOptions={0: "Automobile", 2: "Motorbike", 1: "Bike", 3: "Public Transportation", 4: "Walking"},
        template_form=form
    )

@app.route('/prediction/<gender>/<int:age>/<float:height>/<heightUnit>/<float:weight>/<weightUnit>/<family>/<favc>/<fcvc>/<ncp>/<caec>/<smoke>/<ch2o>/<scc>/<faf>/<tue>/<calc>/<mtrans>', methods=["GET"])
def prediction(gender, age, height, heightUnit, weight, weightUnit, family, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf, tue, calc, mtrans):
    [classifier, scaler] = fit_model()
    userData = np.array([[
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
    scaledUserData = scaler.transform(userData)
    prediction = classifier.predict(scaledUserData)
    
    return render_template(
        'prediction.html',
        template_prediction=prediction
    )