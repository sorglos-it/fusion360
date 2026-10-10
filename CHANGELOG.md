# Changelog

Changes to the repository as a whole. Each add-in keeps its own list in `docs/<name>/CHANGELOG.md`.

## 2026-10-10

- PrintGear removed from the repository: add-in, tools and documentation. It stays in the history.
- All five add-ins set to version 1.0.0.0. From now on four-part numbers `v.x.y.z`: build +1 for a fix, feature +1 for
  something new, release +1 for a release; the first number only on request.
- New `tools/set_version.py`: writes an add-in's number into `VERSION` and its manifest in one go; `--check` reports
  any difference.

## 2026-10-04

- Five single repositories merged into this one, history included: `fusion360-addin-template` (template),
  `fusion360-dovetail`, `fusion360-printgear`, `fusion360-sketch-grid`, `fusion360-system3e`.
- Add-ins moved to `apps/desktop-<name>`, helper scripts to `tools/<name>`, former root files to `docs/<name>`.
- Old release tags kept with the add-in name in front, for example `dovetail-v1.5.0`.
- Paths in helper scripts and tests adjusted to the new layout.
