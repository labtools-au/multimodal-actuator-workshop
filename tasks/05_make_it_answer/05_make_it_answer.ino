// TASK 5: MAKE IT ANSWER BACK
//
// Goal: input drives output. This is the smallest complete interaction, and
// it is the template for most of what you will build in the project weeks.
//
// Everything before this was one half. Task 4 sensed, tasks 1 to 3 acted.
// Here they are wired together: touch the pad, feel a response.
//
// WIRING: the task 04 pad on A0, plus any actuator you like on its own pin.
// The respond() function is deliberately the only thing you need to swap.

#include <ADCTouch.h>

const int PAD   = A0;
const int MOTOR = 9;     // or the solenoid on D6, your choice

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
  analogWrite(MOTOR, 200);
  delay(60);
  analogWrite(MOTOR, 0);
}

void setup() {
  pinMode(MOTOR, OUTPUT);
  Serial.begin(9600);
  for (int i = 0; i < 25; i++) baseline[i] = ADCTouch.read(PAD, 300);
  Serial.println("Touch the pad.");
}

void loop() {
  int reading = ADCTouch.read(PAD, 300);

  if (reading > baselineAverage() * threshold) {
    if (millis() - lastFire > debounceMs) {   // debounce: one touch, one response
      lastFire = millis();
      Serial.println("touch");
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
// 3. Make it answer with a DIFFERENT actuator than the one you expected. Touch
//    that produces warmth, or a knock. Does the mismatch feel wrong, or just
//    unfamiliar?
//
// 4. THE REAL EXERCISE: make it say three different things. Arrived. Something
//    wrong. Finished. Vary only rhythm and strength. Then hand it to another
//    group with the screen turned away and see if they can tell them apart.
//    That is the closing brief.
