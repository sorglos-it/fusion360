# System3E – documentation

System3E is an add-in for Autodesk Fusion 360. It places wall elements of the SYSTEM 3E dry-stack building
system in a design. You click a point, choose one of 74 elements from a list, and the element is created there
as a solid body.

This documentation describes version 1.1.0.0.

## Contents

| File | What you find there |
| --- | --- |
| [installation.md](installation.md) | Requirements, installing, first start, update, removal |
| [usage.md](usage.md) | Placing elements step by step, building a wall in bond, parts list |
| [settings.md](settings.md) | Every field of the dialog, defaults, what is remembered, language |
| [how-it-works.md](how-it-works.md) | Files, element library, how a body is built, points, units |
| [troubleshooting.md](troubleshooting.md) | Every message, its cause and what to do; known limits |
| [development.md](development.md) | Folders, tests, rebuilding the library, versions, release |

Further files: [change log](../CHANGELOG.md), [licence](../LICENSE), [drawing of the points](../s1-wp-punkte.svg).

## What the add-in does

- It adds one button, **SYSTEM 3E element**, to Fusion.
- The button opens a dialog with eight fields and a preview picture.
- The element is created as a component with one solid body.
- Every element carries twelve points of its own. You can click them to place the next element.
- The same element placed again is another copy of the same component. A parts list counts equal elements together.

## What is tested and what is not

| Part | State |
| --- | --- |
| Placing elements | Used inside Fusion by the author |
| The twelve points to click | Used inside Fusion by the author |
| Points shown on the surface and corrected after an element is made (since 1.1.0.1) | Used inside Fusion by the author |
| The choices under **Placed by** | Used inside Fusion by the author |
| **Offset X**, **Offset Y**, **Offset Z** | Used inside Fusion by the author |
| Fixes of version 1.0.0.1 (see the [change log](../CHANGELOG.md)) | Not yet confirmed inside Fusion |
| Left/right names of the corner and window elements | Matched by eye against the manufacturer's catalogue cards, **not confirmed** |
| Element `S0/2 200 P` | Damaged in the manufacturer's 3D file, rebuilt from `S0/2 250 P` |

"Offline" means: checked by a test program without Fusion. See [development.md](development.md).

## Legal

- The add-in is **not affiliated with SYSTEM 3E**.
- Licence: MIT. See [LICENSE](../LICENSE).
- Author: Sorglos Thomas Weirich.
