# Pin map

Every station on one page, for building the room. Each sketch repeats its own
pins at the top, so a student never has to come back here.

Arduino Uno throughout. **Only D3, D5, D6, D9, D10 and D11 do PWM.** Anything
needing a variable level has to sit on one of those.

## Tasks

| Task | Pin | Goes to | Notes |
|---|---|---|---|
| 01 spin | **D9** PWM | 1k → PN2222 base | motor on collector, +5V, 1N4148 across it |
| 02 tap | **D6** | MOSFET gate | own 5V supply, grounds joined, diode across coil |
| 03 warm | **D3** PWM | H-bridge low side | bench supply, heatsink on |
| | **D5** PWM | H-bridge high side | drive one, hold the other at 0 |
| 04 sense | **A0** | bare wire → foil | that is the whole circuit |
| 05 answer | **A0** | the task 04 pad | |
| | **D9** | your actuator | or D6 for the solenoid |
| 06 phone | none | sensors.chomskylab.dk | no board at all |
| 07 turn | **D8, D9, D10, D11** | ULN2003 IN1..IN4 | plus 5V and GND |

## Bench tests

| Bench | Pin | Goes to |
|---|---|---|
| 01 ERM | **D9** PWM, **D2** button | as task 01 |
| 02 piezo | **D8** | piezo, other leg to GND |
| 03 solenoid | **D6** | MOSFET gate |
| 04 capacitive | **A0**, **D9** | pad, servo signal |
| 05 Peltier | **D3**, **D5** PWM | H-bridge |
| 06 transducer | **D11** | PAM8403 input |
| 07 stepper | **D8, D9, D10, D11** | ULN2003 IN1..IN4 |

## The two that catch people

**Stepper pin order.** Wire IN1–IN4 to D8–D11 in order, then write the
constructor **out of order**:

```cpp
Stepper motor(2048, 8, 10, 9, 11);   // IN1, IN3, IN2, IN4
```

Sequential numbering makes it buzz and jitter instead of turning, which looks
exactly like a dead motor.

**Grounds.** Anything on its own supply (solenoid, Peltier) needs that supply's
ground joined to the Arduino's, or the transistor never sees a real gate
voltage and nothing happens.

**Capacitive touch needs laptop USB.** Tasks 04 and 05 sense your body against
the board's ground, and that reference arrives through the mains earth. On a
charger or a battery the sensing goes unstable or dead with nothing visibly
wrong. If you must run it isolated, clip the Arduino GND to something the user
is touching. Never to the sense wire.

## Conflicts to avoid

D9 is used by task 01, task 05 and two bench tests, and D11 by both the
transducer and the stepper. That is fine when each station is a separate board,
but if you combine two on one Uno, move one of them. Any free PWM pin works.

Sources for every electrical figure: [bench_tests/DATASHEETS.md](bench_tests/DATASHEETS.md).
