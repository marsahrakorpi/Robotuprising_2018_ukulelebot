#pip install pyserial
#needed for this to be able to work
import serial

import time 
ArduinoUnoSerial = serial.Serial('com6',500000)

if ArduinoUnoSerial:
    print ("Arduino found!")
else:
    print ("Arduino connecition failed")
    exit()

while True:     
    print ArduinoUnoSerial.readline()    



    