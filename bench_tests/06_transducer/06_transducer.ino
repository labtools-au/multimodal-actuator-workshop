// BENCH TEST 06: TRANSDUCER
//
// Alternates a frequency you FEEL with one you HEAR, from the same driver.
// Confirms the amp and exciter both work before the session.
//
// If you hear nothing: amp power and volume pot.
// If you feel nothing: the exciter is not pressed firmly against the plate.
// It needs contact to couple into a surface.

const int TRANSDUCER = 11;

const int FELT_HZ  = 40;    // low enough to be vibration, not tone
const int HEARD_HZ = 400;   // clearly audible

void setup() {
  pinMode(TRANSDUCER, OUTPUT);
  Serial.begin(9600);
  Serial.println("40 Hz then 400 Hz, alternating.");
}

void loop() {
  Serial.println("40 Hz  (feel it)");
  tone(TRANSDUCER, FELT_HZ);
  delay(2000);
  noTone(TRANSDUCER);
  delay(500);

  Serial.println("400 Hz (hear it)");
  tone(TRANSDUCER, HEARD_HZ);
  delay(2000);
  noTone(TRANSDUCER);
  delay(1500);
}
