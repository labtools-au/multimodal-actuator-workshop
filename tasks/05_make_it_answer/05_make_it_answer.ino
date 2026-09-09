// TASK 5: MAKE IT ANSWER BACK
//
// Goal: input drives output. This is the smallest complete interaction, and
// it is the template for most of what you will build in the project weeks.
//
// Everything before this was one half. Task 4 sensed, tasks 1 to 3 acted.
// Here they are wired together: touch the pad, feel a response.
//
// PINS  build this before you upload
//
//   A0 ---- bare wire ---- foil     the pad you built in task 04
//   D8 ---- piezo ---- GND          the piezo you built first
//
//   Three wires, and still no transistor. You already built both halves;
//   this task only joins them.
//
//   UPGRADE, once the piezo version works: move the output to the coin motor
//   on D9 and swap respond() for the analogWrite version below. That needs
//   the driver circuit from task 01, which is the point at which this stops
//   being three wires.

#include "logger.h"

#include <ADCTouch.h>

const int PAD   = A0;
const int PIEZO = 8;     // start here: no driver, two wires
// const int MOTOR = 9;  // upgrade: needs the task 01 transistor circuit

// ---- CHANGE ME ------------------------------------------------------------
float threshold  = 1.01;
int   debounceMs = 100;   // ignore re-triggers this soon after one fires
// ---------------------------------------------------------------------------

int baseline[25];
int idx = 0;
unsigned long lastFire = 0;

int baselineAverage() {
  long t = 0;
  for (int i = 0; i < 25; i++) t += baseline[i];
  return t / 25;
}

// ---- THE INTERESTING PART -------------------------------------------------
// Everything above is plumbing. THIS is your design decision.
void respond() {
  tone(PIEZO, 2000);
  delay(60);
  noTone(PIEZO);
}

// The motor version, for when you have built the task 01 driver. Same shape,
// different actuator: that is the whole idea of keeping respond() separate.
//
//   analogWrite(MOTOR, 200);
//   delay(60);
//   analogWrite(MOTOR, 0);

void setup() {
  pinMode(PIEZO, OUTPUT);
  logBegin("TASK 05  make it answer", "A0 -> foil pad;  D8 -> piezo -> GND");
  for (int i = 0; i < 25; i++) baseline[i] = ADCTouch.read(PAD, 300);
  logHint("Touch the pad.");
}

void loop() {
  int reading = ADCTouch.read(PAD, 300);

  if (reading > baselineAverage() * threshold) {
    if (millis() - lastFire > debounceMs) {   // debounce: one touch, one response
      lastFire = millis();
      logEvent("touch");
      respond();
    }
  } else {
    baseline[idx] = reading;
    idx = (idx + 1) % 25;
  }
  delay(20);
}

// ---- THINGS TO TRY --------------------------------------------------------
//
// 1. Set debounceMs to 0 and hold your finger on the pad. It fires continuously
//    and feels broken. Debouncing is not a detail; it is the difference between
//    an interaction and a fault.
//
// 2. Rewrite respond() so the response GROWS: a soft pulse for a quick tap, a
//    longer one if you keep your finger down. Hint: record millis() when the
//    touch starts and check how long it has lasted.
//
// 3. Build the task 01 driver and move respond() to the coin motor. The same
//    touch, answered by a buzz instead of a tick. Notice how much more the
//    motor commits to the answer, and how much slower it is to start and stop.
//    Does the mismatch feel wrong, or just unfamiliar?
//
// 4. THE REAL EXERCISE: make it say three different things. Arrived. Something
//    wrong. Finished. Vary only rhythm and strength. Then hand it to another
//    group with the screen turned away and see if they can tell them apart.
//    That is the closing brief.
