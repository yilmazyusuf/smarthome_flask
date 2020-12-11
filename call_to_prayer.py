import sqlite3
from datetime import datetime
import time
import os
import random
import subprocess
import mplayer
conn = sqlite3.connect("/home/pi/Documents/smarthome_flask/qubis.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('select * from prayer_times where id = 1')
r = cursor.fetchone()

call_to_prayer_times = {r['fajr'],r['sunrise'],r['dhuhr'],r['maghrib'],r['isha']}
#print (r['fajr'])
#print (r['sunrise'])
#print (r['dhuhr'])
#print (r['asr'])
#print (r['maghrib'])
#print (r['isha'])
current_time = time.strftime("%H:%M")

#print(random.choice(os.listdir("/home/pi/Documents/smarthome_flask/media/ezan")))
prayers_path = "/home/pi/Documents/smarthome_flask/media/ezan"
if((current_time  in call_to_prayer_times) == True):
    call_to_prayer_file = random.choice(os.listdir(prayers_path))
    file_path = prayers_path + '/' + call_to_prayer_file 
    #os.system('nohup ./connect_speaker.sh </dev/null &>/dev/null &')
    os.system('mplayer -ao alsa:device=hw=1.0 '+file_path)
    print("Prayer Time:")
    
