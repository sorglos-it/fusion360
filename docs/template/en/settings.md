# Settings

The add-in has no settings dialog and no settings file. Everything is set in three places:

1. the entry file `<name>.py`, block `CONFIGURE`
2. the manifest `<name>.manifest`
3. the language files in `lang/`

## Entry file

| Name | Template value | Meaning | Allowed values |
| --- | --- | --- | --- |
| `CMD_ID` | `thwAddInTemplateCmd` | Id of the command | Any text. It must be unique among **all** add-ins installed in Fusion. A collision silently takes over the other add-in's button. The script sets it to `<prefix><name>Cmd` |
| `WORKSPACE_ID` | `FusionSolidEnvironment` | Workspace that gets the button. This one is the design workspace | An id of a Fusion workspace |
| `PANEL_IDS` | `('SketchCreatePanel', 'SolidCreatePanel')` | Toolbar panels, tried in this order. The first one that exists gets the button | A list of panel ids, most wanted first |
| `IN_LINE` | `tplLine` | Id of the selection field | Any text, unique inside this command |
| `IN_LENGTH` | `tplLength` | Id of the length field | as above |
| `IN_FLIP` | `tplFlip` | Id of the check box | as above |
| `RESOURCE_FOLDER` | `resources/<name>` in the add-in folder | Folder with the icons. If it does not exist, the button gets no icon | A folder with `16x16.png`, `32x32.png`, `64x64.png` |
| `LANG_DIR` | `lang` in the add-in folder | Folder with the language files | A folder with `<code>.xml` files |
| `_last` | `{IN_LENGTH: 1.0, IN_FLIP: False}` | Start values, and the values remembered from the last call | One entry per remembered field |
| `_CORE_MODULE` | `addin_core` | Name of the core module. It stands above `CONFIGURE` | Set by the script to `<name in lower case>_core`. Keep it |

### Panel ids named in the code

| Id | Tab |
| --- | --- |
| `SketchCreatePanel`, `SketchModifyPanel` | SKETCH |
| `SolidCreatePanel`, `SolidModifyPanel` | SOLID |
| `InspectPanel`, `ToolsPanel` | UTILITIES |

Each panel is searched in the workspace first, then among all panels of Fusion.
The button is added as "promoted", which means it is shown directly on the panel.

### Remembered values

- `_last` holds the values for the next call of the command.
- They live in memory only. They are gone when Fusion closes or the add-in is restarted.
- Lengths are in **cm**, Fusion's internal unit, no matter what the field shows. `1.0` in a field shown in `mm` reads 10 mm.
- A value is only remembered if `remember()` copies it and `build_inputs()` uses it as the start value.

## Manifest

The manifest is a JSON file. Fusion reads it.

| Field | Template value | Meaning | Set by the script? |
| --- | --- | --- | --- |
| `autodeskProduct` | `Fusion360` | The product. The offline check demands this value | no |
| `type` | `addin` | The kind of extension. The offline check demands this value | no |
| `id` | `00000000-0000-0000-0000-000000000000` | GUID of the add-in. The zeros are a placeholder | yes, a new random GUID |
| `author` | `Your Name` | Author | yes, from `--author` |
| `description` | one text each for `""` (default), `de-DE`, `es-ES`, `fr-FR`, `it-IT` | Description of the add-in | **no – it still describes the template. Edit it** |
| `version` | `1.0.0.0` | Version. The add-in reads it and shows it in brackets after the command name | **no – it keeps the template's number. Set your own** |
| `runOnStartup` | `true` | Start the add-in together with Fusion | no |
| `supportedOS` | `windows\|mac` | Systems the add-in is for | no |
| `editEnabled` | `true` | A Fusion field. The template's code does not use it | no |

The version is written in one place only, the manifest. The code reads it from there, so the dialog title cannot differ from the manifest.
If the manifest cannot be read or has no version, the name is shown without brackets.

## Language files

### Format

One file per language: `lang/<code>.xml`.

```xml
<strings language="en">
  <string key="in.length">Length</string>
</strings>
```

- `en.xml` is the reference. Every key exists there.
- The attribute `language` must be the same as the code in the file name.
- Placeholders `{0}`, `{1}`, … are filled in by the add-in. They must stay in every translation.
- Other files may leave keys out. Missing keys are shown in English.

### Keys in the template

| Key | English text |
| --- | --- |
| `cmd.name` | Add-In Template |
| `cmd.tooltip` | Starting point for a Fusion 360 add-in. / Draws a tick at the midpoint of the selected line. (two lines) |
| `in.line` | Line |
| `in.line.prompt` | Select a sketch line |
| `in.length` | Length |
| `in.flip` | Flip direction |
| `err.no_selection` | Please select exactly one sketch line. |
| `err.length_positive` | The length must be greater than 0. |
| `err.zero_length` | The selected line has no length. |
| `err.too_long` | The length exceeds the selected line ({0} mm). |
| `msg.panel_missing` | No suitable toolbar panel was found. |
| `msg.exec_failed` | Error while creating the geometry: {0} |
| `msg.dialog_failed` | Error while building the dialog: {0} |
| `msg.run_failed` | Start-up failed: {0} |
| `msg.stop_failed` | Shutdown failed: {0} |

`cmd.name` is also the title of every message box.

### How the language is chosen

The language is chosen once, when the add-in starts. There is no switch in the add-in.

1. The language set in Fusion's preferences (the user language).
2. If that gives no supported language: the environment variables `LANG`, `LANGUAGE`, `LC_ALL`, in this order.
3. If that gives nothing: the language of the operating system.
4. Otherwise English.

Supported codes: `de`, `en`, `es`, `fr`, `it`.

After changing the language in Fusion, stop the add-in and run it again.

### Add a language

1. Copy `lang/en.xml` and name the copy after the two-letter code, for example `ja.xml`.
2. Set `language="ja"` in the first tag.
3. Translate the values. Keep the keys and the placeholders.
4. In the core module (`<name>_core.py`) add the code to `SUPPORTED_LANGUAGES`.
5. In the core module add the Fusion language to `FUSION_LANGUAGE_MAP`, for example `'JapaneseLanguage': 'ja'`.
6. Run the offline check, see [development.md](development.md).
