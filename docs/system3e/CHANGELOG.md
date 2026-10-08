# Changelog

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
