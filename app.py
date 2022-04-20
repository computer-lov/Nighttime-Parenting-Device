import nighttimeParenting as infra
import time
from threading import Thread, Lock, Event

# TODO:
#       need to use events for things that run in response to something else

#################### tasks that run in background ####################

# updates oled screen
def updateOLED():
    with i2cL:
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
    with spiL:
        lBar.breathe_in()
        lBar.breathe_out()

# calculate stress level of caregiver
def calculateStessLevel():
    return hrs.getHR_SPO2()

############### tasks that run in response to something ###############

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

###################### tasks that run at start up ######################

def isAwake():
    # constantly monitor audio levels
    while True:
        # time interval to 2 seconds
        timeInt = 2
        # trigger value 2.5V
        trigVal = 2.5

        with spiL:
            isTriggered = m.trigger(trigVal, timeInt)
        
        # return true if audio level above threshold
        if isTriggered:
            return True

if __name__ == "__main__":
    m = infra.micCircuit()
    sd = infra.StereoDecoder()
    oled = infra.OLED()
    lBar = infra.ledBar()
    hrs = infra.HRSensor()
    phyUI = infra.PhysicalUI(sd, oled, lBar)

    i2cL = Lock()
    spiL = Lock()

    t1 = Thread(target=isAwake)
    t1.start()
    t2 = Thread(target=updateOLED)
    t2.start()
    t3 = Thread(target=updateLedBar)
    t3.start()
    t4 = Thread(target=calculateStessLevel)
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

