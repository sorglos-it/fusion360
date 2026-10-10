# Bedienung

## Der Beispielbefehl

Der Beispielbefehl zeichnet eine kurze Linie (einen „Strich“) auf der Mitte einer Skizzenlinie. Der Strich steht im rechten Winkel zu dieser Linie.
Seine einzige Aufgabe ist zu zeigen, dass Auswahl, Vorschau, Prüfungen und Übersetzung funktionieren. Er wird durch den eigenen Befehl ersetzt.

In der unveränderten Vorlage heißt der Befehl **Add-In-Vorlage**. Sein Tooltip lautet:

> Ausgangspunkt für ein Fusion-360-Add-In.
> Zeichnet einen Strich auf der Mitte der gewählten Linie.

### Der Dialog

| Feld | Art | Bedeutung | Startwert |
| --- | --- | --- | --- |
| **Linie** | Auswahl, Aufforderung „Skizzenlinie wählen“ | Die Skizzenlinie, die den Strich bekommt. Genau eine Linie. Nur Skizzenlinien lassen sich wählen | leer, oder die Linie, die vorher ausgewählt war |
| **Länge** | Wert in mm | Länge des Strichs. Nimmt Ausdrücke wie `2 * 3 mm` an | 10 mm |
| **Richtung umkehren** | Kontrollkästchen | Zeichnet den Strich auf die andere Seite der Linie | aus |

### Ausprobieren

1. Eine Skizze öffnen und eine Linie zeichnen.
2. Die Linie anklicken.
3. Die Schaltfläche **Add-In-Vorlage** drücken. Die Linie ist schon in **Linie** eingetragen.
4. Eine **Länge** eingeben. Die Vorschau zeigt den Strich sofort.
5. Den Haken bei **Richtung umkehren** setzen, um den Strich auf die andere Seite zu drehen.
6. **OK** drücken.

Es geht auch umgekehrt: erst die Schaltfläche drücken und danach die Linie wählen.

### Regeln, die der Befehl prüft

| Regel | Meldung bei Verstoß |
| --- | --- |
| Genau eine Skizzenlinie ist ausgewählt | „Bitte genau eine Skizzenlinie wählen.“ |
| Die Länge ist größer als 0 | „Die Länge muss größer als 0 sein.“ |
| Die gewählte Linie ist länger als 0 | „Die gewählte Linie hat keine Länge.“ |
| Der Strich ist nicht länger als die gewählte Linie | „Die Länge überschreitet die gewählte Linie ({0} mm).“ |

Solange eine Regel verletzt ist, ist **OK** ausgegraut und die Vorschau bleibt leer. Der Dialog sagt **nicht**, warum.
Der Meldungstext erscheint nur dann als Meldungsfenster, wenn der Fehler beim Ausführen des Befehls auftritt.

### Weiteres Verhalten

- **Länge** und **Richtung umkehren** werden für den nächsten Aufruf gemerkt. Sie sind vergessen, wenn Fusion geschlossen oder das Add-In neu gestartet wird.
- Der Befehl ist wiederholbar (`isRepeatable` ist gesetzt), sodass „letzten Befehl wiederholen“ von Fusion ihn erneut starten kann.
- Einzelheiten zur Geometrie: Es werden nur die X- und Y-Werte der Endpunkte der Linie in der Skizze benutzt. Der Strich wird bei Z = 0 der Skizze gezeichnet.

Das Verhalten in Fusion ist nach dem Code beschrieben. Es wurde für diese Dokumentation nicht in Fusion geprüft.

## Daraus ein eigenes Add-In machen

Zuerst mit dem Skript eine Kopie anlegen, siehe [installation.md](installation.md). Dann in `<name>.py` arbeiten.

Die Startdatei hat drei Zonen:

| Zone | Inhalt | Bearbeiten? |
| --- | --- | --- |
| über `CONFIGURE` | lädt das Kernmodul | nur, wenn weitere eigene Module hinzukommen |
| `CONFIGURE` bis `END OF TEMPLATE` | Einstellungen und die eigenen Funktionen | **ja – das ist der eigene Teil** |
| unter `END OF TEMPLATE` | die Ereignis-Handler, `run` und `stop` | normalerweise nicht |

### Schritt für Schritt

1. **Die ids setzen.** `CMD_ID`, `WORKSPACE_ID` und `PANEL_IDS` prüfen. Siehe [settings.md](settings.md).
2. **Die Eingabefelder benennen.** `IN_LINE`, `IN_LENGTH`, `IN_FLIP` durch ids für die eigenen Felder ersetzen.
3. **Startwerte setzen.** Den Startwert jedes gemerkten Felds in `_last` eintragen. Längen sind in cm.
4. **Den Dialog aufbauen** in `build_inputs(inputs)`.
5. **Den Dialog lesen** in `read_inputs(inputs)`.
6. **Die Werte prüfen** in `validate(values)`.
7. **Die Arbeit erledigen** in `build_result(values)`.
8. **Werte merken** in `remember(values)`.
9. **Auf Änderungen reagieren** in `on_input_changed(inputs, changed)`, wenn ein Feld ein anderes ändern soll.
10. **Die Texte schreiben.** Die eigenen Schlüssel in `lang/en.xml` eintragen, dann die anderen Dateien übersetzen. Den `TODO`-Tooltip ersetzen.
11. **Die Vorauswahl anpassen.** `CommandCreatedHandler` (unter `END OF TEMPLATE`) sammelt Skizzenlinien, die vor dem Druck auf die Schaltfläche ausgewählt waren. Braucht der eigene Befehl eine andere Art von Objekt, dort die Typprüfung ändern oder den Block entfernen.
12. **Ein Symbol zeichnen**, siehe [development.md](development.md).
13. **Das Manifest ausfüllen**: Beschreibung, Autor, Version. Siehe [settings.md](settings.md).
14. **Die Offline-Prüfung ausführen**, siehe [development.md](development.md).
15. **In Fusion ausprobieren.** Nach jeder Änderung das Add-In stoppen und neu starten.

### Die Funktionen, die bearbeitet werden

| Funktion | Wofür sie da ist | Regeln |
| --- | --- | --- |
| `build_inputs(inputs)` | Legt den Dialog an. Jede Beschriftung kommt über `T('key')` aus dem Textkatalog | Gibt das Auswahlfeld zurück. Der Aufrufer trägt die vorab gewählte Linie dort ein. `None` zurückgeben, wenn es kein Auswahlfeld gibt |
| `read_inputs(inputs)` | Liest jeden Wert des Dialogs an einer Stelle und gibt ein `dict` zurück | Ausführung, Vorschau und Prüfung rufen sie alle auf und sehen so dieselben Zahlen |
| `validate(values)` | Bricht mit `fail('err.key')` ab, bei allem, was der Benutzer beheben muss | Sie läuft vor dem Zeichnen und noch einmal für die OK-Schaltfläche. Eine unmögliche Eingabe graut OK aus, statt mittendrin fehlzuschlagen |
| `build_result(values)` | Erledigt die eigentliche Arbeit | Wenn sie läuft, ist schon alles geprüft. Sie läuft für die Vorschau **und** für das echte Ergebnis |
| `remember(values)` | Kopiert Werte für den nächsten Aufruf nach `_last` | Wird nur nach einer erfolgreichen Ausführung aufgerufen |
| `on_input_changed(inputs, changed)` | Schaltet ein Feld von einem anderen aus ein oder aus oder passt es an | In der Vorlage leer. `_updating` um jeden Wert setzen, der zurückgeschrieben wird, sonst ruft das Schreiben diese Funktion erneut auf |

### Helfer, die aufgerufen werden

| Helfer | Was er macht |
| --- | --- |
| `T(key, *args)` | Gibt den Text für `key` in der aktiven Sprache zurück. `args` füllen `{0}`, `{1}`, … |
| `fail(key, *args)` | Löst einen `AddInError` mit dem Text für `key` aus. Für alles benutzen, was der Benutzer beheben kann |
| `core.report(ui, S, key)` | Zeigt einen unerwarteten Fehler mit seinem Traceback. Nur für das wirklich Unerwartete |

### Einen Text hinzufügen

1. Eine Zeile in `lang/en.xml` eintragen: `<string key="in.width">Width</string>`
2. Sie im Code benutzen: `T('in.width')`
3. Denselben Schlüssel in die anderen Sprachdateien eintragen.

Schlüssel, die in einer anderen Sprache fehlen, werden englisch angezeigt. Platzhalter wie `{0}` müssen in jeder Übersetzung erhalten bleiben.
