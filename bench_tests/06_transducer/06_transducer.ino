// BENCH TEST 06: TRANSDUCER
//
// Alternates a frequency you FEEL with one you HEAR, from the same driver.
// Confirms the amp and exciter both work before the session.
//
// If you hear nothing: amp power and volume pot.
// If you feel nothing: the exciter is not pressed firmly against the plate.
// It needs contact to couple into a surface.
//
// PINS
//   D11        ->  PAM8403 input (through a series cap if you have one)
//   amp power   5V and GND
//   transducer  the amp's speaker output, pressed FLAT against a plate
//
// It needs contact with a surface to couple. Held in the air it does almost
// nothing, which is not a fault.


#include "logger.h"

const int TRANSDUCER = 11;

const int FELT_HZ  = 40;    // low enough to be vibration, not tone
const int HEARD_HZ = 400;   // clearly audible

void setup() {
  pinMode(TRANSDUCER, OUTPUT);
  logBegin("BENCH 06  transducer", "D11 -> PAM8403 input;  transducer FLAT on a plate");
}

void loop() {
  logEvent("40 Hz  (feel it)");
  tone(TRANSDUCER, FELT_HZ);
  delay(2000);
  noTone(TRANSDUCER);
  delay(500);

  logEvent("400 Hz (hear it)");
  tone(TRANSDUCER, HEARD_HZ);
  delay(2000);
  noTone(TRANSDUCER);
  delay(1500);
}
