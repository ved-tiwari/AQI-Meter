from flask import Flask, request, render_template
import requests
import numpy as np
from sklearn.linear_model import LinearRegression
import array as arr
import time

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():

    equation = 0

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
       
        #GET Request from JavaScript
        historicalAQI = request.form.get("array")
        historicalAQI = historicalAQI.split(",")
        historicalAQI.reverse()

        for i in range(61):
            historicalAQI.pop(0)

        # Machine Learning Segment
        length = len(historicalAQI) + 1
        X = np.arange(1, length).reshape(-1,1)
        Y = historicalAQI
        reg = LinearRegression().fit(X, Y)

        slope = reg.coef_[0]
        y_intercept = reg.intercept_
                
        predictions = []

        for i in range(5):
            prediction = len(historicalAQI) + i
            equation = slope * prediction
            equation = equation + y_intercept

            equation = round(equation)
            predictions.append(equation)


        if equation == 0:
            return {
                "status": "success",
                "action": "dont_do_anything"
            }

        if equation != 0:
            return {
                "action": "do_something",
                "value_to_show": predictions
            }
    
@app.route("/about", methods=["POST", "GET"])
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run()

