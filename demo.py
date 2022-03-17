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
    tIntv = 10
    avg = 0 # m.getPkPkAvg(tIntv)
    print("Calculating Average over 10 second interval...")
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
    time.sleep(10)
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
    

    ################## CODE TO TEST HEART RATE SENSOR #################

    # initialize heart rate sensor object
    #hrs = infra.HRSensor()
    #print("Testing Heart Rate Sensor...")
    # call and display HRSensor methods
    #hRate = hrs.getHR()
    #print("Heart Rate (BPM): ", hRate)
    #oSatLevel = hrs.getSPO2()
    #print("Oxygen Saturation Level (SPO2): ", oSatLevel)
    #temp = hrs.getTemp()
    #print("Temperature: ", temp)

    ###################### CODE TO TEST LED Bar #######################

    # initialize led bar object
    lBar = infra.ledBar()
    print("Testing LED Bar...")
    # call and display led bar methods
    print("Breathing in...")
    lBar.breath_in()
    print("Breathing out...")
    lBar.breath_out()






