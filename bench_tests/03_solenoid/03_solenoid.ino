// BENCH TEST 03 — SOLENOID
//
// One tap every two seconds. If it does not click, check in this order:
//   1. bench supply on, and sharing ground with the Arduino
//   2. MOSFET gate on D6
//   3. flyback diode across the coil, striped end to +V
//
// If the board RESETS when it fires, the solenoid is drawing from USB. It
// needs its own supply. That reset looks exactly like a software crash and
// is not one.

const int SOLENOID = 6;
const int PULSE_MS = 15;    // never raise this much. The coil heats fast.

void setup() {
  pinMode(SOLENOID, OUTPUT);
  digitalWrite(SOLENOID, LOW);
  Serial.begin(9600);
  Serial.println("Tapping once every 2 s.");
}

void loop() {
  digitalWrite(SOLENOID, HIGH);
  delay(PULSE_MS);
  digitalWrite(SOLENOID, LOW);   // ALWAYS turn it off
  Serial.println("tap");
  delay(2000);                   // long gap keeps the duty cycle low
}
