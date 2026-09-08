# Photos

Real product photos, pulled from the Labtools component database (the Algolia
`components` index behind the Chomskylab app, which serves images from Firebase
Storage). These are the actual parts in the drawers, not stand-ins.

| File | Part | Drawer | In stock |
|---|---|---|---|
| `erm.jpg` | Vibrating Mini Motor Disc | 1E | 117 |
| `solenoid.jpg` | Mini Push-Pull Solenoid 5V | 3E | 24 |
| `piezo.png` | Piezo Element | 6F | 69 |
| `peltier.jpg` | Peltier element / Cooling Pad | 4C | 25 small, 35 big |
| `transducer.jpg` | Surface Transducer Large | 7F | 12 |

No photo for the capacitive pad, because there is no part to photograph. It is
a wire and a piece of foil, which is the point.

To refresh or add one, query the index and download the `image` field, or drop
a file in named after the slot. Anything missing renders as a dashed PHOTO
frame, so gaps stay visible.

```bash
cd ../deck && python3 build_deck.py && python3 add_notes.py
```

Stock counts were read on 8 September 2026 and will drift. Re-check before the
session if the numbers matter.
