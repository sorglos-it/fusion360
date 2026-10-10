# Uso

Tutti i nomi dei campi qui sotto sono scritti esattamente come compaiono nella finestra di dialogo in italiano. Ogni
campo è spiegato in dettaglio in [settings.md](settings.md).

## Parole usate qui

| Parola | Significato |
|---|---|
| Dente | Una coda di rondine, un triangolo o un rettangolo che sporge dalla linea |
| Tenone | Il dente come parte di uno dei due pezzi |
| Cava | L'incavo corrispondente nell'altro pezzo |
| Tolleranza | Lo spazio tra tenone e cava (il gioco) |
| Fascia | Il contorno chiuso disegnato dall'add-in. Il suo interno è esattamente il gioco. |
| Punto iniziale, punto finale | I due estremi di una linea di schizzo, nell'ordine in cui la linea è stata disegnata |

## Disegnare un giunto su una linea

1. Aprire uno schizzo o modificarne uno esistente.
2. Disegnare una linea retta dove i due pezzi devono incontrarsi.
3. Fare clic sulla linea.
4. Fare clic sul pulsante **Coda di rondine**. Si apre la finestra di dialogo. La linea è già inserita sotto **Linee**.
   Si può anche avviare prima il comando e poi fare clic sulla linea.
5. Impostare **Numero**, **Forma**, **Larghezza (base)**, **Profondità** e **Tolleranza**.
6. Osservare l'anteprima nello schizzo.
7. Premere **OK**.

Risultato:

- Viene disegnata una fascia chiusa nello stesso schizzo della linea.
- La linea originale diventa geometria di costruzione (una linea ausiliaria tratteggiata), se è spuntato
  **Converti la linea originale in geometria di costruzione**. Questo avviene solo con OK, non nell'anteprima.
- L'add-in non aggiunge quote né vincoli alle nuove linee.

Se **OK** è in grigio e non si vede alcuna anteprima, i valori non vanno bene. La finestra di dialogo non dice perché.
Vedere [troubleshooting.md](troubleshooting.md#ok-è-in-grigio).

## Ricavare dalla fascia due pezzi che si incastrano

1. Disegnare il contorno dell'intero pezzo. Far passare la linea del giunto attraverso di esso, da bordo a bordo.
2. Eseguire Dovetail sulla linea del giunto.
3. Estrudere il contorno in un corpo solido.
4. Estrudere la fascia come taglio attraverso quel corpo.

Restano due corpi. Si incastrano l'uno nell'altro con il gioco impostato sotto **Tolleranza**.

I passi 3 e 4 sono normali funzioni di Fusion. L'add-in in sé disegna solo la fascia.

## Scegliere la forma

Usare l'elenco **Forma**:

| Voce | Risultato |
|---|---|
| **Trapezio (coda di rondine)** | Il dente si allarga verso la punta. Si aggancia e non si può sfilare in linea retta. |
| **Triangolo** | Il dente finisce a punta. Non ha aggancio e si può separare tirando. |
| **Rettangolo (giunto a pettine)** | Dente diritto, stessa larghezza alla base e alla punta. |

**Angolo dei fianchi** è attivo solo per **Trapezio (coda di rondine)**. Stabilisce di quanto si allarga il dente. Con
0 gradi il trapezio è uguale a un rettangolo. Un angolo negativo rende il dente più stretto verso la punta.

## Più denti su una linea

1. Impostare **Numero** su 2 o più. Il campo **Passo (centro-centro)** diventa attivo.
2. Impostare **Passo (centro-centro)**: la distanza dal centro di un dente al centro del successivo.

Il gruppo di denti sta sempre in modo simmetrico attorno al centro della linea:

| Numero | Posizione dei denti rispetto al centro (passo 30 mm) |
|---|---|
| 1 | 0 |
| 2 | −15 / +15 |
| 3 | −30 / 0 / +30 |
| 4 | −45 / −15 / +15 / +45 |
| 5 | −60 / −30 / 0 / +30 / +60 |

Un numero dispari mette un dente sul centro. Un numero pari vi mette uno spazio vuoto.

## Spostare i denti lungo la linea

Due modi:

- Scrivere un valore in **Spostamento**. Un valore positivo sposta i denti verso il punto finale della linea, un valore
  negativo verso il punto iniziale. 0 significa centrato.
- Usare i tre pulsanti nella riga **Sposta**:

  | Pulsante | Effetto |
  |---|---|
  | **A sinistra (verso il punto iniziale)** | sposta i denti di un **Incremento** verso il punto iniziale |
  | **Centra** | riporta **Spostamento** a 0 |
  | **A destra (verso il punto finale)** | sposta i denti di un **Incremento** verso il punto finale |

I pulsanti si fermano dove i denti non starebbero più sulla linea. Con più linee questo limite è dato dalla linea
più corta. Un valore scritto a mano non viene corretto: se è troppo grande, OK è in grigio.

**Spostamento** parte da 0 ogni volta che si apre la finestra di dialogo.

## Scegliere quale pezzo cede materiale

Il gioco deve venire da qualche parte. Lo decide l'elenco **La linea è**:

| Voce | Bordo della cava | Bordo del tenone | Usarla quando |
|---|---|---|---|
| **Linea mediana - metà tolleranza per lato** | si sposta verso l'esterno di metà tolleranza | si sposta verso l'interno di metà tolleranza | i due pezzi devono restare uguali |
| **Bordo della cava - tutta la tolleranza sul tenone** | esattamente sulla forma disegnata | si sposta verso l'interno dell'intera tolleranza | il pezzo con le cave deve mantenere la sua misura esatta |
| **Bordo del tenone - tutta la tolleranza sulla cava** | si sposta verso l'esterno dell'intera tolleranza | esattamente sulla forma disegnata | il pezzo con i tenoni deve mantenere la sua misura esatta |

Il gioco tra i pezzi è l'intera tolleranza in tutti e tre i casi.

Esempio con una tolleranza di 0.25 mm:

| Voce | Cava | Tenone | Gioco |
|---|---|---|---|
| Linea mediana | +0.125 mm | −0.125 mm | 0.25 mm |
| Bordo della cava | 0 | −0.25 mm | 0.25 mm |
| Bordo del tenone | +0.25 mm | 0 | 0.25 mm |

## Mettere i denti sull'altro lato

Spuntare **Inverti direzione**.

Senza la spunta, i denti stanno sul lato sinistro della linea guardando dal suo punto iniziale al suo punto finale
(nel piano X/Y dello schizzo). Con la spunta stanno sul lato destro.

Con più linee, ogni linea segue la propria direzione. Le linee disegnate in direzioni opposte hanno i denti su lati
opposti. **Inverti direzione** li ribalta tutti insieme.

## Più linee in una volta

1. Selezionare più linee prima di avviare il comando. Oppure avviare il comando e fare clic sulle linee una dopo l'altra.
   Sono possibili fino a 100 linee.
2. Impostare i valori una sola volta.
3. Premere **OK**.

Ogni linea riceve il proprio giunto con gli stessi valori. Ogni linea viene misurata per conto suo e i suoi denti
sono centrati sul suo centro. Le linee possono avere lunghezze diverse.

I valori devono andare bene su ogni linea. Se una linea è troppo corta, non viene disegnato nulla e OK è in grigio.
Guardare per prima la linea più corta; è la prima a restare senza spazio.

Si possono selezionare solo linee di schizzo rette. Archi, cerchi e spline no.

## Due pezzi identici: Rispecchia la geometria

Spuntare **Rispecchia la geometria**.

Metà dei denti punta allora da una parte e metà dall'altra. Ruotando la fascia di 180 gradi attorno al centro
della linea, essa torna su se stessa. I due pezzi del taglio sono quindi identici. Si può modellare un pezzo e
produrlo due volte; il secondo viene girato.

La finestra di dialogo imposta tre cose da sola, perché ognuna di esse romperebbe la simmetria:

| Cosa | Perché |
|---|---|
| **Numero** viene portato al numero pari successivo | Un dente sul centro dovrebbe puntare in entrambe le direzioni insieme. |
| **La linea è** viene impostato sulla linea mediana e messo in grigio | Solo lì entrambi i pezzi cedono la stessa quantità. |
| **Spostamento** viene impostato a 0; **Spostamento**, **Incremento** e **Sposta** sono messi in grigio | Un gruppo spostato non è più simmetrico rispetto al centro. |

Togliendo la spunta, i campi tornano attivi. I valori cambiati dalla finestra di dialogo restano come sono.

Con più linee, ogni linea viene rispecchiata rispetto al proprio centro.

## Mantenere o convertire la linea originale

Il campo **Converti la linea originale in geometria di costruzione** è spuntato per impostazione predefinita.

- Spuntato: con OK la linea selezionata diventa geometria di costruzione. Conserva quote e vincoli, ma non
  divide più la fascia in due aree.
- Non spuntato: la linea resta una linea normale. Attraversa la fascia e la divide in due aree (profili).

Una linea che è già geometria di costruzione viene lasciata com'è.

## Anteprima

Finché la finestra di dialogo è aperta, l'add-in disegna la fascia come anteprima dopo ogni modifica.

- L'anteprima non modifica mai la linea originale. Per questo l'anteprima mostra la linea ancora come linea normale.
- Se i valori non vanno bene, non viene mostrata alcuna anteprima.

## Eseguire di nuovo il comando

Fusion può ripetere il comando con la sua funzione "repeat last command" (ripeti ultimo comando); l'add-in lo consente.
La finestra di dialogo si riapre con i valori dell'ultima esecuzione riuscita. Vedere
[settings.md](settings.md#cosa-viene-ricordato).
