import serial
import time
from IOT_GD import modport
ModuleNumber = 10
form = '{:5}'
if __name__ == '__main__':
		if modport.OpenSerialfor_ModPort() is True:
				results = modport.MD_ADIN4(Module_Number)
				print "MD-ADIN4, Module_Number " + str(Module_Number) + ": "
				for res in range(0, 4):
					data = form.format(results[res])
					print "Channel " + str(res+1) + ": " + data + "  ",
				print ""
		modport.CloseSerialfor_ModPort()