# Entwicklung

SketchGrid ist eines von mehreren Add-ins im Repository <https://github.com/sorglos-it/fusion360>. Alle Pfade unten beginnen am Wurzelordner des Repositorys.

## Ordner

| Pfad | Inhalt |
| --- | --- |
| `apps/desktop-sketch-grid/SketchGrid/` | Das Add-in genau so, wie Fusion es braucht: `SketchGrid.py`, `sketchgrid_core.py`, `SketchGrid.manifest`, `lang/`, `resources/SketchGrid/` |
| `apps/desktop-sketch-grid/VERSION` | Die Versionsnummer, eine Zeile |
| `apps/desktop-sketch-grid/tests/test_sketchgrid.py` | Die Tests |
| `tools/sketch-grid/make_icon.py` | Zeichnet das Symbol der Schaltfläche (16, 32 und 64 Pixel) |
| `tools/sketch-grid/test_sketchgrid.py` | Leitet nur zu den Tests oben weiter, damit der alte Befehl weiter geht |
| `tools/set_version.py` | Setzt die Versionsnummer (von allen Add-ins gemeinsam genutzt) |
| `tools/release.py` | Packt das Release-ZIP (von allen Add-ins gemeinsam genutzt) |
| `docs/sketch-grid/` | README, CHANGELOG, LICENSE und diese Dokumentation |
| `dist/` | Wird von `tools/release.py` angelegt; nicht in Git |

Ordner, `.py`-Datei und `.manifest`-Datei müssen gemeinsam den Namen `SketchGrid` tragen. Fusion verlangt das.

Alle Skripte brauchen nur ein normales Python 3 mit seiner Standardbibliothek. Es gibt nichts zu bauen; das Add-in läuft so, wie es ist.

## Die Tests ausführen

```
python apps/desktop-sketch-grid/tests/test_sketchgrid.py
python apps/desktop-template/tests/test_addin.py --path apps/desktop-sketch-grid/SketchGrid
```

Der erste Befehl läuft ohne Fusion. Die Testdatei setzt leere Platzhalter für die `adsk`-Module von Fusion ein und importiert dann `SketchGrid.py`. Sie gibt je Prüfung eine Zeile aus (`ok` oder `FAIL`) und endet mit `all tests passed` und Exit-Code 0 oder mit der Zahl der Fehler und Exit-Code 1.

Was sie prüft:

| Abschnitt | Thema |
| --- | --- |
| 1 | Das Standardbeispiel: 10 × 5 mm, Abstand 2 mm, 8 Spalten, 4 Zeilen ergibt 94 × 26 mm und 32 Zellen |
| 2, 2b | Jeder Eintrag für den Bezugspunkt hat die Faktoren, die sein Name verspricht (abgeleitet aus dem Namen des Schlüssels, zum Beispiel `bottom_left`), und der Punkt landet dort, wo der Eintrag es sagt |
| 3 | Lagen der Zellen |
| 4 | Die Betriebsart „Fläche füllen“ zählt nur, was ganz hineinpasst |
| 5 | Jede Ablehnung meldet den richtigen Meldungsschlüssel |
| 6 | Sprachdateien: Alle fünf sind vollständig und erhalten ihre Platzhalter |
| 7 | Versatz vom gewählten Punkt |
| 8 | Der Abstand bleibt bei jeder Form der Abstand: gemessenes Rechteck um das Vieleck, Strecken, wirkliche Größe in der Betriebsart Füllen |
| 9 | Ecken des Rechtecks: Grenzen und der Umriss aus Linien und Bögen |
| 10 | Jeder Eintrag einer Auswahlliste hat einen Text |
| 11 | Textkatalog: Laden jeder Sprache, Rückfall auf Englisch, Meldungen folgen der Sprache |

Der zweite Befehl ist die Strukturprüfung aus dem Vorlagen-Add-in im selben Repository. Sie prüft Manifest, Kennung, Befehlskennung und Symbole.

Als Vorgabe benutzen die Tests und das Symbol-Skript `apps/desktop-sketch-grid/SketchGrid`. Die Umgebungsvariable `SKETCHGRID_ADDIN_DIR` setzen, um eine andere Kopie zu prüfen, zum Beispiel eine installierte.

Was die Tests nicht abdecken: alles, was Fusion braucht. Das sind der Dialog, die Auswahl, die Vorschau und die eigentlichen Zeichenaufrufe. Diese Teile lassen sich nur in Fusion ausprobieren.

## Eine Änderung in Fusion ausprobieren

1. `apps/desktop-sketch-grid/SketchGrid` in den Add-ins-Ordner von Fusion kopieren (siehe [installation.md](installation.md)).
2. In Fusion das Add-in stoppen und wieder starten.

`SketchGrid.py` entfernt `sketchgrid_core` aus dem Modul-Cache von Python, bevor es das Modul importiert. Grund aus dem Kommentar im Code: Fusion hält importierte Module im Cache, ein geänderter Helfer würde also weiter seine alte Fassung liefern, bis Fusion neu startet.

## Versionsnummern

Vier Teile: `v.x.y.z` (Version, Release, Feature, Build), zum Beispiel `1.1.0.0`.

Die Nummer steht an zwei Stellen:

- `apps/desktop-sketch-grid/VERSION`
- der Eintrag `"version"` in `SketchGrid.manifest` (diesen lesen Fusion und der Name der Schaltfläche)

Sie nie von Hand ändern. Das Skript benutzen, es schreibt beide:

```
python tools/set_version.py sketch-grid 1.1.0.1
python tools/set_version.py --check
```

- Der erste Befehl setzt die Version. Er lehnt alles ab, was nicht vier durch Punkte getrennte Zahlen sind.
- `--check` listet jedes Add-in mit beiden Nummern auf und sagt `ok` oder `DIFFERENT OR NOT v.x.y.z`. Exit-Code 1, wenn ein Add-in falsch ist.
- `all` statt `sketch-grid` setzt dieselbe Nummer für jedes Add-in des Repositorys.

Für jede neue Nummer einen Eintrag in `docs/sketch-grid/CHANGELOG.md` ergänzen.

## Ein Release packen

```
python tools/release.py sketch-grid
```

- Schreibt `dist/SketchGrid-<version>.zip`.
- Das ZIP enthält den Ordner `SketchGrid` als oberste Ebene, fertig zum Entpacken in den Add-ins-Ordner von Fusion.
- Weggelassen: `__pycache__`-Ordner und Dateien mit der Endung `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Kompression: Deflate auf der höchsten Stufe, „damit jedes Entpackprogramm es lesen kann“ (Kommentar im Skript).
- Das Skript packt nicht, wenn `VERSION` und das Manifest voneinander abweichen oder die Nummer nicht vier Teile hat.
- Nach dem Schreiben liest es das ZIP wieder ein und bricht ab, wenn eine Datei darin beschädigt ist.
- `all` statt `sketch-grid` packt jedes Add-in.

Das ZIP wird dann an ein Release unter <https://github.com/sorglos-it/fusion360/releases> angehängt. Das Skript lädt nichts hoch.

## Das Symbol neu zeichnen

```
python tools/sketch-grid/make_icon.py
```

Schreibt `16x16.png`, `32x32.png` und `64x64.png` nach `resources/SketchGrid/`. Das Bild ist ein Raster aus 3 × 3 Zellen mit einem Kreuz in der Mitte für den gewählten Punkt. Das Skript schreibt die PNG-Dateien selbst, ohne Bildbibliothek.

## Eine Sprache hinzufügen

1. `lang/en.xml` nach `lang/<code>.xml` kopieren (Code aus zwei Buchstaben) und die Texte übersetzen. Die Schlüssel und die Platzhalter `{0}`, `{1}` erhalten.
2. In `sketchgrid_core.py` den Code in `SUPPORTED_LANGUAGES` und den passenden Sprachnamen von Fusion in `FUSION_LANGUAGE_MAP` eintragen.
3. Die Tests ausführen. Sie prüfen jede Sprache in `SUPPORTED_LANGUAGES`.

## Entscheidungen und ihre Gründe

Aus den Kommentaren im Code übernommen.

| Entscheidung | Genannter Grund |
| --- | --- |
| Die Rasterberechnung (`grid_layout`, `cell_centres`, `corner_outline`) benutzt keine Aufrufe von Fusion. | Das ist der Teil, bei dem sich das Testen lohnt, und so können die Tests laufen, ohne Fusion zu starten. |
| Die Wahl in Auswahllisten wird als Stelle in der Liste gespeichert, nicht als Text. | Der gespeicherte Wert verrutscht nicht, wenn die Sprache der Oberfläche wechselt. |
| Höchstens 2000 Formen (`MAX_SHAPES`). | Eine aus dem Ruder gelaufene Anzahl in der Betriebsart Füllen legt Fusion minutenlang lahm. Stattdessen ablehnen. |
| Ein Wert für Radius / Fase über der Hälfte der kürzeren Kante wird abgelehnt, nicht verkleinert. | Bei genau der Hälfte treffen sich die beiden Schnitte an einer Kante; darüber würden sie aneinander vorbeilaufen. Nur Rundungsrauschen wird aufgefangen. |
| Ecken nehmen an der Aufteilung nicht teil. | Die Hüllkontur ist weiterhin Länge × Tiefe, Teilung, Anzahl und Abstand bleiben also, wie sie waren. |
| Ein regelmäßiges Vieleck meldet seine eigene gemessene Größe, und die Teilung folgt ihr. | Es kann eine Zelle mit anderen Proportionen nicht füllen; sonst ist der verlangte Abstand nicht der Abstand, der herauskommt. |
| Das Rechteck um das Vieleck wird gemessen, nicht angenommen. | Ein Vieleck hat nur bei passenden Seitenzahlen an jedem äußersten Rand eine Ecke; ein Fünfeck sitzt tief in seinem eigenen Rechteck. |
| Ein ganz verrundetes Quadrat wird als Kreis gezeichnet. | Ein Kreis ist keine Kette aus Stücken. |
| Bei einer Ellipse wird der Punkt der Hauptachse auf die längere Achse gelegt. | Sonst weist Fusion die Ellipse zurück. |
| `isComputeDeferred` wird beim Zeichnen gesetzt und in einem `finally`-Block zurückgesetzt. | Es hält den Löser ruhig, bis jede Form gezeichnet ist; bei ein paar hundert Zellen ist das der Unterschied zwischen sofort und unbenutzbar. |
| Der Vorschau-Handler schluckt jeden Fehler. | Er läuft bei jedem Tastendruck, auch bei halb getippten Werten. Das Melden ist Sache der Eingabeprüfung. |
| Die Ereignis-Handler werden angemeldet, bevor der vorher gewählte Punkt übernommen wird, und das Übernehmen darf still scheitern. | Was danach auch scheitert, der Dialog muss weiter arbeiten; der Punkt wird dann im Dialog gewählt. |
| Alle Ereignis-Handler werden in einer Registratur gehalten (`HandlerRegistry`). | Fusion hält nur einen schwachen Verweis auf einen Handler. Ohne einen Verweis auf der Python-Seite hört das Ereignis still auf auszulösen. |
| Mehrere Panel-Kennungen werden der Reihe nach probiert. | Panel-Kennungen wandern zwischen Fusion-Versionen. |
| Die Sprachwerte von Fusion werden über den Namen nachgeschlagen, mit einem Rückfall. | Ein Wert, den diese Fusion-Version nicht kennt, kann das Add-in nicht lahmlegen; es fällt auf Englisch zurück, statt zu scheitern. |
| Ein Schlüssel, der in einer Übersetzung fehlt, wird aus dem Englischen bedient. | Eine halb fertige Übersetzung fällt auf Englisch zurück, statt rohe Schlüssel zu zeigen. |
| Erwartete Probleme werden als `AddInError` mit einem Meldungsschlüssel ausgelöst. | Der Schlüssel ist von der Sprache unabhängig; was sich vom Benutzer beheben lässt, soll OK sperren, statt ein Fenster zu öffnen. |
| Die Version wird aus dem Manifest gelesen, nicht in den Code geschrieben. | Der Dialog kann nicht vom Manifest abweichen, und es gibt nur eine Stelle zum Ändern. |
| Die Version ist Teil des Befehlsnamens. | Fusion nimmt den Befehlsnamen als Titel des Dialogs, dort ist die Version also sichtbar; es gibt nur den einen Namen. |
| Die letzten Werte stehen im Arbeitsspeicher in Zentimetern. | Zentimeter sind die interne Einheit von Fusion, gleich welche Einheit angezeigt wird. |

## Offene Punkte

- Version 1.1.0.0 (der vorher gewählte Punkt kann nicht übernommen werden) ist nur offline geprüft, nicht in Fusion.
- Langlöcher und verrundete oder gefaste Rechtecke werden als getrennte Kurven aus Koordinaten gezeichnet, ohne gemeinsame Endpunkte. Ob sie beim Ziehen verbunden bleiben, muss in Fusion geprüft werden.
- Die Grenze von 2000 zählt Formen, nicht Kurven. Ob sie Kurven zählen muss, muss in Fusion geprüft werden.

## Lizenz

MIT, siehe [LICENSE](../LICENSE). Autor: Sorglos Thomas Weirich.
