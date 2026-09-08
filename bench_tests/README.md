# Bench tests

One sketch per bench, each proving that **one component works**. Nothing here
is a teaching exercise. These exist so you can set the room up and know, before
students arrive, that all six benches actually run.

Run these the morning of the workshop. If a bench fails and you cannot fix it in
five minutes, pull it. Five working benches beat six with a mystery.

| Bench | Sketch | Passes when |
|---|---|---|
| 01 | [`01_erm_motor`](01_erm_motor) | Motor buzzes on serial input 1, 2 or 3 |
| 02 | [`02_lra_piezo`](02_lra_piezo) | Driver found, effects cycle audibly |
| 03 | [`03_solenoid`](03_solenoid) | Audible click every 2 s, board does not reset |
| 04 | [`04_capacitive_touch`](04_capacitive_touch) | Servo reacts to a finger on the pad |
| 05 | [`05_peltier`](05_peltier) | One face warms, then cools after reversing |
| 06 | [`06_transducer`](06_transducer) | 40 Hz felt through the plate, 400 Hz heard |

If something fails, go to [`../utils`](../utils) before you start reading code.
