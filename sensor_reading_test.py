import time 
import serial 
  
ser = serial.Serial('COM4', 9600) 
 
while True: 
 value = ser.readline() 
 print(value) 
 time.sleep(0.5) 