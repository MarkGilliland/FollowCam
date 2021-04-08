import custom_serial_tools as ardLib


#A port has been sucessfully opened, called ser

ser = ardLib.initGimbal()
ardLib.startingAnimation(ser)

##Close the port when done
ser.close()
