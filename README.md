# Feel Before You Build

A 2-hour hands-on prototyping workshop for **Multimodal Interaction** (Lecture 5).

The session is deliberately theory-light. Students meet the hardware first and get
the concepts in the lectures that follow, so nothing here depends on a lecture they
have not had yet.

**Audience:** computer science students, not product development students. They can
write the code. What they lack is any physical sense of what a coin motor, a solenoid
or a Peltier tile actually *feels* like. So touch gets designed on paper, then quietly
dropped from the project, and everything ends up on the screen and the speaker.

**Format:** six pre-wired benches, 10 minutes each on a hard rotation, then one build.
Nobody wires anything during the rotation. They touch things and form opinions.

📄 **[Full session plan, run sheet and kit list](https://claude.ai/code/artifact/1e577f62-4cae-4ec5-a407-69494dc85f7e)**

## Slides

`docs/multimodal-actuator-workshop.pptx`: 19 slides in the AU Department of
Computer Science house style, **with speaker notes on every slide** (timings,
what to say, what goes wrong at each bench).

The layout was reverse-engineered from Eve Hoggan's `MultimodalInteraction_2b_
Visual` deck rather than guessed: 959.76 x 540 pt canvas, AU blue `#002546`
sampled from the file, three layouts (blue title / white section divider /
white content), uppercase heavy headings with a short rule under them, no
accent colour anywhere, and the fixed AU footer on every slide.

Also exported as PDF, for AV systems that won't take a .pptx and for printing:

- `docs/multimodal-actuator-workshop.pdf`: slides only (19 pages)
- `docs/multimodal-actuator-workshop-with-notes.pdf`: each slide with its
  speaker notes underneath (38 pages). This is the one to print and run the
  session from.

Rebuild it with:

```bash
cd docs/deck && python3 build_deck.py && python3 add_notes.py
```

## Run sheet

| Offset | Duration | What |
|---|---|---|
| 0:00 | 10 min | Two motors, same message. Which felt urgent? |
| 0:10 | 60 min | Bench rotation, 10 min each |
| 1:10 | 10 min | Round-the-room: what surprised you |
| 1:20 | 30 min | Build one signal |
| 1:50 | 10 min | Blind test and pack down |

## The six benches

| # | Bench | Modality | Code |
|---|---|---|---|
| 01 | ERM coin motor | vibration | [`01_erm_tacton`](benches/01_erm_tacton) |
| 02 | LRA + piezo disc | vibration | – |
| 03 | Solenoid tap | impact | – |
| 04 | Capacitive touch to servo | touch input | [`04_capacitive_touch`](benches/04_capacitive_touch) |
| 05 | Peltier warm / cool | thermal | – |
| 06 | The same signal, twice | audio + touch | – |

Benches without code here run from library example sketches (`Adafruit_DRV2605`,
`Servo.h`) with only the pin numbers changed. Bench 1 and 4 are the two worth
reading, and both are commented for students rather than for you.

## The one idea worth stealing: capacitive sensing costs a wire

`benches/04_capacitive_touch` is the bench that reliably surprises people. Touch
input with **no breakout board**. A bare wire on an analogue pin, read through the
[ADCTouch](https://github.com/martin2250/ADCTouch) library. Tape it behind foil,
cardboard or fabric and any surface becomes an input.

The pattern that makes it work, and the part students get wrong:

```cpp
const float THRESHOLD = 1.01;   // 1% above the ROLLING AVERAGE, not an absolute value

bool isTouched(int reading) {
  return reading > baselineAverage() * THRESHOLD;
}
```

A capacitive reading drifts with humidity, with mains hum, with how someone is
sitting. A fixed threshold works on the bench in the morning and fails after lunch.
So the baseline is a 25-sample rolling average and, the subtle bit, **the buffer is
only fed while untouched**. Otherwise a long press slowly teaches the baseline
that a finger is normal, and the touch stops registering.

Put the Serial Plotter on screen during this bench. Watching the baseline wander
while the trigger line tracks it explains the design in about ten seconds.

## Prior art: local rigs worth five minutes of screen time

Real work by students at roughly the same stage, which argues better than any slide
that the gap between "we should use haptics" and "it moves when you touch it" is small.

### `capacitive_sensing_and_servos_and_actuators` (SOS 2025, Arduino Uno)
A moving screen that breathes when idle and retreats when touched. 922 lines driving
capacitive sensing, two mirrored servos and four linear actuators, plus a browser
control panel over the serial port. Bench 4 is this sketch with everything but the
sensing stripped out.

**Transferable:** sine-easing and an idle "breathing" loop are what separate *a servo
moved* from *it reacted to me*. Both are about a dozen lines.

### `esp32_pressure_data_sensing` (bachelor project, ESP32)
Instrumented sock. Six force-sensitive resistors under a foot (arch, heel, big toe,
three edges), sampled on an ESP32 and batched to PocketBase over Wi-Fi ten readings
at a time. Each sensor carries its own two-point calibration constants, because
supposedly identical FSRs were not.

**Transferable:** per-sensor calibration, and batching writes rather than one HTTP
request per sample.

> ⚠️ That repo has a hardcoded Wi-Fi SSID/password and a live PocketBase URL with
> patient and session IDs. Scrub it before showing it to a room.

### `remoteCollab`: spatial audio, **not yet added**
The audio/speaker exemplar for bench 6. Not on this machine or either GitHub
account, and likely on AU GitLab under a group member's namespace. Once located, the
things worth pulling out are the panning/positioning setup and how sources are
placed relative to the listener, to make Lecture 7's *crossmodal redundancy* concrete
rather than abstract.

## Closing brief

Encode three messages in **one** actuator, varying only the **rhythm** of the pulses
and how **strong** they are. Suggested set: *message arrived*, *something is wrong*,
*task finished*.

Hand the device to another group with the display turned away. They receive all three
in random order and name them. Write down which two got confused, and what parameter
would have separated them.

**The constraint that makes it interesting:** the recipient cannot look at the device.
If your design only works when someone is watching a screen, you built a visual
interface with a motor glued to it.

## Library dependencies

Arduino IDE → Library Manager:

- **ADCTouch** (martin2250), bench 4
- **Servo**, bundled with the IDE
- **Adafruit DRV2605**, bench 2

## Where this sits in the course

This is **Lecture 5, the prototyping workshop**. It runs before the Actuators lecture,
so it is built to need no prior theory: students form opinions by touching things, and
the vocabulary arrives afterwards in the lectures that cover actuators, auditory
feedback and multimodal feedback design.

The only thing it leans on is the Haptic Modality lecture, and only loosely.

Pneumatics and smart materials are left out: too slow to prep and too fiddly for a
10-minute bench. Electro-vibration is left out because it is not used in the course.
