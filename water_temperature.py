
import os
from time import sleep
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor = '/sys/bus/w1/devices/28-3c01d60739d4/w1_slave'
import RPi.GPIO as GPIO

def read_temp_raw():

   f = open(temp_sensor, 'r')
   lines = f.readlines()
   f.close()
   return lines

def read_temp():

  lines = read_temp_raw()
  #print(lines)
  while lines[0].strip()[-3:] == 'YES':
    sleep(0.2)
    lines = read_temp_raw()
    temp_result = lines[1].find('t=')
    

    if temp_result != -1:
        temp_string = lines[1].strip()[temp_result + 2:]
        # Temperature in Celcius
        temp = float(temp_string) / 1000.0
        # Temperature in Fahrenheit
        #temp = ((float(temp_string) / 1000.0) * (9.0 / 5.0)) + 32.0
        return temp



channel = 26
 


while True:
  current_temp = read_temp()
 
  if(current_temp >=30):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.HIGH)
  else:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.LOW)
    GPIO.cleanup(channel)
    
    
  print(read_temp())
  sleep(1)  

GPIO.cleanup(channel)          