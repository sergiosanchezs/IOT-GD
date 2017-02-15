import serial
import time
from IOT_GD import moacon
ModuleNumber = 7
if __name__ == '__main__':
	if moacon.OpenSerialMoacon() is True:
		results = moacon.RS_SADIN6(ModuleNumber)
		# print results
		print "Module " + str(ModuleNumber)
		for res in range(0, 6):
			print "Channel " + str(res+1) + ": " + str(results[res])
	moacon.CloseSerialMoacon()