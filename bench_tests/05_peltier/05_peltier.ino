// BENCH TEST 05: PELTIER
//
// Warms for 10 s, off, cools for 10 s, off. Touch the tile face to confirm
// both directions work before students arrive.
//
// Two PWM pins per channel, matching how the lab's other actuator rigs drive
// motors: one pin at speed, the other at 0, and swap them to reverse.
//
// SAFETY: heatsink on the hot face, or the tile destroys itself. MAX_LEVEL
// caps the temperature. Do not raise it. Skin burns above 50 C.
//
// PINS
//   D3   PWM   ->  channel LOW side
//   D5   PWM   ->  channel HIGH side
//   Drive one and hold the other at 0 to choose direction. Both to 0 is off.
//   Tile on a BENCH supply, not the Arduino: it wants 2 to 4 A.
//
// SAFETY: heatsink on the hot face before power, every time.


#include "logger.h"

const int tileLow = 3, tileHigh = 5;
const int MAX_LEVEL = 200;

void drive(int lowPin, int highPin, int lvl) {
  analogWrite(lowPin, min(lvl, MAX_LEVEL));
  analogWrite(highPin, 0);
}

void allOff() {
  analogWrite(tileLow, 0);
  analogWrite(tileHigh, 0);
}

void setup() {
  pinMode(tileLow, OUTPUT);
  pinMode(tileHigh, OUTPUT);
  allOff();
  logBegin("BENCH 05  peltier", "D3, D5 PWM -> H-bridge;  tile on the BENCH supply");
}

void loop() {
  logEvent("WARM");
  drive(tileLow, tileHigh, 180);
  delay(10000);

  allOff();
  logEvent("off");
  delay(4000);

  logEvent("COOL");
  drive(tileHigh, tileLow, 180);
  delay(10000);

  allOff();
  logEvent("off");
  delay(4000);
}
