# Bedienung

Alle Feldnamen unten stehen genau so da, wie sie im deutschen Dialog erscheinen. Einzelheiten zu jedem Feld: [settings.md](settings.md).

## Ein Raster zeichnen

1. Eine Skizze öffnen oder bearbeiten.
2. Einen Skizzenpunkt anklicken. Das kann der Ursprung der Skizze sein oder ein selbst gesetzter Punkt.
3. Die Schaltfläche **Skizzenraster** anklicken. Der Dialog öffnet sich. Der angeklickte Punkt ist in **Punkt** schon eingetragen.
4. Ist **Punkt** leer, jetzt einen Skizzenpunkt anklicken. Die Aufforderung lautet „Skizzenpunkt wählen“.
5. Die Werte einstellen. Die Zeile **Ergebnis** zeigt, was herauskommt, zum Beispiel `8 × 4 = 32 Formen, 94.00 × 26.00 mm gesamt`.
6. Die Vorschau in der Skizze ansehen.
7. **OK** drücken.

Nur Skizzenpunkte lassen sich wählen. Es wird genau ein Punkt gebraucht.

**OK** ist ausgegraut, solange ein Wert nicht erlaubt ist. Meist zeigt die Zeile **Ergebnis** dann den Grund. Siehe [troubleshooting.md](troubleshooting.md).

Das Raster liegt entlang der X- und der Y-Achse der Skizze. Im Dialog lässt es sich nicht drehen. Wörter wie „links“, „rechts“, „oben“, „unten“ und „nach oben“ meinen in dieser Dokumentation die Achsen der Skizze: rechts ist +X, oben ist +Y.

Das Übernehmen eines Punkts, der vor dem Öffnen des Dialogs angeklickt wurde (Schritt 3), wurde in Version 1.1.0.0 geändert und nur offline geprüft, nicht in Fusion. Wird der Punkt nicht übernommen, ihn im Dialog wählen (Schritt 4).

## Beispiel

Mit diesen Werten startet der Dialog:

| Feld | Wert |
| --- | --- |
| **Form** | Rechteck |
| **Länge (X)** | 10 mm |
| **Tiefe (Y)** | 5 mm |
| **Abstand X** / **Abstand Y** | 2 mm |
| **Spalten** / **Zeilen** | 8 / 4 |

Ergebnis: 32 Rechtecke. Das Raster misst 94 × 26 mm (8 × 10 + 7 × 2 = 94, 4 × 5 + 3 × 2 = 26). Steht **Punkt liegt im Raster** auf **In der Mitte**, ist der Punkt der Mittelpunkt des Rasters.

## Wählen, wie die Formen gezählt werden

Feld **Anzahl aus**.

### Spalten und Zeilen

1. **Anzahl aus** auf **Spalten und Zeilen** stellen.
2. **Spalten** und **Zeilen** eingeben.

Es entstehen genau so viele. Das Raster wird so groß, wie es sein muss.

### Fläche füllen

1. **Anzahl aus** auf **Fläche füllen** stellen.
2. **Breite der Fläche** und **Höhe der Fläche** eingeben.

Das Add-in zeichnet so viele Formen, wie **ganz** in die Fläche passen. Eine nur teilweise passende Form wird nie gezeichnet.

- Beispiel: Breite der Fläche 100 mm, Länge 10 mm, Abstand 2 mm ergibt 8 Spalten. Sie brauchen 94 mm. Eine neunte Spalte bräuchte 106 mm.
- Das Raster ist meist etwas kleiner als die Fläche. Die Fläche dient nur zum Zählen. Sie wird nicht gezeichnet.
- Der Rest der Fläche bleibt auf der Seite leer, die vom Punkt abgewandt ist. Bei **In der Mitte** wird er gleichmäßig auf beide Seiten verteilt.
- Eine Fläche von genau 94 mm ergibt 8 Spalten; 93,9 mm ergeben 7.

Die Felder **Spalten** und **Zeilen** werden nur in der ersten Betriebsart gezeigt, **Breite der Fläche** und **Höhe der Fläche** nur in der zweiten.

## Die Form wählen

Feld **Form**.

| Eintrag | Was herauskommt |
| --- | --- |
| **Rechteck** | Ein Rechteck von Länge × Tiefe. Seine Ecken lassen sich ändern, siehe unten. |
| **Kreis / Ellipse** | Eine Ellipse mit Länge und Tiefe als ihren beiden Durchmessern. Gleiche Werte ergeben einen Kreis. |
| **Langloch** | Ein Rechteck mit zwei halbrunden Enden. Die Enden liegen in der längeren Richtung: Ist die Länge größer als die Tiefe, sind das linke und das rechte Ende rund. Gleiche Werte ergeben einen Kreis. |
| **Vieleck** | Eine Form mit 3 bis 24 geraden Seiten. Eine Ecke zeigt immer nach oben. |

### Rechteck: Ecken

1. **Form** auf **Rechteck** stellen. Das Feld **Eckenform** erscheint.
2. **Scharfkantig**, **Verrundet** oder **Gefast** wählen. (Gefast heißt: Die Ecke wird mit einer geraden Linie abgeschnitten.)
3. Bei **Verrundet** und **Gefast** erscheint das Feld **Radius / Fase**. Den Radius der Rundung eingeben oder wie weit von der Ecke entfernt der Schnitt an jeder Kante beginnt.

Der größte erlaubte Wert ist die Hälfte der kürzeren Kante. Bei genau diesem Wert:

| Rechteck | Wert | Aus Verrundet wird | Aus Gefast wird |
| --- | --- | --- | --- |
| 10 × 5 mm | 2,5 mm | ein Langloch | eine sechseckige Form |
| 10 × 10 mm | 5 mm | ein Kreis | eine Raute |

Die Ecken ändern weder die Zahl der Formen noch die Teilung noch die Gesamtgröße.

### Vieleck: Ecken und Regelmäßig

1. **Form** auf **Vieleck** stellen. Die Felder **Ecken** und **Regelmäßig** erscheinen.
2. **Ecken** eingeben (3 bis 24).
3. **Regelmäßig** aus lassen oder den Haken setzen.

| **Regelmäßig** | Ergebnis |
| --- | --- |
| aus | Das Vieleck wird so gestreckt, dass es genau Länge × Tiefe misst. Seine Seiten sind dann meist nicht gleich lang. |
| an | Alle Seiten sind gleich lang. Der kleinere Wert von Länge und Tiefe bestimmt die Größe. Die Teilung folgt der wirklichen Größe des Vielecks, der Abstand bleibt also der eingegebene Abstand. |

Beispiel mit 6 Ecken, Länge 10 mm, Tiefe 5 mm, Abstand 2 mm:

| **Regelmäßig** | Größe einer Form | Strecke von einer Form zur nächsten |
| --- | --- | --- |
| aus | 10,00 × 5,00 mm | 12,00 × 7,00 mm |
| an | 4,33 × 5,00 mm | 6,33 × 7,00 mm |

## Größe und Abstand einstellen

- **Länge (X)** und **Tiefe (Y)**: Größe einer Form.
- **Abstand X** und **Abstand Y**: freier Raum zwischen zwei Nachbarn. 0 ist erlaubt; die Formen berühren sich dann. Negative Werte sind nicht erlaubt.

## Festlegen, wo der Punkt liegt

Feld **Punkt liegt im Raster**. Es sagt, wo der angeklickte Punkt im fertigen Raster landet. Es sagt nicht, in welche Richtung das Raster wächst.

Beispiel: **Unten links** setzt den Punkt auf die untere linke Ecke des Rasters. Das Raster erstreckt sich dann nach rechts und nach oben.

Drei der neun Lagen, mit einem Raster von 3 × 2 Formen (`X` ist der Punkt, `#` sind die Formen):

```
  In der Mitte         Unten links          Oben mittig
  #####.#####.#####    #####.#####.#####    #####.##X##.#####
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  ........X........    .................    .................
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  #####.#####.#####    X####.#####.#####    #####.#####.#####
```

Alle neun Einträge stehen in [settings.md](settings.md#punkt-liegt-im-raster).

## Das Raster vom Punkt wegschieben

Felder **Versatz X** und **Versatz Y**.

1. Zuerst die Lage in **Punkt liegt im Raster** wählen.
2. Eingeben, wie weit das ganze Raster rücken soll. Positive Werte schieben es entlang der X- und der Y-Achse der Skizze. Negative Werte schieben es in die andere Richtung.

Das dient dazu, einen Rand einzuhalten: Der Punkt bleibt an einer Ecke des Teils, und das Raster beginnt zum Beispiel 2 mm weiter innen. Der Versatz ändert weder die Zahl der Formen noch die Größe des Rasters.

## Die Zeile Ergebnis lesen

**Ergebnis** lässt sich nicht bearbeiten. Es zeigt entweder

- `{Spalten} × {Zeilen} = {Anzahl} Formen, {Breite} × {Höhe} mm gesamt`, immer in Millimetern mit zwei Nachkommastellen, oder
- eine Meldung, die sagt, welcher Wert nicht erlaubt ist.

## Ein weiteres Raster zeichnen

- Der Dialog öffnet sich mit den Werten des letzten Rasters, das mit **OK** abgeschlossen wurde. Siehe [settings.md](settings.md#was-gemerkt-wird).
- Der Befehl ist als wiederholbar gekennzeichnet. Die Fusion-eigene Funktion „letzten Befehl wiederholen“ kann ihn also erneut starten.

## Was in der Skizze entsteht

- Einfache Skizzenlinien, Bögen, Kreise und Ellipsen. Es wird kein Muster-Element von Fusion angelegt.
- Die Formen sind nicht mit dem Dialog verknüpft. Um das Raster später zu ändern, die Formen löschen und ein neues Raster zeichnen.
- Das Add-in fügt zwischen den Formen und dem Punkt keine eigenen Bemaßungen und keine eigenen Abhängigkeiten hinzu.
