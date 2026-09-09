// TASK 7: MAKE IT TURN
//
// Goal: an actuator that goes to a POSITION, not just on and off.
//
// Everything else in this room is a state: buzzing or still, hot or cold.
// A stepper is different. You ask for 512 steps and you get exactly a quarter
// turn, every time, with no sensor telling it where it is. That precision is
// why steppers are in printers, scanners and camera rigs.
//
// PINS  build this before you upload
//
//   ULN2003 board            Uno
//     IN1        ---------->  D8
//     IN2        ---------->  D9
//     IN3        ---------->  D10
//     IN4        ---------->  D11
//     5V  (+)    ---------->  5V
//     GND (-)    ---------->  GND
//
//   The motor plugs into the white socket on the driver board, one way round.
//   Six wires, no transistor, no diode, nothing you can destroy. The hard
//   part of this task is not the wiring.
//
//   The motor's own five wires, if you ever need them: blue, pink, yellow and
//   orange are the four coils, red is the common. They are already in the
//   right order inside the plug, so you never separate them.
//
// THE POWER HEADER, WHICH IS FOUR PINS AND NOT TWO
//
//     -    +    [ JP ]
//     |    |     \__ jumper bridges the two inner pins
//     |    +------->  Uno 5V
//     +------------>  Uno GND
//
//   The negative is on the OUTSIDE edge. The silkscreen reads minus then
//   plus, which is the opposite of what most people assume.
//
//   That small black jumper is labelled MOTOR ON/OFF. It gates power to the
//   LEDs and the motor. Knock it off and you get no LEDs and no movement,
//   while the logic side keeps working perfectly, so everything you can
//   measure looks fine. This is the most common reason one of these boards
//   appears dead.
//
// THE TRAP, AND IT IS A GOOD ONE
//   You wired IN1..IN4 to D8..D11 in order. The library does NOT want them in
//   that order. It wants IN1, IN3, IN2, IN4, which reads 8, 10, 9, 11.
//
//   Get it wrong and the motor buzzes and shakes without turning. It looks
//   exactly like a dead motor or a bad supply, which is why people spend an
//   hour on the wiring when the bug is one line of code.
//
//   Worth trying deliberately: change it to (2048, 8, 9, 10, 11), upload,
//   listen, then change it back. Knowing what that failure SOUNDS like is
//   worth more than being told about it.
//
// IF NOTHING HAPPENS AT ALL, in this order:
//
//   0. HOW MANY LEDs LIGHT? This splits the problem in one look.
//        two at a time, chasing  -> signals fine, it is a power problem
//        exactly one, ever       -> only one jumper is landing. The other
//                                   three are in the wrong holes or loose
//        none at all             -> the board is unpowered, go to step 1
//
//      Two is correct: the Stepper library energises two coils per step
//      (1010, 0110, 0101, 1001), so two LEDs are lit at every moment. One
//      lonely LED is always a wiring fault and never a power fault, because
//      weak power dims all four together rather than leaving one.
//
//      utils/pin_debug drives D8..D11 one at a time so you can see exactly
//      which jumpers land and which do nothing.
//
//   1. Is the JP jumper fitted, across BOTH inner pins? Most likely cause.
//   2. Are + and - swapped? Negative is the outside pin.
//   3. Is the board's - actually on the Uno's GND? Without a shared ground
//      the driver has no reference and never switches.
//   4. Unplug the motor and jumper any IN pin straight to the board's own -
//      terminal. That LED should light, with the Arduino out of the loop.
//      It lights: board is fine, the fault is between Uno and driver.
//      It stays dark: the board or its power.
//   5. Only then suspect the Arduino. utils/pin_debug drives D8..D11 one at a
//      time and reads each back, so it tells you whether the pins are really
//      going high.
//
//   Worth knowing WHY step 4 works: the LEDs sit on the output side, anode to
//   VCC through a resistor, cathode to the driver output. The ULN2003 only
//   sinks current, never sources it. So a lit LED proves three things at once:
//   power present, jumper fitted, and that channel actually switching. And no
//   LEDs with known-good input signals means an unpowered board rather than a
//   broken one.
//
// POWER: GIVE THE DRIVER ITS OWN SUPPLY. Do not run it from the Uno's 5V pin.
//
//   Each coil pulls roughly 240 mA and the ULN2003 holds coils energised
//   continuously, including when the motor is standing still. That is far more
//   than a laptop USB port wants to give through an Arduino. Measured on the
//   bench: the LEDs lit correctly and the motor never moved, and then the Mac
//   cut the port entirely and the board disappeared from /dev. Unplugging and
//   reconnecting the USB cable resets that.
//
//   So:
//     driver +  ->  external 5V (YwRobot breadboard supply, drawer 8A)
//     driver -  ->  that supply's GND
//     driver -  ->  ALSO the Uno's GND, or the inputs have no reference
//     IN1..IN4  ->  D8..D11 as before
//
//   The Uno then carries signals only, and the coil current never crosses it.
//
//   THE SYMPTOM TO RECOGNISE: LEDs light in sequence but the shaft does not
//   move. The LEDs need a few mA and the coils need hundreds, so a supply that
//   is too weak lights one and not the other. That is not a broken motor.
//
//   The motor also gets warm sitting still, because the coils stay energised.
//   That is this driver being normal, not a fault.

#include "logger.h"

#include <Stepper.h>

// 28BYJ-48: 32 steps per motor turn through a 1/64 gearbox, so 2048 steps
// per turn of the output shaft.
const int STEPS_PER_REV = 2048;

// IN1, IN3, IN2, IN4. Read the trap above before you change this.
Stepper motor(STEPS_PER_REV, 8, 10, 9, 11);

// ---- CHANGE ME ------------------------------------------------------------
int stepsToMove = 512;    // 2048 = a full turn. 512 = a quarter
int speedRpm    = 10;     // this motor stalls somewhere above 15
int pauseMs     = 800;    // stillness between moves is part of the signal
// ---------------------------------------------------------------------------

void setup() {
  logBegin("TASK 07  make it turn", "ULN2003 IN1->D8 IN2->D9 IN3->D10 IN4->D11");
  logHint("LEDs light but shaft still? NOT a dead motor. Not enough current.");
  logHint("Give the driver its own 5V, and join its GND to the Arduino's.");
  logHint("Buzzing and jittering instead? Then it IS the pin order in code.");
  motor.setSpeed(speedRpm);
}

void loop() {
  logValue("steps", stepsToMove);
  motor.step(stepsToMove);
  delay(pauseMs);

  logValue("steps", -stepsToMove);
  motor.step(-stepsToMove);
  delay(pauseMs);
}

// ---- THINGS TO TRY --------------------------------------------------------
//
// 1. Set stepsToMove to 2048 and watch a full turn. Then 2048 again, and
//    again. It ends up exactly where it started every time, with nothing
//    measuring the position. Compare with the coin motor, where "how far did
//    it go" is not even a question you can ask.
//
// 2. Set speedRpm to 25. It stalls, buzzes, and loses steps, and now the
//    position is wrong with no error and no way for the code to know. Open
//    loop control means the motor cannot tell you it failed. This is the real
//    limitation of steppers, and it is the reason printers home themselves
//    against a switch before they start.
//
// 3. Set stepsToMove to 20 and pauseMs to 60. Small nudges instead of sweeps.
//    A stepper is perfectly good at being a haptic device: you feel the
//    detents through whatever it is mounted to. Hold the body of the motor
//    while it runs.
//
// 4. THE ONE THAT MATTERS: do the closing brief with this instead of a buzzer.
//    Arrived, something wrong, finished, using only distance, speed and
//    pauses. You have a richer vocabulary here than a piezo has, because
//    direction means something. Does "it turned back" read as undo, or as
//    refusal? Ask someone who has not seen your code.
