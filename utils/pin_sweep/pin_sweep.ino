// UTIL: PIN SWEEP
//
// "Is it my code or my wiring?" This answers that in ten seconds.
//
// Walks every PWM pin in turn, driving each to full for a second. Whatever is
// connected will move, buzz, click or warm on its turn. If nothing happens on
// the pin you expected, the problem is the wiring, not your sketch.
//
// Borrowed in spirit from ktane's utils/i2c_scanner: keep one dumb diagnostic
// around so you can rule out hardware before you start reading code.
//
// Runs on a bare board with nothing attached. Safe on any of the benches
// EXCEPT bench 05: the Peltier tile should not be driven to full blind.

const int PWM_PINS[] = {3, 5, 6, 9, 10, 11};
const int PIN_COUNT = sizeof(PWM_PINS) / sizeof(PWM_PINS[0]);

// ---- CHANGE ME ------------------------------------------------------------
int level  = 255;     // drop to ~150 if full power is too violent
int holdMs = 1000;    // how long each pin stays on
// ---------------------------------------------------------------------------

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < PIN_COUNT; i++) {
    pinMode(PWM_PINS[i], OUTPUT);
    analogWrite(PWM_PINS[i], 0);
  }
  Serial.println("Pin sweep. Watch which pin makes your thing move.");
}

void loop() {
  for (int i = 0; i < PIN_COUNT; i++) {
    int pin = PWM_PINS[i];
    Serial.print("D");
    Serial.println(pin);

    analogWrite(pin, level);
    delay(holdMs);
    analogWrite(pin, 0);
    delay(300);
  }
  Serial.println("--- sweep done, repeating ---");
  delay(1000);
}
