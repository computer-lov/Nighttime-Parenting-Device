import micCircuit as mic

if __name__ == "__main__":

    ##################### CODE TO TEST MIC CIRCUIT LIBRARY #####################

    # initialize mic object
    m = mic()
    print("Testing Microphone Circuit...")
    # call and display micCircuit methods
    aVal = m.readAnalogVal()
    print("Analog Value: ", aVal)
    dVal = m.atod(aVal)
    print("Digitial Value: ", dVal)
    trigVal = 2.5
    isTriggered = m.trigger(trigVal)
    message = "Voltage is above threshold value..." if isTriggered else "Voltage is below threshold value..."
    print(message); 




