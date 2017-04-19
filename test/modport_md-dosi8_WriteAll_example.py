import serial
import time
from IOT_GD import modport
ModuleNumber = 10
if __name__ == '__main__':
	if modport.OpenSerialfor_ModPort() is True:
		Data_bits = b'10101010'		# Binary number that you want on the outputs
		Data_to_be = sum(int(c) * (2 ** i) for i, c in enumerate(Data_bits[::-1]))	# converting to integer before passing to the function
		modport.MD_DOSI8_Write_All(Module_Number, Data_to_be)
		print "##############################################################"
	modport.CloseSerialfor_ModPort()