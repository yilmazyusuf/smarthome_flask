import Adafruit_DHT
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 5

def getHumudity():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    response =  {'temperature':"{0:0.1f}".format(temperature),'humidity':"{0:0.1f}".format(humidity)}
    return response