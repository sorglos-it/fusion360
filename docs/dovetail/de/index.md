# Dovetail – Dokumentation

Dovetail ist ein Add-in für Autodesk Fusion 360. Es macht aus Skizzenlinien Verbindungen: Schwalbenschwanz, Dreieck
oder Fingerzinken. Für jede gewählte Linie zeichnet es ein geschlossenes Band. Das Band ist genau so breit wie der
Spalt, der zwischen den beiden Teilen bleiben soll. Wird das Band aus einem Körper herausgeschnitten, bleiben zwei
Teile übrig, die ineinander passen.

Diese Dokumentation beschreibt die Version **1.1.0.0**.

## Inhalt

| Datei | Was darin steht |
|---|---|
| [installation.md](installation.md) | Voraussetzungen, Installieren, erster Start, Aktualisieren, Entfernen |
| [usage.md](usage.md) | Jede Funktion, Schritt für Schritt |
| [settings.md](settings.md) | Jedes Dialogfeld: Bedeutung, Vorgabe, Grenzen; was gemerkt wird; Sprache |
| [how-it-works.md](how-it-works.md) | Wie das Band im Inneren entsteht, die Prüfungen, Einheiten |
| [troubleshooting.md](troubleshooting.md) | Jede Meldung, ihre Ursache und was zu tun ist; bekannte Grenzen |
| [development.md](development.md) | Ordner, Tests, Versionsnummern, Release packen, Entscheidungen |

## Auf einen Blick

| | |
|---|---|
| Läuft in | Autodesk Fusion 360 unter Windows und macOS |
| Formen | Trapez (Schwalbenschwanz), Dreieck, Rechteck (Fingerzinken) |
| Linien je Lauf | 1 bis 100 |
| Zähne je Linie | 1 bis 500 |
| Sprachen der Oberfläche | Deutsch, Englisch, Spanisch, Französisch, Italienisch |
| Lizenz | MIT, siehe [LICENSE](../LICENSE) |
| Autor | Sorglos Thomas Weirich |

## Prüfstand

- Die Geometrie-Berechnung und die Sprachdateien werden außerhalb von Fusion mit einem Offline-Testskript geprüft.
- Version 1.1.0.0 hat die Geometrie geändert (siehe [how-it-works.md](how-it-works.md#was-sich-in-1100-geändert-hat)).
  Diese Änderungen wurden **nur offline** geprüft, darunter mit 34.317 zufälligen Konturen. Sie sind **noch nicht
  in Fusion bestätigt**.

## Siehe auch

- [README](../README.md) – kurze Einstiegsseite
- [CHANGELOG](../CHANGELOG.md) – was sich in welcher Version geändert hat
