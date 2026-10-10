# Fehlerbehebung

## OK ist ausgegraut

Der Dialog graut **OK** aus und zeigt keine Vorschau, wenn die Werte nicht passen. **Er sagt nicht, warum.** Die
Meldungstexte unten gibt es im Add-in, sie werden aber nur in einem Meldungsfenster gezeigt, wenn der Lauf selbst
nach OK scheitert.

Diese Liste von oben nach unten durchgehen:

1. Steht unter **Linien** mindestens eine Linie?
2. Sind **Breite (Basis)**, **Tiefe** und **Toleranz** alle größer als 0?
3. Ist **Toleranz** kleiner als die Hälfte von **Breite (Basis)**?
4. Trapez: Liegt **Flankenwinkel** zwischen −89 und 89 Grad? Bei einem negativen Winkel: Ist die Spitze noch
   breiter als 0?
5. Zwei oder mehr Zähne: Ist **Abstand (Mitte-Mitte)** groß genug? Die Formel steht in
   [settings.md](settings.md#abstand-mitte-mitte).
6. Ist die Linie lang genug für alle Zähne? Bei mehreren Linien zuerst die kürzeste prüfen.
7. Wurde eine **Verschiebung** eingetippt? Die Schaltfläche **Zentrieren** in der Zeile **Verschieben** drücken, um
   sie auf 0 zurückzusetzen.
8. Dreieck oder sehr spitzer Zahn: **Toleranz** verkleinern, **Tiefe** verkleinern oder **Breite (Basis)**
   vergrößern.
9. Schmale Trapezspitze mit großer Toleranz: **Toleranz** verkleinern oder **Flankenwinkel** ändern.

Tipp: Immer nur einen Wert ändern. Der zuletzt geänderte Wert ist der erste Verdächtige.

## Meldungen zu den Werten

Alle Meldungsfenster tragen den Titel „Schwalbenschwanz“. `{0}`, `{1}` und `{2}` in der Tabelle stehen für Zahlen
oder Texte, die das Add-in einsetzt. Längen in Meldungen sind in Millimetern angegeben.

| Meldung | Ursache | Was zu tun ist |
|---|---|---|
| „Bitte mindestens eine Skizzenlinie wählen.“ | Der Lauf wurde ohne Linie unter **Linien** gestartet. | Mindestens eine gerade Skizzenlinie anklicken. |
| „Linie {0} von {1}: {2}“ | Mehrere Linien sind gewählt und eine davon verträgt die Werte nicht. {0} ist die Stelle dieser Linie in der Reihenfolge, in der sie gewählt wurden, {1} die Zahl der Linien, {2} die eigentliche Meldung. | Die Meldung hinter dem Doppelpunkt lesen und in dieser Tabelle nachschlagen. Die Werte ändern oder diese Linie aus der Auswahl nehmen. |
| „Die gewählte Linie hat keine Länge.“ | Startpunkt und Endpunkt der Linie liegen auf derselben Stelle (flach in der Skizze gesehen). | Eine andere Linie wählen oder sie verlängern. |
| „Die Breite muss größer als 0 sein.“ | **Breite (Basis)** ist 0 oder negativ. | Eine Breite über 0 eingeben. |
| „Die Tiefe muss größer als 0 sein.“ | **Tiefe** ist 0 oder negativ. | Eine Tiefe über 0 eingeben. |
| „Ein geschlossenes Band braucht eine Toleranz größer als 0.“ | **Toleranz** ist 0 oder negativ. Das Band besteht aus dem Spalt; ohne Spalt gibt es kein Band. | Eine Toleranz über 0 eingeben. |
| „Gespiegelte Geometrie braucht eine gerade Anzahl Zähne.“ | **Geometrie spiegeln** ist an und **Anzahl** ist ungerade. Der Dialog berichtigt das normalerweise selbst. | Eine gerade Anzahl einstellen. |
| „Gespiegelte Geometrie geht nur mit der Mittellinie, weil nur dort beide Teile gleich viel abgeben.“ | **Geometrie spiegeln** ist an und **Die Linie ist** steht nicht auf der Mittellinie. Der Dialog berichtigt das normalerweise selbst. | „Mittellinie - halbe Toleranz je Seite“ wählen oder das Spiegeln ausschalten. |
| „Gespiegelte Geometrie braucht die Verschiebung auf 0, sonst liegt das Muster nicht mehr symmetrisch zur Linienmitte.“ | **Geometrie spiegeln** ist an und **Verschiebung** ist nicht 0. Der Dialog berichtigt das normalerweise selbst. | Die Verschiebung auf 0 setzen oder das Spiegeln ausschalten. |
| „Es wird mindestens ein Schwalbenschwanz gebraucht.“ | **Anzahl** ist kleiner als 1. Das Dialogfeld lässt das nicht zu. | Eine Anzahl von 1 oder mehr einstellen. |
| „Der Flankenwinkel muss zwischen -89 und 89 Grad liegen.“ | Trapez: **Flankenwinkel** ist 89 Grad oder mehr, oder −89 Grad oder weniger. | Einen Winkel innerhalb dieses Bereichs eingeben. |
| „Flankenwinkel zu steil negativ - der Zahn läuft auf 0 zu.“ | Trapez mit negativem Winkel: Die Seiten treffen sich, bevor die Spitze erreicht ist. | Einen weniger negativen Winkel, weniger Tiefe oder mehr Breite nehmen. |
| „Der Abstand muss größer als 0 sein.“ | Zwei oder mehr Zähne und **Abstand (Mitte-Mitte)** ist 0 oder negativ. | Einen Abstand über 0 eingeben. |
| „Der Abstand ist zu klein - die Schwalbenschwänze würden sich überschneiden. Nötig sind mindestens {0} mm.“ | Zwei oder mehr Zähne stehen zu dicht. {0} ist der Mindestabstand für die eingestellten Werte. | Mindestens den genannten Abstand eingeben oder Breite, Flankenwinkel oder Toleranz verkleinern. |
| „Die Verschiebung schiebt die Verzahnung über das Linienende hinaus. Möglich sind höchstens +/- {0} mm.“ | **Verschiebung** ist größer, als die Linie erlaubt. {0} ist die größte mögliche Verschiebung. | Die Verschiebung auf den genannten Wert verkleinern oder **Zentrieren** drücken. |
| „Die Verzahnung ist breiter als die gewählte Linie ({0} mm). Anzahl, Breite oder Abstand verkleinern.“ | Die Zähne samt dem Abstand zu den Linienenden passen nicht auf die Linie. {0} ist die Länge der Linie. Derselbe Text erscheint, wenn eine Kontur über ein Ende der Linie hinauslaufen würde. | **Anzahl**, **Breite (Basis)** oder **Abstand (Mitte-Mitte)** verkleinern oder eine längere Linie nehmen. |
| „Die Toleranzkontur läuft an einer spitzen Ecke aus dem Ruder. Zahn flacher machen (kleinere Tiefe / größere Breite) oder die Toleranz verringern.“ | An einer sehr spitzen Ecke würde die versetzte Kontur weit vom Zahn wegschießen (mehr als das 12-Fache der Versatzstrecke). | Weniger Tiefe, mehr Breite oder weniger Toleranz. |
| „Die Toleranz frisst den Zahn komplett auf. Toleranz verkleinern oder Tiefe vergrößern.“ | Nach Abzug der Toleranz bleibt vom Zahn nichts übrig, oder ein Stück der Kontur schrumpft auf nichts, oder die Kontur würde sich selbst kreuzen. | **Toleranz** verkleinern oder **Tiefe** vergrößern. Bei einer schmalen Trapezspitze auch eine größere Breite oder einen anderen Flankenwinkel versuchen. |
| „Die Toleranz ist im Verhältnis zur Tiefe zu groß.“ | Weniger als 5 % von **Tiefe** bleiben als Zahnhöhe übrig. | **Toleranz** verkleinern oder **Tiefe** vergrößern. |
| „Die Toleranz ist im Verhältnis zur Breite zu groß.“ | Die doppelte **Toleranz** ist so groß wie **Breite (Basis)** oder größer. | **Toleranz** verkleinern oder **Breite (Basis)** vergrößern. |
| „Die Kontur ist entartet.“ | Ein Sicherheitsnetz: Der Umriss hat zu wenige Punkte, oder die beiden Konturen haben nicht gleich viele Punkte. Solange die anderen Prüfungen greifen, sollte das im normalen Gebrauch nicht erscheinen. | Die Werte leicht ändern. Erscheint es wieder, mit den benutzten Werten melden. |

## Meldungen zum Programm

Diese Meldungen enthalten anstelle von `{0}` einen technischen Fehlerbericht (einen „Traceback“). Sie bedeuten
einen unerwarteten Fehler, keinen falschen Wert.

| Meldung | Wann | Was zu tun ist |
|---|---|---|
| „Kein passendes Toolbar-Panel gefunden.“ | Beim Start. Keiner der drei Orte in der Werkzeugleiste ist in diesem Fusion vorhanden (siehe [installation.md](installation.md#erster-start-in-fusion)). Die Schaltfläche wird nicht angelegt. | Fusion aktualisieren. Bleibt die Meldung, sie zusammen mit der Fusion-Version melden. |
| „Fehler beim Erzeugen der Geometrie: {0}“ | Nach OK trat beim Zeichnen ein unerwarteter Fehler auf. Der Lauf wird Fusion als gescheitert gemeldet. | Die Skizze prüfen; Undo (Rückgängig) benutzen, falls Linien zurückgeblieben sind. Noch einmal versuchen. Wiederholt es sich, den ganzen Text melden. |
| „Fehler beim Aufbau des Dialogs: {0}“ | Der Dialog ließ sich beim Klick auf die Schaltfläche nicht aufbauen. | Das Add-in stoppen und starten. Prüfen, ob die Ordner `lang` und `resources` vollständig sind. Wiederholt es sich, den ganzen Text melden. |
| „Start fehlgeschlagen: {0}“ | Das Add-in konnte nicht starten. | Prüfen, ob der Ordner vollständig entpackt ist und `Dovetail` heißt. Neu installieren. Wiederholt es sich, den ganzen Text melden. |
| „Stopp fehlgeschlagen: {0}“ | Das Add-in ließ sich nicht sauber stoppen. | Fusion neu starten. |

Meldungen: <https://github.com/sorglos-it/fusion360/issues>

## Andere Probleme

| Problem | Ursache | Was zu tun ist |
|---|---|---|
| Keine Schaltfläche nach dem Installieren | Das Add-in läuft nicht, oder der Ordner liegt eine Ebene zu tief | [installation.md](installation.md) noch einmal befolgen; prüfen, ob es `AddIns/Dovetail/Dovetail.py` gibt |
| Eine Linie lässt sich im Dialog nicht anklicken | Nur gerade Skizzenlinien werden angenommen | Eine gerade Linie nehmen; Bögen, Kreise und Splines werden nicht unterstützt |
| Das Band zeigt zwei Flächen statt einer | Die Originallinie läuft noch als normale Linie durch das Band | Den Haken bei **Originallinie in Konstruktionslinie umwandeln** setzen oder die Linie von Hand in eine Konstruktionslinie umwandeln |
| Die Vorschau zeigt die Originallinie noch als normale Linie | Die Vorschau ändert die Originallinie nie | Nichts; die Linie wird bei OK umgewandelt |
| Die Zähne sind auf der falschen Seite | Die Seite hängt von der Richtung ab, in der die Linie gezeichnet wurde | Den Haken bei **Richtung umkehren** setzen |
| Manche Linien haben die Zähne auf der einen Seite, manche auf der anderen | Die Linien wurden in entgegengesetzter Richtung gezeichnet | Den Befehl für die beiden Gruppen getrennt ausführen, einmal mit und einmal ohne **Richtung umkehren** |
| Die Schaltflächen von **Verschieben** tun nichts | **Schrittweite** ist 0, oder die Grenze ist erreicht, oder **Geometrie spiegeln** ist an | Eine Schrittweite einstellen oder den Platz auf der Linie prüfen |
| **Verschiebung**, **Die Linie ist**, **Schrittweite** sind ausgegraut | Bei **Geometrie spiegeln** ist der Haken gesetzt | Den Haken entfernen |
| Die falsche Sprache wird gezeigt | Die Sprache wird beim Start des Add-ins gewählt; andere Sprachen als die fünf unterstützten fallen auf Englisch zurück | Siehe [settings.md](settings.md#sprache) |
| Die Werte stehen wieder auf den Vorgaben | Sie werden nur gemerkt, solange Fusion läuft | Sie noch einmal eingeben |

## Bekannte Grenzen

- **Ist OK ausgegraut, wird kein Grund gezeigt.** Die Meldungstexte werden nur gezeigt, wenn der Lauf selbst
  scheitert.
- **Die Höhe wird nicht beachtet.** Linien in einer 3D-Skizze oder Linien außerhalb der Skizzenebene werden
  behandelt, als wären sie flach.
- **Nur gerade Linien.** Bögen, Kreise und Splines lassen sich nicht wählen.
- **Ein Satz Werte für alle Linien.** Bei mehreren Linien bekommt jede Linie dieselben Werte. Eine Einstellung je
  Linie gibt es nicht.
- **Höchstens 100 Linien und 500 Zähne je Linie.**
- **Ein Dreieck hakt nicht ein.** Nur das Trapez mit positivem Flankenwinkel hält gegen Auseinanderziehen.
- **Die Toleranz ist ein Spalt, mehr nicht.** Das Add-in gleicht keine Einflüsse des Fertigungsverfahrens aus.
- **In Fusion nicht bestätigt:** die Geometrie-Änderungen der Version 1.1.0.0 (Abstand von den Linienenden,
  größerer Mindestabstand, Ablehnen von Konturen, die sich selbst kreuzen, Zurücknehmen nach einem gescheiterten
  Lauf). Sie wurden nur offline geprüft.
