# Entwicklung

Dovetail ist eines von mehreren Add-ins im Repository <https://github.com/sorglos-it/fusion360>.
Alle Pfade unten gelten ab dem Wurzelordner des Repositorys.

## Ordner

| Pfad | Inhalt |
|---|---|
| `apps/desktop-dovetail/Dovetail/` | Das Add-in genau so, wie Fusion es haben will: `Dovetail.py`, `Dovetail.manifest`, `lang/`, `resources/` |
| `apps/desktop-dovetail/VERSION` | Die Versionsnummer, eine Zeile |
| `apps/desktop-dovetail/tests/test_geometry.py` | Die Offline-Tests |
| `tools/dovetail/make_icons.py` | Schreibt das Symbol für die Werkzeugleiste (16, 32, 64 px) nach `resources/Dovetail/` |
| `tools/dovetail/make_arrow_icons.py` | Schreibt die Symbole der Schaltflächen von **Verschieben** nach `resources/nudge_left`, `nudge_center`, `nudge_right` |
| `tools/dovetail/test_geometry.py` | Weiterleitung zur verschobenen Testdatei, damit der alte Befehl weiter geht |
| `tools/set_version.py` | Setzt die Version eines Add-ins oder aller (von allen Add-ins gemeinsam genutzt) |
| `tools/release.py` | Packt das Release-ZIP (von allen Add-ins gemeinsam genutzt) |
| `docs/dovetail/` | README, CHANGELOG, LICENSE und diese Dokumentation |
| `dist/` | Ausgabe von `tools/release.py`; nicht in Git |

Fusion verlangt, dass Ordner, `.py`-Datei und `.manifest`-Datei denselben Namen tragen. Nicht eines davon allein
umbenennen.

## Aufbau von `Dovetail.py`

| Abschnitt | Wichtigste Teile |
|---|---|
| Sprache | `Strings`, `T()`, `detect_language()`, `read_version()`, `display_name()` |
| Geometrie | `GeometryError`, `_offset_polyline()`, `_top_half()`, `_check_contour()`, `end_room()`, `max_offset()`, `tooth_directions()`, `build_contours()`, `closed_band()` |
| Zeichnen | `_to_world()`, `_draw_closed_polyline()`, `line_length()`, `create_geometry()` |
| Handler | `_read_inputs()`, `_selected_lines()`, `_check_lines()`, `_run()`, `ExecuteHandler`, `PreviewHandler`, `ValidateHandler`, `InputChangedHandler`, `CommandCreatedHandler`, `_apply_nudge()`, `_apply_mirror()` |
| Start / Stopp | `_find_panel()`, `run()`, `stop()` |

Der Geometrie-Abschnitt ist reine Mathematik. Er benutzt nichts von Fusion und läuft in jedem Python 3.

## Die Tests ausführen

Voraussetzungen: Python 3, nur die Standardbibliothek. Fusion wird nicht gebraucht; die Testdatei setzt kleine
Platzhalter für die `adsk`-Module ein, bevor sie das Add-in importiert.

```bash
python apps/desktop-dovetail/tests/test_geometry.py
```

Der alte Befehl geht weiterhin und liefert dieselbe Ausgabe und denselben Exit-Code:

```bash
python tools/dovetail/test_geometry.py
```

- Jede Prüfung gibt `ok` oder `FAIL` aus.
- Die letzte Zeile ist `all tests passed` oder die Zahl der Fehler.
- Der Exit-Code ist 1, wenn irgendetwas gescheitert ist.

Was die Abschnitte abdecken:

| Abschnitt | Inhalt |
|---|---|
| 1–4 | Die drei Formen; Punkte des Umrisses; die versetzte Kontur ist parallel und hat den richtigen Abstand |
| 5 | Ausrichtung: Die Gruppe ist auf den Mittelpunkt der Linie zentriert |
| 6 | Verschiebung, größte Verschiebung, Abstand von den Linienenden |
| 7 | Wer das Spiel bezahlt (die drei Einträge von **Die Linie ist**) |
| 8 | Gespiegelte Geometrie: beide Teile gleich; in beiden Richtungen gleich angenommen und abgelehnt |
| 9 | Fehler melden den richtigen Schlüssel; eine Verbindung je gewählter Linie; eine schlechte Linie nennt sich selbst |
| 10 | Jeder Eintrag einer Auswahlliste und jeder Tooltip-Schlüssel ist in `en.xml` vorhanden |
| 11 | Sprachdateien: vollständig, keine unbekannten Schlüssel, Platzhalter erhalten, keine leeren Texte |
| 12 | Textkatalog, Rückfall auf Englisch, Spracherkennung ohne Fusion |

Um statt der Kopie im Repository eine installierte Kopie zu prüfen, die Umgebungsvariable
`DOVETAIL_ADDIN_DIR` auf deren Ordner setzen. Die beiden Symbol-Skripte lesen dieselbe Variable.

Von der Testdatei nicht abgedeckt:

- Alles, was Fusion braucht: der Dialog, die Vorschau, das Zeichnen, das Umwandeln in eine Konstruktionslinie, das
  Zurücknehmen nach einem gescheiterten Lauf.
- Der im Changelog genannte Lauf mit 34.317 zufälligen Konturen. Das war eine einmalige Prüfung; sie ist nicht Teil
  von `test_geometry.py`.

## Symbole

```bash
python tools/dovetail/make_icons.py
python tools/dovetail/make_arrow_icons.py
```

Beide schreiben PNG-Dateien nur mit der Standardbibliothek. Sie nur ausführen, wenn sich die Symbole ändern sollen.

## Versionsnummern

Versionen haben vier Teile, `v.x.y.z`: Version, Release, Feature, Build. Beispiel: `1.1.0.0`.

Die Nummer steht an zwei Stellen:

- `apps/desktop-dovetail/VERSION`
- der Eintrag `"version"` in `Dovetail.manifest` (das lesen Fusion und der Titel des Dialogs)

Sie nie von Hand ändern. Das Skript benutzen, es schreibt beide:

```bash
python tools/set_version.py dovetail 1.1.0.1    # set one add-in
python tools/set_version.py all 1.0.0.0         # set all add-ins of the repository
python tools/set_version.py --check             # report add-ins whose two numbers differ
```

Das Skript lehnt eine Nummer ab, die nicht vier Teile hat. `--check` endet mit Exit-Code 1, wenn ein Add-in
abweicht.

## Ein Release packen

```bash
python tools/release.py dovetail
```

- Schreibt `dist/Dovetail-<version>.zip`.
- Das ZIP enthält den Ordner `Dovetail/` genau so, wie Fusion ihn haben will.
- Weggelassen: `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Kompression: Deflate auf der höchsten Stufe, damit jedes Entpackprogramm es lesen kann.
- Nach dem Schreiben wird das ZIP wieder eingelesen und geprüft.
- Das Skript packt nicht, wenn `VERSION` und das Manifest nicht übereinstimmen.

`python tools/release.py all` packt jedes Add-in des Repositorys.

Vorgeschlagene Reihenfolge für ein Release:

1. Die Tests ausführen.
2. Die Version mit `tools/set_version.py` setzen.
3. Den Eintrag in `docs/dovetail/CHANGELOG.md` ergänzen.
4. Diese Dokumentation aktualisieren.
5. Mit `tools/release.py` packen.
6. `dist/Dovetail-<version>.zip` an das Release auf GitHub anhängen.

## Eine Sprache hinzufügen

1. `lang/en.xml` kopieren und die Kopie nach dem zweibuchstabigen Sprachcode benennen.
2. Im Wurzelelement `language="<code>"` setzen und die Werte übersetzen.
3. Jeden Platzhalter (`{0}`, `{1}`, …) erhalten.
4. Den Code in `SUPPORTED_LANGUAGES` und den passenden Sprachnamen von Fusion in `FUSION_LANGUAGE_MAP` in
   `Dovetail.py` eintragen.
5. Die Tests ausführen. Sie prüfen jede Datei auf Vollständigkeit, unbekannte Schlüssel, Platzhalter und leere
   Texte.

`en.xml` ist die Referenzdatei. Jeder Schlüssel ist dort vorhanden. Ein Schlüssel, der woanders fehlt, fällt auf sie
zurück; ein Schlüssel, der überall fehlt, wird als der Schlüssel selbst gezeigt.

## Entscheidungen und ihre Gründe

Aus den Kommentaren im Code übernommen.

| Entscheidung | Grund |
|---|---|
| Texte liegen in `lang/<code>.xml`; Fehler tragen einen Schlüssel, keinen Text | Der Grund eines Fehlers bleibt von der Sprache unabhängig; Tests können Schlüssel vergleichen |
| Form und Aufteilung werden als Index in der Liste gespeichert | Der gespeicherte Wert hängt nicht von der Anzeigesprache ab |
| Die Sprachwerte von Fusion werden mit `getattr` nachgeschlagen | Ein Wert, den diese Fusion-Version nicht kennt, kann das Add-in nicht lahmlegen |
| Die Version wird aus dem Manifest gelesen | Der Dialog kann nicht vom Manifest abweichen |
| Die Version ist Teil des Befehlsnamens | Fusion nimmt den Befehlsnamen als Titel des Dialogs; dort ist eine Version also sichtbar, solange der Dialog offen ist |
| Die Verschiebung wird nicht gemerkt | Sie gehört zur gerade bearbeiteten Linie, nicht zu den Einstellungen |
| Die Originallinie wird zur Konstruktionslinie, statt gelöscht zu werden | Sie erzeugt keine Profile mehr, behält aber ihre Bemaßungen und Abhängigkeiten |
| Die Vorschau lässt die Originallinie in Ruhe | Die Auswahl kann unter dem offenen Dialog nicht ungültig werden |
| Alle Linien werden geprüft, bevor eine gezeichnet wird | Eine schlechte Linie am Ende kann keine halb gezeichnete Skizze hinterlassen |
| Ein Fehler auf einer von mehreren Linien wird mit ihrer Stelle eingepackt | Eine kurze Linie in der Mitte scheitert, während die anderen in Ordnung wären; die Meldung sagt, welche |
| Die Schaltflächen von **Verschieben** nehmen die kürzeste Linie als Grenze | Eine Verschiebung, die über eine Linie hinausläuft, taugt nichts, auch wenn die anderen sie vertragen würden |
| Beim Spiegeln werden Anzahl, Aufteilung und Verschiebung gesetzt und ausgegraut | Jedes davon stört die 180-Grad-Symmetrie; sie festzulegen ist besser, als sie an der Prüfung scheitern zu lassen |
| Spiegeln braucht eine gerade Anzahl | Ein mittlerer Zahn müsste in beide Richtungen zugleich zeigen |
| Der Mindestabstand hat 0,01 mm obendrauf | Bei genau dem Mindestabstand hat die Strecke zwischen zwei Taschen keine Länge mehr |
| Zähne halten Toleranz + 0,01 mm Abstand von den Linienenden | Die Tasche öffnet sich um bis zu die Toleranz; sonst läuft die Kontur über das Ende hinaus und muss umkehren |
| Eine Kontur wird auf Stücke ohne Länge und auf Selbstkreuzung geprüft | Der Versatz bildet an jeder Ecke für sich eine Gehrung; nichts anderes hindert also ein kurzes Stück daran, auf nichts zu schrumpfen oder umzuklappen |
| Eine Gehrungsecke, die weiter weg liegt als 12 × der Versatz, wird abgelehnt | Die Toleranzkontur würde an einer spitzen Ecke aus dem Ruder laufen |
| Ein gescheiterter Lauf setzt `executeFailed` | Fusion nimmt dann zurück, was bis dahin gezeichnet wurde |
| Das Zeichnen läuft mit `isComputeDeferred` | Die Skizze rechnet einmal neu, nicht nach jeder Linie |
| `set_version.py` schreibt VERSION und Manifest zusammen | Die Nummer wird nie von Hand an zwei Stellen geändert |
| Das ZIP benutzt Deflate auf der höchsten Stufe | Jedes Entpackprogramm kann es lesen |

## Bekannte offene Punkte

- Ist OK ausgegraut, zeigt der Dialog keinen Grund. Die Texte gibt es (`err.*`), aber nur das Meldungsfenster nach
  einem gescheiterten Lauf zeigt sie.
- Skizzenlinien werden nur mit X und Y gelesen, und das Band wird bei Z = 0 der Skizze gezeichnet.
- Die Geometrie-Änderungen von 1.1.0.0 sind nur offline geprüft, nicht in Fusion.

## Lizenz

MIT, siehe [LICENSE](../LICENSE). Autor: Sorglos Thomas Weirich.
