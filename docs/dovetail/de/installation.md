# Installation

## Voraussetzungen

- Autodesk Fusion 360 unter Windows oder macOS. Das Add-in meldet genau diese beiden Systeme an.
- Sonst nichts. Das Add-in läuft in dem Python, das Fusion mitbringt, und braucht keine zusätzlichen Pakete.

Im Code ist keine Mindestversion von Fusion genannt. Das Add-in wurde nicht gegen eine Liste von Fusion-Versionen
geprüft.

## Aus dem Release-ZIP installieren

1. <https://github.com/sorglos-it/fusion360/releases> öffnen.
2. Die Datei `Dovetail-<version>.zip` herunterladen, zum Beispiel `Dovetail-1.1.0.0.zip`.
3. Das ZIP in den Add-in-Ordner von Fusion entpacken:

   | System | Ordner |
   |---|---|
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Das Ergebnis prüfen. Das ZIP enthält einen Ordner mit dem Namen `Dovetail`. Nach dem Entpacken muss es das hier
   geben:

   ```
   AddIns/Dovetail/Dovetail.py
   AddIns/Dovetail/Dovetail.manifest
   AddIns/Dovetail/lang/
   AddIns/Dovetail/resources/
   ```

   Hat das Entpackprogramm einen zusätzlichen Ordner darum gelegt (zum Beispiel `AddIns/Dovetail-1.1.0.0/Dovetail/`),
   den inneren Ordner `Dovetail` eine Ebene nach oben schieben.

Den Ordner und die Dateien nicht umbenennen. Ordner, `.py`-Datei und `.manifest`-Datei müssen alle denselben Namen
tragen.

## Erster Start in Fusion

1. Fusion starten.
2. Die Liste der Add-ins öffnen: **Utilities → ADD-INS → Add-Ins**.
   (Der Wortlaut dieses Menüs kommt von Fusion und kann je nach Fusion-Version abweichen.)
3. Den Eintrag **Dovetail** wählen.
4. Den Haken bei **Run on Startup** setzen, falls er fehlt. Das Add-in verlangt das von sich aus in seinem Manifest.
5. **Run** drücken.

Das Add-in legt dann eine Schaltfläche in die Werkzeugleiste. Sie heißt **Schwalbenschwanz**, dahinter steht die
Version in Klammern, zum Beispiel *Schwalbenschwanz (1.1.0.0)*.

Wo die Schaltfläche erscheint:

| Reihenfolge | Ort |
|---|---|
| 1 | das Panel **Create** der Skizzen-Werkzeugleiste |
| 2 | wenn das fehlt: das Panel **Modify** der Skizzen-Werkzeugleiste |
| 3 | wenn auch das fehlt: das Panel **Create** der Registerkarte Solid |

Das Add-in nimmt den ersten dieser Orte, den es gibt. Die Schaltfläche liegt direkt auf der Werkzeugleiste, nicht nur
im Aufklappmenü des Panels.

Gibt es keinen der drei, erscheint die Meldung „Kein passendes Toolbar-Panel gefunden.“ Siehe
[troubleshooting.md](troubleshooting.md).

## Aktualisieren

1. In Fusion die Liste der Add-ins öffnen und Dovetail **stoppen**. Sonst bleibt die alte Version im Speicher.
2. Den alten Ordner `Dovetail` aus dem Add-in-Ordner löschen.
3. Das neue ZIP in den Add-in-Ordner entpacken, wie oben beschrieben.
4. Wieder **Run** drücken oder Fusion neu starten.
5. Die Version im Namen der Schaltfläche oder im Titel des Dialogs prüfen.

Das Add-in speichert keine Einstellungen auf dem Datenträger. Beim Löschen des alten Ordners geht nichts verloren.

Hinweis aus der früheren README, im heutigen Code nicht nachprüfbar: Sehr alte Versionen hießen `Schwalbenschwanz`.
Liegt ein solcher Ordner noch im Add-in-Ordner, dieses Add-in stoppen und den Ordner löschen. Sonst gibt es zwei
Schaltflächen.

## Entfernen

1. In Fusion die Liste der Add-ins öffnen und Dovetail **stoppen**. Das entfernt die Schaltfläche und den Befehl.
2. Fusion schließen.
3. Den Ordner `Dovetail` aus dem Add-in-Ordner löschen.

Das Add-in schreibt keine weiteren Dateien und keine Einstellungen. Bereits gezeichnete Verbindungen bleiben in den
Skizzen; es sind gewöhnliche Skizzenlinien.
