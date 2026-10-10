# System3E – Dokumentation

System3E ist ein Add-In für Autodesk Fusion 360. Es setzt Wandbausteine des mörtellosen Bausystems SYSTEM 3E
in eine Konstruktion. Punkt anklicken, einen von 74 Bausteinen aus einer Liste wählen – der Baustein entsteht dort
als Volumenkörper.

Diese Dokumentation beschreibt die Version 1.1.0.0.

## Inhalt

| Datei | Was dort steht |
| --- | --- |
| [installation.md](installation.md) | Voraussetzungen, Installieren, erster Start, Aktualisieren, Entfernen |
| [usage.md](usage.md) | Bausteine Schritt für Schritt setzen, eine Wand im Verband bauen, Stückliste |
| [settings.md](settings.md) | Jedes Feld des Dialogs, Vorgaben, was gemerkt wird, Sprache |
| [how-it-works.md](how-it-works.md) | Dateien, Bausteinbibliothek, wie ein Körper entsteht, Punkte, Einheiten |
| [troubleshooting.md](troubleshooting.md) | Jede Meldung, ihre Ursache und was zu tun ist; bekannte Grenzen |
| [development.md](development.md) | Ordner, Tests, Bibliothek neu bauen, Versionen, Release |

Weitere Dateien: [Änderungsprotokoll](../CHANGELOG.md), [Lizenz](../LICENSE), [Zeichnung der Punkte](../s1-wp-punkte.svg).

## Was das Add-In macht

- Es fügt Fusion eine Schaltfläche hinzu: **SYSTEM 3E Baustein**.
- Die Schaltfläche öffnet einen Dialog mit acht Feldern und einem Vorschaubild.
- Der Baustein entsteht als Komponente mit einem Volumenkörper.
- Jeder Baustein trägt zwölf eigene Punkte. Sie lassen sich anklicken, um den nächsten Baustein zu setzen.
- Derselbe Baustein, noch einmal gesetzt, ist eine weitere Kopie derselben Komponente. Eine Stückliste zählt gleiche Bausteine zusammen.

## Was geprüft ist und was nicht

| Teil | Stand |
| --- | --- |
| Bausteine setzen | Vom Autor in Fusion benutzt |
| Die zwölf Punkte zum Anklicken | Nur offline geprüft, **nicht in Fusion** |
| Die Auswahl unter **Setzen an** | Nur offline geprüft, **nicht in Fusion** |
| **Versatz X**, **Versatz Y**, **Versatz Z** | Nur offline geprüft, **nicht in Fusion** |
| Korrekturen der Version 1.0.0.1 (siehe [Änderungsprotokoll](../CHANGELOG.md)) | In Fusion noch nicht bestätigt |
| Links/Rechts-Namen der Eck- und Fensterbausteine | Nach Augenmaß mit den Katalogblättern des Herstellers abgeglichen, **nicht bestätigt** |
| Baustein `S0/2 200 P` | In der 3D-Datei des Herstellers beschädigt, aus `S0/2 250 P` nachgebaut |

„Offline“ heißt: von einem Testprogramm ohne Fusion geprüft. Siehe [development.md](development.md).

## Rechtliches

- Das Add-In steht in **keiner Verbindung zu SYSTEM 3E**.
- Lizenz: MIT. Siehe [LICENSE](../LICENSE).
- Autor: Sorglos Thomas Weirich.
