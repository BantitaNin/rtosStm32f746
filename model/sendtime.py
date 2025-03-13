import time
import serial
from datetime import datetime
import serial.tools.list_ports

def find_first_port():
    ports = list(serial.tools.list_ports.comports())
    if ports:
        first_port = ports[2].device
        print(f"Found port: {first_port} - {ports[0].description}")
        return first_port
    return None

ser = serial.Serial(
    port=find_first_port(),
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.writeTimeout = 0 
ser.isOpen() 

TM1 = int(round(time.time() * 1000000))   
ser.write((str(TM1) + "\r\n").encode())  # แปลงเป็นไบต์
time.sleep(2) 

TM2 = int(round(time.time() * 1000000))
ser.write((str(TM2) + "            \r\n").encode())  # แปลงเป็นไบต์
time.sleep(2)

TM3 = int(round(time.time() * 1000000))
ser.write((str(TM3) + "            \r\n").encode())  # แปลงเป็นไบต์
time.sleep(2) 

TM4 = int(round(time.time() * 1000000)) 
ser.write((str(TM4) + "            \r\n").encode())  # แปลงเป็นไบต์
