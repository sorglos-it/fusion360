# fusion360-printgear

[![Fusion 360](https://img.shields.io/badge/Autodesk-Fusion%20360-F60?logo=autodesk&logoColor=white)](#requirements)
[![Type](https://img.shields.io/badge/type-add--in-0b7285.svg)](#installation)
[![Languages](https://img.shields.io/badge/UI-DE%20%7C%20EN%20%7C%20ES%20%7C%20FR%20%7C%20IT-4c1.svg)](#languages)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-0078D6?logo=windows&logoColor=white)](#requirements)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-00457C.svg?logo=paypal)](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)

A Fusion 360 add-in that makes **involute gears for 3D printing**, and asks about the nozzle instead of the module.

Nobody printing a gear cares what the module is. What they care about is whether the teeth survive, and that is decided by how many extrusions fit across the tooth root. So the module follows from the nozzle — **module = nozzle × 2.5** — and the five sizes worth having are on a dropdown:

| Nozzle | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 |
|---|---|---|---|---|---|
| **Module** | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 |

Past 1.0 mm the layer height decides the surface, not the nozzle, so that is where the list stops. The factor is adjustable — 2.0 for fine work, 3.0 when something has to pull — and the module can still be typed in directly if you are matching an existing part.

What you actually set is the **ratio**. Pick one point and you get one gear, or a meshing pair. Pick several points and you get a whole train: first point drives, last point is driven, ratio held between those two.

See also **[fusion360-dovetail](https://github.com/sorglos-it/fusion360-dovetail)** — sketch lines into printable joints — and **[fusion360-addin-template](https://github.com/sorglos-it/fusion360-addin-template)**, the scaffolding this add-in was built from.

## Features

- **Nozzle-driven module** — pick the nozzle, get a module whose teeth that nozzle can actually lay down
- **Ratio is the input** — tooth counts follow from it, not the other way round
- **One point, one gear** — or tick a box and get the mating gear with it, at the correct centre distance
- **Several points, a whole train** — in the order you picked them, ratio carried from the first to the last
- **Straight, helical or herringbone** — herringbone cancels the axial thrust and prints without support
- **Real involute flanks** — with root fillets, because a printed tooth breaks at the root
- **Profile shift below 17 teeth** — undercut teeth get filled back out, and the centre distance is corrected for it
- **Backlash you can dial in** — 0.25 mm by default, taken half from each gear so a pair ends up with exactly that
- **Tips that can be printed** — a tooth that would come to a knife edge is truncated to one extrusion width
- **Bodies or components** — one component per gear when you want an assembly, plain bodies when you do not
- **Shaft bore** — cut after the body, so a helical gear still gets a straight bore
- **Live preview** — circles while you tune, full geometry on demand
- **Five languages** — German, English, Spanish, French, Italian, picked from the Fusion setting
- **No dependencies** — pure Python standard library, nothing to install

## Requirements

- Autodesk Fusion 360 (Windows or macOS), any recent version
- Nothing else — the add-in uses only Python modules that ship with Fusion

## Installation

1. Clone this repository and use the `PrintGear` folder as it is.
2. Copy it into the Fusion add-ins directory, so that `PrintGear\PrintGear.py` ends up one level below it:

   | OS | Path |
   |---|---|
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/` |

3. In Fusion: **Utilities → ADD-INS → Add-Ins**, select the entry, tick *Run on Startup*, press **Run**.
4. The button appears on the **SOLID** tab in the **CREATE** panel, with the installed version in brackets after its name — *PrintGear (1.0.0)*.

Replacing an older copy: stop the add-in in Fusion first, otherwise the running one stays in memory. Keep the folder name and the file names in sync — Fusion requires `<Folder>/<Folder>.py` and `<Folder>/<Folder>.manifest` to match.

## Usage

1. Sketch the points where the gear axes go, and finish the sketch.
2. Click the points **in order** — the first one is the input, the last one the output.
3. Click the PrintGear icon. Whatever you had selected is already in the dialog.
4. Set the nozzle, the size of the first gear and the ratio; press **Create**.

All the points have to be at the same height. Gears only mesh when they are coplanar, so the Z of the first point sets the plane everything is built on and the rest contribute only their X and Y.

## Dialog

### Print setup

| Field | Meaning |
|---|---|
| **Nozzle** | 0.2 / 0.4 / 0.6 / 0.8 / 1.0 mm, or *set the module myself*. |
| **Module factor** | Module = nozzle × factor. 2.5 by default; 2.0 fine, 3.0 sturdy. |
| **Module** | What that works out to. Editable only when you took the module into your own hands. |
| **Backlash** | Total play between two meshing gears, 0.25 mm by default. Each gear gives up half, so the pair ends up with exactly this. Raise it if your prints come out over size. |
| **Face width** | How thick the gears are. |

### Teeth

| Field | Meaning |
|---|---|
| **Tooth form** | `Straight`, `Helical`, `Herringbone (V)`. |
| **Helix angle** | 45° by default. Helical runs quieter but pushes the shaft sideways; herringbone cancels that push and prints without support. |
| **Pressure angle** | 20° standard, 25° for thicker roots — often the better trade in plastic. |
| **Profile shift for small gears** | Below about 17 teeth the flank is undercut and the root goes thin. This fills those teeth back out and corrects the centre distance to match. |

### Gears

| Field | Meaning |
|---|---|
| **Size given as** | Number of teeth, or pitch diameter. |
| **Teeth / pitch diameter** | The first gear. Everything else follows from the ratio and the points. |
| **Ratio** | Reduction from the first gear to the last one. |
| **Points mean** | How the picked points are read — see below. |
| **Add a second gear** | Only with a single point: puts a mating gear against the first. |
| **Direction** | Where that second gear sits, measured from the X axis. **180°** puts the two in a straight line, **90°** puts them round a corner. |

### Output

| Field | Meaning |
|---|---|
| **Bore** | Shaft hole through every gear, 0 leaves them solid. |
| **Each gear as a component** | One component per gear, or plain bodies in the active component. |
| **Preview** | `Circles` (instant, shows size and position), `Full geometry` (what you will get, slow), `Off`. |

Under the dialog is a running report: module, every gear's tooth count and pitch diameter, the centre distances, the ratio you are actually getting, and any warnings.

## The one thing that cannot be exact

A gear train has to satisfy two things that generally disagree. The centre distance between two meshing gears is fixed by their tooth counts — `a = m (z₁ + z₂) / 2` — and tooth counts are whole numbers. So an arbitrary set of points and an exact ratio cannot both be honoured. **Points mean** is where you say which one gives:

- **Direction — ratio stays exact.** The points set the direction from one axis to the next, the meshing sets the distance. You get exactly the ratio you asked for and every pair meshes perfectly; the gears drift off your points by up to half a module each.
- **Exact positions — ratio approximate.** The gears land on your points. Tooth counts are whatever reaches them, so the ratio is whatever falls out and the play varies a little from pair to pair.

Either way the report tells you what you are getting, and warns when the ratio or a centre distance has moved.

Worth knowing about trains: in a simple train the gears in between are **idlers**. They reverse the direction and nothing else — the ratio is set by the first and last gear alone. So the middle gears are sized to reach the points you dropped them on, and only the ends carry the ratio.

## Why the teeth look like that

- **Root fillets.** A printed tooth breaks at the root, and the fillet is free — it is 0.38 × module here, rounder than the 0.25 of a cut gear. It is constructed as a true tangent arc between the flank and the root circle, so it never leaves a notch.
- **A little extra root clearance.** 0.35 × module rather than the textbook 0.25, because the mating tip prints slightly over size and the root slightly under.
- **Truncated tips.** A small gear with a lot of profile shift runs out of tooth before it reaches the nominal tip circle. Rather than draw a knife edge no nozzle can print, the tip is cut back until it is at least one extrusion wide, and the report says so.
- **Chord tolerance, not a fixed point count.** The outline is one closed spline whose point density comes from a 0.02 mm chord tolerance — an order of magnitude finer than any nozzle resolves. A 12 tooth pinion gets what it needs and a 120 tooth wheel does not drown Fusion in spline points.

## Development

The gear mathematics lives in `printgear_math.py` and imports nothing from Fusion, so all of it runs in a normal Python installation. The test suite checks the involute round trip, the outline against root and tip circles, tip truncation, the chord tolerance, backlash accounting, train layout in both modes — and rolls meshing pairs through a full tooth pitch looking for collisions, which is what proves the phasing:

```bash
python tools/test_geometry.py
```

The icons are generated rather than drawn, by rasterising a real gear pair straight out of `printgear_math`:

```bash
python tools/make_icons.py
```

Both scripts resolve paths relative to the repository. Set `PRINTGEAR_ADDIN_DIR` to point them at an installed copy instead.

## Support this project ❤️

If this add-in saved you time, you can support further development:

[![Donate with PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)

**[➡️ Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)**

## License

This project is licensed under the [MIT License](LICENSE) — © 2026 Thomas Weirich.
