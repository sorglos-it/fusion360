# fusion360-printgear

[![Fusion 360](https://img.shields.io/badge/Autodesk-Fusion%20360-F60?logo=autodesk&logoColor=white)](#start-in-3-steps)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-0078D6?logo=windows&logoColor=white)](#start-in-3-steps)
[![Languages](https://img.shields.io/badge/UI-DE%20%7C%20EN%20%7C%20ES%20%7C%20FR%20%7C%20IT-4c1.svg)](#languages)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-00457C.svg?logo=paypal)](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)

A Fusion 360 add-in that makes **involute gears for 3D printing** — and asks about the nozzle instead of the module.
Pick one point for a gear or a meshing pair, several points for a whole gear train, and set the ratio you want.

| Folder | Purpose | Language | Start | Build |
|---|---|---|---|---|
| `apps/desktop-printgear/PrintGear` | the add-in: printable gears, pairs and gear trains | Python 3 (the one inside Fusion) | copy into Fusion's add-ins folder, then *Run* | – (runs as is) |

## Start in 3 steps

1. Clone or copy this repository and take the folder `apps/desktop-printgear/PrintGear`.
2. Copy it into Fusion's add-ins folder, so that `PrintGear\PrintGear.py` ends up one level below it:

   | OS | Path |
   |---|---|
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/` |

3. In Fusion: **Utilities → ADD-INS → Add-Ins**, select the entry, tick *Run on Startup*, press **Run**. The button
   appears on the **SOLID** tab in the **CREATE** panel, with the version in brackets — *PrintGear (1.0.0)*.

You need Autodesk Fusion 360 (Windows or macOS), any recent version — nothing else to install.

## Update

Stop the add-in in Fusion first, otherwise the running one stays in memory. Then replace the folder, keeping its name:
Fusion requires `<Folder>/<Folder>.py` and `<Folder>/<Folder>.manifest` to match.

## Usage

1. Sketch the points where the gear axes go, and finish the sketch.
2. Click the points **in order** — the first one is the input, the last one the output.
3. Click the PrintGear icon. Whatever you had selected is already in the dialog.
4. Set the nozzle, the size of the first gear and the ratio; press **Create**.

All points have to be at the same height: gears only mesh when they are coplanar, so the first point sets the plane and
the others only contribute their X and Y.

## The nozzle decides the module

Whether printed teeth survive depends on how many extrusions fit across the tooth root. So the module follows from the
nozzle — **module = nozzle × 2.5**:

| Nozzle | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 |
|---|---|---|---|---|---|
| **Module** | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 |

Past 1.0 mm the layer height decides the surface, not the nozzle, so the list stops there. The factor is adjustable —
2.0 for fine work, 3.0 when something has to pull — and the module can still be typed in directly to match an existing
part.

What you get:

- **Ratio as the input** — tooth counts follow from it, not the other way round.
- **One gear, a pair or a train** — a mating gear at the correct centre distance, or a whole train through the points
  you picked, in that order.
- **Straight, helical or herringbone** — herringbone cancels the sideways push and prints without support.
- **Real involute flanks with root fillets**, because a printed tooth breaks at the root.
- **Profile shift below 17 teeth** — undercut teeth are filled back out and the centre distance is corrected.
- **Backlash you can dial in** — 0.25 mm by default, half from each gear.
- **Printable tips** — a tooth that would end in a knife edge is cut back to one extrusion width.
- **Bodies or components** — one component per gear for an assembly, or plain bodies.
- **Shaft bore** cut after the body, so a helical gear still gets a straight bore.

## Dialog

### Print setup

| Field | Meaning |
|---|---|
| **Nozzle** | 0.2 / 0.4 / 0.6 / 0.8 / 1.0 mm, or *set the module myself*. |
| **Module factor** | Module = nozzle × factor. 2.5 by default; 2.0 fine, 3.0 sturdy. |
| **Module** | What that works out to. Editable only when you set the module yourself. |
| **Backlash** | Total play between two meshing gears, 0.25 mm by default. Each gear gives up half. Raise it if your prints come out over size. |
| **Face width** | How thick the gears are. |

### Teeth

| Field | Meaning |
|---|---|
| **Tooth form** | `Straight`, `Helical`, `Herringbone (V)`. |
| **Helix angle** | 45° by default. Helical runs quieter but pushes the shaft sideways; herringbone cancels that push and prints without support. |
| **Pressure angle** | 20° standard, 25° for thicker roots — often the better trade in plastic. |
| **Profile shift for small gears** | Below about 17 teeth the flank is undercut and the root goes thin. This fills those teeth back out and corrects the centre distance. |

### Gears

| Field | Meaning |
|---|---|
| **Size given as** | Number of teeth, or pitch diameter. |
| **Teeth / pitch diameter** | The first gear. Everything else follows from the ratio and the points. |
| **Ratio** | Reduction from the first gear to the last one. |
| **Points mean** | How the picked points are read — see below. |
| **Add a second gear** | Only with a single point: puts a mating gear against the first. |
| **Direction** | Where that second gear sits, measured from the X axis: **180°** in a straight line, **90°** round a corner. |

### Output

| Field | Meaning |
|---|---|
| **Bore** | Shaft hole through every gear; 0 leaves them solid. |
| **Each gear as a component** | One component per gear, or plain bodies in the active component. |
| **Preview** | `Circles` (instant: size and position), `Full geometry` (what you will get, slow), `Off`. |

Under the dialog a report shows the module, every gear's tooth count and pitch diameter, the centre distances, the
ratio you actually get, and any warnings.

## Exact ratio or exact positions

The centre distance of two meshing gears is fixed by their tooth counts — `a = m (z₁ + z₂) / 2` — and tooth counts
are whole numbers. So arbitrary points and an exact ratio cannot both be honoured. **Points mean** says which one
gives:

- **Direction — ratio stays exact.** The points set the direction from one axis to the next, the meshing sets the
  distance. Every pair meshes perfectly; the gears drift off your points by up to half a module each.
- **Exact positions — ratio approximate.** The gears land on your points; the ratio is whatever falls out and the play
  varies a little from pair to pair.

Either way the report says what you get and warns when the ratio or a centre distance has moved. In a simple train the
gears in between are **idlers**: they only reverse the direction. The ratio comes from the first and last gear alone,
so the middle gears are sized to reach your points.

## Why the teeth look like that

- **Root fillets** of 0.38 × module, rounder than the 0.25 of a cut gear, built as a true tangent arc — no notch.
- **Extra root clearance** of 0.35 × module instead of 0.25, because the mating tip prints slightly over size and the
  root slightly under.
- **Truncated tips:** a small gear with a lot of profile shift runs out of tooth before the tip circle. Instead of a
  knife edge no nozzle can print, the tip is cut back to at least one extrusion width, and the report says so.
- **Chord tolerance instead of a fixed point count:** the outline is one closed spline with 0.02 mm chord tolerance —
  far finer than any nozzle — so a 12-tooth pinion gets what it needs and a 120-tooth wheel does not drown Fusion in
  points.

## Languages

The interface follows **Preferences → General → User Language** in Fusion: German, English, Spanish, French or
Italian, anything else falls back to English. The texts live in `apps/desktop-printgear/PrintGear/lang/<code>.xml`; `en.xml` is
the reference. To add a language, copy `en.xml`, translate it, name it after the two-letter code and add the code to
`SUPPORTED_LANGUAGES` and `FUSION_LANGUAGE_MAP` in `printgear_core.py`.

## Development

The gear mathematics lives in `printgear_math.py` and imports nothing from Fusion, so it runs in a normal Python 3
(standard library only):

```bash
python apps/desktop-printgear/tests/test_geometry.py
python tools/printgear/make_icons.py
```

The tests check the involute round trip, the outline against root and tip circles, tip truncation, the chord
tolerance, backlash, train layout in both modes, and roll meshing pairs through a full tooth pitch looking for
collisions — which proves the phasing. The icons are a real gear pair rasterised straight from `printgear_math`. Both
scripts find the add-in in `apps/desktop-printgear/PrintGear`; set `PRINTGEAR_ADDIN_DIR` to point them at an installed copy
instead.

## Related

[fusion360-dovetail](https://github.com/sorglos-it/fusion360-dovetail) turns sketch lines into printable joints.
[fusion360-addin-template](https://github.com/sorglos-it/fusion360-addin-template) is the scaffolding this add-in was
built from.

## License

MIT — see [LICENSE](LICENSE). © 2026 Sorglos Thomas Weirich.

## Donate via PayPal

If this add-in saved you time, a donation supports further development. Thank you!

**[➡️ Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)**
