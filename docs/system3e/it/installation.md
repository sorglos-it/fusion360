# Installazione

Torna alla [panoramica](index.md).

## Requisiti

| Che cosa | Dettaglio |
| --- | --- |
| Programma | Autodesk Fusion 360 |
| Sistema operativo | Windows o macOS (l'add-in dichiara entrambi come supportati) |
| Software aggiuntivo | Nessuno. L'add-in usa solo ciò che Fusion porta con sé. |
| Internet | Solo per scaricare il file ZIP. L'add-in stesso non apre alcuna connessione. |

## Installare dallo ZIP di rilascio

1. Aprire <https://github.com/sorglos-it/fusion360/releases>.
2. Scaricare il file `System3E-<version>.zip`, per esempio `System3E-1.3.0.0.zip`.
3. Estrarre lo ZIP nella cartella degli add-in di Fusion:

   | Sistema | Cartella |
   | --- | --- |
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Controllare il risultato. Lo ZIP contiene una cartella di nome `System3E`. Dopo l'estrazione deve esistere questo file:

   `AddIns/System3E/System3E.py`

   Se si vede `AddIns/System3E/System3E/System3E.py`, la cartella è un livello troppo in profondità. Spostare la cartella interna di un livello verso l'alto.

Suggerimento per Windows: digitare `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` nella barra degli indirizzi di Esplora file e
premere Invio.

## Primo avvio in Fusion

1. Avviare Fusion.
2. Aprire **Utilities → ADD-INS → Add-Ins**.
3. Selezionare **System3E** nell'elenco.
4. Premere **Run**.
5. Aprire la scheda **SOLID**. Il pulsante **Elemento SYSTEM 3E** si trova nel pannello **Create**.

Il pulsante mostra la versione tra parentesi, per esempio **Elemento SYSTEM 3E (1.3.0.0)**.

L'add-in è impostato per avviarsi insieme a Fusion (`runOnStartup` nel suo file manifest). Dopo il primo avvio
di norma non occorre premere di nuovo **Run**.

Nota: il percorso di menu del passo 2 è preso dal README del progetto. Non può essere verificato nel codice dell'add-in, e
le versioni di Fusion possono chiamarlo in modo diverso.

## Aggiornamento

1. In Fusion, arrestare l'add-in (**Utilities → ADD-INS → Add-Ins**, selezionare **System3E**, **Stop**), oppure chiudere Fusion.
2. Eliminare la vecchia cartella `System3E` nella cartella degli add-in.
3. Estrarre il nuovo ZIP nella cartella degli add-in, come descritto sopra.
4. Avviare Fusion, oppure premere di nuovo **Run**.

Che cosa succede ai propri progetti:

- Gli elementi già posizionati restano come sono. Sono normali componenti di Fusion.
- Un elemento posizionato con una versione precedente può avere meno di dodici punti. I punti mancanti vengono aggiunti la
  prossima volta che si posiziona lo stesso elemento in quel progetto.
- I valori ricordati della finestra di dialogo vanno persi. Vedere [settings.md](settings.md).

## Rimozione

1. In Fusion, arrestare l'add-in, oppure chiudere Fusion.
2. Eliminare la cartella `System3E` nella cartella degli add-in.

Quando l'add-in si arresta, rimuove il suo pulsante dalla barra degli strumenti. Non salva nulla fuori dalla propria cartella.
Gli elementi nei progetti restano; non hanno bisogno dell'add-in.
