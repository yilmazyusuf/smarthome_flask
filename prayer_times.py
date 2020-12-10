import http.client
import sqlite3
import json 
from datetime import datetime


conn = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 2KlqpwdX6oNZLlGtN271bE:6g6mdj4pDdrZwUl1LIMj8O"
    }

conn.request("GET", "/pray/all?data.city=istanbul", headers=headers)

res = conn.getresponse()
data = res.read()

rs  = json.loads(data.decode("utf-8")) 

fajr    = rs['result'][0]['saat']
sunrise = rs['result'][1]['saat']
dhuhr   = rs['result'][2]['saat']
asr     = rs['result'][3]['saat']
maghrib = rs['result'][4]['saat']
isha    = rs['result'][5]['saat']
date = datetime.today().strftime('%Y-%m-%d')

conn = sqlite3.connect("/home/pi/Documents/smarthome_flask/qubis.db")
cursor = conn.cursor()
cursor.execute('update prayer_times set updated_at=?,fajr=?,sunrise=?,dhuhr=?,asr=?,maghrib=?,isha=? where id = 1', (date,fajr,sunrise,dhuhr,asr,maghrib,isha))
conn.commit()
print("Prayer Times : "+ date,fajr,sunrise,dhuhr,asr,maghrib,isha)
