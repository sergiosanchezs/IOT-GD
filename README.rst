IOT-GD
=====

MOACON MODULES LIBRARY
----------------------
**RS-ADIN4 AND RS-SADIN6 MODULES**

IoT. You can read moacon modules (Modbus communication - cubloc.com) and mcp3208 - 8 channel 12Bit ADC from Rpi 3 and others.

You can install this package by typing the following code in terminal in the rapsberry Pi:

.. code-block:: bash
    
  $ sudo pip install IOT_GD
  
This package include serveral modules:

**Module moacon.py:** This module contains the folling functions:

**OpenSerialfor_Moacon():**

This function allows to open a serial port in raspberry pi 3 named 'Serial0'
and Baud Rate speed at 115200, to communicate well with the 
In Rpi 3 you have to disable bluetooth device and swippe the serial port. 
When you execute the following command and you have 'Serial0 -> ttyAMA0':

.. code-block:: bash

  $ ls -l /dev/

**CloseSerialfor_Moacon():**

This function close the serial connection oppened by OpenSerialfor_Moacon().

**RS_ADIN4(Module Number):**

This function read the RS-ADIN4 moacon module from Cubloc.com.

- **Module Number:** The number of moacon module from 0 to 9 on the device. With a little modification in hardwrare you could read from 10 to 15.

**RS_SADIN6(Module Number):**

This function read the RS-SADIN6 moacon module from Cubloc.com.

- **Module Number:** The number of moacon module from 0 to 9 on the device. With a little modification in hardwrare you could read from 10 to 15.

When data result in each channel is:

- **(-1)**: probably the channel is damaged.
- **(-2)**: Probably the data received is incomplete.
- **(-3)**: It tried to read 3 times and it couldn't get an answer from the module. 
- **(-4)**: Module is Disconnected. Please verify the connection.

**READING EXAMPLE CODE FOR RS_ADIN4. TESTING AND WORKING:**

.. code-block:: python

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


**READING EXAMPLE CODE FOR RS_SADIN6. TESTING AND WORKING:**

.. code-block:: python

  import serial
  import time
  from IOT_GD import moacon
  ModuleNumber = 7
  if __name__ == '__main__':
      if moacon.OpenSerialfor_Moacon() is True:
          results = moacon.RS_SADIN6(ModuleNumber)
          # print results
          print "Module " + str(ModuleNumber)
          for res in range(0, 6):
              print "Channel " + str(res+1) + ": " + str(results[res])
      moacon.CloseSerialfor_Moacon()

MODPORT MODULES LIBRARY
=======================

**MD_ADIN4 - 4 Analog Inputs Module Hi Resolution**

The AD Input Modules' inputs are not isolated, so please be sure not to provide voltage or current
in excess of the specified ranges. Doing so could cause permanent damage.

The AD Input Modules can be wired to read voltage sources or current sources. When reading voltages
sources, the modules can be configured for a 0 ~ 10V range or a 1 ~ 5V range using the dipswitch on the
side of the module. When reading a current source (4-20mA), connect a 250 ohms resister across the input
terminals.

- Output Value: 0 to 10.000
- Resolution: 13.3 bits
- Precision: 0.1%
- Convesion Speed: 30 ms per channel

**How to use the function:**

.. code-block:: python

  MD_ADIN4(Module_Number)
  
**Module Number:** This is the number of the rotary switch on the face of each module to set its
Modbus slave address. It can be from 1 to 15, but directly on the rotary switch you can use 
from 1 to 10, if you wanna connect 5 more modules (from 11 to 15) you need to make a little simple 
soldering modification in hardware.

**READING EXAMPLE CODE FOR MD_ADIN4. TESTING AND WORKING:**

.. code-block:: python

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
      
**MD_HADIN4 - 4 Analog Inputs Module ULTRA Hi Resolution**

The AD Input Modules' inputs are not isolated, so please be sure not to provide voltage or current
in excess of the specified ranges. Doing so could cause permanent damage.

The AD Input Modules can be wired to read voltage sources or current sources. When reading voltages
sources, the modules can be configured for a 0 ~ 10V range or a 1 ~ 5V range using the dipswitch on the
side of the module. When reading a current source (4-20mA), connect a 250 ohms resister across the input
terminals.

- Output Value: 0 to 100.000
- Resolution: 16.6 bits
- Precision: 0.1%
- Convesion Speed: 240 ms per channel

**How to use the function:**

.. code-block:: python

  MD_HADIN4(Module_Number)
  
**Module Number:** This is the number of the rotary switch on the face of each module to set its
Modbus slave address. It can be from 1 to 15, but directly on the rotary switch you can use 
from 1 to 10, if you wanna connect 5 more modules (from 11 to 15) you need to make a little simple 
soldering modification in hardware.

**READING EXAMPLE CODE FOR MD_HADIN4. TESTING AND WORKING:**

.. code-block:: python

  import serial
  import time
  from IOT_GD import modport
  ModuleNumber = 10
  form = '{:6}'
  if __name__ == '__main__':
      if modport.OpenSerialfor_ModPort() is True:
          results = modport.MD_HADIN4(Module_Number)
          print "MD-HADIN4, Module_Number " + str(Module_Number) + ": "
          for res in range(0, 4):
            data = form.format(results[res])
            print "Channel " + str(res+1) + ": " + data + "  ",
          print ""
      modport.CloseSerialfor_ModPort()

**MD_DIDC8 - 8 pin 12-24VDC Digital Inputs**

This module can be read signals from 12 to 24 VDC depending on the ground referenced
in pins C1 and C2. C1 references the 4 first digital inputs, and C2 references the 4 last
digital inputs.

**How to use the function:**

.. code-block:: python

  MD_DIDC8(Module_Number)

**Module Number:** This is the number of the rotary switch on the face of each module to set its
Modbus slave address. It can be from 1 to 15, but directly on the rotary switch you can use 
from 1 to 10, if you wanna connect 5 more modules (from 11 to 15) you need to make a little simple 
soldering modification in hardware.

**READING EXAMPLE CODE FOR MD_DIDC8. TESTING AND WORKING:**

.. code-block:: python

  import serial
  import time
  from IOT_GD import modport
  ModuleNumber = 10
  if __name__ == '__main__':
      if modport.OpenSerialfor_ModPort() is True:
          print "--------------------------------------------------------------"
          results = modport.MD_DIDC8(Module_Number)
          print "MD-DIDC8, Module_Number " + str(Module_Number) + ": "
          for res in range(0, 8):
            data = form.format(results[res])
            print "Ch" + str(res) + ": " + data + " ",
          print ""
      modport.CloseSerialfor_ModPort()

**MD_DOSI8 - 8 pin Digital Sink Ouputs**

This module can be set the ground from signals from 3.3V to 27 VDC on 1 Ampere Maximum current rate.

**How to use the functions available in this module:**

.. code-block:: python

  MD_DOSI8_Write_One(Module_Number, channel, value)
  MD_DOSI8_Write_All(Module_Number, MD_Data)
  MD_DOSI8_Read_All(Module_Number)

**Module Number:** This is the number of the rotary switch on the face of each module to set its
Modbus slave address. It can be from 1 to 15, but directly on the rotary switch you can use 
from 1 to 10, if you wanna connect 5 more modules (from 11 to 15) you need to make a little simple 
soldering modification in hardware.

**channel:** This is the number of the fisical digital channel. This number need to be from 0 to 7.

**Value:** This is the value that you want to set the channel. Deactivated is 0 and Activated is 1.

**MD_Data:** This is the number in integer value that you want to give to all digital bits in the module.
The most significant bit is the channel 7.
The least significant bit is the channel 0.

**READING EXAMPLES CODES FOR MD_DOSI8. TESTING AND WORKING:**

**Using MD_DOSI8_Write_One function:**

.. code-block:: python

  import serial
  import time
  from IOT_GD import modport
  ModuleNumber = 10
  if __name__ == '__main__':
    if modport.OpenSerialfor_ModPort() is True:
        print "MD-DOSI8, Module Number: " + str(10), " "
        Value = 1 # Value to be assiged to the channel (0 - Logic Low, 1 - Logic High)
        for channel in range(0,8):
          bac = modport.MD_DOSI8_Write_One(ModuleNumber, channel, Value)
          print "Channel" + str(channel) + " Value: " + str(bac)
    modport.CloseSerialfor_ModPort()

**Using MD_DOSI8_Write_All function:**

.. code-block:: python

  import serial
  import time
  from IOT_GD import modport
  ModuleNumber = 10
  if __name__ == '__main__':
    if modport.OpenSerialfor_ModPort() is True:
      Data_bits = b'10101010'   # Binary number that you want on the outputs
      Data_to_be = sum(int(c) * (2 ** i) for i, c in enumerate(Data_bits[::-1]))  # converting to integer before passing to the function
      modport.MD_DOSI8_Write_All(Module_Number, Data_to_be)
      print "##############################################################"
    modport.CloseSerialfor_ModPort()

**Using MD_DOSI8_Read_All function:**

.. code-block:: python

  import serial
  import time
  from IOT_GD import modport
  ModuleNumber = 10
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

SPI MODULE LIBRARY
==================

**ADC with MCP3208**

This module let you use the chip ADC MCP3208 which have 8 analog channels to use in differents purposes. Per example, You can connect a LM35 sensor to measure and control the temperature in a close place to control. You can use a different many sensor  depending your application. You can measure the voltage, current, humidity and many things more. 

``Note: You need to add a voltage divider to measure voltages higher than the Vdd Vref``

This module use the SPI protocol to send to RPI all measured data.

The module use the function **_readadc(n)_**  where n is the ADC channel where the sensor is connected. You can use a cycle "for" from n=0 to n=7 if you have connected eight sensors to chip and you want take every measure of these at the same time.

.. code-block:: python

  import time
  from IOT_GD import mcp3208
  if __name__ == "__main__":
    while True:
      channels = []
      for n in range(0, 8):
        data = mcp3208.readadc(n)
        channels.insert(n, data)
      #print channels
      print "----------------------"
      for n in range(0, 8):
        print "channel " + str(n+1) + ": " + str(channels[n])
      print "",
      time.sleep(1)