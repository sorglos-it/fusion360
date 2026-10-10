# Come funziona

## File

Tutto ciò che serve all'add-in sta in una sola cartella, `Dovetail`:

| File | Scopo |
|---|---|
| `Dovetail.py` | L'intero programma: lingua, geometria, disegno, finestra di dialogo, avvio e arresto |
| `Dovetail.manifest` | Descrizione per Fusion: nome, autore, versione, sistemi supportati, avvio insieme a Fusion |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Tutti i testi, un file per lingua |
| `resources/Dovetail/` | Icona della barra degli strumenti a 16, 32 e 64 pixel |
| `resources/nudge_left/`, `nudge_center/`, `nudge_right/` | Icone dei tre pulsanti **Sposta** |

L'add-in legge solo questi file. Non scrive file e non apre connessioni di rete.

## Avvio e arresto

All'avvio l'add-in:

1. sceglie la lingua (vedere [settings.md](settings.md#lingua)),
2. registra il comando con il nome "Coda di rondine" più la versione del manifest tra parentesi,
3. cerca un pannello della barra degli strumenti e vi mette il pulsante (vedere [installation.md](installation.md#primo-avvio-in-fusion)).

All'arresto toglie di nuovo il pulsante e il comando.

## Dalla linea alla fascia

### 1. Un righello lungo la linea

Per ogni linea selezionata l'add-in crea un proprio sistema di misura:

- **s** corre lungo la linea, dal punto iniziale (0) al punto finale (la lunghezza della linea).
- **h** corre ad angolo retto rispetto alla linea, verso il lato a cui puntano i denti.

Senza **Inverti direzione**, h punta a sinistra guardando dal punto iniziale al punto finale.
Con **Inverti direzione**, h punta a destra.

### 2. Dove stanno i denti

Il centro del gruppo si trova a: lunghezza della linea ÷ 2 + Spostamento.
I denti sono disposti ai due lati di esso, ciascuno a un **Passo** di distanza dal successivo.

### 3. Il profilo nominale

Il profilo nominale è il bordo comune che i due pezzi avrebbero senza alcun gioco. È una sola linea aperta a zigzag:

1. parte dal punto iniziale della linea,
2. corre lungo la linea fino al primo dente,
3. sale lungo un fianco del dente, attraversa la punta e scende lungo l'altro fianco,
4. prosegue lungo la linea fino al dente successivo,
5. termina nel punto finale della linea.

La punta è un solo punto per un triangolo e due punti per un trapezio o un rettangolo.

Con **Rispecchia la geometria**, la prima metà dei denti punta verso il lato opposto (meno h), la seconda metà verso
il lato normale (più h).

### 4. Ripartire la tolleranza

Si creano due copie del profilo nominale, ciascuna spostata di lato di una distanza fissa (una copia parallela):

- il profilo della **cava** è spostato verso il lato dei denti. La cava diventa più grande.
- il profilo del **tenone** è spostato verso l'altro lato. Il tenone diventa più piccolo.

**La linea è** decide di quanto viene spostato ciascuno:

| Voce | Cava spostata di | Tenone spostato di |
|---|---|---|
| Linea mediana | ½ × Tolleranza | ½ × Tolleranza |
| Bordo della cava | 0 (resta sul profilo nominale) | Tolleranza |
| Bordo del tenone | Tolleranza | 0 (resta sul profilo nominale) |

Le due quote sommate danno sempre l'intera tolleranza. Poiché entrambi i profili sono copie parallele dello stesso profilo nominale,
il gioco tra loro è uguale dappertutto: alla base, sui fianchi e sulla punta.

Come viene fatto lo spostamento:

- Ogni tratto rettilineo viene spostato di lato della distanza.
- A ogni spigolo i due tratti spostati vengono allungati o accorciati finché si incontrano (uno spigolo a quartabuono).
- I due estremi vengono spostati diritti di lato, così entrambi i profili iniziano a s = 0 e finiscono a s = lunghezza della linea.

### 5. La fascia chiusa

I due profili vengono uniti in un solo anello chiuso:

1. lungo il profilo della cava dall'inizio alla fine della linea,
2. di traverso fino al profilo del tenone alla fine della linea,
3. indietro lungo il profilo del tenone,
4. di traverso fino al punto di partenza.

L'interno di questo anello è il gioco stesso. È una fascia larga esattamente la tolleranza che segue il profilo dei denti.
Tagliandola da un solo solido restano due pezzi che si incastrano.

### 6. Disegno

- La fascia viene disegnata come catena di linee di schizzo rette. Ogni linea parte dal punto finale della precedente e
  l'ultima si richiude sulla prima. Il contorno è quindi collegato.
- Le linee finiscono nello schizzo a cui appartiene la linea selezionata.
- Durante il disegno si dice allo schizzo di non ricalcolare dopo ogni singola linea. Ricalcola una volta sola alla fine.
- Con OK, e solo se la casella è spuntata, la linea originale viene prima convertita in geometria di costruzione. Una linea
  normale attraverserebbe la fascia e la dividerebbe in due aree.
- L'add-in non aggiunge quote né vincoli.

## I controlli

Prima di disegnare qualcosa, l'intera selezione viene calcolata una volta. Il disegno parte solo se ogni linea supera i controlli.
Una linea non valida in fondo alla selezione non può quindi lasciare lo schizzo disegnato a metà.

Per ogni linea i controlli vengono eseguiti in quest'ordine:

| # | Controllo | Chiave del messaggio se fallisce |
|---|---|---|
| 1 | La linea ha una lunghezza | `err.zero_length` |
| 2 | La larghezza è maggiore di 0 | `err.width` |
| 3 | La profondità è maggiore di 0 | `err.depth` |
| 4 | La tolleranza è maggiore di 0 | `err.tolerance_zero` |
| 5 | Il numero è almeno 1 | `err.count` |
| 6 | Rispecchiamento: il numero è pari | `err.mirror_even` |
| 7 | Rispecchiamento: è scelta la linea mediana | `err.mirror_center` |
| 8 | Rispecchiamento: lo spostamento è 0 | `err.mirror_offset` |
| 9 | Trapezio: l'angolo dei fianchi è entro ±89 gradi | `err.angle_range` |
| 10 | Trapezio: la punta conserva una larghezza | `err.angle_negative` |
| 11 | Due o più denti: il passo è maggiore di 0 | `err.spacing_positive` |
| 12 | Due o più denti: il passo è almeno pari al minimo | `err.spacing_too_small` |
| 13 | I denti più la distanza dagli estremi stanno sulla linea | `err.offset_range` oppure `err.does_not_fit` |
| 14 | Nessuno spigolo a quartabuono si allontana più di 12 × la distanza di spostamento | `err.miter_runaway` |
| 15 | Entrambi i profili iniziano e finiscono esattamente agli estremi della linea e restano tra di essi | `err.does_not_fit` |
| 16 | Nessun tratto di un profilo si è ridotto a nulla | `err.tolerance_eats_tooth` |
| 17 | Nessun profilo incrocia se stesso | `err.tolerance_eats_tooth` |
| 18 | Resta un'altezza del dente | `err.tolerance_eats_tooth` |
| 19 | L'altezza del dente rimasta è almeno il 5 % della profondità | `err.tolerance_vs_depth` |
| 20 | Il doppio della tolleranza è minore della larghezza | `err.tolerance_vs_width` |

Con più linee, un errore viene racchiuso in `err.on_line`, che indica la posizione della linea nella selezione.

I testi di tutti i messaggi sono elencati in [troubleshooting.md](troubleshooting.md).

### Cosa fa la finestra di dialogo quando un controllo fallisce

- Finché la finestra di dialogo è aperta: l'anteprima sparisce e **OK** è in grigio. Il testo del messaggio **non** viene mostrato.
- Se è l'esecuzione stessa a fallire dopo OK: una finestra di messaggio mostra il testo e l'esecuzione viene segnalata a Fusion
  come fallita, così che Fusion annulli le linee già disegnate. Questo annullamento non è stato confermato all'interno di Fusion.

## Unità

| Dove | Unità |
|---|---|
| Campi della finestra di dialogo per le lunghezze | millimetri |
| Campo della finestra di dialogo per l'angolo | gradi |
| Numeri nei messaggi | millimetri, due decimali |
| All'interno del programma | centimetri e radianti (le unità interne di Fusion) |

Piccoli valori fissi nel codice:

| Valore | Grandezza | Uso |
|---|---|---|
| Distanza aggiuntiva | 0.01 mm | aggiunta al passo minimo e alla distanza dagli estremi della linea |
| Tratto più corto | 0.00001 mm | un tratto di profilo più corto di così conta come "senza lunghezza" |
| Limite dello spigolo a quartabuono | 12 × distanza di spostamento | oltre questo valore uno spigolo conta come uno che sbanda |
| Angolo dei fianchi massimo | sotto 89 gradi | |

## L'altezza viene ignorata

L'add-in legge solo i valori X e Y degli estremi della linea nello schizzo e disegna la fascia all'altezza 0 dello
schizzo. Una linea in uno schizzo 3D, o una che esce dal piano dello schizzo, viene trattata come se fosse piana.

## Cosa è cambiato nella 1.1.0.0

La versione 1.1.0.0 ha modificato la geometria (costruita la prima volta come 1.0.0.1):

- I denti restano lontani dagli estremi della linea della tolleranza più 0.01 mm. Proprio all'estremo il profilo della cava prima
  andava oltre la linea e tornava indietro, e ne risultava un anello che incrociava se stesso. Lo spostamento massimo è più piccolo di questa quantità.
- Due denti richiedono 0.01 mm di passo in più. Esattamente al vecchio minimo un tratto del profilo non aveva lunghezza.
- Un profilo che incrocerebbe se stesso viene rifiutato invece di essere disegnato.
- Un'esecuzione fallita viene annullata.

Queste modifiche sono state verificate **solo offline**, anche con 34.317 profili validi casuali, nessuno dei quali incrociava se stesso.
**Non sono ancora confermate all'interno di Fusion**.
