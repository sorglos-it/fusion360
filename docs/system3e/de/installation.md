# Installation

Zurück zur [Übersicht](index.md).

## Voraussetzungen

| Was | Einzelheit |
| --- | --- |
| Programm | Autodesk Fusion 360 |
| Betriebssystem | Windows oder macOS (das Add-In gibt beide als unterstützt an) |
| Zusätzliche Software | Keine. Das Add-In nutzt nur, was Fusion mitbringt. |
| Internet | Nur zum Herunterladen der ZIP-Datei. Das Add-In selbst öffnet keine Verbindung. |

## Aus dem Release-ZIP installieren

1. <https://github.com/sorglos-it/fusion360/releases> öffnen.
2. Die Datei `System3E-<version>.zip` herunterladen, zum Beispiel `System3E-1.2.0.0.zip`.
3. Das ZIP in den Add-Ins-Ordner von Fusion entpacken:

   | System | Ordner |
   | --- | --- |
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Das Ergebnis prüfen. Das ZIP enthält einen Ordner namens `System3E`. Nach dem Entpacken muss diese Datei
   vorhanden sein:

   `AddIns/System3E/System3E.py`

   Steht dort `AddIns/System3E/System3E/System3E.py`, liegt der Ordner eine Ebene zu tief. Den inneren Ordner nach
   oben verschieben.

Tipp für Windows: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` in die Adressleiste des Explorers eingeben und
die Eingabetaste drücken.

## Erster Start in Fusion

1. Fusion starten.
2. **Utilities → ADD-INS → Add-Ins** öffnen.
3. In der Liste **System3E** auswählen.
4. **Run** drücken.
5. Die Registerkarte **SOLID** öffnen. Die Schaltfläche **SYSTEM 3E Baustein** steht im Panel **Create**.

Die Schaltfläche zeigt die Version in Klammern, zum Beispiel **SYSTEM 3E Baustein (1.2.0.0)**.

Das Add-In ist so gekennzeichnet, dass es zusammen mit Fusion startet (`runOnStartup` in seiner Manifest-Datei).
Nach dem ersten Start muss **Run** normalerweise nicht noch einmal gedrückt werden.

Hinweis: Der Menüpfad in Schritt 2 stammt aus dem README des Projekts. Er lässt sich im Code des Add-Ins nicht
prüfen, und Fusion-Versionen können ihn anders benennen.

## Aktualisieren

1. In Fusion das Add-In stoppen (**Utilities → ADD-INS → Add-Ins**, **System3E** auswählen, **Stop**) oder Fusion
   schließen.
2. Den alten Ordner `System3E` im Add-Ins-Ordner löschen.
3. Das neue ZIP in den Add-Ins-Ordner entpacken, wie oben beschrieben.
4. Fusion starten oder noch einmal **Run** drücken.

Was mit den eigenen Konstruktionen geschieht:

- Bereits gesetzte Bausteine bleiben, wie sie sind. Es sind normale Fusion-Komponenten.
- Ein Baustein, der mit einer älteren Version gesetzt wurde, kann weniger als zwölf Punkte haben. Die fehlenden Punkte
  kommen hinzu, sobald derselbe Baustein in dieser Konstruktion das nächste Mal gesetzt wird.
- Die gemerkten Dialogwerte gehen verloren. Siehe [settings.md](settings.md).

## Entfernen

1. In Fusion das Add-In stoppen oder Fusion schließen.
2. Den Ordner `System3E` im Add-Ins-Ordner löschen.

Beim Stoppen entfernt das Add-In seine Schaltfläche aus der Werkzeugleiste. Es speichert nichts außerhalb des
eigenen Ordners.
Bausteine in den Konstruktionen bleiben; sie brauchen das Add-In nicht.
