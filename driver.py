import serial, time
import threading
import requests
from datetime import datetime
import json

url = 'http://192.168.137.1:5000/outlets/sendData'
measurements = []

#ser = serial.Serial("/dev/i2c-1",9600,timeout=10)
ser = serial.Serial(port='/dev/ttyS0')
def readport():
    while 1:

        msg = ser.read(25).hex()
        #print(msg)
        volt = int(msg[3*2:5*2],16)/10
        current = int(msg[5*2:7*2],16)/1000
        #print("Volt: ", volt, " V")
        #print("Current: ", current, " A")
        power = int(msg[7*2:16*2],16)/10
        #print("Factor: ", int(msg[19*2:21*2],16)/100)
        #print("Power: ", power, " W")


        measurements.append([volt, current])

try:
    t1=threading.Thread(target=readport)
    t1.start()
except:
    print("Error")

while 1:
    if len(measurements)==30:
        sumI = 0
        sumV = 0
        for x in measurements:
            sumV = sumV + x[0]
            sumI = sumI + x[1]
        print("Average")
        print(sumV/30)
        print(sumI/30)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        myobj = {'outletId': 1,'t': dt_string, 'V':sumV/30, 'I': sumI/30}
        x = requests.post(url, data =myobj)
        
        measurements = []
    #print("Send:")
    ser.write(bytes.fromhex("f8 04 00 00 00 0a 64 64"))
    time.sleep(2)