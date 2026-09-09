#!/usr/bin/env python3
"""
Check every diagram.json against the documented Wokwi format.

Worth having, because Wokwi fails SILENTLY: an unknown part type is dropped
without an error, and a malformed connection can stop the whole canvas from
rendering. Both happened here. Run this after any edit.

    python3 validate.py
"""

import json
import glob
import re
import sys

# From docs.wokwi.com/parts/<name>, checked 9 September 2026.
PINS = {
    "wokwi-arduino-uno": set(
        ["5V", "VIN", "GND.1", "GND.2", "GND.3", "AREF", "RESET"]
        + [str(i) for i in range(14)]
        + [f"A{i}" for i in range(6)]
    ),
    "wokwi-relay-module": {"VCC", "GND", "IN", "NC", "COM", "NO"},
    "wokwi-led": {"A", "C"},
    "wokwi-resistor": {"1", "2"},
    "wokwi-servo": {"PWM", "V+", "GND"},
    "wokwi-pushbutton": {"1.l", "1.r", "2.l", "2.r"},
    "wokwi-text": set(),          # decorative, no pins
}

ROUTING = re.compile(r"\*|[vh]-?\d+")


def check(path: str) -> list[str]:
    d = json.load(open(path))
    errs: list[str] = []

    if d.get("version") != 1:
        errs.append("version must be 1")

    types = {p["id"]: p["type"] for p in d["parts"]}
    for p in d["parts"]:
        if p["type"] not in PINS:
            errs.append(f"unknown part type {p['type']!r} (Wokwi will drop it silently)")
        for coord in ("left", "top"):
            if not isinstance(p.get(coord), (int, float)):
                errs.append(f"{p['id']}: missing {coord}")

    for c in d["connections"]:
        if len(c) != 4:
            errs.append(f"connection needs exactly 4 items: {c}")
            continue
        for end in c[:2]:
            if ":" not in end:
                errs.append(f"endpoint must be partId:pin, got {end!r}")
                continue
            pid, pin = end.split(":", 1)
            if pid not in types:
                errs.append(f"unknown part id {pid!r}")
                continue
            valid = PINS.get(types[pid], set())
            if valid and pin not in valid:
                errs.append(f"{types[pid]} has no pin {pin!r}")
        if not isinstance(c[3], list):
            errs.append("the 4th item must be a routing list (use [] to auto-route)")
            continue
        for step in c[3]:
            if not ROUTING.fullmatch(step):
                errs.append(f"bad routing step {step!r}: use v<n>, h<n> or *")
    return errs


if __name__ == "__main__":
    failed = False
    for f in sorted(glob.glob("*/diagram.json")):
        errs = check(f)
        print(f"{f:34} {'OK' if not errs else 'ERRORS'}")
        for e in errs:
            print("    -", e)
            failed = True
    sys.exit(1 if failed else 0)
