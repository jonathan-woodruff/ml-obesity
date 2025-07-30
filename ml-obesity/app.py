from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

load_dotenv()  #load environment variables from .env

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

### STEP 1: ETL
df = pd.read_csv('obesity-data.csv')

### STEP 2: DATA CLEANING

#Get familiar with the data
print(df.head())
print(df.info())

print(df.columns[df.isnull().sum() > 0]) #check for null values

#take the floor of the age column values and convert the age variable to int
take_floor = lambda x: np.floor(x)
df['Age'] = df['Age'].apply(take_floor).astype(int)

### STEP 3: DATA SPLIT
X = df.drop(columns=['NObeyesdad'])
y = df['NObeyesdad']

@app.route('/', methods=["GET", "POST"])
def index():
    return "Hello, World!"