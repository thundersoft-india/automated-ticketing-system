# import necessary libraries and functions
from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory, send_file
from flask_qrcode import QRcode
from flask_pymongo import PyMongo
import time
import random

# twilio Integration
from twilio.rest import Client
import qrcode
import socket
import os

ticket_num_length = 16
m_id_length = 10
s_epoch_length = 10
adult_length = 2
child_length = 2
valid_hr = 6

hname = socket.gethostname()
server_IP = '192.168.0.1'
UPLOAD_FOLDER = 'QRCodes'
# imageName = ''
mobile_no = '2269755074'

# creating a Flask app
app = Flask(__name__, static_folder=UPLOAD_FOLDER)
QRcode(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'any random string'

# path to the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/records_db"
mongodb_client = PyMongo(app)
db = mongodb_client.db

# Twilio related Data
account_sid = sid
auth_token = auth
client = Client(account_sid, auth_token)


# provides homepage for the visitor
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('VisitorDetails.html')
    return render_template('index.html')


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

            # Twilio Integration
            img = qrcode.make(result)
            imageName = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
            imageName = imageName + '.png'
            img.save(UPLOAD_FOLDER + '/' + imageName)
            media_url = ['http://' + hname + ':5000/' + UPLOAD_FOLDER + '/' + imageName]
            print(media_url)
            # Send WhatsApp Message with QR Code
            # message = client.messages.create(
            #     body='Please use this QR Code at Entry',
            #     media_url = ['http://' + hname + ':5000/' + path + '/' + imageName],
            #     from_='whatsapp:+14155238886',
            #     to='whatsapp:+1' + mobile_no
            # )

            # print(message.sid)

        except:
            errors.append("Please verify details in the form")

        return render_template('TicketGenerator.html', errors=errors, result=result, adult=adult, child=child,
                               billNo=ticket_num, adult_total=str(int(adult) * 150), child_total=str(int(child) * 75),
                               total=str(int(adult) * 150 + int(child) * 75))

    else:
        return 'invalid request'


@app.route('/QRCodes/<name>', methods=['GET'])
def get_image(name):
    print(name)
    # current_path = app.config['UPLOAD_FOLDER'] + '/' + name
    # print(current_path)
    # print(os.path.isfile(current_path))
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


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
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
