import spidev

################### MICROPHONE SOUND LEVEL CIRCUIT SECTION ################### 

# Author: Developed and maintained by Andrew P. Mayer
# Creation Date: 2/15/2022
# Last Updated: 2/15/2022
# License: MIT License 2022
# Further Description:
#   Stub function section for the CMEJ-9745-37-P Electric Condensor Microphone
#   This section was written in VS Code and tested on a Raspberry Pi Zero

class micCircuit: 

    # initializes micCircuit class
    def __init__(self):
        # these numbers may need to be changed
        self.ADC_CH0 = 0b01101000

        self.spi = spidev.SpiDev()
        self.spi.open(0, 1)
        self.spi.mode = 0b00
        self.spi.max_speed_hz = 1200000

    # reads in digital value and returns it
    def getDigitalVal(self):
        # Read from CH0
        readBytes = self.spi.xfer2([self.ADC_CH0, 0x00])
        # obtain digital value
        dVal = (((readBytes[0] & 0b11) << 8) | readBytes[1])
        return dVal

    # converts digital value to analog value
    def getAnalogVal(self):
        # get digital value
        dVal = self.getDigitalVal()
        aVal = (dVal/1024)*3.3
        return aVal
        
    # returns true if curr analog value is greater than threshold false otherwise
    def trigger(self, thresholdVal):
        res = True if (self.getAnalogVal() > thresholdVal) else False
        return res
        
################### AUDIO OUTPUT/STEREO DECODER SECTION ################### 

# Author: Developed and maintained by Aron Goldberg
# Creation Date: 2/15/2022
# Last Updated: 2/15/2022
# License: MIT License 2022
# Further Description:
#   Stub function section for the Adafruit I2S Stereo Decoder - UDA1334A
#   This section was written in VS Code and tested on a Raspberry Pi Zero


# TODO:
#       write stub functions and classes

class StereoDecoder:

    # initializes StereoDecoder class
    def __init__(self):
        pass

    # plays audio
    def play():
        pass

    # pauses audio
    def pause():
        pass

    # increments volume
    def increaseVol():
        pass

    # decrements volume
    def decreaseVol():
        pass



