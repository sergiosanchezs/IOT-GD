import serial
import time
from IOT_GD import modport
Module_Number = 10
form = '{:5}'
if __name__ == '__main__':
	if modport.OpenSerialfor_ModPort() is True:
		Data_bits = b'10110010'		# Binary number that you want on the outputs
		Data_to_be = sum(int(c) * (2 ** i) for i, c in enumerate(Data_bits[::-1]))	# converting to integer before passing to the function
		print "Data: " + str(Data_to_be)
		results = modport.MD_DOSI8_Write_All(Module_Number, Data_to_be)
		for res in range(0, 8):
			data = form.format(results[res])
			print "Ch" + str(res) + ": " + data + " ",
		print ""
	modport.CloseSerialfor_ModPort()