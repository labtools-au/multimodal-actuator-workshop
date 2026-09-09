# Wokwi simulations

Three tasks as runnable [Wokwi](https://wokwi.com) projects. Free, in the
browser, no install and no account needed to try one.

Two things this gives you that a schematic does not:

- **A picture, not symbols.** Wokwi draws the actual board and actual parts.
  Most of this room has never read a schematic, and a transistor triangle
  means nothing to them. A picture of a breadboard does.
- **It runs.** Same code as the bench, so a student can try task 01 before
  touching hardware, and you can link it from the slides for anyone who wants
  to prepare or who missed the session.

## Opening one

Go to [wokwi.com](https://wokwi.com), start a new Arduino Uno project, then
paste `diagram.json` and `sketch.ino` into the matching tabs. Save it to your
own account and the URL is shareable.

| Project | Simulates | Honest limits |
|---|---|---|
| [01 make it spin](01_make_it_spin) | Coin motor through a PN2222, with the flyback diode | The simulated motor just spins. It cannot show you that speed and strength are welded together, which is the point of the task. |
| [02 make it tap](02_make_it_tap) | Solenoid through a MOSFET | Wokwi has no solenoid part, so a relay coil stands in. Same driver circuit, same pins. |
| [04 make it sense](04_make_it_sense) | Touch to servo | **A button replaces the pad.** Wokwi cannot simulate capacitive sensing, so the drifting baseline (the whole lesson) only exists on hardware. |

## What this does not replace

The simulation shows the wiring and proves the logic. It cannot tell you what
anything **feels** like, which is the entire reason the workshop exists. A
simulated Peltier does not take eight seconds to convince you, and a simulated
solenoid does not read as a person tapping your finger.

Use these to arrive knowing the code compiles. Do the rest with your hands.

## Not simulated

Task 03 (Peltier) and tasks 05 and 06 are missing on purpose. Wokwi has no
thermoelectric part, no capacitive sensing, and task 06 needs a real phone.
A simulation that quietly does the wrong thing would be worse than none.
