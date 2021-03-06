#include <Servo.h>

//
// Pin assignments
//

const byte leftSensorPin_I  = 2;
const byte rightSensorPin_I = 3;
const byte leftPWMPin_O  = 10;
const byte rightPWMPin_O = 9;

//
// Constants
//

const unsigned int maxRPM = 150;
const unsigned int wheelCircum = 785; //mm (Wheel diameter is 25cm)
const unsigned int pulsesPerRevolution = 192;
const unsigned int pidPeriod = 200; //ms

//
// Create Servo objects
//

Servo leftWheelServo;
Servo rightWheelServo;

//
// Global variables
//


float leftKp  = 0.1;
float leftKi  = 0.7;
float rightKp = 0.1;
float rightKi = 0.7;

volatile int leftSensorPIDCount  = 0;
volatile int rightSensorPIDCount = 0;

volatile int leftSensorDistanceCount = 0;
volatile int rightSensorDistanceCount = 0;

volatile int leftError = 0;
volatile int rightError = 0;

volatile int leftLastError = 0;
volatile int rightLastError = 0;

volatile int leftOffset = 0;
volatile int rightOffset = 0;

volatile int desiredSpeed = 60;

volatile int desiredLeftPIDCount = 0;
volatile int desiredRightPIDCount = 0;

boolean leftDirection = 0; // 0 - forward, 1 - backward
boolean rightDirection = 0; // 0 - forward, 1 - backward

char serialCommand = 0;
int serialValue= 0;

int timercount=0;


//
// Intial Setup
//

void setup() {

  // Set up hardware interrupts
  attachInterrupt(digitalPinToInterrupt(leftSensorPin_I) , leftSensorISR , CHANGE);
  attachInterrupt(digitalPinToInterrupt(rightSensorPin_I), rightSensorISR, CHANGE);

  // Set up timer interrupt
  TCCR2A = 0;
  TCCR2B = 0;
  TCNT2 = 0;

  OCR2A = 124; // Compare value

  TCCR2A |= (1 << WGM21);
  TCCR2B |= (1 << CS22) | (1 << CS21) | (1 << CS20); // 1024 prescaler
  TIMSK2 |= (1 << OCIE2A);

  // Set up outputs
  leftWheelServo.attach(leftPWMPin_O);
  rightWheelServo.attach(rightPWMPin_O);

  leftWheelServo.write(90);
  rightWheelServo.write(90);

  // Initialise serial communication
  Serial.begin(19200);
}

//
// Hardware Interrupts for counting rotary encoder pulses
//

void leftSensorISR () {
  leftSensorPIDCount ++;
  leftSensorDistanceCount ++;
}

void rightSensorISR () {
  rightSensorPIDCount ++;
  rightSensorDistanceCount ++;
}

//
// PID Controller - for both wheels
//

ISR (TIMER2_COMPA_vect) {

  sei(); //Re-enable all interrupts

  if (timercount >= 24) {

  leftError = desiredLeftPIDCount - leftSensorPIDCount;
  rightError = desiredRightPIDCount - rightSensorPIDCount;

  leftSensorPIDCount = 0;
  rightSensorPIDCount = 0;

  leftOffset  += (leftKp  * (leftError  - leftLastError )) + (leftKi  * leftError );
  rightOffset += (rightKp * (rightError - rightLastError)) + (rightKi * rightError);

  leftLastError = leftError;
  rightLastError = rightError;

  leftOffset = constrain(leftOffset, 0, 90 - (leftDirection * 30)); // If forwards, then 0-90. If backwards, then 0-60
  rightOffset = constrain(rightOffset, 0, 90 - (rightDirection * 30));

  if (leftDirection == 0){
    leftWheelServo.write(90 + leftOffset);
  } else {
    leftWheelServo.write(90 - leftOffset);
  }
  if (rightDirection == 0){
    rightWheelServo.write(90 + rightOffset);
  } else {
    rightWheelServo.write(90 - rightOffset);
  }

  timercount = 0;
  } else {
    timercount++;
  }
}

//
// Movement functions
//

void moveForward (int distance) {
 leftDirection = 0;
 rightDirection = 0;
 desiredLeftPIDCount = (desiredSpeed / (float)60) * pulsesPerRevolution / (float)(1000 / pidPeriod);
 desiredRightPIDCount = (desiredSpeed / (float)60) * pulsesPerRevolution / (float)(1000 / pidPeriod);
}

void moveBackward (int distance) {
 leftDirection = 1;
 rightDirection = 1;
 desiredLeftPIDCount = (desiredSpeed / (float)60) * pulsesPerRevolution / (float)(1000 / pidPeriod);
 desiredRightPIDCount = (desiredSpeed / (float)60) * pulsesPerRevolution / (float)(1000 / pidPeriod);
}

void rotateLeft (int angle) {
 leftDirection = 1;
 rightDirection = 0;
 desiredLeftPIDCount = (desiredSpeed / (float)60) * pulsesPerRevolution / (float)(1000 / pidPeriod);
 desiredRightPIDCount = (desiredSpeed / (float)60) * pulsesPerRevolution / (float)(1000 / pidPeriod);
}

void rotateRight (int angle) {
 leftDirection = 0;
 rightDirection = 1;
 desiredLeftPIDCount = (desiredSpeed / (float)60) * pulsesPerRevolution / (float)(1000 / pidPeriod);
 desiredRightPIDCount = (desiredSpeed / (float)60) * pulsesPerRevolution / (float)(1000 / pidPeriod);

}

// Set Speed function - sets the forward/reverse speed in rpm - not intended to be used in normal operation, only for testing
void setSpeed (int speed) {
  if ((speed >= 0) && (speed <= maxRPM)) {
    desiredSpeed = speed;
  } else {
    desiredSpeed = 0;
    Serial.print("Error, invalid speed set. Speed must be between 0 and ");
    Serial.println(maxRPM);
  }

}

void stopMoving () {
  desiredLeftPIDCount = 0;
  desiredRightPIDCount = 0;
}

//
// Main Loop
//

void loop() {

  if (Serial.available() >= 2) {
    serialCommand = Serial.read();
    serialValue = Serial.parseInt();


    if (serialCommand == 'X') {
      stopMoving();
    } else if (serialCommand == 'F') {
      moveForward(serialValue);
    } else if (serialCommand == 'B') {
      moveBackward(serialValue);
    } else if (serialCommand == 'L') {
      rotateLeft(serialValue);
    } else if (serialCommand == 'R') {
      rotateRight(serialValue);
    } else if (serialCommand == 'S') {        // For testing
      setSpeed(serialValue);                  // For testing
    } else {
      stopMoving();
    }

  }

}
