import socket
import pyaudio
import sounddevice as sd
import wave
#print (sd.query_devices())
HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 48748        # Port to listen on (non-privileged ports are > 1023)


with open('myFile.pcm', 'rb') as pcmfile:
        pcmdata = pcmfile.read()
        with wave.open('myFile.wav', 'wb') as wavfile:
            wavfile.setparams((1, 1, 48000,1, 'NONE', 'NONE'))
            wavfile.writeframes(pcmdata)

"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(4096)
           
            while data != "":
                try:
                    data = conn.recv(4096)
                    stream.write(data)
                except socket.error:
                    print("Client Disconnected")
                break
            if not data:
                break
"""            
            

