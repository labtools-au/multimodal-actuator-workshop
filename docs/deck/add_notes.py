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

    # 5: run sheet
    """Show it, do not narrate it. Fifteen seconds.

The one hard checkpoint is 0:25. Everyone should have task 01 running by then.
If someone is still fighting drivers at 0:30, pair them with a group that is
working rather than debugging it alone.""",

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

    # 8: base kit
    """Hand this out before anything else, or you will spend the session
fetching parts one at a time.

One set per pair. The three drawer numbers are the ones people actually come
back and ask for: 8A breadboard supply, 2C H-bridge, 11F amplifier.

Jumper wires, breadboards and resistors are not tracked in the component
database, so make sure there are enough on the tables before students
arrive.""",

    # 9: coin motor
    """The one everybody already owns without knowing it. Every phone has one.

The point worth making: speed and strength are welded together. That single
constraint is why the other five exist.""",

    # 10: LRA and piezo
    """The escape from the coin motor's compromise. A crystal that flexes when
you put current across it: near-instant, almost no power, but shallow.

A tick, not a thump. Point anyone here who needs something to feel responsive
rather than just present. 69 in the drawer, so nobody has to share.""",

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

    # 16: servo
    """Worth showing even though it is not in a task. Most projects that need
something to physically move end up here rather than on a vibration motor.

80 in stock, so nobody has to share.""",

    # 17: stepper
    """The precision option. Moves in known steps, so you can position it
without any feedback sensor at all. 2048 steps per revolution.

Needs a ULN2003 driver board, drawer 2A, 27 of them.

If anyone tries one: the Stepper constructor does NOT take the pins in numeric
order. Wire IN1 to IN4 on pins 8 to 11, then write Stepper(2048, 8, 10, 9, 11).
Get it wrong and it buzzes and jitters instead of turning, which looks like a
dead motor. bench_tests/07_stepper has it right, with the note.""",

    # 18: electromagnet
    """The one people forget exists. It grabs and lets go, with nothing moving.

Good answer for anything that should hold and then release: a latch, a door, a
thing that falls when the event happens.""",

    # 17: freestyle within three limits
    """Two messages on one slide, and they pull in opposite directions on
purpose. Say the permission warmly, then change tone for the limits.

Permission first: some students will not believe they are allowed to skip
ahead or stop early unless told. The failure mode is a pair rushing all five
badly instead of doing two properly.

Then the three hard limits, and here you should sound firm. Say the numbers
out loud: a pin gives 40 mA, the motor wants about 75. It is not a rule they
have to take on faith.

Worth adding: a board resetting when the solenoid fires is a POWER problem,
not a code bug. That saves someone twenty minutes.""",

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

    # 25: why come
    """The slide that earns the room's attention, so do not rush it.

This audience can write the code already, and they know it. Saying so out loud
buys credibility for the rest. The argument is not "you need to learn to
program a motor", it is "you cannot Google what something feels like".

The second point is practical and lands with everyone: the parts are free and
already in the building.""",

    # 26: reverse engineer what you own
    """The slide the tinkerers will care most about, and the one where being
precise matters, because the internet is full of wrong answers.

The useful surprise: most Garmin watches broadcast heart rate over BLE
natively. Turn on Broadcast Heart Rate, or start a Virtual Run, and the watch
appears as an ordinary heart rate strap that Web Bluetooth can read from a web
page. No Connect IQ app, no SDK, no API key.

Apple Watch will not. HealthKit needs a companion watchOS app in Swift, so
third-party apps that re-broadcast over BLE are the practical route.

Web Bluetooth is Chrome and Edge only. Not Safari, not Firefox. Same lesson as
vibration: check the feature before it goes in a plan.

Good project prompt if anyone wants one: a page that pairs with a strap and
drives an actuator from a live pulse. That is an afternoon.""",

    # 23: what a phone will and will not give you
    """Have them open sensors.chomskylab.dk on their own phones while you talk.
The split between what works and what does not lands far harder on their own
device than on a slide.

The bottom half is the single most useful fact here, and the one people get
wrong because a blog post said otherwise.

Say it plainly: iPhones do not vibrate from a web page. Not with a polyfill,
not with a library, not in Chrome for iOS, which is Safari underneath.

The general lesson is bigger than vibration: check the feature on caniuse
before it goes in a project plan, not after. Two minutes now against a
rewrite in week 46.""",

    # prior art
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

    # 28: before you call it done
    """Put this up while the blind tests run, so groups can check themselves
without asking you.

The middle line matters most: a device that fires continuously when held is
the single most common bug, and it is a debounce problem.

Then close on the bottom half, thirty seconds. If they leave with one thing,
make it the last point: pick the actuator before designing the interaction.
Discovering in week 46 that the chosen one cannot do the job is the expensive
mistake this session exists to prevent.""",

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
