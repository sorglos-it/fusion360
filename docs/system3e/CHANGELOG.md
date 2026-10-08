# Changelog

## 0.3.1 – 2026-10-08

- New field *Offset Z* in mm.
- `tools/system3e/points_sheet.py` draws an element with every point the add-in knows on it as an SVG
  (`docs/system3e/s1-wp-punkte.svg`): yellow can be clicked, red is an alignment point, green is both.

## 0.3.0 – 2026-10-08

- Every element carries six points to click: front end, middle and back end, once on the underside and once at the
  height where the next course stands (50 mm below the top on elements with the raised profile). Elements placed
  with an older version get them the next time the same element is placed.
- New field *Placed by*: lower front left corner, or bottom front end / middle / back end. A wall in bond: place the
  next element by its bottom middle on the upper front or back point of the one below.
- New fields *Offset X* and *Offset Y* in mm, along the design's axes.
- Not yet confirmed inside Fusion.

## 0.2.1 – 2026-10-08

- Parts list: placing an element a second time adds another copy of the same component instead of a new component
  `(1)`, `(2)` … – a parts list now counts equal elements together. Elements placed with 0.2.0 stay separate
  components; the first of them is reused from now on.
- Preview pictures redrawn with a depth buffer: 16 pictures showed faces in the wrong order.

## 0.2.0 – 2026-10-08

- New command *SYSTEM 3E element*: pick a point, a family and an element; a picture shows the element, and it is
  created as a new component with its lower front left corner on the point. Optional rotation about the vertical axis.
- Element library `blocks/blocks.json`: all 70 load-bearing elements of the catalogue plus the 4 partition elements,
  as closed solids with flat faces, one preview picture each. Built by `tools/system3e/build_library.py` from the
  manufacturer's 3D file (kept local).
- `S0/2 200 P` is damaged in the source file and rebuilt from `S0/2 250 P`.
- New test `apps/desktop-system3e/tests/test_blocks.py`.
- Not yet run inside Fusion. The left/right names of the corner and window elements were matched by eye against the
  catalogue cards and still need a check by someone who knows the system.

## 0.1.0 – 2026-10-04

- Scaffold from `fusion360-addin-template`: add-in `System3E` with five languages, structure check and icon tool.
- No SYSTEM 3E function yet – the button still runs the demo command of the template.
