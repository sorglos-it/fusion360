# So funktioniert es

## Dateien

Das installierte Add-in ist ein Ordner, `SketchGrid`:

| Datei | Zweck |
| --- | --- |
| `SketchGrid.py` | Das Add-in selbst: Dialog, Rasterberechnung, Prüfungen, Zeichnen. |
| `sketchgrid_core.py` | Gemeinsame Helfer, die nicht nur zu diesem Add-in gehören: Sprachdateien lesen, Sprache finden, Panel der Werkzeugleiste finden, Ereignis-Handler am Leben halten, unerwartete Fehler zeigen, Version lesen. |
| `SketchGrid.manifest` | Beschreibung für Fusion: Autor, Version, unterstützte Systeme (Windows und macOS), Start mit Fusion. |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Alle Texte, eine Datei je Sprache. `en.xml` ist die Referenz. |
| `resources/SketchGrid/16x16.png`, `32x32.png`, `64x64.png` | Das Symbol der Schaltfläche in drei Größen. |

Das Add-in liest nur seinen eigenen Ordner. Es schreibt keine Dateien und öffnet keine Netzwerkverbindung.

## Start und Stopp

Beim Start (`run`):

1. Die Sprache wird erkannt und die passende Sprachdatei geladen.
2. Eine Befehlsdefinition, die von einem früheren Start übrig ist, wird gelöscht.
3. Der Befehl wird angelegt. Sein Name ist der Text **Skizzenraster** und dahinter die Version aus dem Manifest in Klammern.
4. Das Add-in sucht ein Panel der Werkzeugleiste: zuerst das Panel mit der Kennung `SketchCreatePanel`, dann `SolidCreatePanel`; jeweils zuerst im Arbeitsbereich Design, dann unter allen Panels. Gibt es keines, erscheint die Meldung „Kein passendes Toolbar-Panel gefunden.“ und es wird keine Schaltfläche angelegt.
5. Die Schaltfläche wird in das Panel gelegt und direkt auf der Werkzeugleiste gezeigt.

Beim Stopp (`stop`) werden die Schaltfläche und der Befehl entfernt und die Ereignis-Handler freigegeben.

## Was geschieht, solange der Dialog offen ist

| Ereignis | Was das Add-in tut |
| --- | --- |
| Der Dialog öffnet sich | Baut alle Felder mit den gemerkten Werten auf. Versucht, einen vorher gewählten Skizzenpunkt zu übernehmen. Gelingt das nicht, bleibt der Dialog benutzbar und der Punkt wird im Dialog gewählt. (Nur offline geprüft, nicht in Fusion.) |
| Ein Feld ändert sich | Zeigt oder versteckt die Felder, die zur gewählten Betriebsart und Form gehören. Berechnet die Zeile **Ergebnis** neu. |
| Fusion fragt, ob die Eingaben gültig sind | Führt alle Prüfungen aus. Scheitert eine, wird **OK** gesperrt. |
| Fusion verlangt eine Vorschau | Führt alle Prüfungen aus und zeichnet das Raster als Vorschau. Scheitert eine Prüfung, wird nichts gezeichnet und nichts gemeldet. |
| **OK** | Führt alle Prüfungen noch einmal aus, zeichnet das Raster und merkt sich dann die Werte. |

Die Vorschau wird nicht als Endergebnis weiterbenutzt. Bei **OK** wird das Raster neu gezeichnet.

## Einheiten

- Im Inneren sind alle Längen Zentimeter. Das ist die interne Einheit von Fusion, gleich welche Einheit das Dokument zeigt.
- Die Längenfelder im Dialog werden mit der Einheit `mm` angelegt.
- Für die Zeile **Ergebnis** und für Meldungen werden die Werte in Millimeter umgerechnet (× 10) und mit zwei Nachkommastellen gezeigt.
- Vergleiche lassen eine winzige Toleranz von 0,000000001 cm zu, damit Rundungsrauschen keine Meldung auslöst.

## Wie das Raster berechnet wird

Die Berechnung macht `grid_layout()`. Sie benutzt keine Funktionen von Fusion.

### Schritt 1: Größe einer Form

Normalerweise nimmt eine Form genau Länge × Tiefe ein.

Ausnahme: ein Vieleck, bei dem der Haken bei **Regelmäßig** gesetzt ist. Es braucht weniger Platz. Seine wirkliche Größe wird gemessen:

1. Die Ecken des Vielecks werden auf einen Kreis mit Radius 1 gesetzt, die erste Ecke zeigt nach oben.
2. Breite und Höhe des kleinsten Rechtecks um diese Ecken werden gemessen.
3. Beide werden mit der Hälfte des kleineren Werts von Länge und Tiefe malgenommen.

Beispiel: 6 Ecken, Länge 10 mm, Tiefe 5 mm ergibt 4,33 × 5,00 mm.

### Schritt 2: Teilung

Teilung heißt: die Strecke von einer Form zur selben Stelle an der nächsten Form.

- Teilung X = Größe einer Form in X + **Abstand X**
- Teilung Y = Größe einer Form in Y + **Abstand Y**

### Schritt 3: Zahl der Spalten und Zeilen

**Spalten und Zeilen:** Die Zahlen aus dem Dialog werden genommen.

**Fläche füllen:** n Formen brauchen n Größen und n − 1 Abstände. Also:

- Spalten = (Breite der Fläche + Abstand X) ÷ Teilung X, abgerundet
- Zeilen = (Höhe der Fläche + Abstand Y) ÷ Teilung Y, abgerundet

Beispiel: (100 + 2) ÷ 12 = 8,5, also 8 Spalten.

Ist Spalten × Zeilen mehr als 2000, wird das Raster abgelehnt.

### Schritt 4: Gesamtgröße

- Gesamtbreite = Spalten × Teilung X − Abstand X
- Gesamthöhe = Zeilen × Teilung Y − Abstand Y

Beispiel: 8 × 12 − 2 = 94 mm.

### Schritt 5: Lage (Bezugspunkt und Versatz)

Der Bezugspunkt ist der Eintrag, der in **Punkt liegt im Raster** gewählt ist. Jeder Eintrag steht für zwei Faktoren zwischen 0 und 1: wie weit der Punkt von der linken Kante und von der unteren Kante des Rasters entfernt ist, als Anteil an der Gesamtgröße.

| Eintrag | Faktor X | Faktor Y |
| --- | --- | --- |
| In der Mitte | 0,5 | 0,5 |
| Unten links | 0 | 0 |
| Unten rechts | 1 | 0 |
| Oben links | 0 | 1 |
| Oben rechts | 1 | 1 |
| Unten mittig | 0,5 | 0 |
| Oben mittig | 0,5 | 1 |
| Links mittig | 0 | 0,5 |
| Rechts mittig | 1 | 0,5 |

Die untere linke Ecke des Rasters, gemessen vom gewählten Punkt:

- X = −Faktor X × Gesamtbreite + **Versatz X**
- Y = −Faktor Y × Gesamthöhe + **Versatz Y**

Beispiel: Raster 94 × 26 mm, **In der Mitte**, kein Versatz: Die untere linke Ecke liegt 47 mm links vom Punkt und 13 mm darunter.

Die Versätze werden erst an dieser Stelle hinzugezählt. Sie ändern die Zahl der Formen nicht, auch nicht in der Betriebsart **Fläche füllen**.

### Schritt 6: die einzelnen Formen

`cell_centres()` geht das Raster Zeile für Zeile durch, von der untersten Zeile nach oben, in jeder Zeile von links nach rechts. Für jede Form liefert es die untere linke Ecke ihres Platzes:

- X = Rasterecke X + Spaltennummer × Teilung X
- Y = Rasterecke Y + Zeilennummer × Teilung Y

Spalten- und Zeilennummern beginnen bei 0. Der Name der Funktion ist geschichtlich bedingt; sie liefert Ecken, keine Mittelpunkte.

Der Zeichencode zählt die halbe Größe einer Form hinzu, um den Mittelpunkt zu erhalten, und zählt die Lage des gewählten Punkts in der Skizze hinzu.

Alle Lagen stehen in den Koordinaten der Skizze, zu der der Punkt gehört. Das Raster liegt deshalb immer parallel zur X- und zur Y-Achse dieser Skizze.

## Wie jede Form gezeichnet wird

| Form | Fall | Gezeichnet als |
| --- | --- | --- |
| Rechteck | Ecken **Scharfkantig** | das Zwei-Punkt-Rechteck von Fusion, von der unteren linken zur oberen rechten Ecke |
| Rechteck | **Verrundet**, Radius gleich der Hälfte beider Kanten | ein Kreis |
| Rechteck | **Verrundet**, sonst | bis zu 4 Linien und 4 Bögen |
| Rechteck | **Gefast** | bis zu 4 Linien für die Kanten und 4 Linien für die Schnitte |
| Kreis / Ellipse | Länge gleich Tiefe | ein Kreis |
| Kreis / Ellipse | sonst | eine Ellipse; der längere der beiden Werte wird Fusion als Hauptachse übergeben, weil Fusion die Ellipse sonst zurückweist |
| Langloch | Länge gleich Tiefe | ein Kreis |
| Langloch | sonst | 2 Linien und 2 halbrunde Bögen; die Bögen sitzen an den beiden Enden der längeren Richtung, ihr Radius ist die Hälfte der kürzeren |
| Vieleck | immer | eine Linie je Seite |

Einzelheiten:

- **Verrundetes oder gefastes Rechteck:** `corner_outline()` liefert den Umriss als Liste von Linien und Bögen, gegen den Uhrzeigersinn ab der unteren Kante. Jeder Bogen ist durch drei Punkte gegeben: Anfang, ein Punkt in der Mitte des Bogens, Ende. Ist der Radius oder die Fase genau die Hälfte einer Kante, hat das gerade Stück auf dieser Seite keine Länge und wird weggelassen.
- **Vieleck:** Die erste Ecke zeigt nach oben. Ohne **Regelmäßig** werden die Ecken so gestreckt, dass das kleinste Rechteck um sie genau Länge × Tiefe misst. Mit **Regelmäßig** werden beide Richtungen mit der Hälfte des kleineren Werts von Länge und Tiefe skaliert. In beiden Fällen wird das Vieleck auf sein eigenes Rechteck zentriert, nicht auf seinen Kreis. Das zählt bei ungeraden Seitenzahlen: Ein Fünfeck hat oben eine Ecke, unten aber eine flache Seite.
- **Verbindung der Kurven:** Das Vieleck wird als Kette gezeichnet. Jede Linie beginnt am Endpunkt der Linie davor, und die letzte schließt auf den Startpunkt der ersten. Das Langloch und das verrundete oder gefaste Rechteck werden anders gezeichnet: Jede Linie und jeder Bogen wird für sich aus Koordinaten angelegt. Ihre Enden liegen an derselben Stelle, aber sie werden nicht als gemeinsame Punkte angelegt. Siehe [bekannte Grenzen](troubleshooting.md#bekannte-grenzen).
- Das Add-in selbst fügt keine Bemaßungen und keine Abhängigkeiten hinzu. Ob Fusion dem Zwei-Punkt-Rechteck von sich aus welche gibt, entscheidet nicht das Add-in.

Während das Raster gezeichnet wird, wird der Skizze gesagt, dass sie nicht nach jeder einzelnen Kurve neu rechnen soll (`isComputeDeferred`). Sie rechnet einmal am Ende neu. Die Einstellung wird in jedem Fall zurückgestellt, auch nach einem Fehler.

## Die Prüfungen

Reihenfolge, in der die Prüfungen laufen:

1. Genau ein Skizzenpunkt ist gewählt.
2. Ist die Form ein Vieleck: Ecken zwischen 3 und 24.
3. Länge größer als 0.
4. Tiefe größer als 0.
5. Kein Abstand negativ.
6. Betriebsart **Fläche füllen**: beide Werte der Fläche größer als 0; dann passen mindestens eine Spalte und eine Zeile.
7. Betriebsart **Spalten und Zeilen**: mindestens eine Spalte, mindestens eine Zeile.
8. Spalten × Zeilen höchstens 2000.
9. Ist die Form ein Rechteck und die Eckenform nicht **Scharfkantig**: Radius / Fase größer als 0 und höchstens die Hälfte der kürzeren Kante. Ein zu großer Wert wird abgelehnt, nicht stillschweigend verkleinert.

Die erste Prüfung, die scheitert, bestimmt die Meldung. Die Texte stehen in [troubleshooting.md](troubleshooting.md).

Die Zeile **Ergebnis** führt nur die Prüfungen 3 bis 9 aus. Scheitert Prüfung 1 oder 2, wird **OK** deshalb gesperrt, ohne dass in der Zeile **Ergebnis** ein Text steht.

## Texte und Sprache

- Jede Sprachdatei ist eine Liste aus Schlüsseln und Texten. Der Code kennt nur die Schlüssel.
- Stellen für Werte stehen in den Texten als `{0}`, `{1}` und so weiter und werden vom Add-in gefüllt.
- Englisch wird zuerst als Rückfall geladen. Ein Schlüssel, der in der aktiven Sprache fehlt, wird aus dem Englischen genommen. Ein Schlüssel, der überall fehlt, wird als der Schlüssel selbst gezeigt.
- Wie die Sprache gewählt wird: siehe [settings.md](settings.md#sprache).
