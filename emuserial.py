import serial
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("port", help="Serial port to stream data to")
args = parser.parse_args()

portName = args.port

with open('data/raw_data.txt') as f:
    raw_data = f.readlines()

ser = serial.Serial()
ser.baudrate = 57600
ser.port = portName
ser.open()

for line in raw_data:
    ser.write(line.encode('utf-8'))