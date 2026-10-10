# Dovetail – documentation

Dovetail is an add-in for Autodesk Fusion 360. It turns sketch lines into joints: dovetail, triangle or box joint.
For every selected line it draws one closed band. The band is exactly as wide as the gap you want between the two
parts. Cut the band out of a solid and two parts remain that fit together.

This documentation describes version **1.1.0.0**.

## Contents

| File | What is in it |
|---|---|
| [installation.md](installation.md) | Requirements, installing, first start, update, removal |
| [usage.md](usage.md) | Every function, step by step |
| [settings.md](settings.md) | Every dialog field: meaning, default, limits; what is remembered; language |
| [how-it-works.md](how-it-works.md) | How the band is built inside, the checks, units |
| [troubleshooting.md](troubleshooting.md) | Every message, its cause and what to do; known limits |
| [development.md](development.md) | Folders, tests, version numbers, packing a release, decisions |

## At a glance

| | |
|---|---|
| Runs in | Autodesk Fusion 360 on Windows and macOS |
| Shapes | Trapezoid (dovetail), Triangle, Rectangle (box joint) |
| Lines per run | 1 to 100 |
| Teeth per line | 1 to 500 |
| Interface languages | German, English, Spanish, French, Italian |
| Licence | MIT, see [LICENSE](../LICENSE) |
| Author | Sorglos Thomas Weirich |

## Test status

- The geometry maths and the language files are tested outside Fusion with an offline test script.
- Version 1.1.0.0 changed the geometry (see [how-it-works.md](how-it-works.md#what-changed-in-1100)).
  These changes were tested **offline only**, including 34,317 random contours. They are **not yet confirmed
  inside Fusion**.

## See also

- [README](../README.md) – short entry page
- [CHANGELOG](../CHANGELOG.md) – what changed in which version
