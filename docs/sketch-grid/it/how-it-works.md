# Come funziona

## File

L'add-in installato è una sola cartella, `SketchGrid`:

| File | Scopo |
| --- | --- |
| `SketchGrid.py` | L'add-in vero e proprio: finestra di dialogo, calcolo della griglia, controlli, disegno. |
| `sketchgrid_core.py` | Funzioni di supporto condivise, non specifiche di questo add-in: leggere i file di lingua, trovare la lingua, trovare il pannello della barra degli strumenti, tenere in vita i gestori degli eventi, mostrare gli errori imprevisti, leggere la versione. |
| `SketchGrid.manifest` | Descrizione per Fusion: autore, versione, sistemi supportati (Windows e macOS), avvio insieme a Fusion. |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Tutti i testi, un file per lingua. `en.xml` è il riferimento. |
| `resources/SketchGrid/16x16.png`, `32x32.png`, `64x64.png` | L'icona del pulsante in tre dimensioni. |

L'add-in legge solo la propria cartella. Non scrive file e non apre connessioni di rete.

## Avvio e arresto

All'avvio (`run`):

1. Viene rilevata la lingua e caricato il file di lingua corrispondente.
2. Una definizione di comando rimasta da un avvio precedente viene eliminata.
3. Viene creato il comando. Il suo nome è il testo **Griglia di schizzo** più la versione del manifest tra parentesi.
4. L'add-in cerca un pannello della barra degli strumenti: prima il pannello con l'id `SketchCreatePanel`, poi `SolidCreatePanel`; ciascuno prima nell'area di lavoro Design, poi tra tutti i pannelli. Se non ne esiste nessuno, compare il messaggio "Nessun pannello della barra degli strumenti adatto trovato." e non viene aggiunto alcun pulsante.
5. Il pulsante viene aggiunto al pannello e mostrato direttamente sulla barra degli strumenti.

All'arresto (`stop`) il pulsante e il comando vengono rimossi e i gestori degli eventi vengono rilasciati.

## Cosa succede mentre la finestra di dialogo è aperta

| Evento | Cosa fa l'add-in |
| --- | --- |
| La finestra di dialogo si apre | Costruisce tutti i campi con i valori ricordati. Prova a riprendere un punto di schizzo selezionato in precedenza. Se non ci riesce, la finestra di dialogo resta utilizzabile e il punto viene selezionato nella finestra di dialogo. (Verificato solo offline, non all'interno di Fusion.) |
| Un campo cambia | Mostra o nasconde i campi che appartengono alla modalità e alla forma scelte. Ricalcola la riga **Risultato**. |
| Fusion chiede se i dati inseriti sono validi | Esegue tutti i controlli. Se uno fallisce, **OK** viene disattivato. |
| Fusion chiede un'anteprima | Esegue tutti i controlli e disegna la griglia come anteprima. Se un controllo fallisce, non viene disegnato nulla e non viene segnalato nulla. |
| **OK** | Esegue di nuovo tutti i controlli, disegna la griglia, poi ricorda i valori. |

L'anteprima non viene riutilizzata come risultato finale. Con **OK** la griglia viene disegnata di nuovo.

## Unità

- All'interno tutte le lunghezze sono in centimetri. È l'unità interna di Fusion, qualunque unità mostri il documento.
- I campi di lunghezza nella finestra di dialogo sono creati con l'unità `mm`.
- Per la riga **Risultato** e per i messaggi, i valori vengono convertiti in millimetri (× 10) e mostrati con due decimali.
- I confronti ammettono una tolleranza minima di 0.000000001 cm, così che il rumore di arrotondamento non faccia scattare un messaggio.

## Come viene calcolata la griglia

Il calcolo è fatto da `grid_layout()`. Non usa funzioni di Fusion.

### Fase 1: dimensione di una forma

Di norma una forma occupa esattamente lunghezza × profondità.

Eccezione: un poligono con **Regolare** spuntato. Occupa meno spazio. La sua dimensione reale viene misurata:

1. I vertici del poligono vengono posti su un cerchio di raggio 1, con il primo vertice rivolto verso l'alto.
2. Si misurano la larghezza e l'altezza del riquadro più piccolo attorno a questi vertici.
3. Entrambe vengono moltiplicate per la metà della minore tra lunghezza e profondità.

Esempio: 6 lati, lunghezza 10 mm, profondità 5 mm danno 4.33 × 5.00 mm.

### Fase 2: passo

Passo significa la distanza da una forma allo stesso punto della forma successiva.

- passo X = dimensione di una forma in X + **Distanza X**
- passo Y = dimensione di una forma in Y + **Distanza Y**

### Fase 3: numero di colonne e righe

**Colonne e righe:** si usano i numeri della finestra di dialogo.

**Riempimento di un'area:** n forme richiedono n dimensioni e n − 1 distanze. Quindi:

- colonne = (larghezza dell'area + distanza X) ÷ passo X, arrotondato per difetto
- righe = (altezza dell'area + distanza Y) ÷ passo Y, arrotondato per difetto

Esempio: (100 + 2) ÷ 12 = 8.5, quindi 8 colonne.

Se colonne × righe è più di 2000, la griglia viene rifiutata.

### Fase 4: dimensione totale

- larghezza totale = colonne × passo X − distanza X
- altezza totale = righe × passo Y − distanza Y

Esempio: 8 × 12 − 2 = 94 mm.

### Fase 5: posizione (punto di riferimento e scostamento)

Il punto di riferimento è la voce scelta in **Il punto si trova nella griglia**. Ogni voce corrisponde a due fattori tra 0 e 1: quanto il punto dista dal bordo sinistro e dal bordo inferiore della griglia, come quota della dimensione totale.

| Voce | Fattore X | Fattore Y |
| --- | --- | --- |
| Al centro | 0.5 | 0.5 |
| In basso a sinistra | 0 | 0 |
| In basso a destra | 1 | 0 |
| In alto a sinistra | 0 | 1 |
| In alto a destra | 1 | 1 |
| In basso al centro | 0.5 | 0 |
| In alto al centro | 0.5 | 1 |
| A sinistra al centro | 0 | 0.5 |
| A destra al centro | 1 | 0.5 |

L'angolo in basso a sinistra della griglia, misurato dal punto selezionato:

- X = −fattore X × larghezza totale + **Scostamento X**
- Y = −fattore Y × altezza totale + **Scostamento Y**

Esempio: griglia 94 × 26 mm, **Al centro**, nessuno scostamento: l'angolo in basso a sinistra si trova 47 mm a sinistra e 13 mm sotto il punto.

Gli scostamenti vengono aggiunti solo a questo punto. Non cambiano il numero di forme, nemmeno nella modalità **Riempimento di un'area**.

### Fase 6: le singole forme

`cell_centres()` percorre la griglia riga per riga, dalla riga più bassa verso l'alto, in ogni riga da sinistra a destra. Per ogni forma restituisce l'angolo in basso a sinistra del suo posto:

- X = angolo della griglia X + numero di colonna × passo X
- Y = angolo della griglia Y + numero di riga × passo Y

I numeri di colonna e di riga partono da 0. Il nome della funzione è storico; restituisce angoli, non centri.

Il codice di disegno aggiunge metà della dimensione di una forma per ottenere il centro, e aggiunge la posizione del punto selezionato nello schizzo.

Tutte le posizioni sono nelle coordinate dello schizzo a cui appartiene il punto. La griglia è quindi sempre parallela agli assi X e Y di quello schizzo.

## Come viene disegnata ogni forma

| Forma | Caso | Disegnata come |
| --- | --- | --- |
| Rettangolo | spigoli **Vivi** | il rettangolo a due punti di Fusion, dall'angolo in basso a sinistra a quello in alto a destra |
| Rettangolo | **Raccordati**, raggio uguale alla metà di entrambi i lati | un cerchio |
| Rettangolo | **Raccordati**, negli altri casi | fino a 4 linee e 4 archi |
| Rettangolo | **Smussati** | fino a 4 linee per i lati e 4 linee per i tagli |
| Cerchio / ellisse | lunghezza uguale a profondità | un cerchio |
| Cerchio / ellisse | negli altri casi | un'ellisse; la maggiore delle due viene passata a Fusion come asse principale, perché altrimenti Fusion rifiuta l'ellisse |
| Asola | lunghezza uguale a profondità | un cerchio |
| Asola | negli altri casi | 2 linee e 2 archi semicircolari; gli archi stanno alle due estremità della direzione più lunga, il loro raggio è la metà di quella più corta |
| Poligono | sempre | una linea per lato |

Dettagli:

- **Rettangolo raccordato o smussato:** `corner_outline()` restituisce il contorno come elenco di linee e archi, in senso antiorario a partire dal bordo inferiore. Ogni arco è dato da tre punti: inizio, un punto a metà dell'arco, fine. Quando il raggio o lo smusso è esattamente la metà di un lato, il tratto rettilineo su quel lato non ha lunghezza e viene omesso.
- **Poligono:** il primo vertice punta verso l'alto. Senza **Regolare**, i vertici vengono allungati in modo che il riquadro più piccolo attorno a essi misuri esattamente lunghezza × profondità. Con **Regolare**, entrambe le direzioni vengono scalate per la metà della minore tra lunghezza e profondità. In entrambi i casi il poligono è centrato sul proprio riquadro, non sul proprio cerchio. Questo conta per i numeri dispari di lati: una forma a cinque lati ha un vertice in alto ma una base piatta.
- **Collegamento delle curve:** il poligono viene disegnato come catena. Ogni linea parte dal punto finale della linea precedente e l'ultima si chiude sul punto iniziale della prima. L'asola e il rettangolo raccordato o smussato vengono disegnati in modo diverso: ogni linea e ogni arco viene creato per conto suo a partire dalle coordinate. I loro estremi stanno nello stesso posto, ma non vengono creati come punti condivisi. Vedere [limiti noti](troubleshooting.md#limiti-noti).
- L'add-in in sé non aggiunge quote né vincoli. Se Fusion ne aggiunga di propri al rettangolo a due punti non lo decide l'add-in.

Mentre la griglia viene disegnata, si dice allo schizzo di non ricalcolare dopo ogni singola curva (`isComputeDeferred`). Ricalcola una volta sola alla fine. L'impostazione viene ripristinata in ogni caso, anche dopo un errore.

## I controlli

Ordine in cui vengono eseguiti i controlli:

1. È selezionato esattamente un punto di schizzo.
2. Se la forma è un poligono: lati tra 3 e 24.
3. Lunghezza maggiore di 0.
4. Profondità maggiore di 0.
5. Nessuna delle due distanze negativa.
6. Modalità **Riempimento di un'area**: entrambi i valori dell'area maggiori di 0; poi entrano almeno una colonna e una riga.
7. Modalità **Colonne e righe**: almeno una colonna, almeno una riga.
8. Colonne × righe al massimo 2000.
9. Se la forma è un rettangolo e gli spigoli non sono **Vivi**: raggio / smusso maggiore di 0 e al massimo la metà del lato più corto. Un valore troppo grande viene rifiutato, non ridotto in silenzio.

Il primo controllo che fallisce decide il messaggio. I testi sono elencati in [troubleshooting.md](troubleshooting.md).

La riga **Risultato** esegue solo i controlli da 3 a 9. Un controllo 1 o 2 fallito disattiva quindi **OK** senza un testo nella riga **Risultato**.

## Testi e lingua

- Ogni file di lingua è un elenco di chiavi e testi. Il codice conosce solo le chiavi.
- I posti per i valori sono scritti nei testi come `{0}`, `{1}` e così via e vengono riempiti dall'add-in.
- L'inglese viene caricato per primo come ripiego. Una chiave che manca nella lingua attiva viene presa dall'inglese. Una chiave che manca dappertutto viene mostrata come la chiave stessa.
- Come viene scelta la lingua: vedere [settings.md](settings.md#lingua).
