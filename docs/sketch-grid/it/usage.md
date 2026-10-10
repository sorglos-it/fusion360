# Uso

Tutti i nomi dei campi qui sotto sono scritti esattamente come compaiono nella finestra di dialogo in italiano. Dettagli su ogni campo: [settings.md](settings.md).

## Disegnare una griglia

1. Aprire o modificare uno schizzo.
2. Fare clic su un punto di schizzo. Può essere l'origine dello schizzo o un punto collocato a mano.
3. Fare clic sul pulsante **Griglia di schizzo**. Si apre la finestra di dialogo. Il punto su cui si è fatto clic è già inserito in **Punto**.
4. Se **Punto** è vuoto, fare clic ora su un punto di schizzo. Il testo di invito è "Seleziona un punto di schizzo".
5. Impostare i valori. La riga **Risultato** mostra ciò che si otterrà, per esempio `8 × 4 = 32 forme, 94.00 × 26.00 mm in totale`.
6. Guardare l'anteprima nello schizzo.
7. Premere **OK**.

Si possono selezionare solo punti di schizzo. Serve esattamente un punto.

**OK** è in grigio finché un valore non è consentito. Nella maggior parte dei casi la riga **Risultato** ne mostra allora il motivo. Vedere [troubleshooting.md](troubleshooting.md).

La griglia è disposta lungo gli assi X e Y dello schizzo. Nella finestra di dialogo non si può ruotare. Parole come "sinistra", "destra", "alto", "basso" e "verso l'alto" in questa documentazione si riferiscono agli assi dello schizzo: destra è +X, verso l'alto è +Y.

La ripresa di un punto su cui si è fatto clic prima dell'apertura della finestra di dialogo (passo 3) è stata modificata nella versione 1.1.0.0 e verificata solo offline, non all'interno di Fusion. Se il punto non viene ripreso, selezionarlo nella finestra di dialogo (passo 4).

## Esempio

Questi sono i valori con cui parte la finestra di dialogo:

| Campo | Valore |
| --- | --- |
| **Forma** | Rettangolo |
| **Lunghezza (X)** | 10 mm |
| **Profondità (Y)** | 5 mm |
| **Distanza X** / **Distanza Y** | 2 mm |
| **Colonne** / **Righe** | 8 / 4 |

Risultato: 32 rettangoli. La griglia misura 94 × 26 mm (8 × 10 + 7 × 2 = 94, 4 × 5 + 3 × 2 = 26). Con **Il punto si trova nella griglia** impostato su **Al centro**, il punto è il centro della griglia.

## Scegliere come si contano le forme

Campo **Numero da**.

### Colonne e righe

1. Impostare **Numero da** su **Colonne e righe**.
2. Inserire **Colonne** e **Righe**.

Se ne ottengono esattamente tante. La griglia è grande quanto serve.

### Riempimento di un'area

1. Impostare **Numero da** su **Riempimento di un'area**.
2. Inserire **Larghezza dell'area** e **Altezza dell'area**.

L'add-in disegna tante forme quante ne entrano **per intero** nell'area. Una forma che entra solo in parte non viene mai disegnata.

- Esempio: larghezza dell'area 100 mm, lunghezza 10 mm, distanza 2 mm danno 8 colonne. Occupano 94 mm. Una nona colonna richiederebbe 106 mm.
- Di solito la griglia è un po' più piccola dell'area. L'area serve solo per contare. Non viene disegnata.
- Il resto dell'area rimane vuoto sul lato lontano dal punto. Con **Al centro** viene diviso in parti uguali sui due lati.
- Un'area di esattamente 94 mm dà 8 colonne; 93.9 mm ne danno 7.

I campi **Colonne** e **Righe** sono mostrati solo nella prima modalità, **Larghezza dell'area** e **Altezza dell'area** solo nella seconda.

## Scegliere la forma

Campo **Forma**.

| Voce | Cosa si ottiene |
| --- | --- |
| **Rettangolo** | Un rettangolo di lunghezza × profondità. I suoi spigoli si possono cambiare, vedere sotto. |
| **Cerchio / ellisse** | Un'ellisse con lunghezza e profondità come suoi due diametri. Valori uguali danno un cerchio. |
| **Asola** | Un rettangolo con due estremità semicircolari. Le estremità stanno nella direzione più lunga: se la lunghezza è maggiore della profondità, sono tonde le estremità sinistra e destra. Valori uguali danno un cerchio. |
| **Poligono** | Una forma con 3 fino a 24 lati rettilinei. Un vertice punta sempre verso l'alto. |

### Rettangolo: spigoli

1. Impostare **Forma** su **Rettangolo**. Compare il campo **Spigoli**.
2. Scegliere **Vivi**, **Raccordati** o **Smussati**. (Smussati significa: lo spigolo viene tagliato via con una linea retta.)
3. Per **Raccordati** e **Smussati** compare il campo **Raggio / smusso**. Inserire il raggio del raccordo, oppure a quale distanza dallo spigolo inizia il taglio lungo ciascun lato.

Il valore massimo consentito è la metà del lato più corto. Esattamente a quel valore:

| Rettangolo | Valore | Raccordati diventa | Smussati diventa |
| --- | --- | --- | --- |
| 10 × 5 mm | 2.5 mm | un'asola | una forma a sei lati |
| 10 × 10 mm | 5 mm | un cerchio | un rombo |

Gli spigoli non cambiano il numero di forme, il passo né la dimensione totale.

### Poligono: lati e Regolare

1. Impostare **Forma** su **Poligono**. Compaiono i campi **Lati** e **Regolare**.
2. Inserire **Lati** (da 3 a 24).
3. Lasciare **Regolare** disattivato, oppure spuntarlo.

| **Regolare** | Risultato |
| --- | --- |
| disattivato | Il poligono viene allungato in modo da misurare esattamente lunghezza × profondità. I suoi lati di solito non sono allora di uguale lunghezza. |
| attivato | Tutti i lati sono di uguale lunghezza. La minore tra lunghezza e profondità determina la dimensione. Il passo segue la dimensione reale del poligono, quindi la distanza resta quella inserita. |

Esempio con 6 lati, lunghezza 10 mm, profondità 5 mm, distanza 2 mm:

| **Regolare** | Dimensione di una forma | Distanza da una forma alla successiva |
| --- | --- | --- |
| disattivato | 10.00 × 5.00 mm | 12.00 × 7.00 mm |
| attivato | 4.33 × 5.00 mm | 6.33 × 7.00 mm |

## Impostare dimensione e distanza

- **Lunghezza (X)** e **Profondità (Y)**: dimensione di una forma.
- **Distanza X** e **Distanza Y**: spazio libero tra due forme vicine. 0 è consentito; le forme allora si toccano. I valori negativi non sono consentiti.

## Decidere dove si trova il punto

Campo **Il punto si trova nella griglia**. Dice dove va a finire il punto su cui si è fatto clic dentro la griglia finita. Non dice in quale direzione cresce la griglia.

Esempio: **In basso a sinistra** mette il punto sull'angolo in basso a sinistra della griglia. La griglia si estende allora verso destra e verso l'alto.

Tre delle nove posizioni, con una griglia di 3 × 2 forme (`X` è il punto, `#` le forme):

```
  Al centro            In basso a sinistra  In alto al centro
  #####.#####.#####    #####.#####.#####    #####.##X##.#####
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  ........X........    .................    .................
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  #####.#####.#####    X####.#####.#####    #####.#####.#####
```

Tutte e nove le voci sono elencate in [settings.md](settings.md#il-punto-si-trova-nella-griglia).

## Spostare la griglia rispetto al punto

Campi **Scostamento X** e **Scostamento Y**.

1. Scegliere prima la posizione in **Il punto si trova nella griglia**.
2. Inserire di quanto deve spostarsi l'intera griglia. I valori positivi la spostano lungo l'asse X e l'asse Y dello schizzo. I valori negativi la spostano nella direzione opposta.

Serve a mantenere un margine: il punto resta su un angolo del pezzo e la griglia inizia, per esempio, 2 mm più all'interno. Lo scostamento non cambia il numero di forme né la dimensione della griglia.

## Leggere la riga Risultato

**Risultato** non si può modificare. Mostra

- `{colonne} × {righe} = {numero} forme, {larghezza} × {altezza} mm in totale`, sempre in millimetri con due decimali, oppure
- un messaggio che dice quale valore non è consentito.

## Disegnare un'altra griglia

- La finestra di dialogo si apre con i valori dell'ultima griglia conclusa con **OK**. Vedere [settings.md](settings.md#cosa-viene-ricordato).
- Il comando è contrassegnato come ripetibile, quindi la funzione "repeat last command" (ripeti ultimo comando) di Fusion può avviarlo di nuovo.

## Cosa si ottiene nello schizzo

- Semplici linee, archi, cerchi ed ellissi di schizzo. Non viene creata alcuna lavorazione di serie (pattern) di Fusion.
- Le forme non sono collegate alla finestra di dialogo. Per cambiare la griglia in seguito, eliminare le forme e disegnare una nuova griglia.
- L'add-in non aggiunge quote né vincoli propri tra le forme e il punto.
