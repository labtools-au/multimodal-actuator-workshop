// BENCH TEST 07: STEPPER (28BYJ-48 + ULN2003)
//
// Turns one full revolution each way. If it hums but does not turn, the pin
// ORDER is wrong, not the wiring.
//
// PINS, from the ULN2003 board to the Uno:
//
//   IN1 -> D8      IN2 -> D9      IN3 -> D10     IN4 -> D11
//
//   Board 5V and GND to the Arduino, or its own supply under any load.
//
// THE GOTCHA THAT COSTS PEOPLE AN HOUR:
//   the Stepper constructor does NOT take the pins in numeric order. It wants
//   IN1-IN3-IN2-IN4, so the numbers read 8, 10, 9, 11. Wire them 8..11 in
//   order on the board, then swap the middle two here.
//
//   Get it wrong and the motor buzzes and jitters instead of rotating.

#include <Stepper.h>

// 28BYJ-48 is 32 steps per motor revolution through a 1/64 gearbox,
// so 2048 steps per output shaft revolution in full-step mode.
const int STEPS_PER_REV = 2048;

// IN1, IN3, IN2, IN4. See the note above.
Stepper motor(STEPS_PER_REV, 8, 10, 9, 11);

void setup() {
  Serial.begin(9600);
  Serial.println("Stepper test. One turn each way, repeating.");
  // The library sets the pins as outputs itself.
}

void loop() {
  Serial.println("clockwise, 10 RPM");
  motor.setSpeed(10);          // this motor tops out around 15 RPM
  motor.step(STEPS_PER_REV);
  delay(800);

  Serial.println("anticlockwise, 10 RPM");
  motor.step(-STEPS_PER_REV);
  delay(800);
}
