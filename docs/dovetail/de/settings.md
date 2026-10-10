# Einstellungen

Das Add-in hat keine Einstellungsdatei und keine Einstellungsseite. Alles wird im Dialog des Befehls eingestellt.
Die Felder stehen hier in der Reihenfolge, in der der Dialog sie zeigt.

## Dialogfelder

| Feld | Bedeutung | Vorgabe | Erlaubte Werte |
|---|---|---|---|
| **Linien** | Die Skizzenlinien, die eine Verbindung bekommen. Aufforderungstext: „Eine oder mehrere Skizzenlinien wählen“. | die Linien, die vor dem Start des Befehls gewählt waren | 1 bis 100 gerade Skizzenlinien |
| **Anzahl** | Zahl der Zähne je Linie | 1 | ganze Zahl, 1 bis 500 |
| **Geometrie spiegeln** | Macht beide Teile gleich, siehe [usage.md](usage.md#zwei-gleiche-teile-geometrie-spiegeln) | aus | an / aus |
| **Form** | Form des Zahns | Trapez (Schwalbenschwanz) | Trapez (Schwalbenschwanz), Dreieck, Rechteck (Fingerzinken) |
| **Breite (Basis)** | Breite des Zahns dort, wo er auf die Linie trifft | 10 mm | größer als 0 und größer als die doppelte Toleranz |
| **Tiefe** | Wie weit der Zahn von der Linie absteht | 6 mm | größer als 0 |
| **Flankenwinkel** | Nur Trapez: wie stark sich jede Seite des Zahns nach außen neigt | 15 Grad | mehr als −89 und weniger als 89 Grad; siehe unten |
| **Abstand (Mitte-Mitte)** | Strecke von der Mitte eines Zahns zur Mitte des nächsten. Wird nur bei 2 oder mehr Zähnen benutzt. | 20 mm | größer als 0 und mindestens der Mindestabstand, siehe unten |
| **Verschiebung** | Verschiebung der ganzen Gruppe von Zähnen entlang der Linie. Positiv: zum Endpunkt. | 0 mm, jedes Mal | zwischen minus und plus der größten Verschiebung, siehe unten |
| **Schrittweite** | Wie weit ein Klick auf eine Schaltfläche von **Verschieben** die Zähne schiebt | 1 mm | vom Add-in nicht geprüft, siehe unten |
| **Verschieben** | Drei Schaltflächen: **Nach links (Richtung Startpunkt)**, **Zentrieren**, **Nach rechts (Richtung Endpunkt)** | – | – |
| **Toleranz** | Spalt zwischen den beiden Teilen | 0,25 mm | größer als 0; weitere Grenzen unten |
| **Die Linie ist** | Welches Teil Material für den Spalt abgibt | Mittellinie - halbe Toleranz je Seite | die drei unten genannten Einträge |
| **Richtung umkehren** | Setzt die Zähne auf die andere Seite der Linie | aus | an / aus |
| **Originallinie in Konstruktionslinie umwandeln** | Wandelt die gewählte Linie bei OK in eine Hilfslinie um | an | an / aus |

Einträge von **Die Linie ist**:

| Eintrag | Tasche wächst um | Zapfen schrumpft um |
|---|---|---|
| **Mittellinie - halbe Toleranz je Seite** | die halbe Toleranz | die halbe Toleranz |
| **Kante der Tasche - Toleranz ganz beim Zapfen** | nichts | die volle Toleranz |
| **Kante des Zapfens - Toleranz ganz bei der Tasche** | die volle Toleranz | nichts |

## Felder, die ausgegraut sind

| Feld | Ausgegraut, wenn |
|---|---|
| **Flankenwinkel** | **Form** nicht Trapez (Schwalbenschwanz) ist. Der Wert wird dann nicht beachtet. |
| **Abstand (Mitte-Mitte)** | **Anzahl** 1 ist. Der Wert wird dann nicht beachtet. |
| **Die Linie ist**, **Verschiebung**, **Schrittweite**, **Verschieben** | bei **Geometrie spiegeln** der Haken gesetzt ist |

## Grenzen im Einzelnen

Alle Grenzen stammen aus dem Code. Längen sind unten in Millimetern angegeben.

Die „halbe Spitzenbreite“ kommt in mehreren Grenzen vor. Sie hängt von der Form ab:

| Form | Halbe Spitzenbreite |
|---|---|
| Rechteck (Fingerzinken) | Breite ÷ 2 |
| Dreieck | 0 |
| Trapez (Schwalbenschwanz) | Breite ÷ 2 + Tiefe × tan(Flankenwinkel) |

Die „breiteste Hälfte“ ist der größere Wert von Breite ÷ 2 und der halben Spitzenbreite.

### Flankenwinkel

- Muss mehr als −89 und weniger als 89 Grad betragen. Genau 89 oder −89 wird abgelehnt.
- Bei einem negativen Winkel wird die Spitze schmaler. Die halbe Spitzenbreite muss über 0 bleiben. Sonst würde der
  Zahn auf nichts zulaufen und wird abgelehnt.
- 0 Grad ergibt ein Rechteck.

### Abstand (Mitte-Mitte)

Wird nur bei 2 oder mehr Zähnen geprüft.

Mindestabstand = 2 × breiteste Hälfte + 2 × Toleranz + 0,01 mm

Beispiel mit den Vorgaben (Breite 10 mm, Tiefe 6 mm, Flankenwinkel 15 Grad, Toleranz 0,25 mm):
Die halbe Spitzenbreite beträgt etwa 6,61 mm, der Mindestabstand also etwa 13,73 mm.

### Platz auf der Linie

Die Zähne müssen von beiden Enden der Linie Abstand halten: die Toleranz plus 0,01 mm.

Nötige Länge = (Anzahl − 1) × Abstand + 2 × breiteste Hälfte + 2 × (Toleranz + 0,01 mm)

Beispiel mit den Vorgaben und einem Zahn: Es werden etwa 13,74 mm Linie gebraucht.

### Verschiebung

Größte Verschiebung = Linienlänge ÷ 2 − ( (Anzahl − 1) ÷ 2 × Abstand + breiteste Hälfte + Toleranz + 0,01 mm )

- Die Verschiebung darf zwischen minus und plus diesem Wert liegen.
- Die Schaltflächen von **Verschieben** halten bei diesem Wert an. Bei mehreren Linien entscheidet die kürzeste
  Linie.
- Eine eingetippte Verschiebung wird nicht berichtigt. Ist sie zu groß, ist OK ausgegraut.
- Mit **Geometrie spiegeln** muss die Verschiebung 0 sein.

### Toleranz

- Muss größer als 0 sein. Das Band besteht aus dem Spalt; bei 0 gibt es kein Band.
- Die doppelte Toleranz muss kleiner sein als **Breite (Basis)**.
- Nach Abzug der Toleranz müssen mindestens 5 % von **Tiefe** als Zahnhöhe übrig bleiben. Das zählt vor allem bei
  spitzen Zähnen, bei denen die Spitze mehr Höhe verliert als die Toleranz.
- Das Band darf sich nicht selbst kreuzen, und keines seiner Stücke darf auf nichts schrumpfen. Das kann bei
  schmalen Trapezspitzen und großer Toleranz vorkommen.
- An einer spitzen Ecke darf die versetzte Ecke nicht weiter wegrücken als das 12-Fache des Versatzabstands.

### Anzahl

- 1 bis 500.
- Mit **Geometrie spiegeln** muss die Anzahl gerade sein. Der Dialog erhöht eine ungerade Anzahl um 1.

### Schrittweite

Das Add-in prüft diesen Wert nicht. Aus dem Code: Bei 0 tun die Schaltflächen von **Verschieben** nichts; ein
negativer Wert kehrt die Richtung der linken und der rechten Schaltfläche um.

### Linien

- Nur gerade Skizzenlinien lassen sich wählen.
- Mindestens 1, höchstens 100.
- Eine Linie muss eine Länge größer als 0 haben.

## Einheiten

- Längenfelder werden in Millimetern gezeigt, der Winkel in Grad.
- Zahlen in Fehlermeldungen stehen immer in Millimetern mit zwei Nachkommastellen.
- Im Inneren rechnet das Add-in in Zentimetern und im Bogenmaß, den Einheiten, die Fusion intern benutzt.

## Was gemerkt wird

Das Add-in merkt sich die Werte des letzten Laufs, der mit **OK** beendet wurde und gelungen ist.

| Gemerkt | Nicht gemerkt |
|---|---|
| Anzahl | Linien |
| Geometrie spiegeln | Verschiebung (beginnt immer bei 0) |
| Form | |
| Breite (Basis) | |
| Tiefe | |
| Flankenwinkel | |
| Abstand (Mitte-Mitte) | |
| Schrittweite | |
| Toleranz | |
| Die Linie ist | |
| Richtung umkehren | |
| Originallinie in Konstruktionslinie umwandeln | |

Wie lange:

- Die Werte stehen nur im Arbeitsspeicher. Auf den Datenträger wird nichts geschrieben.
- Sie halten für die laufende Fusion-Sitzung. Nach dem Schließen von Fusion gelten wieder die Vorgaben aus der
  Tabelle oben.
- Das Schließen des Dialogs mit Cancel (Abbrechen) ändert die gemerkten Werte nicht.

Die Verschiebung ist mit Absicht ausgenommen: Sie gehört zur gerade bearbeiteten Linie, nicht zu den Einstellungen.

## Sprache

Das Add-in hat Texte in fünf Sprachen: Deutsch, Englisch, Spanisch, Französisch, Italienisch.

Die Sprache wird einmal gewählt, wenn das Add-in startet:

1. Die in den Voreinstellungen von Fusion eingestellte Sprache (Benutzersprache) wird genommen, wenn sie eine der
   fünf ist.
2. Wenn nicht, sieht das Add-in in den Umgebungsvariablen `LANG`, `LANGUAGE` und `LC_ALL` nach, in dieser
   Reihenfolge.
3. Ergibt das nichts, sieht es nach der Sprache des Betriebssystems.
4. Ergibt auch das nichts, wird Englisch genommen.

Im Dialog gibt es keinen Sprachumschalter. Nach einer Änderung der Sprache in Fusion muss das Add-in neu gestartet
werden (ein Neustart von Fusion erledigt das).

Fehlt in einer Sprachdatei ein einzelner Text, wird stattdessen der englische Text gezeigt.
