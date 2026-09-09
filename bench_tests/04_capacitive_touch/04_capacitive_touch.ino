// Bench 4: Capacitive touch -> servo
//
// Input is a wire. That's it. Tape it behind foil, cardboard or fabric and
// the Arduino can tell when a finger is near, with no breakout board.
//
// Distilled from an earlier student rig (capacitive_sensing_and_servos_and_
// actuators), which does this alongside four linear actuators and a browser
// control panel. Everything that is not the sensing pattern is stripped out.
//
// Library: ADCTouch by martin2250 (Library Manager -> "ADCTouch")
//
// PINS
//   A0         ->  a bare wire  ->  foil, card or fabric
//   D9          ->  servo signal
//   servo power  5V and GND, or its own supply if it stalls
//
// That really is the whole sensor: one wire, no breakout board.


#include "logger.h"

#include <ADCTouch.h>
#include <Servo.h>

const int PIN_TOUCH = A0;   // bare wire to a foil pad
const int PIN_SERVO = 9;

// --- The three numbers that actually matter -------------------------------
//
// RESOLUTION: samples per read. Higher = steadier, slower. 300 is a good start.
// BUFFER:     how many past readings form the baseline. Bigger = slower drift
//             tracking, but more immune to a hand hovering nearby.
// THRESHOLD:  multiplier on the baseline average, NOT an absolute value.
//             1.01 means "1% above normal counts as a touch."
//
// Tune THRESHOLD first. If it fires on its own, raise it. If you have to press
// hard, lower it. Expect to re-tune when you change the pad size or material.
const int   TOUCH_RESOLUTION = 300;
const int   BUFFER_SIZE      = 25;
const float THRESHOLD        = 1.01;
const unsigned long DEBOUNCE_MS = 100;

int  baselineBuffer[BUFFER_SIZE];
int  bufferIndex = 0;
unsigned long lastTouchMs = 0;

Servo servo;

// --- Rolling baseline -----------------------------------------------------
//
// THIS is the whole trick. A capacitive reading drifts with humidity, with
// mains hum, with how you're sitting. A fixed threshold works on the bench in
// the morning and fails in the afternoon. So we keep a running average of
// "untouched" and compare against that instead.
//
// Note in loop(): we only feed the buffer when NOT touched. Otherwise a long
// press slowly teaches the baseline that a finger is normal, and the touch
// silently stops registering.

int baselineAverage() {
  unsigned long total = 0;
  for (int i = 0; i < BUFFER_SIZE; i++) total += baselineBuffer[i];
  return total / BUFFER_SIZE;
}

bool isTouched(int reading) {
  return reading > baselineAverage() * THRESHOLD;
}

void setup() {
  logBegin("BENCH 04  capacitive", "A0 -> bare wire -> foil;  D9 -> servo signal");
  servo.attach(PIN_SERVO);
  servo.write(90);

  // Prime the baseline with real readings. Keep hands off the pad during
  // startup or the rig boots believing a touch is the resting state.
  for (int i = 0; i < BUFFER_SIZE; i++) {
    baselineBuffer[i] = ADCTouch.read(PIN_TOUCH, TOUCH_RESOLUTION);
  }

  logHint("Ready. Open the Serial Plotter to watch the signal.");
}

void loop() {
  int reading = ADCTouch.read(PIN_TOUCH, TOUCH_RESOLUTION);

  // Serial Plotter: raw vs. the line it has to cross. Show students this;
  // seeing the baseline drift explains the whole design in about ten seconds.
  Serial.print(reading);
  Serial.print(' ');
  Serial.println((int)(baselineAverage() * THRESHOLD));

  if (isTouched(reading)) {
    if (millis() - lastTouchMs > DEBOUNCE_MS) {
      lastTouchMs = millis();
      servo.write(150);
    }
  } else {
    baselineBuffer[bufferIndex] = reading;   // only learn while untouched
    bufferIndex = (bufferIndex + 1) % BUFFER_SIZE;
    servo.write(90);
  }
}
