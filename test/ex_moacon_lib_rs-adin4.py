import serial
import time
from IOT_GD import moacon
ModuleNumber = 1
if __name__ == '__main__':
	if moacon.OpenSerialfor_Moacon() is True:
		results = moacon.RS_ADIN4(ModuleNumber)
		# print results
		print "Module " + str(ModuleNumber)
		for res in range(0, 4):
			print "Channel " + str(res+1) + ": " + str(results[res])
	moacon.CloseSerialfor_Moacon()