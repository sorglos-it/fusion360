# Einstellungen

Das Add-in hat keine Einstellungsdatei und keine Einstellungsseite. Alles wird im Dialog des Befehls **Skizzenraster** eingestellt. Die Feldnamen stehen genau so da wie im deutschen Dialog.

## Dialogfelder

Längen werden als Vorgabe in Millimetern eingegeben (die Felder werden mit der Einheit `mm` angelegt). „Keine Grenze“ heißt: Das Add-in selbst prüft nichts weiter.

| Feld | Bedeutung | Vorgabe | Erlaubte Werte |
| --- | --- | --- | --- |
| **Punkt** | Der Skizzenpunkt, um den das Raster gebaut wird. | Der Skizzenpunkt, der vor dem Öffnen des Dialogs gewählt war, sonst leer | Genau ein Skizzenpunkt. Andere Objekte lassen sich nicht wählen. |
| **Anzahl aus** | Wie die Zahl der Formen festgelegt wird. | Spalten und Zeilen | **Spalten und Zeilen**, **Fläche füllen** |
| **Form** | Die Form, die wiederholt wird. | Rechteck | **Rechteck**, **Kreis / Ellipse**, **Langloch**, **Vieleck** |
| **Ecken** | Zahl der Seiten des Vielecks. | 6 | Ganze Zahl, 3 bis 24 |
| **Regelmäßig** | Ankreuzfeld. An: Alle Seiten des Vielecks sind gleich lang. Aus: Das Vieleck wird auf Länge × Tiefe gestreckt. | aus | an, aus |
| **Eckenform** | Was mit den vier Ecken des Rechtecks geschieht. | Scharfkantig | **Scharfkantig**, **Verrundet**, **Gefast** |
| **Radius / Fase** | Radius der Rundung oder Länge des Schnitts an jeder Kante. | 1 mm | Größer als 0, höchstens die Hälfte des kleineren Werts von Länge und Tiefe |
| **Länge (X)** | Größe einer Form in X. | 10 mm | Größer als 0, keine Obergrenze |
| **Tiefe (Y)** | Größe einer Form in Y. | 5 mm | Größer als 0, keine Obergrenze |
| **Abstand X** | Freier Raum zwischen Nachbarn in X. | 2 mm | 0 oder größer, keine Obergrenze |
| **Abstand Y** | Freier Raum zwischen Nachbarn in Y. | 2 mm | 0 oder größer, keine Obergrenze |
| **Spalten** | Zahl der Formen nebeneinander. | 8 | Ganze Zahl, 1 bis 2000 |
| **Zeilen** | Zahl der Formen übereinander. | 4 | Ganze Zahl, 1 bis 2000 |
| **Breite der Fläche** | Breite der Fläche, die gefüllt wird. | 100 mm | Größer als 0 und groß genug für eine Form |
| **Höhe der Fläche** | Höhe der Fläche, die gefüllt wird. | 40 mm | Größer als 0 und groß genug für eine Form |
| **Punkt liegt im Raster** | Wo der gewählte Punkt im fertigen Raster liegt. | In der Mitte | Neun Einträge, siehe unten |
| **Versatz X** | Verschiebt das ganze Raster in X, zusätzlich zu der oben gewählten Lage. | 0 mm | Jeder Wert, auch negativ |
| **Versatz Y** | Verschiebt das ganze Raster in Y. | 0 mm | Jeder Wert, auch negativ |
| **Ergebnis** | Zeigt die Zahl der Formen und die Gesamtgröße oder eine Meldung. | – | Nur zum Lesen |

Eine weitere Grenze gilt für das ganze Raster: Spalten × Zeilen darf nicht mehr als **2000** sein. Das gilt in beiden Zählarten.

## Wann ein Feld gezeigt wird

| Feld | Gezeigt, wenn |
| --- | --- |
| **Ecken**, **Regelmäßig** | **Form** auf **Vieleck** steht |
| **Eckenform** | **Form** auf **Rechteck** steht |
| **Radius / Fase** | **Form** auf **Rechteck** steht und **Eckenform** nicht auf **Scharfkantig** |
| **Spalten**, **Zeilen** | **Anzahl aus** auf **Spalten und Zeilen** steht |
| **Breite der Fläche**, **Höhe der Fläche** | **Anzahl aus** auf **Fläche füllen** steht |
| alle anderen Felder | immer |

Ein ausgeblendetes Feld behält seinen Wert. Ein ausgeblendeter Wert wird nicht benutzt und nicht geprüft.

## Punkt liegt im Raster

| Eintrag | Der Punkt liegt auf |
| --- | --- |
| **In der Mitte** | dem Mittelpunkt des Rasters |
| **Unten links** | der unteren linken Ecke |
| **Unten rechts** | der unteren rechten Ecke |
| **Oben links** | der oberen linken Ecke |
| **Oben rechts** | der oberen rechten Ecke |
| **Unten mittig** | der Mitte der unteren Kante |
| **Oben mittig** | der Mitte der oberen Kante |
| **Links mittig** | der Mitte der linken Kante |
| **Rechts mittig** | der Mitte der rechten Kante |

„Raster“ meint hier das kleinste Rechteck um alle Formen. Links und rechts liegen entlang der X-Achse der Skizze, unten und oben entlang ihrer Y-Achse.

## Hilfetexte im Dialog

An Feldern hängen drei Hilfetexte (Tooltips):

| Feld | Text |
| --- | --- |
| **Regelmäßig** | „Hält das Vieleck gleichseitig, statt es auf Länge × Tiefe zu strecken. Die kleinere der beiden bestimmt dann die Größe, und die Teilung folgt der tatsächlichen Form - der Abstand stimmt so oder so.“ |
| **Eckenform**, **Radius / Fase** | „Nimmt die vier rechten Winkel des Rechtecks weg, entweder als Rundung oder als gerade Fase. Höchstens die Hälfte der kürzeren Kante - genau dieser Radius macht aus dem Rechteck ein Langloch, diese Fase eine Raute. Die Hüllkontur ändert sich nicht, Anzahl, Teilung und Abstand bleiben also, wie sie sind.“ |
| **Versatz X**, **Versatz Y** | „Verschiebt das ganze Raster gegenüber dem gewählten Punkt, zusätzlich zum Bezugspunkt. Damit hältst du einen Rand zu einer Kante ein, ohne den Punkt selbst zu versetzen. Negative Werte gehen in die andere Richtung.“ |

Hinweis zum zweiten Text: Eine Fase von genau der Hälfte der kürzeren Kante ergibt nur dann eine Raute, wenn Länge und Tiefe gleich sind. Bei ungleichen Werten ergibt sie eine sechseckige Form.

Die Schaltfläche selbst hat den Hilfetext: „Baut ein Raster aus Formen um einen Skizzenpunkt. Feste Anzahl Spalten und Zeilen, oder so viele wie in eine Fläche passen.“

## Was gemerkt wird

- Wird ein Raster mit **OK** abgeschlossen, merkt sich das Add-in alle Werte außer dem Punkt: Zählart, Form, Ecken, Regelmäßig, Eckenform, Radius / Fase, Länge, Tiefe, beide Abstände, Spalten, Zeilen, Breite der Fläche, Höhe der Fläche, Lage des Punkts, beide Versätze.
- Beim nächsten Öffnen des Dialogs sind diese Werte eingetragen.
- Werte werden **nicht** gemerkt, wenn der Dialog abgebrochen wird oder wenn OK mit einer Fehlermeldung endet.
- Die Werte stehen nur im Arbeitsspeicher, nie auf dem Datenträger. Sie halten, bis das Add-in gestoppt oder Fusion geschlossen wird. Danach gelten wieder die Vorgaben aus der Tabelle oben.
- Die Werte sind für alle Dokumente gleich, die in dieser Fusion-Sitzung offen sind.

## Sprache

Das Add-in hat fünf Sprachen: Deutsch, Englisch, Spanisch, Französisch, Italienisch.

So wird die Sprache gewählt, in dieser Reihenfolge:

1. Die Sprache, die in Fusion unter **Preferences → General → User Language** eingestellt ist, wenn sie eine der fünf ist.
2. Sonst die Sprache des Betriebssystems, wenn sie eine der fünf ist. (Das Add-in liest die Umgebungsvariablen `LANG`, `LANGUAGE`, `LC_ALL`, dann die Spracheinstellung des Systems.)
3. Sonst Englisch.

Weitere Einzelheiten:

- Im Add-in gibt es keinen Sprachumschalter.
- Die Sprache wird einmal gelesen, wenn das Add-in startet. Nach einer Änderung der Sprache in Fusion das Add-in stoppen und starten oder Fusion neu starten.
- Fehlt in einer Sprache ein Text, wird stattdessen der englische Text gezeigt.
- Die Zeile **Ergebnis** zeigt immer Millimeter, in jeder Sprache.
