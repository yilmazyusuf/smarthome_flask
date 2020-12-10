import sqlite3
import datetime
import http.client


conn = sqlite3.connect("/home/pi/Documents/smarthome_flask/qubis.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('select * from prayer_times where id = 1')
r = cursor.fetchone()


current = datetime.datetime.now().strftime('%H:%M')

living_room_open = datetime.datetime.strptime(r['sunrise'], '%H:%M').strftime('%H:%M')
qubisch_open  = (datetime.datetime.strptime(r['sunrise'], '%H:%M') +  datetime.timedelta(minutes=5)).strftime('%H:%M')

living_room_close = (datetime.datetime.strptime(r['maghrib'], '%H:%M') -  datetime.timedelta(minutes=30)).strftime('%H:%M')
qubisch_close = (datetime.datetime.strptime(r['maghrib'], '%H:%M') -  datetime.timedelta(minutes=25)).strftime('%H:%M')

conn = http.client.HTTPConnection("http://localhost:5000")

if(living_room_open == current or living_room_close == current):
    conn.request("GET", "/curtains/living_room")
    print (current,living_room_open,qubisch_open,living_room_close,qubisch_close)
if(qubisch_open == current or qubisch_close == current):
    conn.request("GET", "/curtains/qubisch_room")
    print (current,living_room_open,qubisch_open,living_room_close,qubisch_close)    


