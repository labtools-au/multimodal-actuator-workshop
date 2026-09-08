// BENCH TEST 05: PELTIER
//
// Warms for 10 s, off, cools for 10 s, off. Touch the tile face to confirm
// both directions work before students arrive.
//
// Two PWM pins per channel, matching how the lab's other actuator rigs drive
// motors: one pin at speed, the other at 0, and swap them to reverse.
//
// SAFETY: heatsink on the hot face, or the tile destroys itself. MAX_LEVEL
// caps the temperature. Do not raise it. Skin burns above 50 C.

const int tileLow = 3, tileHigh = 5;
const int MAX_LEVEL = 200;

void drive(int lowPin, int highPin, int lvl) {
  analogWrite(lowPin, min(lvl, MAX_LEVEL));
  analogWrite(highPin, 0);
}

void allOff() {
  analogWrite(tileLow, 0);
  analogWrite(tileHigh, 0);
}

void setup() {
  pinMode(tileLow, OUTPUT);
  pinMode(tileHigh, OUTPUT);
  allOff();
  Serial.begin(9600);
  Serial.println("Peltier test. Feel the tile face.");
}

void loop() {
  Serial.println("WARM");
  drive(tileLow, tileHigh, 180);
  delay(10000);

  allOff();
  Serial.println("off");
  delay(4000);

  Serial.println("COOL");
  drive(tileHigh, tileLow, 180);
  delay(10000);

  allOff();
  Serial.println("off");
  delay(4000);
}
