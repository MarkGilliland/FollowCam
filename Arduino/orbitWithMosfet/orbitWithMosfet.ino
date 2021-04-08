//Dec 2020 Mark Gilliland

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  initServos();
}

void loop() {
//  if(Serial.available()){
//    String newCommand = Serial.readStringUntil('\n');
//    if(newCommand.startsWith("POS")){//POS pan tlt
//      String panStr = newCommand.substring(4, 7);
//      String tiltStr = newCommand.substring(8, 11);
//      uint16_t panInt = panStr.toInt();
//      uint16_t tiltInt = tiltStr.toInt();
//
//      writePanUnits(panInt);
//      writeTiltUnits(tiltInt);
//    }
//  }
  for(uint8_t i = 0; i < 2; i++){
    enableServos(i);
    
    writeTiltServo(0);
    writePanServo(0);
  
    delay(1000);
  
    writeTiltServo(0);
    writePanServo(1000);
  
    delay(1000);
  
    writeTiltServo(1000);
    writePanServo(1000);
  
    delay(1000);
  
    writeTiltServo(1000);
    writePanServo(0);
  
    delay(1000);
  }
  
}
