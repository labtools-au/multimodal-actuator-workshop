#!/usr/bin/env python3
"""
Build the "Feel Before You Build" workshop deck.

Content only. Everything visual — the AU blue, the logos, the footer, the type
sizes, the rule under each heading — lives in au-template.pptx, on the slide
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
        blocks.append((lead, 17, False, GREY, 14))
    for text, level, bold in (body or []):
        if not text:
            blocks.append(("", 8, False, INK, 0))
        else:
            blocks.append((("• " + text) if level else text,
                           15 if level else 17, bold, INK, 7))
    _fill(s.placeholders[1], blocks)
    _restyle(s)
    _stamp_logos(s, False)
    return s


def bench_slide(prs, num, name, tag, body, question, spec):
    s = prs.slides.add_slide(prs.slide_layouts[BENCH])
    s.placeholders[0].text_frame.text = f"{num}   {name}".upper()

    blocks = [(tag.upper(), 10, True, GREY, 10)]
    for line in body:
        blocks.append((line, 16, False, INK, 9))
    blocks.append(("", 8, False, INK, 4))
    blocks.append(("CARD QUESTION", 9, True, GREY, 4))
    blocks.append((question, 15, True, AU_BLUE, 0))
    _fill(s.placeholders[1], blocks)

    tf = s.placeholders[2].text_frame
    tf.clear()
    for i, (k, v) in enumerate(spec):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
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


def run_sheet_slide(prs, rows):
    s = prs.slides.add_slide(prs.slide_layouts[CONTENT])
    s.placeholders[0].text_frame.text = "RUN SHEET"
    blocks = [("Times are offsets from the start. The rotation is the spine of "
               "the session, so keep it moving.", 15, False, GREY, 16)]
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
        prs, "Why we are here",
        lead="You can read a datasheet. You have never held one of these.",
        body=[
            ("Today you put a vibration motor against your own wrist, decide it "
             "feels cheap, and pick something else. Better now than in week 46.", 0, False),
            ("", 0, False),
            ("Every year, projects end up built entirely on the screen and the "
             "speaker.", 0, False),
            ("Not because touch was the wrong choice. Because nobody knew that a "
             "coin motor costs 12 kr and takes two wires.", 0, False),
        ])

    content_slide(
        prs, "How today works",
        body=[
            ("Six benches. Already wired. Already running.", 0, True),
            ("Ten minutes each, on a hard timer.", 1, False),
            ("You change one parameter and answer one question.", 1, False),
            ("You wire nothing. That is what the project weeks are for.", 1, False),
            ("", 0, False),
            ("Then you build one signal and someone else tries to read it.", 0, True),
        ])

    run_sheet_slide(prs, [
        ("0:00", "10 min", "Two motors, same message. Which felt urgent?"),
        ("0:10", "60 min", "Bench rotation, 10 minutes each"),
        ("1:10", "10 min", "Round-the-room: what surprised you"),
        ("1:20", "30 min", "Build one signal"),
        ("1:50", "10 min", "Blind test and pack down"),
    ])

    section_slide(prs, "The six benches")

    bench_slide(
        prs, "01", "ERM coin motor", "Vibration",
        ["An off-centre weight on a motor shaft. The same part that is in your "
         "phone and every game controller.",
         "Turn the knob and notice what you cannot do. Speed and strength are "
         "mechanically welded together, so \"gentle but fast\" is not available "
         "to you."],
        "At what point does it stop feeling like information and start feeling "
        "like a malfunction?",
        [("part", "10mm 3V coin ERM"), ("drive", "2N2222 + 1N4148"),
         ("pin", "D9 (PWM)"), ("draw", "~75 mA"),
         ("spin-up", "20-40 ms"), ("cost", "~12 kr")])

    bench_slide(
        prs, "02", "LRA + piezo disc", "Vibration",
        ["Two ways out of the ERM's compromise.",
         "The LRA hits resonance in about 5 ms and stops just as fast, which is "
         "why phone keyboards use it.",
         "The piezo is a crystal that flexes when you put current across it. "
         "Near-instant, almost no power, but shallow. A tick, not a thump."],
        "Which of the three vibrators would you actually put on a wrist, and "
        "why not the others?",
        [("parts", "LRA 10mm + piezo"), ("driver", "DRV2605L (I2C)"),
         ("pin", "A4 SDA / A5 SCL"), ("effects", "123 waveforms"),
         ("cost", "~90 kr")])

    bench_slide(
        prs, "03", "Solenoid tap", "Impact",
        ["A push-pull solenoid firing a single 15 ms pulse against a fingertip.",
         "This is the bench everyone remembers. A single knock carries urgency "
         "that no amount of buzzing does, because it reads as a person tapping "
         "you rather than a machine signalling."],
        "How many taps before it goes from alert to nagging?",
        [("part", "5V push-pull"), ("drive", "MOSFET + flyback"),
         ("pin", "D6"), ("peak", "~1.1 A"),
         ("duty", "<= 25%, gets hot"), ("cost", "~45 kr")])

    bench_slide(
        prs, "04", "Capacitive touch", "Touch input",
        ["Touch a surface with a bare finger and the servos react.",
         "There is no button and no sensor you can point at. The input is a "
         "wire taped behind a plate, read on an analogue pin.",
         "Any surface can become an input this way: foil, card, fabric."],
        "Put your hand near the plate without touching. When exactly did it "
        "decide that was a touch?",
        [("sense", "ADCTouch on A0"), ("baseline", "25-sample roll"),
         ("trigger", "1.01x average"), ("debounce", "100 ms"),
         ("servos", "D4 + D13"), ("cost", "~0 kr, a wire")])

    content_slide(
        prs, "Bench 04: the whole trick",
        lead="Touch input for the price of a wire. The thinking is where it costs you.",
        body=[
            ("reading > baselineAverage() * 1.01", 0, True),
            ("", 0, False),
            ("The threshold is RELATIVE, never absolute.", 0, True),
            ("Readings drift with humidity, with mains hum, with how you are "
             "sitting. A fixed threshold works in the morning and fails after "
             "lunch.", 1, False),
            ("", 0, False),
            ("The baseline only learns while untouched.", 0, True),
            ("Otherwise a long press slowly teaches it that a finger is normal, "
             "and the touch quietly stops registering.", 1, False),
        ])

    bench_slide(
        prs, "05", "Peltier warm / cool", "Thermal",
        ["A thermoelectric tile: heats one side, cools the other, reverses when "
         "you flip the current.",
         "Sit with it. It takes several seconds before you are sure which way "
         "it went.",
         "And alternating hot with cold does not read as a pattern. It just "
         "reads as lukewarm."],
        "Time yourself. How long until you would bet money on warmer vs cooler?",
        [("part", "TEC1-12706"), ("drive", "L298N H-bridge"),
         ("pin", "D3 PWM / D4-5"), ("draw", "2-4 A, bench PSU"),
         ("onset", "3-8 s"), ("cap", "45 C in software")])

    bench_slide(
        prs, "06", "The same signal, twice", "Audio + touch",
        ["One transducer on a plate, playing 40 Hz you feel and 400 Hz you hear, "
         "both from the same driver.",
         "Toggle between them alone and together.",
         "Together is not louder. It is more certain. Sending the same thing "
         "down two channels is the cheapest reliability your project can buy."],
        "With ear defenders on, does the signal still work?",
        [("part", "bone-conduction"), ("amp", "PAM8403 class-D"),
         ("pin", "D11 (tone)"), ("felt", "~40 Hz"),
         ("heard", "~400 Hz"), ("cost", "~110 kr")])

    section_slide(prs, "Inputs, and prior art")

    content_slide(
        prs, "Inputs worth knowing about",
        lead="One table, not a rotation. Wander over during the build.",
        body=[
            ("Capacitive touch. A wire on an analogue pin. See bench 04.", 1, False),
            ("Heart rate (PPG). Steady at rest, useless once the hand moves.", 1, False),
            ("Skin conductance (GSR). Drifts constantly, so relative change only.", 1, False),
            ("Flex sensor. The cheap route to a data glove.", 1, False),
            ("Pressure (FSR). How hard, not just whether. Calibrate each pad.", 1, False),
            ("Your own phone. Accelerometer, gyro, mic, camera, vibration motor. "
             "No soldering at all.", 1, False),
        ])

    content_slide(
        prs, "Two rigs that already exist",
        lead="Built here, by students at roughly your stage.",
        body=[
            ("Capacitive sensing, servos and actuators (Arduino Uno)", 0, True),
            ("A moving screen that breathes when idle and retreats when you "
             "touch it, with a browser control panel over the serial port.", 1, False),
            ("Take away: easing and idle motion are what separate \"a servo "
             "moved\" from \"it reacted to me\". Both are a dozen lines.", 1, False),
            ("", 0, False),
            ("Instrumented sock (ESP32, bachelor project)", 0, True),
            ("Six force sensors under a foot, sent to a server over Wi-Fi in "
             "batches, each with its own calibration constants.", 1, False),
            ("Take away: calibrate per sensor, and batch your writes.", 1, False),
        ])

    section_slide(prs, "Build one signal")

    content_slide(
        prs, "The brief",
        lead="30 minutes. Deliberately not long enough to be precious about it.",
        body=[
            ("Pick one actuator from the rotation.", 0, False),
            ("Encode three messages: arrived, something wrong, finished.", 0, False),
            ("Vary only two things: the RHYTHM of the pulses, and how STRONG "
             "they are. No swapping actuators between messages.", 0, False),
            ("Hand it to another group with the screen turned away. They name "
             "all three.", 0, False),
            ("Write down which two got confused, and what would have separated "
             "them.", 0, False),
        ])

    content_slide(
        prs, "The constraint that matters",
        body=[
            ("The recipient cannot look at the device.", 0, True),
            ("", 0, False),
            ("If your design only works when someone is watching a screen, you "
             "built a visual interface with a motor glued to it.", 0, False),
        ])

    title_slide(prs, "Go and touch things",
                "github.com/gust1527/multimodal-actuator-workshop")

    prs.save(OUT)
    print(f"wrote {OUT} ({len(prs.slides._sldIdLst)} slides)")


if __name__ == "__main__":
    build()
