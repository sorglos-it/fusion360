# Installation

## Requirements

- Autodesk Fusion 360 on Windows or macOS. The add-in declares these two systems and no others.
- Nothing else. The add-in uses only the Python that is built into Fusion.

The code does not name a minimum Fusion version.

## Install from the release ZIP

1. Open <https://github.com/sorglos-it/fusion360/releases>.
2. Download the file `SketchGrid-<version>.zip`, for example `SketchGrid-1.1.0.0.zip`.
3. Unpack it into Fusion's add-ins folder:

   | System | Folder |
   | --- | --- |
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Check the result. Inside the add-ins folder there must now be a folder `SketchGrid`, and directly inside it the files `SketchGrid.py` and `SketchGrid.manifest`.

Do not rename the folder. Fusion expects the folder, the `.py` file and the `.manifest` file to have the same name.

## First start in Fusion

1. Start Fusion.
2. Open **Utilities → ADD-INS → Add-Ins**.
3. Select **SketchGrid** in the list.
4. Press **Run**.

The add-in is marked to run on startup in its manifest (`runOnStartup` is set). If it does not start by itself next time, tick **Run on Startup** in the same list.

After the start, a button named **Sketch Grid (1.1.0.0)** appears. The number in brackets is the installed version. The add-in looks for the **CREATE** panel of the sketch toolbar first, and if that does not exist, for the **CREATE** panel of the **SOLID** tab.

## Update

1. In Fusion, open **Utilities → ADD-INS → Add-Ins**, select **SketchGrid** and press **Stop**. Otherwise the old version stays in memory.
2. Delete the folder `SketchGrid` in the add-ins folder.
3. Unpack the new ZIP into the add-ins folder, as above.
4. Press **Run** again.
5. Check the version in brackets on the button.

The add-in stores no settings on disk. Nothing is lost by deleting the folder.

## Removal

1. In Fusion, stop the add-in (**Utilities → ADD-INS → Add-Ins**, select **SketchGrid**, **Stop**). This removes the button.
2. Delete the folder `SketchGrid` in the add-ins folder.

The add-in leaves no other files behind. Grids you already drew stay in your sketches; they are normal sketch geometry.
