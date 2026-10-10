# SketchGrid

SketchGrid is an add-in for Autodesk Fusion 360. You click one point in a sketch and get a grid of equal shapes around it: rectangles, circles or ellipses, slots, or polygons.

This documentation describes version 1.1.0.0.

## Contents

| File | What is in it |
| --- | --- |
| [installation.md](installation.md) | Requirements, installing, first start, update, removal |
| [usage.md](usage.md) | Every function, step by step |
| [settings.md](settings.md) | Every dialog field with default and limits, what is remembered, language |
| [how-it-works.md](how-it-works.md) | Files, how the grid is calculated, how the shapes are drawn |
| [troubleshooting.md](troubleshooting.md) | Every message, its cause and what to do; known limits |
| [development.md](development.md) | Folders, tests, version numbers, packing a release |

## What it does, in short

- Two ways to set the number of shapes: **Columns and rows**, or **Fitting an area** (as many as fit completely).
- Four shapes: **Rectangle** (corners sharp, rounded or chamfered), **Circle / ellipse**, **Slot**, **Polygon** (3 to 24 sides).
- Nine positions for the point inside the grid, plus an offset in X and Y.
- A separate gap for X and Y.
- A **Result** line that shows the number of shapes and the overall size while you type.
- At most 2000 shapes per grid.

## Test status

- The grid calculation, the corner outlines, the messages and the five language files are checked by an automatic test that runs without Fusion.
- The change in version 1.1.0.0 (the dialog keeps working when the point picked beforehand cannot be taken over) was tested offline only, **not inside Fusion**.
- Two known limits come from a code review and are **not confirmed inside Fusion**. See [troubleshooting.md](troubleshooting.md#known-limits).

## Licence and author

MIT licence, see [LICENSE](../LICENSE). Author: Sorglos Thomas Weirich.

Change history: [CHANGELOG.md](../CHANGELOG.md).
