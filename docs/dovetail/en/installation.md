# Installation

## Requirements

- Autodesk Fusion 360 on Windows or macOS. The add-in declares exactly these two systems.
- Nothing else. The add-in runs in the Python that Fusion brings along and uses no extra packages.

No minimum Fusion version is stated in the code. The add-in was not tested against a list of Fusion versions.

## Install from the release ZIP

1. Open <https://github.com/sorglos-it/fusion360/releases>.
2. Download the file `Dovetail-<version>.zip`, for example `Dovetail-1.1.0.0.zip`.
3. Unpack the ZIP into Fusion's add-in folder:

   | System | Folder |
   |---|---|
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Check the result. The ZIP contains one folder named `Dovetail`. After unpacking, this must exist:

   ```
   AddIns/Dovetail/Dovetail.py
   AddIns/Dovetail/Dovetail.manifest
   AddIns/Dovetail/lang/
   AddIns/Dovetail/resources/
   ```

   If your unpacker created an extra folder around it (for example `AddIns/Dovetail-1.1.0.0/Dovetail/`), move the
   inner `Dovetail` folder up one level.

Do not rename the folder or the files. Folder, `.py` file and `.manifest` file must all carry the same name.

## First start in Fusion

1. Start Fusion.
2. Open the list of add-ins: **Utilities → ADD-INS → Add-Ins**.
   (The wording of this menu comes from Fusion and can differ between Fusion versions.)
3. Select the entry **Dovetail**.
4. Tick **Run on Startup** if it is not ticked. The add-in asks for this by itself in its manifest.
5. Press **Run**.

The add-in then adds one button to the toolbar. Its name is **Dovetail** followed by the version in brackets,
for example *Dovetail (1.1.0.0)*.

Where the button appears:

| Order | Place |
|---|---|
| 1 | the **Create** panel of the sketch toolbar |
| 2 | if that is missing: the **Modify** panel of the sketch toolbar |
| 3 | if that is missing too: the **Create** panel of the Solid tab |

The add-in takes the first of these that exists. The button is placed directly on the toolbar, not only in the
drop-down menu of the panel.

If none of the three exists, you get the message "No suitable toolbar panel was found." See
[troubleshooting.md](troubleshooting.md).

## Update

1. In Fusion, open the list of add-ins and **stop** Dovetail. Otherwise the old version stays in memory.
2. Delete the old folder `Dovetail` from the add-in folder.
3. Unpack the new ZIP into the add-in folder, as described above.
4. Press **Run** again, or restart Fusion.
5. Check the version in the button name or in the dialog title.

The add-in stores no settings on disk. Nothing is lost by deleting the old folder.

Note from the earlier README, not checkable in the current code: very old versions were named `Schwalbenschwanz`.
If such a folder is still in your add-in folder, stop that add-in and delete the folder. Otherwise you get two buttons.

## Removal

1. In Fusion, open the list of add-ins and **stop** Dovetail. This removes the button and the command.
2. Close Fusion.
3. Delete the folder `Dovetail` from the add-in folder.

The add-in writes no other files and no settings. Joints already drawn stay in your sketches; they are ordinary
sketch lines.
