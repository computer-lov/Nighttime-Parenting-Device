import nighttimeParenting as infra
import time
from threading import Thread, Lock, Event
from datetime import datetime
import smtplib, ssl

# TODO:
#       need to test this layer
#       need to check if pi has smtplib, ssl libraries
#       might need to remove a few functions
#       have to figure out stuff for analytics
#       figure out when to show time vs encouraging messages

######################## supporting functions ########################

# sends email to caregiver
def sendEmail(message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.set_debuglevel(1)
        #server.ehlo()
        #server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

#################### tasks that run in background ####################

# monitors audio level in bedrooom
def monitorBaby():
    # time interval to 10 seconds
    timeInt = 10
    # trigger value 10
    trigVal = 10

    # constantly monitor audio levels
    while True:
        with spiL:
            # isTriggered = m.trigger(trigVal, timeInt)
            isTriggered = True # made this change to test app layer w/o mic
        
        # return true if audio level above threshold
        if isTriggered:
            wakeup.set()
        time.sleep(3)

# calculate stress level of caregiver
def calculateStessLevel():
    BPM = 111
    Spo2 = 94

    while True:
        # get stress level
        print("Waiting to acquire i2cL in calculateStressLevel")
        with i2cL:
            print("Acquired i2cL in calculateStressLevel")
            stressLevel = hrs.getHR_SPO2()
        print("Released i2cL in calculateStressLevel")

        print(BPM, Spo2)
        """
        # determine if stress level is high
        if (BPM != None and Spo2 != None):
            # calculate average bpm and sp02 
            BPM = stressLevel[0]
            Spo2 = stressLevel[1]
        """

        if (BPM >= 110 and Spo2 < 95):
            disableAll.clear()
            stressHigh.set()
            enableBreathing.set()
            enableMessages.set()
            enableMusic.set()
        else:
            stressHigh.clear()
            enableBreathing.clear()
            enableMessages.clear()
            enableMusic.clear()
            disableAll.set()
        
        time.sleep(2)

# displays time
def timeDisplay():
    while True:
        if not toggleMessage:
            with displayL:
                with i2cL:
                    oled.clearDisplay()
                    oled.displayTime()
            # time.sleep(60) # new time displayed every 60 seconds

############### tasks that run in response to stress level ##############

# sends email warning stress levels are high
def notifyStessLevels():
    stressHigh.wait()    
    message = """\
    Subject: Stress Level Elevated!

    BPM above 110 and SPO2 below 95%."""
    # sendEmail(message)

# displays encouriging messages
def messageDisplay():
    while toggleMessage:
        enableMessages.wait()
        for mes in messages:
            with displayL:
                with i2cL:
                    oled.clearDisplay()
                    oled.printMessage(mes)
                time.sleep(10)
            # time.sleep(10) # new message displayed every 3 seconds

# updates breathing
def updateBreathing():
    while True:
        enableBreathing.wait()
        with spiL:
            lBar.breathe_in()
            lBar.breathe_out()
        time.sleep(3)

# turns on soothing music
def playMusic():
    enableMusic.wait()
    sd.play()

# stops music, breathing exercise, and ecouraging messages
def haltStressRelief():
    disableAll.wait()
    sd.stop()
    # with i2cL:
    #    oled.turnDisplayOff()

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

# pauses messages
def pauseMessages():
    global toggleMessage
    toggleMessage = False

# resumes messages
def resumeMessages():
    global toggleMessage
    toggleMessage = True

# pauses music
def pauseMusic():
    sd.pause()

# resumes music
def resumeMusic():
    sd.unpause()

# adjusts volume
def adjustVolume(volLevel):
    with spiL:
        sd.setVol(volLevel)

############### tasks that run in response to physical UI ##############

# updates brightness
def updateBrightness():
    while True:
        with spiL:
            currBrightness = phyUI.getBrightness()
        with i2cL:
            phyUI.setBrightness(currBrightness)

        time.sleep(3)
    
# updates volume
def updateVolume():
    while True:
        with spiL:
            phyUI.toggleVolume()
        time.sleep(3)

# send SOS message to parent
def sendSOS():
    while True:
        if phyUI.triggerSOS():
            # send email
            print("button")
            message = """\
            Subject: SOS
            
            In dire need of assistance! Please come help!"""
            sendEmail(message)

            # show confirmation on display
            confirmMes = "Email sent successfully!"
            with displayL:
                with i2cL:
                    oled.clearDisplay()
                    oled.displayTime()
                time.sleep(3)
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
    displayL = Lock()

    # create events
    wakeup = Event()
    stressHigh = Event()
    enableBreathing = Event()
    enableMusic = Event()
    enableMessages = Event()
    disableAll = Event()

    # set state to zero by default (display encouring messages)
    toggleMessage = True

    # taken from parenting.firstcry.com
    messages = ["You are doing great; it will be over soon, hang in there!", 
                "Keep calm, hold your breath, and change this diaper.", 
                "3 am. Party in my crib, be there. Bring your own diaper.",
                "Poops, I did it again, I made you believe that this could be pee.",
                "Houston, we have a problem... It is code brown."]

    # set up server for email
    port = 465 #587  # For starttls
    smtp_server = "smtp.mail.yahoo.com" #"smtp.gmail.com"
    #sender_email = "apm532@nyu.edu"
    receiver_email = "ag7997@nyu.edu"
    password = "spqcgqenfthwonyz"
    sender_email = "tzali.goldberg@yahoo.com"
    # receiver_email = input("Type your email and press enter: ")
    # password = input("Type your password and press enter: ")

    # thread everything except browser UI
    t1 = Thread(target=monitorBaby)
    t1.start()
    t2 = Thread(target=calculateStessLevel)
    t2.start()
    t3 = Thread(target=notifyStessLevels)
    t3.start()
    t4 = Thread(target=messageDisplay)
    t4.start()
    t5 = Thread(target=timeDisplay)
    t5.start()
    t6 = Thread(target=updateBreathing)
    t6.start()
    t7 = Thread(target=playMusic)
    t7.start()
    t8 = Thread(target=haltStressRelief)
    t8.start()
    t9 = Thread(target=wakeupEvent)
    t9.start()
    t10 = Thread(target=updateBrightness)
    t10.start()
    t11 = Thread(target=updateVolume)
    t11.start()
    t12 = Thread(target=sendSOS)
    t12.start()

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
    t12.join()

