// BENCH TEST 02: LRA + PIEZO
//
// Does the haptic driver respond at all? Run this before the session.
// Cycles through a few of the DRV2605L's built-in effects.
//
// If nothing happens: check the I2C wiring with utils/i2c_scanner first.
// If it buzzes but sounds wrong: the driver is in the wrong mode. An LRA
// driven as an ERM feels weak and rough. See setup() below.

#include <Wire.h>
#include <Adafruit_DRV2605.h>

Adafruit_DRV2605 drv;

// A few of the 123 built-in waveforms. Full list is in the datasheet.
const int EFFECTS[] = {1, 14, 24, 47, 58};
const int EFFECT_COUNT = sizeof(EFFECTS) / sizeof(EFFECTS[0]);

void setup() {
  Serial.begin(9600);
  if (!drv.begin()) {
    Serial.println("DRV2605L not found. Check SDA/SCL and power.");
    while (1) delay(10);
  }
  drv.selectLibrary(1);
  drv.setMode(DRV2605_MODE_INTTRIG);

  // THE ONE THAT CATCHES PEOPLE: tell it which actuator it is driving.
  // Comment this out for the ERM, keep it for the LRA.
  drv.useLRA();

  Serial.println("DRV2605L online. Cycling effects.");
}

void loop() {
  for (int i = 0; i < EFFECT_COUNT; i++) {
    Serial.print("effect ");
    Serial.println(EFFECTS[i]);

    drv.setWaveform(0, EFFECTS[i]);
    drv.setWaveform(1, 0);        // 0 terminates the sequence
    drv.go();
    delay(1200);
  }
}
