#!/usr/bin/env python3
"""
Generate the QR codes the deck puts on screen.

A URL on a slide is only useful if someone types it correctly from the back of
a room. A QR code is the difference between "I will look at that later" and
thirty phones opening it while you talk.

Needs the qrcode package:

    python3 -m venv .venv && .venv/bin/pip install "qrcode[pil]"
    .venv/bin/python make_qr.py
"""

import qrcode
from pathlib import Path
from qrcode.constants import ERROR_CORRECT_M

HERE = Path(__file__).parent

CODES = {
    # name            url
    "qr_sensors": "https://sensors.chomskylab.dk",
    "qr_repo": "https://github.com/labtools-au/multimodal-actuator-workshop",
}


def build(name: str, url: str) -> None:
    qr = qrcode.QRCode(
        version=None,                 # smallest that fits, so modules stay big
        error_correction=ERROR_CORRECT_M,
        box_size=14,
        border=2,                     # quiet zone; below 2 scanners struggle
    )
    qr.add_data(url)
    qr.make(fit=True)
    # Black on white: the deck has no accent colour, and a tinted QR code
    # scans worse under projector light.
    img = qr.make_image(fill_color="black", back_color="white")
    out = HERE / f"{name}.png"
    img.save(out)
    print(f"{out.name:16} {img.size[0]}x{img.size[1]}  {url}")


if __name__ == "__main__":
    for name, url in CODES.items():
        build(name, url)
