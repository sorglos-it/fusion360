# Impostazioni

L'add-in non ha un file di impostazioni né una pagina di impostazioni. Tutto si imposta nella finestra di dialogo del comando.
I campi sono elencati nell'ordine in cui la finestra di dialogo li mostra.

## Campi della finestra di dialogo

| Campo | Significato | Valore predefinito | Valori consentiti |
|---|---|---|---|
| **Linee** | Le linee di schizzo che ricevono un giunto. Testo di invito: "Seleziona una o più linee di schizzo". | le linee selezionate prima di avviare il comando | da 1 a 100 linee di schizzo rette |
| **Numero** | Numero di denti per linea | 1 | numero intero, da 1 a 500 |
| **Rispecchia la geometria** | Rende identici i due pezzi, vedere [usage.md](usage.md#due-pezzi-identici-rispecchia-la-geometria) | disattivato | attivato / disattivato |
| **Forma** | Forma del dente | Trapezio (coda di rondine) | Trapezio (coda di rondine), Triangolo, Rettangolo (giunto a pettine) |
| **Larghezza (base)** | Larghezza del dente dove incontra la linea | 10 mm | maggiore di 0 e maggiore del doppio della tolleranza |
| **Profondità** | Di quanto il dente sporge dalla linea | 6 mm | maggiore di 0 |
| **Angolo dei fianchi** | Solo trapezio: di quanto ogni fianco del dente si inclina verso l'esterno | 15 deg | più di −89 e meno di 89 gradi; vedere sotto |
| **Passo (centro-centro)** | Distanza dal centro di un dente al centro del successivo. Usato solo con 2 o più denti. | 20 mm | maggiore di 0 e almeno pari al passo minimo, vedere sotto |
| **Spostamento** | Spostamento dell'intero gruppo di denti lungo la linea. Positivo: verso il punto finale. | 0 mm, ogni volta | tra meno e più lo spostamento massimo, vedere sotto |
| **Incremento** | Di quanto un clic su un pulsante **Sposta** sposta i denti | 1 mm | non controllato dall'add-in, vedere sotto |
| **Sposta** | Tre pulsanti: **A sinistra (verso il punto iniziale)**, **Centra**, **A destra (verso il punto finale)** | – | – |
| **Tolleranza** | Gioco tra i due pezzi | 0.25 mm | maggiore di 0; altri limiti sotto |
| **La linea è** | Quale pezzo cede materiale per il gioco | Linea mediana - metà tolleranza per lato | le tre voci elencate sotto |
| **Inverti direzione** | Mette i denti sull'altro lato della linea | disattivato | attivato / disattivato |
| **Converti la linea originale in geometria di costruzione** | Con OK converte la linea selezionata in una linea ausiliaria | attivato | attivato / disattivato |

Voci di **La linea è**:

| Voce | La cava cresce di | Il tenone si riduce di |
|---|---|---|
| **Linea mediana - metà tolleranza per lato** | metà tolleranza | metà tolleranza |
| **Bordo della cava - tutta la tolleranza sul tenone** | niente | l'intera tolleranza |
| **Bordo del tenone - tutta la tolleranza sulla cava** | l'intera tolleranza | niente |

## Campi in grigio

| Campo | In grigio quando |
|---|---|
| **Angolo dei fianchi** | **Forma** non è Trapezio (coda di rondine). Il valore viene allora ignorato. |
| **Passo (centro-centro)** | **Numero** è 1. Il valore viene allora ignorato. |
| **La linea è**, **Spostamento**, **Incremento**, **Sposta** | **Rispecchia la geometria** è spuntato |

## I limiti in dettaglio

Tutti i limiti vengono dal codice. Le lunghezze qui sotto sono in millimetri.

La "mezza larghezza della punta" è usata in diversi limiti. Dipende dalla forma:

| Forma | Mezza larghezza della punta |
|---|---|
| Rettangolo (giunto a pettine) | Larghezza ÷ 2 |
| Triangolo | 0 |
| Trapezio (coda di rondine) | Larghezza ÷ 2 + Profondità × tan(Angolo dei fianchi) |

La "metà più larga" è il maggiore tra Larghezza ÷ 2 e la mezza larghezza della punta.

### Angolo dei fianchi

- Deve essere più di −89 e meno di 89 gradi. Esattamente 89 o −89 viene rifiutato.
- Con un angolo negativo la punta si restringe. La mezza larghezza della punta deve restare sopra 0. Altrimenti il
  dente si annullerebbe e viene rifiutato.
- 0 gradi dà un rettangolo.

### Passo (centro-centro)

Controllato solo con 2 o più denti.

Passo minimo = 2 × metà più larga + 2 × Tolleranza + 0.01 mm

Esempio con i valori predefiniti (Larghezza 10 mm, Profondità 6 mm, Angolo dei fianchi 15 deg, Tolleranza 0.25 mm):
la mezza larghezza della punta è circa 6.61 mm, quindi il passo minimo è circa 13.73 mm.

### Spazio sulla linea

I denti devono mantenere una distanza da entrambi gli estremi della linea: la tolleranza più 0.01 mm.

Lunghezza necessaria = (Numero − 1) × Passo + 2 × metà più larga + 2 × (Tolleranza + 0.01 mm)

Esempio con i valori predefiniti e un dente: servono circa 13.74 mm di linea.

### Spostamento

Spostamento massimo = Lunghezza della linea ÷ 2 − ( (Numero − 1) ÷ 2 × Passo + metà più larga + Tolleranza + 0.01 mm )

- Lo spostamento può stare tra meno e più questo valore.
- I pulsanti **Sposta** si fermano a questo valore. Con più linee decide la linea più corta.
- Uno spostamento scritto a mano non viene corretto. Se è troppo grande, OK è in grigio.
- Con **Rispecchia la geometria** lo spostamento deve essere 0.

### Tolleranza

- Deve essere maggiore di 0. La fascia è fatta dal gioco; con 0 non c'è alcuna fascia.
- Il doppio della tolleranza deve essere minore di **Larghezza (base)**.
- Tolta la tolleranza, deve restare come altezza del dente almeno il 5 % di **Profondità**. Questo conta soprattutto per
  i denti a punta, dove la punta perde più altezza della tolleranza.
- La fascia non deve incrociare se stessa e nessuno dei suoi tratti può ridursi a nulla. Può succedere con punte di
  trapezio strette e una tolleranza grande.
- In uno spigolo acuto lo spigolo spostato non deve allontanarsi più di 12 volte la distanza di spostamento.

### Numero

- Da 1 a 500.
- Con **Rispecchia la geometria** il numero deve essere pari. La finestra di dialogo aumenta di 1 un numero dispari.

### Incremento

L'add-in non controlla questo valore. Dal codice: con 0 i pulsanti **Sposta** non fanno nulla; un valore negativo
inverte la direzione dei pulsanti sinistro e destro.

### Linee

- Si possono selezionare solo linee di schizzo rette.
- Almeno 1, al massimo 100.
- Una linea deve avere una lunghezza maggiore di 0.

## Unità

- I campi di lunghezza sono mostrati in millimetri, l'angolo in gradi.
- I numeri nei messaggi di errore sono sempre in millimetri con due decimali.
- All'interno l'add-in calcola in centimetri e radianti, le unità che Fusion usa internamente.

## Cosa viene ricordato

L'add-in ricorda i valori dell'ultima esecuzione conclusa con **OK** e riuscita.

| Ricordato | Non ricordato |
|---|---|
| Numero | Linee |
| Rispecchia la geometria | Spostamento (parte sempre da 0) |
| Forma | |
| Larghezza (base) | |
| Profondità | |
| Angolo dei fianchi | |
| Passo (centro-centro) | |
| Incremento | |
| Tolleranza | |
| La linea è | |
| Inverti direzione | |
| Converti la linea originale in geometria di costruzione | |

Per quanto tempo:

- I valori sono tenuti solo in memoria. Nulla viene scritto su disco.
- Durano per la sessione di Fusion in corso. Dopo la chiusura di Fusion valgono di nuovo i valori predefiniti della tabella qui sopra.
- Chiudere la finestra di dialogo con Cancel (Annulla) non cambia i valori ricordati.

Lo spostamento è lasciato fuori di proposito: appartiene alla linea del momento, non alle impostazioni.

## Lingua

L'add-in ha testi in cinque lingue: tedesco, inglese, spagnolo, francese, italiano.

La lingua viene scelta una sola volta, all'avvio dell'add-in:

1. Si usa la lingua impostata nelle preferenze di Fusion (lingua dell'utente), se è una delle cinque.
2. Altrimenti l'add-in guarda le variabili d'ambiente `LANG`, `LANGUAGE` e `LC_ALL`, in quest'ordine.
3. Se da lì non risulta nulla, guarda la lingua del sistema operativo.
4. Se nemmeno da lì risulta nulla, si usa l'inglese.

Nella finestra di dialogo non c'è un selettore della lingua. Dopo aver cambiato la lingua in Fusion, l'add-in va avviato
di nuovo (riavviando Fusion questo avviene).

Se in un file di lingua manca un singolo testo, al suo posto viene mostrato il testo inglese.
