// TASK 2: MAKE SOMETHING TAP
//
// Goal: a discrete knock instead of a buzz, and a feel for why that changes
// the message.
//
// A solenoid is a coil that yanks a metal rod when you energise it. Unlike the
// motor in task 1, there is no "half a tap". It fires or it does not, so the
// only things you control are WHEN and HOW OFTEN.
//
// PINS (already wired on the table, you only upload)
//
//   D6 ---------------- MOSFET gate (logic-level, e.g. IRLZ44N)
//                       source -> GND
//                       drain  -> solenoid -> +5V on its OWN supply
//                       1N4148 across the coil, BAND to +5V
//
//   The supply GND and the Arduino GND MUST be joined, or the MOSFET never
//   sees a real gate voltage.
//   Separate supply matters: the datasheet gives 1.1 A at 5V into a 4.5 ohm
//   coil (Adafruit 2776). Off USB alone the board browns out and resets,
//   which looks exactly like a code bug and is not one. Adafruit say this
//   explicitly: "be careful of trying to power/activate from a computer's
//   USB".
//
//   Throw is 3mm at 80g of force, so it is a tap, not a punch.
//
// HEAT: a solenoid held on will cook itself. Never energise it for more than
// about 30 ms, and keep the duty cycle low. The code below does both.

const int SOLENOID = 6;

// ---- CHANGE ME ------------------------------------------------------------
int pulseMs  = 15;        // how long the coil is energised. 10-25 works.
int gapMs    = 120;       // silence between taps in a burst
int tapCount = 1;         // taps per burst
int burstGap = 2000;      // ms between bursts
// ---------------------------------------------------------------------------

void tap(int ms) {
  digitalWrite(SOLENOID, HIGH);
  delay(ms);
  digitalWrite(SOLENOID, LOW);   // always turn it off. Never leave it on.
}

void setup() {
  pinMode(SOLENOID, OUTPUT);
  digitalWrite(SOLENOID, LOW);
  Serial.begin(9600);
  Serial.println("Tapping. Try tapCount 1, then 2, then 3.");
}

void loop() {
  for (int i = 0; i < tapCount; i++) {
    tap(pulseMs);
    if (i < tapCount - 1) delay(gapMs);
  }
  delay(burstGap);
}

// ---- THINGS TO TRY --------------------------------------------------------
//
// 1. Run it with tapCount = 1. Then 2. Then 3. One tap is a notification.
//    Two is a question. Three is a demand. You did not change the strength
//    at all, only the count.
//
// 2. Set gapMs to 60, then to 300. Fast doubles read as one urgent event;
//    slow doubles read as two separate ones. Rhythm carries meaning that
//    volume cannot.
//
// 3. Put your fingertip against the plunger, then rest your whole palm on it.
//    Same pulse, different sensation. Where you place an actuator on the body
//    matters as much as how you drive it.
//
// 4. Compare with task 1 running next to it. Ask someone which one they would
//    want for "your build finished" and which for "your build failed".
