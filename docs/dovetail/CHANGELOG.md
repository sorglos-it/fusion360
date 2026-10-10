# Changelog

## 1.1.0.0 – 2026-10-10

- Release. Same content as build 1.0.0.1.

## 1.0.0.1 – 2026-10-10

Fixes from a code review; nothing new.

- Teeth now keep the tolerance plus 0.01 mm away from the ends of the line. Right at the end the pocket contour ran
  past the line and turned back, which gave a loop crossing itself. The largest offset is smaller by that amount.
- Two teeth need 0.01 mm more spacing than before; at exactly the old minimum a stretch of the contour had no length.
- A contour that would cross itself is refused instead of drawn (narrow trapezoid tips with a large tolerance).
- If drawing fails half way, Fusion undoes the lines already drawn.
- A test that could never fail is gone; a comment about the offset direction said the opposite of the code.
- Checked with 34,317 random valid contours, none crossing itself. Not yet confirmed inside Fusion.

## 1.0.0.0 – 2026-10-10

- Version numbers now have four parts, `v.x.y.z` (version, release, feature, build). All add-ins of this repository
  start again at 1.0.0.0; the content is unchanged. Earlier three-part numbers below keep their meaning.

## Unreleased – 2026-09-22

- Layout after the project standard: the add-in lives in `apps/desktop/Dovetail/`, unchanged inside (Fusion needs
  folder, `.py` and `.manifest` under one name). Its version is also in `apps/desktop/VERSION`.
- The tests moved to `apps/desktop/tests/test_geometry.py`. `tools/make_icons.py` and `tools/make_arrow_icons.py`
  stay in `tools/` and write the icons into `apps/desktop/Dovetail/resources/`; `DOVETAIL_ADDIN_DIR` works as before.
- Compatibility: `python tools/test_geometry.py` still works and runs the moved tests.
- README rewritten: start in 3 steps, shorter sections, every path after the new layout.
- README no longer claims the dialog says which value or line is at fault — it only greys out OK and draws nothing.
- New `CHANGELOG.md`; `.gitignore` after the project standard.

Earlier versions are tags in this repository; their ZIP files went with the former single repository.
