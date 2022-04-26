from flask import Flask, request, render_template, redirect, url_for, session
from flask_pymongo import PyMongo
from pyqrcode import QRCode
from flask_qrcode import QRcode

import json
import pyqrcode

adults_length = 2
kids_length = 2
adults_cost_length = 3
kids_cost_length = 4
payment_mode_length = 4
total_length = 5

app = Flask(__name__)
QRcode(app)
app.secret_key = 'any random string'
app.config["MONGO_URI"] = "mongodb://localhost:27017/harinidb"
mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route("/")
def form1():
    print("flask2")
    return render_template('index.html')

@app.route('/wel2', methods=['GET'])
def form():
    print("flask")
    return render_template('ticform2-1.html')

'''@app.route('/wel2', methods=['POST'])
def form():
    print("flask")
    return render_template('ticform2-1.html')'''


@app.route('/wel3', methods=['POST'])
def form3():
    print("flask3")
    return render_template('ticform2-1.html')


@app.route('/getQR', methods=['POST','GET'])
def getQR():
    result = ""
    errors = []
    if request.method == 'POST':
        try:
            adults = request.form['adults']
            kids = request.form['kids']
            adults_cost = request.form['adults_cost']
            kids_cost = request.form['kids_cost']
            total = request.form['total']
            payment_mode = request.form['payment_mode']

            content = {}
            for var in ["adults", "kids", "adults_cost", "kids_cost", "total", "payment_mode"]:
                content[var] = eval(var)
            # print("db record string", content)

            # Inserting record into the db
            db.records.insert_one(content)

            # converting the dict to QR code format
            result = str(adults).zfill(adults_length) + str(kids).zfill(kids_length) + str(adults_cost).zfill(
                adults_cost_length) + str(kids_cost).zfill(kids_cost_length) + str(payment_mode).zfill(
                payment_mode_length) + str(total).zfill(total_length)
            print('hello')
            print(result)

        except:

            errors.append("Please verify details in the form")
            return render_template('ticform2-1.html', errors=errors, result=result)


    else:
        return 'invalid request'



if __name__ == '__main__':
    app.run(debug=True)
