# Installazione

## Requisiti

- Autodesk Fusion 360 su Windows o macOS. L'add-in dichiara questi due sistemi e nessun altro.
- Nient'altro. L'add-in usa solo il Python integrato in Fusion.

Il codice non indica una versione minima di Fusion.

## Installare dallo ZIP di rilascio

1. Aprire <https://github.com/sorglos-it/fusion360/releases>.
2. Scaricare il file `SketchGrid-<version>.zip`, per esempio `SketchGrid-1.1.0.0.zip`.
3. Estrarlo nella cartella degli add-in di Fusion:

   | Sistema | Cartella |
   | --- | --- |
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Controllare il risultato. Nella cartella degli add-in deve ora esserci una cartella `SketchGrid`, e direttamente al suo interno i file `SketchGrid.py` e `SketchGrid.manifest`.

Non rinominare la cartella. Fusion si aspetta che la cartella, il file `.py` e il file `.manifest` abbiano lo stesso nome.

## Primo avvio in Fusion

1. Avviare Fusion.
2. Aprire **Utilities → ADD-INS → Add-Ins**.
3. Selezionare **SketchGrid** nell'elenco.
4. Premere **Run**.

Nel suo manifest l'add-in è contrassegnato per l'esecuzione all'avvio (`runOnStartup` è impostato). Se la volta successiva non parte da solo, spuntare **Run on Startup** nello stesso elenco.

Dopo l'avvio compare un pulsante di nome **Griglia di schizzo (1.1.0.0)**. Il numero tra parentesi è la versione installata. L'add-in cerca prima il pannello **CREATE** della barra degli strumenti dello schizzo e, se non esiste, il pannello **CREATE** della scheda **SOLID**.

## Aggiornamento

1. In Fusion, aprire **Utilities → ADD-INS → Add-Ins**, selezionare **SketchGrid** e premere **Stop**. Altrimenti la vecchia versione resta in memoria.
2. Eliminare la cartella `SketchGrid` nella cartella degli add-in.
3. Estrarre il nuovo ZIP nella cartella degli add-in, come sopra.
4. Premere di nuovo **Run**.
5. Controllare la versione tra parentesi sul pulsante.

L'add-in non salva impostazioni su disco. Eliminando la cartella non si perde nulla.

## Rimozione

1. In Fusion, arrestare l'add-in (**Utilities → ADD-INS → Add-Ins**, selezionare **SketchGrid**, **Stop**). In questo modo sparisce il pulsante.
2. Eliminare la cartella `SketchGrid` nella cartella degli add-in.

L'add-in non lascia altri file. Le griglie già disegnate restano negli schizzi; sono normale geometria di schizzo.
