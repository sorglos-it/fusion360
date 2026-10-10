# How it works

## Two files

| File | Role |
| --- | --- |
| Entry file `AddInTemplate.py` (later `<name>.py`) | What Fusion starts. Holds the settings, your functions, the event handlers, `run` and `stop` |
| Core module `addin_core.py` (later `<name>_core.py`) | Parts every add-in needs and that are easy to get wrong. Nothing in it belongs to one add-in |

Fusion finds an add-in by name: folder, `.py` file and `.manifest` file must carry the same name.

## What the core module contains

| Part | Task |
| --- | --- |
| `Strings` | Text catalogue read from `lang/<code>.xml`, with English as fallback |
| `detect_language()` | Finds the language Fusion is set to |
| `AddInError` | Error type for failures the user can fix. Carries a key that does not depend on the language |
| `HandlerRegistry` | Keeps event handlers alive |
| `find_panel()` | Finds the first toolbar panel of a list that exists |
| `add_button()` | Puts the command on a panel. Removes a control left over from a reload first |
| `remove_button()` | Takes the control and the command definition off the toolbar again |
| `report()` | Shows an unexpected error with its traceback in a message box |
| `read_version()` | Reads the version from the manifest |
| `display_name()` | Joins name and version: `Name (1.0.0.0)` |
| `FALLBACK_LANGUAGE`, `SUPPORTED_LANGUAGES`, `FUSION_LANGUAGE_MAP` | The language tables |

## Why the core module is renamed per add-in

All add-ins run in the same Python inside Fusion. They share one list of loaded modules (`sys.modules`).
If two add-ins both loaded a module called `addin_core`, they would overwrite each other's core module.

So the script renames the file to `<name in lower case>_core.py` and sets `_CORE_MODULE` in the entry file to match.

Consequence: every add-in has its **own copy** of the core module. A fix made in the template later does not reach add-ins created earlier. It has to be copied by hand.

## Loading the core module

The entry file does this before anything else:

1. It adds its own folder to Python's search path.
2. It removes the core module from `sys.modules`, if it is there.
3. It imports the core module by the name in `_CORE_MODULE`.

Reason for step 2: Fusion caches imported modules. Without it an edited core module would keep its old version until Fusion restarts. With it, stopping and running the add-in is enough.

## Handler registry

Fusion keeps only a weak reference to an event handler. A handler that Python no longer references is cleaned up, and its event stops firing – without any error message. The code comment calls this the most common way for an add-in to half-work.

`HandlerRegistry.add(event, handler)` connects the handler to the event **and** stores it in a list. `clear()` empties the list when the add-in stops.

## Start and stop

### `run(context)`

1. Loads the detected language into the text catalogue.
2. Deletes a command definition with the same `CMD_ID` left over from an earlier run. It would keep its old label and its old handler.
3. Creates the button definition: name with version, tooltip, icon folder (if it exists).
4. Connects `CommandCreatedHandler`.
5. Looks for a panel. If none is found it shows "No suitable toolbar panel was found." and ends.
6. Adds the button to the panel.

Any other error is shown as "Start-up failed:" with the traceback.

### `stop(context)`

1. Removes the control from the panel and deletes the command definition.
2. Empties the handler registry.

An error is shown as "Shutdown failed:" with the traceback.

## Event flow

```
button pressed
   -> commandCreated   build the dialog, connect the four handlers below
        -> inputChanged     a field changed        -> on_input_changed()
        -> validateInputs   may OK be pressed?     -> read_inputs(), validate()
        -> executePreview   show a preview         -> read_inputs(), validate(), build_result()
        -> execute          OK pressed             -> read_inputs(), validate(), build_result(), remember()
```

| Event | Handler | What it does | On error |
| --- | --- | --- | --- |
| created | `CommandCreatedHandler` | Marks the command as repeatable. Collects sketch lines selected before the button was pressed. Calls `build_inputs()`. Puts the first collected line into the selection field if that is still empty. Connects the other four handlers | Message box "Error while building the dialog:" with traceback |
| input changed | `InputChangedHandler` | Calls `on_input_changed()`. Does nothing while `_updating` is set | silent |
| validate | `ValidateHandler` | Calls `read_inputs()` and `validate()`. Sets `areInputsValid` to true, or to false on any error | OK is greyed out, no message |
| preview | `PreviewHandler` | Runs the whole command. Then sets `isValidResult` to `False`, so Fusion discards the preview and runs execute for the real result | silent, no preview |
| execute | `ExecuteHandler` | Runs the whole command, then `remember()` | `AddInError`: message box with the translated text. Anything else: "Error while creating the geometry:" with traceback |

"Runs the whole command" means `_run_command()`: `read_inputs()`, then `validate()`, then `build_result()`.

Points that follow from this:

- The selection is read **before** the inputs are created, and handed to the selection field afterwards. That is why "click a line, then press the button" works.
- The preview fires on every keystroke and sees half-typed values. So it stays silent on errors on purpose.
- Neither the preview nor the validation tells the user **why** something is wrong. Only execute shows a text.
- `build_result()` runs twice for one OK: once or more for the preview, once for the real result.
- Set `isValidResult` to `True` only if the preview already produced the final result.

## Two kinds of errors

| Kind | How it is raised | What the user sees |
| --- | --- | --- |
| Expected – the user can fix it | `fail('err.key')` raises `AddInError` | OK greyed out; a message box with the translated text only at execute |
| Unexpected – a bug | any other exception | A message box with the traceback, through `core.report()` |

`AddInError` stores the key (`err.key`) and the parameters (`err.params`). The text is looked up when the error is created.
The template's own code does not read the key afterwards; it is there for your code.

## Text catalogue and fallback

`S = core.Strings(LANG_DIR)` is created when the entry file is imported. English is loaded at once, so texts exist even before `run()`.
`run()` then loads the detected language.

How `load(code)` works:

1. A code that is not in `SUPPORTED_LANGUAGES` becomes `en`.
2. `en.xml` is read once and kept as the fallback.
3. The file of the chosen language is read as the current set.

How a text is found (`get(key, *args)`):

1. the text of the current language, if it exists and is not empty
2. otherwise the English text
3. otherwise the key itself, for example `in.width`

Then the placeholders are filled. If filling fails – for example a translation asks for `{1}` but only one value was given – the text is returned unfilled instead of raising an error.

A language file that is missing or is not valid XML counts as empty. Then every text comes from English.
If `en.xml` is missing or broken too, the keys themselves are shown.

## Language detection

See [settings.md](settings.md) for the order. Two details from the code:

- The Fusion language values are looked up by name with `getattr`. A value that this Fusion version does not know cannot break the add-in.
- The function never raises. In the worst case it returns English.

## Units

Fusion counts lengths in cm internally. The demo shows that:

- the start value `1.0` is shown as 10 mm
- the value read from the length field is in cm
- for the message "The length exceeds the selected line ({0} mm)." the length of the line is multiplied by 10 and shown with two decimals

## Data

The add-in reads its manifest and its language files. It writes no files.
