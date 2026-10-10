# Dovetail – documentazione

Dovetail è un add-in per Autodesk Fusion 360. Trasforma le linee di schizzo in giunti: coda di rondine, triangolo o
giunto a pettine. Per ogni linea selezionata disegna una fascia chiusa. La fascia è larga esattamente quanto il gioco
desiderato tra i due pezzi. Tagliando la fascia da un solido restano due pezzi che si incastrano.

Questa documentazione descrive la versione **1.1.0.0**.

## Contenuto

| File | Cosa contiene |
|---|---|
| [installation.md](installation.md) | Requisiti, installazione, primo avvio, aggiornamento, rimozione |
| [usage.md](usage.md) | Ogni funzione, passo per passo |
| [settings.md](settings.md) | Ogni campo della finestra di dialogo: significato, valore predefinito, limiti; cosa viene ricordato; lingua |
| [how-it-works.md](how-it-works.md) | Come viene costruita la fascia all'interno, i controlli, le unità |
| [troubleshooting.md](troubleshooting.md) | Ogni messaggio, la sua causa e cosa fare; limiti noti |
| [development.md](development.md) | Cartelle, test, numeri di versione, creazione del pacchetto di rilascio, decisioni |

## In breve

| | |
|---|---|
| Funziona in | Autodesk Fusion 360 su Windows e macOS |
| Forme | Trapezio (coda di rondine), Triangolo, Rettangolo (giunto a pettine) |
| Linee per esecuzione | da 1 a 100 |
| Denti per linea | da 1 a 500 |
| Lingue dell'interfaccia | tedesco, inglese, spagnolo, francese, italiano |
| Licenza | MIT, vedere [LICENSE](../LICENSE) |
| Autore | Sorglos Thomas Weirich |

## Stato dei test

- I calcoli della geometria e i file di lingua sono verificati fuori da Fusion con uno script di test offline.
- La versione 1.1.0.0 ha modificato la geometria (vedere [how-it-works.md](how-it-works.md#cosa-è-cambiato-nella-1100)).
  Queste modifiche sono state verificate **solo offline**, anche con 34.317 profili casuali. **Non sono ancora
  confermate all'interno di Fusion**.

## Vedere anche

- [README](../README.md) – breve pagina di ingresso
- [CHANGELOG](../CHANGELOG.md) – cosa è cambiato in quale versione
