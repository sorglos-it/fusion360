# fusion360-system3e

[![Release](https://img.shields.io/github/v/release/sorglos-it/fusion360-system3e)](https://github.com/sorglos-it/fusion360-system3e/releases)
[![License](https://img.shields.io/github/license/sorglos-it/fusion360-system3e)](LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue)](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)

A Fusion 360 add-in for planning walls with the dry-stack elements of [SYSTEM 3E](https://www.system3e.com/).
**Status: scaffold only** — the add-in loads and shows the demo command of the template, the SYSTEM 3E functions are
not built yet. Not affiliated with SYSTEM 3E.

| Folder | Purpose | Language | Start | Build |
| --- | --- | --- | --- | --- |
| `apps/desktop/System3E` | the add-in | Python 3 (the one inside Fusion) | copy the folder into Fusion's add-ins folder, then *Run* in Fusion | – (runs as is) |

## Start in 3 steps

1. Download or clone this repository.
2. Copy `apps/desktop/System3E` to `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   (macOS: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`).
3. In Fusion: **Utilities → ADD-INS → Add-Ins**, select *System3E*, press **Run**.

## Check

Checks manifest, command id, the five language files (de, en, es, fr, it) and icons without starting Fusion:

```bash
python apps/desktop/tests/test_addin.py
```

## License

MIT – Copyright (c) 2026 Sorglos Thomas Weirich

## Donate via PayPal

If this project helps you: [Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)
