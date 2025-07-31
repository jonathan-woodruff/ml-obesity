from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from dotenv import load_dotenv
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

#Provide an order to the ordinal variables
df['CAEC'] = pd.Categorical(df['CAEC'], ['no', 'Sometimes', 'Frequently', 'Always'], ordered=True)
df['CALC'] = pd.Categorical(df['CALC'], ['no', 'Sometimes', 'Frequently', 'Always'], ordered=True)

#show histograms for Age, Height, Weight
#sns.histplot(x='Weight', data=df)
#plt.show()
#plt.close()

#show value counts for categorical data
print(df['Gender'].value_counts())
print(df['family_history_with_overweight'].value_counts())
print(df['FAVC'].value_counts())
print(df['CAEC'].value_counts())
print(df['SMOKE'].value_counts())
print(df['SCC'].value_counts())
print(df['CALC'].value_counts())
print(df['MTRANS'].value_counts())


### STEP 5: DATA SPLIT
X = df.drop(columns=['NObeyesdad'])
y = df['NObeyesdad']

@app.route('/', methods=["GET", "POST"])
def index():
    return "Hello, World!"