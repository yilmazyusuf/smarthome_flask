from flask import Flask
from flask import request
import RPi.GPIO as GPIO
import sqlite3
import json
from humidity import *
from time import sleep
from datetime import datetime
from flask import jsonify
import os


#12 failed. (curtains en)
#Pull down on gpio 16 failed. (curtains en)
#Pull down on gpio 17 failed(ds18b20)
#Pull up on gpio 20 failed.(humudity)

#Pull up on gpio 21 failed.
#Pull up on gpio 27

curtain_pins = {'living_room':{'a':23,'b':24,'en':12,'action_second':16},'qubisch_room':{'a':6,'b':13,'en':16,'action_second':40}}

app = Flask(__name__)

UPLOAD_FOLDER = '/home/pi/Documents/smarthome_flask/streams'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/humidity")
def humidity():
    humud = getHumudity() 
    return jsonify(humud)

@app.route("/stream",methods=['GET', 'POST'])
def stream():

    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        fl = uploaded_file.save(file_path)
        os.system('amixer -c 1 set PCM 50%')
        os.system('mplayer -ao alsa:device=hw=1.0 '+file_path + ' > /dev/null 2>&1')
    return uploaded_file.filename 
    

@app.route("/lights/living_room_middle")
def lights_living_room_middle():
    
    current_status = get_current_status('living_room_middle')
    changed = change_status(current_status,22)
    update(changed,'living_room_middle')

    return "ok"

@app.route("/lights/living_room_led")
def lights_living_room_led():
    current_status = get_current_status('living_room_led')
    changed = change_status(current_status,18)
    update(changed,'living_room_led')

    return "ok"

@app.route("/lights/sleeping_room")
def lights_sleeping_room():
    current_status = get_current_status('sleeping_room')
    changed = change_status(current_status,27)
    update(changed,'sleeping_room')

    return "ok"


@app.route("/lights/aquarium")
def lights_aquarium():
    current_status = get_current_status('aquarium')
    changed = change_status(current_status,26)
    update(changed,'aquarium')

    return "ok"

@app.route("/lights/qubisch")
def lights_qubisch():
    current_status = get_current_status('qubisch')
    changed = change_status(current_status,21)
    update(changed,'qubisch')

    return "ok"



@app.route("/curtains/living_room")
def curtains_living_room():
    #23 ln 1 24 ln 2 en 25
    curtain_room ='living_room'
    current_status = get_curtain_status(curtain_room)
    update_curtain(0,curtain_room)
    return process_curtain(current_status,curtain_room)

@app.route("/curtains/qubisch_room")
def curtains_qubisch_room():
    curtain_room = 'qubisch_room'
    #23 ln 1 24 ln 2 en 25
    current_status = get_curtain_status(curtain_room)
    update_curtain(0,curtain_room)
    return process_curtain(current_status,curtain_room)

def update_curtain(status,room):
    conn = sqlite3.connect("/home/pi/Documents/smarthome_flask/qubis.db")
    cursor = conn.cursor()
    cursor.execute('update curtains set status  = ? where room=?',(status,room))
    conn.commit()
    
    
    return False

def process_curtain(status,curtain_room):
    methods = {0:curtain_in_action,1:opening_curtain,2:closing_curtain}
    return methods[status](curtain_room)

def get_curtain_response(last_status):
    response = {'status': last_status}
    return json.dumps(response)

def curtain_in_action(curtain_room): 
    return get_curtain_response('in_action');

def opening_curtain(curtain_room):
    curtains_open(curtain_room)
    return get_curtain_response('opened');

def closing_curtain(curtain_room):
    curtains_close(curtain_room)
    return get_curtain_response('closed');

def curtains_open(curtain_room):
    room_pins = curtain_pins[curtain_room]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(room_pins['en'],GPIO.OUT)
    p=GPIO.PWM(room_pins['en'],12000)
    p.start(100)

    GPIO.setup(room_pins['b'],GPIO.OUT)
    GPIO.output(room_pins['b'],GPIO.LOW)

    GPIO.setup(room_pins['a'],GPIO.OUT)
    GPIO.output(room_pins['a'],GPIO.LOW)

    t1 = datetime.now()
    while(datetime.now()-t1).seconds <= room_pins['action_second']:

        GPIO.output(room_pins['a'],GPIO.HIGH)
        GPIO.output(room_pins['b'],GPIO.LOW)

    GPIO.output(room_pins['b'],GPIO.LOW)
    GPIO.output(room_pins['a'],GPIO.LOW)
    update_curtain(2,curtain_room)
    GPIO.cleanup([room_pins['a'],room_pins['b'],room_pins['en']])

def curtains_close(curtain_room):

    room_pins = curtain_pins[curtain_room]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(room_pins['en'],GPIO.OUT)
    p=GPIO.PWM(room_pins['en'],12000)
    p.start(100)
    
    GPIO.setup(room_pins['b'],GPIO.OUT)
    GPIO.setup(room_pins['a'],GPIO.OUT)
    
    t1 = datetime.now()
    while(datetime.now()-t1).seconds <= room_pins['action_second']:
        GPIO.output(room_pins['a'],GPIO.LOW)
        GPIO.output(room_pins['b'],GPIO.HIGH)
    
    GPIO.output(room_pins['a'],GPIO.LOW)
    GPIO.output(room_pins['b'],GPIO.LOW)
    update_curtain(1,curtain_room)
    GPIO.cleanup([room_pins['a'],room_pins['b'],room_pins['en']])

def get_curtain_status(curtain_room):
    conn = sqlite3.connect("/home/pi/Documents/smarthome_flask/qubis.db")
    cursor = conn.cursor()
    room = (curtain_room,)
    living_room_status = cursor.execute('select status from curtains where room=?',room)
    return cursor.fetchone()[0] 



def light_on(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
        
    
    
def light_off(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    GPIO.cleanup(pin)

def change_status(status,pin):
    if status == 0 :
        print("low")
        
        light_on(pin)
        
        return 1
    
    if status == 1 :
        print("high")
        
        light_off(pin)
        
        return 0

def get_current_status(node):
    conn = sqlite3.connect("/home/pi/Documents/smarthome_flask/qubis.db")
    cursor = conn.cursor()
    room = (node,)
    status = cursor.execute('select status from lights where name=?',room)
    return cursor.fetchone()[0] 

def update(status,node):
    conn = sqlite3.connect("/home/pi/Documents/smarthome_flask/qubis.db")
    cursor = conn.cursor()
    cursor.execute('update lights set status  = ? where name=?',(status,node))
    conn.commit()
    return conn.commit()


if __name__  == '__main__':
    app.run(debug=True,host='0.0.0.0')
GPIO.cleanup()      
