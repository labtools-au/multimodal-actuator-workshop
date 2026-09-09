// TASK 04 on Wokwi: a stand-in, not the real thing.
//
// Wokwi cannot simulate capacitive sensing, because ADCTouch measures a real
// physical property of a real wire. So the button here stands in for the pad:
// press it and the servo reacts, which is the SHAPE of the task.
//
// What you cannot learn here, and can only learn at the bench:
//   - that the reading drifts, so the threshold has to be relative
//   - that the baseline must only learn while untouched
//
// Those two are the whole point of task 04. Use this to get the servo moving,
// then do the real thing on hardware.

#include <Servo.h>

const int PAD   = A0;   // the button, standing in for the foil pad
const int SERVO = 9;

Servo servo;

void setup() {
  pinMode(PAD, INPUT_PULLUP);
  servo.attach(SERVO);
  servo.write(90);
  Serial.begin(9600);
  Serial.println("Press the button. On the bench this is a finger on foil.");
}

void loop() {
  // INPUT_PULLUP reads LOW when pressed.
  if (digitalRead(PAD) == LOW) {
    servo.write(150);
  } else {
    servo.write(90);
  }
  delay(20);
}
