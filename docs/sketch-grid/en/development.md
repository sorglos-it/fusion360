# Development

SketchGrid is one of several add-ins in the repository <https://github.com/sorglos-it/fusion360>. All paths below start at the repository root.

## Folders

| Path | Content |
| --- | --- |
| `apps/desktop-sketch-grid/SketchGrid/` | The add-in exactly as Fusion needs it: `SketchGrid.py`, `sketchgrid_core.py`, `SketchGrid.manifest`, `lang/`, `resources/SketchGrid/` |
| `apps/desktop-sketch-grid/VERSION` | The version number, one line |
| `apps/desktop-sketch-grid/tests/test_sketchgrid.py` | The tests |
| `tools/sketch-grid/make_icon.py` | Draws the button icon (16, 32 and 64 pixels) |
| `tools/sketch-grid/test_sketchgrid.py` | Only forwards to the tests above, so the old command keeps working |
| `tools/set_version.py` | Sets the version number (shared by all add-ins) |
| `tools/release.py` | Packs the release ZIP (shared by all add-ins) |
| `docs/sketch-grid/` | README, CHANGELOG, LICENSE and this documentation |
| `dist/` | Created by `tools/release.py`; not in Git |

Folder, `.py` file and `.manifest` file must share the name `SketchGrid`. Fusion requires this.

All scripts need only a normal Python 3 with its standard library. There is nothing to build; the add-in runs as it is.

## Run the tests

```
python apps/desktop-sketch-grid/tests/test_sketchgrid.py
python apps/desktop-template/tests/test_addin.py --path apps/desktop-sketch-grid/SketchGrid
```

The first command runs without Fusion. The test file puts empty stand-ins for Fusion's `adsk` modules in place and then imports `SketchGrid.py`. It prints one line per check (`ok` or `FAIL`) and ends with `all tests passed` and exit code 0, or with the number of failures and exit code 1.

What it checks:

| Section | Subject |
| --- | --- |
| 1 | The standard example: 10 × 5 mm, gap 2 mm, 8 columns, 4 rows gives 94 × 26 mm and 32 cells |
| 2, 2b | Every anchor entry has the factors that its name promises (derived from the key name, for example `bottom_left`), and the point lands where the entry says |
| 3 | Positions of the cells |
| 4 | The mode "Fitting an area" counts only what fits completely |
| 5 | Every refusal reports the right message key |
| 6 | Language files: all five are complete and keep their placeholders |
| 7 | Offset from the picked point |
| 8 | The gap stays the gap for every shape: measured polygon box, stretching, real size in fill mode |
| 9 | Rectangle corners: limits and the outline of lines and arcs |
| 10 | Every drop-down entry has a text |
| 11 | Text catalogue: loading each language, fallback to English, messages follow the language |

The second command is the structure check from the template add-in in the same repository. It checks manifest, id, command id and icons.

By default the tests and the icon script use `apps/desktop-sketch-grid/SketchGrid`. Set the environment variable `SKETCHGRID_ADDIN_DIR` to test another copy, for example an installed one.

What the tests do not cover: everything that needs Fusion. That is the dialog, the selection, the preview and the actual drawing calls. These parts can only be tried inside Fusion.

## Try a change in Fusion

1. Copy `apps/desktop-sketch-grid/SketchGrid` into Fusion's add-ins folder (see [installation.md](installation.md)).
2. In Fusion, stop the add-in and run it again.

`SketchGrid.py` removes `sketchgrid_core` from Python's module cache before importing it. Reason from the code comment: Fusion caches imported modules, so an edited helper would keep serving its old version until Fusion restarts.

## Version numbers

Four parts: `v.x.y.z` (version, release, feature, build), for example `1.1.0.0`.

The number is kept in two places:

- `apps/desktop-sketch-grid/VERSION`
- the entry `"version"` in `SketchGrid.manifest` (Fusion and the button name read this one)

Never edit them by hand. Use the script, which writes both:

```
python tools/set_version.py sketch-grid 1.1.0.1
python tools/set_version.py --check
```

- The first command sets the version. It refuses anything that is not four numbers separated by dots.
- `--check` lists every add-in with both numbers and says `ok` or `DIFFERENT OR NOT v.x.y.z`. Exit code 1 if any add-in is wrong.
- `all` instead of `sketch-grid` sets the same number for every add-in of the repository.

Add an entry to `docs/sketch-grid/CHANGELOG.md` for every new number.

## Pack a release

```
python tools/release.py sketch-grid
```

- Writes `dist/SketchGrid-<version>.zip`.
- The ZIP contains the folder `SketchGrid` as its top level, ready to be unpacked into Fusion's add-ins folder.
- Left out: `__pycache__` folders and files ending in `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compression: Deflate at the highest level, "so every unpacker can read it" (script comment).
- The script refuses to pack when `VERSION` and the manifest differ or the number does not have four parts.
- After writing, it reads the ZIP back and stops if a file in it is damaged.
- `all` instead of `sketch-grid` packs every add-in.

The ZIP is then attached to a release at <https://github.com/sorglos-it/fusion360/releases>. The script does not upload anything.

## Redraw the icon

```
python tools/sketch-grid/make_icon.py
```

Writes `16x16.png`, `32x32.png` and `64x64.png` into `resources/SketchGrid/`. The picture is a 3 × 3 grid of cells with a cross in the middle for the picked point. The script writes the PNG files itself, without an image library.

## Add a language

1. Copy `lang/en.xml` to `lang/<code>.xml` (two-letter code) and translate the texts. Keep the keys and the placeholders `{0}`, `{1}`.
2. In `sketchgrid_core.py`, add the code to `SUPPORTED_LANGUAGES`, and the matching Fusion language name to `FUSION_LANGUAGE_MAP`.
3. Run the tests. They check every language in `SUPPORTED_LANGUAGES`.

## Decisions and their reasons

Taken from the comments in the code.

| Decision | Reason given |
| --- | --- |
| The grid calculation (`grid_layout`, `cell_centres`, `corner_outline`) uses no Fusion calls. | This is the part worth testing, and so the tests can run without starting Fusion. |
| Drop-down choices are stored as their position in the list, not as text. | The stored value does not move when the interface language changes. |
| At most 2000 shapes (`MAX_SHAPES`). | A runaway count in fill mode locks Fusion up for minutes. Refuse instead. |
| A radius / chamfer above half the shorter edge is refused, not reduced. | At exactly half, the two cuts on an edge meet; beyond it they would run past each other. Only rounding noise is absorbed. |
| Corners do not take part in the layout. | The bounding box is still length × depth, so pitch, count and gap stay as they were. |
| A regular polygon reports its own measured size and the pitch follows it. | It cannot fill a cell of other proportions; otherwise the gap you ask for is not the gap you get. |
| The polygon box is measured, not assumed. | A polygon has a corner on every extreme only for suitable side counts; a pentagon sits low in its own box. |
| A fully rounded square is drawn as a circle. | A circle is not a chain of segments. |
| For an ellipse, the main axis point is put on the longer axis. | Otherwise Fusion rejects the ellipse. |
| `isComputeDeferred` is set while drawing and reset in a `finally` block. | It keeps the solver quiet until every shape is drawn; with a few hundred cells that is the difference between instant and unusable. |
| The preview handler swallows every error. | It fires on every keystroke, including half-typed values. Reporting is the job of the input validation. |
| Event handlers are registered before the pre-selected point is taken over, and taking it over may fail silently. | Whatever fails afterwards, the dialog must still work; the user then picks the point in the dialog. |
| All event handlers are kept in a registry (`HandlerRegistry`). | Fusion holds only a weak reference to a handler. Without a reference on the Python side, the event silently stops firing. |
| Several panel ids are tried in order. | Panel ids move between Fusion versions. |
| Fusion's language values are looked up by name with a fallback. | A value this Fusion version does not know cannot break the add-in; it falls back to English instead of failing. |
| A key missing in a translation is served from English. | A half-finished translation degrades to English instead of showing raw keys. |
| Expected problems are raised as `AddInError` with a message key. | The key is independent of the language; things the user can fix should block OK instead of opening a window. |
| The version is read from the manifest, not written into the code. | The dialog cannot drift away from the manifest, and there is only one place to change. |
| The version is part of the command name. | Fusion uses the command name as the dialog title, so this is where the version is visible; there is only the one name. |
| Last values are kept in memory in centimetres. | Centimetres are Fusion's internal unit, regardless of the display unit. |

## Open points

- Version 1.1.0.0 (pre-selected point cannot be taken over) is tested offline only, not inside Fusion.
- Slots and rounded or chamfered rectangles are drawn as separate curves from coordinates, without shared end points. Whether they stay connected when dragged has to be checked inside Fusion.
- The limit of 2000 counts shapes, not curves. Whether it has to count curves has to be checked inside Fusion.

## Licence

MIT, see [LICENSE](../LICENSE). Author: Sorglos Thomas Weirich.
