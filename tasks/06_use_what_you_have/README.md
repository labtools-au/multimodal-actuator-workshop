# Task 06: use what you have

No board, no wiring. The phone in your pocket already has an accelerometer, a
gyroscope, a microphone and a vibration motor. This task finds out which of
them the browser will actually hand you.

## Run it

Everything here needs **HTTPS or localhost**. A `file://` page fails silently,
which is the most common reason "it does not work".

```bash
cd tasks/06_use_what_you_have
python3 -m http.server 8000
```

Open `http://<your-laptop-ip>:8000` on the phone, on the same Wi-Fi. If sensors
stay dead, that is the HTTPS rule: use a tunnel (`ngrok http 8000`, or
`cloudflared tunnel --url http://localhost:8000`).

## What actually works

Checked against caniuse and MDN in September 2026, not assumed.

| | Android Chrome | iOS Safari |
|---|---|---|
| `navigator.vibrate` | yes | **no, at any version** |
| `devicemotion` | yes | yes, after a permission call |
| `getUserMedia` (mic) | yes | yes |

**The vibration one matters.** WebKit has never shipped the Vibration API.
caniuse lists Safari 3.1 through 27 as unsupported, desktop and iOS alike, and
Chrome and Firefox on iOS are Safari underneath so they inherit the gap. If
your project plan says "the phone buzzes", it works on half the room's phones
and no iPhones. Better to find that out now than in week 46.

**Motion needs a tap on iOS.** Since iOS 13, `DeviceMotionEvent.requestPermission()`
must be called from inside a real user gesture, and it must be a secure context.
Call it on page load and it throws. That is why the demo puts it on a button.

## Things to try

1. Open it on an Android phone and an iPhone side by side. One vibrates, one
   is dead. That is a platform decision, not a bug in your code.

2. Put the phone flat and read `|a|`. It sits near 9.8, because gravity never
   switches off. Any "is it moving" test works relative to that resting value,
   the same problem as the capacitive baseline in task 04.

3. Use the microphone as a trigger rather than a recorder: fire when RMS
   crosses a threshold. Then try it in a noisy room and watch your threshold
   stop working.

4. Combine two. Shake to arm, clap to fire. Two cheap signals together beat one
   good one, which is the same redundancy argument as the surface transducer.

## Other things that are already sensors

Worth knowing about, in rough order of how easily you can get data out.

**Your laptop trackpad is a pressure sensor.** Force Touch trackpads report
real pressure, and the web exposes it: a `mousedown`/`mousemove` event carries
`webkitForce` in Safari, and Pointer Events carry `pressure` (0 to 1) where the
hardware supports it. A trackpad genuinely can weigh a light object placed on
it, which is a fun demo and a bad scale.

**Smartwatches are the best sensors nobody can reach.** Apple Watch and Garmin
both have optical heart rate, accelerometer, gyroscope and skin temperature.
The catch is access: neither streams live to a web page. Apple needs a
companion watchOS app in Swift; Garmin needs a Connect IQ app or a pull from
the Garmin Connect API after the fact. Fine for a project that analyses a
session afterwards. Not viable for anything that reacts in real time inside
two weeks.

**A webcam is a heart rate sensor.** Remote photoplethysmography reads the tiny
colour shift in a face as blood moves. Works from `getUserMedia` plus a canvas,
in any browser, with no extra hardware. Noisy and light-dependent, which is a
feature for teaching: it makes signal quality visible.

**Bluetooth heart rate straps are the one that actually streams.** Web
Bluetooth reaches the standard Heart Rate Service directly from Chrome. Not
Safari, so Android or a laptop. If a project needs live physiological data
without soldering, this is the realistic route.

**The keyboard is a timing sensor.** Keystroke rhythm, dwell and flight times
need no permission at all.
