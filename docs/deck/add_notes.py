#!/usr/bin/env python3
"""Add speaker notes to the workshop deck. English, written to be spoken."""

from pptx import Presentation
from pathlib import Path

HERE = Path(__file__).parent
DECK = HERE.parent / "multimodal-actuator-workshop.pptx"

NOTES = [
    # 0: title
    """0:00. Start here. Don't read the slide.

Open with the failing demo, not with talking. Have the coin motor and the
solenoid both wired and ready before anyone sits down.

Buzz a phone-style notification on the ERM. Then send the same message on the
solenoid. Ask: which felt more urgent? Let them answer. Nobody needs theory
for that, and that IS the argument for the whole session.""",

    # 1: why we are here
    """Say the full version out loud, the slide only carries the skeleton:

"You can read a datasheet. You have never held one of these. Today you put a
vibration motor against your own wrist, decide it feels cheap, and pick
something else. Better now than in week 46 with the demo three days out."

Every year projects end up on the screen and the speaker, and touch gets
designed on paper then dropped.

Not because it was wrong. Because nobody had held the parts.

They get the Actuators lecture tomorrow. Today is the hands, not the theory.

Keep this short, 2 minutes. They came to do things, not hear framing.""",

    # 2: how today works
    """Set the rules firmly, because the rotation collapses if you don't.

Nobody wires anything today. Everything is pre-wired and running. They turn
one knob and answer one question.

Say out loud: the timer is hard. Ten minutes means ten minutes. Bench 3, the
solenoid, is the one people will not want to leave.""",

    # 3: run sheet
    """Show it, don't narrate it. Fifteen seconds.

Practical: assign each group a DIFFERENT starting bench so they rotate cleanly.
Six groups, six benches. Write starting numbers on the whiteboard.

If a bench breaks mid-session, pull it and go to five. Five working benches
beat six with a mystery.""",

    # 4: section: the six benches
    """0:10. Rotation starts. Set a visible timer.

You are now a timekeeper, not a lecturer. Call the rotation loudly every ten
minutes. Circulate, but do not rescue. Let them poke at things.

The bench slides that follow are reference for YOU and for anyone who wants to
look back. Do not present them one by one before the rotation. That would eat
the hour.""",

    # 5: bench 01
    """The core limitation, made physical: speed and strength are mechanically
linked on this motor. You cannot get gentle-but-fast.

Common question: "why does it feel weak at low PWM?" Below about 90 the motor
cannot overcome its own friction. That floor is real and worth naming.

Never let anyone rewire this to a bare pin. 40 mA limit, motor pulls 75.""",

    # 6: bench 02
    """The escape from bench 1's compromise. LRA is the phone-keyboard feel:
5 ms on, 5 ms off. Piezo is a crystal that flexes when you put current across
it, so it is sharp but shallow.

If the LRA sounds wrong, the DRV2605L is in ERM mode. It must be told which
type it's driving. That's the failure to expect here.

Good moment to point out: 123 built-in waveforms means they don't have to
design vibration from scratch in their project.""",

    # 7: bench 03
    """The memorable one. A single knock reads as a person tapping you
rather than a machine signalling. Worth naming out loud, because it is the
whole reason it feels different, and the slide only says the short version.

Watch the duty cycle. Solenoids get hot fast, so if it has been hammering for
ten minutes, let it rest.

Separate supply, common ground. On USB alone the board browns out and resets,
which looks like a code bug and isn't.""",

    # 8: bench 04
    """The surprise bench. No breakout board. The input is a wire.

Have the Serial Plotter on a screen here. Watching the baseline wander while
the trigger line tracks it teaches the whole idea in ten seconds.

Let someone hold their hand NEAR without touching. The gradual approach is
what makes the threshold question real.""",

    # 9: bench 04 detail
    """Slow down here. This is the one idea most worth stealing from today.

Two things students get wrong:

1. They use a fixed threshold. Works in the morning, fails after lunch,
   because the reading drifts with humidity and mains hum.

2. They feed the baseline buffer always. Then a long press teaches the
   baseline that a finger is normal, and the touch silently stops working.
   The buffer must ONLY learn while untouched.

Code is in the repo, bench 04, commented for them.""",

    # 10: bench 05
    """Thermal. People are bad at reading thermal patterns, and this is
where they find that out for themselves.

Make them time themselves. The 3 to 8 second onset kills a lot of bad project
ideas before they get proposed, which is exactly what you want happening now
rather than in week 46.

Safety: heatsink on the hot side, capped at 45 C. Skin burns above 50.""",

    # 11: bench 06
    """Redundancy, made physical. One transducer on a plate, two frequencies: 40 Hz
you feel, 400 Hz you hear, both from the same driver.

The point isn't that together is louder. It's that together is more CERTAIN.
Sending the same thing down two channels is the cheapest reliability their
projects can buy.

Ear defenders must actually be used or the comparison is dishonest.""",

    # 12: section: inputs and prior art
    """1:10. Rotation over. Round-the-room now.

One sentence per group: what surprised you. No slides, no laptops. Ten minutes.

Expect the thermal group to report the delay. Let that land, it is more
persuasive coming from a peer than from you.""",

    # 13: inputs
    """Mention, don't teach. These sit on one table with a sign. The slide is one
line each; the caveats below are what actually saves them time.

The honest warnings matter more than the specs: PPG is garbage once the hand
moves, GSR drifts so only relative change is usable, FSRs need per-pad
calibration.

Push the phone option hard. For a lot of projects it genuinely beats
everything else on the table and needs no soldering.""",

    # 14: prior art
    """Five minutes, and show the actual repos on screen if you can. The slide names
them; you supply the detail.

The moving screen has a browser control panel over the serial port, which is
exactly what you want at the project demonstrations.

The argument: this was built by students at your stage, not by a lab with a
budget. The gap between "we should use haptics" and "it moves when you touch
it" is smaller than it looks.

Note for you: the sock repo has a hardcoded Wi-Fi password and live patient
IDs in it. Scrub before showing, or show only the calibration section.""",

    # 15: section: build
    """1:20. Build starts. Thirty minutes.

Groups pick any actuator from the rotation. Most will pick bench 1 or 3
because they are simplest. That is fine, the constraint does the work.""",

    # 16: the brief
    """Read the brief out once, then get out of the way. Full wording, since the
slide is only the bones:

"Pick one actuator. Encode three messages: arrived, something wrong, finished.
Vary only the rhythm of the pulses and how strong they are. Then hand it to
another group with the screen turned away and see if they can name all three."

Rhythm and strength only. If someone asks to add a second actuator, say no.
The constraint is the exercise. Encoding within one channel is the skill.

Suggested set is on the slide, but let them choose their own three messages if
they have a better idea.""",

    # 17: the constraint
    """This is the line worth repeating twice.

1:50. Blind test. Swap groups, receiver looks away, guess all three.

Then have each group name which two got confused and what would have separated
them. That confusion is the actual learning, not the successful ones.

Pack down: everything back in the box, including the resistors. It will not
all come back.""",

    # 18: closing
    """Point them at the repo. Bench 01 and 04 sketches are commented for them.

Last thing to say: pick your actuator before you design the interaction, not
after. Today was so they can do that from experience rather than a datasheet.

If anyone wants to borrow parts for the project weeks, now is when they ask.""",
]


def main():
    prs = Presentation(DECK)
    slides = list(prs.slides)
    if len(NOTES) != len(slides):
        raise SystemExit(f"notes {len(NOTES)} != slides {len(slides)}")
    for slide, note in zip(slides, NOTES):
        slide.notes_slide.notes_text_frame.text = note.strip()
    prs.save(DECK)
    print(f"added notes to {len(slides)} slides")


if __name__ == "__main__":
    main()
