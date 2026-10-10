# Einstellungen

Zurück zur [Übersicht](index.md).

Das Add-In hat keine Einstellungsseite und keine Einstellungsdatei. Alles, was sich einstellen lässt, steht im Dialog des Befehls
**SYSTEM 3E Baustein**.

## Die Felder des Dialogs

| Feld | Bedeutung | Vorgabe | Erlaubte Werte |
| --- | --- | --- | --- |
| **Punkt** | Die Stelle für den Baustein. | Leer, oder der Punkt, der vor dem Druck auf die Schaltfläche ausgewählt war. | Nichts oder genau ein Punkt: ein Skizzenpunkt, eine Ecke eines Körpers oder ein Konstruktionspunkt. Nichts bedeutet den Ursprung der Konstruktion. |
| **Gruppe** | Die Gruppe der Bausteine, die unter **Baustein** angezeigt wird. | Basis | Starter, Basis, Ergänzung, Sturz, Fensterrahmen, Abschluss, Ecke, Trennwand |
| **Baustein** | Der Baustein, der gesetzt wird, mit seiner Größe in mm (Länge x Breite x Höhe). | S1 WP | Die Bausteine der gewählten Gruppe. Siehe die Listen in [usage.md](usage.md). |
| (Bild) | Zeigt den gewählten Baustein. Lässt sich nicht ändern. | Bild des gewählten Bausteins | – |
| **Setzen an** | Welche Stelle des Bausteins auf dem Punkt landet. | Ecke unten vorne rechts | 15 Einträge: drei Ecken und die zwölf Punkte. Siehe unten. |
| **Drehung** | Dreht den Baustein um die senkrechte Achse (Z) um die Stelle, die unter **Setzen an** gewählt ist. | 0 Grad | Jeder Winkel. Positiv ist gegen den Uhrzeigersinn, von oben gesehen. |
| **Versatz X** | Schiebt den Baustein entlang der X-Achse der Konstruktion. | 0 mm | Jede Länge, auch negativ |
| **Versatz Y** | Schiebt den Baustein entlang der Y-Achse der Konstruktion. | 0 mm | Jede Länge, auch negativ |
| **Versatz Z** | Schiebt den Baustein entlang der Z-Achse der Konstruktion. | 0 mm | Jede Länge, auch negativ |

Das Add-In setzt für die Drehung und den Versatz keine Ober- und keine Untergrenze.

### Die Einträge unter „Setzen an“

In dieser Reihenfolge:

1. Ecke unten vorne rechts
2. Ecke oben vorne rechts
3. Ecke oben vorne links
4. unten vorne
5. unten Mitte
6. unten hinten
7. oben vorne
8. oben Mitte
9. oben hinten
10. oben Mitte rechts
11. oben Mitte links
12. unten Mitte rechts
13. unten Mitte links
14. Mitte rechts, 50 mm hoch
15. Mitte links, 50 mm hoch

Was jeder Eintrag bedeutet, steht in [usage.md](usage.md).

Stand: **Setzen an** und die drei Versatz-Felder sind nur offline geprüft, **nicht in Fusion**.

## Was gemerkt wird

Nach dem Druck auf **OK**, wenn der Baustein erzeugt wurde, merkt sich das Add-In diese Werte für das nächste Mal:

- **Gruppe**
- **Baustein**
- **Setzen an**
- **Drehung**
- **Versatz X**, **Versatz Y**, **Versatz Z**

Nicht gemerkt: der **Punkt**.

| Frage | Antwort |
| --- | --- |
| Wie lange? | Bis Fusion geschlossen oder das Add-In gestoppt wird. Die Werte liegen nur im Arbeitsspeicher. |
| Werden sie in einer Datei gespeichert? | Nein. |
| Werden sie in der Konstruktion gespeichert? | Nein. |
| Was, wenn der Dialog abgebrochen wird? | Nichts wird gemerkt. Die Werte des letzten erfolgreichen Setzens bleiben. |
| Was nach einem Neustart? | Es gelten wieder die Vorgaben aus der Tabelle oben. |

## Sprache

Das Add-In hat seine Texte in fünf Sprachen: Deutsch, Englisch, Spanisch, Französisch und Italienisch.

Die Sprache lässt sich im Add-In nicht wählen. Sie wird beim Start des Add-Ins festgelegt:

1. Das Add-In fragt Fusion nach der Sprache, die in den Voreinstellungen von Fusion eingestellt ist. Ist es eine der fünf, wird sie benutzt.
2. Sonst sieht es in den Spracheinstellungen des Betriebssystems nach (die Umgebungsvariablen `LANG`,
   `LANGUAGE`, `LC_ALL`, dann die Sprache des Systems).
3. Ergibt nichts davon eine der fünf Sprachen, wird Englisch benutzt.

Weitere Einzelheiten:

- Um die Sprache zu wechseln: die Sprache in den Voreinstellungen von Fusion ändern und das Add-In neu starten.
- Fehlt ein Text in einer Sprache, wird stattdessen der englische Text angezeigt.
- Namen von Bausteinen (`S1 WP`) und von Komponenten (`SYSTEM 3E S1 WP`) werden nicht übersetzt.
- Die Namen der zwölf Punkte werden in die Konstruktion geschrieben, wenn ein Baustein zum ersten Mal gesetzt wird. Sie behalten
  diese Sprache, auch wenn das Add-In später in einer anderen Sprache läuft.

## Feste Werte, die sich im Dialog nicht ändern lassen

| Wert | Einstellung |
| --- | --- |
| Ort der Schaltfläche | Arbeitsbereich Konstruktion, Panel **Create** der Volumenkörper-Werkzeuge |
| Start mit Fusion | Ja (`runOnStartup` in der Manifest-Datei) |
| Punkte 50 mm über der Unterseite | Fest auf 50 mm |
