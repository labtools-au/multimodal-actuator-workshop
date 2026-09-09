#!/usr/bin/env python3
"""
Create component requests in the Chomskylab app for the multimodal workshop.

Writes exactly what the app's own requestComponent() writes, so the requests
show up in the normal place and lab staff see them as usual:

  users/{yourEmail}/requestedComponents/{componentId}
  latestRequests/{auto}

Run it:

    CHOMSKYLAB_PASSWORD='...' python3 request_components.py          # dry run
    CHOMSKYLAB_PASSWORD='...' python3 request_components.py --commit # for real

Dry run prints the exact writes and touches nothing.
"""

import json
import os
import sys
import urllib.error
import urllib.request

EMAIL = "gustav@gearloose.dk"
PROJECT = "chomskylab-app"
API_KEY = "AIzaSyBB"  # replaced at runtime from the repo .env, see load_api_key

ENV_PATH = os.path.expanduser("~/Git_projects/Chomskylab/.env")

# Quantities for one session: roughly 12 pairs, one working set per task,
# plus a couple of spares on the things that get handled hardest.
#
# Deliberately NOT requesting everything the deck mentions: servo, stepper and
# electromagnet stay in the drawers for other people, since no task drives them.
REQUESTS = [
    # id,                          name,                              qty, drawer, why
    ("FrOd2LNdyxj7xF8ED4NW", "Arduino Uno",                            14, "5A", "one per pair + 2 spare"),
    ("a6V8LN0MqkrZPcmtEjUe", "Vibrating Mini Motor Disc",              16, "1E", "task 01, leads shear"),
    ("0HOfv8sfKxgdxIfOg4IN", "Mini Push-Pull Solenoid - 5V",            6, "3E", "task 02, shared station"),
    ("llXPFhGw68nPrmQxLUoX", "Peltier element / Cooling Pad smal",      4, "4C", "task 03, needs bench PSU"),
    ("4EEyxbMBnFUvU9esmMer", "Piezo Element",                          14, "6F", "compare against the ERM"),
    ("HoaoqJe9pKVJEvQFYAIG", "Surface Transducer - Large",              4, "7F", "only 12 exist, share"),
    ("nq6xC7R05YG21m6EdaGO", "YwRobot Breadboard Powersupply",         14, "8A", "anything past an LED"),
    ("67eV4Yif3AacqJBso4La", "L9110S H-bridge Dual DC Stepper Motor Driver Controller",
                                                                        6, "2C", "Peltier direction"),
    ("K7SATl2y51UsrrF3Uxr0", "PAM8403 Stereo Audio Amplifier Module (2x 3W output)",
                                                                        4, "11F", "drives the transducer"),
    ("tiHWKyDvRoCXGEcMzB7Z", "Square Force-Sensitive Resistor (FSR) - Interlink 406",
                                                                        8, "4A", "input table"),
    ("VaH1SWLKxrVDG3W2fJnq", "Short Flex Sensor",                       4, "4B", "only 8 exist, share"),
    ("KjT4dr1Sxn6Hq783GXMm", "Pulse Sensor",                            4, "9D", "only 9 exist, share"),
]


def load_api_key() -> str:
    with open(ENV_PATH) as f:
        for line in f:
            if line.startswith("REACT_APP_FIREBASE_API_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit(f"No Firebase API key in {ENV_PATH}")


def post(url: str, payload: dict, token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers=headers, method="POST"
    )
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        sys.exit(f"HTTP {e.code}: {body[:400]}")


def sign_in(api_key: str, password: str) -> str:
    res = post(
        f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}",
        {"email": EMAIL, "password": password, "returnSecureToken": True},
    )
    return res["idToken"]


def main() -> None:
    commit = "--commit" in sys.argv
    api_key = load_api_key()

    total = sum(q for _, _, q, _, _ in REQUESTS)
    print(f"{'COMMIT' if commit else 'DRY RUN'}: {len(REQUESTS)} components, {total} units, as {EMAIL}\n")
    for _, name, qty, drawer, why in REQUESTS:
        print(f"  {qty:3} x  {name[:52]:54} {drawer:5} {why}")

    if not commit:
        print("\nNothing written. Re-run with --commit to create the requests.")
        return

    password = os.environ.get("CHOMSKYLAB_PASSWORD")
    if not password:
        sys.exit("\nSet CHOMSKYLAB_PASSWORD to commit.")

    token = sign_in(api_key, password)
    base = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents"
    print()

    for cid, name, qty, _, _ in REQUESTS:
        # Same two writes the app makes. Not batched: urllib has no batch
        # helper, and a partial failure is visible rather than silent.
        doc = {
            "fields": {
                "componentID": {"stringValue": cid},
                "componentName": {"stringValue": name},
                "dateRequested": {"timestampValue": None},
                "amountRequested": {"integerValue": str(qty)},
            }
        }
        # Firestore REST rejects a null timestamp, so send server time as now.
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        doc["fields"]["dateRequested"] = {"timestampValue": now}

        url = (
            f"{base}/users/{EMAIL}/requestedComponents?"
            f"documentId={cid}"
        )
        post(url, doc, token)

        post(
            f"{base}/latestRequests",
            {
                "fields": {
                    "componentID": {"stringValue": cid},
                    "componentName": {"stringValue": name},
                    "dateRequested": {"timestampValue": now},
                    "userEmail": {"stringValue": EMAIL},
                    "amount": {"integerValue": str(qty)},
                }
            },
            token,
        )
        print(f"  requested {qty:3} x {name[:56]}")

    print(f"\nDone. Check the app's profile page to confirm all {len(REQUESTS)} appear.")


if __name__ == "__main__":
    main()
