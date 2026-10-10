# Impostazioni

Torna alla [panoramica](index.md).

L'add-in non ha una pagina di impostazioni né un file di impostazioni. Tutto ciò che si può impostare si trova nella finestra di dialogo del comando
**Elemento SYSTEM 3E**.

## I campi della finestra di dialogo

| Campo | Significato | Valore predefinito | Valori ammessi |
| --- | --- | --- | --- |
| **Punto** | Il posto per l'elemento. | Vuoto, oppure il punto che era selezionato prima di premere il pulsante. | Niente oppure esattamente un punto: un punto di schizzo, uno spigolo d'angolo di un corpo o un punto di costruzione. Niente significa l'origine del progetto. |
| **Famiglia** | Il gruppo di elementi mostrato sotto **Elemento**. | Base | Partenza, Base, Complementare, Architrave, Telaio finestra, Chiusura, Angolo, Parete divisoria |
| **Elemento** | L'elemento da posizionare, con le sue dimensioni in mm (lunghezza x larghezza x altezza). | S1 WP | Gli elementi della famiglia scelta. Vedere gli elenchi in [usage.md](usage.md). |
| (immagine) | Mostra l'elemento scelto. Non può essere modificata. | Immagine dell'elemento scelto | – |
| **Posiziona da** | Quale punto dell'elemento finisce sul punto. | Angolo inferiore anteriore destro | 15 voci: tre angoli e i dodici punti. Vedere sotto. |
| **Rotazione** | Ruota l'elemento attorno all'asse verticale (Z), intorno al punto scelto sotto **Posiziona da**. | 0 gradi | Qualsiasi angolo. Positivo è in senso antiorario visto dall'alto. |
| **Spostamento X** | Sposta l'elemento lungo l'asse X del progetto. | 0 mm | Qualsiasi lunghezza, anche negativa |
| **Spostamento Y** | Sposta l'elemento lungo l'asse Y del progetto. | 0 mm | Qualsiasi lunghezza, anche negativa |
| **Spostamento Z** | Sposta l'elemento lungo l'asse Z del progetto. | 0 mm | Qualsiasi lunghezza, anche negativa |

L'add-in non pone alcun limite superiore o inferiore alla rotazione e agli spostamenti.

### Le voci sotto "Posiziona da"

In quest'ordine:

1. Angolo inferiore anteriore destro
2. Angolo superiore anteriore destro
3. Angolo superiore anteriore sinistro
4. sotto davanti
5. sotto centro
6. sotto dietro
7. sopra davanti
8. sopra centro
9. sopra dietro
10. sopra centro destra
11. sopra centro sinistra
12. sotto centro destra
13. sotto centro sinistra
14. centro destra, 50 mm sopra
15. centro sinistra, 50 mm sopra

Che cosa significa ogni voce è spiegato in [usage.md](usage.md).

Stato: **Posiziona da** e i tre spostamenti sono testati solo offline, **non dentro Fusion**.

## Che cosa viene ricordato

Dopo aver premuto **OK** e dopo che l'elemento è stato creato, l'add-in ricorda questi valori per la volta successiva:

- **Famiglia**
- **Elemento**
- **Posiziona da**
- **Rotazione**
- **Spostamento X**, **Spostamento Y**, **Spostamento Z**

Non viene ricordato: il **Punto**.

| Domanda | Risposta |
| --- | --- |
| Per quanto tempo? | Finché Fusion non viene chiuso o l'add-in non viene arrestato. I valori esistono solo in memoria. |
| Vengono salvati in un file? | No. |
| Vengono salvati nel progetto? | No. |
| E se si annulla la finestra di dialogo? | Non viene ricordato nulla. Restano i valori dell'ultimo posizionamento riuscito. |
| E dopo un riavvio? | Valgono di nuovo i valori predefiniti della tabella qui sopra. |

## Lingua

L'add-in ha i suoi testi in cinque lingue: tedesco, inglese, spagnolo, francese e italiano.

La lingua non si può scegliere nell'add-in. Viene scelta all'avvio dell'add-in:

1. L'add-in chiede a Fusion la lingua impostata nelle preferenze di Fusion. Se è una delle cinque, viene usata.
2. Altrimenti guarda le impostazioni di lingua del sistema operativo (le variabili d'ambiente `LANG`,
   `LANGUAGE`, `LC_ALL`, poi le impostazioni locali del sistema).
3. Se nessuna di queste dà una delle cinque lingue, viene usato l'inglese.

Altri dettagli:

- Per cambiare lingua, cambiare la lingua nelle preferenze di Fusion e avviare di nuovo l'add-in.
- Se in una lingua manca un testo, al suo posto viene mostrato il testo inglese.
- I nomi degli elementi (`S1 WP`) e dei componenti (`SYSTEM 3E S1 WP`) non vengono tradotti.
- I nomi dei dodici punti vengono scritti nel progetto quando un elemento viene posizionato per la prima volta. Mantengono quella
  lingua, anche se in seguito l'add-in funziona in un'altra lingua.

## Valori fissi che non si possono cambiare nella finestra di dialogo

| Valore | Impostazione |
| --- | --- |
| Posto del pulsante | Area di lavoro di progettazione, pannello **Create** degli strumenti per solidi |
| Avvio con Fusion | Sì (`runOnStartup` nel file manifest) |
| Punti a 50 mm sopra il lato inferiore | Fissi a 50 mm |
