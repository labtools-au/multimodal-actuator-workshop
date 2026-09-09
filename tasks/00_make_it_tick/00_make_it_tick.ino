// TASK 0: MAKE IT TICK
//
// Goal: your first circuit, in two wires, with nothing that can go wrong.
//
// Start here. Not because it is impressive, but because when it works you
// know your board, your cable, your port and the IDE are all fine. Every
// failure after this one is in the circuit you built, which is a much
// smaller thing to search.
//
// PINS  build this before you upload
//
//   D8 ---- piezo, one leg
//   GND --- piezo, other leg
//
//   That is the whole circuit. Two wires and no polarity, so it cannot be
//   the wrong way round.
//
// WHY NO TRANSISTOR: a piezo is a capacitor. It draws almost no current, so
// a pin can drive it directly. Compare with task 01, where the motor draws
// 100 mA and a pin only gives 40 mA. That difference is the reason every
// other output in this room needs a driver circuit and this one does not.
//
// A piezo is sharp and shallow. A tick, not a thump. Hold it against the
// table and it gets much louder, because the table becomes the diaphragm.

#include "logger.h"

const int PIEZO = 8;

// ---- CHANGE ME ------------------------------------------------------------
int tickCount   = 3;      // how many ticks in a burst
int gapMs       = 180;    // time between ticks. This is the RHYTHM
int toneHz      = 2000;   // pitch of the tone at the end
// ---------------------------------------------------------------------------

void tick() {
  // A single edge is enough. The piezo snaps once and that is the click.
  digitalWrite(PIEZO, HIGH);
  delayMicroseconds(150);
  digitalWrite(PIEZO, LOW);
}

void setup() {
  pinMode(PIEZO, OUTPUT);
  logBegin("TASK 00  make it tick", "D8 -> piezo -> GND");
  logHint("Change tickCount and gapMs, then upload again.");
}

void loop() {
  for (int i = 0; i < tickCount; i++) {
    logEvent("tick");
    tick();
    delay(gapMs);
  }

  delay(600);

  logEvent("tone");
  tone(PIEZO, toneHz);
  delay(400);
  noTone(PIEZO);

  delay(1500);
}

// ---- THINGS TO TRY --------------------------------------------------------
//
// 1. Set gapMs to 60, then to 400. Same number of ticks, same loudness, and
//    yet one reads as urgent and the other as patient. You have changed
//    nothing but rhythm, and rhythm is doing all the work.
//
// 2. Hold the piezo against the table, then hold it in the air. Same signal,
//    very different loudness. What a thing is touching is part of the output.
//    The surface transducer at the front is this effect taken seriously.
//
// 3. Set toneHz to 400, then 4000. Piezos have a resonant frequency, usually
//    somewhere near 4 kHz, where they are much louder for the same drive.
//    Find the pitch where yours is loudest. That is not the pitch you chose,
//    it is the one the part prefers.
//
// 4. THE ONE THAT MATTERS: make three bursts that mean different things.
//    Arrived, something wrong, finished. You have only tickCount, gapMs and
//    toneHz. Then go and do the same brief on a coin motor in task 01 and
//    notice which messages survive the change of actuator and which do not.
