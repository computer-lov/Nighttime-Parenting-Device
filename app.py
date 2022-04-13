import nighttimeParenting as infra


# tasks that run in background

def updateOLED():
    pass

def updateLedBar():
    pass

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

