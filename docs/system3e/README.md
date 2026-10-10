# fusion360-system3e

[![Release](https://img.shields.io/github/v/release/sorglos-it/fusion360)](https://github.com/sorglos-it/fusion360/releases)
[![License](https://img.shields.io/github/license/sorglos-it/fusion360)](LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue)](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)

A Fusion 360 add-in for planning walls with the dry-stack elements of [SYSTEM 3E](https://www.system3e.com/).
Click a point, choose one of the 74 elements from a list with a preview picture, and the element is created there
as a solid body. Every element brings twelve points of its own to click, so the next course snaps on in bond. **Status: not yet tested inside Fusion.** Not affiliated with SYSTEM 3E.

| Folder | Purpose | Language | Start | Build |
| --- | --- | --- | --- | --- |
| `apps/desktop-system3e/System3E` | the add-in | Python 3 (the one inside Fusion) | copy the folder into Fusion's add-ins folder, then *Run* in Fusion | – (runs as is) |

## Start in 3 steps

1. Download or clone this repository.
2. Copy `apps/desktop-system3e/System3E` to `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   (macOS: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`).
3. In Fusion: **Utilities → ADD-INS → Add-Ins**, select *System3E*, press **Run**. The button *SYSTEM 3E element*
   is on the **SOLID** tab under *Create*.

## Check

Checks manifest, command id, the five language files (de, en, es, fr, it) and icons without starting Fusion:

```bash
python apps/desktop-system3e/tests/test_addin.py
```

## License

MIT – Copyright (c) 2026 Sorglos Thomas Weirich

## Donate via PayPal

If this project helps you: [Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=6CDEVZGJWTNQQ)
