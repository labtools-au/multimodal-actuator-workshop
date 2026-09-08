// TASK 4: MAKE IT NOTICE YOU
//
// Goal: touch input with no sensor. Just a wire.
//
// Tape a wire behind foil, card or fabric and the Arduino can tell when a
// finger is near. This is the cheapest input in the room and the one people
// are most surprised by.
//
// WIRING (bench 04)
//   A0 -> a wire -> a piece of foil. That is the entire circuit.
//
// LIBRARY: Sketch > Include Library > Manage Libraries > search "ADCTouch"

#include <ADCTouch.h>

const int PAD = A0;

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
  Serial.begin(9600);
  // Prime the baseline. Hands OFF the pad while this runs.
  for (int i = 0; i < bufferSize; i++) baseline[i] = ADCTouch.read(PAD, 300);
  Serial.println("Open Tools > Serial Plotter to watch it work.");
}

void loop() {
  int reading = ADCTouch.read(PAD, 300);
  int trigger = baselineAverage() * threshold;

  // Two lines on the plotter: what we read, and the line it must cross.
  Serial.print(reading);
  Serial.print(' ');
  Serial.println(trigger);

  if (reading > trigger) {
    // TOUCHED. Do not feed the baseline here, see note 2 below.
  } else {
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
//    to press hard. There is no correct value, only one that suits your pad,
//    your room and the day. Which is why it is relative and not a fixed number.
//
//    For what it is worth, the rig this came from went through the same thing.
//    An earlier version used 1.008 with a 50-sample baseline; the final one
//    uses 1.01 with 25, and the commit message says "reduced for
//    responsiveness". Expect to tune these. Everyone does.
//
// 4. Swap the foil for a banana, a plant, a door handle. Anything conductive
//    is an input.
