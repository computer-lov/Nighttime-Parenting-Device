import nighttimeParenting as infra

if __name__ == "__main__":

    ##################### CODE TO TEST MIC CIRCUIT LIBRARY #####################

    # initialize mic object
    sleeve = infra()
    print("Testing Microphone Circuit...")
    # call and display micCircuit methods
    dVal = sleeve.getDigitalVal()
    print("Digital Value: ", dVal)
    aVal = sleeve.getAnalogVal()
    print("Analog Value: ", aVal)
    trigVal = 2.5
    isTriggered = m.trigger(trigVal)
    message = "Voltage is above threshold value..." if isTriggered else "Voltage is below threshold value..."
    print(message); 




