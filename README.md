====================================
MOACON MODULES LIBRARY
====================================
#### RS-ADIN4 AND RS-SADIN6 MODULES FROM CUBLOC.COM

IoT. You can read moacon modules (Modbus communication - cubloc.com) and mcp3208 - 8 channel 12Bit ADC from Rpi 3 and others.

This package include serveral modules:
Module moacon.py: This module contains the folling functions:

#### OpenSerialMoacon():

This function allows to open a serial port in raspberry pi 3 named 'Serial0'
and Baud Rate speed at 115200, to communicate well with the 
In Rpi 3 you have to disable bluetooth device and swippe the serial port. 
When you execute the following command and you have 'Serial0 -> ttyAMA0'::
				
				$ ls -l /dev/

#### CloseSerialMoacon(): 

This function close the serial connection oppened by OpenSerialMoacon().

#### RS_ADIN4(Module Number):

This function read the RS-ADIN4 moacon module from Cubloc.com.
- Module Number: The number of moacon module from 0 to 9 on the device. 
With a little modification in hardwrare you could read from 10 to 15.

#### RS_SADIN6(Module Number):

This function read the RS-SADIN6 moacon module from Cubloc.com.
- Module Number: The number of moacon module from 0 to 9 on the device. 
With a little modification in hardwrare you could read from 10 to 15.

When data result in each channel is:

- (-1): probably the channel is damaged.
- (-2): Probably the data received is incomplete.
- (-3): It tried to read 3 times and it couldn't get an answer from the module. 
- (-4): Module is Disconnected. Please verify the connection.


#### READING EXAMPLE CODE FOR RS_ADIN4. TESTING AND WORKING:

		import serial
		import time
		import IOT.moacon
		ModuleNumber = 1
		if __name__ == '__main__':
				if IOT.moacon.OpenSerialMoacon() is True:
						results = IOT.moacon.RS_ADIN4(ModuleNumber)
						# print results
						print "Module " + str(ModuleNumber)
						for res in range(0, 4):
								print "Channel " + str(res+1) + ": " + str(results[res])
				IOT.moacon.CloseSerialMoacon()

#### READING EXAMPLE CODE FOR RS_SADIN6. TESTING AND WORKING:

		import serial
		import time
		import IOT.moacon
		ModuleNumber = 7
		if __name__ == '__main__':
				if IOT.moacon.OpenSerialMoacon() is True:
						results = IOT.moacon.RS_SADIN6(ModuleNumber)
						# print results
						print "Module " + str(ModuleNumber)
						for res in range(0, 6):
								print "Channel " + str(res+1) + ": " + str(results[res])
				IOT.moacon.CloseSerialMoacon()
