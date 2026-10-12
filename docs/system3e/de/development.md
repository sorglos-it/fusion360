# Entwicklung

Zurück zur [Übersicht](index.md).

Alle Befehle werden im Hauptordner des Repositorys <https://github.com/sorglos-it/fusion360> ausgeführt.

## Ordner

| Pfad | Inhalt |
| --- | --- |
| `apps/desktop-system3e/System3E/` | Das Add-In, wie Fusion es lädt (dieser Ordner kommt in das Release-ZIP) |
| `apps/desktop-system3e/System3E/System3E.py` | Befehl, Dialog, Setzen, Punkte |
| `apps/desktop-system3e/System3E/system3e_core.py` | Gemeinsamer Unterbau: Textkatalog, Spracherkennung, Panel-Suche, Handler-Register, Fehlertyp, Version |
| `apps/desktop-system3e/System3E/System3E.manifest` | Fusion-Manifest: id, Autor, Beschreibungen, Version, `runOnStartup`, `supportedOS` |
| `apps/desktop-system3e/System3E/lang/` | `de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml`; `en.xml` ist die Referenz |
| `apps/desktop-system3e/System3E/blocks/` | `blocks.json` und 74 Vorschaubilder `<id>.png` (erzeugt) |
| `apps/desktop-system3e/System3E/resources/System3E/` | Symbol der Schaltfläche in 16, 32 und 64 px |
| `apps/desktop-system3e/VERSION` | Die Versionsnummer, eine Zeile |
| `apps/desktop-system3e/tests/` | `test_addin.py`, `test_blocks.py` |
| `tools/system3e/` | `build_library.py`, `mesh_to_solid.py`, `points_sheet.py`, `make_icon.py` |
| `tools/set_version.py`, `tools/release.py` | Versions- und Release-Werkzeuge für alle Add-Ins des Repositorys |
| `docs/system3e/` | README, Änderungsprotokoll, Lizenz, die Zeichnung der Punkte, diese Dokumentation |
| `assets/system3e/` | Die 3D-Datei des Herstellers. **Nicht im Repository**, liegt nur lokal. |
| `dist/` | Release-ZIPs. Nicht in Git. |

`System3E.py` hat zwei markierte Bereiche. Der Code, der zu diesem Add-In gehört, steht zwischen `CONFIGURE` und
`END OF TEMPLATE`; die Ereignis-Handler und `run`/`stop` darunter sind das Gerüst. Das Add-In wurde aus der
Add-In-Vorlage des Repositorys erzeugt.

## Tests

Beide Tests laufen ohne Fusion. Sie legen Attrappen für die `adsk`-Module in `sys.modules` ab und importieren das
Add-In.
Nur Standardbibliothek.

```bash
python apps/desktop-system3e/tests/test_addin.py
```

```bash
python apps/desktop-system3e/tests/test_blocks.py
```

Rückgabecode 1 heißt: Mindestens eine Prüfung ist fehlgeschlagen.

`test_addin.py` prüft:

| Abschnitt | Prüfungen |
| --- | --- |
| 1) Layout | Ordner, `System3E.py`, `System3E.manifest` und `lang/` sind vorhanden und passen zum Ordnernamen |
| 2) Manifest | Gültiges JSON, `type` ist `addin`, `autodeskProduct` ist `Fusion360`, die id sieht wie eine GUID aus |
| 3) Import | Das Add-In lässt sich importieren, `run` und `stop` sind vorhanden, `CMD_ID` ist gesetzt, die Datei des Kernmoduls ist vorhanden |
| 4) Language files | Jede Sprachdatei ist vorhanden, gibt ihre Sprache an, hat jeden Schlüssel von `en.xml` und keinen unbekannten Schlüssel, behält jeden Platzhalter `{0}`, hat keinen leeren Text |
| 5) Text catalogue | Jede Sprache lässt sich laden, eine unbekannte Sprache fällt auf Englisch zurück, ein fehlender Schlüssel liefert den Schlüssel |
| 6) Icons | Die drei Symboldateien sind vorhanden und sind echte PNG-Dateien |

Optionen: `--addin <name>` und `--path <folder>` richten den Test auf einen anderen Add-In-Ordner.

`test_blocks.py` prüft:

| Abschnitt | Prüfungen |
| --- | --- |
| 1) Library file | Einheit ist `mm`, 74 Bausteine, eindeutige ids und Namen, ids als Dateinamen brauchbar |
| 2) Solids | Jeder Baustein ist ein geschlossener Volumenkörper mit ebenen Flächen, die Umrisse laufen richtig herum, das Volumen ist möglich, die Ecke liegt im Ursprung, Größe und Punkte stimmen überein, die Größe passt zum Katalognamen, keine zwei Bausteine haben dieselbe Form |
| 3) Pictures | Jeder Baustein hat ein PNG, keine übrig gebliebenen Bilder |
| 4) Add-in | Das Add-In liest jeden Baustein; jede Gruppe, jeder Anker und jeder Punktname hat einen Text in allen fünf Sprachen; der vorgegebene Baustein und der vorgegebene Anker sind vorhanden |
| 5) Points for clicking | Die Stapelhöhe von `S1 WP` ist 250 und von `EU 200 W` ist 200; Lage der Anker; zwölf benannte Punkte je Baustein, alle an verschiedenen Stellen und auf dem Baustein; jeder Punkt wird auf der Oberfläche gezeigt, ohne dass zwei an einer Stelle liegen; Bausteine jeden Alters haben am Ende alle zwölf Punkte; ein Baustein abseits des Ursprungs bekommt seine Punkte auf dem Baustein; `make_body()` macht aus jedem Punkt eine Ecke, legt jede Fläche fest, benutzt jede Kante einmal in jeder Richtung und rechnet mm in cm um |

Was die Tests nicht sagen können: ob Fusion einen Körper annimmt, die Konstruktionspunkte anlegt oder das
Exemplar richtig setzt. Das zeigt sich nur in Fusion.

Stand der Prüfung in Fusion: Das Setzen von Bausteinen, die zwölf Punkte, **Setzen an** und den Versatz X/Y/Z hat
der Autor benutzt. Die Korrekturen von 1.0.0.1 sind in Fusion noch nicht bestätigt.

## Die Bausteinbibliothek neu bauen

`blocks/blocks.json` und die Bilder werden erzeugt. Nicht von Hand bearbeiten.

Quelle: die 3D-Datei des Herstellers `assets/system3e/SYSTEM 3E START.3ds`. Sie ist **nicht Teil des Repositorys**.
Ohne sie lässt sich die Bibliothek nicht neu bauen; das Skript bricht mit „Source file missing“ ab.

```bash
python tools/system3e/build_library.py
```

```bash
python tools/system3e/build_library.py --no-pictures
```

Die Bilder brauchen das Python-Paket Pillow. `--no-pictures` lässt sie aus. Das Add-In selbst braucht keines von beiden.

Was der Bau macht:

1. `mesh_to_solid.read_3ds()` liest jedes Dreiecksnetz der Datei und rechnet es in mm um.
2. `mesh_to_solid.solid_from_mesh()` verschmilzt Punkte, die näher als 0,3 mm beieinander liegen, sortiert die
   Dreiecke in Ebenen, fügt alle Dreiecke einer Ebene zu Umrissen (mit Löchern) zusammen, lässt Punkte mitten auf
   geraden Kanten weg und prüft, dass jede Kante einmal in jeder Richtung benutzt wird. Die unterste Ecke des
   Hüllquaders wird der Ursprung.
3. Die Tabelle `NAMES` gibt jeder Netznummer ihren Katalognamen. Die 3D-Datei enthält keine Namen.
4. Die vier Trennwand-Bausteine kommen als einfache Quader mit den Größen aus der Tabelle `PARTITION` hinzu.
5. `S0/2 200 P` wird nachgebaut (siehe unten).
6. `straighten()` gibt Punkten, die sich eine Koordinate teilen sollen, genau denselben Wert, auf 0,1 mm.
7. `bend()` berechnet jede Flächennormale neu aus ihrem Umriss. `stack_level()` ermittelt die Stapelhöhe.
8. `blocks.json` wird in der Reihenfolge der Tabelle `FAMILIES` geschrieben, und je Baustein wird ein Bild gezeichnet.

Der Bau bricht ab, wenn ein Baustein kein geschlossener Volumenkörper ist, wenn zwei Bausteine dieselbe id haben oder
wenn die Prüfung des Nachbaus fehlschlägt.

Um nur die Quelldatei zu untersuchen:

```bash
python tools/system3e/mesh_to_solid.py "assets/system3e/SYSTEM 3E START.3ds" --report
```

Es gibt je Netz eine Zeile aus, mit Größe, Anzahl der Punkte und Flächen, Volumen und Zustand.

### Weitere Werkzeuge

| Werkzeug | Zweck |
| --- | --- |
| `python tools/system3e/points_sheet.py "S1 WP" docs/system3e/s1-wp-punkte.svg` | Zeichnet einen Baustein mit jedem Punkt als SVG. Die Punkte stammen aus dem Add-In selbst. Die Beschriftung ist deutsch. |
| `python tools/system3e/make_icon.py` | Erzeugt die PNGs für das Symbol der Schaltfläche in 16, 32 und 64 px |

## Versionsnummern

Eine Version hat vier Teile, `v.x.y.z`: Version, Release, Feature, Build. Beispiel: `1.2.0.0`.

Die Nummer steht an zwei Stellen: in `apps/desktop-system3e/VERSION` und im Eintrag `version` des Manifests. Fusion
und der Dialogtitel lesen das Manifest. Die beiden nie von Hand bearbeiten; das Werkzeug benutzen:

```bash
python tools/set_version.py system3e 1.1.0.1
```

```bash
python tools/set_version.py --check
```

`--check` listet jedes Add-In des Repositorys auf und meldet jedes, dessen zwei Nummern sich unterscheiden oder nicht
`v.x.y.z` sind.
`all` statt `system3e` setzt jedes Add-In.

Jede Version in `docs/system3e/CHANGELOG.md` festhalten.

## Ein Release packen

```bash
python tools/release.py system3e
```

- Schreibt `dist/System3E-<version>.zip`.
- Das ZIP enthält den Ordner `System3E` genau so, wie Fusion ihn haben will.
- `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db` und `.DS_Store` werden weggelassen.
- Die Komprimierung ist Deflate auf höchster Stufe, damit jeder Entpacker es lesen kann.
- Das ZIP wird nach dem Schreiben zurückgelesen und geprüft.
- Das Werkzeug weigert sich zu packen, wenn `VERSION` und das Manifest nicht übereinstimmen.

Das ZIP wird danach an ein Release auf <https://github.com/sorglos-it/fusion360/releases> angehängt. Dieses Hochladen
gehört nicht zum Werkzeug.

Vor einem Release: beide Tests ausführen, `set_version.py --check` ausführen, das Änderungsprotokoll und diese
Dokumentation aktualisieren.

## Texte hinzufügen oder ändern

- `lang/en.xml` ist die Referenz. Jede andere Sprachdatei muss dieselben Schlüssel und dieselben Platzhalter haben.
- Ein Schlüssel, der in einer Sprache fehlt, wird zur Laufzeit aus dem Englischen bedient, aber `test_addin.py` meldet
  ihn als Fehler.
- Die Namen der Dialogfelder, Gruppen (`family.<id>`), Anker (`anchor.<id>`) und Punkte (`point.<...>`) kommen alle
  aus diesen Dateien.
- Für eine weitere Sprache: sie in `system3e_core.py` zu `SUPPORTED_LANGUAGES` und `FUSION_LANGUAGE_MAP`
  hinzufügen und die Sprachdatei ergänzen.

## Entscheidungen und ihre Gründe

Sie stammen aus den Kommentaren im Code.

| Entscheidung | Grund |
| --- | --- |
| Das Kernmodul wird vor dem Import aus `sys.modules` entfernt. | Fusion hält importierte Module im Zwischenspeicher. Ohne das würde ein bearbeiteter Helfer seine alte Fassung behalten, bis Fusion neu startet. |
| Das Kernmodul hat einen eigenen Namen, `system3e_core`. | Zwei Add-Ins aus derselben Vorlage würden sonst gegenseitig ihr Kernmodul überschreiben. |
| Die Befehls-id hat ein eigenes Präfix (`thwSystem3ECmd`). | Eine doppelt benutzte id kapert stillschweigend die Schaltfläche des anderen Add-Ins. |
| Eine veraltete Befehlsdefinition wird beim Start gelöscht. | Eine Definition, die ein früherer Lauf hinterlassen hat, würde ihre alte Beschriftung und ihren alten Handler behalten. |
| Das Panel wird anhand einer Liste von ids gesucht. | Panel-ids wandern zwischen Fusion-Versionen. |
| Alle Ereignis-Handler werden in einem Register gehalten. | Fusion hält nur eine schwache Referenz. Ein Handler, der auf der Python-Seite nicht gespeichert ist, wird aufgeräumt, und sein Ereignis feuert stillschweigend nicht mehr. |
| Die Handler werden angehängt, bevor der vorab gewählte Punkt übernommen wird. | Was auch immer danach fehlschlägt: Der Dialog muss trotzdem funktionieren. |
| Die Auswahl, die vor dem Druck auf die Schaltfläche getroffen wurde, wird gelesen, bevor die Eingabefelder existieren. | Damit „Punkt anklicken, dann die Schaltfläche“ einfach funktioniert. |
| Alle Dialogwerte werden in einer Funktion gelesen. | Ausführung, Vorschau und Prüfung sehen dann genau dieselben Werte. |
| Die Vorschau schweigt bei Fehlern. | Sie feuert bei jedem Tastendruck, auch bei halb getippten Werten. Stattdessen graut die Prüfung **OK** aus. |
| Die Vorschau setzt `isValidResult` auf false. | Fusion führt dann für das endgültige Ergebnis noch einmal die echte Ausführung aus. |
| Erwartete Fehler sind ein eigener Fehlertyp mit einem sprachunabhängigen Schlüssel. | Die Prüfung kann entscheiden, ohne Text zu zerlegen. Unerwartete Fehler werden mit ihrem Traceback angezeigt. |
| Eine fehlgeschlagene Ausführung setzt `executeFailed`. | Fusion macht dann rückgängig, was bis dahin gebaut wurde, statt eine leere Komponente zurückzulassen. |
| Derselbe Baustein noch einmal ist ein weiteres Exemplar derselben Komponente. | Sonst zeigt eine Stückliste „S1 WP“, „S1 WP (1)“, „S1 WP (2)“ als drei Teile statt ein Teil dreimal. |
| Komponenten werden über ein Attribut gefunden, nicht über den Namen. | Das Umbenennen einer Komponente schadet dann nicht. Bausteine aus der Zeit vor dem Attribut werden über den Namen gefunden. |
| Komponenten einer verknüpften Konstruktion werden übersprungen. | Sie lassen sich aus der aktuellen Konstruktion heraus nicht ändern. |
| Körper und Punkte kommen in parametrischen Konstruktionen in ein base feature. | Bei eingeschalteter Zeitachse müssen ein fertiger Körper und ein Punkt an bloßen Koordinaten in einem base feature liegen. |
| Der Körper wird benannt, solange sein base feature noch offen ist. | So steht es im Code; Version 1.0.0.1 hat das Benennen dorthin verlegt. |
| Einer vorhandenen Komponente werden nur fehlende Punkte hinzugefügt. | Komponenten aus einer älteren Version haben keine oder weniger. |
| Der Versatz wird nach der Drehung angewendet. | Er läuft entlang X, Y und Z der Konstruktion, nicht entlang des gedrehten Bausteins. |
| Die Versatz-Felder zeigen mm, der Wert ist cm. | cm ist die eigene Einheit von Fusion. |
| Die Version wird aus dem Manifest gelesen, nicht fest im Code hinterlegt. | Der Dialog kann nicht vom Manifest abweichen, und es gibt eine einzige Stelle zum Hochzählen. |
| Die Version ist Teil des Befehlsnamens. | Fusion benutzt den Befehlsnamen als Dialogtitel; das ist die einzige Stelle, an der eine Version sichtbar ist, solange der Dialog offen ist. |
| Die Mitglieder der Sprach-Aufzählung werden mit `getattr` nachgeschlagen. | Ein Wert, den diese Fusion-Version nicht kennt, kann das Add-In nicht zum Absturz bringen. Englisch ist der Rückfall. |
| Die Bibliothek speichert Punkte und ebene Flächen, keine Fusion-Dateien. | Die Datei des Herstellers enthält lose Dreiecksnetze (Dreiecke, die sich nur an einem Teil einer Kante berühren, doppelte Punkte, Splitter). Daraus kann Fusion keinen Körper machen. |
| `S0/2 200 P` wird aus `S0/2 250 P` nachgebaut, um 50 mm abgesenkt. | Sein Netz ist irreparabel beschädigt (auf einer Seite offen). Die Starter-Bausteine unterscheiden sich nur in der Höhe des glatten Körpers unter dem oberen Profil. `check_lowering()` belegt das Verfahren an einem Paar, bei dem beide Netze heil sind (`S0/2 250 W` und `S0/2 200 W`). |
| Netznummern werden über eine von Hand erstellte Tabelle Namen zugeordnet. | Die 3D-Datei enthält keine Namen. Die Tabelle entstand, indem jeder Volumenkörper mit der Zeichnung auf seinem Katalogblatt verglichen wurde. Die Länge unterscheidet die Enden: 704 oder 352 mm ist „W“, 3 mm mehr ist eine Feder („P“). |
| Trennwand-Bausteine sind einfache Quader. | Sie sind nicht in der 3D-Datei; ihre Größen stammen von den Katalogblättern. |
| Koordinaten werden auf 0,1 mm geglättet. | Die Quelle hat Gleitkomma-Rauschen (106,4 neben 106,5 mm), das Flächen leicht verbogen zurücklässt. |
| Die Stapelhöhe liegt bei Bausteinen mit Profil 50 mm unter der Oberkante. | Sie tragen die nächste Schicht auf dem Boden zwischen den Stegen; flache Bausteine tragen sie obenauf. |
| Vorschaubilder werden mit einem Tiefenpuffer gezeichnet. | Verdeckte Flächen werden je Pixel entfernt. Ein früheres Verfahren zeigte auf 16 Bildern Flächen in der falschen Reihenfolge. |
| Vorschaubilder werden aus den Volumenkörpern gezeichnet. | Sie stammen nicht aus dem Herstellerkatalog. |

## Offene Punkte

- Die Links/Rechts-Namen der Eck- und Fensterbausteine in der Tabelle `NAMES` wurden nach Augenmaß mit den
  Katalogblättern abgeglichen. Sie brauchen noch eine Prüfung durch jemanden, der das System kennt.

## Lizenz

MIT, Copyright (c) 2026 Sorglos Thomas Weirich. Siehe [LICENSE](../LICENSE). Das Add-In steht in keiner Verbindung zu
SYSTEM 3E.
