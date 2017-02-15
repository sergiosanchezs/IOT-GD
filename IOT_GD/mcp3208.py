import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def readadc(adcnum):

        # change these as desired - they're the pins connected from the SPI port on the ADC to the RPi
        clockpin  = 11
        misopin = 9
        mosipin = 10
        cspin   = 8 # 8 cuando es CS0  7 cuando es CS1 --Permite conectar dos dispositivos via SPI (16 adin)

        # set up the SPI interface pins

        GPIO.setup(mosipin, GPIO.OUT)
        GPIO.setup(misopin, GPIO.IN )
        GPIO.setup(clockpin,  GPIO.OUT)
        GPIO.setup(cspin,   GPIO.OUT)

        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin   , True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin   , False)  # bring CS low

        commandout = adcnum
        commandout |= 0x18            # start bit + single-ended bit
        commandout <<= 3              # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True )
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True )
                GPIO.output(clockpin, False)

        adcout = 0

        # read in one empty bit, one null bit and 12 ADC bits
        # pro desetibitovy prevodnik tu bylo puvodne cislo 12
        for i in range(14):
                GPIO.output(clockpin, True )
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1 # first bit is 'null' so drop it
        return adcout
