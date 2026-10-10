# Installation

## Voraussetzungen

| Was | Wofür nötig |
| --- | --- |
| Autodesk Fusion 360 unter Windows oder macOS | um das Add-In auszuführen |
| Python 3 auf dem eigenen Rechner | für die Werkzeuge in `tools/` (Gerüst, Offline-Prüfung, Symbole, Version, Packen) |

Das Add-In selbst braucht nichts zusätzlich. Es nutzt nur das Python, das in Fusion steckt.
Die Werkzeuge nutzen nur die Python-Standardbibliothek. Mit `pip` muss nichts installiert werden.

## Das Repository holen

Für Version 1.0.0.0 gibt es kein Release-ZIP. Das Repository benutzen.

1. <https://github.com/sorglos-it/fusion360> öffnen.
2. Es klonen, oder es als ZIP herunterladen und entpacken.
3. Im Ordner des Repositorys ein Terminal öffnen.

## Ein neues Add-In anlegen

```bash
python tools/template/new_addin.py MyAddIn --install
```

Das legt das Add-In `MyAddIn` direkt im Add-In-Ordner von Fusion an.

### Regeln für den Namen

- Er muss mit einem Buchstaben beginnen.
- Er darf nur Buchstaben und Ziffern enthalten. Keine Leerzeichen, keine Bindestriche, keine Unterstriche.
- Er darf nicht `AddInTemplate` sein.

Der Name wird ein Python-Modulname. Deshalb sind die Regeln streng.

### Alle Schalter

| Schalter | Vorgabe | Wirkung |
| --- | --- | --- |
| `name` (Pflicht) | – | Name des Add-Ins, zum Beispiel `MyAddIn` |
| `--install` | aus | Es direkt im Add-In-Ordner von Fusion anlegen |
| `--out DIR` | der Ordner, in dem das Repository liegt | Es stattdessen in `DIR` anlegen. `DIR` wird angelegt, wenn es nicht existiert |
| `--author NAME` | `Your Name` | Wird in das Feld `author` des Manifests geschrieben |
| `--prefix STR` | `thw` | Präfix der Befehls-id. Die id wird `<prefix><name>Cmd` |
| `--force` | aus | Einen vorhandenen Ordner dieses Namens überschreiben |
| `-h`, `--help` | – | Den Hilfetext anzeigen |

Hinweise:

- `--install` und `--out` lassen sich nicht zusammen benutzen.
- Ohne `--install` und ohne `--out` wird das Add-In **neben** dem Ordner des Repositorys angelegt, nicht darin.
- `--force` **löscht zuerst den ganzen vorhandenen Ordner**, samt den eigenen Änderungen darin. Dann legt es eine frische Kopie an.
- Ein eigenes `--prefix` wählen. `thw` ist das Präfix des Autors der Vorlage.

### Was das Skript macht

1. Kopiert `apps/desktop-template/AddInTemplate` nach `<target>/<name>` (ohne `__pycache__` und `.pyc`-Dateien).
2. Benennt `AddInTemplate.py` in `<name>.py` um und `AddInTemplate.manifest` in `<name>.manifest`.
3. Benennt `addin_core.py` in `<name in Kleinbuchstaben>_core.py` um, zum Beispiel `myaddin_core.py`.
4. Benennt den Symbolordner `resources/AddInTemplate` in `resources/<name>` um.
5. In der Startdatei: setzt `_CORE_MODULE` und `CMD_ID` und ersetzt jedes `AddInTemplate` durch den neuen Namen.
6. Im Manifest: schreibt eine neue zufällige GUID in `id` und den Autorennamen in `author`.
7. In jeder `lang/*.xml`: setzt `cmd.name` auf den neuen Namen und `cmd.tooltip` auf den Namen plus die Zeile `TODO: describe what this command does.`

Das Skript ändert `description` und `version` im Manifest **nicht**. Sie selbst bearbeiten, siehe [settings.md](settings.md).

### Was dabei entsteht

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

Am Ende gibt das Skript den angelegten Pfad, die Startdatei, das Kernmodul, die Befehls-id und die nächsten Schritte aus.

## Der Add-In-Ordner von Fusion

| System | Pfad |
| --- | --- |
| Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
| macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

Wurde das Add-In ohne `--install` angelegt, den ganzen Ordner `MyAddIn` in diesen Ordner kopieren.

Ordner, Startdatei und Manifest müssen denselben Namen tragen: `MyAddIn/MyAddIn.py` und `MyAddIn/MyAddIn.manifest`.

## Erster Start in Fusion

1. Fusion 360 starten.
2. **Utilities → ADD-INS → Add-Ins** öffnen (das ist der Pfad, den das Skript ausgibt).
3. Das eigene Add-In auswählen und **Run** drücken.
4. Eine Skizze öffnen. Die Schaltfläche steht auf der Registerkarte **SKETCH**, im Panel zum Erstellen. Gibt es dieses Panel nicht, kommt sie in das Panel zum Erstellen der Registerkarte **SOLID**.

Im Manifest steht `runOnStartup` auf `true`.

Die Schaltfläche und der Dialogtitel zeigen den Befehlsnamen mit der Version in Klammern, zum Beispiel `Add-In-Vorlage (1.0.0.0)`.

Diese Schritte folgen dem Code und der Ausgabe des Skripts. Sie wurden für diese Dokumentation nicht in Fusion geprüft.

### Die Vorlage selbst ausprobieren

Auch die unveränderte Vorlage lässt sich ausführen: den Ordner `apps/desktop-template/AddInTemplate` in den Add-In-Ordner von Fusion kopieren und wie oben starten. Ihr Befehl heißt `Add-In-Vorlage`.

## Aktualisieren

Es gibt keine Funktion zum Aktualisieren.

- Ein Add-In, das aus der Vorlage angelegt wurde, hat seine eigene Kopie aller Dateien. Änderungen, die später in der Vorlage gemacht werden, erreichen es nicht.
- Um eine Korrektur zu übernehmen, die Änderung von Hand in die eigene `<name>_core.py` oder die eigene Startdatei kopieren.
- Das Skript noch einmal mit `--force` auszuführen ist keine Aktualisierung. Es löscht den Add-In-Ordner und legt eine frische, leere Kopie an.

## Entfernen

1. In Fusion **Utilities → ADD-INS → Add-Ins** öffnen, das Add-In auswählen und stoppen. Beim Stoppen entfernt das Add-In seine Schaltfläche und seinen Befehl aus der Werkzeugleiste.
2. Fusion schließen.
3. Den Ordner des Add-Ins aus dem Add-In-Ordner von Fusion löschen.

Das Add-In speichert nichts außerhalb des eigenen Ordners. Die gemerkten Werte liegen nur im Arbeitsspeicher, bis Fusion geschlossen wird.
