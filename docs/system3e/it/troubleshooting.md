# Risoluzione dei problemi

Torna alla [panoramica](index.md).

## Messaggi

Questi sono tutti i messaggi che l'add-in può mostrare. I testi sono citati dal file di lingua italiano. Nelle altre
lingue il testo è tradotto. Le finestre di messaggio portano il titolo "Elemento SYSTEM 3E".

### "Scegli un elemento."

| | |
| --- | --- |
| Causa | Nessuna voce è selezionata sotto **Elemento**. |
| Che cosa si vede | Di norma non il messaggio stesso: al suo posto il pulsante **OK** è disattivato (grigio). |
| Che cosa fare | Scegliere una voce sotto **Elemento**. Se l'elenco è vuoto, scegliere di nuovo la **Famiglia**. |

### "Apri prima un progetto."

| | |
| --- | --- |
| Causa | Il documento attivo non è un progetto, quindi non c'è nulla in cui posizionare l'elemento. |
| Che cosa fare | Aprire o creare un progetto e passare all'area di lavoro di progettazione. Poi avviare di nuovo il comando. |

### "Impossibile creare l'elemento {0}:" seguito da un motivo

`{0}` è il nome dell'elemento. La seconda riga è il motivo dato da Fusion.

| | |
| --- | --- |
| Causa | Fusion ha rifiutato di costruire il corpo dai punti e dalle facce dell'elemento. |
| Che cosa fare | 1. Provare un altro elemento per vedere se solo questo è interessato. 2. Installare di nuovo l'add-in da uno ZIP appena scaricato; il file `blocks/blocks.json` può essere danneggiato. 3. Se non riesce ancora, segnalare il nome dell'elemento e il motivo indicato nel messaggio. |
| Effetto | Non resta nulla. Fusion annulla il passo. |

### "Nessun pannello della barra degli strumenti adatto trovato."

| | |
| --- | --- |
| Causa | All'avvio l'add-in non ha trovato il pannello **Create** degli strumenti per solidi. Non è stato aggiunto alcun pulsante. |
| Che cosa fare | Aggiornare Fusion e avviare di nuovo l'add-in. Se il messaggio resta, segnalare la propria versione di Fusion. L'add-in conosce solo questo pannello. |

### "Errore durante la creazione della geometria:" seguito da testo tecnico

| | |
| --- | --- |
| Causa | Un errore imprevisto dopo aver premuto **OK**. Il testo sotto la prima riga è un rapporto tecnico (un "traceback") che mostra dove è successo. |
| Che cosa fare | 1. Riprovare con un altro punto o un altro elemento. 2. Arrestare l'add-in ed eseguirlo di nuovo. 3. Se resta, copiare tutto il testo e segnalarlo. |
| Effetto | Fusion annulla ciò che era stato costruito fino a quel momento. Non resta alcun componente lasciato a metà. |

### "Errore durante la costruzione della finestra di dialogo:" seguito da testo tecnico

| | |
| --- | --- |
| Causa | Non è stato possibile costruire la finestra di dialogo. Un motivo visibile nel codice è un file `blocks/blocks.json` mancante o illeggibile: la finestra di dialogo legge la libreria degli elementi quando si apre. |
| Che cosa fare | Installare di nuovo l'add-in dallo ZIP, in modo che la cartella `blocks` sia completa. Vedere [installation.md](installation.md). |

### "Avvio non riuscito:" seguito da testo tecnico

| | |
| --- | --- |
| Causa | Un errore imprevisto durante l'avvio dell'add-in. |
| Che cosa fare | 1. Controllare che la cartella sia estratta correttamente: `AddIns/System3E/System3E.py`. 2. Riavviare Fusion. 3. Installare di nuovo l'add-in. 4. Se resta, copiare il testo e segnalarlo. |

### "Arresto non riuscito:" seguito da testo tecnico

| | |
| --- | --- |
| Causa | Un errore imprevisto mentre l'add-in si arrestava e rimuoveva il suo pulsante. |
| Che cosa fare | Riavviare Fusion. I progetti non sono interessati. |

## Altri problemi

| Problema | Causa | Che cosa fare |
| --- | --- | --- |
| **System3E** non è nell'elenco degli add-in di Fusion. | La cartella è nel posto sbagliato o un livello troppo in profondità. | Controllare che `AddIns/System3E/System3E.py` esista. Vedere [installation.md](installation.md). |
| Il pulsante manca. | L'add-in non è in esecuzione. | Aprire la finestra degli add-in, selezionare **System3E**, premere **Run**. |
| La finestra di dialogo è in inglese anche se Fusion usa un'altra lingua. | Esistono solo tedesco, inglese, spagnolo, francese e italiano. Le altre lingue ricadono sull'inglese. | – |
| La finestra di dialogo è nella lingua sbagliata dopo aver cambiato la lingua di Fusion. | La lingua viene scelta all'avvio dell'add-in. | Arrestare l'add-in ed eseguirlo di nuovo, oppure riavviare Fusion. |
| L'immagine non cambia quando si sceglie un altro elemento. | Manca il file immagine `blocks/<id>.png` di quell'elemento. Resta la vecchia immagine. | Installare di nuovo l'add-in. |
| Non compare alcuna anteprima dell'elemento mentre la finestra di dialogo è aperta. | È avvenuto un errore durante l'anteprima. Gli errori dell'anteprima non vengono mostrati. | Premere **OK**. Un errore vero viene allora mostrato come messaggio. |
| Non si riesce a cliccare un certo posto. | Si possono selezionare solo punti di schizzo, spigoli d'angolo di corpi e punti di costruzione. Facce, spigoli e punti medi degli spigoli no. | Creare lì un punto di schizzo o un punto di costruzione, oppure usare gli spostamenti. |
| L'elemento sta nell'origine. | Non è stato selezionato alcun punto. | Fare clic su un punto per **Punto**. |
| L'elemento è ruotato nel verso sbagliato. | Una **Rotazione** positiva ruota in senso antiorario visto dall'alto. | Digitare l'angolo con il segno opposto. |
| Gli spostamenti muovono l'elemento in una direzione inattesa. | Gli spostamenti corrono lungo gli assi del progetto, non lungo l'elemento ruotato. | Usare l'asse che corrisponde alla direzione nel progetto. |
| I nomi dei punti sono in una lingua diversa da quella della finestra di dialogo. | I nomi dei punti vengono scritti quando un elemento viene posizionato per la prima volta in un progetto e vengono mantenuti. | Rinominare i punti a mano, se serve. |
| Un elemento più vecchio ha meno di dodici punti. | È stato posizionato con una versione precedente. | Posizionare ancora una volta un elemento qualsiasi in quel progetto. Ogni elemento riceve i punti mancanti. |
| I punti stanno accanto all'elemento, non su di esso. | L'elemento è stato posizionato lontano dall'origine con una versione precedente alla 1.1.0.1. | Posizionare ancora una volta un elemento qualsiasi in quel progetto. I punti vengono creati di nuovo nel posto giusto. |
| Un punto non è esattamente a metà larghezza o sul lato inferiore. | Il posto esatto è dentro il materiale o in aria, quindi il punto è mostrato sulla superficie accanto. | Nulla. Cliccandolo si posiziona comunque rispetto al posto esatto. Vedere [usage.md](usage.md). |
| Dopo un aggiornamento Fusion mostra ancora la vecchia versione sul pulsante. | Fusion esegue la copia nella sua cartella degli add-in, non quella scaricata. | Estrarre il nuovo ZIP sopra la vecchia cartella, poi arrestare ed eseguire l'add-in. Vedere [installation.md](installation.md). |
| La finestra di dialogo riparte con i valori predefiniti. | I valori ricordati durano solo finché Fusion non si chiude o l'add-in non si arresta. | – |
| Una distinta dei pezzi mostra lo stesso elemento su più righe. | Gli elementi sono stati posizionati con la versione 0.2.0, che creava ogni volta un nuovo componente. D'ora in poi viene riutilizzato solo il primo di essi. | Sostituire quelli vecchi con elementi posizionati di nuovo. |

## Limiti noti

- **Sinistra e destra:** i nomi sinistra/destra degli elementi d'angolo e per finestra sono stati abbinati a occhio alle
  schede di catalogo del produttore. Non sono confermati.
- **`S0/2 200 P`:** questo elemento è danneggiato nel file 3D del produttore. È ricostruito da `S0/2 250 P`.
- **Asse verticale:** l'add-in tratta sempre l'asse Z del progetto come "alto". Non guarda un'eventuale diversa
  impostazione di orientamento in Fusion.
- **Solo livello più alto:** gli elementi vengono sempre creati nel livello più alto del progetto (il componente radice), non nel
  componente attivo in quel momento.
- **Progetti collegati:** un elemento dentro un progetto collegato non viene riutilizzato. L'add-in crea un proprio componente.
- **Nessun controllo di compatibilità:** l'add-in non controlla se gli elementi si sovrappongono, se un giunto combacia o se una parete
  è costruibile.
- **Un elemento per esecuzione:** non c'è alcuna funzione per corsi interi o pareti intere.
- **Rotazione:** solo attorno all'asse verticale. Gli elementi non si possono inclinare nella finestra di dialogo.
- **Corpo condiviso:** tutte le copie di un elemento condividono un solo corpo. Modificarne una le modifica tutte.
- **Dimensioni:** le forme vengono dal file 3D del produttore e sono arrotondate a 0,1 mm. I quattro elementi per parete
  divisoria sono blocchi semplici senza profilo.
- **Nessuna affiliazione:** l'add-in non è affiliato a SYSTEM 3E. Non sostituisce i documenti di
  progettazione del produttore.
