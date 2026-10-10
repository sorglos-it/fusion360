# Bedienung

Alle Feldnamen unten stehen genau so da, wie sie im deutschen Dialog erscheinen. Jedes Feld ist ausführlich in
[settings.md](settings.md) erklärt.

## Hier verwendete Wörter

| Wort | Bedeutung |
|---|---|
| Zahn | Ein Schwalbenschwanz, Dreieck oder Rechteck, das von der Linie absteht |
| Zapfen | Der Zahn als Teil des einen Werkstücks |
| Tasche | Die passende Aussparung im anderen Werkstück |
| Toleranz | Der Spalt zwischen Zapfen und Tasche (das Spiel) |
| Band | Der geschlossene Umriss, den das Add-in zeichnet. Sein Inneres ist genau der Spalt. |
| Startpunkt, Endpunkt | Die beiden Enden einer Skizzenlinie, in der Reihenfolge, in der die Linie gezeichnet wurde |

## Eine Verbindung auf einer Linie zeichnen

1. Eine Skizze öffnen oder eine vorhandene bearbeiten.
2. Eine gerade Linie dort zeichnen, wo die beiden Teile aufeinandertreffen sollen.
3. Die Linie anklicken.
4. Die Schaltfläche **Schwalbenschwanz** anklicken. Der Dialog öffnet sich. Die Linie ist unter **Linien** schon
   eingetragen.
   Es geht auch andersherum: erst den Befehl starten, dann die Linie anklicken.
5. **Anzahl**, **Form**, **Breite (Basis)**, **Tiefe** und **Toleranz** einstellen.
6. Die Vorschau in der Skizze ansehen.
7. **OK** drücken.

Ergebnis:

- In derselben Skizze wie die Linie wird ein geschlossenes Band gezeichnet.
- Die Originallinie wird zur Konstruktionslinie (eine gestrichelte Hilfslinie), wenn bei
  **Originallinie in Konstruktionslinie umwandeln** der Haken gesetzt ist. Das geschieht erst bei OK, nicht in der
  Vorschau.
- Das Add-in gibt den neuen Linien keine Bemaßungen und keine Abhängigkeiten.

Ist **OK** ausgegraut und keine Vorschau zu sehen, passen die Werte nicht. Der Dialog sagt nicht, warum.
Siehe [troubleshooting.md](troubleshooting.md#ok-ist-ausgegraut).

## Aus dem Band zwei passende Teile machen

1. Den Umriss des ganzen Stücks zeichnen. Die Linie der Verbindung quer darüber laufen lassen, von Kante zu Kante.
2. Dovetail auf der Linie der Verbindung ausführen.
3. Den Umriss zu einem Volumenkörper extrudieren.
4. Das Band als Schnitt durch diesen Körper extrudieren.

Es bleiben zwei Körper. Sie passen ineinander, mit dem Spalt, der unter **Toleranz** eingestellt ist.

Die Schritte 3 und 4 sind gewöhnliche Funktionen von Fusion. Das Add-in selbst zeichnet nur das Band.

## Die Form wählen

Dafür gibt es die Liste **Form**:

| Eintrag | Ergebnis |
|---|---|
| **Trapez (Schwalbenschwanz)** | Der Zahn wird zur Spitze hin breiter. Er hakt ein und lässt sich nicht gerade herausziehen. |
| **Dreieck** | Der Zahn läuft spitz zu. Er hat keinen Haken und lässt sich auseinanderziehen. |
| **Rechteck (Fingerzinken)** | Gerader Zahn, an Basis und Spitze gleich breit. |

**Flankenwinkel** ist nur bei **Trapez (Schwalbenschwanz)** aktiv. Er legt fest, wie stark der Zahn breiter wird.
Bei 0 Grad ist das Trapez dasselbe wie ein Rechteck. Ein negativer Winkel macht den Zahn zur Spitze hin schmaler.

## Mehrere Zähne auf einer Linie

1. **Anzahl** auf 2 oder mehr setzen. Das Feld **Abstand (Mitte-Mitte)** wird aktiv.
2. **Abstand (Mitte-Mitte)** einstellen: die Strecke von der Mitte eines Zahns zur Mitte des nächsten.

Die Gruppe der Zähne sitzt immer symmetrisch um die Mitte der Linie:

| Anzahl | Lage der Zähne zur Mitte (Abstand 30 mm) |
|---|---|
| 1 | 0 |
| 2 | −15 / +15 |
| 3 | −30 / 0 / +30 |
| 4 | −45 / −15 / +15 / +45 |
| 5 | −60 / −30 / 0 / +30 / +60 |

Eine ungerade Anzahl setzt einen Zahn auf die Mitte. Eine gerade Anzahl setzt dort eine Lücke.

## Die Zähne entlang der Linie verschieben

Zwei Wege:

- Einen Wert in **Verschiebung** eintippen. Ein positiver Wert schiebt die Zähne zum Endpunkt der Linie, ein
  negativer Wert zum Startpunkt. 0 heißt mittig.
- Die drei Schaltflächen in der Zeile **Verschieben** benutzen:

  | Schaltfläche | Wirkung |
  |---|---|
  | **Nach links (Richtung Startpunkt)** | schiebt die Zähne um eine **Schrittweite** zum Startpunkt |
  | **Zentrieren** | setzt **Verschiebung** zurück auf 0 |
  | **Nach rechts (Richtung Endpunkt)** | schiebt die Zähne um eine **Schrittweite** zum Endpunkt |

Die Schaltflächen halten dort an, wo die Zähne nicht mehr auf die Linie passen würden. Bei mehreren Linien bestimmt
die kürzeste Linie diese Grenze. Ein eingetippter Wert wird nicht berichtigt: Ist er zu groß, ist OK ausgegraut.

**Verschiebung** beginnt bei jedem Öffnen des Dialogs bei 0.

## Wählen, welches Teil Material abgibt

Der Spalt muss irgendwoher kommen. Die Liste **Die Linie ist** entscheidet das:

| Eintrag | Kante der Tasche | Kante des Zapfens | Geeignet, wenn |
|---|---|---|---|
| **Mittellinie - halbe Toleranz je Seite** | rückt um die halbe Toleranz nach außen | rückt um die halbe Toleranz nach innen | beide Teile gleich bleiben sollen |
| **Kante der Tasche - Toleranz ganz beim Zapfen** | genau auf der gezeichneten Form | rückt um die volle Toleranz nach innen | das Teil mit den Taschen sein genaues Maß behalten muss |
| **Kante des Zapfens - Toleranz ganz bei der Tasche** | rückt um die volle Toleranz nach außen | genau auf der gezeichneten Form | das Teil mit den Zapfen sein genaues Maß behalten muss |

Der Spalt zwischen den Teilen ist in allen drei Fällen die volle Toleranz.

Beispiel mit einer Toleranz von 0,25 mm:

| Eintrag | Tasche | Zapfen | Spalt |
|---|---|---|---|
| Mittellinie | +0,125 mm | −0,125 mm | 0,25 mm |
| Kante der Tasche | 0 | −0,25 mm | 0,25 mm |
| Kante des Zapfens | +0,25 mm | 0 | 0,25 mm |

## Die Zähne auf die andere Seite setzen

Den Haken bei **Richtung umkehren** setzen.

Ohne den Haken stehen die Zähne auf der linken Seite der Linie, wenn man von ihrem Startpunkt zu ihrem Endpunkt
blickt (in der X/Y-Ebene der Skizze). Mit dem Haken stehen sie auf der rechten Seite.

Bei mehreren Linien folgt jede Linie ihrer eigenen Richtung. Linien, die in entgegengesetzter Richtung gezeichnet
wurden, bekommen ihre Zähne auf entgegengesetzten Seiten. **Richtung umkehren** dreht sie alle gemeinsam um.

## Mehrere Linien auf einmal

1. Mehrere Linien wählen, bevor der Befehl gestartet wird. Oder den Befehl starten und die Linien nacheinander
   anklicken. Bis zu 100 Linien sind möglich.
2. Die Werte einmal einstellen.
3. **OK** drücken.

Jede Linie bekommt aus denselben Werten ihre eigene Verbindung. Jede Linie wird für sich gemessen, und ihre Zähne
werden auf ihre eigene Mitte ausgerichtet. Die Linien dürfen verschieden lang sein.

Die Werte müssen auf jede Linie passen. Ist eine Linie zu kurz, wird gar nichts gezeichnet und OK ist ausgegraut.
Zuerst die kürzeste Linie ansehen; ihr geht als erster der Platz aus.

Nur gerade Skizzenlinien lassen sich wählen. Bögen, Kreise und Splines nicht.

## Zwei gleiche Teile: Geometrie spiegeln

Den Haken bei **Geometrie spiegeln** setzen.

Die Hälfte der Zähne zeigt dann zur einen Seite und die andere Hälfte zur anderen. Wird das Band um 180 Grad um die
Mitte der Linie gedreht, fällt es auf sich selbst. Beide Teile des Schnitts sind deshalb gleich. Es reicht, ein Teil
zu modellieren und es zweimal herzustellen; das zweite wird umgedreht.

Der Dialog stellt drei Dinge selbst ein, weil jedes von ihnen die Symmetrie stören würde:

| Was | Warum |
|---|---|
| **Anzahl** wird auf die nächste gerade Zahl erhöht | Ein Zahn auf der Mitte müsste in beide Richtungen zugleich zeigen. |
| **Die Linie ist** wird auf die Mittellinie gesetzt und ausgegraut | Nur dort geben beide Teile gleich viel ab. |
| **Verschiebung** wird auf 0 gesetzt; **Verschiebung**, **Schrittweite** und **Verschieben** werden ausgegraut | Eine verschobene Gruppe ist nicht mehr symmetrisch zur Mitte. |

Wird der Haken entfernt, werden die Felder wieder aktiv. Die Werte, die der Dialog geändert hat, bleiben, wie sie
sind.

Bei mehreren Linien wird jede Linie um ihre eigene Mitte gespiegelt.

## Die Originallinie behalten oder umwandeln

Beim Feld **Originallinie in Konstruktionslinie umwandeln** ist der Haken als Vorgabe gesetzt.

- Haken gesetzt: Die gewählte Linie wird bei OK zur Konstruktionslinie. Sie behält ihre Bemaßungen und
  Abhängigkeiten, teilt das Band aber nicht mehr in zwei Flächen.
- Haken nicht gesetzt: Die Linie bleibt eine normale Linie. Sie läuft durch das Band und teilt es in zwei Flächen
  (Profile).

Eine Linie, die schon Konstruktionslinie ist, bleibt, wie sie ist.

## Vorschau

Solange der Dialog offen ist, zeichnet das Add-in das Band nach jeder Änderung als Vorschau.

- Die Vorschau ändert die Originallinie nie. Deshalb zeigt die Vorschau die Linie noch als normale Linie.
- Passen die Werte nicht, wird keine Vorschau gezeigt.

## Den Befehl noch einmal ausführen

Fusion kann den Befehl mit seiner eigenen Funktion „letzten Befehl wiederholen“ wiederholen; das Add-in erlaubt das.
Der Dialog öffnet sich wieder mit den Werten des letzten erfolgreichen Laufs. Siehe
[settings.md](settings.md#was-gemerkt-wird).
