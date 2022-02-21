import nighttimeParenting as infra

if __name__ == "__main__":

    ##################### CODE TO TEST MIC CIRCUIT #####################

    # initialize mic object
    m = infra.micCircuit()
    print("Testing Microphone Circuit...")
    # call and display micCircuit methods
    dVal = m.getDigitalVal()
    print("Digital Value: ", dVal)
    aVal = m.getAnalogVal()
    print("Analog Value: ", aVal)
    trigVal = 2.5
    isTriggered = m.trigger(trigVal)
    message = "Voltage is above threshold value..." if isTriggered else "Voltage is below threshold value..."
    print(message); 

    #################### CODE TO TEST STEREO DECODER ##################

    # initialize stereo decoder object
    sd = infra.StereoDecoder()
    print("Testing Stereo Decoder...")
    # call and display StereoDecoder methods
    print("Pressing play...")
    sd.play()
    print("Pressing pause...")
    sd.pause()
    print("Increasing volume...")
    sd.increaseVol()
    print("Decreasing volume...")
    sd.decreaseVol()

    ################## CODE TO TEST HEART RATE SENSOR #################

    # initialize heart rate sensor object
    hrs = infra.HRSensor()
    print("Testing Heart Rate Sensor")
    # call and display HRSensor methods
    hRate = hrs.getHR()
    print("Heart Rate (BPM): ", hRate)
    oSatLevel = hrs.getSPO2()
    print("Oxygen Saturation Level (SPO2): ", oSatLevel)
    temp = hrs.getTemp()
    print("Temperature: ", temp)




