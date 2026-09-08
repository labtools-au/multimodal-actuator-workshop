#!/usr/bin/env python3
"""
Build the "Feel Before You Build" workshop deck in the AU Department of
Computer Science house style.

Layout rules were reverse-engineered from Eve Hoggan's MultimodalInteraction_2b_
Visual.pdf: 959.76x540pt canvas, three layouts (blue title / white section
divider / white content), AU blue #002546 sampled from the file, uppercase heavy
headings with a short rule, no accent colour anywhere, and a fixed footer on
every slide (AU wordmark bottom-left, seal bottom-right, course + byline centre).
"""

from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pathlib import Path

HERE = Path(__file__).parent
ART = HERE
OUT = HERE.parent / "multimodal-actuator-workshop.pptx"

# --- canvas: match the source deck exactly (959.76 x 540 pt) ----------------
SW, SH = Pt(959.76), Pt(540)

AU_BLUE = RGBColor(0x00, 0x25, 0x46)   # sampled from the PDF
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
INK     = RGBColor(0x00, 0x00, 0x00)
GREY    = RGBColor(0x59, 0x59, 0x59)

# Arial: what the source deck subsets, and always present on AU machines.
FONT = "Arial"

L = Pt(72)          # left margin, ~7.5%, matches the source
CONTENT_W = Pt(816)


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tf


def para(tf, text, size, bold=False, color=INK, space_after=0, level=0,
         first=False, spacing=1.0):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.text = text
    p.level = level
    p.space_after = Pt(space_after)
    p.line_spacing = spacing
    for r in p.runs:
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        r.font.name = FONT
    return p


def rule(slide, x, y, w=Pt(46), color=INK):
    """The short horizontal rule that sits under every heading."""
    from pptx.enum.shapes import MSO_SHAPE
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Pt(2.5))
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def blank(prs, bg=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])   # 6 = truly blank
    if bg is not None:
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = bg
    return slide


def footer(slide, light=False):
    """AU signature block: wordmark bottom-left, seal bottom-right, course
    line and byline in the middle. Present on every slide in the source."""
    wm = ART / ("wordmark_light.png" if light else "wordmark_dark.png")
    sl = ART / ("seal_light.png" if light else "seal_dark.png")
    ink = WHITE if light else INK

    # wordmark: same box the source uses, bottom-left
    slide.shapes.add_picture(str(wm), Pt(27), Pt(487), width=Pt(163))
    # seal: bottom-right
    slide.shapes.add_picture(str(sl), Pt(884), Pt(470), height=Pt(56))

    tf = textbox(slide, Pt(360), Pt(492), Pt(200), Pt(40))
    para(tf, "MULTIMODAL INTERACTION", 7, color=ink, first=True, spacing=1.15)
    para(tf, "PROTOTYPING WORKSHOP", 7, color=ink, spacing=1.15)

    tf2 = textbox(slide, Pt(600), Pt(492), Pt(220), Pt(40))
    para(tf2, "GUSTAV SIMONSEN", 7, color=ink, first=True, spacing=1.15)
    para(tf2, "TEACHING ASSISTANT", 7, color=ink, spacing=1.15)


# --- the three layouts ------------------------------------------------------

def title_slide(prs, title, subtitle=None):
    s = blank(prs, AU_BLUE)
    tf = textbox(s, L, Pt(200), Pt(820), Pt(140))
    para(tf, title.upper(), 54, bold=True, color=WHITE, first=True, spacing=0.95)
    if subtitle:
        t2 = textbox(s, L, Pt(330), Pt(760), Pt(60))
        para(t2, subtitle, 20, color=WHITE, first=True, spacing=1.25)
    footer(s, light=True)
    return s


def section_slide(prs, title):
    s = blank(prs, WHITE)
    rule(s, L, Pt(130))
    tf = textbox(s, L, Pt(230), Pt(820), Pt(150))
    para(tf, title.upper(), 44, bold=True, color=INK, first=True, spacing=0.98)
    footer(s)
    return s


def content_slide(prs, title, body=None, lead=None):
    """body: list of (text, level, bold). level 0 = top line, 1 = bullet."""
    s = blank(prs, WHITE)
    tf = textbox(s, L, Pt(58), Pt(830), Pt(60))
    para(tf, title.upper(), 32, bold=True, color=INK, first=True, spacing=0.98)
    rule(s, L, Pt(118))

    y = Pt(150)
    if lead:
        lf = textbox(s, L, y, Pt(700), Pt(40))
        para(lf, lead, 17, color=GREY, first=True, spacing=1.3)
        y = Pt(190)

    if body:
        bf = textbox(s, L, y, Pt(780), Pt(300))
        for i, (text, level, bold) in enumerate(body):
            size = 17 if level == 0 else 15
            para(bf, ("• " + text) if level else text,
                 size, bold=bold, color=INK, first=(i == 0),
                 space_after=7 if level == 0 else 3,
                 level=0, spacing=1.25)
    footer(s)
    return s


def bench_slide(prs, num, name, tag, body, question, spec):
    """Two-column: description left, monospace-ish spec block right."""
    s = blank(prs, WHITE)

    hf = textbox(s, L, Pt(58), Pt(600), Pt(70))
    para(hf, f"{num}   {name}".upper(), 30, bold=True, color=INK,
         first=True, spacing=0.98)
    rule(s, L, Pt(118))

    tf = textbox(s, L, Pt(134), Pt(520), Pt(24))
    para(tf, tag.upper(), 10, bold=True, color=GREY, first=True)

    bf = textbox(s, L, Pt(168), Pt(520), Pt(180))
    for i, line in enumerate(body):
        para(bf, line, 16, color=INK, first=(i == 0), space_after=9, spacing=1.3)

    qf = textbox(s, L, Pt(360), Pt(520), Pt(70))
    para(qf, "CARD QUESTION", 9, bold=True, color=GREY, first=True,
         space_after=5)
    para(qf, question, 15, bold=True, color=AU_BLUE, spacing=1.3)

    # spec block, right column
    sf = textbox(s, Pt(650), Pt(168), Pt(250), Pt(240))
    for i, (k, v) in enumerate(spec):
        p = para(sf, f"{k}   {v}", 12, color=INK, first=(i == 0),
                 space_after=6, spacing=1.2)
        p.runs[0].font.name = "Consolas"
    footer(s)
    return s


def run_sheet_slide(prs, rows):
    s = blank(prs, WHITE)
    tf = textbox(s, L, Pt(58), Pt(830), Pt(60))
    para(tf, "RUN SHEET", 32, bold=True, color=INK, first=True)
    rule(s, L, Pt(118))

    lf = textbox(s, L, Pt(150), Pt(700), Pt(30))
    para(lf, "Times are offsets from the start. The rotation is the spine of it, so "
             "keep it moving.", 15, color=GREY, first=True)

    y = Pt(196)
    for clock, dur, what in rows:
        cf = textbox(s, L, y, Pt(90), Pt(30))
        p = para(cf, clock, 17, bold=True, color=AU_BLUE, first=True)
        p.runs[0].font.name = "Consolas"

        df = textbox(s, Pt(150), y + Pt(2), Pt(70), Pt(30))
        para(df, dur, 12, color=GREY, first=True)

        wf = textbox(s, Pt(235), y, Pt(620), Pt(30))
        para(wf, what, 16, color=INK, first=True)
        y += Pt(46)
    footer(s)
    return s


# ---------------------------------------------------------------------------

def build():
    prs = Presentation()
    prs.slide_width, prs.slide_height = SW, SH

    title_slide(prs, "Feel Before You Build",
                "Hands-on prototyping with actuators  ·  2 hours")

    content_slide(
        prs, "Why we are here",
        lead="You can read a datasheet. You have never held one of these.",
        body=[
            ("Today you put a vibration motor against your own wrist, decide it feels "
             "cheap, and pick something else. Better now than in week 46.", 0, False),
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
        prs, "01", "ERM coin motor", "Cutaneous · vibration",
        ["An off-centre weight on a motor shaft. The same part that is in your "
         "phone and every game controller.",
         "Turn the knob and notice what you cannot do. Speed and strength are "
         "mechanically welded together, so \"gentle but fast\" is not "
         "available to you."],
        "At what point does it stop feeling like information and start feeling "
        "like a malfunction?",
        [("part", "10mm 3V coin ERM"), ("drive", "2N2222 + 1N4148"),
         ("pin", "D9 (PWM)"), ("draw", "~75 mA"),
         ("spin-up", "20–40 ms"), ("cost", "~12 kr")])

    bench_slide(
        prs, "02", "LRA + piezo disc", "Cutaneous · vibration",
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
        prs, "03", "Solenoid tap", "Cutaneous · impact",
        ["A push-pull solenoid firing a single 15 ms pulse against a fingertip.",
         "This is the bench everyone remembers. A single knock carries urgency "
         "that no amount of buzzing does, because it reads as a person "
         "tapping you rather than a machine signalling."],
        "How many taps before it goes from alert to nagging?",
        [("part", "5V push-pull"), ("drive", "MOSFET + flyback"),
         ("pin", "D6"), ("peak", "~1.1 A"),
         ("duty", "<= 25%, gets hot"), ("cost", "~45 kr")])

    bench_slide(
        prs, "04", "Capacitive touch", "Kinesthetic · touch-to-actuate",
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
        prs, "05", "Peltier warm / cool", "Cutaneous · thermal",
        ["A thermoelectric tile: heats one side, cools the other, reverses when "
         "you flip the current.",
         "Sit with it. It takes several seconds before you are sure which way "
         "it went.",
         "And alternating hot with cold does not read as a pattern. It just "
         "reads as lukewarm."],
        "Time yourself. How long until you would bet money on warmer vs cooler?",
        [("part", "TEC1-12706"), ("drive", "L298N H-bridge"),
         ("pin", "D3 PWM / D4-5"), ("draw", "2–4 A, bench PSU"),
         ("onset", "3–8 s"), ("cap", "45 C in software")])

    bench_slide(
        prs, "06", "The same signal, twice", "Intramodal · audio + haptic",
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
            ("A moving screen that breathes when idle and retreats when you touch "
             "it, with a browser control panel over the serial port.", 1, False),
            ("Take away: easing and idle motion are what separate \"a servo moved\" "
             "from \"it reacted to me\". Both are a dozen lines.", 1, False),
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
            ("Vary only two things: the RHYTHM of the pulses, and how STRONG they "
             "are. No swapping actuators between messages.", 0, False),
            ("Hand it to another group with the screen turned away. They name all "
             "three.", 0, False),
            ("Write down which two got confused, and what would have separated "
             "them.", 0, False),
        ])

    content_slide(
        prs, "The constraint that matters",
        body=[
            ("The recipient cannot look at the device.", 0, True),
            ("", 0, False),
            ("If your design only works when someone is watching a screen, "
             "you built a visual interface with a motor glued to it.", 0, False),
        ])

    title_slide(prs, "Go and touch things",
                "github.com/gust1527/multimodal-actuator-workshop")

    prs.save(OUT)
    print(f"wrote {OUT}  ({len(prs.slides.__iter__.__self__._sldIdLst)} slides)")


if __name__ == "__main__":
    build()
