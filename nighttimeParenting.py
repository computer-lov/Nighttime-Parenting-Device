import spidev
import time

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
    # will convert current digitalvalue by default
    # else it will convert whatever is passed into dVal
    def getAnalogVal(self, dVal = None):
        if (dVal == None):
            dVal = self.getDigitalVal()
        aVal = (dVal/1024)*3.3
        return aVal

    # calculate and returns peak-to-peak average value over a given time interval
    # step value is set to 100ms by default
    def getPkPkAvg(self, timeInterval, step = 0.1):
        start = time.time()
        # sums up digital value
        sum = 0
        # count number of times something is added to sum
        count = 0
        while ((time.time() - start) <= timeInterval):
            sum += abs(self.getDigitalVal()-512)
            count += 512
            time.sleep(step)
        
        avg = (sum / count)*1024*3
        return avg

        
    # returns true if curr analog value is greater than threshold false otherwise
    def trigger(self, thresholdVal, timeInterval):
        aVal = self.getAnalogVal(self.getPkPkAvg(thresholdVal, timeInterval))
        res = True if (aVal  > thresholdVal) else False
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
    def play(self):
        pass

    # pauses audio
    def pause(self):
        pass

    # increments volume
    def increaseVol(self):
        pass

    # decrements volume
    def decreaseVol(self):
        pass

    
################### HEART RATE SENSOR SECTION ################### 

# Author: Developed and maintained by Beatriz Perez
# Creation Date: 2/20/2022
# Last Updated: 2/20/2022
# License: MIT License 2022
# Further Description:
#   Stub function section for Heart Rate Sensor with MAX30102 chip
#   This section was written in VS Code and tested on a Raspberry Pi Zero


class HRSensor:

    # initializes Heart Rate Sensor Class
    def __init__(self):
        # initialize i2c here
        pass

    # reads heart rate from sensor and returns BPM
    def getHR(self):
        BPM = None;
        return BPM

    # reads oxygen saturation level and returns value
    def getSPO2(self):
        SPO2 = None;
        return SPO2
        

    # reads temperature at sensor and returns value
    def getTemp(self):
        temp = None;
        return temp
        




