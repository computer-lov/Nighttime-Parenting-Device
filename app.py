import nighttimeParenting as infra
import time
from threading import Thread, Lock, Event
from datetime import datetime
import smtplib, ssl

# TODO:
#       need to test this layer
#       need to check if pi has smtplib, ssl libraries

######################## supporting functions ########################

# sends email to caregiver
def sendEmail(message):
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

# averages bpm and spo2 over specified time interval
def stressLevelAvg(timeInt):
    # sample bpm and spo2 over 2 second interval
    bpmSum = 0
    spo2Sum = 0
    count = 0
    start = time.time()
    while (time.time() - start) < timeInt:
        curr = hrs.getHR_SPO2()
        bpmSum += curr[0]
        spo2Sum += curr[1]
        count += 1
    
    # calculate average bpm and sp02 
    avgBPM = bpmSum / count
    avgSpo2 = spo2Sum / count

    return (avgBPM, avgSpo2)

# displays time
def timeDisplay():
    with i2cL:
        oled.clearDisplay()
        oled.displayTime()
        time.sleep(1) # new time displayed every second

# displays encouriging messages
def messageDisplay():
    with i2cL:
        for mes in messages:
            oled.clearDisplay()
            oled.printMessage(mes)
            time.sleep(3) # new message displayed every 3 seconds

#################### tasks that run in background ####################

# monitors audio level in bedrooom
def monitorBaby():
    # time interval to 2 seconds
    timeInt = 2
    # trigger value 2.5V
    trigVal = 2.5

    # constantly monitor audio levels
    while True:
        with spiL:
            # isTriggered = m.trigger(trigVal, timeInt)
            isTriggered = True # made this change to test app layer w/o mic
        
        # return true if audio level above threshold
        if isTriggered:
            wakeup.set()

# calculate stress level of caregiver
def calculateStessLevel():
     # time interval to 2 seconds
    timeInt = 2

    while True:
        # get stress level
        stressLevel = stressLevelAvg(timeInt)
        
        # calculate average bpm and sp02 
        avgBPM = stressLevel[0]
        avgSpo2 = stressLevel[1]

        # determine if stress level is high
        if (avgBPM >= 110 and avgSpo2 < 95):
            stressLOW.clear()
            stressHIGH.set()
        else:
            stressHIGH.clear()
            stressLOW.set()

############### tasks that run in response to stress level ##############

# sends email warning stress levels are high
def notifyStessLevels():
    stressHIGH.wait()    
    message = """\
    Subject: Stress Level Elevated!

    BPM above 110 and SPO2 below 95%."""
    # sendEmail(message)

# updates encouriging messages
def updateDisplay():
    stressHIGH.wait()
    while True:
        if state:
            timeDisplay()
        else:
            messageDisplay()

# updates breathing
def updateBreathing():
    stressHIGH.wait()
    while True:
        with spiL:
            lBar.turnOnLBar()
            lBar.breathe_in()
            lBar.breathe_out()

# turns on soothing music
def playMusic():
    stressHIGH.wait()
    sd.play()

# stops music, breathing exercise, and ecouraging messages
def haltStressRelief():
    stressLOW.wait()
    sd.stop()
    with spiL:
        lBar.turnOffLBar()
    with i2cL:
        oled.turnDisplayOff()

############### tasks that run in response to baby wakeup ##############

# adds to log and sends email when wakeup event occurs
def wakeupEvent():
    global log
    wakeup.wait()
    wakeupTime = datetime.now().strftime("%B %d, %Y %H:%M:%S %p")
    log.append(wakeupTime)
    message = """\
    Subject: Your baby is Awake! 
        
    Your baby woke up at approximately """ + wakeupTime + "."
    # sendEmail(message)
    wakeup.clear()

############### tasks that run in response to stress browser UI ##############

# toggles message and time for display
def changeScreenView():
    global state
    if state:
        state = 0
    else:
        state = 1

# pauses music
def pauseMusic():
    sd.pause()

# unpauses music
def unpauseMusic():
    sd.unpause()

############### tasks that run in response to physical UI ##############

# updates brightness
def updateBrightness():
    with spiL:
        phyUI.toggleBrightness()

# updates volume
def updateVolume():
    with spiL:
        phyUI.toggleVolume()

# send SOS message to parent
def sendSOS():
    if phyUI.triggerSOS():
        # send email
        message = """\
        Subject: SOS
            
        In dire need of assistance! Please come help!"""
        #sendEmail(message)

        # show confirmation on display
        confirmMes = "Email sent successfully!"
        with i2cL:
            oled.clearDisplay()
            oled.printMessage(confirmMes)
            time.sleep(3) # let it appear on screen for 3 seconds 

if __name__ == "__main__":
    # create objects
    m = infra.micCircuit()
    sd = infra.StereoDecoder()
    oled = infra.OLED()
    lBar = infra.ledBar()
    hrs = infra.HRSensor()
    phyUI = infra.PhysicalUI(sd, oled, lBar)

    # create empty log
    log = []

    # creates locks
    i2cL = Lock()
    spiL = Lock()

    # create events
    wakeup = Event()
    stressHIGH = Event()
    stressLOW = Event()

    # set state to zero by default (display encouring messages)
    state = 0
    # taken from parenting.firstcry.com
    messages = ["You are doing great; it will be over soon, hang in there!", 
                "Keep calm, hold your breath, and change this diaper.", 
                "3 am. Party in my crib, be there. Bring your own diaper.",
                "Poops, I did it again, I made you believe that this could be pee.",
                "Huston, we have a problem… It is code brown."]

    # set up server for email
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "apm532@nyu.edu"
    # receiver_email = input("Type your email and press enter: ")
    # password = input("Type your password and press enter: ")

    # thread everything except browser UI
    t1 = Thread(target=monitorBaby)
    t1.start()
    t2 = Thread(target=calculateStessLevel)
    t2.start()
    t3 = Thread(target=notifyStessLevels)
    t3.start()
    t4 = Thread(target=updateDisplay)
    t4.start()
    t5 = Thread(target=updateBreathing)
    t5.start()
    t6 = Thread(target=playMusic)
    t6.start()
    t7 = Thread(target=haltStressRelief)
    t7.start()
    t8 = Thread(target=wakeupEvent)
    t8.start()
    t9 = Thread(target=updateBrightness)
    t9.start()
    t10 = Thread(target=updateVolume)
    t10.start()
    t11 = Thread(target=sendSOS)
    t11.start()

    # join threads
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()
    t11.join()

