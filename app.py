import nighttimeParenting as infra
import time
from threading import Thread


# tasks that run in background

# updates oled screen
def updateOLED():
    messages = [] # need to add messages
    oled.clearDisplay()
    oled.displayTime()
    oled.clearDisplay()
    
    for mes in messages:
        oled.printMessage(mes)
        time.sleep(3)
        oled.clearDisplay()

# updates oled bar
def updateLedBar():
    lBar.breathe_in()
    lBar.breath_out()

def calculateStessLevel():
    pass

# tasks that run in response to something

def turnOFFScreen():
    pass

def playMusic():
    pass

def adjustVolume():
    pass

def notifyStessLevels():
    pass

def updateLog():
    pass

def cueBreathing():
    pass

def changeScreenView():
    pass

# tasks that run at start up 

def isAwake():
    pass

if __name__ == "__main__":
    m = infra.micCircuit()
    sd = infra.StereoDecoder()
    oled = infra.OLED()
    lBar = infra.ledBar()
    hrs = infra.HRSensor()
    phyUI = infra.PhysicalUI(sd, oled, lBar)

    t1 = Thread(target=updateOLED)
    t1.start()
    t2 = Thread(target=updateLedBar)
    t2.start()
    t3 = Thread(target=calculateStessLevel)
    t3.start()

    t1.join()
    t2.join()
    t3.join()

