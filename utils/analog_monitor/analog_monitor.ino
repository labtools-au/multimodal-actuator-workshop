// UTIL: ANALOG MONITOR
//
// Prints one analogue pin continuously, in a format the Serial Plotter draws.
// Use it on any sensor at the input table before you write real code: flex,
// GSR, FSR, a potentiometer, a photoresistor.
//
// The point is to learn the RANGE your sensor actually produces before you
// pick a threshold. Almost nothing gives you a clean 0 to 1023, and a
// threshold guessed from a datasheet usually misses.
//
// Tools > Serial Plotter. Then squeeze, bend or press the sensor and watch.
//
// NOT for the capacitive pad: that needs ADCTouch and its own baseline, see
// bench_tests/04_capacitive_touch.

const int SENSOR = A1;

// ---- CHANGE ME ------------------------------------------------------------
int sampleMs = 20;      // how often to read. 20 ms = 50 readings a second
bool showMinMax = true; // also print the range seen so far
// ---------------------------------------------------------------------------

int seenMin = 1023;
int seenMax = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Move the sensor through its full range, then read the min/max.");
}

void loop() {
  int v = analogRead(SENSOR);

  if (v < seenMin) seenMin = v;
  if (v > seenMax) seenMax = v;

  // Plotter draws every space-separated number as its own line.
  Serial.print(v);
  if (showMinMax) {
    Serial.print(' ');
    Serial.print(seenMin);
    Serial.print(' ');
    Serial.print(seenMax);
  }
  Serial.println();

  delay(sampleMs);
}

// ---- WHAT TO DO WITH THE NUMBERS ------------------------------------------
//
// Once you know the real range, map it instead of guessing:
//
//   int level = map(analogRead(SENSOR), seenMin, seenMax, 0, 255);
//
// And when you need a threshold, put it somewhere in the middle of the range
// you actually measured, not at a round number that looked reasonable.
