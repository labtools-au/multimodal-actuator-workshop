// TASK 3: MAKE SOMETHING WARM
//
// Goal: drive a Peltier tile both directions, and find out how slow your own
// skin actually is.
//
// A Peltier moves heat from one face to the other. Reverse the current and it
// reverses. An H-bridge is what lets you flip that current from code.
//
//
// PINS  build this before you upload
//
//   D3  PWM ---- channel LOW side  \
//                                    both to the H-bridge, tile across it
//   D5  PWM ---- channel HIGH side /
//
//   Drive one and hold the other at 0 to choose direction. Both 0 is off.
//   Tile runs from a BENCH supply, not the Arduino: it wants 2 to 4 A.
//   Heatsink on the hot face, always.
//
//   Two PWM pins per channel is the same pattern the lab's other actuator
//   rigs use, so it will look familiar if you read that code.
//
// SAFETY, NOT OPTIONAL
//   * The heatsink must be on. Without it the tile cooks itself in a minute.
//   * Skin burns above 50 C. MAX_LEVEL below caps roughly at 45 C on this
//     rig. Do not raise it.
//   * Never leave it running unattended.

#include "logger.h"

const int tileLow = 3, tileHigh = 5;   // both must be PWM pins

// ---- CHANGE ME ------------------------------------------------------------
int level    = 180;       // 0-255. LEAVE AT OR BELOW MAX_LEVEL.
int holdMs   = 8000;      // how long to hold each direction
// ---------------------------------------------------------------------------

const int MAX_LEVEL = 200;   // do not raise. Thermal limit, not a style choice.

void warm(int lvl) {
  analogWrite(tileLow, min(lvl, MAX_LEVEL));
  analogWrite(tileHigh, 0);
}

void cool(int lvl) {
  analogWrite(tileLow, 0);
  analogWrite(tileHigh, min(lvl, MAX_LEVEL));
}

void off() {
  analogWrite(tileLow, 0);
  analogWrite(tileHigh, 0);   // both off, or the tile keeps working
}

void setup() {
  pinMode(tileLow, OUTPUT); pinMode(tileHigh, OUTPUT);
  off();
  logBegin("TASK 03  make it warm", "D3, D5 PWM -> H-bridge;  tile on the BENCH supply");
  logHint("Finger on the tile. Say out loud when you are SURE.");
}

void loop() {
  logEvent("WARM");
  warm(level); delay(holdMs);

  off(); delay(3000);          // let it settle, or you feel the old state

  logEvent("COOL");
  cool(level); delay(holdMs);

  off(); delay(3000);
}

// ---- THINGS TO TRY --------------------------------------------------------
//
// 1. Watch the Serial Monitor and time yourself. From the moment it prints
//    WARM, how many seconds until you would BET MONEY it is warming? Most
//    people need 3 to 8. That is enormous compared to a motor's 20 ms.
//
// 2. Cut holdMs to 2000 so it alternates quickly. You stop feeling hot and
//    cold and start feeling lukewarm. Thermal patterns mostly do not work.
//
// 3. Given 1 and 2: what could thermal actually be good for in your project?
//    Slow ambient state, not alerts. "The room is busy" rather than
//    "you have a message".
