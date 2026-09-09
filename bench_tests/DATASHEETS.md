# Where the numbers come from

Every electrical figure in these sketches and on the slides is from the
manufacturer's own page for the exact part in the lab's drawers, not from
memory or a generic tutorial. Checked 9 September 2026.

| Part | Source | What it fixed |
|---|---|---|
| Vibrating Mini Motor Disc | [adafruit.com/product/1201](https://www.adafruit.com/product/1201) | Draws **100 mA at 5V**, not the ~75 mA first written. Rated 2.5-3.8V, runs 2-5V, 11000 RPM at 5V. Adafruit suggest a **PN2222**. |
| Mini Push-Pull Solenoid 5V | [adafruit.com/product/2776](https://www.adafruit.com/product/2776) | **1.1 A at 5V**, 4.5 ohm coil, throw **3mm at 80g**, not the 10mm first written. Adafruit warn explicitly against powering it from USB. |
| 28BYJ-48 + ULN2003 | [lastminuteengineers.com](https://lastminuteengineers.com/28byj48-stepper-motor-arduino-tutorial/), and Rachana Jain's [Instructables walkthrough](https://www.instructables.com/How-to-Control-28BYJ-48-Stepper-Motor-With-ULN2003-/) | **2048 steps/rev**, and the constructor takes pins **IN1-IN3-IN2-IN4**, so `Stepper(2048, 8, 10, 9, 11)`. Sequential order makes it buzz instead of turn. Two independent sources agree, and the Instructables one explains WHY: IN1/IN3 are one coil, IN2/IN4 the other, so the constructor wants coil pairs, not pin order. Rated 5V, 4 phase, stride 5.625°/64, gear ratio 1/64. |
| ULN2003 board LEDs | [manufacturer PCB schematic, p.3](https://www.electronicoscaldas.com/datasheet/ULN2003A-PCB.pdf) | The LEDs are on the **output** side: anode through a resistor to VCC, cathode to the ULN2003 output. The chip is open-collector and only sinks. So with no board power the LEDs stay dark no matter what the input pins do. Dark LEDs plus verified-HIGH inputs means an unpowered board, not a dead one. |
| Capacitive sensing | The lab's own SOS 2025 rig | Rolling baseline at 1.01x, 25 samples, 100 ms debounce. Taken from working code, not invented. |

## Still unverified

- **Peltier**: the lab record has no product URL, and the generic TEC1-12706
  figures (2-4 A) are typical rather than confirmed for this exact tile.
  Measure the current draw before the session.
- **Surface transducer**: supplier page blocked scraping. Impedance and power
  are assumed to be 4 ohm / 3 W for the medium and 8 ohm / 1 W for the bone
  conductor, per the lab record names. Confirm before relying on the amp
  settings.
- **Nothing has been flashed on hardware.** Every sketch passes a syntax check
  only. Run them all before the session.
