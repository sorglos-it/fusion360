# Utilizzo

## Il comando dimostrativo

Il comando dimostrativo traccia una linea corta (un "segno") a metà di una linea di schizzo. Il segno è ad angolo retto rispetto a quella linea.
Il suo unico compito è mostrare che selezione, anteprima, controlli e traduzione funzionano. Sostituirlo con il proprio comando.

Nel modello non modificato il comando si chiama **Modello di add-in**. La sua descrizione comando dice:

> Punto di partenza per un add-in di Fusion 360.
> Traccia un segno a metà della linea selezionata.

### La finestra di dialogo

| Campo | Tipo | Significato | Valore iniziale |
| --- | --- | --- | --- |
| **Linea** | selezione, testo di richiesta "Seleziona una linea di schizzo" | La linea di schizzo che riceve il segno. Esattamente una linea. Si possono selezionare solo linee di schizzo | vuoto, oppure la linea che era selezionata prima |
| **Lunghezza** | valore in mm | Lunghezza del segno. Accetta espressioni come `2 * 3 mm` | 10 mm |
| **Inverti direzione** | casella di controllo | Traccia il segno dall'altro lato della linea | disattivata |

### Provarlo

1. Aprire uno schizzo e disegnare una linea.
2. Fare clic sulla linea.
3. Premere il pulsante **Modello di add-in**. La linea è già inserita in **Linea**.
4. Inserire una **Lunghezza**. L'anteprima mostra subito il segno.
5. Spuntare **Inverti direzione** per girare il segno dall'altro lato.
6. Premere **OK**.

Si può anche premere prima il pulsante e selezionare la linea dopo.

### Regole che il comando controlla

| Regola | Messaggio quando non è rispettata |
| --- | --- |
| È selezionata esattamente una linea di schizzo | "Seleziona esattamente una linea di schizzo." |
| La lunghezza è maggiore di 0 | "La lunghezza deve essere maggiore di 0." |
| La linea selezionata è più lunga di 0 | "La linea selezionata ha lunghezza zero." |
| Il segno non è più lungo della linea selezionata | "La lunghezza supera la linea selezionata ({0} mm)." |

Finché una regola non è rispettata, **OK** è disattivato (grigio) e l'anteprima resta vuota. La finestra di dialogo **non** dice perché.
Il testo del messaggio compare come finestra di messaggio solo se l'errore avviene quando il comando viene eseguito.

### Altro comportamento

- **Lunghezza** e **Inverti direzione** vengono ricordati per la chiamata successiva. Vengono dimenticati quando Fusion si chiude o l'add-in viene riavviato.
- Il comando è ripetibile (`isRepeatable` è impostato), quindi la funzione "repeat last command" di Fusion può avviarlo di nuovo.
- Dettagli della geometria: vengono usati solo i valori X e Y dei punti finali della linea nello schizzo. Il segno viene tracciato a Z = 0 dello schizzo.

Il comportamento dentro Fusion è descritto a partire dal codice. Per questa documentazione non è stato testato in Fusion.

## Farne il proprio add-in

Prima creare una copia con lo script, vedere [installation.md](installation.md). Poi lavorare in `<name>.py`.

Il file di ingresso ha tre zone:

| Zona | Contenuto | Modificare? |
| --- | --- | --- |
| sopra `CONFIGURE` | carica il modulo core | solo quando si aggiungono altri moduli propri |
| da `CONFIGURE` a `END OF TEMPLATE` | impostazioni e le proprie funzioni | **sì – questa è la propria zona** |
| sotto `END OF TEMPLATE` | gli handler di eventi, `run` e `stop` | di norma no |

### Passo per passo

1. **Impostare gli id.** Controllare `CMD_ID`, `WORKSPACE_ID` e `PANEL_IDS`. Vedere [settings.md](settings.md).
2. **Dare un nome ai campi di input.** Sostituire `IN_LINE`, `IN_LENGTH`, `IN_FLIP` con id per i propri campi.
3. **Impostare i valori iniziali.** Mettere in `_last` il valore iniziale di ogni campo ricordato. Le lunghezze sono in cm.
4. **Costruire la finestra di dialogo** in `build_inputs(inputs)`.
5. **Leggere la finestra di dialogo** in `read_inputs(inputs)`.
6. **Controllare i valori** in `validate(values)`.
7. **Fare il lavoro** in `build_result(values)`.
8. **Ricordare i valori** in `remember(values)`.
9. **Reagire alle modifiche** in `on_input_changed(inputs, changed)`, se un campo deve modificarne un altro.
10. **Scrivere i testi.** Aggiungere le proprie chiavi a `lang/en.xml`, poi tradurre gli altri file. Sostituire la descrizione comando `TODO`.
11. **Adattare la preselezione.** `CommandCreatedHandler` (sotto `END OF TEMPLATE`) raccoglie le linee di schizzo che erano selezionate prima di premere il pulsante. Se il proprio comando ha bisogno di un altro tipo di oggetto, cambiare lì il controllo del tipo, oppure rimuovere il blocco.
12. **Disegnare un'icona**, vedere [development.md](development.md).
13. **Compilare il manifest**: descrizione, autore, versione. Vedere [settings.md](settings.md).
14. **Eseguire il controllo offline**, vedere [development.md](development.md).
15. **Provarlo in Fusion.** Dopo ogni modifica arrestare l'add-in ed eseguirlo di nuovo.

### Le funzioni da modificare

| Funzione | A che cosa serve | Regole |
| --- | --- | --- |
| `build_inputs(inputs)` | Dispone la finestra di dialogo. Ogni etichetta viene dal catalogo dei testi tramite `T('key')` | Restituisce il campo di selezione. Il chiamante vi mette la linea preselezionata. Restituire `None` se non c'è un campo di selezione |
| `read_inputs(inputs)` | Legge ogni valore dalla finestra di dialogo in un unico posto e restituisce un `dict` | Esecuzione, anteprima e validazione la chiamano tutte, quindi vedono gli stessi numeri |
| `validate(values)` | Si ferma con `fail('err.key')` per tutto ciò che l'utente deve correggere | Viene eseguita prima di disegnare e di nuovo per il pulsante OK. Un valore impossibile disattiva OK invece di fallire a metà strada |
| `build_result(values)` | Fa il lavoro vero e proprio | Quando viene eseguita tutto è già controllato. Viene eseguita per l'anteprima **e** per il risultato vero |
| `remember(values)` | Copia i valori in `_last` per la chiamata successiva | Chiamata solo dopo un'esecuzione riuscita |
| `on_input_changed(inputs, changed)` | Attiva, disattiva o adatta un campo a partire da un altro | Vuota nel modello. Impostare `_updating` attorno a ogni valore che si riscrive, altrimenti la scrittura chiama di nuovo questa funzione |

### Funzioni di supporto da chiamare

| Funzione di supporto | Che cosa fa |
| --- | --- |
| `T(key, *args)` | Restituisce il testo di `key` nella lingua attiva. `args` riempiono `{0}`, `{1}`, … |
| `fail(key, *args)` | Solleva un `AddInError` con il testo di `key`. Usarla per tutto ciò che l'utente può correggere |
| `core.report(ui, S, key)` | Mostra un errore imprevisto con il suo traceback. Solo per ciò che è davvero imprevisto |

### Aggiungere un testo

1. Aggiungere una riga a `lang/en.xml`: `<string key="in.width">Width</string>`
2. Usarla nel codice: `T('in.width')`
3. Aggiungere la stessa chiave agli altri file di lingua.

Le chiavi mancanti in un'altra lingua vengono mostrate in inglese. I segnaposto come `{0}` devono restare in ogni traduzione.
