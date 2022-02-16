import micCircuit as mic

if __name__ == "__main__":

    ##################### CODE TO TEST MIC CIRCUIT LIBRARY #####################

    # initialize mic object
    m = mic()
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




