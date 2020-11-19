from flask import Flask
from flask import request
import RPi.GPIO as GPIO
import sqlite3
import json
from time import sleep
from datetime import datetime





app = Flask(__name__)



@app.route("/lights/living_room_middle")
def lights_living_room_middle():
    current_status = get_current_status('living_room_middle')
    changed = change_status(current_status,4)
    update(changed,'living_room_middle')

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
    
    
    current_status = get_curtain_status('living_room')
    update_curtain(0,'living_room')
    
    return process_curtain(current_status)

def update_curtain(status,room):
    conn = sqlite3.connect("/home/pi/qubis.db")
    cursor = conn.cursor()
    cursor.execute('update curtains set status  = ? where room=?',(status,room))
    conn.commit()
    
    
    return False

def process_curtain(status):
    methods = {0:curtain_in_action,1:opening_curtain,2:closing_curtain}
    return methods[status]()

def get_curtain_response(last_status):
    response = {'status': last_status}
    return json.dumps(response)

def curtain_in_action(): 
    return get_curtain_response('in_action');

def opening_curtain():
    curtains_open()
    return get_curtain_response('opened');

def closing_curtain():
    curtains_close()
    return get_curtain_response('closed');

def curtains_open():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(25,GPIO.OUT)
    p=GPIO.PWM(25,12000)
    p.start(100)
    
    GPIO.setup(24,GPIO.OUT)
    GPIO.output(24,GPIO.LOW)
    
    GPIO.setup(23,GPIO.OUT)
    GPIO.output(23,GPIO.LOW)
    
    t1 = datetime.now()
    while(datetime.now()-t1).seconds <=16:
        
        GPIO.output(23,GPIO.HIGH)
        GPIO.output(24,GPIO.LOW)
        
    
    GPIO.output(24,GPIO.LOW)
    GPIO.output(23,GPIO.LOW)
    update_curtain(2,'living_room')
    GPIO.cleanup([23,24,25])

def curtains_close():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(25,GPIO.OUT)
    p=GPIO.PWM(25,12000)
    p.start(100)
    
    GPIO.setup(24,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    
    t1 = datetime.now()
    while(datetime.now()-t1).seconds <=16:
        GPIO.output(23,GPIO.LOW)
        GPIO.output(24,GPIO.HIGH)
    
    GPIO.output(23,GPIO.LOW)
    GPIO.output(24,GPIO.LOW)
    update_curtain(1,'living_room')
    GPIO.cleanup([23,24,25])

def get_curtain_status(curtain_room):
    conn = sqlite3.connect("/home/pi/qubis.db")
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
    conn = sqlite3.connect("/home/pi/qubis.db")
    cursor = conn.cursor()
    room = (node,)
    status = cursor.execute('select status from lights where name=?',room)
    return cursor.fetchone()[0] 

def update(status,node):
    conn = sqlite3.connect("/home/pi/qubis.db")
    cursor = conn.cursor()
    cursor.execute('update lights set status  = ? where name=?',(status,node))
    conn.commit()
    return conn.commit()


if __name__  == '__main__':
    app.run(debug=True,host='0.0.0.0')
GPIO.cleanup()      