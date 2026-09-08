# Photos

Real product photos, pulled from the Labtools component database: the Algolia
`components` index behind the Chomskylab app, which serves images from Firebase
Storage. These are the parts actually in the drawers.

| File | Part | Drawer | In stock |
|---|---|---|---|
| `erm.jpg` | Vibrating Mini Motor Disc | 1E | 117 |
| `piezo.png` | Piezo Element | 6F | 69 |
| `solenoid.jpg` | Mini Push-Pull Solenoid 5V | 3E | 24 |
| `peltier.jpg` | Peltier element / Cooling Pad | 4C | 25 + 35 |
| `transducer.jpg` | Surface Transducer Large | 7F | 12 |
| `servo.jpg` | Servo Tower Pro SG-5010 | 2F | 80 |
| `stepper.jpg` | Stepper motor 28BYJ-48 | 2A | 44 |
| `electromagnet.jpg` | Mini electromagnet | 3D | 17 |
| `hbridge.jpg` | L9110S H-bridge | 2C | 24 |
| `amp.jpg` | PAM8403 amplifier | 11F | 25 |
| `bbpsu.jpg` | YwRobot breadboard supply | 8A | 42 |
| `boneconductor.jpg` | Bone Conductor Transducer | 7F | 23 |
| `fsr.jpg` | Square FSR (Interlink 406) | 4A | 33 |
| `flex.jpg` | Short Flex Sensor | 4B | 8 |
| `pulse.jpg` | Pulse Sensor | 9D | 9 |

No photo for the capacitive pad. There is no part to photograph: it is a wire
and a piece of foil, which is the point.

## Refreshing these

Query the index and download the `image` field. Search key is public and
committed in the Chomskylab app (`src/react_components/Main.tsx`), read-only.

```bash
curl -s -X POST "https://QTEVXHL3O4-dsn.algolia.net/1/indexes/components/query" \
  -H "X-Algolia-API-Key: e7b7f3cb983836187b5eacb1ff7dc19b" \
  -H "X-Algolia-Application-Id: QTEVXHL3O4" \
  -d '{"query":"solenoid","hitsPerPage":3}'
```

Some images come back as WebP behind a `.jpg` name; python-pptx rejects those,
so convert with Pillow before use. Anything missing renders as a dashed PHOTO
frame, so gaps stay visible.

Counts read 8 September 2026 and will drift.
