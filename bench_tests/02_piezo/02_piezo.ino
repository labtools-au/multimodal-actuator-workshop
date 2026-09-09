// BENCH TEST 02: PIEZO
//
// Does the piezo click? Run this before the session.
//
// The lab has no DRV2605L haptic driver, so this drives a bare piezo element
// straight from a pin. That is fine: a piezo is a capacitor, it draws almost
// nothing, and it does not need a transistor the way the motor does.
//
// PINS
//   D8         ->  piezo, one leg
//   GND         ->  piezo, other leg
//
//   Drawer 6F, 69 in stock. No breakout board, no driver, no resistor.
//
// A piezo is sharp and shallow: a tick, not a thump. That contrast against
// the coin motor is the point of having both on the table.

const int PIEZO = 8;

void setup() {
  pinMode(PIEZO, OUTPUT);
  Serial.begin(9600);
  Serial.println("Piezo test. Three ticks, then a short tone, repeating.");
}

void loop() {
  // Three sharp ticks. A single edge is enough to hear a piezo click.
  for (int i = 0; i < 3; i++) {
    Serial.println("tick");
    digitalWrite(PIEZO, HIGH);
    delayMicroseconds(150);
    digitalWrite(PIEZO, LOW);
    delay(180);
  }

  delay(600);

  // A tone, to prove the same part can also make a sound rather than a click.
  Serial.println("tone 2 kHz");
  tone(PIEZO, 2000);
  delay(400);
  noTone(PIEZO);

  delay(1500);
}
