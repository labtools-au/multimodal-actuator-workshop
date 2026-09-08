# Utils

Diagnostics. Not part of the session, but the things that save it when a bench
misbehaves at 9am.

The habit is borrowed from `ktane/utils/`: keep a dumb, dependency-free
diagnostic around so you can rule out the hardware before you start reading your
own code.

| Sketch | Answers |
|---|---|
| [`pin_sweep`](pin_sweep) | "Is anything on this pin at all?" Drives every PWM pin in turn |
| [`i2c_scanner`](i2c_scanner) | "Can the board see the chip?" Bench 02 should show 0x5A |
| [`analog_monitor`](analog_monitor) | "What range does this sensor really give?" Plots one analogue pin |

Do not run `pin_sweep` on bench 05. The Peltier should not be driven blind.
