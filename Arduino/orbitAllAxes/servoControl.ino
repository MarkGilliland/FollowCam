#include <Servo.h>

Servo panServo;
Servo tiltServo;

const int TILT_SERVO_MAX = 100;
const int TILT_SERVO_MIN = 10;

const int PAN_SERVO_MAX = 160;
const int PAN_SERVO_MIN = 20;

void initServos(){
  panServo.attach(9);
  tiltServo.attach(8);
}

void writeTiltServo(uint8_t pos){
  if(pos < TILT_SERVO_MIN){
    pos = TILT_SERVO_MIN;
  }
  else if(pos > TILT_SERVO_MAX){
    pos = TILT_SERVO_MAX;
  }
  tiltServo.write(pos);
}

void writePanServo(uint8_t pos){
  if(pos < PAN_SERVO_MIN){
    pos = PAN_SERVO_MIN;
  }
  else if(pos > PAN_SERVO_MAX){
    pos = PAN_SERVO_MAX;
  }
  panServo.write(pos);
}
