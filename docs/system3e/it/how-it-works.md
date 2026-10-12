# Come funziona

Torna alla [panoramica](index.md).

## I file dell'add-in

La cartella installata `System3E` contiene:

| File o cartella | Scopo |
| --- | --- |
| `System3E.py` | Il comando: finestra di dialogo, posizionamento, punti |
| `system3e_core.py` | Funzioni di supporto generali: lingua, pulsante della barra degli strumenti, messaggi di errore, versione |
| `System3E.manifest` | Comunica a Fusion nome, autore, versione e che l'add-in si avvia con Fusion |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Tutti i testi, un file per lingua |
| `blocks/blocks.json` | La libreria degli elementi: la forma di tutti i 74 elementi |
| `blocks/<id>.png` | Un'immagine di anteprima per elemento, 74 in tutto |
| `resources/System3E/16x16.png`, `32x32.png`, `64x64.png` | L'icona del pulsante |

L'add-in legge solo questi file. Non scrive file e non apre alcuna connessione di rete.

## Avvio e arresto

Quando l'add-in si avvia:

1. Rileva la lingua (vedere [settings.md](settings.md)) e carica i testi.
2. Rimuove una definizione di pulsante rimasta da un'esecuzione precedente, se ce n'è una.
3. Crea il pulsante **Elemento SYSTEM 3E**. La versione presa dal manifest viene aggiunta tra parentesi.
4. Cerca il pannello **Create** degli strumenti per solidi nell'area di lavoro di progettazione e vi mette il pulsante.
   Se il pannello non viene trovato, mostra un messaggio e non aggiunge alcun pulsante.

Quando l'add-in si arresta, rimuove di nuovo il pulsante.

## La libreria degli elementi

`blocks/blocks.json` è un file di testo in formato JSON. Contiene:

- `unit`: sempre `mm`. Tutte le lunghezze nel file sono millimetri.
- `blocks`: un elenco di 74 elementi nell'ordine del catalogo.

Ogni elemento ha queste voci:

| Voce | Contenuto | Esempio |
| --- | --- | --- |
| `id` | Nome breve per i file, in minuscolo | `s1-wp` |
| `name` | Nome di catalogo | `S1 WP` |
| `family` | Uno tra `starter`, `basic`, `complementary`, `lintel`, `window`, `top`, `corner`, `partition` | `basic` |
| `size` | Lunghezza, larghezza, altezza in mm interi | `[707, 352, 300]` |
| `stack` | Altezza a cui poggia il corso successivo, mm | `250.0` |
| `points` | I punti d'angolo della forma, ciascuno come x, y, z in mm | `[0.0, 271.0, 200.0]` |
| `faces` | Le facce piane. Ognuna ha una direzione (`normal`) e uno o più contorni (`loops`). | – |

Un contorno è un elenco di numeri. Ogni numero indica uno dei `points`. Il primo contorno di una faccia è il suo bordo
esterno. Gli altri contorni sono fori nella faccia.

Ogni elemento giace con il suo angolo più basso in 0, 0, 0. La lunghezza corre lungo x, la larghezza (lo spessore della parete)
lungo y, l'altezza lungo z.

La libreria viene letta una volta sola, la prima volta che si apre la finestra di dialogo. L'immagine di anteprima di un elemento è il file
`blocks/<id>.png`.

## Come viene costruito un corpo

Gli elementi non sono salvati come file di Fusion. L'add-in costruisce ogni corpo dai punti e dalle facce:

1. Ogni punto dell'elemento diventa un vertice del corpo.
2. Ogni faccia diventa una faccia piana. La sua posizione viene dal suo primo punto e dalla sua direzione.
3. Ogni contorno diventa una catena chiusa di spigoli rettilinei.
4. Ogni spigolo è definito una volta sola e usato dalle sue due facce vicine, in direzioni opposte. Questo rende il
   corpo chiuso (un solido).
5. Fusion controlla il risultato per intero e crea il corpo. Se Fusion lo rifiuta, l'add-in mostra il messaggio
   "Impossibile creare l'elemento {0}:" con il motivo dato da Fusion.

Tutte le facce sono piane e tutti gli spigoli sono rettilinei. Non ci sono superfici curve.

## Componenti e riutilizzo

Quando si preme **OK**:

1. L'add-in passa in rassegna ogni elemento già presente nel progetto. I punti che mancano vengono aggiunti. I punti
   che non sono dove devono stare vengono tolti e creati di nuovo. Così gli elementi posizionati con una versione
   precedente vengono aggiornati.
2. L'add-in cerca nel progetto un componente di questo elemento.
   - Cerca un contrassegno invisibile (un attributo di Fusion, gruppo `System3E`, nome `block`) con l'`id` dell'elemento.
   - Gli elementi posizionati prima che esistesse il contrassegno vengono trovati tramite il nome `SYSTEM 3E <name>`.
   - I componenti senza corpo e i componenti di un progetto collegato vengono saltati.
3. **Trovato:** l'add-in inserisce un'altra copia di quel componente nel nuovo posto.
4. **Non trovato:** l'add-in costruisce il corpo, crea un nuovo componente di nome `SYSTEM 3E <name>` nel livello più alto
   del progetto, lo contrassegna, vi mette il corpo di nome `<name>` e aggiunge i dodici punti.

Poiché gli elementi uguali sono copie di un solo componente, una distinta dei pezzi li conta insieme.

In un progetto con timeline (Fusion lo chiama progetto parametrico) un corpo già pronto deve arrivare dentro una
"base feature". L'add-in ne crea una, vi mette il corpo e i punti e la chiude. In un progetto senza
timeline il corpo e i punti vengono aggiunti direttamente.

Se qualcosa non riesce mentre un elemento viene creato, l'add-in comunica a Fusion che il comando non è riuscito. Fusion allora
annulla ciò che era stato costruito fino a quel momento.

## I punti di costruzione

Ogni componente riceve dodici punti di costruzione. Con L = lunghezza, W = larghezza e S = `stack` dell'elemento,
rappresentano questi posti nelle coordinate proprie dell'elemento (mm):

| Nome | x | y | z |
| --- | --- | --- | --- |
| sotto davanti | 0 | W/2 | 0 |
| sotto centro | L/2 | W/2 | 0 |
| sotto dietro | L | W/2 | 0 |
| sopra davanti | 0 | W/2 | S |
| sopra centro | L/2 | W/2 | S |
| sopra dietro | L | W/2 | S |
| sopra centro destra | L/2 | 0 | S |
| sopra centro sinistra | L/2 | W | S |
| sotto centro destra | L/2 | 0 | 0 |
| sotto centro sinistra | L/2 | W | 0 |
| centro destra, 50 mm sopra | L/2 | 0 | 50 |
| centro sinistra, 50 mm sopra | L/2 | W | 50 |

I tre angoli offerti sotto **Posiziona da** non sono punti di costruzione. Con H = altezza si trovano in:

| Voce | x | y | z |
| --- | --- | --- | --- |
| Angolo inferiore anteriore destro | 0 | 0 | 0 |
| Angolo superiore anteriore destro | 0 | 0 | H |
| Angolo superiore anteriore sinistro | 0 | W | H |

Questi posti derivano dalle dimensioni esterne. Su un elemento con un maschio, una scanalatura o un incavo un tale
posto può essere dentro il materiale, dove il punto non si vede, oppure in aria. Allora il punto viene mostrato altrove:

1. dritto sopra o sotto, sulla faccia più vicina;
2. se sopra o sotto non c'è alcuna faccia, o se lì c'è già un altro punto: lungo la lunghezza;
3. altrimenti nel posto più vicino sulla superficie, poi di traverso alla parete.

Esempio `S1 WP`: "sopra centro" rappresenta l'altezza 250 mm ed è mostrato sopra il maschio a 300 mm. "sotto
centro" rappresenta l'altezza 0 ed è mostrato nella scanalatura a 50 mm. Sui mezzi elementi d'angolo `SNL/2` e
`SNP/2` non resta alcun posto libero per "sotto centro sinistra"; resta in aria.

Ogni punto porta contrassegni invisibili (gruppo di attributi `System3E`):

| Nome | Contenuto |
| --- | --- |
| `point` | La chiave del punto. Da essa l'add-in sa quali punti un componente ha già. |
| `shift` | Il percorso da dove il punto è mostrato al posto che rappresenta, in mm. |
| `asis` | Impostato quando Fusion ha messo il punto altrove e non è stato possibile correggerlo. Un tale punto viene lasciato com'è. |

Quando si fa clic su uno di questi punti, l'add-in aggiunge `shift` e così posiziona rispetto al posto che il punto
rappresenta. Una parete a giunti sfalsati risulta quindi uguale ovunque sia mostrato un punto.

Dopo aver creato un punto, l'add-in rilegge dove Fusion lo ha messo. Per un nuovo tipo di elemento posizionato
lontano dall'origine Fusion prendeva le coordinate come quelle dell'intero progetto; i punti stavano allora accanto
all'elemento. In quel caso l'add-in trova la copia del componente il cui posizionamento spiega la differenza, rimuove
il punto e lo crea di nuovo con coordinate corrette.

Il punto appartiene al componente. Quindi ogni copia di un elemento mostra gli stessi dodici punti nel proprio posto.

## Come viene calcolata la posizione

1. Il punto scelto sotto **Posiziona da** viene spostato nell'origine.
2. L'elemento viene ruotato attorno all'asse Z del valore di **Rotazione**.
3. L'elemento viene spostato sul punto cliccato più **Spostamento X**, **Spostamento Y**, **Spostamento Z**.
   Senza un punto cliccato viene usata l'origine (0, 0, 0).

Gli spostamenti vengono applicati dopo la rotazione. Quindi corrono lungo gli assi del progetto, non lungo l'elemento ruotato.

La posizione di un punto di schizzo cliccato viene presa nelle coordinate dell'intero progetto, non del suo schizzo.
La posizione di un punto di costruzione cliccato viene ricavata dal punto dentro il suo componente e dal
posizionamento della copia che è stata cliccata.

## Unità

| Dove | Unità |
| --- | --- |
| Libreria degli elementi `blocks.json` | mm |
| Campi **Spostamento X**, **Spostamento Y**, **Spostamento Z** | mostrati in mm |
| Campo **Rotazione** | mostrato in gradi |
| Dentro l'interfaccia di programmazione di Fusion | cm e radianti |

L'add-in divide per 10 ogni valore della libreria quando lo passa a Fusion. Non occorre convertire nulla.

## L'anteprima

Mentre la finestra di dialogo è aperta, Fusion chiede all'add-in un'anteprima dopo ogni modifica. L'add-in esegue allora gli stessi
passi che per **OK**. Fusion scarta questa anteprima ed esegue di nuovo i passi quando si preme **OK**.
Gli errori durante l'anteprima non vengono mostrati.
