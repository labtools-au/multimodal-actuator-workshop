#!/usr/bin/env python3
"""
Build the "Feel Before You Build" workshop deck.

Content only. Everything visual. the AU blue, the logos, the footer, the type
sizes, the rule under each heading. lives in au-template.pptx, on the slide
master and its four layouts. Run au_template.py to regenerate that.

That split is deliberate, so the deck stays editable later:

  * slides use real TITLE and BODY placeholders, so PowerPoint's outline view
    works and you can retype content without hunting for text boxes
  * the AU footer is defined once per layout, not copied onto 19 slides
  * changing the byline or course line means editing au_template.py, or the
    slide master in PowerPoint, and every slide follows

Edit the CONTENT list at the bottom to change what the deck says.
"""

from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE = HERE / "au-template.pptx"
OUT = HERE.parent / "multimodal-actuator-workshop.pptx"

AU_BLUE = RGBColor(0x00, 0x25, 0x46)
PHOTOS = HERE.parent / "photos"      # drop real photos here, named as below
L = Pt(72)                           # left margin, matches the layouts
LIGHT_LAYOUTS = {0}          # blue ground -> white logos
GREY = RGBColor(0x59, 0x59, 0x59)
INK = RGBColor(0x00, 0x00, 0x00)
FONT = "Arial"

# Layout indices in au-template.pptx
TITLE, CONTENT, SECTION, BENCH = 0, 1, 2, 3


def _fill(ph, blocks):
    """blocks: list of (text, size, bold, color, space_after)."""
    tf = ph.text_frame
    tf.clear()
    for i, (text, size, bold, color, after) in enumerate(blocks):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text
        p.space_after = Pt(after)
        p.line_spacing = 1.0 if bold and size > 20 else 1.28
        _no_bullet(p)
        p.alignment = PP_ALIGN.LEFT
        for r in p.runs:
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color
            r.font.name = FONT
    return tf


def title_slide(prs, title, subtitle):
    s = prs.slides.add_slide(prs.slide_layouts[TITLE])
    s.placeholders[0].text_frame.text = title.upper()
    s.placeholders[1].text_frame.text = subtitle
    _restyle(s)
    _stamp_logos(s, True)
    return s


def section_slide(prs, title):
    s = prs.slides.add_slide(prs.slide_layouts[SECTION])
    s.placeholders[0].text_frame.text = title.upper()
    _restyle(s)
    _stamp_logos(s, False)
    return s


def content_slide(prs, title, lead=None, body=None):
    s = prs.slides.add_slide(prs.slide_layouts[CONTENT])
    s.placeholders[0].text_frame.text = title.upper()
    blocks = []
    if lead:
        blocks.append((lead, 17, False, GREY, 12))
    for text, level, bold in (body or []):
        if not text:
            blocks.append(("", 8, False, INK, 0))
        else:
            blocks.append((("• " + text) if level else text,
                           15 if level else 17, bold, INK, 4))
    _fill(s.placeholders[1], blocks)
    _restyle(s)
    _stamp_logos(s, False)
    return s


def bench_slide(prs, num, name, tag, body, question, spec, used=None):
    s = prs.slides.add_slide(prs.slide_layouts[BENCH])
    s.placeholders[0].text_frame.text = f"{num}   {name}".upper()

    blocks = [(tag.upper(), 10, True, GREY, 12)]
    for line in body:
        # blank strings are deliberate breathing room between thoughts
        blocks.append((line, 16, False, INK, 4 if line else 0))
    blocks.append(("", 6, False, INK, 10))
    blocks.append(("CARD QUESTION", 9, True, GREY, 4))
    blocks.append((question, 15, True, AU_BLUE, 0))
    _fill(s.placeholders[1], blocks)

    tf = s.placeholders[2].text_frame
    tf.clear()
    if used:
        p0 = tf.paragraphs[0]
        p0.text = "USED FOR"
        p0.space_after = Pt(4)
        _no_bullet(p0)
        for r in p0.runs:
            r.font.size = Pt(9); r.font.bold = True
            r.font.color.rgb = GREY; r.font.name = FONT
        p1 = tf.add_paragraph()
        p1.text = used
        p1.space_after = Pt(16)
        p1.line_spacing = 1.25
        _no_bullet(p1)
        for r in p1.runs:
            r.font.size = Pt(12); r.font.color.rgb = AU_BLUE; r.font.name = FONT
    for i, (k, v) in enumerate(spec):
        p = tf.paragraphs[0] if (i == 0 and not used) else tf.add_paragraph()
        p.text = f"{k}   {v}"
        p.space_after = Pt(6)
        p.line_spacing = 1.2
        _no_bullet(p)
        for r in p.runs:
            r.font.size = Pt(12)
            r.font.color.rgb = INK
            r.font.name = "Consolas"
    _restyle(s)
    _stamp_logos(s, False)
    return s


def actuator_slide(prs, name, photo_name, what, feels, used, spec):
    """One actuator: photo on the left, plain description on the right."""
    s = prs.slides.add_slide(prs.slide_layouts[CONTENT])
    s.placeholders[0].text_frame.text = name.upper()

    photo(s, photo_name, name, L, Pt(150), Pt(330), Pt(250))

    tf = s.placeholders[1].text_frame
    tf.clear()
    blocks = [
        (what, 16, False, INK, 12),
        (feels, 16, True, AU_BLUE, 14),
        ("USED FOR", 9, True, GREY, 4),
        (used, 14, False, INK, 14),
        (spec, 12, False, GREY, 0),
    ]
    for i, (text, size, bold, color, after) in enumerate(blocks):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.text = text
        par.space_after = Pt(after)
        par.line_spacing = 1.3
        _no_bullet(par)
        par.alignment = PP_ALIGN.LEFT
        for r in par.runs:
            r.font.size = Pt(size); r.font.bold = bold
            r.font.color.rgb = color
            r.font.name = "Consolas" if size == 12 else FONT
    # narrow the text box so it sits beside the photo
    ph = s.placeholders[1]
    ph.left, ph.top, ph.width, ph.height = Pt(430), Pt(150), Pt(432), Pt(260)

    _restyle(s)
    _stamp_logos(s, False)
    return s


def qr(slide, name, caption, x, y, size=Pt(126), light=False):
    """A QR code with its URL underneath.

    Put one wherever the deck asks the room to open something. A URL read from
    the back of a lecture theatre is a URL nobody opens.
    """
    f = HERE / f"{name}.png"
    if f.exists():
        slide.shapes.add_picture(str(f), x, y, width=size, height=size)
    tb = slide.shapes.add_textbox(x - Pt(30), y + size + Pt(6), size + Pt(60), Pt(24))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    par = tf.paragraphs[0]
    par.text = caption
    par.alignment = PP_ALIGN.CENTER
    _no_bullet(par)
    for r in par.runs:
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xC8, 0xD2, 0xDC) if light else GREY
        r.font.name = FONT
    return slide


def photo_strip(slide, names, y, box_w=Pt(150), box_h=Pt(112), gap=Pt(14)):
    """A row of small photos along the bottom of a slide.

    For slides that talk about several parts at once (the base kit, the sensor
    table) a single big photo would be misleading. A strip shows what each
    thing physically looks like without pretending one of them is the subject.
    """
    x = L
    for name in names:
        photo(slide, name, name, x, y, box_w, box_h)
        x += box_w + gap
    return slide


def caption_strip(slide, labels, y, box_w=Pt(150), gap=Pt(14)):
    """Small captions under a photo strip, aligned to the same grid."""
    x = L
    for text in labels:
        tb = slide.shapes.add_textbox(x, y, box_w, Pt(26))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        par = tf.paragraphs[0]
        par.text = text
        par.line_spacing = 1.15
        _no_bullet(par)
        par.alignment = PP_ALIGN.LEFT
        for r in par.runs:
            r.font.size = Pt(9)
            r.font.color.rgb = GREY
            r.font.name = FONT
        x += box_w + gap
    return slide


def run_sheet_slide(prs, rows):
    s = prs.slides.add_slide(prs.slide_layouts[CONTENT])
    s.placeholders[0].text_frame.text = "RUN SHEET"
    blocks = [("Times are offsets from the start. The only hard checkpoint is "
               "0:25: everyone has task 01 running.", 15, False, GREY, 16)]
    for clock, dur, what in rows:
        blocks.append((f"{clock}   {dur:>8}    {what}", 16, False, INK, 12))
    tf = _fill(s.placeholders[1], blocks)
    for p in list(tf.paragraphs)[1:]:
        for r in p.runs:
            r.font.name = "Consolas"
            r.font.size = Pt(14)
    _restyle(s)
    _stamp_logos(s, False)
    return s


def photo(slide, name, caption, x, y, w, h):
    """Place a photo if it exists, otherwise draw a labelled empty frame.

    Same idea as the PHOTO GOES HERE callouts in the wood workshop guide: the
    slot is visible and labelled, so it is obvious what is missing and nobody
    forgets. Drop <name>.jpg (or .png) into docs/photos/ and re-run this
    script; the frame is replaced by the real thing automatically.
    """
    for ext in (".jpg", ".jpeg", ".png"):
        f = PHOTOS / (name + ext)
        if f.exists():
            pic = slide.shapes.add_picture(str(f), x, y, width=w)
            # keep it inside the box, crop-free: scale down if too tall
            if pic.height > h:
                ratio = h / pic.height
                pic.height = h
                pic.width = int(pic.width * ratio)
            return pic

    from pptx.enum.shapes import MSO_SHAPE
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    box.fill.background()
    box.line.color.rgb = GREY
    box.line.width = Pt(1)
    box.line.dash_style = 4          # dashed, reads as "not final"
    box.shadow.inherit = False

    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Pt(10)
    from pptx.enum.text import MSO_ANCHOR
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p0 = tf.paragraphs[0]
    p0.text = "NO PART" if caption.startswith("!") else "PHOTO"
    p0.alignment = PP_ALIGN.CENTER
    for r in p0.runs:
        r.font.size = Pt(9); r.font.bold = True
        r.font.color.rgb = GREY; r.font.name = FONT
    p1 = tf.add_paragraph()
    p1.text = caption.lstrip("!")
    p1.alignment = PP_ALIGN.CENTER
    p1.line_spacing = 1.2
    for r in p1.runs:
        r.font.size = Pt(11); r.font.color.rgb = GREY; r.font.name = FONT
    return box


def _stamp_logos(slide, light):
    """The AU wordmark and seal are defined on the layouts, which is what makes
    them editable in one place in PowerPoint. LibreOffice, however, does not
    render pictures inherited from a layout, so PDF exports would lose them.
    Stamping a copy onto each slide keeps both paths correct."""
    wm = HERE / ("wordmark_light.png" if light else "wordmark_dark.png")
    seal = HERE / ("seal_light.png" if light else "seal_dark.png")
    slide.shapes.add_picture(str(wm), Pt(27), Pt(487), width=Pt(163))
    slide.shapes.add_picture(str(seal), Pt(884), Pt(470), height=Pt(56))


def _no_bullet(paragraph):
    """Strip the inherited list bullet. Set on the layout too, but LibreOffice
    does not resolve that from a layout, so assert it per paragraph as well."""
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set("marL", "0")
    pPr.set("indent", "0")
    for tag in ("a:buChar", "a:buAutoNum", "a:buNone"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    pPr.append(pPr.makeelement(qn("a:buNone"), {}))


def _restyle(slide):
    """Placeholders inherit layout styling in PowerPoint, but LibreOffice and
    some renderers do not resolve that fully. Re-assert the essentials so the
    exported PDF matches what PowerPoint shows."""
    lay = {ph.placeholder_format.idx: ph for ph in slide.slide_layout.placeholders}
    for ph in slide.placeholders:
        for p in ph.text_frame.paragraphs:
            _no_bullet(p)
            p.alignment = PP_ALIGN.LEFT
        src = lay.get(ph.placeholder_format.idx)
        if src is None:
            continue
        ref = src.text_frame.paragraphs[0].font
        for p in ph.text_frame.paragraphs:
            for r in p.runs:
                if r.font.size is None:
                    r.font.size = ref.size
                if r.font.bold is None:
                    r.font.bold = ref.bold
                if r.font.name is None:
                    r.font.name = ref.name or FONT
                if r.font.color and r.font.color.type is None and ref.color:
                    try:
                        r.font.color.rgb = ref.color.rgb
                    except Exception:
                        pass


def build():
    prs = Presentation(str(TEMPLATE))

    title_slide(prs, "Feel Before You Build",
                "Hands-on prototyping with actuators  ·  2 hours")

    content_slide(
        prs, "TLDR",
        lead="Two hours finding out what actuators feel like, and leaving able to "
             "drive one from your own code.",
        body=[
            ("Get a board and run task 01. Something spins.", 0, False),
            ("Change two numbers, upload again. That loop is the workshop.", 0, False),
            ("Pick up the actuators you are not driving.", 0, False),
            ("Work through as many of the five tasks as you get to.", 0, False),
            ("Build one signal someone else can read without looking.", 0, False),
        ])

    content_slide(
        prs, "Why we are here",
        lead="You can read a datasheet. You have never held one of these.",
        body=[
            ("Most projects end up on the screen and the speaker", 0, False),
            ("Not because touch was wrong", 1, False),
            ("Because nobody knew the lab has 117 coin motors", 1, False),
            ("", 0, False),
            ("Today: decide it feels cheap, pick something else", 0, True),
            ("Better now than in week 46", 1, False),
        ])

    content_slide(
        prs, "How today works",
        body=[
            ("A board each. You build the circuits yourself", 0, True),
            ("Every part, every wire, from an empty breadboard", 1, False),
            ("Two or three stations each, getting harder", 0, True),
            ("Start with two wires. End with a transistor", 1, False),
            ("Actuators are on the tables at the front", 0, True),
            ("Go and feel the ones you did not build", 1, False),
            ("Finish by building one signal someone else can read", 0, True),
        ])

    run_sheet_slide(prs, [
        ("0:00", "10 min", "Two motors, same message. Which felt urgent?"),
        ("0:10", "10 min", "Breadboards out. Piezo: two wires, everyone"),
        ("0:20", "20 min", "Task 01: your first driver circuit, together"),
        ("0:40", "45 min", "Build on, at your own pace"),
        ("1:25", "10 min", "Round-the-room: what surprised you"),
        ("1:35", "20 min", "Blind test on task 05"),
        ("1:55", "5 min", "Pack down"),
    ])

    content_slide(
        prs, "The tasks, in build order",
        lead="Each one adds a single new thing to the circuit before it.",
        body=[
            ("00   Make it tick        piezo             2 wires", 0, True),
            ("04   Make it notice you  wire and foil     1 wire", 0, True),
            ("05   Make it answer      both of the above 3 wires", 0, True),
            ("", 0, False),
            ("01   Make something spin coin motor        + transistor", 0, True),
            ("02   Make something tap  solenoid          + own supply", 0, True),
            ("03   Make something warm Peltier tile      + H-bridge", 0, True),
            ("", 0, False),
            ("Two or three each. Nobody does all of them.", 0, False),
        ])

    content_slide(
        prs, "How the task sketches work",
        lead="Wire it from the diagram at the top, then upload. "
             "All of them: github.com/labtools-au/multimodal-actuator-workshop",
        body=[
            ("A PINS block at the very top", 0, True),
            ("Every leg, every wire. Build from that, not from memory", 1, False),
            ("A CHANGE ME block below it", 0, True),
            ("Two or three numbers. Edit, upload, feel the difference", 1, False),
            ("A THINGS TO TRY list at the bottom", 0, True),
            ("Four experiments. The last is the interesting one", 1, False),
        ])

    pin_slide = content_slide(
        prs, "Pin map",
        lead="Every sketch repeats its own pins at the top. This is the whole "
             "room on one page, for setting up.")
    tf = pin_slide.placeholders[1].text_frame
    tf.clear()
    rows = [
        ("01  spin",    "D9  PWM",       "1k to PN2222 base, motor on collector"),
        ("02  tap",     "D6",            "MOSFET gate, own supply, grounds joined"),
        ("03  warm",    "D3 + D5 PWM",   "H-bridge low and high, bench supply"),
        ("04  sense",   "A0",            "bare wire to foil. That is all of it"),
        ("05  answer",  "A0 + D9",       "the pad, plus any actuator"),
        ("07  stepper", "D8 D9 D10 D11", "ULN2003 IN1 to IN4"),
    ]
    for i, (task, pin, note) in enumerate(rows):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.text = f"{task:12}{pin:16}{note}"
        par.space_after = Pt(7)
        _no_bullet(par)
        par.alignment = PP_ALIGN.LEFT
        for r in par.runs:
            r.font.size = Pt(13)
            r.font.color.rgb = INK
            r.font.name = "Consolas"
    last = tf.add_paragraph()
    last.text = ("Only D3, D5, D6, D9, D10, D11 do PWM. Stepper pins go into "
                 "the constructor OUT of order: 8, 10, 9, 11.")
    last.space_after = Pt(0)
    _no_bullet(last)
    last.alignment = PP_ALIGN.LEFT
    for r in last.runs:
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = AU_BLUE
        r.font.name = FONT


    base = content_slide(
        prs, "What you get in the base kit",
        lead="One set per pair, collected before you start task 01. Below: the three parts people always come back for.",
        body=[
            ("Board, breadboard, jumper wires, resistors: on the tables.", 0, False),
            ("Not in the drawers, so take what you need.", 0, False),
        ])
    photo_strip(base, ["bbpsu", "hbridge", "amp"], Pt(262))
    caption_strip(base, [
        "Breadboard supply, 8A. Anything past an LED.",
        "L9110S H-bridge, 2C. Reversing, and the Peltier.",
        "PAM8403 amp, 11F. A transducer needs one.",
    ], Pt(380))

    actuator_slide(
        prs, "Vibrating mini motor disc", "erm",
        "An off-centre weight on a motor shaft, sealed in a disc. The same part "
        "as in your phone.",
        "Feels like: a buzz you cannot make gentle and fast at once.",
        "Phone notifications, controller rumble, anything worn under clothing.",
        "1E  |  117  |  2.5-3.8V rated  |  100 mA at 5V  |  PWM")

    actuator_slide(
        prs, "Piezo element", "piezo",
        "A crystal that flexes when you put current across it. Near-instant, "
        "almost no power, but shallow.",
        "Feels like: a tick, not a thump.",
        "Clicks and confirmations. Anything where lag would feel broken.",
        "Drawer 6F  |  69 in stock  |  any digital pin")

    actuator_slide(
        prs, "Mini push-pull solenoid", "solenoid",
        "A coil that yanks a metal rod when you energise it. No half a tap: it "
        "fires or it does not.",
        "Feels like: a person tapping you, not a machine signalling.",
        "Navigation cues on the body, braille cells, alerts in noise.",
        "3E  |  24  |  5V, 1.1 A, 4.5 ohm  |  3mm throw, 80g")

    actuator_slide(
        prs, "Capacitive pad", "!there is nothing to photograph. A wire, and a piece of foil.",
        "A wire taped behind foil, card or fabric. No sensor and no breakout "
        "board, which is why the box on the left is empty.",
        "Feels like: nothing. That is the point. The surface stays plain.",
        "Invisible controls in wood or fabric, waterproof panels.",
        "No drawer, no part number, no cost. Any analogue pin")

    actuator_slide(
        prs, "Peltier tile", "peltier",
        "Heats one face and cools the other. Flip the current and it reverses.",
        "Feels like: slow. Several seconds before you are sure which way.",
        "Slow ambient state. Never an alert.",
        "Drawer 4C  |  25 small, 35 big  |  needs an H bridge")

    actuator_slide(
        prs, "Surface transducer", "transducer",
        "Turns any surface into a speaker. Drive it so one frequency is felt "
        "and another is heard, from the same part.",
        "Feels like: more certain, rather than louder.",
        "Noisy or bright environments, and accessibility.",
        "Drawer 7F  |  12 large, 13 medium, 23 bone  |  needs an amp")

    actuator_slide(
        prs, "Servo", "servo",
        "A motor that holds a position instead of spinning freely. Tell it an "
        "angle and it goes there.",
        "Feels like: something deliberate moving, with force behind it.",
        "Anything that points, pushes, opens or resists a hand.",
        "Drawer 2F  |  80 in stock  |  Servo.h  |  needs its own 5V")

    actuator_slide(
        prs, "Stepper motor", "stepper",
        "Moves in fixed steps rather than continuously, so you always know "
        "where it is without a sensor.",
        "Feels like: precise, and audibly clicky.",
        "Slow accurate motion. Dials, sliders, anything positioned.",
        "2A  |  44  |  ULN2003 driver  |  2048 steps/rev")

    actuator_slide(
        prs, "Electromagnet", "electromagnet",
        "Grabs and releases ferrous metal on command. No moving parts of its "
        "own.",
        "Feels like: a grip that appears and vanishes.",
        "Latches, holds, and anything that should let go on cue.",
        "Drawer 3D  |  17 mini, 11 standard  |  needs a MOSFET")

    content_slide(
        prs, "Freestyle, within three limits",
        lead="You do not have to do the tasks in order, or finish them. "
             "Playing properly with two beats rushing all five.",
        body=[
            ("If you want to drive something not in front of you, go get it.", 0, False),
            ("The three things that are not negotiable", 0, True),
            ("Solenoid and Peltier get their own supply, never USB", 1, False),
            ("The Peltier heatsink goes on before it is switched on", 1, False),
            ("No motor straight from a pin. 40 mA limit, it wants 75", 1, False),
        ])

    content_slide(
        prs, "The one that surprises people",
        lead="Touch input for the price of a wire. The thinking is where it costs you.",
        body=[
            ("Threshold is relative, never absolute", 0, True),
            ("Readings drift with humidity and mains hum", 1, False),
            ("Fixed threshold works at 9am, fails at 1pm", 1, False),
            ("Baseline only learns while untouched", 0, True),
            ("Or a long press teaches it that a finger is normal", 1, False),
        ])

    section_slide(prs, "Inputs, and prior art")

    sensors_slide = content_slide(
        prs, "Inputs worth knowing about",
        lead="One table with a sign. Wander over between tasks.",
        body=[
            ("Capacitive touch. A wire. That is task 04", 1, False),
            ("GSR, drawer 0C5. Exactly one in the lab, so ask first", 1, False),
            ("Your own phone. No soldering at all", 1, False),
        ])
    photo_strip(sensors_slide, ["fsr", "flex", "pulse"], Pt(258))
    caption_strip(sensors_slide, [
        "Force (FSR), 4A. 46 tiny, 33 square. Calibrate each one.",
        "Flex, 4B. Only 8 left, so share them.",
        "Pulse, 9D. 9 in stock. Steady at rest, useless once moving.",
    ], Pt(376))

    content_slide(
        prs, "You already write code. Why come?",
        lead="Fair question. Three honest answers.",
        body=[
            ("You cannot Google what something feels like", 0, True),
            ("No datasheet says a knock reads as a person, a buzz as a machine", 1, False),
            ("The parts are free and already here", 0, True),
            ("Borrowing beats ordering. Nothing to buy, nothing to wait for", 1, False),
            ("Your devices hide sensors you may not be able to reach", 0, True),
            ("Find out today which open up, and which are locked", 1, False),
        ])

    content_slide(
        prs, "Reverse engineer what you already own",
        lead="The trackers in your pocket and on your wrist. What opens up, and what does not.",
        body=[
            ("BLE heart rate strap: readable from a web page", 0, True),
            ("Web Bluetooth, standard GATT. Chrome and Edge only", 1, False),
            ("Most Garmin watches: the same, with no app", 0, True),
            ("Turn on Broadcast Heart Rate and it acts as a strap", 1, False),
            ("Apple Watch: nothing live, whatever you write", 0, True),
            ("HealthKit needs a watchOS app in Swift", 1, False),
            ("Garmin history: Connect IQ, or the API afterwards", 0, True),
            ("Good for analysis. Useless for reacting in real time", 1, False),
        ])

    phone_slide = content_slide(
        prs, "What a phone will and will not give you",
        lead="Open sensors.chomskylab.dk on your own phone right now.",
        body=[
            ("Works in a web page", 0, True),
            ("Accelerometer and gyroscope, microphone, camera", 1, False),
            ("Pointer pressure, though a trackpad reports only 0 or 0.5", 1, False),
            ("Does not, whatever the tutorial says", 0, True),
            ("Phone vibration on iOS. WebKit has never shipped it, at any "
             "version, and Chrome on iOS is Safari underneath", 1, False),
            ("", 0, False),
            ("So \"the phone buzzes\" works on no iPhone in this room.", 0, True),
            ("Check the feature, not the tutorial, before it is in a plan.", 1, False),
        ])
    qr(phone_slide, "qr_sensors", "sensors.chomskylab.dk", Pt(700), Pt(170))

    content_slide(
        prs, "Two rigs that already exist",
        lead="Built here, by students at roughly your stage.",
        body=[
            ("Moving screen, Arduino Uno", 0, True),
            ("Breathes when idle. Retreats when touched", 1, False),
            ("Easing and idle motion do the work. A dozen lines", 1, False),
            ("Instrumented sock, ESP32", 0, True),
            ("Six force sensors under a foot, batched over Wi-Fi", 1, False),
            ("Calibrate per sensor. Batch your writes", 1, False),
        ])

    section_slide(prs, "Build one signal")

    content_slide(
        prs, "The brief",
        lead="30 minutes. Not long enough to be precious about it.",
        body=[
            ("One actuator, whichever you built", 0, True),
            ("Three messages: arrived, something wrong, finished", 1, False),
            ("Vary rhythm above all", 0, True),
            ("Piezo: rhythm is all you have. Motor: strength too", 1, False),
            ("Blind test: they name all three", 0, True),
            ("Note which two got confused, and why", 1, False),
        ])

    content_slide(
        prs, "The constraint that matters",
        body=[
            ("The recipient cannot look at the device.", 0, True),
            ("", 0, False),
            ("If it only works while someone watches a screen,", 0, False),
            ("you built a visual interface with a motor glued to it.", 0, False),
        ])

    content_slide(
        prs, "Before you call it done",
        lead="Hand your device to another group with the screen turned away.",
        body=[
            ("They can tell all three messages apart", 1, False),
            ("It does not fire continuously when held", 1, False),
            ("You know which two got confused, and why", 1, False),
            ("", 0, False),
            ("What you actually leave with", 0, True),
            ("What things feel like, how to drive one, and which to pick", 1, False),
            ("That last one is the expensive mistake this prevents", 1, False),
        ])

    closing = title_slide(prs, "Go and touch things",
                          "Everything is open: code, slides and session plan")
    qr(closing, "qr_repo", "github.com/labtools-au/\nmultimodal-actuator-workshop",
       Pt(730), Pt(300), size=Pt(118), light=True)

    prs.save(OUT)
    print(f"wrote {OUT} ({len(prs.slides._sldIdLst)} slides)")


if __name__ == "__main__":
    build()
