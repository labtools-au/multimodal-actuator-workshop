#!/usr/bin/env python3
"""
Build an AU Department of Computer Science .potx-style template.

The point of this file is EDITABILITY. Everything that repeats lives on the
slide master, so:

  * the AU footer is defined ONCE, not copied onto every slide
  * slides use real TITLE and BODY placeholders, so PowerPoint's outline view
    works and you can retype content without hunting for text boxes
  * restyling the deck means editing the master, not 19 slides

Run this to regenerate `au-template.pptx`, then build_deck.py fills it in.
"""

from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path
import copy

HERE = Path(__file__).parent
OUT = HERE / "au-template.pptx"

# Sampled from the department's own deck, not guessed.
AU_BLUE = RGBColor(0x00, 0x25, 0x46)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x00, 0x00, 0x00)
GREY = RGBColor(0x59, 0x59, 0x59)

FONT = "Arial"
SW, SH = Pt(959.76), Pt(540)
L = Pt(72)

# Edit these two lines to re-brand the whole deck.
COURSE_LINE = ("MULTIMODAL INTERACTION", "PROTOTYPING WORKSHOP")
BYLINE = ("GUSTAV SIMONSEN", "TEACHING ASSISTANT")


_SCRATCH = {"prs": None, "slide": None}


def _shapes_of(container):
    """Layouts cannot add shapes. Build on a scratch slide instead; move_to_layout
    then relocates the XML onto the layout."""
    from pptx.shapes.shapetree import LayoutShapes
    if isinstance(container, LayoutShapes) or container.__class__.__name__ == "LayoutShapes":
        return _SCRATCH["slide"].shapes
    return container


def move_to_layout(layout, n):
    """Move the last n shapes off the scratch slide onto `layout`."""
    src = _SCRATCH["slide"].shapes._spTree
    dst = layout.shapes._spTree
    kids = [c for c in src if c.tag.endswith('}sp') or c.tag.endswith('}pic')]
    for el in kids[-n:]:
        src.remove(el)
        dst.append(el)


def _clear(shapes):
    for sh in list(shapes):
        sh._element.getparent().remove(sh._element)


def _txt(container, x, y, w, h, lines, size, color, bold=False, spacing=1.15):
    tb = _shapes_of(container).add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.line_spacing = spacing
        for r in p.runs:
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color
            r.font.name = FONT
    return tb


def au_signature(container, light=False):
    """The fixed AU block. Defined once per layout, inherited by every slide."""
    wm = HERE / ("wordmark_light.png" if light else "wordmark_dark.png")
    seal = HERE / ("seal_light.png" if light else "seal_dark.png")
    ink = WHITE if light else INK

    sh = _shapes_of(container)
    sh.add_picture(str(wm), Pt(27), Pt(487), width=Pt(163))
    sh.add_picture(str(seal), Pt(884), Pt(470), height=Pt(56))
    _txt(container, Pt(360), Pt(492), Pt(200), Pt(40), list(COURSE_LINE), 7, ink)
    _txt(container, Pt(600), Pt(492), Pt(220), Pt(40), list(BYLINE), 7, ink)


def style_ph(ph, size, bold, color, upper=False, anchor=MSO_ANCHOR.TOP):
    """Style a placeholder so typed text picks up AU styling automatically."""
    tf = ph.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for p in tf.paragraphs:
        p.line_spacing = 0.98 if bold else 1.28
        f = p.font
        f.size = Pt(size)
        f.bold = bold
        f.color.rgb = color
        f.name = FONT


def build():
    prs = Presentation()
    prs.slide_width, prs.slide_height = SW, SH
    master = prs.slide_masters[0]

    # scratch slide: the only place python-pptx lets us author shapes
    _SCRATCH["prs"] = prs
    _SCRATCH["slide"] = prs.slides.add_slide(master.slide_layouts[6])

    # Master carries nothing visual itself; each layout paints its own ground
    # so the blue title layout and the white content layouts can differ.
    _clear(master.shapes)
    for ph in list(master.placeholders):
        ph._element.getparent().remove(ph._element)

    layouts = master.slide_layouts

    # ---- 0: Title (blue) --------------------------------------------------
    lay = layouts[0]
    _clear(lay.shapes)
    lay.background.fill.solid()
    lay.background.fill.fore_color.rgb = AU_BLUE
    _rebuild_title_layout(lay)
    au_signature(lay.shapes, light=True)
    move_to_layout(lay, 4)   # wordmark, seal, course line, byline

    # ---- 1: Title and Content (white) ------------------------------------
    lay = layouts[1]
    _clear(lay.shapes)
    lay.background.fill.solid()
    lay.background.fill.fore_color.rgb = WHITE
    _rebuild_content_layout(lay)
    au_signature(lay.shapes, light=False)
    move_to_layout(lay, 5)   # rule + 4 signature shapes

    # ---- 2: Section Header (white) ---------------------------------------
    lay = layouts[2]
    _clear(lay.shapes)
    lay.background.fill.solid()
    lay.background.fill.fore_color.rgb = WHITE
    _rebuild_section_layout(lay)
    au_signature(lay.shapes, light=False)
    move_to_layout(lay, 5)

    # ---- 3: Two Content — used for the bench slides -----------------------
    lay = layouts[3]
    _clear(lay.shapes)
    lay.background.fill.solid()
    lay.background.fill.fore_color.rgb = WHITE
    _rebuild_bench_layout(lay)
    au_signature(lay.shapes, light=False)
    move_to_layout(lay, 5)

    # The four AU layouts are 0-3; the stock ones after them are left in place
    # (removing them means rewriting package relationships for little gain).
    # Use "Title Slide", "Title and Content", "Section Header", "Two Content".

    # remove the scratch slide properly: drop the sldId, the relationship, and
    # the part itself. Removing only the sldId leaves an orphan slide1.xml that
    # collides on the next save.
    sld_lst = prs.slides._sldIdLst
    sldId = list(sld_lst)[0]
    rId = sldId.rId
    sld_lst.remove(sldId)
    prs.part.drop_rel(rId)

    prs.save(OUT)
    print(f"wrote {OUT}")


# --- layout builders -------------------------------------------------------
# python-pptx cannot add placeholders directly, so we clone the XML of the
# stock ones and reposition. Each layout ends up with real TITLE/BODY
# placeholders that PowerPoint treats as first-class editable fields.

from pptx.oxml.ns import qn


def _no_bullets():
    """Nine outline levels, all left-aligned with no bullet glyph and no indent.
    Placeholders inherit PowerPoint's default bulleted list otherwise, which is
    not the department's style."""
    return "".join(
        f'<a:lvl{i}pPr marL="0" indent="0" algn="l"><a:buNone/></a:lvl{i}pPr>'
        for i in range(1, 10))


def _mk_ph(layout, idx, ph_type, name, x, y, w, h):
    """Create a placeholder on a layout via raw XML."""
    spTree = layout.shapes._spTree
    xml = (
        '<p:sp xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<p:nvSpPr><p:cNvPr id="{100+idx}" name="{name}"/>'
        '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
        f'<p:nvPr><p:ph type="{ph_type}" idx="{idx}"/></p:nvPr></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/>'
        f'<a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm></p:spPr>'
        '<p:txBody><a:bodyPr wrap="square"><a:normAutofit/></a:bodyPr>'
        '<a:lstStyle/><a:p><a:endParaRPr/></a:p></p:txBody></p:sp>'
    )
    from pptx.oxml import parse_xml
    sp = parse_xml(xml)
    spTree.append(sp)
    return layout.shapes[-1]


def _rule(container, x, y, w=Pt(46), color=INK):
    s = _shapes_of(container).add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Pt(2.5))
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def _rebuild_title_layout(lay):
    t = _mk_ph(lay, 0, "ctrTitle", "Title", L, Pt(200), Pt(820), Pt(120))
    style_ph(t, 54, True, WHITE)
    s = _mk_ph(lay, 1, "subTitle", "Subtitle", L, Pt(330), Pt(760), Pt(60))
    style_ph(s, 20, False, WHITE)


def _rebuild_content_layout(lay):
    t = _mk_ph(lay, 0, "title", "Title", L, Pt(58), Pt(830), Pt(56))
    style_ph(t, 32, True, INK)
    _rule(lay.shapes, L, Pt(118))
    b = _mk_ph(lay, 1, "body", "Body", L, Pt(150), Pt(790), Pt(310))
    style_ph(b, 17, False, INK)


def _rebuild_section_layout(lay):
    _rule(lay.shapes, L, Pt(130))
    t = _mk_ph(lay, 0, "title", "Section Title", L, Pt(230), Pt(820), Pt(130))
    style_ph(t, 44, True, INK)


def _rebuild_bench_layout(lay):
    t = _mk_ph(lay, 0, "title", "Bench Title", L, Pt(58), Pt(600), Pt(60))
    style_ph(t, 30, True, INK)
    _rule(lay.shapes, L, Pt(118))
    b = _mk_ph(lay, 1, "body", "Bench Description", L, Pt(134), Pt(520), Pt(300))
    style_ph(b, 16, False, INK)
    s = _mk_ph(lay, 2, "body", "Spec Block", Pt(650), Pt(168), Pt(250), Pt(240))
    style_ph(s, 12, False, INK)


if __name__ == "__main__":
    build()
