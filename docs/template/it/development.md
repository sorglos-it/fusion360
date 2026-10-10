# Sviluppo

## Cartelle

| Percorso | Contenuto |
| --- | --- |
| `apps/desktop-template/AddInTemplate/` | L'add-in modello, come serve a Fusion |
| `apps/desktop-template/AddInTemplate/AddInTemplate.py` | File di ingresso |
| `apps/desktop-template/AddInTemplate/addin_core.py` | Modulo core |
| `apps/desktop-template/AddInTemplate/AddInTemplate.manifest` | Manifest |
| `apps/desktop-template/AddInTemplate/lang/` | `de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` |
| `apps/desktop-template/AddInTemplate/resources/AddInTemplate/` | Icone `16x16.png`, `32x32.png`, `64x64.png` |
| `apps/desktop-template/VERSION` | Numero di versione di questa parte |
| `apps/desktop-template/tests/test_addin.py` | Controllo offline |
| `tools/template/new_addin.py` | Script di generazione, vedere [installation.md](installation.md) |
| `tools/template/make_icon.py` | Strumento per le icone |
| `tools/template/test_addin.py` | Inoltra al controllo offline (vecchio percorso) |
| `tools/set_version.py` | Imposta i numeri di versione, per tutti gli add-in del repository |
| `tools/release.py` | Crea lo ZIP di un add-in, per tutti gli add-in del repository |
| `docs/template/` | README, CHANGELOG, LICENSE e questa documentazione |
| `dist/` | File ZIP creati. Non in Git |

Non c'è una fase di compilazione. L'add-in funziona così com'è. Tutti gli strumenti usano solo la libreria standard di Python.

## Controllo offline

Il controllo verifica un add-in senza avviare Fusion. Il commento nel codice lo definisce l'unico ciclo di riscontro che non richiede un riavvio.

```bash
python apps/desktop-template/tests/test_addin.py                    # the template itself
python apps/desktop-template/tests/test_addin.py --path ../MyAddIn  # an add-in next to the repository
```

| Opzione | Valore predefinito | Effetto |
| --- | --- | --- |
| `--addin NAME` | `AddInTemplate` | Nome della cartella dentro `apps/desktop-template` di questo repository |
| `--path DIR` | – | Percorso completo di una cartella di add-in. Prevale su `--addin` |

Per un add-in creato con `--install`, passare a `--path` la sua cartella nella cartella degli add-in di Fusion.

Il vecchio comando `python tools/template/test_addin.py` funziona ancora. Inoltra al controllo con gli stessi argomenti, lo stesso output e lo stesso codice di uscita.

### Come funziona

Mette al loro posto dei sostituti vuoti dei moduli `adsk`, `adsk.core` e `adsk.fusion` e poi importa l'add-in.
Solo le classi base degli handler sono classi vere (vuote). Quindi il controllo dimostra che il file si importa e che i testi sono in ordine. **Non** esegue alcuna chiamata a Fusion: nessuna finestra di dialogo, nessuna geometria, nessun `run()`.

### Che cosa controlla

| Sezione | Controlli |
| --- | --- |
| 1) Struttura | La cartella esiste. `<name>.py` e `<name>.manifest` corrispondono al nome della cartella. `lang/` esiste |
| 2) Manifest | JSON valido. `type` è `addin`. `autodeskProduct` è `Fusion360`. `id` ha l'aspetto di un GUID. Avvisi: GUID segnaposto, autore `Your Name` |
| 3) Importazione | L'add-in si importa. `run` e `stop` esistono. `CMD_ID` è impostato. `_CORE_MODULE` ha un file corrispondente. Avvisi: `CMD_ID` ancora al valore del modello, modulo core non rinominato |
| 4) File di lingua | `SUPPORTED_LANGUAGES` è disponibile. `en.xml` esiste e ha delle chiavi. Per ogni lingua supportata: il file esiste, dichiara il `language` giusto, ha ogni chiave, non ha chiavi sconosciute, mantiene ogni segnaposto, non ha testi vuoti |
| 5) Catalogo dei testi | Ogni lingua si carica e restituisce un `cmd.name`. Una lingua sconosciuta ricade sull'inglese. Una chiave mancante restituisce la chiave. Avviso: la descrizione comando dice ancora `TODO` |
| 6) Icone | `resources/<name>/` esiste. I tre file PNG esistono e iniziano con la firma PNG |

### Risultato

- Le righe iniziano con `ok`, `FAIL` o `warn`.
- Con almeno un `FAIL` lo script termina con codice di uscita 1 e stampa il numero di errori.
- Gli avvisi non cambiano il codice di uscita.
- Senza errori stampa `all checks passed`.

Esecuzione per questa documentazione sul modello, versione 1.0.0.0: `3 warning(s)`, `all checks passed`. I tre avvisi (GUID segnaposto, autore, id del comando) sono normali per il modello.

## Strumento per le icone

Fusion vuole tre file PNG con trasparenza: 16x16, 32x32 e 64x64 pixel, nella cartella passata alla definizione del pulsante.

```bash
python tools/template/make_icon.py                            # the template's placeholder
python tools/template/make_icon.py --root .. --addin MyAddIn  # an add-in next to the repository
```

| Opzione | Valore predefinito | Effetto |
| --- | --- | --- |
| `--addin NAME` | `AddInTemplate` | Nome della cartella dell'add-in |
| `--root DIR` | `apps/desktop-template` di questo repository | Cartella che contiene l'add-in |

I file vengono scritti in `<root>/<addin>/resources/<addin>/`. La cartella viene creata se serve. Le icone esistenti vengono sovrascritte.

Per disegnare una propria icona, modificare lo script:

| Nome | Significato |
| --- | --- |
| `SHAPES` | Elenco di `(colour, polygon)`. I punti vanno da 0 a 1, con y rivolto verso l'**alto**. Dove le forme si sovrappongono, quella elencata per prima resta sopra |
| `DARK`, `ACCENT` | I due colori come valori RGB |
| `SS` | Campioni per lato di pixel per bordi lisci. 4 dà bordi puliti fino a 16 px |

Il segnaposto mostra quattro parentesi d'angolo e una diagonale. Ha l'aspetto di un segnaposto di proposito. Sostituirlo prima di distribuire il proprio add-in.

## Numeri di versione

Le versioni hanno quattro parti: `v.x.y.z` (versione, rilascio, funzione, build). Attuale: `1.0.0.0`.

Il numero è tenuto in due posti:

- `apps/desktop-template/VERSION`
- il campo `version` del manifest – Fusion e il titolo della finestra di dialogo leggono questo

Non modificarli mai a mano. Usare lo strumento, che li scrive entrambi:

```bash
python tools/set_version.py template 1.0.0.1   # this part
python tools/set_version.py all 1.0.0.0        # every add-in of the repository
python tools/set_version.py --check            # report differences
```

- `template` è il nome della cartella `apps/desktop-template` senza `desktop-`.
- `--check` stampa una riga per add-in, che termina con `ok` o `DIFFERENT OR NOT v.x.y.z`, e restituisce il codice di uscita 1 se una riga è sbagliata.
- Lo strumento lavora solo sugli add-in di questo repository. In un proprio add-in fuori dal repository, modificare direttamente il campo `version` del suo manifest – lì è l'unico posto.

## Creazione del pacchetto

```bash
python tools/release.py template
python tools/release.py all
```

- Scrive `dist/AddInTemplate-<version>.zip`.
- Lo ZIP contiene la cartella `AddInTemplate` come la vuole Fusion. Estrarlo nella cartella degli add-in di Fusion.
- Esclusi: `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compressione: Deflate al livello più alto, così ogni programma di estrazione può leggerlo.
- Rifiuta di creare il pacchetto se `VERSION` e il manifest differiscono o se il numero non ha quattro parti.
- Dopo la creazione testa lo ZIP e stampa il numero di file e la dimensione.
- Gli strumenti (`tools/`) non sono nello ZIP. Esistono solo nel repository.

Non è stato rilasciato alcuno ZIP della versione 1.0.0.0. Il modello si usa dal repository.

## Decisioni e loro motivi

| Decisione | Motivo indicato nel codice |
| --- | --- |
| File di ingresso e modulo core sono separati | Il core contiene ciò che serve a ogni add-in e ciò che è facile sbagliare. Il proprio codice resta tra due marcatori |
| Il modulo core viene rinominato per ogni add-in | Due add-in nati da questo modello non devono sovrascriversi a vicenda il modulo core in `sys.modules` |
| Il modulo core viene rimosso da `sys.modules` prima dell'importazione | Fusion tiene in cache i moduli. In questo modo "arrestare, eseguire" recepisce le modifiche |
| Tutti gli handler passano per `HandlerRegistry` | Fusion mantiene gli handler debolmente. Quelli senza riferimento vengono eliminati e l'evento smette di scattare in silenzio |
| `PANEL_IDS` è un elenco, con una ricerca globale come secondo tentativo | Gli id dei pannelli cambiano tra le versioni di Fusion |
| Una definizione di comando obsoleta viene eliminata all'avvio | Manterrebbe la vecchia etichetta e il vecchio handler |
| `read_inputs()` è l'unico posto che legge la finestra di dialogo | Esecuzione, anteprima e validazione guardano esattamente gli stessi numeri |
| `validate()` viene eseguita prima di disegnare e di nuovo per il pulsante OK | Un valore impossibile disattiva OK invece di fallire a metà strada |
| L'anteprima inghiotte gli errori | Scatta a ogni tasto premuto, anche per valori digitati a metà |
| L'anteprima imposta `isValidResult` su `False` | Fusion esegue allora l'esecuzione per il risultato vero |
| Gli errori portano una chiave, non solo un testo | Il motivo è noto senza analizzare testo in una qualche lingua |
| `report()` è solo per gli errori imprevisti | Ciò che l'utente può correggere deve essere un `AddInError`, così OK viene bloccato invece di far comparire una finestra di dialogo |
| L'inglese è il ripiego per ogni testo | Una traduzione fatta a metà mostra l'inglese invece delle chiavi nude |
| I valori di lingua di Fusion vengono cercati per nome | Un valore che questa versione di Fusion non conosce non può rompere l'add-in |
| Il rilevamento della lingua non solleva mai un errore | Una build di Fusion con un valore inatteso avvia comunque l'add-in |
| La versione viene letta dal manifest | La finestra di dialogo non può discostarsi dal manifest. Un solo posto in cui aumentarla |
| La versione fa parte del nome del comando | Fusion usa quel nome come titolo della finestra di dialogo. È l'unico posto in cui una versione è visibile mentre la finestra di dialogo è aperta. Compare anche sul pulsante – c'è solo quell'unico nome |
| `isComputeDeferred` viene ripristinato in `finally` | Altrimenti dopo un errore lo schizzo smetterebbe di aggiornarsi |
| La selezione viene letta prima che esistano i campi di input | "Cliccare una linea, poi premere il pulsante" funziona |
| L'icona segnaposto ha l'aspetto di un segnaposto | Un'icona che non è stata sostituita si nota facilmente |
| Lo script scrive i file con fine riga `\n` e in UTF-8 | Non spiegato nel codice |
| Chiavi, identificatori e commenti sono in inglese | Non spiegato nel codice; il README esistente dice che così un traduttore non deve mai aprire un file `.py` |

## Licenza

MIT. Autore: Sorglos Thomas Weirich. Vedere [LICENSE](../LICENSE).
