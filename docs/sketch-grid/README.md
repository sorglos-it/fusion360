# SketchGrid

[![Fusion 360](https://img.shields.io/badge/Autodesk-Fusion%20360-F60?logo=autodesk&logoColor=white)](#start-in-3-steps)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-0078D6?logo=windows&logoColor=white)](#start-in-3-steps)
[![Languages](https://img.shields.io/badge/UI-DE%20%7C%20EN%20%7C%20ES%20%7C%20FR%20%7C%20IT-4c1.svg)](#languages)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-00457C.svg?logo=paypal)](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)

A Fusion 360 add-in that builds a **grid of shapes around a sketch point**. Click a point, say how big one cell is and
how far apart the cells sit, and get the whole array in one go — rectangles, circles, slots or polygons. Part of the [fusion360](../../README.md) repository.

**Full documentation** in English, Deutsch, Italiano, Español and Français: [index.md](index.md).

| Folder | Purpose | Language | Start | Build |
|---|---|---|---|---|
| `apps/desktop-sketch-grid/SketchGrid` | the add-in: grids of shapes around a sketch point | Python 3 (the one inside Fusion) | copy into Fusion's add-ins folder, then *Run* | – (runs as is) |

## Start in 3 steps

1. Download the latest `SketchGrid-*.zip` from
   **[Releases](https://github.com/sorglos-it/fusion360/releases)** — or clone this repository and take the
   folder `apps/desktop-sketch-grid/SketchGrid`.
2. Unpack or copy it into Fusion's add-ins folder, so that `SketchGrid\SketchGrid.py` ends up one level below it:

   | OS | Path |
   |---|---|
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/` |

3. In Fusion: **Utilities → ADD-INS → Add-Ins**, select the entry, tick *Run on Startup*, press **Run**. The button
   appears on the **SKETCH** tab in the **CREATE** panel, with the installed version in brackets after its name.

You need Autodesk Fusion 360 (Windows or macOS), any recent version — nothing else to install.

## Update

Stop the add-in in Fusion first, otherwise the running one stays in memory. Then replace the folder, keeping its name:
Fusion requires `<Folder>/<Folder>.py` and `<Folder>/<Folder>.manifest` to match.

## Usage

1. Open or edit a sketch.
2. Click a point — the sketch origin, or any point you placed yourself.
3. Click the grid icon. The point is already in the dialog.
4. Set the values, read the result line, press **OK**.

Example, the one the add-in was built around: length 10 mm, depth 5 mm, gap 2 mm, 8 columns and 4 rows. That gives a
pitch of 12 × 7 mm, a grid of 94 × 26 mm and 32 rectangles, centred on the point you picked.

What you get:

- **Two ways to count** — columns and rows outright, or as many as fit completely into an area.
- **Four shapes** — rectangle (corners sharp, rounded or chamfered), circle/ellipse, slot, polygon with 3 to 24 sides.
- **Nine anchor positions** plus an X/Y offset, so the point can stay where it belongs.
- **Separate gaps** for X and Y, 0 allowed — measured between the shapes, whatever their form.
- **Live read-out and preview** — *8 × 4 = 32 shapes, 94 × 26 mm overall*, updated as you type.
- **Explained refusals** — an area too small for one shape says how big it would have to be; more than 2000 shapes
  are refused instead of freezing Fusion.

## Dialog

| Field | Meaning |
|---|---|
| **Point** | The sketch point the grid is built around. Pre-filled from the current selection. |
| **Count from** | `Columns and rows` or `Fitting an area`. Switches which fields below are shown. |
| **Shape** | `Rectangle`, `Circle / ellipse`, `Slot`, `Polygon`. |
| **Sides** | Polygon only: 3 to 24. |
| **Regular** | Polygon only. Off: stretched to fill the cell. On: equilateral, sized by the smaller cell edge, and the pitch follows the shape. |
| **Corners** | Rectangle only: `Sharp`, `Rounded` or `Chamfered`. |
| **Radius / chamfer** | Rectangle only, once the corners are not sharp: the fillet radius or the leg length of the chamfer. |
| **Length (X)** / **Depth (Y)** | The size of one cell. |
| **Gap X** / **Gap Y** | Space between neighbours. 0 makes them touch. |
| **Columns** / **Rows** | Fixed mode: the count outright. |
| **Area width** / **Area height** | Fill mode: the space to fill. |
| **Point sits** | Where the picked point is in the grid: middle, a corner, or the middle of an edge. |
| **Offset X** / **Offset Y** | Shifts the whole grid off the point, on top of the anchor. Negative goes the other way. |
| **Result** | Read-only: how many shapes and how big the grid comes out. |

## The two modes

**Columns and rows:** `n` shapes span `n × size + (n−1) × gap`, so 8 columns of 10 mm with a 2 mm gap come to 94 mm,
not 96.

**Fitting an area:** as many as fit in *completely*, `floor((area + gap) / (size + gap))`. A partial shape at the edge
is never drawn.

- 100 mm with 10 mm shapes and a 2 mm gap gives **8** columns (94 mm used, 6 mm left). A ninth would need 106 mm.
- The leftover sits on the far side of the grid; the anchor decides which side that is, the middle splits it.
- An area of exactly 94 mm gives 8, at 93.9 mm it drops to 7 — a rounded-off number can cost a whole column.

## Anchor

**Point sits in the grid** means exactly that: where the point you clicked ends up *inside* the finished grid — not the
direction the grid grows in. A point at the bottom left means the grid extends up and to the right of it. Three of
the nine positions, with a 3 × 2 grid, `X` the point and `#` the shapes:

```
  In the middle        Bottom left          Top centre
  #####.#####.#####    #####.#####.#####    #####.##X##.#####
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  ........X........    .................    .................
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  #####.#####.#####    X####.#####.#####    #####.#####.#####
```

`In the middle` is the default and grows the grid evenly in all four directions: for the 8 × 4 example the lower left
corner lands 47 mm left of and 13 mm below the point.

## Offset

**Offset X** and **Offset Y** move the whole grid off the point, on top of the anchor. The case it is for: your point
sits at 0/0, but the grid should start 2 mm in, to keep a margin. The point stays where it is, and the margin does not
have to match the gap. Count, pitch and overall size stay the same; in fill mode the offset does not change how many
shapes fit, it only moves them.

## Shapes

| Shape | Built from | Note |
|---|---|---|
| **Rectangle** | length × depth | Its corners can be rounded or chamfered — see below. |
| **Circle / ellipse** | length and depth as the two axes | Equal values give a true circle. |
| **Slot** | rectangle with semicircular ends | Rounded on the shorter axis; equal length and depth make a circle. |
| **Polygon** | length × depth, first vertex pointing up | Stretched to fill the cell. Tick **Regular** to keep it equilateral — then the smaller cell edge sets its size. |

## Corners

**Corners** picks a fillet arc or a straight chamfer, **Radius / chamfer** says how much — rectangle only. The limit
is **half the shorter edge**, and there the rectangle turns into something else:

| Radius / chamfer | Rounded | Chamfered |
|---|---|---|
| 1 mm on a 10 × 5 rectangle | soft corners | the corners cut off |
| 2.5 mm on a 10 × 5 rectangle — the maximum | a slot | a hexagon |
| 5 mm on a 10 × 10 square — the maximum | a circle | a diamond |

More than the limit is refused, and the message names the value that would still fit. The bounding box stays length ×
depth, so count, pitch and overall size do not change; the gap along the flat edges stays the gap you set, across a
corner there is more of it.

## The gap is measured between the shapes

Every shape fills its cell, so the pitch is `size + gap` and the space between neighbours is the gap you asked for.
A **regular** polygon is the exception — it has a single diameter and cannot fill a cell of other proportions — so the
pitch follows its measured footprint instead:

| 10 × 5 cell, gap 2, hexagon | Shape | Pitch | Gap |
|---|---|---|---|
| stretched (default) | 10.00 × 5.00 | 12.00 × 7.00 | 2.00 / 2.00 |
| regular | 4.33 × 5.00 | 6.33 × 7.00 | 2.00 / 2.00 |

## Languages

The interface follows **Preferences → General → User Language** in Fusion: German, English, Spanish, French or
Italian, anything else falls back to English. The texts live in `apps/desktop-sketch-grid/SketchGrid/lang/<code>.xml`; `en.xml` is
the reference and a key missing elsewhere falls back to it. To add a language, copy `en.xml`, translate it, name it
after the two-letter code and add the code to `SUPPORTED_LANGUAGES` and `FUSION_LANGUAGE_MAP` in `sketchgrid_core.py`.

## Notes & caveats

- **The count is capped at 2000.** Fusion takes minutes over more with the sketch solver awake; the cap refuses with a
  message instead of appearing to hang.
- **Only the rectangle has corners to take off.** A polygon keeps its own, sharp.
- **A regular polygon uses the smaller cell edge.** In a wide, flat cell it looks lost — use a rectangle or an ellipse
  when the cell is not roughly square.
- **The polygon's orientation is fixed** with a vertex pointing up. For flat-top hexagons swap length and depth, or
  rotate the finished sketch.
- **Shapes are plain sketch geometry, not a Fusion pattern.** Changing the source later does not update them — on
  purpose: you can trim, constrain and extrude them without a pattern feature in the way.
- **Gaps can be 0 but not negative.** Overlapping shapes would make profiles that fight each other; for overlap, draw
  one grid and offset a second.
- **The leftover in fill mode is not centred** unless you anchor to the middle.
- **Only sketch points can be picked** — the sketch origin or any point you place, not a vertex on a body.

## Development

The grid maths has no Fusion dependency, so it runs in a normal Python 3 (standard library only):

```bash
python apps/desktop-sketch-grid/tests/test_sketchgrid.py
python apps/desktop-template/tests/test_addin.py --path apps/desktop-sketch-grid/SketchGrid
python tools/sketch-grid/make_icon.py
```

The first checks the layout, the anchor factors (derived from each entry's own name, so a label that disagrees with
the geometry fails), both counting modes, the corner outlines, every error key and all five language files. The second
is the structural check from the template repository, cloned next to this one — manifest, GUID, command id, icons.
The third draws the toolbar icon. The tests and the icon script find the add-in in `apps/desktop-sketch-grid/SketchGrid`; set
`SKETCHGRID_ADDIN_DIR` to point them at an installed copy instead. `python tools/sketch-grid/test_sketchgrid.py` still works and
runs the same tests.

How it works, in short: `grid_layout()` works out count, pitch, overall size and where the grid sits relative to the
point, `cell_centres()` walks the cells, and `corner_outline()` returns a cut rectangle as plain lines and arcs — none
of them touches the Fusion API, which is why the tests can check them. Each shape is then drawn by its own small
function, with `isComputeDeferred` set; with a few hundred cells that is the difference between instant and unusable.

## Related

Scaffolded from **[desktop-template](https://github.com/sorglos-it/fusion360/tree/main/apps/desktop-template)**, which carries
the translated interface, the handler registry and the panel lookup used here. See also
[desktop-dovetail](https://github.com/sorglos-it/fusion360/tree/main/apps/desktop-dovetail) — joints on a sketch line.

## License

MIT — see [LICENSE](LICENSE). © 2026 Sorglos Thomas Weirich.

## Donate via PayPal

If this add-in saved you time, a donation supports further development. Thank you!

**[➡️ Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)**
