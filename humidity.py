import Adafruit_DHT
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 20

def getHumudity():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    response =  {'temperature':"{0:0.1f}".format(temperature),'humidity':"{0:0.1f}".format(humidity)}
    return response

#sudo python3 -m pip install --upgrade pip setuptools wheel
#sudo pip3 install Adafruit_DHT    
#/usr/local/lib/python3.7/dist-packages/Adafruit_DHT/platform_detect.py
# elif match.group(1) == 'BCM2711':
#return 3
#https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/