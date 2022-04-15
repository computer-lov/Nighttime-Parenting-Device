import nighttimeParenting as infra
import time

if __name__ == "__main__":

    ##################### CODE TO TEST MIC CIRCUIT #####################

    # initialize mic object
    m = infra.micCircuit()
    print("Testing Microphone Circuit...")
    # call and display micCircuit methods
    dVal = m.getDigitalVal()
    aVal = m.getAnalogVal()
    print("Current Digital Value: ", dVal)
    print("Current Analog Value: ", "{:.2f}".format(aVal), "V")
    tIntv = 2
    avg = m.getPkPkAvg(tIntv)
    print("Calculating Average over 2 second interval...")
    print("Average Digital Value: ", "{:.0f}".format(avg))
    print("Average Analog Value: ",  "{:.2f}".format(m.getAnalogVal(avg)), "V")
    trigVal = 2.5
    isTriggered = m.trigger(trigVal, tIntv)
    message = "Voltage is above threshold value..." if isTriggered else "Voltage is below threshold value..."
    print(message); 

    #################### CODE TO TEST STEREO DECODER ##################

    # initialize stereo decoder object
    sd = infra.StereoDecoder()
    print("Testing Stereo Decoder...")
    # call and display StereoDecoder methods
    print("Pressing play...")
    sd.play()
    time.sleep(3)
    print("Pressing pause...")
    sd.pause()
    time.sleep(3)
    print("Pressing unpause")
    sd.unpause()
    time.sleep(3)
    print("Increasing volume by 8...")
    sd.increaseVol()
    sd.increaseVol()
    sd.increaseVol()
    sd.increaseVol()
    sd.increaseVol()
    sd.increaseVol()
    sd.increaseVol()
    sd.increaseVol()
    time.sleep(3)
    print("Decreasing volume by 5...")
    sd.decreaseVol()
    sd.decreaseVol()
    sd.decreaseVol()
    sd.decreaseVol()
    sd.decreaseVol()
    time.sleep(3)
    print("Stopping audio...")
    sd.stop()
    
    oled = infra.OLED()
    print("Displaying clock")
    print(oled.displayTime())
    time.sleep(3)
    text1 = "abcd efghij klmnopqr"
    text2 = "abcd efghij klmnopqr stuvwxyz 12345 6789"
    text3 = "abcd efghij klmnopqr stuvwxyz 12345 6789" + text1
    text4 = text2 + text2
    print("Display text1")
    oled.printMessage(text1)
    time.sleep(3)
    print("Display text2")
    oled.printMessage(text2)
    time.sleep(3)
    print("Display text3")
    oled.printMessage(text3)
    time.sleep(3)
    print("Display text4")
    oled.printMessage(text4)
    time.sleep(3)
    print("Shutting display")
    oled.turnDisplayOff()
    time.sleep(2)
    print("Turning display back on")
    oled.turnDisplayOn()
    time.sleep(3)
    print("Clearing display")
    oled.clearDisplay()
    time.sleep(3)
    
    ################## CODE TO TEST HEART RATE SENSOR #################

    # initialize heart rate sensor object
    hrs = infra.HRSensor()
    print("Testing Heart Rate Sensor...")
    # call and display HRSensor methods
    hr_spo2 = hrs.getHR_SPO2()
    print("Heart Rate (BPM): ", hr_spo2[0])
    print("Oxygen Saturation Level (SPO2): ", hr_spo2[1])
    
    ###################### CODE TO TEST LED Bar #######################

    # initialize led bar object
    lBar = infra.ledBar()
    print("Testing LED Bar...")
    # call and display led bar methods
    print("Breathing in...")
    lBar.breath_in()
    print("Breathing out...")
    lBar.breath_out()




