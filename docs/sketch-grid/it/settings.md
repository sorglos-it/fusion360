# Impostazioni

L'add-in non ha un file di impostazioni né una pagina di impostazioni. Tutto si imposta nella finestra di dialogo del comando **Griglia di schizzo**. I nomi dei campi sono scritti esattamente come nella finestra di dialogo in italiano.

## Campi della finestra di dialogo

Le lunghezze si inseriscono in millimetri per impostazione predefinita (i campi sono creati con l'unità `mm`). "Nessun limite" significa: l'add-in in sé non controlla altro.

| Campo | Significato | Valore predefinito | Valori consentiti |
| --- | --- | --- | --- |
| **Punto** | Il punto di schizzo attorno al quale viene costruita la griglia. | Il punto di schizzo selezionato prima dell'apertura della finestra di dialogo, altrimenti vuoto | Esattamente un punto di schizzo. Altri oggetti non si possono selezionare. |
| **Numero da** | Come si stabilisce il numero di forme. | Colonne e righe | **Colonne e righe**, **Riempimento di un'area** |
| **Forma** | La forma che viene ripetuta. | Rettangolo | **Rettangolo**, **Cerchio / ellisse**, **Asola**, **Poligono** |
| **Lati** | Numero di lati del poligono. | 6 | Numero intero, da 3 a 24 |
| **Regolare** | Casella di spunta. Attivata: tutti i lati del poligono sono di uguale lunghezza. Disattivata: il poligono viene allungato a lunghezza × profondità. | disattivata | attivata, disattivata |
| **Spigoli** | Cosa succede ai quattro spigoli del rettangolo. | Vivi | **Vivi**, **Raccordati**, **Smussati** |
| **Raggio / smusso** | Raggio del raccordo, oppure lunghezza del taglio lungo ciascun lato. | 1 mm | Maggiore di 0, al massimo la metà della minore tra lunghezza e profondità |
| **Lunghezza (X)** | Dimensione di una forma in X. | 10 mm | Maggiore di 0, nessun limite superiore |
| **Profondità (Y)** | Dimensione di una forma in Y. | 5 mm | Maggiore di 0, nessun limite superiore |
| **Distanza X** | Spazio libero tra forme vicine in X. | 2 mm | 0 o più, nessun limite superiore |
| **Distanza Y** | Spazio libero tra forme vicine in Y. | 2 mm | 0 o più, nessun limite superiore |
| **Colonne** | Numero di forme una accanto all'altra. | 8 | Numero intero, da 1 a 2000 |
| **Righe** | Numero di forme una sopra l'altra. | 4 | Numero intero, da 1 a 2000 |
| **Larghezza dell'area** | Larghezza dell'area da riempire. | 100 mm | Maggiore di 0 e abbastanza grande per una forma |
| **Altezza dell'area** | Altezza dell'area da riempire. | 40 mm | Maggiore di 0 e abbastanza grande per una forma |
| **Il punto si trova nella griglia** | Dove si trova il punto selezionato dentro la griglia finita. | Al centro | Nove voci, vedere sotto |
| **Scostamento X** | Sposta l'intera griglia in X, in aggiunta alla posizione scelta sopra. | 0 mm | Qualsiasi valore, anche negativo |
| **Scostamento Y** | Sposta l'intera griglia in Y. | 0 mm | Qualsiasi valore, anche negativo |
| **Risultato** | Mostra il numero di forme e la dimensione totale, oppure un messaggio. | – | Sola lettura |

Un altro limite vale per l'intera griglia: colonne × righe non deve superare **2000**. Questo vale in entrambe le modalità di conteggio.

## Quando viene mostrato un campo

| Campo | Mostrato quando |
| --- | --- |
| **Lati**, **Regolare** | **Forma** è **Poligono** |
| **Spigoli** | **Forma** è **Rettangolo** |
| **Raggio / smusso** | **Forma** è **Rettangolo** e **Spigoli** non è **Vivi** |
| **Colonne**, **Righe** | **Numero da** è **Colonne e righe** |
| **Larghezza dell'area**, **Altezza dell'area** | **Numero da** è **Riempimento di un'area** |
| tutti gli altri campi | sempre |

Un campo nascosto conserva il suo valore. Un valore nascosto non viene usato né controllato.

## Il punto si trova nella griglia

| Voce | Il punto si trova |
| --- | --- |
| **Al centro** | al centro della griglia |
| **In basso a sinistra** | sull'angolo in basso a sinistra |
| **In basso a destra** | sull'angolo in basso a destra |
| **In alto a sinistra** | sull'angolo in alto a sinistra |
| **In alto a destra** | sull'angolo in alto a destra |
| **In basso al centro** | a metà del bordo inferiore |
| **In alto al centro** | a metà del bordo superiore |
| **A sinistra al centro** | a metà del bordo sinistro |
| **A destra al centro** | a metà del bordo destro |

"Griglia" qui significa il rettangolo più piccolo attorno a tutte le forme. Sinistra e destra sono lungo l'asse X dello schizzo, basso e alto lungo il suo asse Y.

## Testi di aiuto nella finestra di dialogo

Tre testi di aiuto (descrizioni comando) sono collegati ai campi:

| Campo | Testo |
| --- | --- |
| **Regolare** | "Mantiene il poligono equilatero invece di allungarlo a lunghezza × profondità. La minore delle due ne determina la dimensione e il passo segue la forma reale - la distanza impostata viene rispettata in entrambi i casi." |
| **Spigoli**, **Raggio / smusso** | "Elimina i quattro angoli retti del rettangolo, come raccordo o come smusso diritto. Al massimo metà del lato più corto: proprio quel raggio trasforma il rettangolo in un'asola, quello smusso in un rombo. L'ingombro non cambia, quindi numero, passo e distanza restano quelli di prima." |
| **Scostamento X**, **Scostamento Y** | "Sposta l'intera griglia rispetto al punto selezionato, in aggiunta a quanto stabilito dal punto di riferimento. Serve a mantenere un margine da un bordo senza spostare il punto stesso. I valori negativi vanno nella direzione opposta." |

Nota sul secondo testo: uno smusso pari esattamente alla metà del lato più corto dà un rombo solo quando lunghezza e profondità sono uguali. Con valori diversi dà una forma a sei lati.

Il pulsante stesso ha il testo di aiuto: "Costruisce una griglia di forme attorno a un punto di schizzo. Numero fisso di colonne e righe, oppure quante ne stanno in un'area."

## Cosa viene ricordato

- Quando una griglia viene conclusa con **OK**, l'add-in ricorda tutti i valori tranne il punto: modalità di conteggio, forma, lati, Regolare, spigoli, raggio / smusso, lunghezza, profondità, entrambe le distanze, colonne, righe, larghezza dell'area, altezza dell'area, posizione del punto, entrambi gli scostamenti.
- Alla successiva apertura della finestra di dialogo questi valori sono già inseriti.
- I valori **non** vengono ricordati quando si annulla la finestra di dialogo, o quando OK termina con un messaggio di errore.
- I valori sono tenuti solo in memoria, mai su disco. Durano finché l'add-in non viene arrestato o Fusion non viene chiuso. Dopo valgono di nuovo i valori predefiniti della tabella qui sopra.
- I valori sono gli stessi per tutti i documenti aperti in questa sessione di Fusion.

## Lingua

L'add-in ha cinque lingue: tedesco, inglese, spagnolo, francese, italiano.

Come viene scelta la lingua, in quest'ordine:

1. La lingua impostata in Fusion sotto **Preferences → General → User Language**, se è una delle cinque.
2. Altrimenti la lingua del sistema operativo, se è una delle cinque. (L'add-in legge le variabili d'ambiente `LANG`, `LANGUAGE`, `LC_ALL`, poi le impostazioni locali del sistema.)
3. Altrimenti l'inglese.

Altri dettagli:

- Nell'add-in non c'è un selettore della lingua.
- La lingua viene letta una sola volta, all'avvio dell'add-in. Dopo aver cambiato la lingua in Fusion, arrestare e avviare l'add-in, oppure riavviare Fusion.
- Se in una lingua manca un testo, al suo posto viene mostrato il testo inglese.
- La riga **Risultato** mostra sempre millimetri, in ogni lingua.
