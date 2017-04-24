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
# The porpose of this software is to use the Moacon Module_Numbers from ComfileTech.com 
# with the RASPBERRY PI MODELS A+, B+, RASPBERRY PI 2 B AND RASPBERRY PI 3 B,
# with the industrial board named "RPi Industrial IOT Gateway" where you can 
# get in www.rpi-iot.com

import serial
import time
import struct
import sys

# =================================================================================
_CRC16TABLE = (
        0, 49345, 49537,   320, 49921,   960,   640, 49729, 50689,  1728,  1920, 
    51009,  1280, 50625, 50305,  1088, 52225,  3264,  3456, 52545,  3840, 53185, 
    52865,  3648,  2560, 51905, 52097,  2880, 51457,  2496,  2176, 51265, 55297, 
     6336,  6528, 55617,  6912, 56257, 55937,  6720,  7680, 57025, 57217,  8000, 
    56577,  7616,  7296, 56385,  5120, 54465, 54657,  5440, 55041,  6080,  5760, 
    54849, 53761,  4800,  4992, 54081,  4352, 53697, 53377,  4160, 61441, 12480, 
    12672, 61761, 13056, 62401, 62081, 12864, 13824, 63169, 63361, 14144, 62721, 
    13760, 13440, 62529, 15360, 64705, 64897, 15680, 65281, 16320, 16000, 65089, 
    64001, 15040, 15232, 64321, 14592, 63937, 63617, 14400, 10240, 59585, 59777, 
    10560, 60161, 11200, 10880, 59969, 60929, 11968, 12160, 61249, 11520, 60865, 
    60545, 11328, 58369,  9408,  9600, 58689,  9984, 59329, 59009,  9792,  8704, 
    58049, 58241,  9024, 57601,  8640,  8320, 57409, 40961, 24768, 24960, 41281, 
    25344, 41921, 41601, 25152, 26112, 42689, 42881, 26432, 42241, 26048, 25728, 
    42049, 27648, 44225, 44417, 27968, 44801, 28608, 28288, 44609, 43521, 27328, 
    27520, 43841, 26880, 43457, 43137, 26688, 30720, 47297, 47489, 31040, 47873, 
    31680, 31360, 47681, 48641, 32448, 32640, 48961, 32000, 48577, 48257, 31808, 
    46081, 29888, 30080, 46401, 30464, 47041, 46721, 30272, 29184, 45761, 45953, 
    29504, 45313, 29120, 28800, 45121, 20480, 37057, 37249, 20800, 37633, 21440, 
    21120, 37441, 38401, 22208, 22400, 38721, 21760, 38337, 38017, 21568, 39937, 
    23744, 23936, 40257, 24320, 40897, 40577, 24128, 23040, 39617, 39809, 23360, 
    39169, 22976, 22656, 38977, 34817, 18624, 18816, 35137, 19200, 35777, 35457, 
    19008, 19968, 36545, 36737, 20288, 36097, 19904, 19584, 35905, 17408, 33985, 
    34177, 17728, 34561, 18368, 18048, 34369, 33281, 17088, 17280, 33601, 16640, 
    33217, 32897, 16448)
"""CRC-16 lookup table with 256 elements.
    Built with this code:    
    
    poly=0xA001
    table = []
    for index in range(256):
        data = index << 1
        crc = 0
        for _ in range(8, 0, -1):
            data >>= 1
            if (data ^ crc) & 0x0001:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
        table.append(crc)
    output = ''
    for i, m in enumerate(table):
        if not i%11:
            output += "\n"
        output += "{:5.0f}, ".format(m)
    print output
    """

# =================================================================================
def _calculateCrcString(inputstring):
    """Calculate CRC-16 for Modbus.
    This function returns a two-byte CRC string, where the least significant byte is first.
    """
    # _checkString(inputstring, description='input CRC string')
 
    # Preload a 16-bit register with ones
    register = 0xFFFF
    # Proccess the data input with CRC table of 16 bits
    for char in inputstring:
        register = (register >> 8) ^ _CRC16TABLE[(register ^ ord(char)) & 0xFF]
 
    # return _numToTwoByteString(register, LsbFirst=True)
    # Putting lsbfirst in the result

    numberOfDecimals = 0
    multiplier = 10 ** numberOfDecimals
    integer = int(float(register) * multiplier)
    # integer = int(register)
    formatcode = '<H'  # Little-endian

    try:
        result = struct.pack(formatcode, integer)
    except:
        errortext = 'Error. The integer to send is probably out of range'

    if sys.version_info[0] > 2:
        return str(result, encoding='latin1')  # Python3 Compatible

    return result

# =================================================================================
def OpenSerialfor_ModPort():
	global serialport
	# This function works well for Raspberry Pi 3 when you disable the bluetooth and 
	# swap the virtual or software serial port with the fisical serial port.
	# this apply for several raspberry models
	port = '/dev/serial0'
	serialport = serial.Serial()
	serialport.port = "/dev/serial0"
	serialport.baudrate = 57600
	serialport.parity = serial.PARITY_NONE
	serialport.stopbits = serial.STOPBITS_ONE
	serialport.bytesize = serial.EIGHTBITS
	serialport.timeout = 0.01
	# it can be called like this:
	# serialport = serial.serial('/dev/ttyS0', 115200)
	try:
		# Open a Moacon Serial port
		serialport.open()
		print "serial port opened"
		return True
	except Exception as e:
		print "The serial port named: " + port + " couldn't open, Error: " + str(e)
		return False
		serialport.close()

# =================================================================================
def CloseSerialfor_ModPort():
	global serialport
	serialport.close()

# =================================================================================
def checking_CRC_sum(data_str):
	l = len(data_str)
	check_crc = ord(data_str[1])
	for n in range(2, l-1):		# l-1: with this the sum must be zero.
		check_crc = check_crc ^ ord(data_str[n])

	if check_crc == 0xa:
		if debug: print "CRC checking 0xA"
		check_crc = check_crc ^ 0xa
	return check_crc

# =================================================================================
def reverse_bits(Original_byte, numbits):
	# numbits = 8
	# Original_byte = 2
	return sum(1<<(numbits-1-bit) for bit in range(numbits) if ord(Original_byte)>>bit&1)
	# The above code is the same of this bellow	
	# suma = 0
	# for bit in range(numbits):
	# 	if Original_byte>>bit&1:
	# 		suma += 1<<(numbits-1-bit)

"""
=========================================================================================================================
=			READ FUNCTION OF MODPORT Module_Number OF 4 ANALOG INPUTS MD-ADIN4 - SPEED COMMUNICATION: 57.600 BAUD				=
=	Buy this Module_Number in: http://www.comfiletech.com/etc/field-i-o/modport-i-o-Module_Number/									=
=	New version: V1.00	Release Date:	2017-03-10																		=
=========================================================================================================================
"""
def MD_ADIN4(Module_Number, debug=False):
	"""
	Each Module_Number has 8 channels, each with its own unique Modbus address. The following table details each
	Module_Number’s channel, and the channel’s starting address. All values are given in base 10.
	|-----------------------------------------------------|
	|  CHANNEL			|	 1	 |	 2	 |	 3	 |	 4	  |
	|-----------------------------------------------------|
	|  STARTING ADDRESS |	100	 |	101	 |	102	 |	103   |
	|-----------------------------------------------------|
	"""
	MD_Address = 100
	MD_lenght = 4
	numChannels = 4

	if not Module_Number in range(1,16):
		raise IOError('Wrong Number. The number of Module_Numbers MD-ADIN4 to read is from 1 to 15')

	return FncCode_3_Read_Input_register(Module_Number, MD_Address, MD_lenght, numChannels, debug)

"""
=========================================================================================================================
=			READ FUNCTION OF MODPORT Module_Number OF 4 ANALOG INPUTS MD-HADIN4 - SPEED COMMUNICATION: 57.600 BAUD				=
=	Buy this Module_Number in: http://www.comfiletech.com/etc/field-i-o/modport-i-o-Module_Number/									=
=	New version: V1.00	Release Date:	2017-03-10																		=
=========================================================================================================================
"""
def MD_HADIN4(Module_Number, debug=False):
	"""
	Each Module_Number has 8 channels, each with its own unique Modbus address. The following table details each
	Module_Number’s channel, and the channel’s starting address. All values are given in base 10.
	Negative numbers read from this Module_Number will be expressed in 2’s complement. Because each value is 32 bits, 
	2 words (16 bits each) must be read to receive the full 32 bits.
	|-----------------------------------------------------------|
	|  CHANNEL			|    1    |    2    |    3    |    4    |
	|-----------------------------------------------------------|
	|  STARTING ADDRESS | 200,201 | 202,203 | 204,205 | 206,207 |
	|-----------------------------------------------------------|
	Note: This function is just teorically and it has no tested yet.
	"""
	MD_Address = 200
	MD_lenght = 8
	numChannels = 4

	if not Module_Number in range(1,16):
		raise IOError('Wrong Number. The number of Module_Numbers MD-HADIN4 to read is from 1 to 15')

	return FncCode_3_Read_Input_register(Module_Number, MD_Address, MD_lenght, numChannels, debug)
"""
=========================================================================================================================
=			READ FUCNTION OF CODE 3 FOR READ HOLDING / INPUT REGISTERS													=
=	New version: V1.00	Release Date:	2017-03-10																		=
=========================================================================================================================
"""
def FncCode_3_Read_Input_register( Module_Number, MD_Address, MD_lenght, numChannels, debug=False):
	"""
	These two functions read one or more word (16 bits) values starting at a given address.
	The register address is the address of the first register to read. Length is the number of bytes to read.
	"""
	Function_Code = 3

	MD_request_data_pack (Module_Number, Function_Code, MD_Address, MD_lenght, debug)

	read_data = ""
	read_data = serialport.read(30)	# Read the data arrived from moacon Module_Numbers

	lenght_readData = len(read_data)

	# Checking if there is data en read_data
	if lenght_readData > 12:
		len_recv = ord(read_data[2])	# This is the lenght arrived in the frame from Module_Number readed
		calc_crc = _calculateCrcString(read_data[0:3+len_recv])
		if calc_crc == read_data[3+len_recv:5+len_recv] and chr(Module_Number) == read_data[0] and chr(Function_Code) == read_data[1]:
			if debug: print "CRC ===== OK == OK == OK ====="
			if len_recv == 8:
				k = 3
				RawData = []
				for n in range(0, numChannels):
					data = ( ord(read_data[k]) * 256 ) + ord(read_data[k+1])
					if data == 11111:
						data = -1
					elif data == 55555:
						data = -2
					elif data > 11000:
						data = 0
					RawData.insert(n, data)
					# print "Dato " + str(n+1) + ": " + str(RawData[n])		# Print example
					k += 2
				return RawData

			elif len_recv == 16:
				k = 3
				RawData = []
				for n in range(0, numChannels):
					data = (ord(read_data[k]) * 256)  + ord(read_data[k+1])
					data = (data * 256) + ord(read_data[k+2])
					data = (data * 256) + ord(read_data[k+3])	

					if data == 111111:
						data = -1
					elif data == 555555:
						data = -2
					elif data > 111000:
						data = 0
					RawData.insert(n, data)
					# print "Dato " + str(n+1) + ": " + str(RawData[n])		# Print example
					k += 4
				return RawData
		else:	# If the CRC arrived is corrupted
			if debug: print "Error data received (CRC corrupted)"
			RawData = []
			for n in range(0, numChannels):
				RawData.insert(n, -3)
			return RawData
	else:	# if there is no data in read_data fill the array with -4 to show an error.
		RawData = []
		for n in range(0, numChannels):
			RawData.insert(n, -4)
		return RawData
	
	""" 
	When data result in each channel is:
	-> -1: You have configured in 0 to 5V and the voltage maybe is an open circuit or BELOW than 0.8V.
	-> -2: You have configured in 0 to 5V and the voltage is ABOVE than 5.2V.
	-> -3: The CRC arrived in the data is corrupted. 
	-> -4: Module_Number is Disconnected. Please verify the connection.
	"""
"""
=========================================================================================================================
=			READ FUNCTION OF MODPORT Module_Number OF 8 DIGITAL INPUTS MD-DIDC8 - SPEED COMMUNICATION: 57.600 BAUD				=
=	Buy this Module_Number in: http://www.comfiletech.com/etc/field-i-o/modport-i-o-Module_Number/									=
=	New version: V1.00	Release Date:	2017-03-10																		=
=========================================================================================================================
"""
def MD_DIDC8(Module_Number, debug=False):
	"""
	8 DIGITAL INPUTS FROM 12 TO 24 VDC.
	|---------------------------------------------------|
	|  CHANNEL			| 0	| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
	|---------------------------------------------------|
	|  STARTING ADDRESS | 0	| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
	|---------------------------------------------------|
	"""
	MD_Address = 0
	MD_lenght = 8

	if not Module_Number in range(1,16):
		raise IOError('Wrong Number. The number of Module_Numbers MD-DIDC8 to read is from 1 to 15')

	return FncCode_1_Read_coil_Input_Status(Module_Number, MD_Address, MD_lenght, debug)
"""
=========================================================================================================================
=		READ FUNCTION OF MODPORT Module_Number OF 8 POINTS SINK DC OUPUT MD-DOSI8 - SPEED COMMUNICATION: 57.600 BAUD			=
=	Buy this Module_Number in: http://www.comfiletech.com/etc/field-i-o/modport-i-o-Module_Number/									=
=	New version: V1.00	Release Date:	2017-03-10																		=
=========================================================================================================================
"""
def MD_DOSI8_Read_All(Module_Number, debug=False):
	"""
	8 POINTS DIGITAL SINK DC OUTPUT FROM 3.3V-27V 1A. This function is to get the Status of the outputs.
	|---------------------------------------------------------------------------|
	|  CHANNEL			|	0  |   1  |   2  |   3  |   4  |   5  |   6  |   7	|
	|---------------------------------------------------------------------------|
	|  STARTING ADDRESS | 3100 | 3101 | 3102 | 3103 | 3104 | 3105 | 3106 | 3107 |
	|---------------------------------------------------------------------------|
	"""
	MD_Address = 3100
	MD_lenght = 8

	if not Module_Number in range(1,16):
		raise IOError('Wrong Number. The number of Module_Numbers MD-DOSI8 to read is from 1 to 15')

	return FncCode_1_Read_coil_Input_Status(Module_Number, MD_Address, MD_lenght, debug)
"""
=========================================================================================================================
=			READ FUCNTION OF CODE 1 FOR READ COIL / INPUT STATUS														=
=	New version: V1.00	Release Date:	2017-03-10																		=
=========================================================================================================================
"""
def FncCode_1_Read_coil_Input_Status(Module_Number, MD_Address, MD_lenght, debug=False):
	"""
	These two functions read bit values starting at a given address.
	The start address is the address of the first bit to read. Length is the number of bits to read, however, the
	response will always be in multiples of 8 bits. For example, if length is 5, the response will contain 8 bits. If
	length is 14, the response will be 16 bits.
	"""
	Function_Code = 1

	# debug = False	# If you wanna to activate debug (print) for testing
	MD_request_data_pack (Module_Number, Function_Code, MD_Address, MD_lenght, debug)

	read_data = ""
	read_data = serialport.read(20)	# Read the data arrived from moacon Module_Numbers
	lenght_readData = len(read_data)

	if debug: print "Lenght: " + str(lenght_readData) + " -Received RAW Data: "
	for num in range(0,lenght_readData):
		if debug: print hex(ord(read_data[num])),
	if debug:
		print ""
		print "Read size: " + str(len(read_data))

	# Checking if there is data en read_data
	if lenght_readData > 5:
		calc_crc = _calculateCrcString(read_data[0:lenght_readData-2])
		if calc_crc == read_data[lenght_readData-2:lenght_readData] and chr(Module_Number) == read_data[0] and chr(Function_Code) == read_data[1]:
			if debug: print "CRC ===== OK == OK == OK ====="
			rev_byte = reverse_bits(read_data[3], 8)
			RawData = [int(i) for i in "{0:08b}".format(rev_byte)]
			if debug: print RawData
			return RawData
		else:	# If the CRC arrived is corrupted
			RawData = [-3 for i in "{0:08b}".format(ord(" "))]
			if debug: print RawData
			return RawData
	else:	# if there is no data in read_data fill the array with -4 to show an error.
		RawData = [-4 for i in "{0:08b}".format(ord(" "))]
		if debug: print RawData
		return RawData

	""" 
	When data result in each channel is:
	-> -3: The CRC arrived in the data is corrupted. 
	-> -4: Module_Number is Disconnected. Please verify the connection.
	"""
	

"""
=========================================================================================================================
=		WRITE FUNCTION OF MODPORT Module_Number OF 8 POINTS SINK DC OUPUT MD-DOSI8 - SPEED COMMUNICATION: 57.600 BAUD	=
=	Buy this Module_Number in: http://www.comfiletech.com/etc/field-i-o/modport-i-o-Module_Number/						=
=	New version: V1.00	Release Date:	2017-03-17																		=
=========================================================================================================================
"""
def MD_DOSI8_Write_One(Module_Number, channel, value, debug=False):
	"""
	8 POINTS DIGITAL SINK DC OUTPUT FROM 3.3V-27V 1A. WRITE FUNCTION
	|---------------------------------------------------------------------------|
	|  CHANNEL			|	0  |   1  |   2  |   3  |   4  |   5  |   6  |   7	|
	|---------------------------------------------------------------------------|
	|  STARTING ADDRESS | 3100 | 3101 | 3102 | 3103 | 3104 | 3105 | 3106 | 3107 |
	|---------------------------------------------------------------------------|
	"""
	MD_Address = 3100 + channel

	if not channel in range(0,8):
		raise IOError('Wrong Number. The number of Channel MD-DOSI8 to Write must be from 0 to 7')

	if not Module_Number in range(1,16):
		raise IOError('Wrong Number. The number of Module_Numbers MD-DOSI8 to Write must be from 1 to 15')

	if not value in range(0,2):
		raise IOError('Wrong Number. The number of Value MD-DOSI8 to Write must be from 0 or 1')

	return FncCode_5_Force_Single_Coil_Status(Module_Number, MD_Address, value, debug=False)
	
"""
=========================================================================================================================
=			WRITE OR FORCE SINGLE COIL / OUTPUT STATUS																	=
=	New version: V1.00	Release Date:	2017-03-17																		=
=========================================================================================================================
"""
def FncCode_5_Force_Single_Coil_Status(Module_Number, MD_Address, value, debug=False):
	"""
	This function sets the value of a single bit at a given address.
	Start address is the address of the bit to set, and data is the value to set the bit to. To turn a bit ON, data
	must be 0xFF00. To turn a bit OFF, data must b 0x0000.
	"""
	Function_Code = 5

	if value == 1:
		value = 65280	# This is that the packet function could send a "0xFF 0x00" data to set digital output to logic High.

	MD_Data = value
	# debug = False	# If you wanna to activate debug (print) for testing
	MD_request_data_pack (Module_Number, Function_Code, MD_Address, MD_Data, debug)

	read_data = ""
	read_data = serialport.read(20)	# Read the data arrived from moacon Module_Numbers
	lenght_readData = len(read_data)

	if debug: print "Lenght: " + str(lenght_readData) + " -Received RAW Data: "
	for num in range(0,lenght_readData):
		if debug: print hex(ord(read_data[num])),
	if debug:
		print ""
		print "Read size: " + str(len(read_data))
		# for data in read_data:
		# 	print hex(data)

	# Checking if there is data en read_data
	if lenght_readData > 7:
		calc_crc = _calculateCrcString(read_data[0:lenght_readData-2])
		if calc_crc == read_data[lenght_readData-2:lenght_readData] and chr(Module_Number) == read_data[0] and chr(Function_Code) == read_data[1]:
			if debug: print "CRC ===== OK == OK == OK ====="
			calc_value = (ord(read_data[4]) * 256) + ord(read_data[5])
			if  calc_value == value:
				# if the values are equal it means that the value was assigned satisfactory
				if value == 65280: value = 1
				return value
			else:	# if the value wasn't assinged correctly
				RawData = -1
				return RawData
		else:	# If the CRC arrived is corrupted
			RawData = -3
			return RawData
	else:	# if there is no data in read_data fill the variable with -4 to show an error.
		RawData = -4
		return RawData

	""" 
	When data result in each channel is:
	-> -1: if the value wasn't assinged correctly.
	-> -3: The CRC arrived in the data is corrupted. 
	-> -4: Module_Number is Disconnected. Please verify the connection.
	"""
"""
=========================================================================================================================
=		WRITE FUNCTION OF MODPORT Module_Number OF 8 POINTS SINK DC OUPUT MD-DOSI8 - SPEED COMMUNICATION: 57.600 BAUD	=
=	Buy this Module_Number in: http://www.comfiletech.com/etc/field-i-o/modport-i-o-Module_Number/						=
=	New version: V1.00	Release Date:	2017-03-17																		=
=========================================================================================================================
"""
def MD_DOSI8_Write_All(Module_Number, MD_Data, debug=False):
	"""
	8 POINTS DIGITAL SINK DC OUTPUT FROM 3.3V-27V 1A. WRITE FUNCTION
	|---------------------------------------------------------------------------|
	|  CHANNEL			|	0  |   1  |   2  |   3  |   4  |   5  |   6  |   7	|
	|---------------------------------------------------------------------------|
	|  STARTING ADDRESS | 3100 | 3101 | 3102 | 3103 | 3104 | 3105 | 3106 | 3107 |
	|---------------------------------------------------------------------------|
	"""
	MD_Address = 3100

	if not Module_Number in range(1,16):
		raise IOError('Wrong Number. The number of Module_Numbers MD-DOSI8 to Write must be from 1 to 15')

	return FncCode_15_Force_Multiple_Coil_Status(Module_Number, MD_Address, MD_Data, debug)
"""
=========================================================================================================================
=			WRITE OR FORCE MULTIPLE COIL / OUTPUT STATUS																=
=	New version: V1.00	Release Date:	2017-03-17																		=
=========================================================================================================================
"""
def FncCode_15_Force_Multiple_Coil_Status(Module_Number, MD_Address, MD_Data, debug=False):
	"""
	This function sets the value of multiple bits starting at a given address.
	Start address is the address of the first bit to set, and data is a bit array containing the value for each bit to
	set. Length is the number of bits to set, and byte count is size of the data in bytes.
	"""
	global serialport
	Function_Code = 15
	Byte_Count = 2
	MD_lenght = 8

	# data = struct.pack('>BBHHBH',Module_Number, Function_Code, MD_Address, MD_lenght, Byte_Count, MD_Data)
	data = struct.pack('>BBHHB',Module_Number, Function_Code, MD_Address, MD_lenght, Byte_Count) +  struct.pack('<H', MD_Data)
	crc = _calculateCrcString(data)
	tx_data = data + crc
	if debug: print "Transmit Data: ",
	if debug: print " ".join("{:02x}".format(ord(c)) for c in tx_data)
	serialport.write(tx_data)		# Send the request channels data to modport Module_Number

	read_data = ""
	read_data = serialport.read(20)	# Read the data arrived from moacon Module_Numbers
	lenght_readData = len(read_data)

	if debug: print "Lenght: " + str(lenght_readData) + " -Received RAW Data: "
	for num in range(0,lenght_readData):
		if debug: print hex(ord(read_data[num])),
	if debug:
		print ""
		print "Read size: " + str(len(read_data))
		# for data in read_data:
		# 	print hex(data)

	# Checking if there is data en read_data
	if lenght_readData > 7:
		calc_crc = _calculateCrcString(read_data[0:lenght_readData-2])
		if calc_crc == read_data[lenght_readData-2:lenght_readData] and chr(Module_Number) == read_data[0] and chr(Function_Code) == read_data[1]:
			if debug: print "CRC ===== OK == OK == OK ====="
			if  MD_lenght == ord(read_data[lenght_readData-3]):
				# if the values are equal it means that the value was assigned satisfactory and return a 1 to show it
				rev_byte = reverse_bits(chr(MD_Data), 8)
				RawData = [rev_byte >> i & 1 for i in range(7,-1,-1)]
				return RawData
			else:	# if the value wasn't assinged correctly
				RawData = []
				for n in range(0, numChannels):
					RawData.insert(n, -1)
				return RawData
		else:	# If the CRC arrived is corrupted
			RawData = []
			for n in range(0, numChannels):
				RawData.insert(n, -3)
			return RawData
	else:	# if there is no data in read_data fill the variable with -4 to show an error.
		RawData = []
		for n in range(0, numChannels):
			RawData.insert(n, -4)
		return RawData

	""" 
	When data result in each channel is:
	-> -1: if the value wasn't assinged correctly or lenght is not the same.
	-> -3: The CRC arrived in the data is corrupted. 
	-> -4: Module_Number is Disconnected. Please verify the connection.
	"""

"""
=========================================================================================================================
=			THIS IS A FUNCTION THAT ASSEMBLY THE DATA PACK AND SEND IT TO THE Module_Number									=
=	New version: V1.00	Release Date:	2017-03-09																		=
=========================================================================================================================
"""
def MD_request_data_pack (Module_Number, Function_Code, MD_Address, MD_lenght, debug=False):
	global serialport		# Getting global variable of serial port
	"""
	It takes a string output data from pack function
	fromat:
	>: means least significant byte should be first in the resulting string.
	B: Integer of 1 byte size
	H: Integer of 2 byte size
	https://docs.python.org/2/library/struct.html
	"""
	data = struct.pack('>BBHH',Module_Number, Function_Code, MD_Address, MD_lenght)

	crc = _calculateCrcString(data)
	tx_data = data + crc

	# if debug: print "0x" + " 0x".join("{:02x}".format(ord(c)) for c in tx_data)
	if debug: print "Transmit Data: ",
	if debug: print " ".join("{:02x}".format(ord(c)) for c in tx_data)

	serialport.write(tx_data)		# Send the request channels data to modport Module_Number