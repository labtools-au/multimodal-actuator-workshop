# Photos

Drop actuator photos here and re-run the deck build. Empty slots render as a
dashed **PHOTO** frame on the slide, so it stays obvious what is still missing.

| Filename | Slide | What to shoot |
|---|---|---|
| `erm` | Coin motor | The coin motor next to a 1 kr coin for scale |
| `lra_piezo` | LRA and piezo disc | Both parts side by side, with the DRV2605L breakout |
| `solenoid` | Solenoid | The solenoid with its plunger visible, ideally mid-throw |
| `captouch` | Capacitive pad | A wire taped behind foil. Make it look as cheap as it is |
| `peltier` | Peltier tile | The tile with its heatsink attached |
| `transducer` | Transducer | The exciter pressed against its plate |

Any of `.jpg`, `.jpeg` or `.png`. The build scales to fit the frame and keeps
the aspect ratio, so exact dimensions do not matter. Landscape, roughly 4:3,
works best. Shoot on a plain background.

```bash
cd ../deck && python3 build_deck.py && python3 add_notes.py
```
