// Bench 1: ERM coin motor, and the closing brief
//
// An off-centre weight on a motor shaft. Same part as in your phone.
//
// The core limitation, made physical: speed and strength are mechanically
// linked. You cannot ask for "gentle but fast", because spinning it faster to
// raise the rate also makes it stronger. Everything below works around that
// limit rather than pretending it is not there.
//
// WIRING: never drive the motor from a bare pin. 40 mA limit, the motor pulls
// ~75 mA. Pin D9 -> 1k -> 2N2222 base; motor across collector and +5V with a
// 1N4148 across it (band to +5V) to catch the flyback spike.

const int PIN_MOTOR = 9;      // must be PWM
const int PIN_BUTTON = 2;

// --- The two parameters you get ---------------------------------------------
//
// Two parameters, and only two:
//   STRENGTH = PWM duty. How strong each pulse feels.
//   RHYTHM    = the pattern of on/off durations.
//
// The brief asks for three distinguishable messages using only these. Resist
// adding a second actuator: the constraint is the exercise.

void pulse(int strength, int ms) {
  analogWrite(PIN_MOTOR, strength);
  delay(ms);
  analogWrite(PIN_MOTOR, 0);
}

// Below ~90 the motor often won't overcome its own friction and just buzzes
// weakly or stalls. Find your own floor; it varies per motor.
const int SOFT = 130;
const int HARD = 255;

// One soft tap. Deliberately unremarkable: routine news should feel routine.
void messageArrived() {
  pulse(SOFT, 60);
}

// Three hard, fast pulses. Urgency comes from RATE, not just strength.
// this is the pattern people reliably rank as most alarming.
void somethingWrong() {
  for (int i = 0; i < 3; i++) {
    pulse(HARD, 90);
    delay(70);
  }
}

// Rising: short and soft, then long and strong. Reads as resolution, and is
// hard to confuse with the other two because the SHAPE differs, not the level.
void taskFinished() {
  pulse(SOFT, 40);
  delay(60);
  pulse(220, 220);
}

void setup() {
  pinMode(PIN_MOTOR, OUTPUT);
  pinMode(PIN_BUTTON, INPUT_PULLUP);
  Serial.begin(9600);
  Serial.println(F("1 = arrived  2 = wrong  3 = finished"));
}

void loop() {
  // Serial trigger, so the receiver can be handed the device with the screen
  // turned away. The blind test only works if they cannot see which message
  // you sent.
  if (Serial.available()) {
    switch (Serial.read()) {
      case '1': messageArrived();  break;
      case '2': somethingWrong();  break;
      case '3': taskFinished();    break;
    }
  }
}
