# Troubleshooting

The texts below are the English ones from `lang/en.xml`. In another language the add-in shows the translation.
Every message box has the command name as its title.

## Messages of the demo command

These four come from `validate()`. While one of them applies, **OK** is greyed out and no preview is shown – without any text.
The text itself only appears as a message box if the error occurs at the moment the command is executed.

| Message | Cause | What to do |
| --- | --- | --- |
| "Please select exactly one sketch line." | The field **Line** is empty, or the selected object is not a sketch line | Pick one straight sketch line |
| "The length must be greater than 0." | **Length** is 0 or negative | Enter a length above 0 |
| "The selected line has no length." | Start and end point of the line lie on the same spot (only X and Y are compared) | Pick another line |
| "The length exceeds the selected line ({0} mm)." | **Length** is greater than the selected line. `{0}` is the length of the line in mm with two decimals | Enter a length up to that value, or pick a longer line |

## Messages of the add-in itself

The four messages with `{0}` show a Python traceback in place of `{0}`. The traceback names the file and the line of the error.

| Message | When | Cause | What to do |
| --- | --- | --- | --- |
| "No suitable toolbar panel was found." | at start | None of the ids in `PANEL_IDS` exists, neither in the workspace `WORKSPACE_ID` nor anywhere in Fusion. The add-in runs but has no button | Put panel ids that exist in your Fusion version into `PANEL_IDS`. See [settings.md](settings.md) |
| "Error while creating the geometry: {0}" | after OK | An unexpected error in `read_inputs()`, `validate()`, `build_result()` or `remember()` – a bug, not a wrong input | Read the last lines of the traceback and fix the code. If the user can cause it, catch the case in `validate()` with `fail('err.key')` |
| "Error while building the dialog: {0}" | when the button is pressed | An unexpected error in `build_inputs()` or while connecting the handlers | Read the traceback. Typical: the same input id used twice, or a wrong unit text |
| "Start-up failed: {0}" | when the add-in starts | An unexpected error in `run()` | Read the traceback |
| "Shutdown failed: {0}" | when the add-in stops | An unexpected error in `stop()` | Read the traceback. Restart Fusion if the button stays on the toolbar |

The "typical" causes in this table are examples. They were not reproduced in Fusion for this documentation.

## Messages of the scaffolding script

| Message | Cause | What to do |
| --- | --- | --- |
| `The name must start with a letter and contain only letters and digits - it becomes a Python module name. Got: '…'` | The name has a space, a hyphen, an underscore, another sign, or starts with a digit | Use a name such as `MyAddIn` |
| `Pick a name other than AddInTemplate.` | The name is the template's own name | Choose another name |
| `Template folder not found: …` | `apps/desktop-template/AddInTemplate` is missing. The script was moved, or the repository is incomplete | Run the script from a complete copy of the repository |
| `… already exists. Pass --force to overwrite it.` | The target folder exists | Choose another name or folder. `--force` deletes the existing folder with everything in it |
| `Use either --install or --out, not both.` | Both flags were given | Use one of them |

On a system that is not macOS, `--install` builds the path from the environment variable `APPDATA`. If it is not set (for example on Linux), the folder is created relative to the current folder. Use `--out` there.

## Messages of the version and packing tools

| Message | Cause | What to do |
| --- | --- | --- |
| `The version needs four numbers, like 1.0.0.0 - got '…'` | The version does not have four parts | Use `v.x.y.z`, for example `1.0.0.1` |
| `No add-in "…". There are: …` | The name is not a folder `apps/desktop-<name>` with exactly one manifest | Use a name from the list. The template is called `template` |
| `No "version" entry in …` | The manifest has no `version` field | Add the field to the manifest |
| `DIFFERENT OR NOT v.x.y.z` (from `--check`) | `VERSION` and the manifest differ, or the number does not have four parts | Run `python tools/set_version.py template <version>` |
| `template: VERSION and manifest disagree - run tools/set_version.py first.` | As above, noticed while packing | As above, then pack again |
| `template: … is damaged in the ZIP` | The ZIP test after packing failed | Pack again; check the disk |

## Offline check: FAIL and warn

The check is described in [development.md](development.md). A `FAIL` line names what is wrong. `warn` lines do not make the check fail.

| Warning | Meaning |
| --- | --- |
| `id is not the placeholder GUID` | The manifest still has the zeros as `id` |
| `author has been filled in` | The author is still `Your Name` |
| `CMD_ID is no longer the template default` | `CMD_ID` is still `thwAddInTemplateCmd` |
| `the core module was renamed, so it cannot clash with another add-in` | An add-in other than the template still uses `addin_core` |
| `cmd.tooltip no longer says TODO` | The English tooltip still contains `TODO` |

For the template itself the first three warnings are normal.

## Pitfalls

These come from the comments in the code.

| Symptom | Cause | What to do |
| --- | --- | --- |
| A code change has no effect | Fusion caches imported modules. An edited module keeps its old version until Fusion restarts | Stop the add-in and run it again. This works for the core module, because the entry file removes it from `sys.modules` before importing it. Give every further module of your own the same treatment |
| Another add-in's button does something strange, or yours does | Two add-ins use the same `CMD_ID`. The collision is silent | Use your own prefix and a unique id |
| Two add-ins from the template disturb each other | Both use a core module with the same name | Keep the renamed core module `<name>_core.py` |
| An event stops firing, without an error | Fusion holds handlers only weakly. A handler Python no longer references is cleaned up | Connect every handler with `_handlers.add(event, handler)` |
| The button keeps an old label or old behaviour | A command definition from an earlier run is still there | `run()` deletes it first. Keep that code |
| OK is grey and nobody knows why | Validation and preview do not show a reason | By design. Keep the rules simple and name them in the tooltip or the labels |
| The preview shows nothing | The preview swallows every error, also real bugs | Press OK with valid inputs. Execute shows the error with traceback |
| A message pops up on every keystroke | Error display was moved into the preview | Leave the preview silent. It fires on every keystroke, also on half-typed values |
| Values are ten times too big or small | Fusion counts in cm, whatever the field shows. `createByReal(1.0)` shown in `mm` reads 10 mm | Calculate in cm. Multiply by 10 only for display in mm |
| The sketch no longer updates after an error | `isComputeDeferred` was set to `True` and never reset | Reset it in a `finally` block, as `build_result()` does |
| `on_input_changed()` runs endlessly or twice | A value written back there fires the event again | Set `_updating` to `True` before the write and to `False` after it. It is a module variable: declare `global _updating` in the function |
| The button is missing after a Fusion update | Panel ids move between Fusion versions | List several ids in `PANEL_IDS`, most wanted first |
| The button has no icon | The folder `resources/<name>` is missing. Then the add-in passes no icon folder | Create the icons, see [development.md](development.md) |
| A text shows a key such as `in.width` | The key is missing in the language file **and** in `en.xml` | Add the key to `en.xml` |
| A text shows `{0}` instead of a value | The placeholders of the text do not fit the values given | Compare the text with the call `T('key', value)` |
| All texts are English | The language is not in `SUPPORTED_LANGUAGES`, or its file is missing or is not valid XML | Check the file and the tables in the core module |
| A fix in the template does not appear in my add-in | Every add-in has its own copy of the core module | Copy the fix by hand into `<name>_core.py` |
| Fusion does not list the add-in | Folder, `.py` and `.manifest` do not carry the same name | Give all three the same name. The offline check tests this |
