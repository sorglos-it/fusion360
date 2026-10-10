# Installation

## Voraussetzungen

- Autodesk Fusion 360 unter Windows oder macOS. Das Add-in meldet diese beiden Systeme an und keine anderen.
- Sonst nichts. Das Add-in benutzt nur das Python, das in Fusion eingebaut ist.

Der Code nennt keine Mindestversion von Fusion.

## Aus dem Release-ZIP installieren

1. <https://github.com/sorglos-it/fusion360/releases> öffnen.
2. Die Datei `SketchGrid-<version>.zip` herunterladen, zum Beispiel `SketchGrid-1.1.0.0.zip`.
3. Sie in den Add-ins-Ordner von Fusion entpacken:

   | System | Ordner |
   | --- | --- |
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Das Ergebnis prüfen. Im Add-ins-Ordner muss es jetzt einen Ordner `SketchGrid` geben und direkt darin die Dateien `SketchGrid.py` und `SketchGrid.manifest`.

Den Ordner nicht umbenennen. Fusion erwartet, dass der Ordner, die `.py`-Datei und die `.manifest`-Datei denselben Namen haben.

## Erster Start in Fusion

1. Fusion starten.
2. **Utilities → ADD-INS → Add-Ins** öffnen.
3. In der Liste **SketchGrid** wählen.
4. **Run** drücken.

Das Add-in ist in seinem Manifest so gekennzeichnet, dass es beim Start von Fusion mitläuft (`runOnStartup` ist gesetzt). Startet es beim nächsten Mal nicht von selbst, in derselben Liste den Haken bei **Run on Startup** setzen.

Nach dem Start erscheint eine Schaltfläche mit dem Namen **Skizzenraster (1.1.0.0)**. Die Zahl in Klammern ist die installierte Version. Das Add-in sucht zuerst das Panel **CREATE** der Skizzen-Werkzeugleiste und, wenn es das nicht gibt, das Panel **CREATE** der Registerkarte **SOLID**.

## Aktualisieren

1. In Fusion **Utilities → ADD-INS → Add-Ins** öffnen, **SketchGrid** wählen und **Stop** drücken. Sonst bleibt die alte Version im Speicher.
2. Den Ordner `SketchGrid` im Add-ins-Ordner löschen.
3. Das neue ZIP in den Add-ins-Ordner entpacken, wie oben.
4. Wieder **Run** drücken.
5. Die Version in Klammern auf der Schaltfläche prüfen.

Das Add-in speichert keine Einstellungen auf dem Datenträger. Beim Löschen des Ordners geht nichts verloren.

## Entfernen

1. In Fusion das Add-in stoppen (**Utilities → ADD-INS → Add-Ins**, **SketchGrid** wählen, **Stop**). Das entfernt die Schaltfläche.
2. Den Ordner `SketchGrid` im Add-ins-Ordner löschen.

Das Add-in hinterlässt keine weiteren Dateien. Bereits gezeichnete Raster bleiben in den Skizzen; sie sind normale Skizzengeometrie.
