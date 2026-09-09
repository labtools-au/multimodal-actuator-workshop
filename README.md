# Feel Before You Build

A 2-hour hands-on prototyping workshop for **Multimodal Interaction** (Lecture 5).

The session is deliberately theory-light. Students meet the hardware first and get
the concepts in the lectures that follow, so nothing here depends on a lecture they
have not had yet.

**Audience:** computer science students, not product development students. They can
write the code. What they lack is any physical sense of what a coin motor, a solenoid
or a Peltier tile actually *feels* like. So touch gets designed on paper, then quietly
dropped from the project, and everything ends up on the screen and the speaker.

**Format:** a board each and five tasks. Everything is pre-wired, so they upload,
change two numbers, upload again. The actuators they are not currently driving sit on
benches around the room, to pick up and compare between tasks.

📄 **[Full session plan, run sheet and kit list](https://claude.ai/code/artifact/1e577f62-4cae-4ec5-a407-69494dc85f7e)**

## Building it

[BUILD.md](BUILD.md) is the step-by-step: what to buy, which drawers to raid,
which library to install, and each station in the order to build and test it,
with what "working" looks like for each.

Start there if you are setting the room up.

## Try it before you touch hardware

[`wokwi/`](wokwi) has three tasks as runnable browser simulations, so a student
can check their code compiles and behaves before touching hardware.

Be aware of the limits before showing one to a room: Wokwi has no transistor,
MOSFET, diode, DC motor or solenoid part, so each project substitutes (a relay
module for the motor driver, a button for the touch pad) and says so on the
canvas. The driver circuit you actually build is in the `// PINS` block at the
top of each sketch and in [PINS.md](PINS.md), not in the simulation.

See [wokwi/README.md](wokwi/README.md) for exactly what each one does and does
not show.

## Pin map

[PINS.md](PINS.md) has every station on one page, which is what you want when
building the room. Each sketch also repeats its own pins at the top, so a
student never has to look elsewhere.

Two things catch people: only D3, D5, D6, D9, D10 and D11 do PWM on an Uno,
and the stepper's pins go into the constructor **out of order** (8, 10, 9, 11).

## What is where

```
BUILD.md          start here when setting the room up. Shop list, drawers,
                  then each station in build order with a pass criterion
PINS.md           every pin on one page
README.md         this file

tasks/            what students do. Five Arduino sketches + one browser task
bench_tests/      one sketch per station, proving the hardware works    (you)
utils/            diagnostics for when a station misbehaves             (you)
wokwi/            four tasks as runnable browser simulations
scripts/          request_components.py, and sync_logger.py
docs/             the deck, the session plan, and the build scripts
  deck/           build_deck.py, add_notes.py, the AU template, QR codes
  photos/         part photos, pulled from the component database
```

Structure follows `ktane` (Physical Computing 2023): tiny per-component tests
kept separate from the real code, plus a utils folder of dumb diagnostics.
Every sketch sits in a folder of the same name, which the Arduino IDE requires.

Each of those folders also holds a copy of `logger.h`, so every sketch prints
the same banner and timestamped events. It is duplicated rather than installed
as a library, which means there is nothing to install before the first upload.
`scripts/sync_logger.py` keeps the copies identical, and `--check` fails if one
has drifted.

**Split by audience.** `tasks/` is written for students and commented for them.
`bench_tests/` and `utils/` are for you, and assume you know what a MOSFET is.
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

### Photos

`docs/photos/` holds the actuator photos. Anything missing renders as a dashed
PHOTO frame on the slide, so it is obvious what still needs shooting. Drop a
file in, re-run the build, and it lands. Filenames are listed in
[`docs/photos/README.md`](docs/photos/README.md).

### Editing it later

The deck is built on a template, `docs/deck/au-template.pptx`, so it stays
editable rather than being a pile of loose text boxes:

- Slides use real **title and body placeholders**, so PowerPoint's outline view
  works (View > Outline) and you can retype content without hunting for boxes.
- The AU branding lives on the **slide master and its four layouts**, not on
  each slide. Change the byline or course line once in View > Slide Master and
  all 19 slides follow.
- Four layouts: *Title Slide* (blue), *Title and Content*, *Section Header*,
  *Two Content* (the bench slides).

Small edits: open the .pptx and type. Structural changes: edit
`docs/deck/build_deck.py` (content), `au_template.py` (branding and layout), or
`add_notes.py` (speaker notes), then:

```bash
cd docs/deck
python3 au_template.py   # only if you changed branding or layouts
python3 build_deck.py
python3 add_notes.py
```

One caveat: the AU logos are stamped onto each slide as well as sitting on the
layouts. LibreOffice does not render pictures inherited from a layout, so
without that the PDF exports would lose them.

## Run sheet

| Offset | Duration | What |
|---|---|---|
| 0:00 | 10 min | Two motors, same message. Which felt urgent? |
| 0:10 | 15 min | Boards out, task 01 running for everyone |
| 0:25 | 60 min | Tasks 02 to 05, at your own pace |
| 1:25 | 10 min | Round-the-room: what surprised you |
| 1:35 | 20 min | Blind test on task 05 |
| 1:55 | 5 min | Pack down |

## The six benches

| # | Bench | Modality | Code |
|---|---|---|---|
| 01 | ERM coin motor | vibration | [`01_erm_motor`](bench_tests/01_erm_motor) |
| 02 | Piezo element | vibration | [`02_piezo`](bench_tests/02_piezo) |
| 03 | Solenoid tap | impact | [`03_solenoid`](bench_tests/03_solenoid) |
| 04 | Capacitive touch to servo | touch input | [`04_capacitive_touch`](bench_tests/04_capacitive_touch) |
| 05 | Peltier warm / cool | thermal | [`05_peltier`](bench_tests/05_peltier) |
| 06 | The same signal, twice | audio + touch | [`06_transducer`](bench_tests/06_transducer) |

Every bench now has a test sketch. They are deliberately minimal: each proves one
component works and nothing more. See [`bench_tests/`](bench_tests).

## The tasks

`tasks/` holds five self-contained sketches. Upload one and it runs. Each has a
**CHANGE ME** block at the top (two or three numbers to edit) and a **THINGS TO TRY**
list at the bottom (four experiments, easy to hard).

| # | Task | What they learn |
|---|---|---|
| 01 | [Make something spin](tasks/01_make_it_spin) | PWM, and that a motor stalls below ~90 |
| 02 | [Make something tap](tasks/02_make_it_tap) | One tap vs three. Rhythm carries meaning |
| 03 | [Make something warm](tasks/03_make_it_warm) | H-bridge direction, and how slow skin is |
| 04 | [Make it notice you](tasks/04_make_it_sense) | Capacitive input from a wire |
| 05 | [Make it answer back](tasks/05_make_it_answer) | Input driving output. A real interaction |
| 06 | [Use what you have](tasks/06_use_what_you_have) | Phone sensors in a browser. No board at all. Live at [sensors.chomskylab.dk](https://sensors.chomskylab.dk) |

The arc is deliberate: 1 to 3 are output, 4 is input, 5 is both. By task 5 they have
built a complete interaction loop, which is the shape of most project work. Task 5's
last experiment is the closing brief, so it carries straight over.

Nobody is expected to finish all five. Getting task 1 working and then properly
playing with task 2 beats rushing through everything.

## The one idea worth stealing: capacitive sensing costs a wire

`bench_tests/04_capacitive_touch` is the bench that reliably surprises people. Touch
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
control panel over the serial port. Bench 4 and task 04 are this sketch with
everything but the sensing stripped out, and they keep its constants verbatim:
`TOUCH_RESOLUTION = 300`, threshold `1.01`, and a 25-sample rolling baseline
that is only fed while untouched. The 25 is itself a tuned value; the repo's
own commit says "Reduced touch smoothing buffer size for improved
responsiveness", down from 50.

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

### `ktane` (Physical Computing 2023, gitlab.au.dk/exploronauterne)
Keep Talking And Nobody Explodes, built physically. Not multimodal, but its
`Test of components and features/` directory is a good model for this workshop:
one tiny sketch per component, each provably working before anything is
combined. Also a useful reminder of what CS students actually get stuck on at
this level, which is I2C between boards, `millis()` timing instead of `delay()`,
and debouncing.

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

## Where this sits in the course

This is **Lecture 5, the prototyping workshop**. It runs before the Actuators lecture,
so it is built to need no prior theory: students form opinions by touching things, and
the vocabulary arrives afterwards in the lectures that cover actuators, auditory
feedback and multimodal feedback design.

The only thing it leans on is the Haptic Modality lecture, and only loosely.

Pneumatics and smart materials are left out: too slow to prep and too fiddly for a
10-minute bench. Electro-vibration is left out because it is not used in the course.
