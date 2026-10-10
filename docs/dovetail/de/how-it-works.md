# So funktioniert es

## Dateien

Alles, was das Add-in braucht, liegt in einem Ordner, `Dovetail`:

| Datei | Zweck |
|---|---|
| `Dovetail.py` | Das ganze Programm: Sprache, Geometrie, Zeichnen, Dialog, Start und Stopp |
| `Dovetail.manifest` | Beschreibung für Fusion: Name, Autor, Version, unterstützte Systeme, Start mit Fusion |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Alle Texte, eine Datei je Sprache |
| `resources/Dovetail/` | Symbol für die Werkzeugleiste in 16, 32 und 64 Pixeln |
| `resources/nudge_left/`, `nudge_center/`, `nudge_right/` | Symbole der drei Schaltflächen von **Verschieben** |

Das Add-in liest nur diese Dateien. Es schreibt keine Dateien und öffnet keine Netzwerkverbindung.

## Start und Stopp

Beim Start macht das Add-in Folgendes:

1. Es wählt die Sprache (siehe [settings.md](settings.md#sprache)),
2. meldet den Befehl mit dem Namen „Schwalbenschwanz“ und der Version aus dem Manifest in Klammern an,
3. sucht ein Panel der Werkzeugleiste und legt die Schaltfläche dort ab (siehe
   [installation.md](installation.md#erster-start-in-fusion)).

Beim Stopp entfernt es die Schaltfläche und den Befehl wieder.

## Von der Linie zum Band

### 1. Ein Lineal entlang der Linie

Für jede gewählte Linie richtet das Add-in ein eigenes Maßsystem ein:

- **s** läuft entlang der Linie, vom Startpunkt (0) zum Endpunkt (der Linienlänge).
- **h** läuft im rechten Winkel zur Linie, zu der Seite, zu der die Zähne zeigen.

Ohne **Richtung umkehren** zeigt h nach links, wenn man vom Startpunkt zum Endpunkt blickt.
Mit **Richtung umkehren** zeigt h nach rechts.

### 2. Wo die Zähne sitzen

Die Mitte der Gruppe liegt bei: Linienlänge ÷ 2 + Verschiebung.
Die Zähne werden zu beiden Seiten davon gesetzt, jeder um einen **Abstand** vom nächsten entfernt.

### 3. Der Sollumriss

Der Sollumriss ist die gemeinsame Kante, die die beiden Teile ganz ohne Spalt hätten. Er ist eine offene
Zickzacklinie:

1. Er beginnt am Startpunkt der Linie,
2. läuft entlang der Linie zum ersten Zahn,
3. geht an einer Seite des Zahns hinauf, über die Spitze und an der anderen Seite hinunter,
4. läuft weiter entlang der Linie zum nächsten Zahn,
5. endet am Endpunkt der Linie.

Die Spitze ist bei einem Dreieck ein Punkt, bei einem Trapez oder Rechteck sind es zwei Punkte.

Mit **Geometrie spiegeln** zeigt die erste Hälfte der Zähne zur Gegenseite (minus h), die zweite Hälfte zur
normalen Seite (plus h).

### 4. Die Toleranz aufteilen

Vom Sollumriss werden zwei Kopien gemacht, jede um eine feste Strecke seitlich versetzt (ein Parallelversatz):

- Die Kontur der **Tasche** wird zur Zahnseite versetzt. Die Tasche wird größer.
- Die Kontur des **Zapfens** wird zur anderen Seite versetzt. Der Zapfen wird kleiner.

**Die Linie ist** entscheidet, wie weit jede versetzt wird:

| Eintrag | Tasche versetzt um | Zapfen versetzt um |
|---|---|---|
| Mittellinie | ½ × Toleranz | ½ × Toleranz |
| Kante der Tasche | 0 (bleibt auf dem Sollumriss) | Toleranz |
| Kante des Zapfens | Toleranz | 0 (bleibt auf dem Sollumriss) |

Die beiden Anteile ergeben zusammen immer die volle Toleranz. Weil beide Konturen parallele Kopien desselben
Umrisses sind, ist der Spalt zwischen ihnen überall gleich: an der Basis, an den Seiten und an der Spitze.

So wird versetzt:

- Jedes gerade Stück wird um die Strecke seitlich verschoben.
- An jeder Ecke werden die beiden verschobenen Stücke verlängert oder gekürzt, bis sie sich treffen (eine
  Gehrungsecke).
- Die beiden Enden werden gerade seitlich verschoben. So beginnen beide Konturen bei s = 0 und enden bei
  s = Linienlänge.

### 5. Das geschlossene Band

Die beiden Konturen werden zu einem geschlossenen Zug verbunden:

1. entlang der Kontur der Tasche vom Anfang zum Ende der Linie,
2. hinüber zur Kontur des Zapfens am Ende der Linie,
3. zurück entlang der Kontur des Zapfens,
4. hinüber zum Ausgangspunkt.

Das Innere dieses Zugs ist der Spalt selbst. Es ist ein Band von genau der Toleranz, das dem Umriss der Zähne
folgt. Wird es aus einem Körper herausgeschnitten, bleiben zwei Teile, die passen.

### 6. Zeichnen

- Das Band wird als Kette gerader Skizzenlinien gezeichnet. Jede Linie beginnt am Endpunkt der vorigen, und die
  letzte schließt zurück zur ersten. Der Umriss ist deshalb verbunden.
- Die Linien kommen in die Skizze, zu der die gewählte Linie gehört.
- Beim Zeichnen wird der Skizze gesagt, dass sie nicht nach jeder einzelnen Linie neu rechnen soll. Sie rechnet
  einmal am Ende neu.
- Bei OK, und nur wenn der Haken gesetzt ist, wird zuerst die Originallinie in eine Konstruktionslinie umgewandelt.
  Eine normale Linie würde durch das Band laufen und es in zwei Flächen teilen.
- Das Add-in fügt keine Bemaßungen und keine Abhängigkeiten hinzu.

## Die Prüfungen

Bevor irgendetwas gezeichnet wird, wird die ganze Auswahl einmal durchgerechnet. Erst wenn jede Linie besteht,
beginnt das Zeichnen. Eine schlechte Linie am Ende der Auswahl kann deshalb keine halb gezeichnete Skizze
hinterlassen.

Die Prüfungen laufen für jede Linie in dieser Reihenfolge:

| # | Prüfung | Schlüssel der Meldung, wenn sie scheitert |
|---|---|---|
| 1 | Die Linie hat eine Länge | `err.zero_length` |
| 2 | Die Breite ist größer als 0 | `err.width` |
| 3 | Die Tiefe ist größer als 0 | `err.depth` |
| 4 | Die Toleranz ist größer als 0 | `err.tolerance_zero` |
| 5 | Die Anzahl ist mindestens 1 | `err.count` |
| 6 | Spiegeln: Die Anzahl ist gerade | `err.mirror_even` |
| 7 | Spiegeln: Die Mittellinie ist gewählt | `err.mirror_center` |
| 8 | Spiegeln: Die Verschiebung ist 0 | `err.mirror_offset` |
| 9 | Trapez: Der Flankenwinkel liegt innerhalb von ±89 Grad | `err.angle_range` |
| 10 | Trapez: Die Spitze behält eine Breite | `err.angle_negative` |
| 11 | Zwei oder mehr Zähne: Der Abstand ist größer als 0 | `err.spacing_positive` |
| 12 | Zwei oder mehr Zähne: Der Abstand ist mindestens der Mindestabstand | `err.spacing_too_small` |
| 13 | Die Zähne samt dem Abstand zu den Enden passen auf die Linie | `err.offset_range` oder `err.does_not_fit` |
| 14 | Keine Gehrungsecke rückt weiter weg als 12 × die Versatzstrecke | `err.miter_runaway` |
| 15 | Beide Konturen beginnen und enden genau an den Linienenden und bleiben dazwischen | `err.does_not_fit` |
| 16 | Kein Stück einer Kontur ist auf nichts geschrumpft | `err.tolerance_eats_tooth` |
| 17 | Keine Kontur kreuzt sich selbst | `err.tolerance_eats_tooth` |
| 18 | Es bleibt eine Zahnhöhe übrig | `err.tolerance_eats_tooth` |
| 19 | Die verbleibende Zahnhöhe beträgt mindestens 5 % der Tiefe | `err.tolerance_vs_depth` |
| 20 | Die doppelte Toleranz ist kleiner als die Breite | `err.tolerance_vs_width` |

Bei mehreren Linien wird ein Fehler in `err.on_line` eingepackt. Das nennt die Stelle der Linie in der Auswahl.

Die Texte aller Meldungen stehen in [troubleshooting.md](troubleshooting.md).

### Was der Dialog mit einer gescheiterten Prüfung macht

- Solange der Dialog offen ist: Die Vorschau verschwindet und **OK** ist ausgegraut. Der Text der Meldung wird
  **nicht** gezeigt.
- Scheitert der Lauf selbst nach OK: Ein Meldungsfenster zeigt den Text, und der Lauf wird Fusion als gescheitert
  gemeldet, damit Fusion die schon gezeichneten Linien zurücknimmt. Dieses Zurücknehmen wurde in Fusion nicht
  bestätigt.

## Einheiten

| Wo | Einheit |
|---|---|
| Dialogfelder für Längen | Millimeter |
| Dialogfeld für den Winkel | Grad |
| Zahlen in Meldungen | Millimeter, zwei Nachkommastellen |
| Im Programm | Zentimeter und Bogenmaß (die internen Einheiten von Fusion) |

Feste kleine Werte im Code:

| Wert | Größe | Verwendung |
|---|---|---|
| Zusatzabstand | 0,01 mm | wird zum Mindestabstand und zum Abstand von den Linienenden hinzugezählt |
| Kürzestes Stück | 0,00001 mm | ein kürzeres Konturstück gilt als „keine Länge“ |
| Gehrungsgrenze | 12 × Versatzstrecke | darüber gilt eine Ecke als aus dem Ruder gelaufen |
| Größter Flankenwinkel | unter 89 Grad | |

## Die Höhe wird nicht beachtet

Das Add-in liest nur die X- und Y-Werte der Linienenden in der Skizze und zeichnet das Band auf Höhe 0 der Skizze.
Eine Linie in einer 3D-Skizze oder eine, die die Skizzenebene verlässt, wird behandelt, als wäre sie flach.

## Was sich in 1.1.0.0 geändert hat

Version 1.1.0.0 hat die Geometrie geändert (zuerst als 1.0.0.1 gebaut):

- Zähne halten die Toleranz plus 0,01 mm Abstand von den Enden der Linie. Direkt am Ende lief die Kontur der Tasche
  früher über die Linie hinaus und kehrte um. Das ergab eine Schleife, die sich selbst kreuzte. Die größte
  Verschiebung ist um diesen Betrag kleiner.
- Zwei Zähne brauchen 0,01 mm mehr Abstand. Bei genau dem alten Mindestabstand hatte ein Stück der Kontur keine
  Länge.
- Eine Kontur, die sich selbst kreuzen würde, wird abgelehnt statt gezeichnet.
- Ein gescheiterter Lauf wird zurückgenommen.

Diese Änderungen wurden **nur offline** geprüft, darunter mit 34.317 zufälligen gültigen Konturen, von denen sich
keine selbst kreuzte. Sie sind **noch nicht in Fusion bestätigt**.
