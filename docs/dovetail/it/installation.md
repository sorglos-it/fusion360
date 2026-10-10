# Installazione

## Requisiti

- Autodesk Fusion 360 su Windows o macOS. L'add-in dichiara esattamente questi due sistemi.
- Nient'altro. L'add-in gira nel Python fornito da Fusion e non usa pacchetti aggiuntivi.

Nel codice non è indicata una versione minima di Fusion. L'add-in non è stato provato con un elenco di versioni di Fusion.

## Installare dallo ZIP di rilascio

1. Aprire <https://github.com/sorglos-it/fusion360/releases>.
2. Scaricare il file `Dovetail-<version>.zip`, per esempio `Dovetail-1.1.0.0.zip`.
3. Estrarre lo ZIP nella cartella degli add-in di Fusion:

   | Sistema | Cartella |
   |---|---|
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Controllare il risultato. Lo ZIP contiene una cartella di nome `Dovetail`. Dopo l'estrazione deve esistere questo:

   ```
   AddIns/Dovetail/Dovetail.py
   AddIns/Dovetail/Dovetail.manifest
   AddIns/Dovetail/lang/
   AddIns/Dovetail/resources/
   ```

   Se il programma di estrazione ha creato una cartella in più attorno (per esempio `AddIns/Dovetail-1.1.0.0/Dovetail/`),
   spostare la cartella interna `Dovetail` di un livello verso l'alto.

Non rinominare la cartella né i file. La cartella, il file `.py` e il file `.manifest` devono avere tutti lo stesso nome.

## Primo avvio in Fusion

1. Avviare Fusion.
2. Aprire l'elenco degli add-in: **Utilities → ADD-INS → Add-Ins**.
   (Il testo di questo menu viene da Fusion e può cambiare da una versione di Fusion all'altra.)
3. Selezionare la voce **Dovetail**.
4. Spuntare **Run on Startup**, se non è già spuntato. L'add-in lo richiede da solo nel suo manifest.
5. Premere **Run**.

L'add-in aggiunge quindi un pulsante alla barra degli strumenti. Il suo nome è **Coda di rondine** seguito dalla
versione tra parentesi, per esempio *Coda di rondine (1.1.0.0)*.

Dove compare il pulsante:

| Ordine | Posto |
|---|---|
| 1 | il pannello **Create** della barra degli strumenti dello schizzo |
| 2 | se manca: il pannello **Modify** della barra degli strumenti dello schizzo |
| 3 | se manca anche quello: il pannello **Create** della scheda Solid |

L'add-in prende il primo di questi che esiste. Il pulsante viene messo direttamente sulla barra degli strumenti, non
solo nel menu a discesa del pannello.

Se nessuno dei tre esiste, compare il messaggio "Nessun pannello della barra degli strumenti adatto trovato." Vedere
[troubleshooting.md](troubleshooting.md).

## Aggiornamento

1. In Fusion, aprire l'elenco degli add-in e **arrestare** Dovetail. Altrimenti la vecchia versione resta in memoria.
2. Eliminare la vecchia cartella `Dovetail` dalla cartella degli add-in.
3. Estrarre il nuovo ZIP nella cartella degli add-in, come descritto sopra.
4. Premere di nuovo **Run**, oppure riavviare Fusion.
5. Controllare la versione nel nome del pulsante o nel titolo della finestra di dialogo.

L'add-in non salva impostazioni su disco. Eliminando la vecchia cartella non si perde nulla.

Nota presa dal README precedente, non verificabile nel codice attuale: le versioni molto vecchie si chiamavano `Schwalbenschwanz`.
Se una cartella così è ancora nella cartella degli add-in, arrestare quell'add-in ed eliminare la cartella. Altrimenti compaiono due pulsanti.

## Rimozione

1. In Fusion, aprire l'elenco degli add-in e **arrestare** Dovetail. In questo modo spariscono il pulsante e il comando.
2. Chiudere Fusion.
3. Eliminare la cartella `Dovetail` dalla cartella degli add-in.

L'add-in non scrive altri file né impostazioni. I giunti già disegnati restano negli schizzi; sono normali
linee di schizzo.
