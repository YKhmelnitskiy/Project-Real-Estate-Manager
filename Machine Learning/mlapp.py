#  Authored by ‘Robert Rua’, ‘Jeremy Halek’, ‘Gaston Alvarado’, 'Erika Haren,  ‘Yevgeniy Khmelnitskiy’
#import necessary libraries
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import pandas as pd

#Create our app

    

# df = pd.DataFrame.from_dict (inputs)
# X_scaler = StandardScaler().fit(X)
# print(X_scaler)
# X_scale = X_scaler.transform(X)
# print(X_scale)

# inputs=[[5, 5, 55, 5, 5, 5, 5]]
# df = pd.DataFrame.from_dict (inputs)
# X = df.iloc[:,:]
# X_scaler = StandardScaler().fit(X)
# X_scale = X_scaler.transform(X)

model = pickle.load(open('model.pkl','rb'))
  
# model=pickle.load(open('regressor.pkl','rb'))   

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():

    if request.method == "POST":
        medhousing = request.form["medhousing"]
        bedrooms = request.form["bedrooms"]
        bathrooms = request.form["bathrooms"]
        yearbuilt = request.form["yearbuilt"] #sqaure footage
        acres = request.form["acres"]
        graduates = request.form["graduates"]
        foodstamps = request.form["foodstamps"]

        inputs=[]

        inputs.append(medhousing)
        inputs.append(bedrooms)
        inputs.append(bathrooms)
        inputs.append(yearbuilt)
        inputs.append(acres)
        inputs.append(graduates)
        inputs.append(foodstamps)

        inputs2=list(map(float, inputs))

        print(inputs2)

        X1 = np.array(inputs2)
        X=X1.reshape(1, -1)
        prediction= model.predict(X)
        print(prediction)
        output = prediction[0]
        output5=output[0]
        output6=int(output5)
        output2= "{:,}".format(output6)
        print(output2)
    
        return render_template("registration.html", output2=output2)  

    return render_template("registration.html", output2="0")  



# @app.route("/Registration", methods = ["GET", "POST"])
# def registration():
    
#     if request.method == "POST":
#         medhousing = request.form["medhousing"]
#         bedrooms = request.form["bedrooms"]
#         bathrooms = request.form["bathrooms"]
#         yearbuilt = request.form["yearbuilt"] #sqaure footage
#         acres = request.form["acres"]
#         graduates = request.form["graduates"]
#         foodstamps = request.form["foodstamps"]

#         inputs=[]

#         inputs.append(medhousing)
#         inputs.append(bedrooms)
#         inputs.append(bathrooms)
#         inputs.append(yearbuilt)
#         inputs.append(acres)
#         inputs.append(graduates)
#         inputs.append(foodstamps)

#         inputs2=list(map(int, inputs))

#         print(inputs2)

#         X1 = np.array(inputs2)
#         X=X1.reshape(1, -1)
#         prediction= model.predict(X)
#         print(prediction)
#         output = prediction[0]
#         output5=output[0]
#         output6=int(output5)
#         output2= "{:,}".format(output6)
#         print(output2)
    
#         return render_template("registration.html", output2=output2)  

#     return render_template("registration.html", output2="0")  


if __name__ == "__main__":

    app.run()