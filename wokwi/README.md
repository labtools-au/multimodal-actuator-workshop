# Wokwi simulations

Three tasks as runnable [Wokwi](https://wokwi.com) projects. Free, browser
based, no install.

## After editing a diagram

```bash
python3 validate.py
```

Wokwi fails **silently**: an unknown part type is dropped with no error, and a
malformed connection can stop the whole canvas rendering. Both happened while
building these. The validator checks part types, pin names and routing syntax
against the documented format.

One rule worth knowing: leave the routing array **empty** (`[]`) and let Wokwi
place the wire. Hand-written hops like `"v0"` are what broke the first version.

## Opening one

Go to [wokwi.com](https://wokwi.com), start a new Arduino Uno project, then
paste `diagram.json` and `sketch.ino` into the matching tabs. Save it and the
URL is shareable.

## What they actually simulate, and what they cannot

Read this before showing one to a room. Wokwi has **no transistor, MOSFET,
diode, DC motor or solenoid part**, so none of the driver circuits can be drawn
as they are built. Every project here substitutes, and says so on the canvas.

| Project | Substitution | What it still teaches |
|---|---|---|
| 01 make it spin | A **relay module** replaces the transistor and motor. The module contains the same driver circuit you build by hand. An LED shows when it is on. | The code is identical. The rhythm and timing are real. |
| 02 make it tap | Same relay, on D6. | You can **hear** the relay click each pulse, so the rhythm of a tacton is audible. |
| 04 make it sense | A **button** replaces the foil pad. | The shape of the task: touch causes a response. |

**What none of them show:** the flyback diode, the base resistor, and where
each leg physically goes. Those live in the `// PINS` block at the top of every
sketch and in [PINS.md](../PINS.md).

**What none of them can show:** what anything feels like. A simulated Peltier
does not take eight seconds to convince you, and a relay click is not a
solenoid against your fingertip. That is the whole reason the workshop exists.

## Not simulated at all

Tasks 03, 05 and 06. No thermoelectric part, no capacitive sensing, and task 06
needs a real phone. A simulation that quietly does the wrong thing is worse
than none.

## If you want a real wiring picture

Photograph the built benches. For an audience that has never read a schematic,
a photo of the actual thing beats every diagram, and you are building the
stations anyway.
