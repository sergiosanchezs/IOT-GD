import serial
import time
from IOT_GD import moacon
ModuleNumber = 1
if __name__ == '__main__':

	while True:
		if moacon.OpenSerialfor_Moacon() is True:
			
			for ModuleNumber in range(1,3):
				results = moacon.RS_ADIN4(ModuleNumber)
				print "Module " + str(ModuleNumber) + ": "
				for res in range(0, 4):
					print "Channel " + str(res+1) + ": " + str(results[res])
				# time.sleep(.05)
			# Recolecting data from digital inputs
			time.sleep(1)

	moacon.CloseSerialfor_Moacon()