# System3E

[![Release](https://img.shields.io/github/v/release/sorglos-it/fusion360)](https://github.com/sorglos-it/fusion360/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue)](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)

A Fusion 360 add-in for planning walls with the dry-stack elements of [SYSTEM 3E](https://www.system3e.com/).
Click a point, choose one of the 74 elements from a list with a preview picture, and the element is created there
as a solid body. Every element brings twelve points of its own to click, so the next course snaps on in bond.
Not affiliated with SYSTEM 3E. Part of the [fusion360](../../README.md) repository.

| Folder | Purpose | Language | Start | Build |
| --- | --- | --- | --- | --- |
| `apps/desktop-system3e/System3E` | the add-in | Python 3 (the one inside Fusion) | unpack the ZIP into Fusion's add-ins folder, then *Run* in Fusion | `python tools/release.py system3e` |

## Start in 3 steps

1. Download the latest `System3E-*.zip` from **[Releases](https://github.com/sorglos-it/fusion360/releases)**.
2. Unpack it into `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   (macOS: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`), so that
   `System3E\System3E.py` ends up one level below it.
3. In Fusion: **Utilities → ADD-INS → Add-Ins**, select *System3E*, press **Run**. The button *SYSTEM 3E element*
   is on the **SOLID** tab under *Create*.

## The dialog

| Field | What it does |
| --- | --- |
| Point | where the element goes: a sketch point, a corner of a body, a construction point – or one of the points of an element already placed. Nothing picked: the origin. |
| Family | starter, basic, complementary, lintel, window framing, top, corner, partition wall |
| Element | the elements of that family with their size in mm; the picture shows the chosen one |
| Placed by | which spot of the new element lands on the point: one of three corners or any of its twelve points |
| Rotation | turns the element about the vertical axis |
| Offset X, Y, Z | moves it by that many mm along the axes of the design |

The same element placed again is another copy of the same component, so a parts list counts equal elements together.

## The points of an element

Every element carries twelve construction points. They can be clicked as the place for the next element and chosen
under *Placed by*. The drawing [s1-wp-punkte.svg](s1-wp-punkte.svg) shows them on the basic element S1 WP.

| Where | Points |
| --- | --- |
| Underside, middle of the wall thickness | front end, middle, back end |
| Height where the next course stands, middle of the wall thickness | front end, middle, back end |
| Wall faces at half length, right and left | on the underside, 50 mm above it, and at the height of the next course |

"Front" is the end at length 0. Right and left are as seen from the front end looking along the wall. On elements
with the raised top profile the next course stands 50 mm below the highest point.

A wall in bond: choose *Placed by: bottom middle* and click the upper front or back point of the element below.

## State

- Placing elements has been used in Fusion. The points, *Placed by* and the offsets are tested offline only.
- The left and right names of the corner and window elements were matched by eye against the catalogue cards.
- `S0/2 200 P` is damaged in the manufacturer's 3D file and rebuilt from `S0/2 250 P`.

## Check and rebuild

Without starting Fusion – manifest, language files, icons, and every element as a closed solid:

```bash
python apps/desktop-system3e/tests/test_addin.py
```

```bash
python apps/desktop-system3e/tests/test_blocks.py
```

The element library `blocks/blocks.json` and the preview pictures are built from the manufacturer's 3D file, which
is not part of the repository (`assets/system3e/`). The pictures need Pillow:

```bash
python tools/system3e/build_library.py
```

## License

MIT – Copyright (c) 2026 Sorglos Thomas Weirich

## Donate via PayPal

If this project helps you: [Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)
