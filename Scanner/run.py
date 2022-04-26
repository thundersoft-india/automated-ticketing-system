# import time
# a=time.gmtime()
# print(a)
# b=time.gmtime(0)
# print(b)
# validity=a-b
# print(validity)
# import time

# start = "09:35:23"
# end = "10:23:00"
# start_dt = datetime.datetime.strptime(start, '%H:%M:%S')
# end_dt = datetime.datetime.strptime(end, '%H:%M:%S')
# diff = (end_dt - start_dt)
# print(diff)

# print(time.time())
import geocoder
import time
from flask import Flask, request

app = Flask(__name__)


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

if __name__ == '__main__':
    # export FLASK_ENV=development
    # flask run
    app.run(host="0.0.0.0", port= "5000",debug=True)
    #app.run()
    # flask run --host=0.0.0.0 --port=80
    # app.run(port=80)
    # app.run(host='0.0.0.0', port=80)
    # app.run(host='0.0.0.0', port='80', debug=True)
"""
import time
from flask import Flask
app = Flask(__name__)


@app.route('/',methods = ['GET'])  
def login():
    arg=request.args.get('uname')
    s_epoch = int(arg[26:36])
    print(s_epoch)
    curr_epoch = int(time.time())
    validity = curr_epoch - s_epoch
    if validity < s_epoch:
        return 'ticket is valid'
    else:
        return 'ticket is invalid'
if __name__ == '__main__':
    app.run(host="0.0.0.0", port= "80",debug=True) """
