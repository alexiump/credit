from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    #Legalstatus_Partnership=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        
        Volume=float(request.form['Volume'])
        
        Budget=float(request.form['Budget'])
        
        
        Legalstatus_Sole_Trader=request.form['Legalstatus_Sole_Trader']
        
        if(Legalstatus_Sole_Trader=='Sole_Trader'):
                Legalstatus_Sole_Trader=1
                Legalstatus_Partnership=0
        
        elif(Legalstatus_Sole_Trader=='Partnership'):
            Legalstatus_Sole_Trader=0
            Legalstatus_Partnership=1
            
        else:
            Legalstatus_Sole_Trader=0
            Legalstatus_Partnership=0
        
        Year=2022-Year
        
        Product_type_Petrol=request.form['Product_type_Petrol']
        
        if(Product_type_Petrol=='Petrol'):
            Product_type_Petrol=1
        else:
            Product_type_Petrol=0
        
        Payment_type_Direct_Debit =  request.form['Payment_type_Direct_Debit']
        
        if(Payment_type_Direct_Debit=='Direct_Debit'):
            Payment_type_Direct_Debit=1
        else:
            Payment_type_Direct_Debit=0
            
            
        prediction=model.predict([[Volume,Budget,Year,Product_type_Petrol,
                                   Legalstatus_Partnership,Legalstatus_Sole_Trader, 
                                   Payment_type_Direct_Debit]])
        
        output=round(prediction[0],2)
        
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you we can get you a credit")
        else:
            return render_template('index.html',prediction_text="Your monthly credit limit {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)