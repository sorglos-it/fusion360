# Sviluppo

Dovetail è uno dei vari add-in del repository <https://github.com/sorglos-it/fusion360>.
Tutti i percorsi qui sotto sono relativi alla radice del repository.

## Cartelle

| Percorso | Contenuto |
|---|---|
| `apps/desktop-dovetail/Dovetail/` | L'add-in esattamente come lo vuole Fusion: `Dovetail.py`, `Dovetail.manifest`, `lang/`, `resources/` |
| `apps/desktop-dovetail/VERSION` | Il numero di versione, una riga |
| `apps/desktop-dovetail/tests/test_geometry.py` | I test offline |
| `tools/dovetail/make_icons.py` | Scrive l'icona della barra degli strumenti (16, 32, 64 px) in `resources/Dovetail/` |
| `tools/dovetail/make_arrow_icons.py` | Scrive le icone dei pulsanti **Sposta** in `resources/nudge_left`, `nudge_center`, `nudge_right` |
| `tools/dovetail/test_geometry.py` | Rimando al file di test spostato, così il vecchio comando continua a funzionare |
| `tools/set_version.py` | Imposta la versione di un add-in o di tutti (condiviso da tutti gli add-in) |
| `tools/release.py` | Crea lo ZIP di rilascio (condiviso da tutti gli add-in) |
| `docs/dovetail/` | README, CHANGELOG, LICENSE e questa documentazione |
| `dist/` | Risultato di `tools/release.py`; non è in Git |

Fusion richiede che la cartella, il file `.py` e il file `.manifest` abbiano lo stesso nome. Non rinominarne uno solo.

## Struttura di `Dovetail.py`

| Sezione | Parti principali |
|---|---|
| Lingua | `Strings`, `T()`, `detect_language()`, `read_version()`, `display_name()` |
| Geometria | `GeometryError`, `_offset_polyline()`, `_top_half()`, `_check_contour()`, `end_room()`, `max_offset()`, `tooth_directions()`, `build_contours()`, `closed_band()` |
| Disegno | `_to_world()`, `_draw_closed_polyline()`, `line_length()`, `create_geometry()` |
| Gestori | `_read_inputs()`, `_selected_lines()`, `_check_lines()`, `_run()`, `ExecuteHandler`, `PreviewHandler`, `ValidateHandler`, `InputChangedHandler`, `CommandCreatedHandler`, `_apply_nudge()`, `_apply_mirror()` |
| Avvio / arresto | `_find_panel()`, `run()`, `stop()` |

La sezione della geometria è pura matematica. Non usa nulla di Fusion e può girare in qualsiasi Python 3.

## Eseguire i test

Requisiti: Python 3, solo libreria standard. Fusion non serve; il file di test mette piccoli sostituti dei
moduli `adsk` al loro posto prima di importare l'add-in.

```bash
python apps/desktop-dovetail/tests/test_geometry.py
```

Il vecchio comando funziona ancora e dà lo stesso risultato e lo stesso codice di uscita:

```bash
python tools/dovetail/test_geometry.py
```

- Ogni controllo stampa `ok` oppure `FAIL`.
- L'ultima riga è `all tests passed`, oppure il numero di errori.
- Il codice di uscita è 1 se qualcosa è fallito.

Cosa coprono le sezioni:

| Sezione | Contenuto |
|---|---|
| 1–4 | Le tre forme; i punti del profilo; il profilo spostato è parallelo e alla distanza giusta |
| 5 | Allineamento: il gruppo è centrato sul punto medio della linea |
| 6 | Spostamento, spostamento massimo, distanza dagli estremi della linea |
| 7 | Chi paga il gioco (le tre voci di **La linea è**) |
| 8 | Geometria rispecchiata: i due pezzi identici; accettata e rifiutata allo stesso modo in entrambi i versi |
| 9 | Gli errori riportano la chiave giusta; un giunto per ogni linea selezionata; una linea non valida indica se stessa |
| 10 | Ogni voce degli elenchi a discesa e ogni chiave di descrizione comando esiste in `en.xml` |
| 11 | File di lingua: completi, senza chiavi sconosciute, segnaposto conservati, nessun testo vuoto |
| 12 | Catalogo dei testi, ripiego sull'inglese, rilevamento della lingua senza Fusion |

Per provare una copia installata invece di quella del repository, impostare la variabile d'ambiente
`DOVETAIL_ADDIN_DIR` sulla sua cartella. I due script delle icone leggono la stessa variabile.

Non coperto dal file di test:

- Tutto ciò che richiede Fusion: la finestra di dialogo, l'anteprima, il disegno, la conversione in geometria di costruzione,
  l'annullamento dopo un'esecuzione fallita.
- L'esecuzione con 34.317 profili casuali citata nel changelog. È stata una verifica una tantum; non fa parte di
  `test_geometry.py`.

## Icone

```bash
python tools/dovetail/make_icons.py
python tools/dovetail/make_arrow_icons.py
```

Entrambi scrivono file PNG usando solo la libreria standard. Eseguirli solo quando le icone devono cambiare.

## Numeri di versione

Le versioni hanno quattro parti, `v.x.y.z`: versione, rilascio, funzione, build. Esempio: `1.1.0.0`.

Il numero è tenuto in due posti:

- `apps/desktop-dovetail/VERSION`
- la voce `"version"` di `Dovetail.manifest` (è quella che leggono Fusion e il titolo della finestra di dialogo)

Non modificarli mai a mano. Usare lo script, che li scrive entrambi:

```bash
python tools/set_version.py dovetail 1.1.0.1    # set one add-in
python tools/set_version.py all 1.0.0.0         # set all add-ins of the repository
python tools/set_version.py --check             # report add-ins whose two numbers differ
```

Lo script rifiuta un numero che non ha quattro parti. `--check` termina con codice di uscita 1 se un add-in presenta una differenza.

## Creare il pacchetto di rilascio

```bash
python tools/release.py dovetail
```

- Scrive `dist/Dovetail-<version>.zip`.
- Lo ZIP contiene la cartella `Dovetail/` esattamente come la vuole Fusion.
- Esclusi: `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compressione: Deflate al livello più alto, così ogni programma di estrazione può leggerlo.
- Dopo la scrittura, lo ZIP viene riletto e verificato.
- Lo script rifiuta di creare il pacchetto se `VERSION` e il manifest non coincidono.

`python tools/release.py all` crea il pacchetto di ogni add-in del repository.

Ordine consigliato per un rilascio:

1. Eseguire i test.
2. Impostare la versione con `tools/set_version.py`.
3. Aggiungere la voce a `docs/dovetail/CHANGELOG.md`.
4. Aggiornare questa documentazione.
5. Creare il pacchetto con `tools/release.py`.
6. Allegare `dist/Dovetail-<version>.zip` al rilascio su GitHub.

## Aggiungere una lingua

1. Copiare `lang/en.xml` e dare alla copia il nome del codice di lingua di due lettere.
2. Impostare `language="<code>"` nell'elemento radice e tradurre i valori.
3. Conservare ogni segnaposto (`{0}`, `{1}`, …).
4. Aggiungere il codice a `SUPPORTED_LANGUAGES` e il nome di lingua di Fusion corrispondente a `FUSION_LANGUAGE_MAP` in
   `Dovetail.py`.
5. Eseguire i test. Controllano in ogni file completezza, chiavi sconosciute, segnaposto e testi vuoti.

`en.xml` è il file di riferimento. Ogni chiave esiste lì. Una chiave che manca altrove ripiega su di esso; una chiave che manca
dappertutto viene mostrata come la chiave stessa.

## Decisioni e loro motivi

Presi dai commenti nel codice.

| Decisione | Motivo |
|---|---|
| I testi stanno in `lang/<code>.xml`; gli errori portano una chiave, non un testo | Il motivo di un errore resta indipendente dalla lingua; i test possono confrontare le chiavi |
| Forma e ripartizione sono salvate come indice nell'elenco | Il valore salvato non dipende dalla lingua di visualizzazione |
| I valori di lingua di Fusion vengono cercati con `getattr` | Un valore che questa versione di Fusion non conosce non può mandare in errore l'add-in |
| La versione viene letta dal manifest | La finestra di dialogo non può scostarsi dal manifest |
| La versione fa parte del nome del comando | Fusion usa il nome del comando come titolo della finestra di dialogo, quindi è qui che una versione è visibile mentre la finestra di dialogo è aperta |
| Lo spostamento non viene ricordato | Appartiene alla linea del momento, non alle impostazioni |
| La linea originale diventa geometria di costruzione invece di essere eliminata | Smette di creare profili ma conserva quote e vincoli |
| L'anteprima non tocca la linea originale | La selezione non può essere invalidata sotto la finestra di dialogo aperta |
| Tutte le linee vengono controllate prima di disegnarne una | Una linea non valida in fondo non può lasciare lo schizzo disegnato a metà |
| Un errore su una di più linee viene racchiuso insieme alla sua posizione | Una linea corta in mezzo fallisce mentre le altre andrebbero bene; il messaggio dice quale |
| I pulsanti **Sposta** usano la linea più corta come limite | Uno spostamento che esce da una linea non va bene anche se le altre lo potrebbero accogliere |
| Con il rispecchiamento, numero, ripartizione e spostamento vengono impostati e messi in grigio | Ognuno di essi rompe la simmetria a 180 gradi; fissarli è meglio che lasciarli fallire alla convalida |
| Il rispecchiamento richiede un numero pari | Un dente centrale dovrebbe puntare in entrambe le direzioni insieme |
| Il passo minimo ha 0.01 mm in più | Esattamente al minimo il tratto tra due cave non ha più lunghezza |
| I denti restano a tolleranza + 0.01 mm dagli estremi della linea | La cava si apre di una quantità pari alla tolleranza; altrimenti il profilo va oltre l'estremo e deve tornare indietro |
| Un profilo viene controllato per tratti di lunghezza zero e per incroci con se stesso | Lo spostamento tratta a quartabuono ogni spigolo per conto suo, quindi nient'altro impedisce a un tratto corto di ridursi a nulla o di ribaltarsi |
| Uno spigolo a quartabuono più lontano di 12 × lo spostamento viene rifiutato | Il profilo di accoppiamento sbanderebbe in uno spigolo acuto |
| Un'esecuzione fallita imposta `executeFailed` | Fusion annulla allora ciò che è stato disegnato fino a quel momento |
| Il disegno gira con `isComputeDeferred` | Lo schizzo ricalcola una volta sola, non dopo ogni linea |
| `set_version.py` scrive insieme VERSION e manifest | Il numero non viene mai modificato a mano in due posti |
| Lo ZIP usa Deflate al livello più alto | Ogni programma di estrazione può leggerlo |

## Punti aperti noti

- Quando OK è in grigio, la finestra di dialogo non mostra alcun motivo. I testi esistono (`err.*`) ma li mostra solo la
  finestra di messaggio dopo un'esecuzione fallita.
- Le linee di schizzo vengono lette solo con X e Y e la fascia viene disegnata a Z = 0 dello schizzo.
- Le modifiche alla geometria della 1.1.0.0 sono verificate solo offline, non all'interno di Fusion.

## Licenza

MIT, vedere [LICENSE](../LICENSE). Autore: Sorglos Thomas Weirich.
