# Installation

## Requirements

| What | Needed for |
| --- | --- |
| Autodesk Fusion 360 on Windows or macOS | running the add-in |
| Python 3 on your computer | the tools in `tools/` (scaffolding, offline check, icons, version, packing) |

The add-in itself needs nothing extra. It only uses the Python that comes inside Fusion.
The tools use the Python standard library only. Nothing has to be installed with `pip`.

## Get the repository

There is no release ZIP for version 1.0.0.0. Use the repository.

1. Open <https://github.com/sorglos-it/fusion360>.
2. Clone it, or download it as a ZIP and unpack it.
3. Open a terminal in the repository folder.

## Create a new add-in

```bash
python tools/template/new_addin.py MyAddIn --install
```

This creates the add-in `MyAddIn` directly in Fusion's add-in folder.

### Rules for the name

- It must start with a letter.
- It may contain letters and digits only. No spaces, no hyphens, no underscores.
- It must not be `AddInTemplate`.

The name becomes a Python module name. That is why the rules are strict.

### All flags

| Flag | Default | Effect |
| --- | --- | --- |
| `name` (required) | – | Name of the add-in, for example `MyAddIn` |
| `--install` | off | Create it directly in Fusion's add-in folder |
| `--out DIR` | the folder that contains the repository | Create it in `DIR` instead. `DIR` is created if it does not exist |
| `--author NAME` | `Your Name` | Written into the `author` field of the manifest |
| `--prefix STR` | `thw` | Prefix of the command id. The id becomes `<prefix><name>Cmd` |
| `--force` | off | Overwrite an existing folder of that name |
| `-h`, `--help` | – | Show the help text |

Notes:

- `--install` and `--out` cannot be used together.
- Without `--install` and without `--out` the add-in is created **next to** the repository folder, not inside it.
- `--force` **deletes the whole existing folder first**, including your own changes in it. Then it creates a fresh copy.
- Choose your own `--prefix`. `thw` is the template author's prefix.

### What the script does

1. Copies `apps/desktop-template/AddInTemplate` to `<target>/<name>` (without `__pycache__` and `.pyc` files).
2. Renames `AddInTemplate.py` to `<name>.py` and `AddInTemplate.manifest` to `<name>.manifest`.
3. Renames `addin_core.py` to `<name in lower case>_core.py`, for example `myaddin_core.py`.
4. Renames the icon folder `resources/AddInTemplate` to `resources/<name>`.
5. In the entry file: sets `_CORE_MODULE` and `CMD_ID`, and replaces every `AddInTemplate` with the new name.
6. In the manifest: writes a new random GUID into `id` and your author name into `author`.
7. In every `lang/*.xml`: sets `cmd.name` to the new name and `cmd.tooltip` to the name plus the line `TODO: describe what this command does.`

The script does **not** change the `description` and the `version` in the manifest. Edit them yourself, see [settings.md](settings.md).

### What you get

```
MyAddIn/
  MyAddIn.py            entry file - your code goes here
  myaddin_core.py       core module, renamed for this add-in
  MyAddIn.manifest      what Fusion reads, with a new GUID
  lang/
    en.xml              reference: every key exists here
    de.xml es.xml fr.xml it.xml
  resources/
    MyAddIn/            16x16.png 32x32.png 64x64.png
```

At the end the script prints the created path, the entry file, the core module, the command id and the next steps.

## Fusion's add-in folder

| System | Path |
| --- | --- |
| Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
| macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

If you created the add-in without `--install`, copy the whole folder `MyAddIn` into this folder.

Folder, entry file and manifest must carry the same name: `MyAddIn/MyAddIn.py` and `MyAddIn/MyAddIn.manifest`.

## First start in Fusion

1. Start Fusion 360.
2. Open **Utilities → ADD-INS → Add-Ins** (this is the path the script prints).
3. Select your add-in and press **Run**.
4. Open a sketch. The button is on the **SKETCH** tab, in the create panel. If that panel does not exist, it goes to the create panel of the **SOLID** tab.

The manifest has `runOnStartup` set to `true`.

The button and the dialog title show the command name with the version in brackets, for example `Add-In Template (1.0.0.0)`.

These steps follow the code and the script output. They were not tested in Fusion for this documentation.

### Trying the template itself

You can also run the unchanged template: copy the folder `apps/desktop-template/AddInTemplate` into Fusion's add-in folder and start it as above. Its command is called `Add-In Template`.

## Update

There is no update function.

- An add-in created from the template holds its own copy of all files. Changes made in the template later do not reach it.
- To take over a fix, copy the change by hand into your `<name>_core.py` or your entry file.
- Running the script again with `--force` is not an update. It deletes your add-in folder and creates a fresh, empty copy.

## Removal

1. In Fusion open **Utilities → ADD-INS → Add-Ins**, select the add-in and stop it. On stop the add-in removes its button and its command from the toolbar.
2. Close Fusion.
3. Delete the add-in's folder from Fusion's add-in folder.

The add-in stores nothing outside its own folder. The remembered values live only in memory until Fusion closes.
