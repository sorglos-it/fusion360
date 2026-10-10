# Funktionsweise

## Zwei Dateien

| Datei | Rolle |
| --- | --- |
| Startdatei `AddInTemplate.py` (später `<name>.py`) | Das, was Fusion startet. Enthält die Einstellungen, die eigenen Funktionen, die Ereignis-Handler, `run` und `stop` |
| Kernmodul `addin_core.py` (später `<name>_core.py`) | Teile, die jedes Add-In braucht und die man leicht falsch macht. Nichts darin gehört zu einem bestimmten Add-In |

Fusion findet ein Add-In über den Namen: Ordner, `.py`-Datei und `.manifest`-Datei müssen denselben Namen tragen.

## Was das Kernmodul enthält

| Teil | Aufgabe |
| --- | --- |
| `Strings` | Textkatalog, gelesen aus `lang/<code>.xml`, mit Englisch als Rückfall |
| `detect_language()` | Ermittelt die Sprache, auf die Fusion eingestellt ist |
| `AddInError` | Fehlertyp für Fehler, die der Benutzer beheben kann. Trägt einen Schlüssel, der nicht von der Sprache abhängt |
| `HandlerRegistry` | Hält Ereignis-Handler am Leben |
| `find_panel()` | Findet das erste Panel der Werkzeugleiste aus einer Liste, das existiert |
| `add_button()` | Setzt den Befehl auf ein Panel. Entfernt zuerst ein Bedienelement, das von einem Neuladen übrig ist |
| `remove_button()` | Nimmt das Bedienelement und die Befehlsdefinition wieder von der Werkzeugleiste |
| `report()` | Zeigt einen unerwarteten Fehler mit seinem Traceback in einem Meldungsfenster |
| `read_version()` | Liest die Version aus dem Manifest |
| `display_name()` | Fügt Name und Version zusammen: `Name (1.0.0.0)` |
| `FALLBACK_LANGUAGE`, `SUPPORTED_LANGUAGES`, `FUSION_LANGUAGE_MAP` | Die Sprachtabellen |

## Warum das Kernmodul je Add-In umbenannt wird

Alle Add-Ins laufen im selben Python in Fusion. Sie teilen sich eine Liste der geladenen Module (`sys.modules`).
Würden zwei Add-Ins beide ein Modul namens `addin_core` laden, würden sie gegenseitig ihr Kernmodul überschreiben.

Deshalb benennt das Skript die Datei in `<name in Kleinbuchstaben>_core.py` um und setzt `_CORE_MODULE` in der Startdatei passend dazu.

Folge: Jedes Add-In hat seine **eigene Kopie** des Kernmoduls. Eine Korrektur, die später in der Vorlage gemacht wird, erreicht früher angelegte Add-Ins nicht. Sie muss von Hand kopiert werden.

## Das Kernmodul laden

Die Startdatei macht das vor allem anderen:

1. Sie fügt ihren eigenen Ordner zum Suchpfad von Python hinzu.
2. Sie entfernt das Kernmodul aus `sys.modules`, falls es dort ist.
3. Sie importiert das Kernmodul über den Namen in `_CORE_MODULE`.

Grund für Schritt 2: Fusion hält importierte Module im Zwischenspeicher. Ohne ihn würde ein bearbeitetes Kernmodul seine alte Fassung behalten, bis Fusion neu startet. Mit ihm genügt es, das Add-In zu stoppen und neu zu starten.

## Handler-Register

Fusion hält nur eine schwache Referenz auf einen Ereignis-Handler. Ein Handler, auf den Python nicht mehr verweist, wird aufgeräumt, und sein Ereignis feuert nicht mehr – ohne jede Fehlermeldung. Der Kommentar im Code nennt das den häufigsten Weg, auf dem ein Add-In nur halb funktioniert.

`HandlerRegistry.add(event, handler)` verbindet den Handler mit dem Ereignis **und** speichert ihn in einer Liste. `clear()` leert die Liste, wenn das Add-In stoppt.

## Start und Stopp

### `run(context)`

1. Lädt die erkannte Sprache in den Textkatalog.
2. Löscht eine Befehlsdefinition mit derselben `CMD_ID`, die von einem früheren Lauf übrig ist. Sie würde ihre alte Beschriftung und ihren alten Handler behalten.
3. Legt die Definition der Schaltfläche an: Name mit Version, Tooltip, Symbolordner (falls er existiert).
4. Verbindet `CommandCreatedHandler`.
5. Sucht nach einem Panel. Wird keines gefunden, zeigt es „Kein passendes Toolbar-Panel gefunden.“ und endet.
6. Fügt die Schaltfläche zum Panel hinzu.

Jeder andere Fehler wird als „Start fehlgeschlagen:“ mit dem Traceback angezeigt.

### `stop(context)`

1. Entfernt das Bedienelement vom Panel und löscht die Befehlsdefinition.
2. Leert das Handler-Register.

Ein Fehler wird als „Stopp fehlgeschlagen:“ mit dem Traceback angezeigt.

## Ablauf der Ereignisse

```
button pressed
   -> commandCreated   build the dialog, connect the four handlers below
        -> inputChanged     a field changed        -> on_input_changed()
        -> validateInputs   may OK be pressed?     -> read_inputs(), validate()
        -> executePreview   show a preview         -> read_inputs(), validate(), build_result()
        -> execute          OK pressed             -> read_inputs(), validate(), build_result(), remember()
```

| Ereignis | Handler | Was er macht | Bei einem Fehler |
| --- | --- | --- | --- |
| created | `CommandCreatedHandler` | Kennzeichnet den Befehl als wiederholbar. Sammelt Skizzenlinien, die vor dem Druck auf die Schaltfläche ausgewählt waren. Ruft `build_inputs()` auf. Trägt die erste gesammelte Linie in das Auswahlfeld ein, wenn es noch leer ist. Verbindet die anderen vier Handler | Meldungsfenster „Fehler beim Aufbau des Dialogs:“ mit Traceback |
| input changed | `InputChangedHandler` | Ruft `on_input_changed()` auf. Macht nichts, solange `_updating` gesetzt ist | still |
| validate | `ValidateHandler` | Ruft `read_inputs()` und `validate()` auf. Setzt `areInputsValid` auf true, oder bei jedem Fehler auf false | OK ist ausgegraut, keine Meldung |
| preview | `PreviewHandler` | Führt den ganzen Befehl aus. Setzt dann `isValidResult` auf `False`, sodass Fusion die Vorschau verwirft und für das echte Ergebnis execute ausführt | still, keine Vorschau |
| execute | `ExecuteHandler` | Führt den ganzen Befehl aus, dann `remember()` | `AddInError`: Meldungsfenster mit dem übersetzten Text. Alles andere: „Fehler beim Erzeugen der Geometrie:“ mit Traceback |

„Führt den ganzen Befehl aus“ bedeutet `_run_command()`: `read_inputs()`, dann `validate()`, dann `build_result()`.

Punkte, die daraus folgen:

- Die Auswahl wird gelesen, **bevor** die Eingabefelder angelegt werden, und danach an das Auswahlfeld übergeben. Deshalb funktioniert „eine Linie anklicken, dann die Schaltfläche drücken“.
- Die Vorschau feuert bei jedem Tastendruck und sieht halb getippte Werte. Deshalb schweigt sie bei Fehlern mit Absicht.
- Weder die Vorschau noch die Prüfung sagt dem Benutzer, **warum** etwas falsch ist. Nur execute zeigt einen Text.
- `build_result()` läuft für ein OK zweimal: einmal oder öfter für die Vorschau, einmal für das echte Ergebnis.
- `isValidResult` nur dann auf `True` setzen, wenn die Vorschau schon das endgültige Ergebnis erzeugt hat.

## Zwei Arten von Fehlern

| Art | Wie er ausgelöst wird | Was der Benutzer sieht |
| --- | --- | --- |
| Erwartet – der Benutzer kann ihn beheben | `fail('err.key')` löst `AddInError` aus | OK ausgegraut; ein Meldungsfenster mit dem übersetzten Text nur bei execute |
| Unerwartet – ein Programmfehler | jede andere Ausnahme | Ein Meldungsfenster mit dem Traceback, über `core.report()` |

`AddInError` speichert den Schlüssel (`err.key`) und die Parameter (`err.params`). Der Text wird nachgeschlagen, wenn der Fehler angelegt wird.
Der eigene Code der Vorlage liest den Schlüssel danach nicht; er ist für den eigenen Code da.

## Textkatalog und Rückfall

`S = core.Strings(LANG_DIR)` wird angelegt, wenn die Startdatei importiert wird. Englisch wird sofort geladen, sodass es Texte schon vor `run()` gibt.
`run()` lädt dann die erkannte Sprache.

Wie `load(code)` arbeitet:

1. Ein Code, der nicht in `SUPPORTED_LANGUAGES` steht, wird zu `en`.
2. `en.xml` wird einmal gelesen und als Rückfall behalten.
3. Die Datei der gewählten Sprache wird als aktueller Satz gelesen.

Wie ein Text gefunden wird (`get(key, *args)`):

1. der Text der aktuellen Sprache, wenn er vorhanden und nicht leer ist
2. sonst der englische Text
3. sonst der Schlüssel selbst, zum Beispiel `in.width`

Dann werden die Platzhalter gefüllt. Schlägt das Füllen fehl – zum Beispiel verlangt eine Übersetzung `{1}`, aber es wurde nur ein Wert übergeben –, wird der Text ungefüllt zurückgegeben, statt einen Fehler auszulösen.

Eine Sprachdatei, die fehlt oder kein gültiges XML ist, gilt als leer. Dann kommt jeder Text aus dem Englischen.
Fehlt auch `en.xml` oder ist sie ebenfalls defekt, werden die Schlüssel selbst angezeigt.

## Spracherkennung

Die Reihenfolge steht in [settings.md](settings.md). Zwei Einzelheiten aus dem Code:

- Die Sprachwerte von Fusion werden mit `getattr` über den Namen nachgeschlagen. Ein Wert, den diese Fusion-Version nicht kennt, kann das Add-In nicht zum Absturz bringen.
- Die Funktion löst nie einen Fehler aus. Im schlimmsten Fall gibt sie Englisch zurück.

## Einheiten

Fusion zählt Längen intern in cm. Das Beispiel zeigt das:

- der Startwert `1.0` wird als 10 mm angezeigt
- der Wert, der aus dem Längenfeld gelesen wird, ist in cm
- für die Meldung „Die Länge überschreitet die gewählte Linie ({0} mm).“ wird die Länge der Linie mit 10 multipliziert und mit zwei Nachkommastellen angezeigt

## Daten

Das Add-In liest sein Manifest und seine Sprachdateien. Es schreibt keine Dateien.
