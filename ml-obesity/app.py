from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()  #load environment variables from .env

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

### STEP 1: ETL
df = pd.read_csv('obesity-data.csv')

### STEP 2: DATA CLEANING
X = df.drop(columns=['NObeyesdad'])
y = df['NObeyesdad']
print(X.columns[X.isnull().sum()>0])

@app.route('/', methods=["GET", "POST"])
def index():
    return "Hello, World!"