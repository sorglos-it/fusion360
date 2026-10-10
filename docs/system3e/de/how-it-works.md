# Funktionsweise

Zurück zur [Übersicht](index.md).

## Die Dateien des Add-Ins

Der installierte Ordner `System3E` enthält:

| Datei oder Ordner | Zweck |
| --- | --- |
| `System3E.py` | Der Befehl: Dialog, Setzen, Punkte |
| `system3e_core.py` | Allgemeine Helfer: Sprache, Schaltfläche in der Werkzeugleiste, Fehlermeldungen, Version |
| `System3E.manifest` | Nennt Fusion den Namen, den Autor, die Version und dass das Add-In mit Fusion startet |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Alle Texte, eine Datei je Sprache |
| `blocks/blocks.json` | Die Bausteinbibliothek: die Form aller 74 Bausteine |
| `blocks/<id>.png` | Ein Vorschaubild je Baustein, zusammen 74 |
| `resources/System3E/16x16.png`, `32x32.png`, `64x64.png` | Das Symbol der Schaltfläche |

Das Add-In liest nur diese Dateien. Es schreibt keine Dateien und öffnet keine Netzwerkverbindung.

## Start und Stopp

Wenn das Add-In startet:

1. Es ermittelt die Sprache (siehe [settings.md](settings.md)) und lädt die Texte.
2. Es entfernt eine übrig gebliebene Schaltflächen-Definition eines früheren Laufs, falls es eine gibt.
3. Es legt die Schaltfläche **SYSTEM 3E Baustein** an. Die Version aus dem Manifest wird in Klammern angehängt.
4. Es sucht im Arbeitsbereich Konstruktion das Panel **Create** der Volumenkörper-Werkzeuge und setzt die Schaltfläche dorthin.
   Wird das Panel nicht gefunden, zeigt es eine Meldung und fügt keine Schaltfläche hinzu.

Wenn das Add-In stoppt, entfernt es die Schaltfläche wieder.

## Die Bausteinbibliothek

`blocks/blocks.json` ist eine Textdatei im JSON-Format. Sie enthält:

- `unit`: immer `mm`. Alle Längen in der Datei sind Millimeter.
- `blocks`: eine Liste von 74 Bausteinen in Katalogreihenfolge.

Jeder Baustein hat diese Einträge:

| Eintrag | Inhalt | Beispiel |
| --- | --- | --- |
| `id` | Kurzname für Dateien, Kleinbuchstaben | `s1-wp` |
| `name` | Katalogname | `S1 WP` |
| `family` | Eines von `starter`, `basic`, `complementary`, `lintel`, `window`, `top`, `corner`, `partition` | `basic` |
| `size` | Länge, Breite, Höhe in ganzen mm | `[707, 352, 300]` |
| `stack` | Höhe, auf der die nächste Schicht steht, mm | `250.0` |
| `points` | Die Eckpunkte der Form, jeder als x, y, z in mm | `[0.0, 271.0, 200.0]` |
| `faces` | Die ebenen Flächen. Jede hat eine Richtung (`normal`) und einen oder mehrere Umrisse (`loops`). | – |

Ein Umriss ist eine Liste von Zahlen. Jede Zahl nennt einen der `points`. Der erste Umriss einer Fläche ist ihr äußerer
Rand. Weitere Umrisse sind Löcher in der Fläche.

Jeder Baustein liegt mit seiner untersten Ecke bei 0, 0, 0. Seine Länge läuft entlang x, seine Breite (die Wanddicke)
entlang y, seine Höhe entlang z.

Die Bibliothek wird einmal gelesen, wenn der Dialog zum ersten Mal aufgeht. Das Vorschaubild eines Bausteins ist die Datei
`blocks/<id>.png`.

## Wie ein Körper entsteht

Die Bausteine sind nicht als Fusion-Dateien gespeichert. Das Add-In baut jeden Körper aus den Punkten und Flächen:

1. Jeder Punkt des Bausteins wird eine Ecke des Körpers.
2. Jede Fläche wird eine ebene Fläche. Ihre Lage ergibt sich aus ihrem ersten Punkt und ihrer Richtung.
3. Jeder Umriss wird eine geschlossene Kette gerader Kanten.
4. Jede Kante wird einmal festgelegt und von ihren zwei Nachbarflächen benutzt, in entgegengesetzter Richtung. Dadurch ist
   der Körper geschlossen (ein Volumenkörper).
5. Fusion prüft das Ergebnis vollständig und erzeugt den Körper. Lehnt Fusion es ab, zeigt das Add-In die Meldung
   „Der Baustein {0} konnte nicht erzeugt werden:“ mit dem Grund von Fusion.

Alle Flächen sind eben und alle Kanten gerade. Es gibt keine gekrümmten Flächen.

## Komponenten und Wiederverwendung

Beim Druck auf **OK**:

1. Das Add-In sucht in der Konstruktion nach einer Komponente dieses Bausteins.
   - Es sucht nach einer unsichtbaren Markierung (ein Fusion-Attribut, Gruppe `System3E`, Name `block`) mit der `id` des Bausteins.
   - Bausteine, die gesetzt wurden, bevor es die Markierung gab, werden über den Namen `SYSTEM 3E <name>` gefunden.
   - Komponenten ohne Körper und Komponenten einer verknüpften Konstruktion werden übersprungen.
2. **Gefunden:** Das Add-In ergänzt die der zwölf Punkte, die fehlen, und fügt eine weitere Kopie dieser
   Komponente an der neuen Stelle ein.
3. **Nicht gefunden:** Das Add-In baut den Körper, legt in der obersten Ebene der Konstruktion eine neue Komponente namens
   `SYSTEM 3E <name>` an, markiert sie, legt den Körper namens `<name>` hinein und fügt die zwölf Punkte hinzu.

Weil gleiche Bausteine Kopien einer Komponente sind, zählt eine Stückliste sie zusammen.

In einer Konstruktion mit Zeitachse (Fusion nennt das eine parametrische Konstruktion) muss ein fertiger Körper in einem
„base feature“ ankommen. Das Add-In legt eines an, legt den Körper und die Punkte hinein und schließt es. In einer Konstruktion ohne
Zeitachse werden der Körper und die Punkte direkt hinzugefügt.

Schlägt beim Erzeugen eines Bausteins etwas fehl, meldet das Add-In Fusion, dass der Befehl fehlgeschlagen ist. Fusion macht dann
rückgängig, was bis dahin gebaut wurde.

## Die Konstruktionspunkte

Jede Komponente bekommt zwölf Konstruktionspunkte. Mit L = Länge, W = Breite und S = `stack` des Bausteins liegen sie
an diesen Stellen in den eigenen Koordinaten des Bausteins (mm):

| Name | x | y | z |
| --- | --- | --- | --- |
| unten vorne | 0 | W/2 | 0 |
| unten Mitte | L/2 | W/2 | 0 |
| unten hinten | L | W/2 | 0 |
| oben vorne | 0 | W/2 | S |
| oben Mitte | L/2 | W/2 | S |
| oben hinten | L | W/2 | S |
| oben Mitte rechts | L/2 | 0 | S |
| oben Mitte links | L/2 | W | S |
| unten Mitte rechts | L/2 | 0 | 0 |
| unten Mitte links | L/2 | W | 0 |
| Mitte rechts, 50 mm hoch | L/2 | 0 | 50 |
| Mitte links, 50 mm hoch | L/2 | W | 50 |

Die drei Ecken, die unter **Setzen an** angeboten werden, sind keine Konstruktionspunkte. Mit H = Höhe liegen sie bei:

| Eintrag | x | y | z |
| --- | --- | --- | --- |
| Ecke unten vorne rechts | 0 | 0 | 0 |
| Ecke oben vorne rechts | 0 | 0 | H |
| Ecke oben vorne links | 0 | W | H |

Jeder Punkt trägt eine unsichtbare Markierung (Attributgruppe `System3E`, Name `point`) mit seinem Schlüssel. An dieser Markierung
erkennt das Add-In, welche Punkte eine Komponente schon hat, und ergänzt nur die fehlenden.

Der Punkt gehört zur Komponente. Deshalb zeigt jede Kopie eines Bausteins dieselben zwölf Punkte an ihrer eigenen Stelle.

## Wie die Lage berechnet wird

1. Die Stelle, die unter **Setzen an** gewählt ist, wird in den Ursprung geschoben.
2. Der Baustein wird um die Z-Achse um die **Drehung** gedreht.
3. Der Baustein wird zum angeklickten Punkt plus **Versatz X**, **Versatz Y**, **Versatz Z** geschoben.
   Ohne angeklickten Punkt wird der Ursprung (0, 0, 0) benutzt.

Der Versatz wird nach der Drehung angewendet. Er läuft also entlang der Achsen der Konstruktion, nicht entlang des gedrehten Bausteins.

Die Lage eines angeklickten Skizzenpunkts wird in den Koordinaten der ganzen Konstruktion genommen, nicht in denen seiner Skizze.

## Einheiten

| Wo | Einheit |
| --- | --- |
| Bausteinbibliothek `blocks.json` | mm |
| Felder **Versatz X**, **Versatz Y**, **Versatz Z** | in mm angezeigt |
| Feld **Drehung** | in Grad angezeigt |
| In der Programmierschnittstelle von Fusion | cm und Bogenmaß |

Das Add-In teilt jeden Wert der Bibliothek durch 10, wenn es ihn an Fusion übergibt. Umrechnen muss man nichts.

## Die Vorschau

Solange der Dialog offen ist, fragt Fusion das Add-In nach jeder Änderung nach einer Vorschau. Das Add-In führt dann dieselben
Schritte aus wie bei **OK**. Fusion verwirft diese Vorschau und führt die Schritte noch einmal aus, wenn **OK** gedrückt wird.
Fehler während der Vorschau werden nicht angezeigt.
