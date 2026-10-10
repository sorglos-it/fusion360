# Development

Back to the [overview](index.md).

All commands are run from the root of the repository <https://github.com/sorglos-it/fusion360>.

## Folders

| Path | Content |
| --- | --- |
| `apps/desktop-system3e/System3E/` | The add-in as Fusion loads it (this folder goes into the release ZIP) |
| `apps/desktop-system3e/System3E/System3E.py` | Command, dialog, placement, points |
| `apps/desktop-system3e/System3E/system3e_core.py` | Shared machinery: text catalogue, language detection, panel lookup, handler registry, error type, version |
| `apps/desktop-system3e/System3E/System3E.manifest` | Fusion manifest: id, author, descriptions, version, `runOnStartup`, `supportedOS` |
| `apps/desktop-system3e/System3E/lang/` | `de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml`; `en.xml` is the reference |
| `apps/desktop-system3e/System3E/blocks/` | `blocks.json` and 74 preview pictures `<id>.png` (generated) |
| `apps/desktop-system3e/System3E/resources/System3E/` | Button icon in 16, 32 and 64 px |
| `apps/desktop-system3e/VERSION` | The version number, one line |
| `apps/desktop-system3e/tests/` | `test_addin.py`, `test_blocks.py` |
| `tools/system3e/` | `build_library.py`, `mesh_to_solid.py`, `points_sheet.py`, `make_icon.py` |
| `tools/set_version.py`, `tools/release.py` | Version and release tools for all add-ins of the repository |
| `docs/system3e/` | README, change log, licence, the points drawing, this documentation |
| `assets/system3e/` | The manufacturer's 3D file. **Not in the repository**, kept local. |
| `dist/` | Release ZIPs. Not in Git. |

`System3E.py` has two marked regions. Add-in specific code lives between `CONFIGURE` and `END OF TEMPLATE`; the
event handlers and `run`/`stop` below are the scaffold. The add-in was scaffolded from the repository's add-in
template.

## Tests

Both tests run without Fusion. They put stand-ins for the `adsk` modules into `sys.modules` and import the add-in.
Standard library only.

```bash
python apps/desktop-system3e/tests/test_addin.py
```

```bash
python apps/desktop-system3e/tests/test_blocks.py
```

Exit code 1 means at least one check failed.

`test_addin.py` checks:

| Section | Checks |
| --- | --- |
| 1) Layout | Folder, `System3E.py`, `System3E.manifest` and `lang/` exist and match the folder name |
| 2) Manifest | Valid JSON, `type` is `addin`, `autodeskProduct` is `Fusion360`, id looks like a GUID |
| 3) Import | The add-in imports, `run` and `stop` exist, `CMD_ID` is set, the core module file exists |
| 4) Language files | Every language file exists, declares its language, has every key of `en.xml` and no unknown key, keeps every placeholder `{0}`, has no empty text |
| 5) Text catalogue | Every language loads, an unknown language falls back to English, a missing key returns the key |
| 6) Icons | The three icon files exist and are real PNG files |

Options: `--addin <name>` and `--path <folder>` point the test at another add-in folder.

`test_blocks.py` checks:

| Section | Checks |
| --- | --- |
| 1) Library file | Unit is `mm`, 74 elements, unique ids and names, ids usable as file names |
| 2) Solids | Every element is a closed solid with flat faces, outlines run the right way round, the volume is possible, the corner is at the origin, size and points agree, the size fits the catalogue name, no two elements have the same shape |
| 3) Pictures | Every element has a PNG, no left-over pictures |
| 4) Add-in | The add-in reads every element; every family, anchor and point name has a text in all five languages; the default element and default anchor exist |
| 5) Points for clicking | Stacking height of `S1 WP` is 250 and of `EU 200 W` is 200; anchor positions; twelve named points per element, all in different places and on the element; `make_body()` turns every point into a vertex, defines every face, uses every edge once in each direction, and converts mm to cm |

What the tests cannot tell: whether Fusion accepts a body, creates the construction points or places the
occurrence correctly. That is only known inside Fusion.

State of testing inside Fusion: placing elements, the twelve points, **Placed by** and the offsets X/Y/Z have been
used by the author. The fixes of 1.0.0.1 are not yet confirmed inside Fusion.

## Rebuilding the element library

`blocks/blocks.json` and the pictures are generated. Do not edit them by hand.

Source: the manufacturer's 3D file `assets/system3e/SYSTEM 3E START.3ds`. It is **not part of the repository**.
Without it the library cannot be rebuilt; the script stops with "Source file missing".

```bash
python tools/system3e/build_library.py
```

```bash
python tools/system3e/build_library.py --no-pictures
```

The pictures need the Python package Pillow. `--no-pictures` skips them. The add-in itself needs neither.

What the build does:

1. `mesh_to_solid.read_3ds()` reads every triangle mesh of the file and converts it to mm.
2. `mesh_to_solid.solid_from_mesh()` welds points closer than 0.3 mm, sorts the triangles into planes, joins
   all triangles of one plane into outlines (with holes), drops points in the middle of straight edges, and
   checks that every edge is used once in each direction. The lowest corner of the bounding box becomes the origin.
3. The table `NAMES` gives each mesh number its catalogue name. The 3D file carries no names.
4. The four partition wall elements are added as plain boxes with the sizes from the table `PARTITION`.
5. `S0/2 200 P` is rebuilt (see below).
6. `straighten()` gives points that are meant to share a coordinate exactly the same value, to 0.1 mm.
7. `bend()` recomputes every face normal from its outline. `stack_level()` finds the stacking height.
8. `blocks.json` is written in the order of the table `FAMILIES`, and one picture per element is drawn.

The build stops if an element is not a closed solid, if two elements share an id, or if the rebuild check fails.

To inspect the source file alone:

```bash
python tools/system3e/mesh_to_solid.py "assets/system3e/SYSTEM 3E START.3ds" --report
```

It prints one line per mesh with size, point and face count, volume and state.

### Other tools

| Tool | Purpose |
| --- | --- |
| `python tools/system3e/points_sheet.py "S1 WP" docs/system3e/s1-wp-punkte.svg` | Draws one element with every point as an SVG. The points are taken from the add-in itself. The labels are German. |
| `python tools/system3e/make_icon.py` | Generates the button icon PNGs in 16, 32 and 64 px |

## Version numbers

A version has four parts, `v.x.y.z`: version, release, feature, build. Example: `1.1.0.0`.

The number is kept in two places: `apps/desktop-system3e/VERSION` and the `version` entry of the manifest. Fusion
and the dialog title read the manifest. Never edit the two by hand; use the tool:

```bash
python tools/set_version.py system3e 1.1.0.1
```

```bash
python tools/set_version.py --check
```

`--check` lists every add-in of the repository and reports any whose two numbers differ or are not `v.x.y.z`.
`all` instead of `system3e` sets every add-in.

Record every version in `docs/system3e/CHANGELOG.md`.

## Packing a release

```bash
python tools/release.py system3e
```

- Writes `dist/System3E-<version>.zip`.
- The ZIP holds the folder `System3E` exactly as Fusion wants it.
- `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db` and `.DS_Store` are left out.
- Compression is Deflate at the highest level, so every unpacker can read it.
- The ZIP is read back and tested after writing.
- The tool refuses to pack when `VERSION` and the manifest disagree.

The ZIP is then attached to a release on <https://github.com/sorglos-it/fusion360/releases>. This upload is not
part of the tool.

Before a release: run both tests, run `set_version.py --check`, update the change log and this documentation.

## Adding or changing texts

- `lang/en.xml` is the reference. Every other language file must have the same keys and the same placeholders.
- A key missing in a language is served from English at run time, but `test_addin.py` reports it as a failure.
- Names of dialog fields, families (`family.<id>`), anchors (`anchor.<id>`) and points (`point.<...>`) all come
  from these files.
- To support a further language, add it to `SUPPORTED_LANGUAGES` and `FUSION_LANGUAGE_MAP` in
  `system3e_core.py` and add the language file.

## Decisions and their reasons

These are taken from the comments in the code.

| Decision | Reason |
| --- | --- |
| The core module is removed from `sys.modules` before import. | Fusion caches imported modules. Without this an edited helper would keep its old version until Fusion restarts. |
| The core module has its own name, `system3e_core`. | Two add-ins built from the same template would otherwise overwrite each other's core module. |
| The command id has a prefix of its own (`thwSystem3ECmd`). | An id used twice silently hijacks the other add-in's button. |
| A stale command definition is deleted at start. | A definition left by a previous run would keep its old label and its old handler. |
| The panel is searched from a list of ids. | Panel ids move between Fusion versions. |
| All event handlers are kept in a registry. | Fusion holds only a weak reference. A handler not stored on the Python side is collected and its event silently stops firing. |
| Handlers are attached before the pre-selected point is taken over. | Whatever fails afterwards, the dialog must still work. |
| The selection made before the button was pressed is read before the inputs exist. | So that clicking a point and then the button just works. |
| All dialog values are read in one function. | Execute, preview and validation then look at exactly the same values. |
| The preview stays silent on errors. | It fires on every keystroke, also for half-typed values. Validation greys out **OK** instead. |
| The preview sets `isValidResult` to false. | Fusion then runs the real execute again for the final result. |
| Expected errors are an own error type with a language-independent key. | Validation can decide without parsing text. Unexpected errors are shown with their traceback. |
| A failed execute sets `executeFailed`. | Fusion then undoes what was built so far, instead of leaving an empty component behind. |
| The same element again is another occurrence of the same component. | Otherwise a parts list shows "S1 WP", "S1 WP (1)", "S1 WP (2)" as three parts instead of one part three times. |
| Components are found by an attribute, not by name. | Renaming a component then does no harm. Elements from before the attribute existed are found by name. |
| Components of a linked design are skipped. | They cannot be changed from the current design. |
| Body and points go into a base feature in parametric designs. | With the timeline on, a ready-made body and a point at plain coordinates have to live in a base feature. |
| The body is named while its base feature is still open. | Stated in the code; version 1.0.0.1 moved the naming there. |
| Only missing points are added to an existing component. | Components made by an older version have none or fewer. |
| The offset is applied after the rotation. | It runs along the design's X, Y and Z, not along the turned element. |
| Offset fields show mm, the value is cm. | cm is Fusion's own unit. |
| The version is read from the manifest, not hard-coded. | The dialog cannot drift away from the manifest, and there is one place to bump. |
| The version is part of the command name. | Fusion uses the command name as the dialog title; this is the only place where a version is visible while the dialog is open. |
| Language enum members are looked up with `getattr`. | A value this Fusion version does not know cannot break the add-in. English is the fallback. |
| The library stores points and flat faces, not Fusion files. | The manufacturer's file holds loose triangle meshes (triangles touching along part of an edge, doubled points, slivers). Fusion cannot make a body from that. |
| `S0/2 200 P` is rebuilt from `S0/2 250 P`, lowered by 50 mm. | Its mesh is damaged beyond repair (open on one side). The starter elements differ only in the height of the plain body under the top profile. `check_lowering()` proves the method on a pair where both meshes are sound (`S0/2 250 W` and `S0/2 200 W`). |
| Mesh numbers are mapped to names by a hand-made table. | The 3D file carries no names. The table was made by comparing every solid with the drawing on its catalogue card. Length tells the ends apart: 704 or 352 mm is "W", 3 mm more is a tongue ("P"). |
| Partition wall elements are plain boxes. | They are not in the 3D file; their sizes come from the catalogue cards. |
| Coordinates are straightened to 0.1 mm. | The source has float noise (106.4 next to 106.5 mm), which leaves faces slightly bent. |
| The stacking height is 50 mm below the top on profiled elements. | They carry the next course on the floor between the ridges; flat elements carry it on top. |
| Preview pictures are drawn with a depth buffer. | Hidden surfaces are removed per pixel. An earlier method showed faces in the wrong order on 16 pictures. |
| Preview pictures are drawn from the solids. | They are not taken from the manufacturer's catalogue. |

## Open points

- The left/right names of the corner and window elements in the table `NAMES` were matched by eye against the
  catalogue cards. They still need a check by someone who knows the system.
- The points, **Placed by** and the offsets need a test inside Fusion.

## Licence

MIT, Copyright (c) 2026 Sorglos Thomas Weirich. See [LICENSE](../LICENSE). The add-in is not affiliated with
SYSTEM 3E.
