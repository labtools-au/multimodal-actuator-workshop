// TASK 3 — MAKE SOMETHING WARM
//
// Goal: drive a Peltier tile both directions, and find out how slow your own
// skin actually is.
//
// A Peltier moves heat from one face to the other. Reverse the current and it
// reverses. That is what the H-bridge is for: two pins decide direction, one
// PWM pin decides how hard.
//
// WIRING (bench 05)
//   D3  -> ENA (speed)      D4, D5 -> IN1, IN2 (direction)
//   Tile on a bench supply, heatsink glued to the hot face.
//
// SAFETY, NOT OPTIONAL
//   * The heatsink must be on. Without it the tile cooks itself in a minute.
//   * Skin burns above 50 C. MAX_LEVEL below caps roughly at 45 C on this
//     rig. Do not raise it.
//   * Never leave it running unattended.

const int ENA = 3, IN1 = 4, IN2 = 5;

// ---- CHANGE ME ------------------------------------------------------------
int level    = 180;       // 0-255. LEAVE AT OR BELOW MAX_LEVEL.
int holdMs   = 8000;      // how long to hold each direction
// ---------------------------------------------------------------------------

const int MAX_LEVEL = 200;   // do not raise. Thermal limit, not a style choice.

void warm(int lvl) {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  analogWrite(ENA, min(lvl, MAX_LEVEL));
}

void cool(int lvl) {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  analogWrite(ENA, min(lvl, MAX_LEVEL));
}

void off() { analogWrite(ENA, 0); }

void setup() {
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  off();
  Serial.begin(9600);
  Serial.println("Finger on the tile. Say out loud when you are SURE.");
}

void loop() {
  Serial.println("WARM");
  warm(level); delay(holdMs);

  off(); delay(3000);          // let it settle, or you feel the old state

  Serial.println("COOL");
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
