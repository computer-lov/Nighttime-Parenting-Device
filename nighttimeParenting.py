import time
import sys
import os
import smbus
import spidev
import pygame as pg
import RPi.GPIO as GPIO
import InfraLibraries.max30102 as MAX30102
import InfraLibraries.hrcalc as hrcalc
import math
import datetime
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


################### MICROPHONE SOUND LEVEL CIRCUIT SECTION ################### 

# Author: Developed and maintained by Andrew P. Mayer
# Creation Date: 2/15/2022
# Last Updated: 4/12/2022
# License: MIT License 2022
# Further Description:
#   Stub function section for the CMEJ-9745-37-P Electric Condensor Microphone
#   This section was written in VS Code and tested on a Raspberry Pi Zero

class micCircuit:

    # initializes micCircuit class
    def __init__(self):
        self.channel = 0 # adc channel 0

        self.spi = spidev.SpiDev()
        self.spi.open(0, 1)
        self.mode = 0b00
        self.spi.max_speed_hz = 1350000

    # reads in digital value and returns it
    def getDigitalVal(self):
        # Read from CH0
        readBytes = self.spi.xfer2([1, (8+self.channel)<<4, 0])
      
        # obtain digital value
        dVal = (((readBytes[1] & 3) << 8) + readBytes[2])
        return dVal

    # converts digital value to analog value
    # will convert current digitalvalue by default
    # else it will convert whatever is passed into dVal
    def getAnalogVal(self, dVal = None):
        if (dVal == None):
            dVal = self.getDigitalVal()
        aVal = (dVal/1024)*3.3
        return aVal

    # gets local maximum in single step interval
    def getAmplitude(self, step):
        start = time.time()
        localMax = 0
        localMin = 1024
        # get local max and min in step interval
        while ((time.time() - start) <= step):
            currVal = self.getDigitalVal()
            localMax = max(currVal, localMax)
            localMin = min(currVal, localMin)

        # calculate peakTopeak amplitude
        peakToPeak = localMax - localMin
        return peakToPeak

    # calculate and returns peak-to-peak average value over a given time interval
    # step value is set to 100ms by default
    def getPkPkAvg(self, timeInterval, step = 0.1):
        start = time.time()
        # sums up digital value
        sum = 0
        # count number of times something is added to sum
        count = 0
        while ((time.time() - start) <= timeInterval):
            curr = self.getAmplitude(step)
            if (curr > 0):
                sum += curr
                count += 1
        
        if (count > 0):
            return sum / count
        else:
            return 0
        
    # returns true if avg digital value is greater than threshold false otherwise
    def trigger(self, thresholdVal, timeInterval):
        dVal = self.getPkPkAvg(timeInterval)
        res = True if (dVal  >= thresholdVal) else False
        return res

    # closes spi
    def close(self):
        self.spi.close()

        
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
            
            # -1 means play on infinite loop, there's one mp3 file of three combined songs
            self.mixer.music.play(-1)

    # pauses any playing audio
    def pause(self):
        #if self.mixer.music.get_busy():
        self.mixer.music.pause()
            
    # unpauses any paused audio
    def unpause(self):
        self.mixer.music.unpause()
        
    # returns volume as a float between 0.0 and 1.0
    def getVol(self):
        return self.mixer.music.get_volume()
    
    # volume should be a float between 0.0 and 1.0
    def setVol(self, volume):
        if volume <= 1.0 and volume >= 0.0:
            self.mixer.music.set_volume(volume)

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
        
################### OLED DISPLAY SECTION ################### 

# Author: Developed and maintained by Aron Goldberg
# Creation Date: 4/6/2022
# Last Updated: 4/6/2022
# License: MIT License 2022
# Further Description:
#  Uses PIL library and i2c

class OLED:

    OLED_WIDTH = 128
    OLED_HEIGHT = 64
    OLED_ADDRESS = 0x3c
    OLED_REGADDR = 0x00
    OLED_DISPOFF = 0xAE
    OLED_DISPON  = 0xAF


    

    # initializes i2c communication parameters for OLED
    def __init__(self):
        # Initialize I2C library busio
        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(OLED.OLED_WIDTH, OLED.OLED_HEIGHT,
            i2c, addr=OLED.OLED_ADDRESS)
        

    def printMessage(self, text):
        # Graphics stuff - create a canvas to draw/write on
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Draw a rectangle with no fill, ten pixels thick
        draw.rectangle((0, 0, self.oled.width-1, self.oled.height-1),
            outline=10, fill=0)

        # Draw some text
        (font_width, font_height) = font.getsize(text)
        if len(text) < 21:
            draw.text( # position text in center
                (self.oled.width // 2 - font_width // 2, self.oled.height // 2 - font_height // 2),
                text,
                font=font,
                fill=255,
            )
        elif len(text) < 41:
            line1 = text[:20]
            line2 = text[20:]
            draw.text( # position text starting at middle left
                (3, 18),
                line1 + "\n" + line2,
                font=font,
                fill=255,
            )
        elif len(text) < 61:
            line1 = text[:20]
            line2 = text[20:40]
            line3 = text[40:]
            draw.text( # position text starting at upper middle left
                (3, 10),
                line1 + "\n" + line2 + "\n" + line3,
                font=font,
                fill=255,
            )
        elif len(text) < 81:
            line1 = text[:20]
            line2 = text[20:40]
            line3 = text[40:60]
            line4 = text[60:]
            draw.text( # # position text starting at upper left corner
                (3, 1),
                line1 + "\n" + line2 + "\n" + line3 + "\n" + line4,
                font=font,
                fill=255,
            )
        else:
            draw.text( # position text in center
                (5, 18),
                "Message too long - \n80 character limit",
                font=font,
                fill=255,
            )

        # Display image
        self.oled.image(image)
        self.oled.show()

    def turnDisplayOff(self):
        self.oled.write_cmd(OLED.OLED_DISPOFF)

    def turnDisplayOn(self):
        self.oled.write_cmd(OLED.OLED_DISPON)
    
    def clearDisplay(self):
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)

        # Draw a rectangle with no fill, ten pixels thick
        draw.rectangle((0, 0, self.oled.width, self.oled.height),
            outline=0, fill=0)
        
        self.oled.image(image)
        self.oled.show()
        
        # helper function for displayTime
    def posn(self, angle, arm_length):
        dx = int(math.cos(math.radians(angle)) * arm_length)
        dy = int(math.sin(math.radians(angle)) * arm_length)
        return (dx, dy)
      
        
    # displays analog and digital time
    def displayTime(self):
        today_last_time = "Unknown"
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        once = True
        while once:
            now = datetime.datetime.now()
            today_date = now.strftime("%d %b %y")
            today_time = now.strftime("%I:%M:%S")
            if today_time != today_last_time:
                today_last_time = today_time
                #with canvas(device) as draw:
                now = datetime.datetime.now()
                today_date = now.strftime("%d %b %y")

                margin = 4

                cx = 30
                cy = min(self.oled.height, 64) / 2

                left = cx - cy
                right = cx + cy
                """
                hrs_angle = 270 + (30 * (now.hour + (now.minute / 60.0)))
                hrs = self.posn(hrs_angle, cy - margin - 7)

                min_angle = 270 + (6 * now.minute)
                mins = self.posn(min_angle, cy - margin - 2)

                sec_angle = 270 + (6 * now.second)
                secs = self.posn(sec_angle, cy - margin - 2)

                draw.ellipse((left + margin, margin, right - margin, min(self.oled.height, 64) - margin), outline=255) #"white")
                draw.line((cx, cy, cx + hrs[0], cy + hrs[1]), fill=255)#"white")
                draw.line((cx, cy, cx + mins[0], cy + mins[1]), fill=255)#"white")
                draw.line((cx, cy, cx + secs[0], cy + secs[1]), fill=140)#"red")
                draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=255, outline=255)#"white", outline="white")
                """
                draw.text((self.oled.width // 2 - font_width // 2, (self.oled.height // 2 - font_height // 2 - 8)), today_date, font = font, fill=190)#"yellow")
                draw.text((self.oled.width // 2 - font_width // 2, self.oled.height // 2 - font_height // 2), today_time, font = font, fill=190)#"yellow")
                self.oled.image(image)
                self.oled.show()

            time.sleep(0.1)
            once = False
        return today_time

        
    
################### HEART RATE SENSOR SECTION ################### 

# Author: Developed and maintained by Beatriz Perez and Andrew P. Mayer
# Creation Date: 2/20/2022
# Last Updated: 4/5/2022
# License: MIT License 2022
# Further Description:
#   Stub function section for Heart Rate Sensor with MAX30102 chip
#   This section was written in VS Code and tested on a Raspberry Pi Zero

class HRSensor:

    # initializes Heart Rate Sensor sensor
    def __init__(self):
        # initialize heart rate monitor class
        self.sensor = MAX30102.MAX30102()

    # collects bpm and spo2 data from heart rate sensor
    def getAllData(self):
        ir_data = []
        red_data = []
        dataCap = 100
        dataCount = 0
    
        # grab all the data and stash it into arrays
        # loop until data is found
        while dataCount <= dataCap:
            # check if any data is available
            num_bytes = self.sensor.get_data_present()

            while num_bytes > 0:
                red, ir = self.sensor.read_fifo()
                num_bytes -= 1
                dataCount += 1
                ir_data.append(ir)
                red_data.append(red)

        # calculate hr and spo2
        bpm, valid_bpm, spo2, valid_spo2 = hrcalc.calc_hr_and_spo2(ir_data, red_data)

        # validate data
        if valid_bpm and valid_spo2:
            # case if finger not detected
            if (sum(ir_data)/len(ir_data) < 50000 and sum(red_data)/len(red_data) < 50000):
                self.bpm = 0
                print("Finger not detected")
            return bpm, spo2
        else:
            return (None, None)

    # reads heart rate and oxygen saturation level from sensor and returns them
    def getHR_SPO2(self):
        print("Place finger on HR monitor")
        HR_SPO2 = (None, None)

        # wait for valid data
        while HR_SPO2[0] == None and HR_SPO2[1] == None:
            HR_SPO2 = self.getAllData()
        
        return (HR_SPO2[0], HR_SPO2[1])

################### LED BAR GUIDED BREATHING SECTION ################### 

# Author: Developed and maintained by Beatriz Perez and Andrew P. Mayer
# Creation Date: 3/05/2022
# Last Updated: 4/19/2022
# License: MIT License 2022
# Further Description:
#   This section was written in VS Code and tested on a Raspberry Pi Zero

class ledBar:

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.mode = 0b00
        self.spi.max_speed_hz = 7629
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)
        self.dt = 0.5  # Time delay between LED breaths

    def breathe_in(self):
        self.spi.xfer([0b00000000])
        GPIO.output(5, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        time.sleep(2)
        self.spi.xfer([0b10000000])
        time.sleep(self.dt)
        self.spi.xfer([0b11000000])
        time.sleep(self.dt)
        self.spi.xfer([0b11100000])
        time.sleep(self.dt)
        self.spi.xfer([0b11110000])
        time.sleep(self.dt)
        self.spi.xfer([0b11111000])
        time.sleep(self.dt)
        self.spi.xfer([0b11111100])
        time.sleep(self.dt)
        self.spi.xfer([0b11111110])
        time.sleep(self.dt)
        self.spi.xfer([0b11111111])
        time.sleep(self.dt)
        GPIO.output(27, GPIO.HIGH)
        time.sleep(self.dt)
        GPIO.output(5, GPIO.HIGH)

    def breathe_out(self):
        time.sleep(2)
        GPIO.output(5, GPIO.LOW)
        time.sleep(self.dt)
        GPIO.output(27, GPIO.LOW)
        time.sleep(self.dt)
        self.spi.xfer([0b11111111])
        time.sleep(self.dt)
        self.spi.xfer([0b11111110])
        time.sleep(self.dt)
        self.spi.xfer([0b11111100])
        time.sleep(self.dt)
        self.spi.xfer([0b11111000])
        time.sleep(self.dt)
        self.spi.xfer([0b11110000])
        time.sleep(self.dt)
        self.spi.xfer([0b11100000])
        time.sleep(self.dt)
        self.spi.xfer([0b11000000])
        time.sleep(self.dt)
        self.spi.xfer([0b10000000])
        time.sleep(self.dt)
        self.spi.xfer([0b00000000])
        time.sleep(self.dt)
    
    # turns off led bar
    def turnOffLBar(self):
        GPIO.setup(5, GPIO.IN)
        GPIO.output(27, GPIO.IN)

    # turns on led bar
    def turnOnLBar(self):
        GPIO.setup(5, GPIO.OUT)
        GPIO.output(27, GPIO.OUT)

############################## Physical UI ###############################

# Author: Developed and maintained by Andrew P. Mayer
# Creation Date: 4/6/2022
# Last Updated: 4/19/2022
# License: MIT License 2022
# Further Description:
#  a class to implement the physical user interface methods

# TODO:
# should we initialize all of the spi stuff in this class
# needs to be test (not sure if all devices that use spi will conflict with each other)

class PhysicalUI:

    def __init__(self, sd, oled, lbar):

        # inherit Stereo decoder class and OLED
        self.sd = sd
        self.oled = oled
        self.lbar = lbar

        # set up adc channel 1 and 2
        self.channel1 = 1
        self.channel2 = 2

        self.spi = spidev.SpiDev()
        self.spi.open(0, 1)
        self.spi.mode = 0b00
        self.spi.max_speed_hz = 1350000

        # get current volume
        # Read from CH1
        readBytes = self.spi.xfer2([1, (8+self.channel1)<<4, 0])
        # obtain digital value
        self.currVol = (((readBytes[1] & 3) << 8) + readBytes[2])

        # set up GPIO
        GPIO.setmode(GPIO.BCM)
        self.pin = 17 # gpio 17
        GPIO.setup(self.pin, GPIO.IN)

    # changes stereo decoder volume
    def toggleVolume(self):
        # save prev volume
        prevVol = self.currVol
        # Read from CH1
        readBytes = self.spi.xfer2([1, (8+self.channel1)<<4, 0])
        # obtain digital value
        self.currVol = (((readBytes[1] & 3) << 8) + readBytes[2])
        # map volume to value between 0 and 1
        self.currVol = (self.currVol/1023)*1

        # set volume
        self.sd.setVol(self.currVol)
        
    # turns oled screen on/off
    def toggleBrightness(self):
        # get current brightness
        # Read from CH2
        readBytes = self.spi.xfer2([1, (8+self.channel2)<<4, 0])
        # obtain digital value
        currBrightness = (((readBytes[1] & 3) << 8) + readBytes[2])

        # toggle brightness by difference
        if (currBrightness < 255):
            self.oled.turnDisplayOff()
            self.lbar.turnOffLBar()
        
        elif (currBrightness > 755):
            self.oled.turnDisplayOn()
            self.lbar.turnOnLBar()

    # trigger SOS button
    def triggerSOS(self):
        if GPIO.input(self.pin):
            return True




