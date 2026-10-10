# Fehlerbehebung

Alle Texte sind aus der deutschen Sprachdatei übernommen. `{0}` und `{1}` stehen für Werte, die das Add-in einsetzt.

## Wo Meldungen erscheinen

| Ort | Wann |
| --- | --- |
| Zeile **Ergebnis** im Dialog | Ein Wert ist nicht erlaubt. **OK** ist zugleich gesperrt. |
| Gesperrtes **OK** ohne Text | Es ist kein Skizzenpunkt gewählt (siehe erste Zeile unten). |
| Meldungsfenster mit dem Titel **Skizzenraster** | Eine Prüfung scheitert erst in dem Augenblick, in dem **OK** gedrückt wird, oder etwas Unerwartetes ist schiefgegangen. |

## Meldungen zur Eingabe

| Meldung | Ursache | Was zu tun ist |
| --- | --- | --- |
| „Bitte genau einen Skizzenpunkt wählen.“ | **Punkt** ist leer, oder das gewählte Objekt ist kein Skizzenpunkt. Dieser Text wird normalerweise nicht gezeigt; **OK** ist einfach gesperrt. | **Punkt** anklicken und einen Skizzenpunkt wählen: den Ursprung der Skizze oder einen selbst gesetzten Punkt. Punkte auf Körpern lassen sich nicht wählen. |
| „Die Länge muss größer als 0 sein.“ | **Länge (X)** ist 0 oder negativ. | Einen Wert über 0 eingeben. |
| „Die Tiefe muss größer als 0 sein.“ | **Tiefe (Y)** ist 0 oder negativ. | Einen Wert über 0 eingeben. |
| „Der Abstand darf nicht negativ sein.“ | **Abstand X** oder **Abstand Y** ist kleiner als 0. | 0 oder mehr eingeben. Überlappende Formen sind nicht möglich. |
| „Es wird mindestens eine Spalte gebraucht.“ | **Spalten** ist kleiner als 1. | 1 oder mehr eingeben. Das Feld selbst nimmt nur 1 bis 2000 an, diese Meldung sollte also normalerweise nicht erscheinen. |
| „Es wird mindestens eine Zeile gebraucht.“ | **Zeilen** ist kleiner als 1. | 1 oder mehr eingeben. Das Feld selbst nimmt nur 1 bis 2000 an, diese Meldung sollte also normalerweise nicht erscheinen. |
| „Die Fläche muss in beiden Richtungen größer als 0 sein.“ | Betriebsart **Fläche füllen**: **Breite der Fläche** oder **Höhe der Fläche** ist 0 oder negativ. | In beiden Feldern Werte über 0 eingeben. |
| „In diese Fläche passt nicht einmal eine Form. Nötig sind mindestens {0} × {1} mm.“ | Betriebsart **Fläche füllen**: Die Fläche ist kleiner als eine Form. Die beiden Zahlen sind die Größe einer Form. | **Breite der Fläche** und **Höhe der Fläche** mindestens so groß machen wie die Zahlen in der Meldung, oder die Form verkleinern. |
| „Ein Vieleck braucht zwischen {0} und {1} Ecken.“ | **Ecken** liegt außerhalb von 3 bis 24. | 3 bis 24 eingeben. Das Feld selbst nimmt nur diesen Bereich an, diese Meldung sollte also normalerweise nicht erscheinen. |
| „Radius bzw. Fase muss größer als 0 sein.“ | **Eckenform** steht auf **Verrundet** oder **Gefast**, und **Radius / Fase** ist 0 oder negativ. | Einen Wert über 0 eingeben oder **Eckenform** auf **Scharfkantig** stellen. |
| „Radius bzw. Fase darf höchstens {0} mm betragen, die Hälfte der kürzeren Kante.“ | **Radius / Fase** ist größer als die Hälfte des kleineren Werts von **Länge (X)** und **Tiefe (Y)**. Die Zahl ist der größte erlaubte Wert. | Höchstens den Wert aus der Meldung eingeben oder das Rechteck vergrößern. |
| „Das wären {0} Formen. Erlaubt sind höchstens {1} - mehr legt Fusion lahm.“ | Spalten × Zeilen ist mehr als 2000. Die erste Zahl ist das, was die eingestellten Werte ergäben. | Weniger Spalten oder Zeilen nehmen. In der Betriebsart **Fläche füllen**: eine kleinere Fläche, größere Formen oder größere Abstände. Für mehr Formen mehrere Raster zeichnen. |

Sind mehrere Werte falsch, wird nur das erste Problem gezeigt. Es beheben, dann erscheint das nächste.

## Meldungen zum Add-in selbst

Diese erscheinen in einem Meldungsfenster. `{0}` wird durch einen technischen Fehlerbericht ersetzt (einen Python-Traceback).

| Meldung | Ursache | Was zu tun ist |
| --- | --- | --- |
| „Kein passendes Toolbar-Panel gefunden.“ | Beim Start fand das Add-in weder das Panel CREATE der Skizzen-Werkzeugleiste noch das Panel CREATE der Registerkarte SOLID. Es wird keine Schaltfläche angelegt. | In den Arbeitsbereich **Design** wechseln, dann das Add-in stoppen und wieder starten. Bleibt es dabei, mit der Fusion-Version melden. |
| „Fehler beim Erzeugen der Geometrie: {0}“ | Beim Zeichnen nach **OK** ist etwas Unerwartetes gescheitert. | Noch einmal versuchen. Bleibt es dabei, mit dem ganzen Text melden. |
| „Fehler beim Aufbau des Dialogs: {0}“ | Beim Aufbau des Dialogs ist etwas Unerwartetes gescheitert. | Das Add-in stoppen und wieder starten. Bleibt es dabei, mit dem ganzen Text melden. |
| „Start fehlgeschlagen: {0}“ | Beim Start des Add-ins ist etwas Unerwartetes gescheitert. | Prüfen, ob der Ordner vollständig ist und noch `SketchGrid` heißt (siehe [installation.md](installation.md)). Es wieder starten. |
| „Stopp fehlgeschlagen: {0}“ | Beim Stoppen des Add-ins ist etwas Unerwartetes gescheitert. | Fusion neu starten. |

Meldungen gehen an <https://github.com/sorglos-it/fusion360/issues>.

## Andere Probleme

| Problem | Ursache | Was zu tun ist |
| --- | --- | --- |
| **OK** ist grau und **Ergebnis** zeigt ein normales Ergebnis | Es ist kein Punkt gewählt. | In **Punkt** einen Skizzenpunkt wählen. |
| Der vorher angeklickte Punkt steht nicht im Dialog | Der Punkt konnte nicht übernommen werden. Seit Version 1.1.0.0 arbeitet der Dialog in diesem Fall weiter (nur offline geprüft, nicht in Fusion). | Den Punkt im Dialog wählen. |
| Keine Vorschau beim Tippen | Ein Wert ist in diesem Augenblick nicht erlaubt. Die Vorschau bleibt ohne Meldung leer. | Die Zeile **Ergebnis** lesen und den Wert berichtigen. |
| Die Schaltfläche fehlt | Das Add-in läuft nicht, oder es wurde kein Panel gefunden. | **Utilities → ADD-INS → Add-Ins** öffnen, **SketchGrid** wählen, **Run** drücken. |
| Die Schaltfläche zeigt eine alte Versionsnummer | Das alte Add-in ist noch im Speicher. | Das Add-in stoppen, den Ordner ersetzen, es wieder starten. |
| Der Dialog ist englisch, obwohl Fusion auf eine andere Sprache gestellt ist | Es gibt nur Deutsch, Englisch, Spanisch, Französisch und Italienisch. Oder die Sprache wurde geändert, während das Add-in lief. | Das Add-in stoppen und wieder starten. Siehe [settings.md](settings.md#sprache). |
| Ein Text erscheint als Schlüssel wie `in.point` | Die Sprachdateien fehlen oder sind beschädigt. | Das Add-in neu aus dem ZIP installieren. |
| Das Raster füllt die Fläche nicht | Es werden nur ganze Formen gezeichnet. | Das ist so gewollt. Siehe [usage.md](usage.md#fläche-füllen). |
| Ein regelmäßiges Vieleck ist viel kleiner als Länge × Tiefe | Mit **Regelmäßig** bestimmt der kleinere Wert von Länge und Tiefe die Größe. | Ähnliche Werte für Länge und Tiefe nehmen oder den Haken bei **Regelmäßig** entfernen. |
| Der Dialog startet wieder mit den Standardwerten | Gemerkte Werte halten nur, bis das Add-in stoppt oder Fusion schließt. | Sie noch einmal eingeben. |

## Bekannte Grenzen

In Fusion nicht bestätigt (bei einer Durchsicht des Codes gefunden):

- **Langlöcher und Rechtecke mit verrundeten oder gefasten Ecken** werden als getrennte Linien und Bögen gezeichnet. Ihre Enden liegen auf derselben Stelle, aber sie bleiben womöglich nicht verbunden, wenn ein Teil der Form gezogen wird. Vielecke und scharfkantige Rechtecke sind auf diese Weise nicht betroffen.
- **Die Grenze von 2000 zählt Formen, nicht Kurven.** Ein Vieleck mit 24 Ecken sind 24 Linien. Ein großes Raster aus Vielecken, Langlöchern oder gefasten Rechtecken kann deshalb langsam sein, obwohl es innerhalb der Grenze liegt.

Aus dem Code:

- Nur Skizzenpunkte lassen sich wählen. Ecken von Körpern oder Punkte auf Kanten nicht.
- Das Raster liegt immer parallel zur X- und zur Y-Achse der Skizze. Im Dialog lässt es sich nicht drehen.
- Beim Vieleck zeigt immer eine Ecke nach oben. Der Dialog hat kein Feld, um es zu drehen.
- Nur das Rechteck kann verrundete oder gefaste Ecken haben.
- Abstände können nicht negativ sein. Formen können sich nicht überlappen.
- Die Formen sind einfache Skizzengeometrie. Ein später geänderter Wert aktualisiert ein vorhandenes Raster nicht.
- Das Add-in fügt keine Bemaßungen und keine Abhängigkeiten hinzu. Das Raster ist nach dem Zeichnen nicht an den Punkt gebunden.
- Die gemerkten Werte gehen verloren, wenn das Add-in stoppt oder Fusion schließt.
- In der Betriebsart **Fläche füllen** wird der leere Rest nur dann mittig verteilt, wenn **Punkt liegt im Raster** auf **In der Mitte** steht (oder für diese eine Richtung auf einem Eintrag mit „mittig“).
