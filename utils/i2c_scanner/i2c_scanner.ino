// UTIL — I2C SCANNER
//
// Lists every I2C device the board can see. Run this FIRST whenever an I2C
// part misbehaves: bench 02's DRV2605L haptic driver, or an MPR121 if you add
// one for a project.
//
// No address found means the problem is wiring or power, not your code.
// Wrong address means your library is looking in the wrong place.
//
// Expected on bench 02: 0x5A (DRV2605L).
//
// The same scanner lives in ktane/utils/. Keeping one around is a habit worth
// copying: rule out the hardware before you start reading your own code.

#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
  while (!Serial) delay(10);
  Serial.println("I2C scanner");
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

  if (found == 0) Serial.println("nothing found. Check SDA, SCL and power.");
  Serial.println("---");
  delay(3000);
}
