// Shared logger. The same file sits in every sketch folder, so the Serial
// Monitor looks the same whichever sketch you uploaded.
//
// You do not need to install anything. The Arduino IDE compiles every file
// next to the .ino, so this is picked up automatically.
//
// Why it exists: at a bench, "tick" on its own does not tell you whether you
// uploaded the right sketch to the right board. logBegin() prints a banner
// that names the sketch and the pins, so one glance confirms it.

#pragma once
#include <Arduino.h>

// Opens the port and prints the banner. Call this first in setup().
//   name  what this sketch is, e.g. "02 piezo"
//   pins  the wiring in one line, e.g. "D8 -> piezo, other leg -> GND"
inline void logBegin(const char *name, const char *pins) {
  Serial.begin(9600);
  while (!Serial && millis() < 2000) { }   // USB boards; Uno passes straight through

  Serial.println();
  Serial.println(F("========================================"));
  Serial.print(F("  "));
  Serial.println(name);
  Serial.print(F("  pins: "));
  Serial.println(pins);
  Serial.println(F("========================================"));
}

// One event, timestamped. Use for anything that happens: "tick", "tap", "WARM".
// The timestamp is what makes a rhythm legible when you cannot hear it well.
inline void logEvent(const char *msg) {
  Serial.print(millis());
  Serial.print(F(" ms  "));
  Serial.println(msg);
}

// An event with a number attached, e.g. logValue("strength", 130).
inline void logValue(const char *label, long value) {
  Serial.print(millis());
  Serial.print(F(" ms  "));
  Serial.print(label);
  Serial.print(F(" = "));
  Serial.println(value);
}

// A line the student is meant to act on, set apart from the event stream.
inline void logHint(const char *msg) {
  Serial.print(F(">>> "));
  Serial.println(msg);
}

// NOTE ON THE SERIAL PLOTTER
// Sketches that draw a graph (04 capacitive, analog_monitor) must print bare
// numbers separated by spaces, and nothing else, or the plotter cannot parse
// them. Those sketches use logBegin() for the banner and then print raw
// numbers directly. Do not wrap their data lines in logEvent().
