# Risoluzione dei problemi

## OK è in grigio

La finestra di dialogo mette in grigio **OK** e non mostra alcuna anteprima quando i valori non vanno bene. **Non dice perché.** I testi
dei messaggi qui sotto esistono nell'add-in, ma vengono mostrati in una finestra di messaggio solo se è l'esecuzione stessa a fallire dopo OK.

Scorrere questo elenco dall'alto in basso:

1. C'è almeno una linea elencata sotto **Linee**?
2. **Larghezza (base)**, **Profondità** e **Tolleranza** sono tutte maggiori di 0?
3. **Tolleranza** è minore della metà di **Larghezza (base)**?
4. Trapezio: **Angolo dei fianchi** è tra −89 e 89 gradi? Con un angolo negativo: la punta è ancora più larga di 0?
5. Due o più denti: **Passo (centro-centro)** è abbastanza grande? Vedere
   [settings.md](settings.md#passo-centro-centro) per la formula.
6. La linea è abbastanza lunga per tutti i denti? Con più linee, controllare per prima la più corta.
7. È stato scritto uno **Spostamento**? Premere il pulsante **Centra** nella riga **Sposta** per riportarlo a 0.
8. Triangolo o dente molto appuntito: ridurre **Tolleranza**, ridurre **Profondità** o aumentare **Larghezza (base)**.
9. Punta di trapezio stretta con una tolleranza grande: ridurre **Tolleranza** o cambiare **Angolo dei fianchi**.

Suggerimento: cambiare un valore alla volta. Il valore cambiato per ultimo è il primo sospetto.

## Messaggi sui valori

Tutte le finestre di messaggio hanno il titolo "Coda di rondine". `{0}`, `{1}` e `{2}` nella tabella stanno per numeri o testi che
l'add-in inserisce. Le lunghezze nei messaggi sono in millimetri.

| Messaggio | Causa | Cosa fare |
|---|---|---|
| "Seleziona almeno una linea di schizzo." | L'esecuzione è stata avviata senza alcuna linea sotto **Linee**. | Fare clic su almeno una linea di schizzo retta. |
| "Linea {0} di {1}: {2}" | Sono selezionate più linee e una di esse non può accogliere i valori. {0} è la posizione di quella linea nell'ordine in cui sono state selezionate, {1} il numero di linee, {2} il messaggio vero e proprio. | Leggere il messaggio dopo i due punti e cercarlo in questa tabella. Cambiare i valori, oppure togliere quella linea dalla selezione. |
| "La linea selezionata ha lunghezza zero." | Punto iniziale e punto finale della linea stanno nello stesso posto (visti in piano nello schizzo). | Scegliere un'altra linea o allungarla. |
| "La larghezza deve essere maggiore di 0." | **Larghezza (base)** è 0 o negativa. | Inserire una larghezza sopra 0. |
| "La profondità deve essere maggiore di 0." | **Profondità** è 0 o negativa. | Inserire una profondità sopra 0. |
| "Una fascia chiusa richiede una tolleranza maggiore di 0." | **Tolleranza** è 0 o negativa. La fascia è fatta dal gioco; senza gioco non c'è alcuna fascia. | Inserire una tolleranza sopra 0. |
| "La geometria rispecchiata richiede un numero pari di denti." | **Rispecchia la geometria** è attivo e **Numero** è dispari. Di norma la finestra di dialogo lo corregge da sola. | Impostare un numero pari. |
| "La geometria rispecchiata funziona solo con la linea mediana, l’unica in cui entrambi i pezzi cedono lo stesso." | **Rispecchia la geometria** è attivo e **La linea è** non è la linea mediana. Di norma la finestra di dialogo lo corregge da sola. | Scegliere "Linea mediana - metà tolleranza per lato" oppure disattivare il rispecchiamento. |
| "La geometria rispecchiata richiede spostamento 0, altrimenti il motivo non è più simmetrico rispetto alla mezzeria." | **Rispecchia la geometria** è attivo e **Spostamento** non è 0. Di norma la finestra di dialogo lo corregge da sola. | Impostare lo spostamento a 0 oppure disattivare il rispecchiamento. |
| "Serve almeno una coda di rondine." | **Numero** è sotto 1. Il campo della finestra di dialogo non lo permette. | Impostare un numero pari a 1 o più. |
| "L'angolo dei fianchi deve essere compreso tra -89 e 89 gradi." | Trapezio: **Angolo dei fianchi** è 89 gradi o più, oppure −89 gradi o meno. | Inserire un angolo dentro questo intervallo. |
| "Angolo dei fianchi troppo negativo - il dente si annulla." | Trapezio con angolo negativo: i fianchi si incontrano prima di arrivare alla punta. | Usare un angolo meno negativo, meno profondità o più larghezza. |
| "Il passo deve essere maggiore di 0." | Due o più denti e **Passo (centro-centro)** è 0 o negativo. | Inserire un passo sopra 0. |
| "Il passo è troppo piccolo - le code di rondine si sovrapporrebbero. Servono almeno {0} mm." | Due o più denti stanno troppo vicini. {0} è il passo minimo per i valori inseriti. | Inserire almeno il passo indicato, oppure ridurre larghezza, angolo dei fianchi o tolleranza. |
| "Lo spostamento porta la dentatura oltre la fine della linea. Al massimo sono possibili +/- {0} mm." | **Spostamento** è più grande di quanto la linea consente. {0} è lo spostamento massimo possibile. | Ridurre lo spostamento al valore indicato, oppure premere **Centra**. |
| "La dentatura è più larga della linea selezionata ({0} mm). Riduci il numero, la larghezza o il passo." | I denti più la distanza dagli estremi della linea non stanno sulla linea. {0} è la lunghezza della linea. Lo stesso testo compare se un profilo andrebbe oltre un estremo della linea. | Ridurre **Numero**, **Larghezza (base)** o **Passo (centro-centro)**, oppure usare una linea più lunga. |
| "Il profilo di accoppiamento sbanda in uno spigolo acuto. Rendi il dente più basso (meno profondità / più larghezza) oppure riduci la tolleranza." | In uno spigolo molto acuto il profilo spostato schizzerebbe lontano dal dente (più di 12 volte la distanza di spostamento). | Meno profondità, più larghezza o meno tolleranza. |
| "La tolleranza divora l'intero dente. Riduci la tolleranza o aumenta la profondità." | Tolta la tolleranza, del dente non resta nulla, oppure un tratto del profilo si riduce a nulla, oppure il profilo incrocerebbe se stesso. | Ridurre **Tolleranza** o aumentare **Profondità**. Con una punta di trapezio stretta, provare anche una larghezza maggiore o un altro angolo dei fianchi. |
| "La tolleranza è troppo grande rispetto alla profondità." | Come altezza del dente resta meno del 5 % di **Profondità**. | Ridurre **Tolleranza** o aumentare **Profondità**. |
| "La tolleranza è troppo grande rispetto alla larghezza." | Il doppio di **Tolleranza** è grande quanto **Larghezza (base)** o di più. | Ridurre **Tolleranza** o aumentare **Larghezza (base)**. |
| "Il profilo è degenere." | Una rete di sicurezza: il profilo ha troppo pochi punti, oppure i due profili non hanno lo stesso numero di punti. Con gli altri controlli in funzione, nell'uso normale non dovrebbe comparire. | Cambiare leggermente i valori. Se compare di nuovo, segnalarlo insieme ai valori usati. |

## Messaggi sul programma

Questi messaggi contengono un rapporto tecnico di errore (un "traceback") al posto di `{0}`. Indicano un errore imprevisto,
non un valore sbagliato.

| Messaggio | Quando | Cosa fare |
|---|---|---|
| "Nessun pannello della barra degli strumenti adatto trovato." | All'avvio. In questo Fusion non esiste nessuno dei tre posti della barra degli strumenti (vedere [installation.md](installation.md#primo-avvio-in-fusion)). Il pulsante non viene creato. | Aggiornare Fusion. Se il messaggio resta, segnalarlo insieme alla versione di Fusion. |
| "Errore durante la creazione della geometria: {0}" | Dopo OK si è verificato un errore imprevisto durante il disegno. L'esecuzione viene segnalata a Fusion come fallita. | Controllare lo schizzo; usare Undo (Annulla) se sono rimaste delle linee. Riprovare. Se si ripete, segnalare il testo completo. |
| "Errore durante la costruzione della finestra di dialogo: {0}" | Non è stato possibile costruire la finestra di dialogo al clic sul pulsante. | Arrestare e avviare l'add-in. Controllare che le cartelle `lang` e `resources` siano complete. Se si ripete, segnalare il testo completo. |
| "Avvio non riuscito: {0}" | L'add-in non è riuscito ad avviarsi. | Controllare che la cartella sia estratta per intero e si chiami `Dovetail`. Reinstallarlo. Se si ripete, segnalare il testo completo. |
| "Arresto non riuscito: {0}" | Non è stato possibile arrestare l'add-in in modo pulito. | Riavviare Fusion. |

Segnalazioni: <https://github.com/sorglos-it/fusion360/issues>

## Altri problemi

| Problema | Causa | Cosa fare |
|---|---|---|
| Nessun pulsante dopo l'installazione | L'add-in non è in esecuzione, oppure la cartella è annidata un livello troppo in profondità | Seguire di nuovo [installation.md](installation.md); controllare che esista `AddIns/Dovetail/Dovetail.py` |
| Nella finestra di dialogo non si riesce a fare clic su una linea | Sono accettate solo linee di schizzo rette | Usare una linea retta; archi, cerchi e spline non sono supportati |
| La fascia mostra due aree invece di una | La linea originale attraversa ancora la fascia come linea normale | Spuntare **Converti la linea originale in geometria di costruzione**, oppure convertire a mano la linea in geometria di costruzione |
| L'anteprima mostra ancora la linea originale come linea normale | L'anteprima non modifica mai la linea originale | Niente; la linea viene convertita con OK |
| I denti sono sul lato sbagliato | Il lato dipende dalla direzione in cui la linea è stata disegnata | Spuntare **Inverti direzione** |
| Alcune linee hanno i denti da un lato, altre dall'altro | Le linee sono state disegnate in direzioni opposte | Eseguire il comando separatamente per i due gruppi, una volta con e una volta senza **Inverti direzione** |
| I pulsanti **Sposta** non fanno nulla | **Incremento** è 0, oppure il limite è raggiunto, oppure **Rispecchia la geometria** è attivo | Impostare un incremento, oppure controllare lo spazio sulla linea |
| **Spostamento**, **La linea è**, **Incremento** sono in grigio | **Rispecchia la geometria** è spuntato | Togliere la spunta |
| Viene mostrata la lingua sbagliata | La lingua viene scelta all'avvio dell'add-in; le lingue diverse dalle cinque supportate ripiegano sull'inglese | Vedere [settings.md](settings.md#lingua) |
| I valori sono tornati a quelli predefiniti | Vengono ricordati solo finché Fusion è in esecuzione | Inserirli di nuovo |

## Limiti noti

- **Quando OK è in grigio non viene mostrato alcun motivo.** I testi dei messaggi vengono mostrati solo se è l'esecuzione stessa a fallire.
- **L'altezza viene ignorata.** Le linee in uno schizzo 3D o le linee fuori dal piano dello schizzo sono trattate come se fossero piane.
- **Solo linee rette.** Archi, cerchi e spline non si possono selezionare.
- **Un solo insieme di valori per tutte le linee.** Con più linee, ogni linea riceve gli stessi valori. Non c'è un'impostazione per
  singola linea.
- **Al massimo 100 linee e 500 denti per linea.**
- **Un triangolo non si aggancia.** Solo il trapezio con un angolo dei fianchi positivo resiste alla separazione per trazione.
- **La tolleranza è un gioco, niente di più.** L'add-in non compensa gli effetti del processo di fabbricazione.
- **Non confermato all'interno di Fusion:** le modifiche alla geometria della versione 1.1.0.0 (distanza dagli estremi della linea, passo
  minimo più grande, rifiuto dei profili che incrociano se stessi, annullamento dopo un'esecuzione fallita). Sono state verificate solo offline.
