# Utilizzo

Torna alla [panoramica](index.md).

L'add-in ha una sola funzione: il comando **Elemento SYSTEM 3E**. Posiziona un elemento per pareti a ogni esecuzione.

## Posizionare un elemento

1. Aprire un progetto in Fusion.
2. Nella scheda **SOLID**, nel pannello **Create**, fare clic su **Elemento SYSTEM 3E**.
3. **Punto**: fare clic sul posto per l'elemento. Si può cliccare
   - un punto di schizzo,
   - uno spigolo d'angolo di un corpo,
   - un punto di costruzione – compresi i punti di un elemento posizionato in precedenza.

   Se non si clicca nulla, l'elemento va all'origine del progetto. Lo dice il testo di richiesta:
   "Seleziona un punto (nessuno: origine)".
4. **Famiglia**: scegliere il gruppo di elementi.
5. **Elemento**: scegliere l'elemento. Ogni voce mostra il nome e le dimensioni in mm come lunghezza x larghezza x altezza,
   per esempio `S1 WP   707 x 352 x 300`.
6. Guardare l'immagine sotto l'elenco. Mostra l'elemento scelto.
7. **Posiziona da**: scegliere quale punto dell'elemento finisce sul punto cliccato. Vedere sotto.
8. **Rotazione**: digitare un angolo se l'elemento deve essere ruotato.
9. **Spostamento X**, **Spostamento Y**, **Spostamento Z**: digitare una distanza se l'elemento deve essere allontanato dal punto.
10. Premere **OK**.

Si può anche cliccare prima il punto e poi il pulsante. L'add-in riporta il punto nel campo **Punto**.

Mentre la finestra di dialogo è aperta, Fusion mostra l'elemento al suo posto come anteprima. Viene creato in modo definitivo quando
si preme **OK**.

## Famiglia ed elemento

Ci sono otto famiglie con 74 elementi. L'ordine è quello del catalogo del produttore.

| Famiglia | Elementi |
| --- | --- |
| Partenza | 12 |
| Base | 6 |
| Complementare | 8 |
| Architrave | 8 |
| Telaio finestra | 6 |
| Chiusura | 12 |
| Angolo | 18 |
| Parete divisoria | 4 |

Quando si cambia famiglia, l'elenco degli elementi viene riempito di nuovo e viene selezionato il suo primo elemento.

Tutti gli elementi, con le dimensioni in mm (lunghezza x larghezza x altezza):

**Partenza**

| Elemento | Dimensioni |
| --- | --- |
| S0 200 WP | 707 x 352 x 200 |
| S0 200 W | 704 x 352 x 200 |
| S0/2 200 W | 352 x 352 x 200 |
| S0/2 200 P | 355 x 352 x 200 |
| S0 250 WP | 707 x 352 x 250 |
| S0 250 W | 704 x 352 x 250 |
| S0/2 250 W | 352 x 352 x 250 |
| S0/2 250 P | 355 x 352 x 250 |
| S0 300 WP | 707 x 352 x 300 |
| S0 300 W | 704 x 352 x 300 |
| S0/2 300 W | 352 x 352 x 300 |
| S0/2 300 P | 355 x 352 x 300 |

**Base**

| Elemento | Dimensioni |
| --- | --- |
| S1 WP | 707 x 352 x 300 |
| S1 W | 704 x 352 x 300 |
| S1/2 W | 352 x 352 x 300 |
| S1/2 P | 355 x 352 x 300 |
| ST W | 222 x 352 x 300 |
| ST P | 225 x 352 x 300 |

**Complementare**

| Elemento | Dimensioni |
| --- | --- |
| EU 150 WP | 707 x 352 x 150 |
| EU 150 W | 704 x 352 x 150 |
| EU/2 150 W | 352 x 352 x 150 |
| EU/2 150 P | 355 x 352 x 150 |
| EU 200 WP | 707 x 352 x 200 |
| EU 200 W | 704 x 352 x 200 |
| EU/2 200 W | 352 x 352 x 200 |
| EU/2 200 P | 355 x 352 x 200 |

**Architrave**

| Elemento | Dimensioni |
| --- | --- |
| EN WP | 707 x 352 x 170 |
| EN W | 704 x 352 x 170 |
| EN/2 W | 352 x 352 x 170 |
| EN/2 P | 355 x 352 x 170 |
| EPN WP L | 707 x 352 x 300 |
| EPN W L | 704 x 352 x 300 |
| EPN WP P | 707 x 352 x 300 |
| EPN W P | 704 x 352 x 300 |

**Telaio finestra**

| Elemento | Dimensioni |
| --- | --- |
| EO/2 WP L | 707 x 352 x 300 |
| EO/2 WP P | 707 x 352 x 300 |
| EO/2 W P | 704 x 352 x 300 |
| EO/2 200 WP L | 707 x 352 x 300 |
| EO/2 200 WP P | 707 x 352 x 300 |
| EO/2 200 W P | 704 x 352 x 300 |

**Chiusura**

| Elemento | Dimensioni |
| --- | --- |
| EWN WP L | 707 x 352 x 250 |
| EWN W L | 704 x 352 x 250 |
| EWN WP P | 707 x 352 x 250 |
| EWN W P | 704 x 352 x 250 |
| SZ/EO WP | 707 x 352 x 250 |
| SZ/EO W | 704 x 352 x 250 |
| SZ/2 W | 352 x 352 x 250 |
| SZ/2 P | 355 x 352 x 250 |
| SZ/EO 200 WP | 707 x 352 x 200 |
| SZ/EO 200 W | 704 x 352 x 200 |
| SZ/2 200 W | 352 x 352 x 200 |
| SZ/2 200 P | 355 x 352 x 200 |

**Angolo**

| Elemento | Dimensioni |
| --- | --- |
| SNL | 704 x 352 x 300 |
| SNL/2 | 352 x 352 x 300 |
| SNP | 704 x 352 x 300 |
| SNP/2 | 352 x 352 x 300 |
| ENL | 704 x 352 x 300 |
| ENP | 704 x 352 x 300 |
| SZL | 704 x 352 x 250 |
| SZP | 704 x 352 x 250 |
| EWNL | 704 x 352 x 250 |
| EWNP | 704 x 352 x 250 |
| EO/2 LT | 704 x 352 x 300 |
| EO/2 LP | 698 x 352 x 300 |
| EO/2 PT | 704 x 352 x 300 |
| EO/2 PP | 704 x 352 x 300 |
| EO/2 200 LT | 704 x 352 x 300 |
| EO/2 200 LP | 704 x 352 x 300 |
| EO/2 200 PT | 704 x 352 x 300 |
| EO/2 200 PP | 704 x 352 x 300 |

**Parete divisoria**

| Elemento | Dimensioni |
| --- | --- |
| D1 115 | 704 x 115 x 250 |
| D1/2 115 | 352 x 115 x 250 |
| D1 175 | 704 x 175 x 200 |
| D1/2 175 | 352 x 175 x 200 |

Note sull'elenco:

- Le dimensioni sono le dimensioni esterne salvate nella libreria degli elementi, arrotondate a mm interi.
- I nomi sono i nomi di catalogo. L'add-in non li traduce.
- I nomi sinistra/destra degli elementi d'angolo e per finestra sono stati abbinati a occhio alle schede di catalogo
  del produttore. **Non sono confermati**. Controllare l'immagine e il corpo posizionato prima di fidarsi del nome.
- `S0/2 200 P` è danneggiato nel file 3D del produttore. La sua forma è ricostruita da `S0/2 250 P`.
- I quattro elementi per parete divisoria sono blocchi semplici. Le loro dimensioni vengono dalle schede di catalogo.

## L'immagine di anteprima

- L'immagine mostra l'elemento scelto come vista ombreggiata in grigio, visto da davanti a sinistra e dall'alto.
- Cambia quando si cambia **Famiglia** o **Elemento**.
- Le immagini sono disegnate a partire dalla libreria degli elementi. Non sono prese dal catalogo del produttore.

## Direzioni su un elemento

Queste parole sono usate per i punti e sotto **Posiziona da**.

| Parola | Significato |
| --- | --- |
| davanti | l'estremità dell'elemento alla lunghezza 0 |
| dietro | l'altra estremità |
| destra, sinistra | visto dall'estremità davanti, guardando lungo la parete |
| sotto | il lato inferiore |
| sopra | l'altezza a cui poggia il corso successivo (vedere sotto), oppure il punto più alto per i due angoli superiori |

Un corso è uno strato di elementi in una parete.

Con **Rotazione** 0, la lunghezza corre lungo l'asse X del progetto, lo spessore della parete lungo Y e l'altezza
lungo Z. "Destra" è allora il lato con il valore Y più piccolo.

## I dodici punti di un elemento

Ogni elemento posizionato porta dodici punti di costruzione. Un punto di costruzione è un punto ausiliario di Fusion che si
può cliccare. I punti hanno dei nomi. I nomi sono scritti nella lingua che l'add-in usava quando l'elemento è stato
posizionato per la prima volta.

| Nome | Dove si trova |
| --- | --- |
| sotto davanti | lato inferiore, estremità davanti, centro dello spessore della parete |
| sotto centro | lato inferiore, metà lunghezza, centro dello spessore della parete |
| sotto dietro | lato inferiore, estremità dietro, centro dello spessore della parete |
| sopra davanti | altezza del corso successivo, estremità davanti, centro dello spessore della parete |
| sopra centro | altezza del corso successivo, metà lunghezza, centro dello spessore della parete |
| sopra dietro | altezza del corso successivo, estremità dietro, centro dello spessore della parete |
| sopra centro destra | altezza del corso successivo, metà lunghezza, faccia destra della parete |
| sopra centro sinistra | altezza del corso successivo, metà lunghezza, faccia sinistra della parete |
| sotto centro destra | lato inferiore, metà lunghezza, faccia destra della parete |
| sotto centro sinistra | lato inferiore, metà lunghezza, faccia sinistra della parete |
| centro destra, 50 mm sopra | 50 mm sopra il lato inferiore, metà lunghezza, faccia destra della parete |
| centro sinistra, 50 mm sopra | 50 mm sopra il lato inferiore, metà lunghezza, faccia sinistra della parete |

"Altezza del corso successivo": gli elementi con il profilo rialzato in alto portano il corso successivo 50 mm sotto il loro
punto più alto. Gli elementi piatti lo portano in cima. Esempio: `S1 WP` è alto 300 mm, il corso successivo poggia a 250 mm.

Il disegno mostra tutti i punti sull'elemento base `S1 WP`. Le sue scritte sono in tedesco. Giallo: si può cliccare.
Rosso: si può scegliere sotto **Posiziona da**. Verde: entrambe le cose.

![I punti sull'elemento S1 WP](../s1-wp-punkte.svg)

Dalla 1.1.0.1 ogni punto è visibile sulla superficie dell'elemento. Se il posto della tabella è dentro il materiale o
in aria – in una scanalatura, su una linguetta, in un incavo – il punto si sposta sulla superficie accanto: prima in
alto o in basso, altrimenti lungo la lunghezza. Cliccandolo vale ancora il posto della tabella, quindi un muro
sfalsato risulta uguale. Gli elementi di versioni precedenti ricevono i punti spostati alla prossima posa di un
elemento. Lo spostamento è stato usato dall'autore dentro Fusion.

Stato: i punti sono testati solo offline, **non dentro Fusion**.

## Posiziona da

**Posiziona da** decide quale punto del nuovo elemento finisce sul punto cliccato. L'elenco ha 15 voci:

| Voce | Punto dell'elemento |
| --- | --- |
| Angolo inferiore anteriore destro | angolo più basso dell'estremità davanti, lato destro. È il valore predefinito. |
| Angolo superiore anteriore destro | angolo più alto dell'estremità davanti, lato destro |
| Angolo superiore anteriore sinistro | angolo più alto dell'estremità davanti, lato sinistro |
| sotto davanti … centro sinistra, 50 mm sopra | uno dei dodici punti della tabella qui sopra |

I due angoli superiori usano l'altezza intera dell'elemento, non l'altezza del corso successivo.

Stato: le scelte sotto **Posiziona da** sono testate solo offline, **non dentro Fusion**.

## Rotazione

- **Rotazione** ruota l'elemento attorno all'asse verticale. È l'asse Z del progetto.
- La rotazione avviene intorno al punto scelto sotto **Posiziona da**. Quel punto resta sul punto cliccato.
- L'angolo è indicato in gradi. Un angolo positivo ruota in senso antiorario guardando dall'alto.

## Spostamenti

- **Spostamento X**, **Spostamento Y** e **Spostamento Z** allontanano l'elemento dal punto cliccato.
- I valori sono in mm.
- Corrono lungo gli assi del progetto. Non ruotano con l'elemento.
- I valori negativi spostano nella direzione opposta.

Esempio: nessun punto cliccato, **Spostamento Z** 300 mm. L'elemento viene posizionato 300 mm sopra l'origine.

Stato: gli spostamenti sono testati solo offline, **non dentro Fusion**.

## Costruire una parete a giunti sfalsati

"A giunti sfalsati" significa: ogni corso è spostato di mezzo elemento rispetto al corso sottostante.

1. Posizionare il primo elemento del corso più basso. Usare **Posiziona da**: **Angolo inferiore anteriore destro**.
2. Avviare di nuovo il comando. Scegliere **Posiziona da**: **sotto davanti**.
3. Fare clic sul punto **sotto dietro** dell'elemento appena posizionato. L'elemento successivo prosegue il corso.
4. Ripetere finché il primo corso è finito.
5. Per il secondo corso, avviare di nuovo il comando. Scegliere **Posiziona da**: **sotto centro**.
6. Fare clic sul punto **sopra davanti** o **sopra dietro** di un elemento del corso sottostante.
   Il nuovo elemento sta allora per metà su quell'elemento e per metà accanto.
7. Proseguire il secondo corso come nei passi 2 e 3.

Le impostazioni restano come sono state lasciate, quindi basta cliccare il punto successivo e premere **OK**.

Note:

- Il passo 6 è il modo che la descrizione dell'add-in stesso indica per una parete a giunti sfalsati. I passi da 2 a 4 derivano dalle posizioni
  dei punti; **non sono testati dentro Fusion**.
- Sugli elementi con un maschio all'estremità (3 mm più lunghi, nomi che finiscono in `WP` o `P`) i punti **sotto davanti** e
  **sotto dietro** si trovano alle estremità più esterne. Controllare nel proprio progetto il giunto tra due elementi.
- L'add-in non controlla se gli elementi si sovrappongono né se un elemento entra in un dato posto.

## Distinta dei pezzi: come contano gli elementi uguali

- La prima volta che si posiziona un elemento, l'add-in crea un componente di nome `SYSTEM 3E <name>`,
  per esempio `SYSTEM 3E S1 WP`. Il corpo al suo interno ha il nome dell'elemento, per esempio `S1 WP`.
- Ogni volta successiva che si posiziona lo stesso elemento in quel progetto, l'add-in aggiunge un'altra copia di quello stesso
  componente. Non crea un nuovo componente.
- Una distinta dei pezzi mostra quindi una sola riga per l'elemento con la sua quantità, non `S1 WP`, `S1 WP (1)`, `S1 WP (2)`.
- Il componente si può rinominare. L'add-in lo trova lo stesso, perché vi lascia un contrassegno invisibile.
- Poiché le copie condividono un solo componente, una modifica al corpo di una copia modifica tutte le copie.
- Tutti gli elementi vengono creati direttamente nel livello più alto del progetto (il componente radice).
