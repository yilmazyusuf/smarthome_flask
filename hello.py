from flask import Flask
from flask import request
import RPi.GPIO as GPIO
import sqlite3
import json
from time import sleep
from datetime import datetime

app = Flask(__name__)

in1 = 24
in2 = 23
en = 25
temp1=1




GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)

p.start(20)


def get_current_status():
    conn = sqlite3.connect("/home/pi/qubis.db")
    cursor = conn.cursor()
    room = ('living_room',)
    living_room_status = cursor.execute('select status from curtains where room=?',room)
    return cursor.fetchone()[0] 
    
def update(status):
    conn = sqlite3.connect("/home/pi/qubis.db")
    cursor = conn.cursor()
    cursor.execute('update curtains set status  = ? where room=?',(status,'living_room'))
    conn.commit()
    return False

def get_response(last_status):
    response = {'status': last_status}
    return json.dumps(response)

def in_action(): 
    return get_response('in_action');

def opening():
    curtains_open()
    return get_response('opened');

def closing():
    curtains_close()
    return get_response('closed');

def process(status):
    methods = {0:in_action,1:opening,2:closing}
    return methods[status]()

def curtains_close():
    t1 = datetime.now()
    while(datetime.now()-t1).seconds <=21:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
    
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    update(1)
        
def curtains_open():
    t1 = datetime.now()
    while(datetime.now()-t1).seconds <=21:
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        
    
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    update(2)


@app.route("/curtains/living_room")
def curtains_living_room():
    current_status = get_current_status()
    update(0)
    return process(current_status)



if __name__  == '__main__':
    app.run(debug=True,host='0.0.0.0')
    
GPIO.cleanup()    