import socket
import pyaudio
import sounddevice as sd
import os
import wave
#print (sd.query_devices())
HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 48748        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 4096

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            while data != '':
                print(data)
            f.close()
            if not data:
                break
            conn.sendall(data)
