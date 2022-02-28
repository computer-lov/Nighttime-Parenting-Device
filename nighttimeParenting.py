import spidev
import time
import smbus
import sys
import pygame as pg
import os
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
#   This uses the pygame library, documentation found here https://github.com/pygame/pygame and 
#   here https://web.archive.org/web/20211006193848/http://www.pygame.org/docs/ref/mixer.html
#   Sample code found here https://learn.adafruit.com/adafruit-i2s-stereo-decoder-uda1334a/audio-with-pygame#run-demo-2693434-7


class StereoDecoder:

    # initializes StereoDecoder class
    def __init__(self):
        freq=44100
        bitsize=-16
        channels=2
        buffer=2048
        self.mixer = pg.mixer
        self.mixer.init(freq, bitsize, channels, buffer)
        # default starting volume will be 20%
        self.mixer.music.set_volume(0.2)

    # queues up and starts audio
    def play(self):
        mp3s = []
        for file in os.listdir("."):
            if file.endswith(".mp3"):
                mp3s.append(file)
                
        for x in mp3s:
            try:
                self.mixer.music.load(x)
            except pygame.error:
                print("File {} not found! {}".format(music_file, pg.get_error()))
                return
            
            self.mixer.music.play()
            # check if playback is finished
            while self.mixer.music.get_busy():
                clock.tick(30)
            # small pause between songs
            time.sleep(0.25)

    # pauses any playing audio
    def pause(self):
        if self.mixer.music.get_busy():
            self.mixer.pause()
            
    # unpauses any paused audio
    def unpause(self):
        self.mixer.unpause()

    # increments volume, volume is a float between 0.0 and 1.0
    def increaseVol(self):
        if self.mixer.music.get_volume() <= 0.9:
        self.mixer.music.set_volume(self.mixer.music.get_volume() + 0.1)

    # decrements volume, volume is a float between 0.0 and 1.0
    def decreaseVol(self):
        if self.mixer.music.get_volume() >= 0.1:
        self.mixer.music.set_volume(self.mixer.music.get_volume() - 0.1)
        
    # stops all audio
    def stop(self):
        self.mixer.stop()
    
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
        self.HR_ADDR = 0x57
        self.WRITE_ADDR = 0xAE
        self.READ_ADDR = 0xAF
        
        self.i2c = smbus.SMBus(1)
        self.bpm = 0
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
        # temperature read in integer and fraction, both added
        # to find total temp
        
        # Enabling the temperature reading
        i2c.write_byte_data(HR_ADDR, 0x21, 1) # TEMP_EN
        i2c.write_byte_data(HR_ADDR, 0x03, 1) #DIE_TEMP_RDY_EN
        
        # Address for temp int = 0x1F
        T_int = i2c.read_byte_data(HR_ADDR, 0x1F)
        # Address for temp frac = 0x20
        T_frac = i2c.read_byte_data(HR_ADDR, 0x20)
        
        temp = T_int + T_frac
        return temp
        
        

        



