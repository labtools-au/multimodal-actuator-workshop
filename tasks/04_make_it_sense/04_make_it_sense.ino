// TASK 4: MAKE IT NOTICE YOU
//
// Goal: touch input with no sensor. Just a wire.
//
// Tape a wire behind foil, card or fabric and the Arduino can tell when a
// finger is near. This is the cheapest input in the room and the one people
// are most surprised by.
//
// PINS  build this before you upload
//
//   A0 ---- a bare wire ---- foil, card or fabric
//
//   That is the entire circuit. ONE wire. No breakout board, no resistor,
//   and no ground connection to the pad. Any analogue pin works; A0 is just
//   convention.
//
//   Output is the LED already on the board, next to pin 13. Nothing to wire
//   for it, so if the LED follows your finger, the sensing works and nothing
//   else can be blamed.
//
// KEEP IT ON USB. Capacitive sensing measures your body against the board's
// ground, and on a laptop that reference comes through the mains earth. Run
// the Uno from an isolated supply instead (a phone charger, a battery, a
// bench PSU) and the shared reference disappears: readings go unstable or
// stop responding altogether, with nothing visibly wrong. Verified on the
// bench. If it worked and then stopped, check what is powering the board
// before you touch the code.
//
//   IF YOU MUST run it off USB power, a charger or a battery: give it back a
//   reference by hand. An alligator clip from the Arduino's GND to something
//   you are touching (foil under your wrist, a metal chair frame, a metal
//   enclosure) puts you and the board on the same ground again and the
//   sensing returns.
//
//   Two rules for that clip. Do NOT clip GND to the sense wire, that shorts
//   out the thing you are measuring. And do not reach for mains earth while
//   the board floats on its own supply; keep it to a local object.
//
//   This is also why commercial capacitive panels tend to live in metal
//   housings. The housing is doing this job for free.
//
// LIBRARY: Sketch > Include Library > Manage Libraries > search "ADCTouch"

#include "logger.h"

#include <ADCTouch.h>

const int PAD = A0;
const int LED = LED_BUILTIN;   // the one already on the board, no wiring

// ---- CHANGE ME ------------------------------------------------------------
float threshold = 1.01;   // 1.01 = "1% above normal counts as a touch"
int   bufferSize = 25;    // how many past readings form the baseline.
                          // Max 50, see the array below.
// ---------------------------------------------------------------------------

int baseline[50];         // fixed size: bufferSize must stay <= 50
int idx = 0;

int baselineAverage() {
  long total = 0;
  for (int i = 0; i < bufferSize; i++) total += baseline[i];
  return total / bufferSize;
}

void setup() {
  pinMode(LED, OUTPUT);
  logBegin("TASK 04  make it sense", "A0 -> bare wire -> foil pad");
  // Prime the baseline. Hands OFF the pad while this runs.
  for (int i = 0; i < bufferSize; i++) baseline[i] = ADCTouch.read(PAD, 300);
  logHint("Touch the pad: the LED by pin 13 lights.");
  logHint("Then open Tools > Serial Plotter to see WHY.");
}

void loop() {
  int reading = ADCTouch.read(PAD, 300);
  int trigger = baselineAverage() * threshold;

  // Two lines on the plotter: what we read, and the line it must cross.
  Serial.print(reading);
  Serial.print(' ');
  Serial.println(trigger);

  if (reading > trigger) {
    digitalWrite(LED, HIGH);
    // TOUCHED. Do not feed the baseline here, see note 2 below.
  } else {
    digitalWrite(LED, LOW);
    baseline[idx] = reading;
    idx = (idx + 1) % bufferSize;
  }
  delay(20);
}

// ---- THINGS TO TRY --------------------------------------------------------
//
// 1. Open the Serial Plotter and move your hand slowly toward the pad. You can
//    see it react BEFORE you make contact. Capacitive sensing detects
//    proximity, not touch; "touch" is just a threshold you chose.
//
// 2. THE IMPORTANT ONE. Notice the baseline only updates while untouched.
//    Move that line into the touched branch instead and hold your finger down:
//    within a couple of seconds the touch stops registering, because you have
//    taught the baseline that a finger is normal. Put it back.
//
// 3. Set threshold to 1.001. It fires at nothing. Set it to 1.2 and you have
//    to press hard. Do not go far the other way either: much above about 1.02
//    on a bare wire and the baseline stops being refreshed often enough, so it
//    goes stale and the whole thing drifts out of range. Measured on an Uno
//    with a bare jumper: 1.01 sat about 5 counts below the line, 1.03 lost the
//    baseline entirely. There is no correct value, only one that suits your pad,
//    your room and the day. Which is why it is relative and not a fixed number.
//
//    For what it is worth, the rig this came from went through the same thing.
//    An earlier version used 1.008 with a 50-sample baseline; the final one
//    uses 1.01 with 25, and the commit message says "reduced for
//    responsiveness". Expect to tune these. Everyone does.
//
// 4. Swap the foil for a banana, a plant, a door handle. Anything conductive
//    is an input.
//
// 5. Size matters more than you expect. A bare jumper end works but sits close
//    to the threshold; tape it to a palm-sized piece of foil and the signal
//    gets much bigger, because you have built a bigger capacitor plate. If
//    yours is twitchy, make the pad bigger before you touch the numbers.
