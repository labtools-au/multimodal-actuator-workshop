// UTIL: I2C SCANNER
//
// Lists every I2C device the board can see. Run this FIRST whenever an I2C
// part misbehaves. Nothing in this workshop uses I2C, so this is here for
// project work: an MPR121 touch breakout, an MPU6050, an OLED, a DRV2605L
// haptic driver if you buy one.
//
// No address found means the problem is wiring or power, not your code.
// Wrong address means your library is looking in the wrong place.
//
// The same scanner lives in ktane/utils/. Keeping one around is a habit worth
// copying: rule out the hardware before you start reading your own code.

#include "logger.h"

#include <Wire.h>

void setup() {
  Wire.begin();
  logBegin("UTIL  i2c scanner", "A4 SDA, A5 SCL, plus 5V and GND");
  while (!Serial) delay(10);
}

void loop() {
  int found = 0;

  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    byte error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("device at 0x");
      if (addr < 16) Serial.print("0");
      Serial.println(addr, HEX);
      found++;
    }
  }

  if (found == 0)  logEvent("nothing found. Check SDA, SCL and power.");
  logEvent("scan complete");
  delay(3000);
}
