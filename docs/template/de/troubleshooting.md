# Fehlerbehebung

Die Texte unten sind die deutschen aus `lang/de.xml`. In einer anderen Sprache zeigt das Add-In die Übersetzung.
Jedes Meldungsfenster hat den Befehlsnamen als Titel.

## Meldungen des Beispielbefehls

Diese vier kommen aus `validate()`. Solange eine davon zutrifft, ist **OK** ausgegraut und es wird keine Vorschau angezeigt – ohne jeden Text.
Der Text selbst erscheint nur dann als Meldungsfenster, wenn der Fehler in dem Moment auftritt, in dem der Befehl ausgeführt wird.

| Meldung | Ursache | Was zu tun ist |
| --- | --- | --- |
| „Bitte genau eine Skizzenlinie wählen.“ | Das Feld **Linie** ist leer, oder das gewählte Objekt ist keine Skizzenlinie | Eine gerade Skizzenlinie wählen |
| „Die Länge muss größer als 0 sein.“ | **Länge** ist 0 oder negativ | Eine Länge über 0 eingeben |
| „Die gewählte Linie hat keine Länge.“ | Start- und Endpunkt der Linie liegen auf derselben Stelle (es werden nur X und Y verglichen) | Eine andere Linie wählen |
| „Die Länge überschreitet die gewählte Linie ({0} mm).“ | **Länge** ist größer als die gewählte Linie. `{0}` ist die Länge der Linie in mm mit zwei Nachkommastellen | Eine Länge bis zu diesem Wert eingeben oder eine längere Linie wählen |

## Meldungen des Add-Ins selbst

Die vier Meldungen mit `{0}` zeigen an der Stelle von `{0}` einen Python-Traceback. Der Traceback nennt die Datei und die Zeile des Fehlers.

| Meldung | Wann | Ursache | Was zu tun ist |
| --- | --- | --- | --- |
| „Kein passendes Toolbar-Panel gefunden.“ | beim Start | Keine der ids in `PANEL_IDS` existiert, weder im Arbeitsbereich `WORKSPACE_ID` noch irgendwo in Fusion. Das Add-In läuft, hat aber keine Schaltfläche | Panel-ids in `PANEL_IDS` eintragen, die es in der eigenen Fusion-Version gibt. Siehe [settings.md](settings.md) |
| „Fehler beim Erzeugen der Geometrie: {0}“ | nach OK | Ein unerwarteter Fehler in `read_inputs()`, `validate()`, `build_result()` oder `remember()` – ein Programmfehler, keine falsche Eingabe | Die letzten Zeilen des Tracebacks lesen und den Code korrigieren. Kann der Benutzer ihn auslösen, den Fall in `validate()` mit `fail('err.key')` abfangen |
| „Fehler beim Aufbau des Dialogs: {0}“ | beim Druck auf die Schaltfläche | Ein unerwarteter Fehler in `build_inputs()` oder beim Verbinden der Handler | Den Traceback lesen. Typisch: dieselbe Eingabe-id zweimal benutzt, oder ein falscher Einheitentext |
| „Start fehlgeschlagen: {0}“ | beim Start des Add-Ins | Ein unerwarteter Fehler in `run()` | Den Traceback lesen |
| „Stopp fehlgeschlagen: {0}“ | beim Stoppen des Add-Ins | Ein unerwarteter Fehler in `stop()` | Den Traceback lesen. Fusion neu starten, wenn die Schaltfläche in der Werkzeugleiste bleibt |

Die „typischen“ Ursachen in dieser Tabelle sind Beispiele. Sie wurden für diese Dokumentation nicht in Fusion nachgestellt.

## Meldungen des Gerüst-Skripts

| Meldung | Ursache | Was zu tun ist |
| --- | --- | --- |
| `The name must start with a letter and contain only letters and digits - it becomes a Python module name. Got: '…'` | Der Name hat ein Leerzeichen, einen Bindestrich, einen Unterstrich, ein anderes Zeichen oder beginnt mit einer Ziffer | Einen Namen wie `MyAddIn` benutzen |
| `Pick a name other than AddInTemplate.` | Der Name ist der eigene Name der Vorlage | Einen anderen Namen wählen |
| `Template folder not found: …` | `apps/desktop-template/AddInTemplate` fehlt. Das Skript wurde verschoben, oder das Repository ist unvollständig | Das Skript aus einer vollständigen Kopie des Repositorys ausführen |
| `… already exists. Pass --force to overwrite it.` | Der Zielordner existiert | Einen anderen Namen oder Ordner wählen. `--force` löscht den vorhandenen Ordner mit allem, was darin ist |
| `Use either --install or --out, not both.` | Beide Schalter wurden angegeben | Einen von beiden benutzen |

Auf einem System, das nicht macOS ist, baut `--install` den Pfad aus der Umgebungsvariablen `APPDATA`. Ist sie nicht gesetzt (zum Beispiel unter Linux), wird der Ordner relativ zum aktuellen Ordner angelegt. Dort `--out` benutzen.

## Meldungen der Versions- und Pack-Werkzeuge

| Meldung | Ursache | Was zu tun ist |
| --- | --- | --- |
| `The version needs four numbers, like 1.0.0.0 - got '…'` | Die Version hat keine vier Teile | `v.x.y.z` benutzen, zum Beispiel `1.0.0.1` |
| `No add-in "…". There are: …` | Der Name ist kein Ordner `apps/desktop-<name>` mit genau einem Manifest | Einen Namen aus der Liste benutzen. Die Vorlage heißt `template` |
| `No "version" entry in …` | Das Manifest hat kein Feld `version` | Das Feld im Manifest ergänzen |
| `DIFFERENT OR NOT v.x.y.z` (von `--check`) | `VERSION` und das Manifest unterscheiden sich, oder die Nummer hat keine vier Teile | `python tools/set_version.py template <version>` ausführen |
| `template: VERSION and manifest disagree - run tools/set_version.py first.` | Wie oben, beim Packen bemerkt | Wie oben, dann noch einmal packen |
| `template: … is damaged in the ZIP` | Die ZIP-Prüfung nach dem Packen ist fehlgeschlagen | Noch einmal packen; den Datenträger prüfen |

## Offline-Prüfung: FAIL und warn

Die Prüfung ist in [development.md](development.md) beschrieben. Eine `FAIL`-Zeile nennt, was falsch ist. `warn`-Zeilen lassen die Prüfung nicht fehlschlagen.

| Warnung | Bedeutung |
| --- | --- |
| `id is not the placeholder GUID` | Das Manifest hat als `id` noch die Nullen |
| `author has been filled in` | Der Autor ist noch `Your Name` |
| `CMD_ID is no longer the template default` | `CMD_ID` ist noch `thwAddInTemplateCmd` |
| `the core module was renamed, so it cannot clash with another add-in` | Ein anderes Add-In als die Vorlage benutzt noch `addin_core` |
| `cmd.tooltip no longer says TODO` | Der englische Tooltip enthält noch `TODO` |

Für die Vorlage selbst sind die ersten drei Warnungen normal.

## Stolperfallen

Sie stammen aus den Kommentaren im Code.

| Anzeichen | Ursache | Was zu tun ist |
| --- | --- | --- |
| Eine Änderung am Code hat keine Wirkung | Fusion hält importierte Module im Zwischenspeicher. Ein bearbeitetes Modul behält seine alte Fassung, bis Fusion neu startet | Das Add-In stoppen und neu starten. Beim Kernmodul funktioniert das, weil die Startdatei es vor dem Import aus `sys.modules` entfernt. Jedes weitere eigene Modul genauso behandeln |
| Die Schaltfläche eines anderen Add-Ins macht etwas Seltsames, oder die eigene | Zwei Add-Ins benutzen dieselbe `CMD_ID`. Die Überschneidung bleibt still | Ein eigenes Präfix und eine eindeutige id benutzen |
| Zwei Add-Ins aus der Vorlage stören einander | Beide benutzen ein Kernmodul mit demselben Namen | Das umbenannte Kernmodul `<name>_core.py` beibehalten |
| Ein Ereignis feuert nicht mehr, ohne Fehler | Fusion hält Handler nur schwach. Ein Handler, auf den Python nicht mehr verweist, wird aufgeräumt | Jeden Handler mit `_handlers.add(event, handler)` verbinden |
| Die Schaltfläche behält eine alte Beschriftung oder ein altes Verhalten | Eine Befehlsdefinition aus einem früheren Lauf ist noch da | `run()` löscht sie zuerst. Diesen Code beibehalten |
| OK ist grau und niemand weiß, warum | Prüfung und Vorschau zeigen keinen Grund | So gewollt. Die Regeln einfach halten und sie im Tooltip oder in den Beschriftungen nennen |
| Die Vorschau zeigt nichts | Die Vorschau schluckt jeden Fehler, auch echte Programmfehler | Mit gültigen Eingaben OK drücken. Execute zeigt den Fehler mit Traceback |
| Bei jedem Tastendruck erscheint eine Meldung | Die Fehleranzeige wurde in die Vorschau verlegt | Die Vorschau still lassen. Sie feuert bei jedem Tastendruck, auch bei halb getippten Werten |
| Werte sind zehnmal zu groß oder zu klein | Fusion zählt in cm, egal was das Feld anzeigt. `createByReal(1.0)`, in `mm` angezeigt, ergibt 10 mm | In cm rechnen. Nur für die Anzeige in mm mit 10 multiplizieren |
| Die Skizze aktualisiert sich nach einem Fehler nicht mehr | `isComputeDeferred` wurde auf `True` gesetzt und nie zurückgesetzt | Es in einem `finally`-Block zurücksetzen, wie `build_result()` es macht |
| `on_input_changed()` läuft endlos oder zweimal | Ein Wert, der dort zurückgeschrieben wird, löst das Ereignis erneut aus | `_updating` vor dem Schreiben auf `True` und danach auf `False` setzen. Es ist eine Modulvariable: in der Funktion `global _updating` angeben |
| Die Schaltfläche fehlt nach einer Aktualisierung von Fusion | Panel-ids wandern zwischen Fusion-Versionen | Mehrere ids in `PANEL_IDS` eintragen, die liebste zuerst |
| Die Schaltfläche hat kein Symbol | Der Ordner `resources/<name>` fehlt. Dann übergibt das Add-In keinen Symbolordner | Die Symbole anlegen, siehe [development.md](development.md) |
| Ein Text zeigt einen Schlüssel wie `in.width` | Der Schlüssel fehlt in der Sprachdatei **und** in `en.xml` | Den Schlüssel in `en.xml` ergänzen |
| Ein Text zeigt `{0}` statt eines Werts | Die Platzhalter des Texts passen nicht zu den übergebenen Werten | Den Text mit dem Aufruf `T('key', value)` vergleichen |
| Alle Texte sind englisch | Die Sprache steht nicht in `SUPPORTED_LANGUAGES`, oder ihre Datei fehlt oder ist kein gültiges XML | Die Datei und die Tabellen im Kernmodul prüfen |
| Eine Korrektur in der Vorlage erscheint nicht im eigenen Add-In | Jedes Add-In hat seine eigene Kopie des Kernmoduls | Die Korrektur von Hand nach `<name>_core.py` kopieren |
| Fusion führt das Add-In nicht in der Liste | Ordner, `.py` und `.manifest` tragen nicht denselben Namen | Allen dreien denselben Namen geben. Die Offline-Prüfung testet das |
