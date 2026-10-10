# Risoluzione dei problemi

I testi qui sotto sono quelli italiani di `lang/it.xml`. In un'altra lingua l'add-in mostra la traduzione.
Ogni finestra di messaggio ha come titolo il nome del comando.

## Messaggi del comando dimostrativo

Questi quattro vengono da `validate()`. Finché uno di essi vale, **OK** è disattivato (grigio) e non viene mostrata alcuna anteprima – senza alcun testo.
Il testo stesso compare come finestra di messaggio solo se l'errore avviene nel momento in cui il comando viene eseguito.

| Messaggio | Causa | Che cosa fare |
| --- | --- | --- |
| "Seleziona esattamente una linea di schizzo." | Il campo **Linea** è vuoto, oppure l'oggetto selezionato non è una linea di schizzo | Selezionare una linea di schizzo rettilinea |
| "La lunghezza deve essere maggiore di 0." | **Lunghezza** è 0 o negativa | Inserire una lunghezza superiore a 0 |
| "La linea selezionata ha lunghezza zero." | Punto iniziale e punto finale della linea si trovano nello stesso posto (vengono confrontati solo X e Y) | Selezionare un'altra linea |
| "La lunghezza supera la linea selezionata ({0} mm)." | **Lunghezza** è maggiore della linea selezionata. `{0}` è la lunghezza della linea in mm con due decimali | Inserire una lunghezza fino a quel valore, oppure selezionare una linea più lunga |

## Messaggi dell'add-in stesso

I quattro messaggi con `{0}` mostrano un traceback di Python al posto di `{0}`. Il traceback indica il file e la riga dell'errore.

| Messaggio | Quando | Causa | Che cosa fare |
| --- | --- | --- | --- |
| "Nessun pannello della barra degli strumenti adatto trovato." | all'avvio | Nessuno degli id in `PANEL_IDS` esiste, né nell'area di lavoro `WORKSPACE_ID` né altrove in Fusion. L'add-in è in esecuzione ma non ha un pulsante | Mettere in `PANEL_IDS` id di pannelli che esistono nella propria versione di Fusion. Vedere [settings.md](settings.md) |
| "Errore durante la creazione della geometria: {0}" | dopo OK | Un errore imprevisto in `read_inputs()`, `validate()`, `build_result()` o `remember()` – un bug, non un valore sbagliato | Leggere le ultime righe del traceback e correggere il codice. Se può causarlo l'utente, intercettare il caso in `validate()` con `fail('err.key')` |
| "Errore durante la costruzione della finestra di dialogo: {0}" | quando si preme il pulsante | Un errore imprevisto in `build_inputs()` o durante il collegamento degli handler | Leggere il traceback. Tipico: lo stesso id di campo usato due volte, oppure un testo di unità sbagliato |
| "Avvio non riuscito: {0}" | quando l'add-in si avvia | Un errore imprevisto in `run()` | Leggere il traceback |
| "Arresto non riuscito: {0}" | quando l'add-in si arresta | Un errore imprevisto in `stop()` | Leggere il traceback. Riavviare Fusion se il pulsante resta sulla barra degli strumenti |

Le cause "tipiche" in questa tabella sono esempi. Per questa documentazione non sono state riprodotte in Fusion.

## Messaggi dello script di generazione

| Messaggio | Causa | Che cosa fare |
| --- | --- | --- |
| `The name must start with a letter and contain only letters and digits - it becomes a Python module name. Got: '…'` | Il nome ha uno spazio, un trattino, un trattino basso, un altro segno, oppure inizia con una cifra | Usare un nome come `MyAddIn` |
| `Pick a name other than AddInTemplate.` | Il nome è quello del modello stesso | Scegliere un altro nome |
| `Template folder not found: …` | Manca `apps/desktop-template/AddInTemplate`. Lo script è stato spostato, oppure il repository è incompleto | Eseguire lo script da una copia completa del repository |
| `… already exists. Pass --force to overwrite it.` | La cartella di destinazione esiste | Scegliere un altro nome o un'altra cartella. `--force` elimina la cartella esistente con tutto ciò che contiene |
| `Use either --install or --out, not both.` | Sono state date entrambe le opzioni | Usarne una sola |

Su un sistema che non è macOS, `--install` costruisce il percorso dalla variabile d'ambiente `APPDATA`. Se non è impostata (per esempio su Linux), la cartella viene creata relativamente alla cartella corrente. Lì usare `--out`.

## Messaggi degli strumenti di versione e di creazione del pacchetto

| Messaggio | Causa | Che cosa fare |
| --- | --- | --- |
| `The version needs four numbers, like 1.0.0.0 - got '…'` | La versione non ha quattro parti | Usare `v.x.y.z`, per esempio `1.0.0.1` |
| `No add-in "…". There are: …` | Il nome non è una cartella `apps/desktop-<name>` con esattamente un manifest | Usare un nome dell'elenco. Il modello si chiama `template` |
| `No "version" entry in …` | Il manifest non ha un campo `version` | Aggiungere il campo al manifest |
| `DIFFERENT OR NOT v.x.y.z` (da `--check`) | `VERSION` e il manifest differiscono, oppure il numero non ha quattro parti | Eseguire `python tools/set_version.py template <version>` |
| `template: VERSION and manifest disagree - run tools/set_version.py first.` | Come sopra, notato durante la creazione del pacchetto | Come sopra, poi creare di nuovo il pacchetto |
| `template: … is damaged in the ZIP` | Il test dello ZIP dopo la creazione del pacchetto non è riuscito | Creare di nuovo il pacchetto; controllare il disco |

## Controllo offline: FAIL e warn

Il controllo è descritto in [development.md](development.md). Una riga `FAIL` indica che cosa non va. Le righe `warn` non fanno fallire il controllo.

| Avviso | Significato |
| --- | --- |
| `id is not the placeholder GUID` | Il manifest ha ancora gli zeri come `id` |
| `author has been filled in` | L'autore è ancora `Your Name` |
| `CMD_ID is no longer the template default` | `CMD_ID` è ancora `thwAddInTemplateCmd` |
| `the core module was renamed, so it cannot clash with another add-in` | Un add-in diverso dal modello usa ancora `addin_core` |
| `cmd.tooltip no longer says TODO` | La descrizione comando inglese contiene ancora `TODO` |

Per il modello stesso i primi tre avvisi sono normali.

## Insidie

Vengono dai commenti nel codice.

| Sintomo | Causa | Che cosa fare |
| --- | --- | --- |
| Una modifica al codice non ha effetto | Fusion tiene in cache i moduli importati. Un modulo modificato mantiene la vecchia versione fino al riavvio di Fusion | Arrestare l'add-in ed eseguirlo di nuovo. Questo funziona per il modulo core, perché il file di ingresso lo rimuove da `sys.modules` prima di importarlo. Riservare lo stesso trattamento a ogni altro modulo proprio |
| Il pulsante di un altro add-in fa qualcosa di strano, oppure lo fa il proprio | Due add-in usano lo stesso `CMD_ID`. La collisione è silenziosa | Usare un proprio prefisso e un id univoco |
| Due add-in nati dal modello si disturbano a vicenda | Entrambi usano un modulo core con lo stesso nome | Mantenere il modulo core rinominato `<name>_core.py` |
| Un evento smette di scattare, senza errore | Fusion mantiene gli handler solo debolmente. Un handler a cui Python non fa più riferimento viene eliminato | Collegare ogni handler con `_handlers.add(event, handler)` |
| Il pulsante mantiene una vecchia etichetta o un vecchio comportamento | C'è ancora una definizione di comando di un'esecuzione precedente | `run()` la elimina per prima cosa. Mantenere quel codice |
| OK è grigio e nessuno sa perché | Validazione e anteprima non mostrano un motivo | È voluto. Mantenere le regole semplici e nominarle nella descrizione comando o nelle etichette |
| L'anteprima non mostra nulla | L'anteprima inghiotte ogni errore, anche i bug veri | Premere OK con valori validi. L'esecuzione mostra l'errore con il traceback |
| Compare un messaggio a ogni tasto premuto | La visualizzazione degli errori è stata spostata nell'anteprima | Lasciare l'anteprima silenziosa. Scatta a ogni tasto premuto, anche per valori digitati a metà |
| I valori sono dieci volte troppo grandi o troppo piccoli | Fusion conta in cm, qualunque cosa mostri il campo. `createByReal(1.0)` mostrato in `mm` vale 10 mm | Calcolare in cm. Moltiplicare per 10 solo per la visualizzazione in mm |
| Lo schizzo non si aggiorna più dopo un errore | `isComputeDeferred` è stato impostato su `True` e mai ripristinato | Ripristinarlo in un blocco `finally`, come fa `build_result()` |
| `on_input_changed()` viene eseguita senza fine o due volte | Un valore riscritto lì fa scattare di nuovo l'evento | Impostare `_updating` su `True` prima della scrittura e su `False` dopo. È una variabile di modulo: dichiarare `global _updating` nella funzione |
| Il pulsante manca dopo un aggiornamento di Fusion | Gli id dei pannelli cambiano tra le versioni di Fusion | Elencare più id in `PANEL_IDS`, il più desiderato per primo |
| Il pulsante non ha icona | Manca la cartella `resources/<name>`. Allora l'add-in non passa alcuna cartella delle icone | Creare le icone, vedere [development.md](development.md) |
| Un testo mostra una chiave come `in.width` | La chiave manca nel file di lingua **e** in `en.xml` | Aggiungere la chiave a `en.xml` |
| Un testo mostra `{0}` invece di un valore | I segnaposto del testo non corrispondono ai valori dati | Confrontare il testo con la chiamata `T('key', value)` |
| Tutti i testi sono in inglese | La lingua non è in `SUPPORTED_LANGUAGES`, oppure il suo file manca o non è XML valido | Controllare il file e le tabelle nel modulo core |
| Una correzione nel modello non compare nel proprio add-in | Ogni add-in ha la propria copia del modulo core | Copiare la correzione a mano in `<name>_core.py` |
| Fusion non elenca l'add-in | Cartella, `.py` e `.manifest` non portano lo stesso nome | Dare a tutti e tre lo stesso nome. Il controllo offline lo verifica |
