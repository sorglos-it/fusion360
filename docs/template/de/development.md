# Entwicklung

## Ordner

| Pfad | Inhalt |
| --- | --- |
| `apps/desktop-template/AddInTemplate/` | Das Vorlagen-Add-In, wie Fusion es braucht |
| `apps/desktop-template/AddInTemplate/AddInTemplate.py` | Startdatei |
| `apps/desktop-template/AddInTemplate/addin_core.py` | Kernmodul |
| `apps/desktop-template/AddInTemplate/AddInTemplate.manifest` | Manifest |
| `apps/desktop-template/AddInTemplate/lang/` | `de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` |
| `apps/desktop-template/AddInTemplate/resources/AddInTemplate/` | Symbole `16x16.png`, `32x32.png`, `64x64.png` |
| `apps/desktop-template/VERSION` | Versionsnummer dieses Teils |
| `apps/desktop-template/tests/test_addin.py` | Offline-Prüfung |
| `tools/template/new_addin.py` | Gerüst-Skript, siehe [installation.md](installation.md) |
| `tools/template/make_icon.py` | Symbol-Werkzeug |
| `tools/template/test_addin.py` | Leitet an die Offline-Prüfung weiter (alter Pfad) |
| `tools/set_version.py` | Setzt Versionsnummern, für alle Add-Ins des Repositorys |
| `tools/release.py` | Packt ein Add-In in ein ZIP, für alle Add-Ins des Repositorys |
| `docs/template/` | README, CHANGELOG, LICENSE und diese Dokumentation |
| `dist/` | Gepackte ZIP-Dateien. Nicht in Git |

Es gibt keinen Bauschritt. Das Add-In läuft, wie es ist. Alle Werkzeuge nutzen nur die Python-Standardbibliothek.

## Offline-Prüfung

Die Prüfung testet ein Add-In, ohne Fusion zu starten. Der Kommentar im Code nennt sie die einzige Rückmeldeschleife, die keinen Neustart braucht.

```bash
python apps/desktop-template/tests/test_addin.py                    # the template itself
python apps/desktop-template/tests/test_addin.py --path ../MyAddIn  # an add-in next to the repository
```

| Schalter | Vorgabe | Wirkung |
| --- | --- | --- |
| `--addin NAME` | `AddInTemplate` | Ordnername innerhalb von `apps/desktop-template` dieses Repositorys |
| `--path DIR` | – | Voller Pfad zu einem Add-In-Ordner. Hat Vorrang vor `--addin` |

Bei einem Add-In, das mit `--install` angelegt wurde, seinen Ordner im Add-In-Ordner von Fusion an `--path` übergeben.

Der alte Befehl `python tools/template/test_addin.py` funktioniert weiterhin. Er leitet an die Prüfung weiter, mit denselben Argumenten, derselben Ausgabe und demselben Rückgabecode.

### Wie sie arbeitet

Sie setzt leere Attrappen für die Module `adsk`, `adsk.core` und `adsk.fusion` ein und importiert dann das Add-In.
Nur die Basisklassen der Handler sind echte (leere) Klassen. Die Prüfung belegt also, dass die Datei sich importieren lässt und dass die Texte in Ordnung sind. Sie führt **keinen** Fusion-Aufruf aus: keinen Dialog, keine Geometrie, kein `run()`.

### Was sie prüft

| Abschnitt | Prüfungen |
| --- | --- |
| 1) Layout | Der Ordner existiert. `<name>.py` und `<name>.manifest` passen zum Ordnernamen. `lang/` existiert |
| 2) Manifest | Gültiges JSON. `type` ist `addin`. `autodeskProduct` ist `Fusion360`. `id` sieht wie eine GUID aus. Warnungen: Platzhalter-GUID, Autor `Your Name` |
| 3) Import | Das Add-In lässt sich importieren. `run` und `stop` sind vorhanden. `CMD_ID` ist gesetzt. `_CORE_MODULE` hat eine passende Datei. Warnungen: `CMD_ID` noch der Wert der Vorlage, Kernmodul nicht umbenannt |
| 4) Language files | `SUPPORTED_LANGUAGES` ist verfügbar. `en.xml` existiert und hat Schlüssel. Für jede unterstützte Sprache: Die Datei existiert, gibt die richtige `language` an, hat jeden Schlüssel, hat keinen unbekannten Schlüssel, behält jeden Platzhalter, hat keinen leeren Text |
| 5) Text catalogue | Jede Sprache lässt sich laden und liefert einen `cmd.name`. Eine unbekannte Sprache fällt auf Englisch zurück. Ein fehlender Schlüssel liefert den Schlüssel. Warnung: Im Tooltip steht noch `TODO` |
| 6) Icons | `resources/<name>/` existiert. Die drei PNG-Dateien existieren und beginnen mit der PNG-Signatur |

### Ergebnis

- Zeilen beginnen mit `ok`, `FAIL` oder `warn`.
- Bei mindestens einem `FAIL` endet das Skript mit Rückgabecode 1 und gibt die Anzahl der Fehler aus.
- Warnungen ändern den Rückgabecode nicht.
- Ohne Fehler gibt es `all checks passed` aus.

Lauf für diese Dokumentation auf der Vorlage, Version 1.0.0.0: `3 warning(s)`, `all checks passed`. Die drei Warnungen (Platzhalter-GUID, Autor, Befehls-id) sind für die Vorlage normal.

## Symbol-Werkzeug

Fusion will drei PNG-Dateien mit Transparenz: 16x16, 32x32 und 64x64 Pixel, in dem Ordner, der an die Definition der Schaltfläche übergeben wird.

```bash
python tools/template/make_icon.py                            # the template's placeholder
python tools/template/make_icon.py --root .. --addin MyAddIn  # an add-in next to the repository
```

| Schalter | Vorgabe | Wirkung |
| --- | --- | --- |
| `--addin NAME` | `AddInTemplate` | Name des Add-In-Ordners |
| `--root DIR` | `apps/desktop-template` dieses Repositorys | Ordner, in dem das Add-In liegt |

Die Dateien werden nach `<root>/<addin>/resources/<addin>/` geschrieben. Der Ordner wird bei Bedarf angelegt. Vorhandene Symbole werden überschrieben.

Um ein eigenes Symbol zu zeichnen, das Skript bearbeiten:

| Name | Bedeutung |
| --- | --- |
| `SHAPES` | Liste von `(colour, polygon)`. Punkte gehen von 0 bis 1, wobei y nach **oben** zeigt. Wo sich Formen überlappen, bleibt die zuerst genannte oben |
| `DARK`, `ACCENT` | Die zwei Farben als RGB-Werte |
| `SS` | Abtastungen je Pixelkante für glatte Kanten. 4 ergibt saubere Kanten bis hinunter zu 16 px |

Der Platzhalter zeigt vier Eckwinkel und eine Diagonale. Er sieht mit Absicht wie ein Platzhalter aus. Ihn ersetzen, bevor das eigene Add-In weitergegeben wird.

## Versionsnummern

Versionen haben vier Teile: `v.x.y.z` (Version, Release, Feature, Build). Aktuell: `1.0.0.0`.

Die Nummer steht an zwei Stellen:

- `apps/desktop-template/VERSION`
- im Feld `version` des Manifests – dieses lesen Fusion und der Dialogtitel

Sie nie von Hand bearbeiten. Das Werkzeug benutzen, es schreibt beide:

```bash
python tools/set_version.py template 1.0.0.1   # this part
python tools/set_version.py all 1.0.0.0        # every add-in of the repository
python tools/set_version.py --check            # report differences
```

- `template` ist der Ordnername `apps/desktop-template` ohne `desktop-`.
- `--check` gibt je Add-In eine Zeile aus, die mit `ok` oder `DIFFERENT OR NOT v.x.y.z` endet, und gibt Rückgabecode 1 zurück, wenn eine Zeile falsch ist.
- Das Werkzeug arbeitet nur auf den Add-Ins dieses Repositorys. In einem eigenen Add-In außerhalb des Repositorys das Feld `version` seines Manifests direkt ändern – das ist dort die einzige Stelle.

## Packen

```bash
python tools/release.py template
python tools/release.py all
```

- Schreibt `dist/AddInTemplate-<version>.zip`.
- Das ZIP enthält den Ordner `AddInTemplate`, wie Fusion ihn haben will. Es in den Add-In-Ordner von Fusion entpacken.
- Weggelassen: `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Komprimierung: Deflate auf höchster Stufe, damit jeder Entpacker es lesen kann.
- Es weigert sich zu packen, wenn `VERSION` und das Manifest sich unterscheiden oder die Nummer keine vier Teile hat.
- Nach dem Packen prüft es das ZIP und gibt die Anzahl der Dateien und die Größe aus.
- Die Werkzeuge (`tools/`) sind nicht im ZIP. Es gibt sie nur im Repository.

Von Version 1.0.0.0 wurde kein ZIP veröffentlicht. Die Vorlage wird aus dem Repository benutzt.

## Entscheidungen und ihre Gründe

| Entscheidung | Grund, der im Code steht |
| --- | --- |
| Startdatei und Kernmodul sind getrennt | Der Kern enthält, was jedes Add-In braucht und was man leicht falsch macht. Der eigene Code bleibt zwischen zwei Markierungen |
| Das Kernmodul wird je Add-In umbenannt | Zwei Add-Ins aus dieser Vorlage dürfen sich in `sys.modules` nicht gegenseitig das Kernmodul überschreiben |
| Das Kernmodul wird vor dem Import aus `sys.modules` entfernt | Fusion hält Module im Zwischenspeicher. So übernimmt „stoppen, starten“ die Änderungen |
| Alle Handler laufen über `HandlerRegistry` | Fusion hält Handler schwach. Solche ohne Verweis werden aufgeräumt, und das Ereignis feuert stillschweigend nicht mehr |
| `PANEL_IDS` ist eine Liste, mit einer globalen Suche als zweitem Versuch | Panel-ids wandern zwischen Fusion-Versionen |
| Eine veraltete Befehlsdefinition wird beim Start gelöscht | Sie würde ihre alte Beschriftung und ihren alten Handler behalten |
| `read_inputs()` ist die einzige Stelle, die den Dialog liest | Ausführung, Vorschau und Prüfung sehen genau dieselben Zahlen |
| `validate()` läuft vor dem Zeichnen und noch einmal für die OK-Schaltfläche | Eine unmögliche Eingabe sperrt OK, statt mittendrin fehlzuschlagen |
| Die Vorschau schluckt Fehler | Sie feuert bei jedem Tastendruck, auch bei halb getippten Werten |
| Die Vorschau setzt `isValidResult` auf `False` | Fusion führt dann für das echte Ergebnis execute aus |
| Fehler tragen einen Schlüssel, nicht nur einen Text | Der Grund ist bekannt, ohne Text in irgendeiner Sprache zu zerlegen |
| `report()` ist nur für unerwartete Fehler | Was der Benutzer beheben kann, soll ein `AddInError` sein, damit OK gesperrt wird, statt dass ein Dialog aufgeht |
| Englisch ist der Rückfall für jeden Text | Eine halbfertige Übersetzung zeigt Englisch statt roher Schlüssel |
| Die Sprachwerte von Fusion werden über den Namen nachgeschlagen | Ein Wert, den diese Fusion-Version nicht kennt, kann das Add-In nicht zum Absturz bringen |
| Die Spracherkennung löst nie einen Fehler aus | Auch ein Fusion-Build mit einem unerwarteten Wert startet das Add-In |
| Die Version wird aus dem Manifest gelesen | Der Dialog kann nicht vom Manifest abweichen. Eine Stelle, um sie zu erhöhen |
| Die Version ist Teil des Befehlsnamens | Fusion benutzt diesen Namen als Dialogtitel. Das ist die einzige Stelle, an der eine Version sichtbar ist, solange der Dialog offen ist. Sie steht auch auf der Schaltfläche – es gibt nur den einen Namen |
| `isComputeDeferred` wird in `finally` zurückgesetzt | Nach einem Fehler würde sich die Skizze sonst nicht mehr aktualisieren |
| Die Auswahl wird gelesen, bevor die Eingabefelder existieren | „Eine Linie anklicken, dann die Schaltfläche drücken“ funktioniert |
| Das Platzhalter-Symbol sieht wie ein Platzhalter aus | Ein Symbol, das nicht ersetzt wurde, fällt leicht auf |
| Das Skript schreibt Dateien mit `\n`-Zeilenenden und UTF-8 | Im Code nicht erklärt |
| Schlüssel, Bezeichner und Kommentare sind englisch | Im Code nicht erklärt; das vorhandene README sagt, ein Übersetzer muss dann nie eine `.py`-Datei öffnen |

## Lizenz

MIT. Autor: Sorglos Thomas Weirich. Siehe [LICENSE](../LICENSE).
