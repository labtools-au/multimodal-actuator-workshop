# Build sheet

What to do, in order, to get from an empty table to a working session. Written
to be followed with parts in your hands.

Nothing here has been built or flashed yet, so treat the first pass as
discovery. Budget an evening, not an hour.

---

## Before you start: shopping

Five things are not in the component database and have to come from somewhere
else. Everything else is in the drawers.

**Quantities assume students build their own circuits**, two or three each.
That makes transistors and diodes consumables rather than fixtures, and some
will be destroyed. Buy accordingly.

- [ ] **Breadboards**, one per student plus four spares. Half-size is fine.
- [ ] **Jumper wires**, male-male and male-female. Buy far more than you think:
      a student building from scratch uses six to ten per circuit.
- [ ] **Resistors**: a mixed kit, but you specifically need 1k and 220R. Get
      at least 40 of the 1k, since every motor circuit uses one.
- [ ] **Transistors**: PN2222 or 2N2222 (small NPN), **at least 40**, and
      IRLZ44N or another logic-level MOSFET, at least 15. Expect to lose some
      to reversed diodes.
- [ ] **Diodes**: 1N4148 or 1N4001, **at least 40**. **Not optional.** Every
      motor, solenoid and electromagnet needs one across it or the transistor
      dies. This is the single most common destructive mistake, so have spares
      within arm's reach during the session.

Two things to check rather than buy:

- [ ] **A bench supply for the Peltier.** It wants 2 to 4 A. The database
      lists one Wanptek TPS305 at OB3 showing 0 available, so find out whether
      that is a tracking artefact or genuinely gone.
- [ ] **Heatsink and thermal paste** for the Peltier. Safety-critical.

---

## Step 1: pull the parts

All confirmed in stock on 9 September 2026. Re-check anything you depend on.

One board per student, and enough actuators that everyone can build the
first three tasks at the same time. **The 14 Unos set your class size**: past
that, students pair up.

| Drawer | Part | Take |
|---|---|---|
| **5A** | Arduino Uno | 14, one each |
| **1E** | Vibrating Mini Motor Disc | 16 |
| **6F** | Piezo Element | 20, everyone starts here |
| **3E** | Mini Push-Pull Solenoid 5V | 6 |
| **4C** | Peltier element / Cooling Pad | 4 |
| **7F** | Surface Transducer | 4 |
| **8A** | YwRobot breadboard supply | 14 |
| **2C** | L9110S H-bridge | 6 |
| **11F** | PAM8403 amplifier | 4 |
| **2A** | Stepper 28BYJ-48 + ULN2003 | 4 of each |
| **4A** | FSR | 8 |
| **4B** | Flex sensor | 4 |
| **9D** | Pulse sensor | 4 |
| **0C5** | GSR sensor | **1, the only one in the lab** |

There is a request script at `scripts/request_components.py` if you want
these to go through the app rather than being taken off the shelf.

---

## Step 2: install the libraries, once

Arduino IDE, Library Manager:

- [ ] **ADCTouch** by martin2250 (tasks 04 and 05)
- [ ] **Servo** and **Stepper** ship with the IDE, nothing to do

Nothing else is needed. Bench 02 drives the piezo straight from a pin.

---

## Step 3: build one station at a time, and test it

**Students build their own circuits on the day.** These bench tests are for
you, beforehand: one working example of each circuit, so that when a student
is stuck you can put a known-good build next to theirs and compare. Keep them
assembled and bring them.

Do these in order. Each one proves a single component before you combine
anything.

Flash from `bench_tests/<name>/`, watch the Serial Monitor at 9600 baud.

Every sketch prints the same way, because they all share `logger.h`. On reset
you get a banner naming the sketch and its pins:

```
========================================
  BENCH 02  piezo
  pins: D8 -> piezo, other leg -> GND
========================================
1483 ms  tick
```

That banner is the fastest check that you uploaded the sketch you think you
did, to the board you think you did. Lines starting `>>>` are instructions to
act on. Everything else is timestamped, so you can read a rhythm off the
screen when you cannot hear it clearly.

`logger.h` is copied into each sketch folder rather than installed as a
library. The IDE compiles every file next to the `.ino`, so there is nothing
to set up. Edit `bench_tests/01_erm_motor/logger.h` and re-run
`scripts/sync_logger.py` to push the change to all fifteen.

### 02 piezo: start here, it proves the toolchain

Two wires and no driver, so nothing between the pin and the part can be
wrong. Do this one first: if it works, your board, cable, port and IDE are
all good, and any later failure is in the driver circuit rather than the
setup.

```
D8 -> piezo, one leg;  GND -> piezo, other leg
```

- [ ] Three audible ticks, then a short tone, repeating
- No transistor, no resistor. A piezo draws almost nothing
- Serial at 9600 prints `tick` and `tone 2 kHz`, which separates "not running"
  from "running but I cannot hear it"
- A bare disc is quiet. Press it flat against the table and it gets much
  louder, because the table becomes the diaphragm. Same effect as bench 06

### 01 motor: the template every driver circuit copies

```
D9 --[ 1k ]-- PN2222 base
              emitter -> GND
              collector -> motor -> +5V
              1N4148 across the motor, BAND to +5V
```

- [ ] Motor buzzes on serial input 1, 2 or 3
- Passes when the three patterns feel different from each other
- If it does nothing below PWM 90, that is the motor's stall floor, not a bug

### 07 stepper: do it early, it has the worst trap

```
ULN2003:  IN1 -> D8   IN2 -> D9   IN3 -> D10   IN4 -> D11
```

- [ ] One full turn each way, smoothly
- **If it buzzes and jitters instead of turning, the code is wrong, not the
  wiring.** The constructor takes the pins out of order:
  `Stepper(2048, 8, 10, 9, 11)`

### 03 solenoid: the one that needs its own supply

```
D6 -> MOSFET gate
      source -> GND
      drain -> solenoid -> +5V on its OWN supply
      1N4148 across the coil, BAND to +5V
      supply GND joined to Arduino GND
```

- [ ] Audible click every two seconds
- [ ] **The board does not reset when it fires**
- A reset means it is drawing from USB. Adafruit warn about this explicitly:
  1.1 A at 5V is too much

### 04 capacitive: the one that will surprise you

```
A0 -> a bare wire -> foil, card or fabric
D9 -> servo signal
```

- [ ] Servo reacts to a finger on the pad
- [ ] Open the Serial Plotter and watch the baseline drift. That drift is the
      whole lesson, so make sure it is visible before the session

### 05 Peltier: safety first, and slow

```
D3 PWM -> H-bridge low side
D5 PWM -> H-bridge high side
tile on the BENCH supply
```

- [ ] **Heatsink on the hot face before you switch anything on**
- [ ] One face warms, then cools after it reverses
- Give it 10 seconds each way. It is genuinely slow, which is the point

### 06 transducer

```
D11 -> PAM8403 input
amp -> transducer, pressed FLAT against a plate
```

- [ ] 40 Hz felt through the plate, 400 Hz heard
- It needs surface contact to couple. Held in the air it does almost nothing

---

## Step 4: the parts table

Students take what they need from here, so it has to be self-service.

- [ ] One tray per component type, labelled. Transistors and diodes in their
      own trays, clearly apart: they look similar and swapping them is the
      mistake that costs parts
- [ ] **A diode orientation card** next to the diode tray. One line: band goes
      to +V. This is the most expensive mistake in the room and a card at the
      point of use prevents more of it than a slide does
- [ ] FSR, flex, pulse, GSR on one table
- [ ] A note saying there is **only one GSR sensor**, so ask before taking it
- [ ] Your own built benches at the front, working, as reference builds

---

## Step 5: the morning of

- [ ] Re-run every bench test. Things move overnight
- [ ] Write `github.com/labtools-au/multimodal-actuator-workshop` on the board
- [ ] Write `sensors.chomskylab.dk` next to it
- [ ] Check the Peltier's heatsink paste
- [ ] Have the coin motor and solenoid both wired for the opening demo
- [ ] Lay out the parts trays and the diode orientation card
- [ ] Put your reference builds where students can walk up to them
- [ ] **Photograph each station** while it is built and working. Drop them in
      `docs/photos/`, re-run the deck build, and next year is easier

**If a station fails and you cannot fix it in five minutes, pull it.** Five
working stations beat six with a mystery.

---

## When something does not work

`utils/` has three diagnostics, and they answer different questions:

| Symptom | Run |
|---|---|
| Nothing happens on a pin | `pin_sweep`, which drives every PWM pin in turn |
| An I2C part is silent | `i2c_scanner`. Is the chip even visible? |
| A sensor reads oddly | `analog_monitor`. What range does it really give? |

Do not run `pin_sweep` on the Peltier station. It drives pins to full.

---

## What is still unverified

Being straight about this so nothing surprises you:

- **No sketch has ever run on hardware.** All fifteen compile clean for the
  Uno under `arduino-cli` (`arduino:avr@1.8.8`), which catches syntax and
  missing libraries but proves nothing about wiring. Step 3 is the first real
  test.
- The **Peltier's 2 to 4 A** is a generic TEC1-12706 figure. The lab record has
  no datasheet link. Measure it.
- The **transducer's impedance** is assumed from its name. The supplier page
  blocked scraping.
- Everything else comes from the manufacturers' own pages, listed in
  [bench_tests/DATASHEETS.md](bench_tests/DATASHEETS.md).
