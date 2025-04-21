#!/usr/bin/env python3

#Based on resources from https://w140.com/tekwiki/wiki/TDS210
#(especially the example RS232 programs https://w140.com/tekwiki/images/c/c5/066-0108-00.zip )

import serial
import numpy as np

##### Consts
PORT='/dev/ttyS0'
BAUD=9600
PARITY=serial.PARITY_NONE
STOPBITS=serial.STOPBITS_ONE
BYTESIZE=serial.EIGHTBITS
CH="CH1"

RECORD_LEN = 2500
DATA_START = 512
DATA_END = 1023
####### Fcts
def get_volt_scale(ser, CH):
	command=f"{CH}:SCALE?\n"
	ser.write(bytes(command,'ascii'))
	return float(ser.readline().decode('ascii'))

def get_time_scale(ser):
	ser.write(b"HORIZONTAL:MAIN:SCALE?\n")
	return float(ser.readline().decode('ascii'))

def get_samp_rate(ser): #Untested
	ser.write(b"WFMPre:XINcr?\n")
	return float(ser.readline().decode('ascii'))

def set_data_source(ser, ch):
	command=f"DATA:SOURCE {ch}\n"
	ser.write(bytes(command,'ascii'))
	
def set_data_encoding_ascii(ser):
	command=f"DATA:ENCDG ASCII;WIDTH 1\n"
	ser.write(bytes(command,'ascii'))

def set_record_len(ser,_len):
	command=f"HORIZONTAL:RECORDLENGTH {_len}\n"
	ser.write(bytes(command,'ascii'))
	
def get_record_len(ser):
	command=f"HORIZONTAL:RECORDLENGTH?\n"
	ser.write(bytes(command,'ascii'))
	return ser.readline()

def set_data_start(ser, pos):
	command=f"DATA:START {pos}\n"
	ser.write(bytes(command,'ascii'))
	
def set_data_end(ser, pos):
	command=f"DATA:STOP {pos}\n"
	ser.write(bytes(command,'ascii'))

def set_acquire_run(ser):
	command=f"ACQUIRE:STATE RUN\n"
	ser.write(bytes(command,'ascii'))

def get_curve(ser):
	command=f"CURVE?\n"
	ser.write(bytes(command,'ascii'))
	return ser.readline()
	
def parse_curve(data,volt_scale):
	data = data.decode('ascii')
	data = np.fromstring(data, dtype=np.float32, sep=',')
	data *= volt_scale
	return data
	
	
###### Main

ser = serial.Serial(port=PORT, baudrate=BAUD, parity=PARITY, stopbits=STOPBITS, bytesize=BYTESIZE)

ser.isOpen()
ser.write(b'\n')

set_data_source(ser, CH)
set_data_encoding_ascii(ser)
set_record_len(ser,RECORD_LEN)
set_data_start(ser, DATA_START)
set_data_end(ser,DATA_END)

while(True):
	volt_scale = get_volt_scale(ser, CH)
	volt_scale = (volt_scale * 5.12) / 128

	data = get_curve(ser)
	print(parse_curve(data, volt_scale))
