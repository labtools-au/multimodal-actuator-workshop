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
                           15 if level else 17, bold, INK, 6))
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
            ("Because nobody knew a coin motor costs 12 kr", 1, False),
            ("", 0, False),
            ("Today: decide it feels cheap, pick something else", 0, True),
            ("Better now than in week 46", 1, False),
        ])

    content_slide(
        prs, "How today works",
        body=[
            ("A board each, five tasks, everything pre-wired", 0, True),
            ("Upload, change two numbers, upload again", 1, False),
            ("You wire nothing today", 1, False),
            ("", 0, False),
            ("Actuators are on the tables around you", 0, True),
            ("Go and feel the ones your task does not use", 1, False),
            ("", 0, False),
            ("Finish by building one signal", 0, True),
            ("Someone else has to read it", 1, False),
        ])

    run_sheet_slide(prs, [
        ("0:00", "10 min", "Two motors, same message. Which felt urgent?"),
        ("0:10", "15 min", "Boards out, task 01 running for everyone"),
        ("0:25", "60 min", "Tasks 02 to 05, at your own pace"),
        ("1:25", "10 min", "Round-the-room: what surprised you"),
        ("1:35", "20 min", "Blind test on task 05"),
        ("1:55", "5 min", "Pack down"),
    ])

    section_slide(prs, "Five tasks")

    content_slide(
        prs, "Five tasks, one board each",
        lead="Upload, change two numbers, upload again. That loop is the point.",
        body=[
            ("01   Make something spin        coin motor", 0, True),
            ("02   Make something tap         solenoid", 0, True),
            ("03   Make something warm        Peltier tile", 0, True),
            ("04   Make it notice you         a wire and foil", 0, True),
            ("05   Make it answer back        both together", 0, True),
            ("", 0, False),
            ("1 to 3 are output. 4 is input. 5 is both.", 0, False),
            ("Nobody is expected to finish all five.", 0, False),
        ])

    content_slide(
        prs, "How the task sketches work",
        lead="Every sketch runs the moment you upload it. Nothing to wire.",
        body=[
            ("A CHANGE ME block at the top", 0, True),
            ("Two or three numbers. Edit, upload, feel the difference", 1, False),
            ("", 0, False),
            ("A THINGS TO TRY list at the bottom", 0, True),
            ("Four experiments, roughly in order of difficulty", 1, False),
            ("The last one is usually the interesting one", 1, False),
            ("", 0, False),
            ("github.com/gust1527/multimodal-actuator-workshop", 0, True),
        ])

    content_slide(
        prs, "Freestyle is encouraged",
        body=[
            ("You do not have to do the tasks in order.", 0, True),
            ("You do not have to finish them.", 0, True),
            ("", 0, False),
            ("Getting task 01 working and then properly playing with task 02 "
             "beats rushing through all five.", 0, False),
            ("", 0, False),
            ("If you want to drive something that is not in front of you, "
             "go and get it.", 0, False),
        ])

    content_slide(
        prs, "Before you power anything",
        body=[
            ("The solenoid and the Peltier both pull real current.", 0, True),
            ("They need their own supply. Ask before you rewire either.", 1, False),
            ("", 0, False),
            ("The Peltier needs its heatsink on. Every time.", 0, True),
            ("Without it the tile cooks itself in about a minute.", 1, False),
            ("", 0, False),
            ("Never drive a motor straight from a pin.", 0, True),
            ("40 mA limit. The motor wants nearly twice that.", 1, False),
        ])

    content_slide(
        prs, "The one that surprises people",
        lead="Touch input for the price of a wire. The thinking is where it costs you.",
        body=[
            ("reading > baselineAverage() * 1.01", 0, True),
            ("", 0, False),
            ("Threshold is relative, never absolute", 0, True),
            ("Readings drift with humidity and mains hum", 1, False),
            ("Fixed threshold works at 9am, fails at 1pm", 1, False),
            ("", 0, False),
            ("Baseline only learns while untouched", 0, True),
            ("Or a long press teaches it that a finger is normal", 1, False),
        ])

    section_slide(prs, "Inputs, and prior art")

    content_slide(
        prs, "Inputs worth knowing about",
        lead="One table with a sign. Wander over between tasks.",
        body=[
            ("Capacitive touch. A wire. That is task 04", 1, False),
            ("Heart rate (PPG). Useless once the hand moves", 1, False),
            ("Skin conductance (GSR). Relative change only", 1, False),
            ("Flex sensor. The cheap data glove", 1, False),
            ("Pressure (FSR). Calibrate every pad", 1, False),
            ("Your own phone. No soldering at all", 1, False),
        ])

    content_slide(
        prs, "Two rigs that already exist",
        lead="Built here, by students at roughly your stage.",
        body=[
            ("Moving screen, Arduino Uno", 0, True),
            ("Breathes when idle. Retreats when touched", 1, False),
            ("Easing and idle motion do the work. A dozen lines", 1, False),
            ("", 0, False),
            ("Instrumented sock, ESP32", 0, True),
            ("Six force sensors under a foot, batched over Wi-Fi", 1, False),
            ("Calibrate per sensor. Batch your writes", 1, False),
        ])

    section_slide(prs, "Build one signal")

    content_slide(
        prs, "The brief",
        lead="30 minutes. Not long enough to be precious about it.",
        body=[
            ("One actuator. Three messages", 0, True),
            ("Arrived. Something wrong. Finished", 1, False),
            ("", 0, False),
            ("Vary two things only", 0, True),
            ("Rhythm of the pulses", 1, False),
            ("How strong they are", 1, False),
            ("", 0, False),
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
        prs, "Test it",
        lead="Hand your device to another group with the screen turned away.",
        body=[
            ("They can tell all three messages apart.", 1, False),
            ("It does not fire continuously when held.", 1, False),
            ("You know which two got confused, and what would have separated "
             "them.", 1, False),
            ("It still works when they are not looking at it.", 1, False),
        ])

    content_slide(
        prs, "What you actually learn",
        lead="Three things you cannot get from a datasheet.",
        body=[
            ("What things feel like", 0, True),
            ("A motor is a nudge. A solenoid is a knock. A Peltier is slow.", 1, False),
            ("", 0, False),
            ("How to drive one", 0, True),
            ("PWM, direction, debouncing, and why a motor never goes straight "
             "to a pin.", 1, False),
            ("", 0, False),
            ("What to pick", 0, True),
            ("Choosing the actuator before designing the interaction, not in "
             "week 46.", 1, False),
        ])

    title_slide(prs, "Go and touch things",
                "github.com/gust1527/multimodal-actuator-workshop")

    prs.save(OUT)
    print(f"wrote {OUT} ({len(prs.slides._sldIdLst)} slides)")


if __name__ == "__main__":
    build()
