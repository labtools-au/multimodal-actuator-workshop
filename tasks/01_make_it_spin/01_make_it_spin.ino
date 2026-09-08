// TASK 1: MAKE SOMETHING SPIN
//
// Goal: a motor you control from code, in under five minutes.
//
// Upload this. The motor pulses. Then change the two numbers marked CHANGE ME
// and upload again. That loop, edit and re-upload, is the whole workshop.
//
// WIRING (bench 01)
//   D9 -> 1k resistor -> transistor base
//   motor between transistor collector and +5V
//   diode across the motor, striped end to +5V
//   Already wired at the bench. You only upload.
//
// WHY NOT STRAIGHT TO THE PIN: an Arduino pin gives 40 mA. This motor wants
// about 75 mA. The transistor lets a small pin current switch a bigger one.

const int MOTOR = 9;      // must be a PWM pin: 3, 5, 6, 9, 10, 11

// ---- CHANGE ME ------------------------------------------------------------
int strength = 200;       // 0-255. How hard it buzzes.
int onTime   = 150;       // ms the motor runs
int offTime  = 850;       // ms of silence between buzzes
// ---------------------------------------------------------------------------

void setup() {
  pinMode(MOTOR, OUTPUT);
  Serial.begin(9600);
  Serial.println("Spinning. Edit strength/onTime/offTime and re-upload.");
}

void loop() {
  analogWrite(MOTOR, strength);   // on
  delay(onTime);
  analogWrite(MOTOR, 0);          // off
  delay(offTime);
}

// ---- THINGS TO TRY --------------------------------------------------------
//
// 1. Drop `strength` to 80. Does it still move? Most coin motors stall
//    somewhere around 90 because they cannot overcome their own friction.
//    Find YOUR motor's floor. Write it down, you will need it later.
//
// 2. Set onTime to 40 and offTime to 60. Now it is a texture, not an event.
//    Somewhere between 60 ms and 400 ms it stops feeling like a buzz and
//    starts feeling like a pulse. Where is that line for you?
//
// 3. Try strength 255 with onTime 800. Is it more urgent, or just annoying?
//    Urgency comes mostly from RATE, not power. Worth knowing before you
//    design an alert.
//
// 4. Harder: make it ramp. Replace loop() with a for-loop that walks
//    `strength` from 0 to 255 in steps of 5 with a delay(20) between each.
//    A motor that eases in reads as deliberate; one that slams on reads as
//    a fault.
