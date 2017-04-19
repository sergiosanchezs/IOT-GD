import serial
import time
from IOT_GD import modport
ModuleNumber = 10
if __name__ == '__main__':
	if modport.OpenSerialfor_ModPort() is True:
			print "MD-DOSI8, Module Number: " + str(10), " "
			Value = 1	# Value to be assiged to the channel (0 - Logic Low, 1 - Logic High)
			for channel in range(0,8):
				bac = modport.MD_DOSI8_Write_One(ModuleNumber, channel, Value)
				print "Channel" + str(channel) + " Value: " + str(bac)
	modport.CloseSerialfor_ModPort()