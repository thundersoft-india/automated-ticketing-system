from flask import Flask, request, render_template, redirect, url_for, session
from flask_pymongo import PyMongo
from pyqrcode import QRCode
from flask_qrcode import QRcode

import json
import pyqrcode
import geocoder
import time
#from flask import Flask, request

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

@app.route('/login', methods=['GET'])
def hello_world():
    arg = request.args.get('uname')
    a = int(arg[26:36])
    my_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(a))
    print(my_time)
    ## get the input from the user
    string = arg[16:26]
    ## initializing a new string to append only alphabets
    only_alpha = ""
    ## looping through the string to find out alphabets
    for char in string:
    ## checking whether the char is an alphabet or not using chr.isalpha() method
        if char.isalpha():
            only_alpha += char
    ## printing the string which contains only alphabets
    ipadress=geocoder.ip('me')
    latlong=ipadress.latlng
    print(only_alpha)
    s_epoch = int(arg[26:36])
    curr_epoch = int(time.time())
    validity = curr_epoch - s_epoch
    if validity < 21600:
        if validity < 3600:
            return ('valid ticket,' + arg[0:16] + ',' + str(only_alpha) + ',' + str(my_time) + ',' + arg[36:38] + ',' + arg[38:40]+ ',' + str(latlong)+ ',' + 'you have less than 6 hour left')
        elif validity < 7200 and validity > 3600:
            return ('valid ticket,' + arg[0:16] + ',' + str(only_alpha) + ',' + str(my_time) + ',' + arg[36:38] + ',' + arg[38:40]+ ',' + str(latlong)+ ',' + 'you have less than 5 hour left')
            #return ('valid ticket,' + arg[1:16] + ',' + arg[17:25] + ',' + str(my_time) + ',' + arg[36] + ',' + 'you have less than 5 hour left')
        elif validity < 10800 and validity > 7200:
            return ('valid ticket,' + arg[0:16] + ',' + str(only_alpha) + ',' + str(my_time) + ',' + arg[36:38] + ',' + arg[38:40]+ ',' + str(latlong)+ ',' + 'you have less than 4 hour left')
        elif validity < 14400 and validity > 10800:
            return ('valid ticket,' + arg[0:16] + ',' + str(only_alpha) + ',' + str(my_time) + ',' + arg[36:38] + ',' + arg[38:40]+ ',' + str(latlong)+ ',' + 'you have less than 3 hour left')
        elif validity < 18000 and validity > 14400:
            return ('valid ticket,' + arg[0:16] + ',' + str(only_alpha) + ',' + str(my_time) + ',' + arg[36:38] + ',' + arg[38:40]+ ',' + str(latlong)+ ',' + 'you have less than 2 hour left')
        elif validity < 21600:
            return ('valid ticket,' + arg[0:16] + ',' + str(only_alpha) + ',' + str(my_time) + ',' + arg[36:38] + ',' + arg[38:40]+ ',' + str(latlong)+ ',' + 'you have less than 1 hour left')
    else:
        return ('invalid ticket')
        # return validity
        # return (',valid_ticket,'+'unique sequence number '+arg[1:16]+',Machine ID'+arg[17:25]+',Date and time of ticket '+arg[26:36]+',Gender '+arg[36])
        # return ('valid ticket,'+arg[1:16]+','+arg[17:25]+','+arg[26:36]+','+arg[36]+','+str(validity)+'hello Ruthvik Mallikarjun')
    #else:
        #return validity
        #return (',invlaid_ticket,'+'unique sequence number '+arg[1:16]+',Machine ID'+arg[17:25]+',Date and time of ticket '+arg[26:36]+',Gender '+arg[36])
        #return ('invalid ticket,'+arg[1:16]+','+arg[17:25]+','+arg[26:36]+','+arg[36]+','+str(validity))

@app.route('/epoch')
def epoch():
    a=time.time()
    c=int(a)
    b=str(c)
    return b

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
    #app.run(host="0.0.0.0", port= "5000",debug=True)
