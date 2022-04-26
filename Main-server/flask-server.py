# code for parsing json file
# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, request, render_template, session, redirect, url_for
from flask_qrcode import QRcode
from flask_pymongo import PyMongo
import time
import random
import json
import pyqrcode
import png

ticket_num_length = 16
m_id_length = 10
s_epoch_length = 10
adult_length = 2
child_length = 2
valid_hr = 6

# creating a Flask app
app = Flask(__name__)
QRcode(app)
app.secret_key = 'any random string'

# path to the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/records_db"
mongodb_client = PyMongo(app)
db = mongodb_client.db


# provides homepage for the visitor
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('ticket_generation.html')
    return render_template('index.html')
    # return render_template('ticket_generation.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# receives the data from the webpage and sends the processed string back
@app.route('/getQR', methods=['POST'])
def getQR():
    # global result
    errors = []
    if request.method == 'POST':
        try:
            m_id = request.form['mid']
            adult = request.form['adult']
            child = request.form['child']
            # getting server epoch
            s_epoch = int(time.time())
            # generating random number
            ticket_num = random.randint(0, 1e16)
            content = {}
            for var in ["ticket_num", "m_id", "s_epoch", "adult", "child"]:
                content[var] = eval(var)
            # print("db record string", content)

            # Inserting record into the db
            db.records.insert_one(content)

            # converting the dict to QR code format
            result = str(ticket_num).zfill(ticket_num_length) + str(m_id).zfill(m_id_length) + str(s_epoch).zfill(
                s_epoch_length) + str(adult).zfill(adult_length) + str(child).zfill(child_length)
            print(result)
        except:
            errors.append("Please verify details in the form")

        return render_template('printQR.html', errors=errors, result=result)

    else:
        return 'invalid request'


@app.route('/get_validity', methods=['GET'])
def get_validity():
    arg = request.args.get("scanQR")
    # print(arg)
    # ticket_num = arg[0:16]
    s_epoch = int(arg[26:36])
    print(s_epoch)
    curr_epoch = int(time.time())
    validity = curr_epoch - s_epoch
    if validity < valid_hr * 3600:
        return 'ticket is valid'
    else:
        return 'ticket is invalid'


# driver function
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80, threaded=True)
