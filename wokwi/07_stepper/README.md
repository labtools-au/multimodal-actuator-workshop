# 07_stepper on Wokwi

Paste `diagram.json` and `sketch.ino` into a new Arduino Uno project at
[wokwi.com](https://wokwi.com).

This is the **most faithful** of the four simulations. Wokwi has a real stepper
part, and it takes the same four coil signals the ULN2003 board passes through
from IN1 to IN4, so D8 to D11 map straight across.

It is also the one where the simulation earns its keep: get the constructor
pin order wrong and you can watch it jitter instead of turn, without wasting a
motor or an hour at the bench.

The one difference from the bench: there is no ULN2003 in the picture, because
the driver board is a pass-through. On real hardware it sits between the Uno
and the motor, and the motor needs its own 5V.
