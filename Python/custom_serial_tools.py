import serial

from time import sleep

def list_serial_ports(debugPrinting = False):
    #Lists openable serial ports
    #Only works on windows
    #Ensures that the com port is a CH340
    #$Change: add SiLabs as a possible device
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    prefPorts = []
    otherPorts = []
    if debugPrinting:
        print("CH340 Ports:")
    for port in ports:
        if port.vid == 0x1A86 or port.vid == 0x10C4:
            if debugPrinting:
                print(port.device)
            prefPorts.append(port)
    if debugPrinting:
        print("Other Device Ports:")
    for port in ports:
        if port.vid != 0x1A86:
            if debugPrinting:
                print(port.device)
            otherPorts.append(port)
    return [prefPorts, otherPorts]

def writeNewPos(ser, posX, posY):
    pan = posX*500 + 500
    tilt = posY*500 + 500
    pan = max(min(pan, 999), 0)
    tilt = max(min(tilt, 999), 0)
    pan = int(pan)
    tilt = int(tilt)
    sendString = "POS {:03d} {:03d}\n".format(pan, tilt)
    ser.write(bytes(sendString, "UTF-8"))
    return [(pan-500)/500, (tilt-500)/500]

def initGimbal(useFirstFound=False):
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.timeout = 1.0#seconds

    #Get port from the user
    while True:#Loop that exits when a port has been opened
        while True:
            ports, otherPorts = list_serial_ports()
            if len(ports) > 0:
                break
            else:
                print("No CH340 COM Ports were detected")
                input("Press any key to check for new ports...")
                print("Retrying...")
        portNameDict = {}
        for port in ports:
            #append the new port name to the dictionary
            portNameDict[int(port.device.replace('COM', ''))] = port.device
        if useFirstFound == False:
            while True:
                for key,val in portNameDict.items():
                    print("[{}] {}".format(key, val))
                comPortSelection = input("Select a COM Port: ")
                if comPortSelection.isdecimal() and int(comPortSelection) in portNameDict.keys():
                    break;
                else:
                    print("Invalid Selection")
        else:
            for key,val in portNameDict.items():
                comPortSelection = key
            
            
        ser.port = portNameDict[int(comPortSelection)]
        #Port is now selected
        try:
            ser.open()
            print("{} has been opened".format(ser.port))
            break
        except serial.SerialException:
            print("Port could not be opened")

    sleep(1.5)#Give the arduino time to rest for a second
    return ser

def startingAnimation(ser):
    xys = [(0.5,0), (-0.5,0), (0,-0.5), (0,0.5), (0,0), ]
    for x,y in xys:
        writeNewPos(ser, x, y)
        sleep(0.3)
    
    
            
    
