# AddInTemplate

AddInTemplate è il punto di partenza per scrivere un proprio add-in per Autodesk Fusion 360.
Ha due parti:

- un **add-in dimostrativo** (`apps/desktop-template/AddInTemplate`) con un comando, una finestra di dialogo tradotta, un'anteprima dal vivo e controlli dei valori inseriti
- uno **script di generazione** (`tools/template/new_addin.py`) che copia l'add-in dimostrativo e rinomina tutto ciò che deve essere univoco

| Dato | Valore |
| --- | --- |
| Versione | 1.0.0.0 |
| ZIP di rilascio | nessuno per questa versione – si usa dal repository |
| Funziona su | Windows e macOS (manifest: `windows\|mac`) |
| Lingue dell'interfaccia | tedesco, inglese, spagnolo, francese, italiano |
| Dipendenze | nessuna – solo la libreria standard di Python |
| Licenza | MIT |
| Autore | Sorglos Thomas Weirich |
| Repository | <https://github.com/sorglos-it/fusion360> |

## Contenuto

| File | Che cosa vi si trova |
| --- | --- |
| [installation.md](installation.md) | Requisiti, ottenere il repository, creare un nuovo add-in, la cartella degli add-in di Fusion, primo avvio, rimozione |
| [usage.md](usage.md) | Che cosa fa il comando dimostrativo e come trasformare la copia nel proprio add-in |
| [settings.md](settings.md) | Tutto ciò che si imposta nel file di ingresso, nel manifest e nei file di lingua |
| [how-it-works.md](how-it-works.md) | File di ingresso, modulo core, registro degli handler, flusso degli eventi, catalogo dei testi |
| [troubleshooting.md](troubleshooting.md) | Ogni messaggio, la sua causa e che cosa fare; insidie note |
| [development.md](development.md) | Cartelle, controllo offline, strumento per le icone, numeri di versione, creazione del pacchetto, decisioni |

## Buono a sapersi prima di iniziare

- Ogni add-in creato dal modello riceve la **propria copia** del modulo core. Una correzione fatta in seguito nel modello **non** arriva agli add-in creati prima.
- Il controllo offline è stato eseguito per questa documentazione ed è stato superato. Il comportamento dentro Fusion 360 è descritto a partire dal codice; per questa documentazione **non è stato testato in Fusion**.

Altre lingue: [elenco delle lingue](../index.md)
