# Einstellungen

Das Add-In hat keinen Einstellungsdialog und keine Einstellungsdatei. Alles wird an drei Stellen eingestellt:

1. in der Startdatei `<name>.py`, Block `CONFIGURE`
2. im Manifest `<name>.manifest`
3. in den Sprachdateien in `lang/`

## Startdatei

| Name | Wert in der Vorlage | Bedeutung | Erlaubte Werte |
| --- | --- | --- | --- |
| `CMD_ID` | `thwAddInTemplateCmd` | Id des Befehls | Beliebiger Text. Er muss unter **allen** in Fusion installierten Add-Ins eindeutig sein. Bei einer Überschneidung wird stillschweigend die Schaltfläche des anderen Add-Ins übernommen. Das Skript setzt ihn auf `<prefix><name>Cmd` |
| `WORKSPACE_ID` | `FusionSolidEnvironment` | Arbeitsbereich, der die Schaltfläche bekommt. Dieser ist der Arbeitsbereich Konstruktion | Eine id eines Fusion-Arbeitsbereichs |
| `PANEL_IDS` | `('SketchCreatePanel', 'SolidCreatePanel')` | Panels der Werkzeugleiste, in dieser Reihenfolge versucht. Das erste, das existiert, bekommt die Schaltfläche | Eine Liste von Panel-ids, das liebste zuerst |
| `IN_LINE` | `tplLine` | Id des Auswahlfelds | Beliebiger Text, eindeutig innerhalb dieses Befehls |
| `IN_LENGTH` | `tplLength` | Id des Längenfelds | wie oben |
| `IN_FLIP` | `tplFlip` | Id des Kontrollkästchens | wie oben |
| `RESOURCE_FOLDER` | `resources/<name>` im Add-In-Ordner | Ordner mit den Symbolen. Existiert er nicht, bekommt die Schaltfläche kein Symbol | Ein Ordner mit `16x16.png`, `32x32.png`, `64x64.png` |
| `LANG_DIR` | `lang` im Add-In-Ordner | Ordner mit den Sprachdateien | Ein Ordner mit `<code>.xml`-Dateien |
| `_last` | `{IN_LENGTH: 1.0, IN_FLIP: False}` | Startwerte und die Werte, die vom letzten Aufruf gemerkt sind | Ein Eintrag je gemerktem Feld |
| `_CORE_MODULE` | `addin_core` | Name des Kernmoduls. Er steht über `CONFIGURE` | Vom Skript auf `<name in Kleinbuchstaben>_core` gesetzt. So lassen |

### Panel-ids, die im Code genannt sind

| Id | Registerkarte |
| --- | --- |
| `SketchCreatePanel`, `SketchModifyPanel` | SKETCH |
| `SolidCreatePanel`, `SolidModifyPanel` | SOLID |
| `InspectPanel`, `ToolsPanel` | UTILITIES |

Jedes Panel wird zuerst im Arbeitsbereich gesucht, dann unter allen Panels von Fusion.
Die Schaltfläche wird als „promoted“ hinzugefügt. Das heißt, sie wird direkt auf dem Panel angezeigt.

### Gemerkte Werte

- `_last` enthält die Werte für den nächsten Aufruf des Befehls.
- Sie liegen nur im Arbeitsspeicher. Sie sind weg, wenn Fusion geschlossen oder das Add-In neu gestartet wird.
- Längen sind in **cm**, der internen Einheit von Fusion, egal was das Feld anzeigt. `1.0` in einem Feld, das in `mm` anzeigt, ergibt 10 mm.
- Ein Wert wird nur gemerkt, wenn `remember()` ihn kopiert und `build_inputs()` ihn als Startwert benutzt.

## Manifest

Das Manifest ist eine JSON-Datei. Fusion liest sie.

| Feld | Wert in der Vorlage | Bedeutung | Vom Skript gesetzt? |
| --- | --- | --- | --- |
| `autodeskProduct` | `Fusion360` | Das Produkt. Die Offline-Prüfung verlangt diesen Wert | nein |
| `type` | `addin` | Die Art der Erweiterung. Die Offline-Prüfung verlangt diesen Wert | nein |
| `id` | `00000000-0000-0000-0000-000000000000` | GUID des Add-Ins. Die Nullen sind ein Platzhalter | ja, eine neue zufällige GUID |
| `author` | `Your Name` | Autor | ja, aus `--author` |
| `description` | je ein Text für `""` (Vorgabe), `de-DE`, `es-ES`, `fr-FR`, `it-IT` | Beschreibung des Add-Ins | **nein – sie beschreibt noch die Vorlage. Bearbeiten** |
| `version` | `1.0.0.0` | Version. Das Add-In liest sie und zeigt sie in Klammern hinter dem Befehlsnamen | **nein – sie behält die Nummer der Vorlage. Die eigene setzen** |
| `runOnStartup` | `true` | Das Add-In zusammen mit Fusion starten | nein |
| `supportedOS` | `windows\|mac` | Systeme, für die das Add-In gedacht ist | nein |
| `editEnabled` | `true` | Ein Fusion-Feld. Der Code der Vorlage benutzt es nicht | nein |

Die Version steht nur an einer Stelle, im Manifest. Der Code liest sie von dort, deshalb kann der Dialogtitel nicht vom Manifest abweichen.
Lässt sich das Manifest nicht lesen oder hat es keine Version, wird der Name ohne Klammern angezeigt.

## Sprachdateien

### Format

Eine Datei je Sprache: `lang/<code>.xml`.

```xml
<strings language="en">
  <string key="in.length">Length</string>
</strings>
```

- `en.xml` ist die Referenz. Jeder Schlüssel ist dort vorhanden.
- Das Attribut `language` muss dem Code im Dateinamen entsprechen.
- Platzhalter `{0}`, `{1}`, … werden vom Add-In gefüllt. Sie müssen in jeder Übersetzung erhalten bleiben.
- Andere Dateien dürfen Schlüssel weglassen. Fehlende Schlüssel werden englisch angezeigt.

### Schlüssel in der Vorlage

| Schlüssel | Deutscher Text |
| --- | --- |
| `cmd.name` | Add-In-Vorlage |
| `cmd.tooltip` | Ausgangspunkt für ein Fusion-360-Add-In. / Zeichnet einen Strich auf der Mitte der gewählten Linie. (zwei Zeilen) |
| `in.line` | Linie |
| `in.line.prompt` | Skizzenlinie wählen |
| `in.length` | Länge |
| `in.flip` | Richtung umkehren |
| `err.no_selection` | Bitte genau eine Skizzenlinie wählen. |
| `err.length_positive` | Die Länge muss größer als 0 sein. |
| `err.zero_length` | Die gewählte Linie hat keine Länge. |
| `err.too_long` | Die Länge überschreitet die gewählte Linie ({0} mm). |
| `msg.panel_missing` | Kein passendes Toolbar-Panel gefunden. |
| `msg.exec_failed` | Fehler beim Erzeugen der Geometrie: {0} |
| `msg.dialog_failed` | Fehler beim Aufbau des Dialogs: {0} |
| `msg.run_failed` | Start fehlgeschlagen: {0} |
| `msg.stop_failed` | Stopp fehlgeschlagen: {0} |

`cmd.name` ist auch der Titel jedes Meldungsfensters.

### Wie die Sprache gewählt wird

Die Sprache wird einmal gewählt, beim Start des Add-Ins. Im Add-In gibt es keinen Umschalter.

1. Die Sprache, die in den Voreinstellungen von Fusion eingestellt ist (die Benutzersprache).
2. Ergibt das keine unterstützte Sprache: die Umgebungsvariablen `LANG`, `LANGUAGE`, `LC_ALL`, in dieser Reihenfolge.
3. Ergibt das nichts: die Sprache des Betriebssystems.
4. Sonst Englisch.

Unterstützte Codes: `de`, `en`, `es`, `fr`, `it`.

Nach einem Wechsel der Sprache in Fusion das Add-In stoppen und neu starten.

### Eine Sprache hinzufügen

1. `lang/en.xml` kopieren und die Kopie nach dem Code aus zwei Buchstaben benennen, zum Beispiel `ja.xml`.
2. Im ersten Tag `language="ja"` setzen.
3. Die Werte übersetzen. Die Schlüssel und die Platzhalter beibehalten.
4. Im Kernmodul (`<name>_core.py`) den Code zu `SUPPORTED_LANGUAGES` hinzufügen.
5. Im Kernmodul die Fusion-Sprache zu `FUSION_LANGUAGE_MAP` hinzufügen, zum Beispiel `'JapaneseLanguage': 'ja'`.
6. Die Offline-Prüfung ausführen, siehe [development.md](development.md).
