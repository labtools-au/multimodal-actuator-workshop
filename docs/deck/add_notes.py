#!/usr/bin/env python3
"""Add speaker notes to the workshop deck. English, written to be spoken."""

from pptx import Presentation
from pathlib import Path

HERE = Path(__file__).parent
DECK = HERE.parent / "multimodal-actuator-workshop.pptx"

NOTES = [
    # 0: title
    """0:00. Start here, and do not read the slide.

Open with the demo, not with talking. Have the coin motor and the solenoid both
wired and running before anyone sits down.

Buzz a phone-style notification on the motor. Then send the same message on the
solenoid. Ask which felt more urgent. Let them answer. Nobody needs theory for
that, and it is the argument for the whole session.""",

    # 1: tldr
    """Fifteen seconds. It is a map, not a talk.

Useful because half the room arrives expecting a lecture and needs to be told
immediately that this is not one.""",

    # 2: why we are here
    """Say the full version out loud, the slide only carries the skeleton:

"You can read a datasheet. You have never held one of these. Today you put a
vibration motor against your own wrist, decide it feels cheap, and pick
something else. Better now than in week 46 with the demo three days out."

Every year projects end up on the screen and the speaker, and touch gets
designed on paper then dropped. Two minutes, then move.""",

    # 2: how today works
    """Set the shape clearly, because it is not a lecture and they will wait to be
lectured at.

A board each. Five tasks. Everything pre-wired. They upload, change numbers,
upload again.

The actuators they are NOT driving sit on tables around the room. Tell them
explicitly to go and pick those up between tasks. The comparison still happens,
just on their own initiative rather than on a timer.""",

    # 3: run sheet
    """Show it, do not narrate it. Fifteen seconds.

The one hard checkpoint is 0:25. Everyone should have task 01 running by then.
If someone is still fighting drivers at 0:30, pair them with a group that is
working rather than debugging it alone.""",

    # 4: section, five tasks
    """0:10. Boards out.

Get EVERYONE through task 01 before anyone races ahead. It is the shortest and
it flushes out the setup problems: wrong board, wrong port, missing driver.

Once task 01 runs for a pair, they can move at their own pace.""",

    # 5: five tasks list
    """Ninety seconds on this slide, no more.

Name the arc, it is the point: 1 to 3 are output, 4 is input, 5 is both. By
task 5 they have built a complete interaction loop, which is the shape of most
project work.

Say clearly that nobody is expected to finish all five. Getting 01 working and
then properly playing with 02 beats rushing all of them.

Task 05's last experiment IS the closing brief, so the work carries over.""",

    # 6: how the sketches work
    """Say the format once here rather than repeating it per task.

CHANGE ME at the top: two or three numbers, already set to something that
works. THINGS TO TRY at the bottom: four experiments, easy to hard, and the
last one usually asks for a rewrite rather than a tweak.

Upload problems, in the order they will hit you:
  * wrong board or port under Tools
  * ADCTouch not installed (tasks 04 and 05)
  * solenoid task: board resets when it fires means its supply is off

Write the repo URL on the whiteboard now. It gets asked for six times.

If a task's hardware fails, utils/ has the diagnostics: pin_sweep, i2c_scanner,
analog_monitor.""",

    # 8: section, what is on the tables
    """Two minutes total for this whole run of slides. It is a menu, not a
lecture: they are choosing what to go and pick up later.

Hold up the real part as you show each one. The photo is a reminder for people
reading the deck afterwards; the object in your hand is what lands in the
room.""",

    # 9: coin motor
    """The one everybody already owns without knowing it. Every phone has one.

The point worth making: speed and strength are welded together. That single
constraint is why the other five exist.""",

    # 10: LRA and piezo
    """Both solve the coin motor's problem, differently. LRA is what a modern
phone keyboard uses. Piezo is sharp but shallow.

If someone is designing anything that needs to feel responsive rather than
just present, point them here.""",

    # 11: solenoid
    """Pass this one around if you can. It is the one people remember, because a
knock reads as a person rather than a machine.

Warn them now that it needs its own supply, so it does not come as a surprise
at task 02.""",

    # 12: capacitive pad
    """Hold up a wire and a piece of foil. That is genuinely the whole sensor.

This is the slide that changes what people think is possible, because it costs
nothing and hides completely inside a prototype.""",

    # 13: peltier tile
    """Say the honest limitation out loud: it is slow, and hot alternating with
cold just reads as lukewarm.

Good for slow ambient state. Wrong for alerts. Saying so here saves a project
from finding out in week 46.""",

    # 14: transducer
    """The redundancy argument. Same driver, one frequency you feel and one you
hear.

Together is not louder, it is more certain. Cheapest reliability a project can
buy, and it is also the accessibility answer.""",

    # 15: freestyle
    """Say this out loud, do not just show it. Some students will not believe
they are allowed to skip ahead or stop early unless you tell them.

The failure mode is a pair rushing all five tasks badly instead of doing two
properly. Name that explicitly.""",

    # 9: before you power anything
    """The only slide where you should sound firm.

Three real hazards:
  * solenoid and Peltier on their own supply, not USB
  * Peltier heatsink on before it is switched on, no exceptions
  * no motor straight from a pin

Say the numbers: a pin gives 40 mA, the motor wants about 75. It is not a rule
they have to take on faith.

Also mention that a board resetting when the solenoid fires is a POWER problem,
not a code bug. It will save someone twenty minutes.""",

    # 10: the one that surprises people
    """Slow down here. This is the single idea most worth stealing from today, and
it is worth interrupting the room for once most people have reached task 04.

Two things students get wrong:

1. A fixed threshold. Works in the morning, fails after lunch, because the
   reading drifts with humidity and mains hum.

2. Feeding the baseline buffer always. A long press then teaches the baseline
   that a finger is normal, and the touch silently stops working. The buffer
   must only learn while untouched.

Put the Serial Plotter on the projector. Watching the baseline wander while the
trigger line tracks it explains the whole design in ten seconds.

For what it is worth, the rig this came from went through the same tuning: an
earlier version used 1.008 with a 50-sample baseline, the final one 1.01 with
25. Everyone tunes these.""",

    # 8: section, inputs and prior art
    """1:25. Pull the room back together.

One sentence per group: what surprised you. No slides, no laptops. Ten minutes.

Expect someone to report the Peltier delay. Let that land, it is far more
persuasive from a peer than from you.""",

    # 9: inputs
    """Mention, do not teach. These sit on one table with a sign.

The honest warnings matter more than the specs: PPG is useless once the hand
moves, GSR drifts so only relative change works, FSRs need per-pad calibration.

Push the phone option hard. For a lot of projects it beats everything else on
the table and needs no soldering at all.""",

    # 10: prior art
    """Five minutes, and put the actual repos on screen if you can.

The argument: this was built by students at your stage, not by a lab with a
budget. The gap between "we should use touch" and "it moves when you touch it"
is smaller than it looks.

The moving screen has a browser control panel over the serial port, which is
what you will wish you had at the project demonstrations.

Note for you: the sock repo has a hardcoded Wi-Fi password and live patient IDs
in it. Scrub before showing, or show only the calibration section.""",

    # 11: section, build one signal
    """1:35. The blind test.

Most groups will already have something from task 05. This is where it gets
tested by someone who did not build it.""",

    # 12: the brief
    """Read the brief out once, then get out of the way. Full wording, since the
slide is only the bones:

"Pick one actuator. Encode three messages: arrived, something wrong, finished.
Vary only the rhythm of the pulses and how strong they are. Then hand it to
another group with the screen turned away and see if they can name all three."

If someone asks to add a second actuator, say no. The constraint is the
exercise.""",

    # 13: the constraint
    """The line worth repeating twice.

Run the test: swap groups, receiver looks away, guess all three.

Then have each group name which two got confused and what would have separated
them. That confusion is the actual learning, not the successful ones.""",

    # 17: test it
    """Put this up while the blind tests are running so groups can check
themselves without asking you.

The second line matters most: a device that fires continuously when held is
the single most common bug, and it is a debounce problem.""",

    # 18: what you actually learn
    """The closing argument. Thirty seconds.

If they leave with only one thing, it should be the third: pick the actuator
before designing the interaction. Discovering in week 46 that the chosen one
cannot do the job is the expensive mistake this session exists to prevent.""",

    # 19: closing
    """Point them at the repo. Every task sketch is commented for them, and the
bench test sketches are there too if they want to see the minimal version.

Last thing to say: pick your actuator before you design the interaction, not
after. Today was so they can do that from experience rather than a datasheet.

Pack down: everything back in the box, including the resistors. It will not all
come back.

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
