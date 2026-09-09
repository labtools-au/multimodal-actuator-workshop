// UTIL: PIN DEBUG
//
// "Nothing is happening" has two very different causes: the Arduino is not
// driving the pin, or the thing on the end of the wire is not responding.
// This tells you which, without a multimeter.
//
// It drives D8..D11 one at a time and, for each, reads the pin back and
// mirrors it onto the onboard LED. The onboard LED needs no wiring, so it
// proves the sketch is alive and the pin really is going high even when the
// external board does nothing at all.
//
// PINS
//   nothing required. Works on a bare Uno.
//   Whatever you are debugging stays connected: D8..D11 for a ULN2003.
//
// HOW TO READ IT
//   onboard LED blinks in step with the serial output
//       -> the Arduino is fine. The fault is the driver board, its power,
//          or the wiring between them.
//   onboard LED does nothing
//       -> the sketch is not running. Wrong board, failed upload, or reset.
//   a pin reads LOW while being driven HIGH
//       -> that pin is shorted to ground, usually a jumper in the wrong hole
//          or a bridged pair. The line is flagged SHORT.

#include "logger.h"

const int PINS[] = {8, 9, 10, 11};
const int N = 4;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  for (int i = 0; i < N; i++) {
    pinMode(PINS[i], OUTPUT);
    digitalWrite(PINS[i], LOW);
  }
  logBegin("UTIL  pin debug", "drives D8..D11 one at a time, mirrors to onboard LED");
  logHint("Watch the onboard LED by pin 13, and any LEDs on your driver board.");
  logHint("Onboard blinking but driver dark = the fault is past the Arduino.");
}

void loop() {
  for (int i = 0; i < N; i++) {
    digitalWrite(PINS[i], HIGH);
    digitalWrite(LED_BUILTIN, HIGH);

    // Read the pin back. An output pin driven HIGH must read HIGH; if it does
    // not, something external is holding it down.
    delayMicroseconds(50);
    bool readback = digitalRead(PINS[i]);

    Serial.print(millis());
    Serial.print(F(" ms  D"));
    Serial.print(PINS[i]);
    Serial.print(F(" HIGH   reads back "));
    Serial.print(readback ? F("HIGH  ok") : F("LOW   SHORT TO GROUND"));
    Serial.println();

    delay(700);
    digitalWrite(PINS[i], LOW);
    digitalWrite(LED_BUILTIN, LOW);
    delay(300);
  }
  logEvent("--- cycle done, repeating ---");
}
