# Development

## Folders

| Path | Content |
| --- | --- |
| `apps/desktop-template/AddInTemplate/` | The template add-in, as Fusion needs it |
| `apps/desktop-template/AddInTemplate/AddInTemplate.py` | Entry file |
| `apps/desktop-template/AddInTemplate/addin_core.py` | Core module |
| `apps/desktop-template/AddInTemplate/AddInTemplate.manifest` | Manifest |
| `apps/desktop-template/AddInTemplate/lang/` | `de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` |
| `apps/desktop-template/AddInTemplate/resources/AddInTemplate/` | Icons `16x16.png`, `32x32.png`, `64x64.png` |
| `apps/desktop-template/VERSION` | Version number of this part |
| `apps/desktop-template/tests/test_addin.py` | Offline check |
| `tools/template/new_addin.py` | Scaffolding script, see [installation.md](installation.md) |
| `tools/template/make_icon.py` | Icon tool |
| `tools/template/test_addin.py` | Forwards to the offline check (old path) |
| `tools/set_version.py` | Sets version numbers, for all add-ins of the repository |
| `tools/release.py` | Packs an add-in into a ZIP, for all add-ins of the repository |
| `docs/template/` | README, CHANGELOG, LICENSE and this documentation |
| `dist/` | Packed ZIP files. Not in Git |

There is no build step. The add-in runs as it is. All tools use the Python standard library only.

## Offline check

The check tests an add-in without starting Fusion. The code comment calls it the only feedback loop that needs no restart.

```bash
python apps/desktop-template/tests/test_addin.py                    # the template itself
python apps/desktop-template/tests/test_addin.py --path ../MyAddIn  # an add-in next to the repository
```

| Flag | Default | Effect |
| --- | --- | --- |
| `--addin NAME` | `AddInTemplate` | Folder name inside `apps/desktop-template` of this repository |
| `--path DIR` | – | Full path to an add-in folder. Wins over `--addin` |

For an add-in created with `--install`, give its folder in Fusion's add-in folder to `--path`.

The old command `python tools/template/test_addin.py` still works. It forwards to the check with the same arguments, the same output and the same exit code.

### How it works

It puts empty stand-ins for the modules `adsk`, `adsk.core` and `adsk.fusion` in place and then imports the add-in.
Only the handler base classes are real (empty) classes. So the check proves that the file imports and that the texts are in order. It does **not** run any Fusion call: no dialog, no geometry, no `run()`.

### What it checks

| Section | Checks |
| --- | --- |
| 1) Layout | The folder exists. `<name>.py` and `<name>.manifest` match the folder name. `lang/` exists |
| 2) Manifest | Valid JSON. `type` is `addin`. `autodeskProduct` is `Fusion360`. `id` looks like a GUID. Warnings: placeholder GUID, author `Your Name` |
| 3) Import | The add-in imports. `run` and `stop` exist. `CMD_ID` is set. `_CORE_MODULE` has a matching file. Warnings: `CMD_ID` still the template value, core module not renamed |
| 4) Language files | `SUPPORTED_LANGUAGES` is available. `en.xml` exists and has keys. For every supported language: the file exists, declares the right `language`, has every key, has no unknown key, keeps every placeholder, has no empty text |
| 5) Text catalogue | Every language loads and returns a `cmd.name`. An unknown language falls back to English. A missing key returns the key. Warning: the tooltip still says `TODO` |
| 6) Icons | `resources/<name>/` exists. The three PNG files exist and start with the PNG signature |

### Result

- Lines start with `ok`, `FAIL` or `warn`.
- With at least one `FAIL` the script ends with exit code 1 and prints the number of failures.
- Warnings do not change the exit code.
- Without failures it prints `all checks passed`.

Run for this documentation on the template, version 1.0.0.0: `3 warning(s)`, `all checks passed`. The three warnings (placeholder GUID, author, command id) are normal for the template.

## Icon tool

Fusion wants three PNG files with transparency: 16x16, 32x32 and 64x64 pixels, in the folder passed to the button definition.

```bash
python tools/template/make_icon.py                            # the template's placeholder
python tools/template/make_icon.py --root .. --addin MyAddIn  # an add-in next to the repository
```

| Flag | Default | Effect |
| --- | --- | --- |
| `--addin NAME` | `AddInTemplate` | Add-in folder name |
| `--root DIR` | `apps/desktop-template` of this repository | Folder that holds the add-in |

The files are written to `<root>/<addin>/resources/<addin>/`. The folder is created if needed. Existing icons are overwritten.

To draw your own icon, edit the script:

| Name | Meaning |
| --- | --- |
| `SHAPES` | List of `(colour, polygon)`. Points are from 0 to 1, with y pointing **up**. Where shapes overlap, the one listed first stays on top |
| `DARK`, `ACCENT` | The two colours as RGB values |
| `SS` | Samples per pixel edge for smooth edges. 4 gives clean edges down to 16 px |

The placeholder shows four corner brackets and a diagonal. It looks like a placeholder on purpose. Replace it before you pass your add-in on.

## Version numbers

Versions have four parts: `v.x.y.z` (version, release, feature, build). Current: `1.0.0.0`.

The number is kept in two places:

- `apps/desktop-template/VERSION`
- the `version` field of the manifest – Fusion and the dialog title read this one

Never edit them by hand. Use the tool, it writes both:

```bash
python tools/set_version.py template 1.0.0.1   # this part
python tools/set_version.py all 1.0.0.0        # every add-in of the repository
python tools/set_version.py --check            # report differences
```

- `template` is the folder name `apps/desktop-template` without `desktop-`.
- `--check` prints one line per add-in, ends with `ok` or `DIFFERENT OR NOT v.x.y.z`, and returns exit code 1 if any line is wrong.
- The tool works on the add-ins of this repository only. In an add-in of your own outside the repository, change the `version` field of its manifest directly – that is the only place there.

## Packing

```bash
python tools/release.py template
python tools/release.py all
```

- Writes `dist/AddInTemplate-<version>.zip`.
- The ZIP holds the folder `AddInTemplate` as Fusion wants it. Unpack it into Fusion's add-in folder.
- Left out: `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compression: Deflate at the highest level, so every unpacker can read it.
- It refuses to pack if `VERSION` and the manifest differ or the number does not have four parts.
- After packing it tests the ZIP and prints the number of files and the size.
- The tools (`tools/`) are not in the ZIP. They exist only in the repository.

No ZIP of version 1.0.0.0 has been released. The template is used from the repository.

## Decisions and their reasons

| Decision | Reason given in the code |
| --- | --- |
| Entry file and core module are separate | The core holds what every add-in needs and what is easy to get wrong. Your code stays between two markers |
| The core module is renamed per add-in | Two add-ins from this template must not overwrite each other's core module in `sys.modules` |
| The core module is removed from `sys.modules` before import | Fusion caches modules. This way "stop, run" picks up changes |
| All handlers go through `HandlerRegistry` | Fusion holds handlers weakly. Unreferenced ones are collected and the event stops firing silently |
| `PANEL_IDS` is a list, with a global search as second try | Panel ids move between Fusion versions |
| A stale command definition is deleted at start | It would keep its old label and its old handler |
| `read_inputs()` is the only place that reads the dialog | Execute, preview and validation look at exactly the same numbers |
| `validate()` runs before drawing and again for the OK button | An impossible input disables OK instead of failing halfway through |
| The preview swallows errors | It fires on every keystroke, also on half-typed values |
| The preview sets `isValidResult` to `False` | Fusion then runs execute for the real result |
| Errors carry a key, not only a text | The reason is known without parsing text in some language |
| `report()` is only for unexpected errors | What the user can fix should be an `AddInError`, so OK is blocked instead of a dialog popping up |
| English is the fallback for every text | A half-finished translation shows English instead of raw keys |
| Fusion's language values are looked up by name | A value this Fusion version does not know cannot break the add-in |
| Language detection never raises | A Fusion build with an unexpected value still starts the add-in |
| The version is read from the manifest | The dialog cannot drift away from the manifest. One place to raise it |
| The version is part of the command name | Fusion uses that name as dialog title. It is the only place where a version is visible while the dialog is open. It also shows on the button – there is only the one name |
| `isComputeDeferred` is reset in `finally` | After an error the sketch would otherwise stop updating |
| The selection is read before the inputs exist | "Click a line, then press the button" works |
| The placeholder icon looks like a placeholder | An icon that was not replaced is easy to spot |
| The script writes files with `\n` line ends and UTF-8 | Not explained in the code |
| Keys, identifiers and comments are English | Not explained in the code; the existing README says a translator then never has to open a `.py` file |

## Licence

MIT. Author: Sorglos Thomas Weirich. See [LICENSE](../LICENSE).
