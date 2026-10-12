# Installation

Back to the [overview](index.md).

## Requirements

| What | Detail |
| --- | --- |
| Program | Autodesk Fusion 360 |
| Operating system | Windows or macOS (the add-in declares both as supported) |
| Extra software | None. The add-in uses only what Fusion brings along. |
| Internet | Only for downloading the ZIP file. The add-in itself opens no connection. |

## Install from the release ZIP

1. Open <https://github.com/sorglos-it/fusion360/releases>.
2. Download the file `System3E-<version>.zip`, for example `System3E-1.2.0.0.zip`.
3. Unpack the ZIP into Fusion's add-ins folder:

   | System | Folder |
   | --- | --- |
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Check the result. The ZIP contains one folder named `System3E`. After unpacking, this file must exist:

   `AddIns/System3E/System3E.py`

   If you see `AddIns/System3E/System3E/System3E.py`, the folder is one level too deep. Move the inner folder up.

Tip for Windows: type `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` into the address bar of the Explorer and
press Enter.

## First start in Fusion

1. Start Fusion.
2. Open **Utilities → ADD-INS → Add-Ins**.
3. Select **System3E** in the list.
4. Press **Run**.
5. Open the **SOLID** tab. The button **SYSTEM 3E element** is in the **Create** panel.

The button shows the version in brackets, for example **SYSTEM 3E element (1.2.0.0)**.

The add-in is marked to start together with Fusion (`runOnStartup` in its manifest file). After the first start you
normally do not have to press **Run** again.

Note: the menu path in step 2 is taken from the project's README. It cannot be checked in the add-in's code, and
Fusion versions may name it differently.

## Update

1. In Fusion, stop the add-in (**Utilities → ADD-INS → Add-Ins**, select **System3E**, **Stop**), or close Fusion.
2. Delete the old folder `System3E` in the add-ins folder.
3. Unpack the new ZIP into the add-ins folder, as described above.
4. Start Fusion, or press **Run** again.

What happens to your designs:

- Elements already placed stay as they are. They are normal Fusion components.
- An element placed with an older version may have fewer than twelve points. The missing points are added the
  next time you place the same element in that design.
- The remembered dialog values are lost. See [settings.md](settings.md).

## Removal

1. In Fusion, stop the add-in, or close Fusion.
2. Delete the folder `System3E` in the add-ins folder.

When the add-in stops, it removes its button from the toolbar. It stores nothing outside its own folder.
Elements in your designs stay; they do not need the add-in.
