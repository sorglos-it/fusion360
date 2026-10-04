# fusion360

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue)](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)

All Fusion 360 add-ins by Sorglos in one repository. Each add-in is a folder you copy into Fusion's add-in directory;
none of them needs anything installed besides Fusion 360.

| Folder | Purpose | Language | Start | Build |
| --- | --- | --- | --- | --- |
| `apps/desktop-dovetail` | Sketch lines become dovetail, triangle or box joints | Python | copy `Dovetail` into the add-in folder | – |
| `apps/desktop-sketch-grid` | Grid of shapes around a sketch point | Python | copy `SketchGrid` into the add-in folder | – |
| `apps/desktop-printgear` | Involute gears for 3D printing | Python | copy `PrintGear` into the add-in folder | – |
| `apps/desktop-system3e` | Walls from SYSTEM 3E elements – scaffold only, functions not built yet | Python | copy `System3E` into the add-in folder | – |
| `apps/desktop-template` | Starting point for a new add-in | Python | `python tools/template/new_addin.py MyAddIn` | – |

Every add-in keeps its own version in `apps/desktop-<name>/VERSION` and its own notes in `docs/<name>/`
(README, CHANGELOG). Helper scripts live in `tools/<name>/`.

## Start in 3 steps

1. Copy the add-in folder, for example `apps/desktop-dovetail/Dovetail`, to
   `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns`.
2. In Fusion: Utilities → ADD-INS → Add-Ins.
3. Select the add-in and press Run.

## Tests

The tests run without Fusion, one file per add-in:

```powershell
python apps/desktop-dovetail/tests/test_geometry.py
```

## Known limits

- The READMEs under `docs/<name>/` were written for the former single repositories; paths and download links in
  them still name the old layout.
- `tools/system3e/mesh_to_solid.py` expects the SYSTEM 3E model files under `assets/system3e/`; they are not part
  of the repository.

## License

MIT – Copyright (c) 2026 Sorglos Thomas Weirich

## Donate via PayPal

If this project helps you: [Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)
