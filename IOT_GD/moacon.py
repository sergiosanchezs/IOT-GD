# -*- coding: iso-8859-1 -*-
# /usr/lib/python2.7/moacon.py
# moacon/moacon1.py: the DB-API 1.0 interface
#
# Copyright (C) 2016 Sergio Sanchez <sergio.sanchezs@ingenieros.com>
#
# This file is part of Rpi-IoT.
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#	claim that you wrote the original software. If you use this software
#	in a product, an acknowledgment in the product documentation would be
#	appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#	misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#
# The porpose of this software is to use the Moacon Modules from ComfileTech.com 
# with the RASPBERRY PI MODELS A+, B+, RASPBERRY PI 2 B AND RASPBERRY PI 3 B,
# with the industrial board named "RPi Industrial IOT Gateway" where you can 
# get in www.rpi-iot.com

import serial
import time
# import sys

def OpenSerialfor_Moacon():
	global ser_moacon
	# This function works well for Raspberry Pi 3 when you disable the bluetooth and 
	# swap the virtual or software serial port with the fisical serial port.
	# this apply for several raspberry models
	port = '/dev/serial0'
	ser_moacon = serial.Serial()
	ser_moacon.port = "/dev/serial0"
	ser_moacon.baudrate = 115200
	ser_moacon.parity = serial.PARITY_NONE
	ser_moacon.stopbits = serial.STOPBITS_ONE
	ser_moacon.bytesize = serial.EIGHTBITS
	ser_moacon.timeout = 0.01
	# it can be called like this:
	# ser_moacon = serial.serial('/dev/ttyS0', 115200)
	try:
		# Open a Moacon Serial port
		ser_moacon.open()
		print "serial port opened"
		return True
	except Exception as e:
		print "The serial port named: " + port + " couldn't open, Error: " + str(e)
		return False
		ser_moacon.close()

def CloseSerialfor_Moacon():
	global ser_moacon
	ser_moacon.close()

def checking_CRC_sum(data_str):
	l = len(data_str)
	check_crc = ord(data_str[1])
	for n in range(2, l-1):		# l-1: with this the sum must be zero.
		check_crc = check_crc ^ ord(data_str[n])
	return check_crc

#//=========================================================================================================================
#//=				FUNCION QUE EXTRAE LA DATA REAL DE LAS TRAMAS RECIBIDAS POR LOS MODULOS RS-ADIN4 Y RS-SADIN6			=
#//=========================================================================================================================
def Fix_RSModule_Data(read_data, debug=False):
	lenght_readData = len(read_data)

	if debug:
		print "Lenght: " + str(lenght_readData) + " -RAW Data: "
		for num in range(0,lenght_readData):
			print hex(ord(read_data[num])),
		print ""

	_MBrxdata = ""
	k = 0
	while k < lenght_readData:
		# swapping the "0x10 0x30" to "0x10"
		if read_data[k] == chr(0x10) and read_data[k+1] == chr(0x30):
			_MBrxdata += chr(0x10)
			k += 1	# Aditional jump to get analize the next raw data
		# swapping the "0x10 0x22" to "0x02"
		elif read_data[k] == chr(0x10) and read_data[k+1] == chr(0x22):
			_MBrxdata += chr(0x02)
			k += 1	# Aditional jump to get analize the next raw data
		# swapping the "0x10 0x23" to "0x03"
		elif read_data[k] == chr(0x10) and read_data[k+1] == chr(0x23):
			_MBrxdata += chr(0x03)
			k += 1	# Aditional jump to get analize the next raw data
		# Deleting the "0x4E 0x00", it is a data division of RS-ADIN4 Module
		elif read_data[k] == chr(0x4E) and read_data[k+1] == chr(0x00):
			k += 1	# Aditional jump to get analize the next raw data
		# Deleting the "0x44 0x00", it is a data division of RS-ADIN4 Module
		elif read_data[k] == chr(0x44) and read_data[k+1] == chr(0x00):
			k += 1	# Aditional jump to get analize the next raw data
		# If doesn't exist a coincidence with previous, we keep the raw data
		else:
			_MBrxdata += read_data[k]
		k += 1	# Normal jump to get analize the next raw data

	# Se imprimen los datos recibidos procesados con datos reales.
	if debug:
		print "=============================================="
		real_lenght = len(_MBrxdata)
		print "Lenght: " + str(lenght_readData) + " -Real Data: "
		for num in range(0,real_lenght):
			print hex(ord(_MBrxdata[num])),
		print ""


	return _MBrxdata

"""
=========================================================================================================================
=					READ FUNCTION OF MOACON MODULE RS_SADIN6 - SPEED COMMUNICATION: 115.200 BAUD						=
=	Buy this module in: http://www.comfiletech.com/rs-sadin6-ad-input/													=
=	New version: V1.2	Release Date:	2017-01-27																		=
=	It proccess the data before verify the check sum CRC																=
=========================================================================================================================
"""
def RS_SADIN6(ReadModule, debug=False):
	RS_Code = 0x27	# Defining the code of RS-SADIN6 Modules
	numChannels = 6	# Number of channels in the ADC Module
	# debug = False	# If you wanna to activate debug (print) for testing
	Values = RS_Read(ReadModule, RS_Code, numChannels, debug)
	return Values
"""
=========================================================================================================================
=					READ FUNCTION OF MOACON MODULE RS_ADIN4 - SPEED COMMUNICATION: 115.200 BAUD							=
=	Buy this module in: http://www.comfiletech.com/rs-adin4-ad-input/													=
=	New version: V1.2	Release Date:	2017-01-27																		=
=	It proccess the data before verify the check sum CRC but in some cases It verify the check sum CRC before it 		=
=	proccess the data																									=
=========================================================================================================================
"""
def RS_ADIN4(ReadModule, debug=False):
	RS_Code = 0x21	# Defining the code of RS-ADIN4 Modules
	numChannels = 4	# Number of channels in the ADC Module
	# debug = False	# If you wanna to activate debug (print) for testing
	Values = RS_Read(ReadModule, RS_Code, numChannels, debug)
	return Values
"""
=========================================================================================================================
=			READ FUNCTION OF MOACON MODULES RS_ADIN4 and RS_SADIN6 - SPEED COMMUNICATION: 115.200 BAUD					=
=	New version: V1.2	Release Date:	2017-01-27																		=
=========================================================================================================================
"""
def RS_Read (ReadModule, RS_Code, numChannels, debug):
	global ser_moacon		# Getting global variable of serial port
	RS_ADIN4_Code = 0x21	# Defining the code of RS-ADIN4 Modules
	RS_SADIN6_Code = 0x27	# Defining the code of RS-SADIN6 Modules
	STX = 0x02				# Start of Text
	ETX = 0x03				# End of Text
	rd_start = 0x30			# Position of the first module from ASCII code (0x30 = '0')
	count_attemps_read = 0	# Counter of how many time it request data from modules
	max_attemps_read = 3	# Maximum attemps 

	module_number = ReadModule + rd_start

	_Txb = [chr(STX), chr(RS_Code), chr(module_number), chr(ETX)]		# Defining the basic array
	crc = chr( RS_Code ^ (module_number) )							# Calculating the CRC

	if debug: print "The Real CRC is: " + hex(ord(crc))

	# Checking the CRC for hexadecimals 02, 03 and 10 in the frames.
	if crc == chr(0x02):	# the 02 is replace with 0x10 and 0x22
		_Txb.insert(3,chr(0x10))
		_Txb.insert(4,chr(0x22))
	elif crc == chr(0x03):	# the 03 is replace with 0x10 and 0x23
		_Txb.insert(3,chr(0x10))
		_Txb.insert(4,chr(0x23))
	elif crc == chr(0x10):	# the 10 is replace with 0x10 and 0x30
		_Txb.insert(3,chr(0x10))
		_Txb.insert(4,chr(0x30))
	else:	# if dont found any of those charaters just put in the frame the real CRC
		_Txb.insert(3,crc)

	# passing all the array data to a string data 
	tx_data = ""
	for data in _Txb:
		# print hex(ord(data))
		tx_data += data

	while count_attemps_read < max_attemps_read:

		ser_moacon.flushInput()
		if debug: print "Transmit: " + str(_Txb)
		ser_moacon.write(tx_data)		# Send the request channels data to moacon module
		count_attemps_read += 1

		read_data = ""
		read_data = ser_moacon.read(200)	# Read the data arrived from moacon modules
		# print type(read_data)	
		# read_data = readuntilchr03(ser_moacon, tx_data)

		# Print data to view how received the data
		lenght_readData = len(read_data)
		# if debug: print "Lenght: " + str(lenght_readData) + " -RAW Data: "
		# for num in range(0,lenght_readData):
		# 	if debug:
		# 		print hex(ord(read_data[num])),
		# if debug:
		# 	print ""
		# 	print "Read size: " + str(len(read_data))


		# Checking if there is data en read_data
		if lenght_readData > 0:	
			# RS_SADIN6 proccess the data before verify the check sum CRC.
			# if RS_Code == RS_SADIN6_Code:	# *¨*******************
			read_data = Fix_RSModule_Data(read_data, debug)		# Function that fix all modbus data to real data

			check_crc = checking_CRC_sum(read_data)				# Checking if the CRC of data is OK

			if debug: print "Check CRC: " + str(hex(check_crc))

			flag_pasted_frames = False		# Flag of joined frames. flag=True: 
			# poner un if len(read_data) > 5:
			if ord(read_data[1]) == RS_Code and check_crc == 0 and ord(read_data[2]) == module_number:
				# Extraer, procesar y retornar arreglo
				if debug: print "No spliting, CRC ===== OK == OK == OK ====="
				count_attemps_read = 3
				pass
			else:
				# read_data = read_data[0:read_data.index(chr(0x03))+1]
				if debug: print "Looking two frames together"
				try:
					read_data.index(chr(0x03)+chr(0x02))	# Verify if there are two joined frames searching 0x03 and 0x02 in hex
				except Exception as e:
					# Si detecta que no hay tramas unidas
					# If detects that arent joined frame 
					if debug: print "No frames together"
					flag_pasted_frames = True		# Flag that that show at the end if in the data received are two joined frames
					pass
				else:	# Si hay 2 tramas unidas, Se separan en dos variables para analizar cual es la verdadera con el CRC
					if debug: print "frames together found"
					read_data1 = read_data[0 : read_data.index(chr(0x03)+chr(0x02)) + 1]
					read_data2 = read_data[read_data.index(chr(0x03)+chr(0x02)) + 1 : lenght_readData + 1]
					# Calcular CRC de la parte 1 y 2
					check_crc1 = checking_CRC_sum(read_data1)
					check_crc2 = checking_CRC_sum(read_data2)
					if debug:
						print "Real size data1: " + str(read_data1.index(chr(0x03))+1)
						print "Check CRC1: " + str(hex(check_crc1))
						print "Real size data2: " + str(read_data2.index(chr(0x03))+1)
						print "Check CRC2: " + str(hex(check_crc2))
					# Revisar si los checksum son iguales a 0 y el código coincide
					if ord(read_data1[1]) == RS_Code and check_crc1 == 0 and ord(read_data[2]) == module_number:
						# Extraer, procesar y retornar arreglo de la parte 1
						read_data = read_data1
						count_attemps_read = max_attemps_read
						pass
					elif ord(read_data2[1]) == RS_Code and check_crc2 == 0 and ord(read_data[2]) == module_number:
						# Extraer, procesar y retornar arreglo de la parte 2
						read_data = read_data2
						count_attemps_read = max_attemps_read
						pass
					else:	# Si no es ninguna de las dos no hace nada, la idea es que pase a revisar si hay mas tramas unidas
						flag_pasted_frames = True
						pass


			# if read_data.index(chr(0x03)+chr(0x02)):
			# 	read_data = read_data[read_data.index(chr(0x03)+chr(0x02))+1:lenght_readData+1]
			
			if not flag_pasted_frames:
				if debug: print "Real size: " + str(read_data.index(chr(0x03))+1)
				RawData = []
				if len(read_data) > 6:
					# RS_ADIN4 verify the check sum CRC before the proccess the data
					# if RS_Code == RS_ADIN4_Code: read_data = Fix_RSModule_Data(read_data)	# Function that fix all modbus data to real data***************
					k = 3
					data = 0
					if debug: print "Array size: " + str(len(read_data))
					"""Cicle to extract the real ADC data to proccess in the specific application"""
					for n in range(0, numChannels):
						data = ( ord(read_data[k]) * 256 ) + ord(read_data[k+1])
						if data >= 11000:
							data = -1
						RawData.insert(n, data)
						# print "Dato " + str(n+1) + ": " + str(RawData[n])		# Print example
						k += 2
					return RawData
				else:
					for n in range(0, numChannels):
						RawData.insert(n, -2)
					return RawData
					
			elif count_attemps_read == max_attemps_read:	# entra cuando no hay tramas juntas
				RawData = []
				for n in range(0, numChannels):
					RawData.insert(n, -3)
				return RawData

			time.sleep(.03)
		# if there is no data in read_data fill the array with -4 to show an error.
		else:
			RawData = []
			for n in range(0, numChannels):
				RawData.insert(n, -4)
			return RawData

		""" 
		When data result in each channel is:
		-> -1: probably the channel is damaged.
		-> -2: Probably the data received is incomplete.
		-> -3: It tried to read 3 times and it couldn't get an answer from the module. 
		-> -4: Module is Disconnected. Please verify the connection.
		"""

"""
=====================================================================================
=			READING EXAMPLE CODE FOR RS_ADIN4. TESTING AND WORKING					=
=====================================================================================
"""
# import serial
# import time
# import IOT.moacon
# ModuleNumber = 1
# if __name__ == '__main__':	
# 	if IOT.moacon.OpenSerialfor_Moacon() is True:
# 		results = IOT.moacon.RS_ADIN4(ModuleNumber)
# 		# print results
# 		print "Module " + str(ModuleNumber)
# 		for res in range(0, 4):
# 			print "Channel " + str(res+1) + ": " + str(results[res])
# 	IOT.moacon.CloseSerialfor_Moacon()
"""
=====================================================================================
=			READING EXAMPLE CODE FOR RS_SADIN6. TESTING AND WORKING					=
=====================================================================================
"""
# import serial
# import time
# import IOT.moacon
# ModuleNumber = 7
# if __name__ == '__main__':
# 	if IOT.moacon.OpenSerialfor_Moacon() is True:
# 		results = IOT.moacon.RS_SADIN6(ModuleNumber)
# 		# print results
# 		print "Module " + str(ModuleNumber)
# 		for res in range(0, 6):
# 			print "Channel " + str(res+1) + ": " + str(results[res])
# 	IOT.moacon.CloseSerialfor_Moacon()