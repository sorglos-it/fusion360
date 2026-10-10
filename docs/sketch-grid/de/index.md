# SketchGrid

SketchGrid ist ein Add-in für Autodesk Fusion 360. Ein Klick auf einen Punkt in einer Skizze ergibt ein Raster aus gleichen Formen um ihn herum: Rechtecke, Kreise oder Ellipsen, Langlöcher oder Vielecke.

Diese Dokumentation beschreibt die Version 1.1.0.0.

## Inhalt

| Datei | Was darin steht |
| --- | --- |
| [installation.md](installation.md) | Voraussetzungen, Installieren, erster Start, Aktualisieren, Entfernen |
| [usage.md](usage.md) | Jede Funktion, Schritt für Schritt |
| [settings.md](settings.md) | Jedes Dialogfeld mit Vorgabe und Grenzen, was gemerkt wird, Sprache |
| [how-it-works.md](how-it-works.md) | Dateien, wie das Raster berechnet wird, wie die Formen gezeichnet werden |
| [troubleshooting.md](troubleshooting.md) | Jede Meldung, ihre Ursache und was zu tun ist; bekannte Grenzen |
| [development.md](development.md) | Ordner, Tests, Versionsnummern, Release packen |

## Was es tut, in Kürze

- Zwei Wege, die Zahl der Formen festzulegen: **Spalten und Zeilen** oder **Fläche füllen** (so viele, wie ganz hineinpassen).
- Vier Formen: **Rechteck** (Ecken scharfkantig, verrundet oder gefast), **Kreis / Ellipse**, **Langloch**, **Vieleck** (3 bis 24 Ecken).
- Neun Lagen für den Punkt im Raster, dazu ein Versatz in X und Y.
- Ein eigener Abstand für X und für Y.
- Eine Zeile **Ergebnis**, die schon beim Tippen die Zahl der Formen und die Gesamtgröße zeigt.
- Höchstens 2000 Formen je Raster.

## Prüfstand

- Die Rasterberechnung, die Eckenumrisse, die Meldungen und die fünf Sprachdateien werden von einem automatischen Test geprüft, der ohne Fusion läuft.
- Die Änderung in Version 1.1.0.0 (der Dialog arbeitet weiter, wenn der vorher gewählte Punkt nicht übernommen werden kann) wurde nur offline geprüft, **nicht in Fusion**.
- Zwei bekannte Grenzen stammen aus einer Durchsicht des Codes und sind **in Fusion nicht bestätigt**. Siehe [troubleshooting.md](troubleshooting.md#bekannte-grenzen).

## Lizenz und Autor

MIT-Lizenz, siehe [LICENSE](../LICENSE). Autor: Sorglos Thomas Weirich.

Änderungsverlauf: [CHANGELOG.md](../CHANGELOG.md).
