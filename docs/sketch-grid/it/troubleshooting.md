# Risoluzione dei problemi

Tutti i testi sono citati dal file di lingua italiano. `{0}` e `{1}` stanno per valori che l'add-in inserisce.

## Dove compaiono i messaggi

| Posto | Quando |
| --- | --- |
| Riga **Risultato** nella finestra di dialogo | Un valore non è consentito. Allo stesso tempo **OK** è disattivato. |
| **OK** disattivato senza un testo | Non è selezionato alcun punto di schizzo (vedere la prima riga qui sotto). |
| Finestra di messaggio con il titolo **Griglia di schizzo** | Un controllo fallisce solo nel momento in cui si preme **OK**, oppure è successo qualcosa di imprevisto. |

## Messaggi sui dati inseriti

| Messaggio | Causa | Cosa fare |
| --- | --- | --- |
| "Seleziona esattamente un punto di schizzo." | **Punto** è vuoto, oppure l'oggetto selezionato non è un punto di schizzo. Di norma questo testo non viene mostrato; **OK** è semplicemente disattivato. | Fare clic su **Punto** e selezionare un punto di schizzo: l'origine dello schizzo o un punto collocato a mano. I punti sui corpi non si possono selezionare. |
| "La lunghezza deve essere maggiore di 0." | **Lunghezza (X)** è 0 o negativa. | Inserire un valore sopra 0. |
| "La profondità deve essere maggiore di 0." | **Profondità (Y)** è 0 o negativa. | Inserire un valore sopra 0. |
| "La distanza non può essere negativa." | **Distanza X** o **Distanza Y** è sotto 0. | Inserire 0 o più. Forme sovrapposte non sono possibili. |
| "Serve almeno una colonna." | **Colonne** è sotto 1. | Inserire 1 o più. Il campo stesso accetta solo da 1 a 2000, quindi di norma questo messaggio non dovrebbe comparire. |
| "Serve almeno una riga." | **Righe** è sotto 1. | Inserire 1 o più. Il campo stesso accetta solo da 1 a 2000, quindi di norma questo messaggio non dovrebbe comparire. |
| "L'area deve essere maggiore di 0 in entrambe le direzioni." | Modalità **Riempimento di un'area**: **Larghezza dell'area** o **Altezza dell'area** è 0 o negativa. | Inserire valori sopra 0 in entrambi i campi. |
| "In quest'area non entra nemmeno una forma. Servono almeno {0} × {1} mm." | Modalità **Riempimento di un'area**: l'area è più piccola di una forma. I due numeri sono la dimensione di una forma. | Rendere **Larghezza dell'area** e **Altezza dell'area** grandi almeno quanto i numeri del messaggio, oppure rendere la forma più piccola. |
| "Un poligono richiede da {0} a {1} lati." | **Lati** è fuori dall'intervallo da 3 a 24. | Inserire da 3 a 24. Il campo stesso accetta solo questo intervallo, quindi di norma questo messaggio non dovrebbe comparire. |
| "Il raggio / smusso deve essere maggiore di 0." | **Spigoli** è **Raccordati** o **Smussati**, e **Raggio / smusso** è 0 o negativo. | Inserire un valore sopra 0, oppure impostare **Spigoli** su **Vivi**. |
| "Il raggio / smusso può essere al massimo di {0} mm, metà del lato più corto." | **Raggio / smusso** è più grande della metà della minore tra **Lunghezza (X)** e **Profondità (Y)**. Il numero è il valore massimo consentito. | Inserire al massimo il valore del messaggio, oppure rendere il rettangolo più grande. |
| "Sarebbero {0} forme. Ne sono consentite al massimo {1} - oltre, Fusion si blocca." | Colonne × righe è più di 2000. Il primo numero è ciò che darebbero i valori inseriti. | Usare meno colonne o meno righe. Nella modalità **Riempimento di un'area**: un'area più piccola, forme più grandi o distanze più grandi. Per avere più forme, disegnare più griglie. |

Se più valori sono sbagliati, viene mostrato solo il primo problema. Correggerlo, poi compare il successivo.

## Messaggi sull'add-in stesso

Questi compaiono in una finestra di messaggio. `{0}` viene sostituito da un rapporto tecnico di errore (un traceback di Python).

| Messaggio | Causa | Cosa fare |
| --- | --- | --- |
| "Nessun pannello della barra degli strumenti adatto trovato." | All'avvio l'add-in non ha trovato né il pannello CREATE della barra degli strumenti dello schizzo né il pannello CREATE della scheda SOLID. Non viene aggiunto alcun pulsante. | Passare all'area di lavoro **Design**, poi arrestare ed eseguire di nuovo l'add-in. Se resta, segnalarlo insieme alla versione di Fusion. |
| "Errore durante la creazione della geometria: {0}" | Qualcosa di imprevisto è fallito durante il disegno dopo **OK**. | Riprovare. Se resta, segnalarlo con il testo completo. |
| "Errore durante la costruzione della finestra di dialogo: {0}" | Qualcosa di imprevisto è fallito mentre veniva costruita la finestra di dialogo. | Arrestare ed eseguire di nuovo l'add-in. Se resta, segnalarlo con il testo completo. |
| "Avvio non riuscito: {0}" | Qualcosa di imprevisto è fallito durante l'avvio dell'add-in. | Controllare che la cartella sia completa e si chiami ancora `SketchGrid` (vedere [installation.md](installation.md)). Eseguirlo di nuovo. |
| "Arresto non riuscito: {0}" | Qualcosa di imprevisto è fallito durante l'arresto dell'add-in. | Riavviare Fusion. |

Le segnalazioni vanno a <https://github.com/sorglos-it/fusion360/issues>.

## Altri problemi

| Problema | Causa | Cosa fare |
| --- | --- | --- |
| **OK** è in grigio e **Risultato** mostra un risultato normale | Non è selezionato alcun punto. | Selezionare un punto di schizzo in **Punto**. |
| Il punto su cui si è fatto clic prima non è nella finestra di dialogo | Non è stato possibile riprendere il punto. Dalla versione 1.1.0.0 in questo caso la finestra di dialogo continua a funzionare (verificato solo offline, non all'interno di Fusion). | Selezionare il punto nella finestra di dialogo. |
| Nessuna anteprima mentre si scrive | In quel momento un valore non è consentito. L'anteprima resta vuota senza un messaggio. | Leggere la riga **Risultato** e correggere il valore. |
| Il pulsante manca | L'add-in non è in esecuzione, oppure non è stato trovato alcun pannello. | Aprire **Utilities → ADD-INS → Add-Ins**, selezionare **SketchGrid**, premere **Run**. |
| Il pulsante mostra un vecchio numero di versione | Il vecchio add-in è ancora in memoria. | Arrestare l'add-in, sostituire la cartella, eseguirlo di nuovo. |
| La finestra di dialogo è in inglese anche se Fusion è impostato su un'altra lingua | Esistono solo tedesco, inglese, spagnolo, francese e italiano. Oppure la lingua è stata cambiata mentre l'add-in era in esecuzione. | Arrestare ed eseguire di nuovo l'add-in. Vedere [settings.md](settings.md#lingua). |
| Un testo compare come chiave, per esempio `in.point` | I file di lingua mancano o sono danneggiati. | Installare di nuovo l'add-in dallo ZIP. |
| La griglia non riempie l'area | Vengono disegnate solo forme complete. | È voluto. Vedere [usage.md](usage.md#riempimento-di-unarea). |
| Un poligono regolare è molto più piccolo di lunghezza × profondità | Con **Regolare**, la minore tra lunghezza e profondità determina la dimensione. | Usare valori simili per lunghezza e profondità, oppure togliere la spunta da **Regolare**. |
| La finestra di dialogo riparte con i valori standard | I valori ricordati durano solo finché l'add-in non si arresta o Fusion non si chiude. | Inserirli di nuovo. |

## Limiti noti

Non confermati all'interno di Fusion (trovati in una revisione del codice):

- **Le asole e i rettangoli con spigoli raccordati o smussati** vengono disegnati come linee e archi separati. I loro estremi stanno nello stesso punto, ma potrebbero non restare collegati quando si trascina una parte della forma. I poligoni e i rettangoli a spigoli vivi non ne sono interessati in questo modo.
- **Il limite di 2000 conta le forme, non le curve.** Un poligono con 24 lati sono 24 linee. Una grande griglia di poligoni, asole o rettangoli tagliati può quindi essere lenta anche se rientra nel limite.

Dal codice:

- Si possono selezionare solo punti di schizzo. Vertici di corpi o punti su spigoli no.
- La griglia è sempre parallela agli assi X e Y dello schizzo. Nella finestra di dialogo non si può ruotare.
- Il poligono ha sempre un vertice che punta verso l'alto. La finestra di dialogo non ha un campo per ruotarlo.
- Solo il rettangolo può avere spigoli raccordati o smussati.
- Le distanze non possono essere negative. Le forme non possono sovrapporsi.
- Le forme sono semplice geometria di schizzo. Cambiare un valore in seguito non aggiorna una griglia esistente.
- L'add-in non aggiunge quote né vincoli. Dopo il disegno la griglia non è legata al punto.
- I valori ricordati vanno persi quando l'add-in si arresta o Fusion si chiude.
- Nella modalità **Riempimento di un'area**, il resto vuoto viene centrato solo quando **Il punto si trova nella griglia** è **Al centro** (o una voce "al centro" per quella sola direzione).
