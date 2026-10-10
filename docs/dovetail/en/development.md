# Development

Dovetail is one of several add-ins in the repository <https://github.com/sorglos-it/fusion360>.
All paths below are relative to the repository root.

## Folders

| Path | Content |
|---|---|
| `apps/desktop-dovetail/Dovetail/` | The add-in exactly as Fusion wants it: `Dovetail.py`, `Dovetail.manifest`, `lang/`, `resources/` |
| `apps/desktop-dovetail/VERSION` | The version number, one line |
| `apps/desktop-dovetail/tests/test_geometry.py` | The offline tests |
| `tools/dovetail/make_icons.py` | Writes the toolbar icon (16, 32, 64 px) into `resources/Dovetail/` |
| `tools/dovetail/make_arrow_icons.py` | Writes the icons of the **Move** buttons into `resources/nudge_left`, `nudge_center`, `nudge_right` |
| `tools/dovetail/test_geometry.py` | Forwarder to the moved test file, so the old command keeps working |
| `tools/set_version.py` | Sets the version of one add-in or of all (shared by all add-ins) |
| `tools/release.py` | Packs the release ZIP (shared by all add-ins) |
| `docs/dovetail/` | README, CHANGELOG, LICENSE and this documentation |
| `dist/` | Output of `tools/release.py`; not in Git |

Fusion requires folder, `.py` file and `.manifest` file to carry the same name. Do not rename one of them alone.

## Structure of `Dovetail.py`

| Section | Main parts |
|---|---|
| Language | `Strings`, `T()`, `detect_language()`, `read_version()`, `display_name()` |
| Geometry | `GeometryError`, `_offset_polyline()`, `_top_half()`, `_check_contour()`, `end_room()`, `max_offset()`, `tooth_directions()`, `build_contours()`, `closed_band()` |
| Drawing | `_to_world()`, `_draw_closed_polyline()`, `line_length()`, `create_geometry()` |
| Handlers | `_read_inputs()`, `_selected_lines()`, `_check_lines()`, `_run()`, `ExecuteHandler`, `PreviewHandler`, `ValidateHandler`, `InputChangedHandler`, `CommandCreatedHandler`, `_apply_nudge()`, `_apply_mirror()` |
| Start / stop | `_find_panel()`, `run()`, `stop()` |

The geometry section is pure maths. It uses nothing from Fusion and can run in any Python 3.

## Running the tests

Requirements: Python 3, standard library only. No Fusion needed; the test file puts small stand-ins for the
`adsk` modules in place before importing the add-in.

```bash
python apps/desktop-dovetail/tests/test_geometry.py
```

The old command still works and gives the same output and exit code:

```bash
python tools/dovetail/test_geometry.py
```

- Every check prints `ok` or `FAIL`.
- The last line is `all tests passed`, or the number of failures.
- The exit code is 1 if anything failed.

What the sections cover:

| Section | Content |
|---|---|
| 1–4 | The three shapes; points of the outline; the offset contour is parallel and at the right distance |
| 5 | Alignment: the group is centred on the midpoint of the line |
| 6 | Offset, largest offset, distance from the line ends |
| 7 | Who pays for the clearance (the three entries of **The line is**) |
| 8 | Mirrored geometry: both parts identical; accepted and refused the same way either way round |
| 9 | Failures report the right key; one joint per selected line; a bad line names itself |
| 10 | Every drop-down entry and tooltip key exists in `en.xml` |
| 11 | Language files: complete, no unknown keys, placeholders kept, no empty texts |
| 12 | Text catalogue, fallback to English, language detection without Fusion |

To test an installed copy instead of the one in the repository, set the environment variable
`DOVETAIL_ADDIN_DIR` to its folder. The two icon scripts read the same variable.

Not covered by the test file:

- Anything that needs Fusion: the dialog, the preview, drawing, the conversion to construction geometry, the undo
  after a failed run.
- The run with 34,317 random contours named in the changelog. It was a one-off check; it is not part of
  `test_geometry.py`.

## Icons

```bash
python tools/dovetail/make_icons.py
python tools/dovetail/make_arrow_icons.py
```

Both write PNG files with the standard library only. Run them only when the icons shall change.

## Version numbers

Versions have four parts, `v.x.y.z`: version, release, feature, build. Example: `1.1.0.0`.

The number is kept in two places:

- `apps/desktop-dovetail/VERSION`
- the `"version"` entry of `Dovetail.manifest` (this is what Fusion and the dialog title read)

Never edit them by hand. Use the script, which writes both:

```bash
python tools/set_version.py dovetail 1.1.0.1    # set one add-in
python tools/set_version.py all 1.0.0.0         # set all add-ins of the repository
python tools/set_version.py --check             # report add-ins whose two numbers differ
```

The script refuses a number that does not have four parts. `--check` ends with exit code 1 if any add-in differs.

## Packing a release

```bash
python tools/release.py dovetail
```

- Writes `dist/Dovetail-<version>.zip`.
- The ZIP holds the folder `Dovetail/` exactly as Fusion wants it.
- Left out: `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compression: Deflate at the highest level, so every unpacker can read it.
- After writing, the ZIP is read back and tested.
- The script refuses to pack if `VERSION` and the manifest disagree.

`python tools/release.py all` packs every add-in of the repository.

Suggested order for a release:

1. Run the tests.
2. Set the version with `tools/set_version.py`.
3. Add the entry to `docs/dovetail/CHANGELOG.md`.
4. Update this documentation.
5. Pack with `tools/release.py`.
6. Attach `dist/Dovetail-<version>.zip` to the release on GitHub.

## Adding a language

1. Copy `lang/en.xml` and name the copy after the two-letter language code.
2. Set `language="<code>"` in the root element and translate the values.
3. Keep every placeholder (`{0}`, `{1}`, …).
4. Add the code to `SUPPORTED_LANGUAGES` and the matching Fusion language name to `FUSION_LANGUAGE_MAP` in
   `Dovetail.py`.
5. Run the tests. They check every file for completeness, unknown keys, placeholders and empty texts.

`en.xml` is the reference file. Every key exists there. A key missing elsewhere falls back to it; a key missing
everywhere is shown as the key itself.

## Decisions and their reasons

Taken from the comments in the code.

| Decision | Reason |
|---|---|
| Texts live in `lang/<code>.xml`; errors carry a key, not a text | The reason for an error stays independent of the language; tests can compare keys |
| Shape and split are stored as the index in the list | The stored value does not depend on the display language |
| Fusion's language values are looked up with `getattr` | A value this Fusion version does not know cannot break the add-in |
| The version is read from the manifest | The dialog cannot drift from the manifest |
| The version is part of the command name | Fusion uses the command name as the dialog title, so this is where a version is visible while the dialog is open |
| The offset is not remembered | It belongs to the line at hand, not to the settings |
| The original line becomes construction geometry instead of being deleted | It stops creating profiles but keeps its dimensions and constraints |
| The preview leaves the original line alone | The selection cannot be invalidated underneath the open dialog |
| All lines are checked before any is drawn | A bad line at the end cannot leave half the sketch drawn |
| A failure on one of several lines is wrapped with its position | A short line in the middle fails while the others would be fine; the message says which one |
| The **Move** buttons use the shortest line as limit | An offset that runs off one line is no good even if the others could take it |
| With mirroring, count, split and offset are set and greyed out | Each of them breaks the 180 degree symmetry; pinning them is better than leaving them to fail validation |
| Mirroring needs an even count | A middle tooth would have to point both ways at once |
| Minimum spacing has 0.01 mm on top | At exactly the minimum the stretch between two pockets has no length left |
| Teeth keep tolerance + 0.01 mm from the line ends | The pocket opens up by as much as the tolerance; otherwise the contour runs past the end and has to turn back |
| A contour is checked for zero-length pieces and for crossing itself | The offset mitres every corner on its own, so nothing else stops a short piece from shrinking to nothing or flipping round |
| A mitre corner further away than 12 × the offset is refused | The mating contour would run away at a sharp corner |
| A failed run sets `executeFailed` | Fusion then undoes what was drawn so far |
| Drawing runs with `isComputeDeferred` | The sketch recalculates once, not after every line |
| `set_version.py` writes VERSION and manifest together | The number is never edited by hand in two places |
| The ZIP uses Deflate at the highest level | Every unpacker can read it |

## Known open points

- When OK is greyed out, the dialog shows no reason. The texts exist (`err.*`) but only the message box after a
  failed run shows them.
- Sketch lines are read with X and Y only and the band is drawn at Z = 0 of the sketch.
- The geometry changes of 1.1.0.0 are tested offline only, not inside Fusion.

## Licence

MIT, see [LICENSE](../LICENSE). Author: Sorglos Thomas Weirich.
