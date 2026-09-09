// BENCH TEST 03: SOLENOID
//
// One tap every two seconds. If it does not click, check in this order:
//   1. bench supply on, and sharing ground with the Arduino
//   2. MOSFET gate on D6
//   3. flyback diode across the coil, striped end to +V
//
// If the board RESETS when it fires, the solenoid is drawing from USB. It
// needs its own supply. That reset looks exactly like a software crash and
// is not one.
//
// PINS
//   D6         ->  MOSFET gate (IRLZ44N or similar logic-level)
//   MOSFET      source to GND, drain to the solenoid
//   solenoid    other leg to +5V on ITS OWN supply
//   diode       1N4148 across the coil, BAND to +5V
//   grounds     the supply GND and the Arduino GND must be joined
//
// Adafruit 2776: 5V, 1.1 A, 4.5 ohm coil, 3mm throw at 80g. Adafruit warn
// against powering it from USB, and they are right: the board browns out.


#include "logger.h"

const int SOLENOID = 6;
const int PULSE_MS = 15;    // never raise this much. The coil heats fast.

void setup() {
  pinMode(SOLENOID, OUTPUT);
  digitalWrite(SOLENOID, LOW);
  logBegin("BENCH 03  solenoid", "D6 -> MOSFET gate;  solenoid on its OWN supply");
}

void loop() {
  digitalWrite(SOLENOID, HIGH);
  delay(PULSE_MS);
  digitalWrite(SOLENOID, LOW);   // ALWAYS turn it off
  logEvent("tap");
  delay(2000);                   // long gap keeps the duty cycle low
}
