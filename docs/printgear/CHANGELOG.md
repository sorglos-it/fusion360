# Changelog

## 1.0.0.0 – 2026-10-10

- Version numbers now have four parts, `v.x.y.z` (version, release, feature, build). All add-ins of this repository
  start again at 1.0.0.0; the content is unchanged. Earlier three-part numbers below keep their meaning.

## Unreleased – 2026-09-22

- Layout after the project standard: the add-in lives in `apps/desktop/PrintGear/`, unchanged inside apart from one
  comment that names the new test path (Fusion needs folder, `.py` and `.manifest` under one name). Its version is also
  in `apps/desktop/VERSION`.
- The tests moved to `apps/desktop/tests/test_geometry.py`. `tools/make_icons.py` stays in `tools/` and writes the
  icons into `apps/desktop/PrintGear/resources/`; `PRINTGEAR_ADDIN_DIR` works as before.
- README rewritten: start in 3 steps, shorter sections, a languages section, every path after the new layout.
- New `CHANGELOG.md`; `.gitignore` after the project standard.

## 1.0.0 – 2026-08-26

- First version: involute gears sized for the printing nozzle — one gear, a pair or a gear train.
