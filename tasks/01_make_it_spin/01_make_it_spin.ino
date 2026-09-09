// TASK 1: MAKE SOMETHING SPIN
//
// Goal: a motor you control from code, in under five minutes.
//
// Upload this. The motor pulses. Then change the two numbers marked CHANGE ME
// and upload again. That loop, edit and re-upload, is the whole workshop.
//
// PINS (already wired on the table, you only upload)
//
//   D9  PWM ---[ 1k ]--- PN2222 base
//                        emitter -> GND
//                        collector -> motor -> +5V
//                        1N4148 across the motor, BAND to +5V
//
//   Only pins 3, 5, 6, 9, 10 and 11 can do PWM on an Uno. The motor needs
//   one of those, because analogWrite on any other pin only gives on/off.
//
// WHY NOT STRAIGHT TO THE PIN: an Arduino pin gives 40 mA. This motor draws
// 100 mA at 5V (80 mA at 4V, 60 mA at 3V, per the Adafruit 1201 datasheet).
// The transistor lets a small pin current switch a bigger one. Adafruit
// suggest a PN2222 for full control; a 2N2222 behaves the same here.
//
// Rated 2.5 to 3.8V, but it will run from 2V to 5V. Higher voltage means
// more current AND a stronger buzz, which is the compromise this task is
// about. 11000 RPM at 5V.

#include "logger.h"

const int MOTOR = 9;      // must be a PWM pin: 3, 5, 6, 9, 10, 11

// ---- CHANGE ME ------------------------------------------------------------
int strength = 200;       // 0-255. How hard it buzzes.
int onTime   = 150;       // ms the motor runs
int offTime  = 850;       // ms of silence between buzzes
// ---------------------------------------------------------------------------

void setup() {
  pinMode(MOTOR, OUTPUT);
  logBegin("TASK 01  make it spin", "D9 PWM -> 1k -> PN2222 base -> motor");
  logHint("Edit strength / onTime / offTime, then upload again.");
}

void loop() {
  analogWrite(MOTOR, strength);   // on
  delay(onTime);
  analogWrite(MOTOR, 0);          // off
  delay(offTime);
}

// ---- THINGS TO TRY --------------------------------------------------------
//
// 1. Drop `strength` to 80. Does it still move? Most coin motors stall
//    somewhere around 90 because they cannot overcome their own friction.
//    Find YOUR motor's floor. Write it down, you will need it later.
//
// 2. Set onTime to 40 and offTime to 60. Now it is a texture, not an event.
//    Somewhere between 60 ms and 400 ms it stops feeling like a buzz and
//    starts feeling like a pulse. Where is that line for you?
//
// 3. Try strength 255 with onTime 800. Is it more urgent, or just annoying?
//    Urgency comes mostly from RATE, not power. Worth knowing before you
//    design an alert.
//
// 4. Harder: make it ramp. Replace loop() with a for-loop that walks
//    `strength` from 0 to 255 in steps of 5 with a delay(20) between each.
//    A motor that eases in reads as deliberate; one that slams on reads as
//    a fault.
