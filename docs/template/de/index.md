# AddInTemplate

AddInTemplate ist der Ausgangspunkt, um ein eigenes Add-In für Autodesk Fusion 360 zu schreiben.
Es hat zwei Teile:

- ein **Beispiel-Add-In** (`apps/desktop-template/AddInTemplate`) mit einem Befehl, einem übersetzten Dialog, einer sofortigen Vorschau und Eingabeprüfungen
- ein **Gerüst-Skript** (`tools/template/new_addin.py`), das das Beispiel-Add-In kopiert und alles umbenennt, was eindeutig sein muss

| Angabe | Wert |
| --- | --- |
| Version | 1.0.0.0 |
| Release-ZIP | keines für diese Version – sie wird aus dem Repository benutzt |
| Läuft auf | Windows und macOS (Manifest: `windows\|mac`) |
| Sprachen der Oberfläche | Deutsch, Englisch, Spanisch, Französisch, Italienisch |
| Abhängigkeiten | keine – nur die Python-Standardbibliothek |
| Lizenz | MIT |
| Autor | Sorglos Thomas Weirich |
| Repository | <https://github.com/sorglos-it/fusion360> |

## Inhalt

| Datei | Was dort steht |
| --- | --- |
| [installation.md](installation.md) | Voraussetzungen, das Repository holen, ein neues Add-In anlegen, der Add-In-Ordner von Fusion, erster Start, Entfernen |
| [usage.md](usage.md) | Was der Beispielbefehl macht und wie aus der Kopie ein eigenes Add-In wird |
| [settings.md](settings.md) | Alles, was in der Startdatei, im Manifest und in den Sprachdateien eingestellt wird |
| [how-it-works.md](how-it-works.md) | Startdatei, Kernmodul, Handler-Register, Ablauf der Ereignisse, Textkatalog |
| [troubleshooting.md](troubleshooting.md) | Jede Meldung, ihre Ursache und was zu tun ist; bekannte Stolperfallen |
| [development.md](development.md) | Ordner, Offline-Prüfung, Symbol-Werkzeug, Versionsnummern, Packen, Entscheidungen |

## Gut zu wissen vor dem Start

- Jedes Add-In, das aus der Vorlage angelegt wird, bekommt seine **eigene Kopie** des Kernmoduls. Eine Korrektur, die später in der Vorlage gemacht wird, erreicht früher angelegte Add-Ins **nicht**.
- Die Offline-Prüfung wurde für diese Dokumentation ausgeführt und bestanden. Das Verhalten in Fusion 360 ist nach dem Code beschrieben; es wurde für diese Dokumentation **nicht in Fusion geprüft**.

Andere Sprachen: [Sprachliste](../index.md)
