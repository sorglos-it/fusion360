# Fehlerbehebung

Zurück zur [Übersicht](index.md).

## Meldungen

Das sind alle Meldungen, die das Add-In zeigen kann. Die Texte sind aus der deutschen Sprachdatei zitiert. In anderen
Sprachen ist der Text übersetzt. Meldungsfenster tragen den Titel „SYSTEM 3E Baustein“.

### „Bitte einen Baustein wählen.“

| | |
| --- | --- |
| Ursache | Unter **Baustein** ist kein Eintrag ausgewählt. |
| Was zu sehen ist | Normalerweise nicht die Meldung selbst: Stattdessen ist die Schaltfläche **OK** ausgegraut. |
| Was zu tun ist | Unter **Baustein** einen Eintrag wählen. Ist die Liste leer, die **Gruppe** noch einmal wählen. |

### „Bitte zuerst eine Konstruktion öffnen.“

| | |
| --- | --- |
| Ursache | Das aktive Dokument ist keine Konstruktion. Es gibt also nichts, in das der Baustein gesetzt werden kann. |
| Was zu tun ist | Eine Konstruktion öffnen oder anlegen und in den Arbeitsbereich Konstruktion wechseln. Dann den Befehl noch einmal starten. |

### „Der Baustein {0} konnte nicht erzeugt werden:“ gefolgt von einem Grund

`{0}` ist der Name des Bausteins. Die zweite Zeile ist der Grund, den Fusion nennt.

| | |
| --- | --- |
| Ursache | Fusion hat es abgelehnt, den Körper aus den Punkten und Flächen des Bausteins zu bauen. |
| Was zu tun ist | 1. Einen anderen Baustein versuchen, um zu sehen, ob nur dieser eine betroffen ist. 2. Das Add-In aus einem frischen ZIP neu installieren; die Datei `blocks/blocks.json` kann beschädigt sein. 3. Schlägt es weiter fehl, den Namen des Bausteins und den Grund aus der Meldung melden. |
| Wirkung | Es bleibt nichts zurück. Fusion macht den Schritt rückgängig. |

### „Kein passendes Toolbar-Panel gefunden.“

| | |
| --- | --- |
| Ursache | Beim Start hat das Add-In das Panel **Create** der Volumenkörper-Werkzeuge nicht gefunden. Es wurde keine Schaltfläche hinzugefügt. |
| Was zu tun ist | Fusion aktualisieren und das Add-In neu starten. Bleibt die Meldung, die eigene Fusion-Version melden. Das Add-In kennt nur dieses eine Panel. |

### „Fehler beim Erzeugen der Geometrie:“ gefolgt von technischem Text

| | |
| --- | --- |
| Ursache | Ein unerwarteter Fehler nach dem Druck auf **OK**. Der Text unter der ersten Zeile ist ein technischer Bericht (ein „Traceback“), der zeigt, wo es passiert ist. |
| Was zu tun ist | 1. Es mit einem anderen Punkt oder einem anderen Baustein noch einmal versuchen. 2. Das Add-In stoppen und neu starten. 3. Bleibt es dabei, den ganzen Text kopieren und melden. |
| Wirkung | Fusion macht rückgängig, was bis dahin gebaut wurde. Es bleibt keine halbfertige Komponente zurück. |

### „Fehler beim Aufbau des Dialogs:“ gefolgt von technischem Text

| | |
| --- | --- |
| Ursache | Der Dialog konnte nicht aufgebaut werden. Ein Grund, der im Code zu sehen ist: Die Datei `blocks/blocks.json` fehlt oder ist nicht lesbar. Der Dialog liest die Bausteinbibliothek, wenn er aufgeht. |
| Was zu tun ist | Das Add-In aus dem ZIP neu installieren, damit der Ordner `blocks` vollständig ist. Siehe [installation.md](installation.md). |

### „Start fehlgeschlagen:“ gefolgt von technischem Text

| | |
| --- | --- |
| Ursache | Ein unerwarteter Fehler beim Start des Add-Ins. |
| Was zu tun ist | 1. Prüfen, ob der Ordner richtig entpackt ist: `AddIns/System3E/System3E.py`. 2. Fusion neu starten. 3. Das Add-In neu installieren. 4. Bleibt es dabei, den Text kopieren und melden. |

### „Stopp fehlgeschlagen:“ gefolgt von technischem Text

| | |
| --- | --- |
| Ursache | Ein unerwarteter Fehler, während das Add-In gestoppt und seine Schaltfläche entfernt wurde. |
| Was zu tun ist | Fusion neu starten. Die eigenen Konstruktionen sind nicht betroffen. |

## Andere Probleme

| Problem | Ursache | Was zu tun ist |
| --- | --- | --- |
| **System3E** steht nicht in der Add-Ins-Liste von Fusion. | Der Ordner liegt am falschen Ort oder eine Ebene zu tief. | Prüfen, ob `AddIns/System3E/System3E.py` vorhanden ist. Siehe [installation.md](installation.md). |
| Die Schaltfläche fehlt. | Das Add-In läuft nicht. | Den Add-Ins-Dialog öffnen, **System3E** auswählen, **Run** drücken. |
| Der Dialog ist englisch, obwohl Fusion eine andere Sprache benutzt. | Es gibt nur Deutsch, Englisch, Spanisch, Französisch und Italienisch. Bei anderen Sprachen wird Englisch benutzt. | – |
| Der Dialog hat die falsche Sprache, nachdem die Sprache von Fusion geändert wurde. | Die Sprache wird beim Start des Add-Ins festgelegt. | Das Add-In stoppen und neu starten, oder Fusion neu starten. |
| Das Bild wechselt nicht, wenn ein anderer Baustein gewählt wird. | Die Bilddatei `blocks/<id>.png` dieses Bausteins fehlt. Das alte Bild bleibt stehen. | Das Add-In neu installieren. |
| Solange der Dialog offen ist, erscheint keine Vorschau des Bausteins. | Während der Vorschau ist ein Fehler aufgetreten. Fehler der Vorschau werden nicht angezeigt. | **OK** drücken. Ein echter Fehler wird dann als Meldung angezeigt. |
| Eine bestimmte Stelle lässt sich nicht anklicken. | Wählbar sind nur Skizzenpunkte, Ecken von Körpern und Konstruktionspunkte. Flächen, Kanten und Kantenmitten nicht. | Dort einen Skizzenpunkt oder einen Konstruktionspunkt anlegen, oder den Versatz benutzen. |
| Der Baustein steht im Ursprung. | Es war kein Punkt ausgewählt. | Für **Punkt** einen Punkt anklicken. |
| Der Baustein ist falsch herum gedreht. | Eine positive **Drehung** dreht gegen den Uhrzeigersinn, von oben gesehen. | Den Winkel mit dem anderen Vorzeichen eingeben. |
| Der Versatz schiebt den Baustein in eine unerwartete Richtung. | Der Versatz läuft entlang der Achsen der Konstruktion, nicht entlang des gedrehten Bausteins. | Die Achse benutzen, die zur Richtung in der Konstruktion passt. |
| Die Punktnamen haben eine andere Sprache als der Dialog. | Punktnamen werden geschrieben, wenn ein Baustein zum ersten Mal in eine Konstruktion gesetzt wird, und bleiben erhalten. | Die Punkte bei Bedarf von Hand umbenennen. |
| Ein älterer Baustein hat weniger als zwölf Punkte. | Er wurde mit einer älteren Version gesetzt. | Irgendeinen Baustein noch einmal in diese Konstruktion setzen. Jeder Baustein bekommt seine fehlenden Punkte. |
| Die Punkte liegen neben dem Baustein, nicht auf ihm. | Der Baustein wurde mit einer Version vor 1.1.0.1 abseits des Ursprungs gesetzt. | Irgendeinen Baustein noch einmal in diese Konstruktion setzen. Die Punkte werden an der richtigen Stelle neu angelegt. |
| Ein Punkt liegt nicht genau auf halber Breite oder an der Unterseite. | Der genaue Ort liegt im Material oder in der Luft. Deshalb wird der Punkt auf der Fläche daneben gezeigt. | Nichts. Beim Anklicken zählt weiter der genaue Ort. Siehe [usage.md](usage.md). |
| Nach einem Update zeigt Fusion auf der Schaltfläche noch die alte Version. | Fusion führt die Kopie in seinem Add-Ins-Ordner aus, nicht die heruntergeladene. | Das neue ZIP über den alten Ordner entpacken, dann das Add-In stoppen und starten. Siehe [installation.md](installation.md). |
| Der Dialog beginnt wieder mit den Vorgaben. | Die gemerkten Werte halten nur, bis Fusion geschlossen oder das Add-In gestoppt wird. | – |
| Eine Stückliste zeigt denselben Baustein in mehreren Zeilen. | Die Bausteine wurden mit Version 0.2.0 gesetzt, die jedes Mal eine neue Komponente angelegt hat. Nur der erste davon wird ab jetzt wiederverwendet. | Die alten durch neu gesetzte Bausteine ersetzen. |

## Bekannte Grenzen

- **Links und rechts:** Die Links/Rechts-Namen der Eck- und Fensterbausteine wurden nach Augenmaß mit den
  Katalogblättern des Herstellers abgeglichen. Sie sind nicht bestätigt.
- **`S0/2 200 P`:** Dieser Baustein ist in der 3D-Datei des Herstellers beschädigt. Er ist aus `S0/2 250 P` nachgebaut.
- **Senkrechte Achse:** Das Add-In behandelt immer die Z-Achse der Konstruktion als „oben“. Eine andere
  Ausrichtungseinstellung in Fusion beachtet es nicht.
- **Nur oberste Ebene:** Bausteine entstehen immer in der obersten Ebene der Konstruktion (der Stammkomponente), nicht
  in der Komponente, die gerade aktiv ist.
- **Verknüpfte Konstruktionen:** Ein Baustein in einer verknüpften Konstruktion wird nicht wiederverwendet. Das Add-In
  legt eine eigene Komponente an.
- **Keine Passprüfung:** Das Add-In prüft nicht, ob sich Bausteine überschneiden, ob eine Fuge passt oder ob eine Wand
  baubar ist.
- **Ein Baustein je Durchlauf:** Es gibt keine Funktion für ganze Schichten oder Wände.
- **Drehen:** nur um die senkrechte Achse. Bausteine lassen sich im Dialog nicht kippen.
- **Gemeinsamer Körper:** Alle Kopien eines Bausteins teilen sich einen Körper. Wer eine ändert, ändert alle.
- **Größen:** Die Formen stammen aus der 3D-Datei des Herstellers und sind auf 0,1 mm gerundet. Die vier
  Trennwand-Bausteine sind einfache Quader ohne Profil.
- **Keine Verbindung:** Das Add-In steht in keiner Verbindung zu SYSTEM 3E. Es ersetzt nicht die
  Planungsunterlagen des Herstellers.
