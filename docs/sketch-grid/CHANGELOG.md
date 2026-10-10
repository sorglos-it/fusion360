# Changelog

## 1.0.0.0 – 2026-10-10

- Version numbers now have four parts, `v.x.y.z` (version, release, feature, build). All add-ins of this repository
  start again at 1.0.0.0; the content is unchanged. Earlier three-part numbers below keep their meaning.

## Unreleased – 2026-09-22

- Layout after the project standard: the add-in lives in `apps/desktop/SketchGrid/`, unchanged inside apart from two
  comments that name the new test path (Fusion needs folder, `.py` and `.manifest` under one name). Its version is also
  in `apps/desktop/VERSION`.
- The tests moved to `apps/desktop/tests/test_sketchgrid.py`. `tools/make_icon.py` stays in `tools/` and writes the
  icon into `apps/desktop/SketchGrid/resources/`; `SKETCHGRID_ADDIN_DIR` works as before.
- Compatibility: `python tools/test_sketchgrid.py` still works and runs the moved tests.
- The structural check from the template is now
  `python ../fusion360-addin-template/apps/desktop/tests/test_addin.py --path apps/desktop/SketchGrid`.
- README rewritten: start in 3 steps, shorter sections, a languages section, every path after the new layout.
- New `CHANGELOG.md`; `.gitignore` after the project standard.

Earlier versions: [Releases](https://github.com/sorglos-it/fusion360-sketch-grid/releases).
