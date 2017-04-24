import serial
import time
from IOT_GD import modport
Module_Number = 10
form = '{:5}'
if __name__ == '__main__':
	if modport.OpenSerialfor_ModPort() is True:
		print "--------------------------------------------------------------"
		results = modport.MD_DOSI8_Read_All(Module_Number)
		print "MD-DOSI8, Module Number " + str(Module_Number) + ": "
		for res in range(0, 8):
			data = form.format(results[res])
			print "Ch" + str(res) + ": " + data + " ",
		print ""
	modport.CloseSerialfor_ModPort()