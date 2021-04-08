void setup() {
  initServos();
}

void loop() {
  writeTiltServo(0);
  writePanServo(0);

  delay(2000);

  writeTiltServo(0);
  writePanServo(255);

  delay(2000);

  writeTiltServo(255);
  writePanServo(255);

  delay(2000);

  writeTiltServo(255);
  writePanServo(0);

  delay(2000);
  
  
}
