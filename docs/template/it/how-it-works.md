# Come funziona

## Due file

| File | Ruolo |
| --- | --- |
| File di ingresso `AddInTemplate.py` (poi `<name>.py`) | Ciò che Fusion avvia. Contiene le impostazioni, le proprie funzioni, gli handler di eventi, `run` e `stop` |
| Modulo core `addin_core.py` (poi `<name>_core.py`) | Parti che servono a ogni add-in e che è facile sbagliare. Nulla al suo interno appartiene a un solo add-in |

Fusion trova un add-in tramite il nome: cartella, file `.py` e file `.manifest` devono portare lo stesso nome.

## Che cosa contiene il modulo core

| Parte | Compito |
| --- | --- |
| `Strings` | Catalogo dei testi letto da `lang/<code>.xml`, con l'inglese come ripiego |
| `detect_language()` | Trova la lingua su cui è impostato Fusion |
| `AddInError` | Tipo di errore per i problemi che l'utente può correggere. Porta una chiave che non dipende dalla lingua |
| `HandlerRegistry` | Mantiene in vita gli handler di eventi |
| `find_panel()` | Trova, in un elenco, il primo pannello della barra degli strumenti che esiste |
| `add_button()` | Mette il comando su un pannello. Prima rimuove un controllo rimasto da un ricaricamento |
| `remove_button()` | Toglie di nuovo dalla barra degli strumenti il controllo e la definizione del comando |
| `report()` | Mostra un errore imprevisto con il suo traceback in una finestra di messaggio |
| `read_version()` | Legge la versione dal manifest |
| `display_name()` | Unisce nome e versione: `Name (1.0.0.0)` |
| `FALLBACK_LANGUAGE`, `SUPPORTED_LANGUAGES`, `FUSION_LANGUAGE_MAP` | Le tabelle delle lingue |

## Perché il modulo core viene rinominato per ogni add-in

Tutti gli add-in girano nello stesso Python dentro Fusion. Condividono un unico elenco di moduli caricati (`sys.modules`).
Se due add-in caricassero entrambi un modulo chiamato `addin_core`, si sovrascriverebbero a vicenda il modulo core.

Perciò lo script rinomina il file in `<name in lower case>_core.py` e imposta di conseguenza `_CORE_MODULE` nel file di ingresso.

Conseguenza: ogni add-in ha la **propria copia** del modulo core. Una correzione fatta in seguito nel modello non arriva agli add-in creati prima. Va copiata a mano.

## Caricamento del modulo core

Il file di ingresso fa questo prima di ogni altra cosa:

1. Aggiunge la propria cartella al percorso di ricerca di Python.
2. Rimuove il modulo core da `sys.modules`, se c'è.
3. Importa il modulo core con il nome indicato in `_CORE_MODULE`.

Motivo del passo 2: Fusion tiene in cache i moduli importati. Senza di esso un modulo core modificato manterrebbe la vecchia versione fino al riavvio di Fusion. Con esso basta arrestare ed eseguire l'add-in.

## Registro degli handler

Fusion mantiene solo un riferimento debole a un handler di eventi. Un handler a cui Python non fa più riferimento viene eliminato, e il suo evento smette di scattare – senza alcun messaggio di errore. Il commento nel codice lo definisce il modo più comune in cui un add-in funziona a metà.

`HandlerRegistry.add(event, handler)` collega l'handler all'evento **e** lo conserva in un elenco. `clear()` svuota l'elenco quando l'add-in si arresta.

## Avvio e arresto

### `run(context)`

1. Carica nel catalogo dei testi la lingua rilevata.
2. Elimina una definizione di comando con lo stesso `CMD_ID` rimasta da un'esecuzione precedente. Manterrebbe la vecchia etichetta e il vecchio handler.
3. Crea la definizione del pulsante: nome con versione, descrizione comando, cartella delle icone (se esiste).
4. Collega `CommandCreatedHandler`.
5. Cerca un pannello. Se non ne trova nessuno mostra "Nessun pannello della barra degli strumenti adatto trovato." e termina.
6. Aggiunge il pulsante al pannello.

Ogni altro errore viene mostrato come "Avvio non riuscito:" con il traceback.

### `stop(context)`

1. Rimuove il controllo dal pannello ed elimina la definizione del comando.
2. Svuota il registro degli handler.

Un errore viene mostrato come "Arresto non riuscito:" con il traceback.

## Flusso degli eventi

```
button pressed
   -> commandCreated   build the dialog, connect the four handlers below
        -> inputChanged     a field changed        -> on_input_changed()
        -> validateInputs   may OK be pressed?     -> read_inputs(), validate()
        -> executePreview   show a preview         -> read_inputs(), validate(), build_result()
        -> execute          OK pressed             -> read_inputs(), validate(), build_result(), remember()
```

| Evento | Handler | Che cosa fa | In caso di errore |
| --- | --- | --- | --- |
| creazione | `CommandCreatedHandler` | Contrassegna il comando come ripetibile. Raccoglie le linee di schizzo selezionate prima di premere il pulsante. Chiama `build_inputs()`. Mette la prima linea raccolta nel campo di selezione, se questo è ancora vuoto. Collega gli altri quattro handler | Finestra di messaggio "Errore durante la costruzione della finestra di dialogo:" con traceback |
| modifica di un campo | `InputChangedHandler` | Chiama `on_input_changed()`. Non fa nulla finché `_updating` è impostato | in silenzio |
| validazione | `ValidateHandler` | Chiama `read_inputs()` e `validate()`. Imposta `areInputsValid` su true, oppure su false a ogni errore | OK è disattivato (grigio), nessun messaggio |
| anteprima | `PreviewHandler` | Esegue l'intero comando. Poi imposta `isValidResult` su `False`, così Fusion scarta l'anteprima ed esegue l'esecuzione per il risultato vero | in silenzio, nessuna anteprima |
| esecuzione | `ExecuteHandler` | Esegue l'intero comando, poi `remember()` | `AddInError`: finestra di messaggio con il testo tradotto. Tutto il resto: "Errore durante la creazione della geometria:" con traceback |

"Esegue l'intero comando" significa `_run_command()`: `read_inputs()`, poi `validate()`, poi `build_result()`.

Punti che ne derivano:

- La selezione viene letta **prima** che i campi di input vengano creati, e passata al campo di selezione dopo. Per questo "cliccare una linea, poi premere il pulsante" funziona.
- L'anteprima scatta a ogni tasto premuto e vede valori digitati a metà. Perciò tace di proposito in caso di errori.
- Né l'anteprima né la validazione dicono all'utente **perché** qualcosa non va. Solo l'esecuzione mostra un testo.
- `build_result()` viene eseguita due volte per un solo OK: una o più volte per l'anteprima, una volta per il risultato vero.
- Impostare `isValidResult` su `True` solo se l'anteprima ha già prodotto il risultato finale.

## Due tipi di errori

| Tipo | Come viene sollevato | Che cosa vede l'utente |
| --- | --- | --- |
| Previsto – l'utente può correggerlo | `fail('err.key')` solleva `AddInError` | OK disattivato (grigio); una finestra di messaggio con il testo tradotto solo all'esecuzione |
| Imprevisto – un bug | qualsiasi altra eccezione | Una finestra di messaggio con il traceback, tramite `core.report()` |

`AddInError` conserva la chiave (`err.key`) e i parametri (`err.params`). Il testo viene cercato quando l'errore viene creato.
Il codice del modello non legge la chiave in seguito; è lì per il proprio codice.

## Catalogo dei testi e ripiego

`S = core.Strings(LANG_DIR)` viene creato quando il file di ingresso viene importato. L'inglese viene caricato subito, quindi i testi esistono anche prima di `run()`.
`run()` carica poi la lingua rilevata.

Come funziona `load(code)`:

1. Un codice che non è in `SUPPORTED_LANGUAGES` diventa `en`.
2. `en.xml` viene letto una volta sola e tenuto come ripiego.
3. Il file della lingua scelta viene letto come insieme corrente.

Come viene trovato un testo (`get(key, *args)`):

1. il testo della lingua corrente, se esiste e non è vuoto
2. altrimenti il testo inglese
3. altrimenti la chiave stessa, per esempio `in.width`

Poi vengono riempiti i segnaposto. Se il riempimento non riesce – per esempio una traduzione chiede `{1}` ma è stato dato un solo valore – il testo viene restituito non riempito invece di sollevare un errore.

Un file di lingua che manca o non è XML valido conta come vuoto. Allora ogni testo viene dall'inglese.
Se anche `en.xml` manca o è rotto, vengono mostrate le chiavi stesse.

## Rilevamento della lingua

Per l'ordine vedere [settings.md](settings.md). Due dettagli dal codice:

- I valori di lingua di Fusion vengono cercati per nome con `getattr`. Un valore che questa versione di Fusion non conosce non può rompere l'add-in.
- La funzione non solleva mai un errore. Nel caso peggiore restituisce l'inglese.

## Unità

Fusion conta internamente le lunghezze in cm. L'esempio dimostrativo lo fa vedere:

- il valore iniziale `1.0` viene mostrato come 10 mm
- il valore letto dal campo della lunghezza è in cm
- per il messaggio "La lunghezza supera la linea selezionata ({0} mm)." la lunghezza della linea viene moltiplicata per 10 e mostrata con due decimali

## Dati

L'add-in legge il suo manifest e i suoi file di lingua. Non scrive file.
