# Usage

## The demo command

The demo command draws a short line (a "tick") at the midpoint of a sketch line. The tick stands at a right angle to that line.
Its only job is to show that selection, preview, checks and translation work. Replace it with your own command.

In the unchanged template the command is called **Add-In Template**. Its tooltip reads:

> Starting point for a Fusion 360 add-in.
> Draws a tick at the midpoint of the selected line.

### The dialog

| Field | Type | Meaning | Start value |
| --- | --- | --- | --- |
| **Line** | selection, prompt "Select a sketch line" | The sketch line that gets the tick. Exactly one line. Only sketch lines can be picked | empty, or the line you had selected before |
| **Length** | value in mm | Length of the tick. Accepts expressions such as `2 * 3 mm` | 10 mm |
| **Flip direction** | check box | Draws the tick to the other side of the line | off |

### Try it

1. Open a sketch and draw a line.
2. Click the line.
3. Press the button **Add-In Template**. The line is already entered in **Line**.
4. Enter a **Length**. The preview shows the tick at once.
5. Tick **Flip direction** to turn the tick to the other side.
6. Press **OK**.

You can also press the button first and pick the line afterwards.

### Rules the command checks

| Rule | Message when broken |
| --- | --- |
| Exactly one sketch line is selected | "Please select exactly one sketch line." |
| The length is greater than 0 | "The length must be greater than 0." |
| The selected line is longer than 0 | "The selected line has no length." |
| The tick is not longer than the selected line | "The length exceeds the selected line ({0} mm)." |

While a rule is broken, **OK** is greyed out and the preview stays empty. The dialog does **not** say why.
The message text only appears as a message box if the error occurs when the command is executed.

### Other behaviour

- **Length** and **Flip direction** are remembered for the next call. They are forgotten when Fusion closes or the add-in is restarted.
- The command is repeatable (`isRepeatable` is set), so Fusion's "repeat last command" can start it again.
- Details of the geometry: only the X and Y values of the line's end points in the sketch are used. The tick is drawn at Z = 0 of the sketch.

Behaviour inside Fusion is described from the code. It was not tested in Fusion for this documentation.

## Make it your own add-in

First create a copy with the script, see [installation.md](installation.md). Then work in `<name>.py`.

The entry file has three zones:

| Zone | Content | Edit? |
| --- | --- | --- |
| above `CONFIGURE` | loads the core module | only when you add more modules of your own |
| `CONFIGURE` to `END OF TEMPLATE` | settings and your functions | **yes – this is yours** |
| below `END OF TEMPLATE` | the event handlers, `run` and `stop` | normally not |

### Step by step

1. **Set the ids.** Check `CMD_ID`, `WORKSPACE_ID` and `PANEL_IDS`. See [settings.md](settings.md).
2. **Name your inputs.** Replace `IN_LINE`, `IN_LENGTH`, `IN_FLIP` with ids for your own fields.
3. **Set start values.** Put the start value of every remembered field into `_last`. Lengths are in cm.
4. **Build the dialog** in `build_inputs(inputs)`.
5. **Read the dialog** in `read_inputs(inputs)`.
6. **Check the values** in `validate(values)`.
7. **Do the work** in `build_result(values)`.
8. **Remember values** in `remember(values)`.
9. **React to changes** in `on_input_changed(inputs, changed)`, if one field should change another.
10. **Write the texts.** Add your keys to `lang/en.xml`, then translate the other files. Replace the `TODO` tooltip.
11. **Adjust the pre-selection.** `CommandCreatedHandler` (below `END OF TEMPLATE`) collects sketch lines that were selected before the button was pressed. If your command needs another kind of object, change the type test there, or remove the block.
12. **Draw an icon**, see [development.md](development.md).
13. **Fill in the manifest**: description, author, version. See [settings.md](settings.md).
14. **Run the offline check**, see [development.md](development.md).
15. **Try it in Fusion.** After each change stop the add-in and run it again.

### The functions you edit

| Function | What it is for | Rules |
| --- | --- | --- |
| `build_inputs(inputs)` | Lays out the dialog. Every label comes from the text catalogue through `T('key')` | Returns the selection input. The caller puts the pre-selected line into it. Return `None` if you have no selection input |
| `read_inputs(inputs)` | Reads every value from the dialog in one place and returns a `dict` | Execute, preview and validation all call it, so they see the same numbers |
| `validate(values)` | Stops with `fail('err.key')` for anything the user must fix | It runs before drawing and again for the OK button. An impossible input greys out OK instead of failing halfway |
| `build_result(values)` | Does the actual work | Everything is already checked when it runs. It runs for the preview **and** for the real result |
| `remember(values)` | Copies values into `_last` for the next call | Called only after a successful execute |
| `on_input_changed(inputs, changed)` | Enables, disables or adjusts one field from another | Empty in the template. Set `_updating` around every value you write back, otherwise the write calls this function again |

### Helpers you call

| Helper | What it does |
| --- | --- |
| `T(key, *args)` | Returns the text for `key` in the active language. `args` fill `{0}`, `{1}`, … |
| `fail(key, *args)` | Raises an `AddInError` with the text for `key`. Use it for everything the user can fix |
| `core.report(ui, S, key)` | Shows an unexpected error with its traceback. Only for the really unexpected |

### Adding a text

1. Add a line to `lang/en.xml`: `<string key="in.width">Width</string>`
2. Use it in the code: `T('in.width')`
3. Add the same key to the other language files.

Keys missing in another language are shown in English. Placeholders such as `{0}` must stay in every translation.
