# Sviluppo

Torna alla [panoramica](index.md).

Tutti i comandi vengono eseguiti dalla radice del repository <https://github.com/sorglos-it/fusion360>.

## Cartelle

| Percorso | Contenuto |
| --- | --- |
| `apps/desktop-system3e/System3E/` | L'add-in così come Fusion lo carica (questa cartella va nello ZIP di rilascio) |
| `apps/desktop-system3e/System3E/System3E.py` | Comando, finestra di dialogo, posizionamento, punti |
| `apps/desktop-system3e/System3E/system3e_core.py` | Meccanismi condivisi: catalogo dei testi, rilevamento della lingua, ricerca del pannello, registro degli handler, tipo di errore, versione |
| `apps/desktop-system3e/System3E/System3E.manifest` | Manifest di Fusion: id, autore, descrizioni, versione, `runOnStartup`, `supportedOS` |
| `apps/desktop-system3e/System3E/lang/` | `de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml`; `en.xml` è il riferimento |
| `apps/desktop-system3e/System3E/blocks/` | `blocks.json` e 74 immagini di anteprima `<id>.png` (generati) |
| `apps/desktop-system3e/System3E/resources/System3E/` | Icona del pulsante a 16, 32 e 64 px |
| `apps/desktop-system3e/VERSION` | Il numero di versione, una riga |
| `apps/desktop-system3e/tests/` | `test_addin.py`, `test_blocks.py` |
| `tools/system3e/` | `build_library.py`, `mesh_to_solid.py`, `points_sheet.py`, `make_icon.py` |
| `tools/set_version.py`, `tools/release.py` | Strumenti di versione e di rilascio per tutti gli add-in del repository |
| `docs/system3e/` | README, registro delle modifiche, licenza, il disegno dei punti, questa documentazione |
| `assets/system3e/` | Il file 3D del produttore. **Non è nel repository**, viene tenuto in locale. |
| `dist/` | ZIP di rilascio. Non in Git. |

`System3E.py` ha due zone contrassegnate. Il codice specifico dell'add-in sta tra `CONFIGURE` e `END OF TEMPLATE`; gli
handler di eventi e `run`/`stop` più sotto sono l'impalcatura. L'add-in è stato generato dal modello di add-in
del repository.

## Test

Entrambi i test funzionano senza Fusion. Mettono dei sostituti dei moduli `adsk` in `sys.modules` e importano l'add-in.
Solo libreria standard.

```bash
python apps/desktop-system3e/tests/test_addin.py
```

```bash
python apps/desktop-system3e/tests/test_blocks.py
```

Il codice di uscita 1 significa che almeno un controllo non è riuscito.

`test_addin.py` controlla:

| Sezione | Controlli |
| --- | --- |
| 1) Struttura | La cartella, `System3E.py`, `System3E.manifest` e `lang/` esistono e corrispondono al nome della cartella |
| 2) Manifest | JSON valido, `type` è `addin`, `autodeskProduct` è `Fusion360`, l'id ha l'aspetto di un GUID |
| 3) Importazione | L'add-in si importa, `run` e `stop` esistono, `CMD_ID` è impostato, il file del modulo core esiste |
| 4) File di lingua | Ogni file di lingua esiste, dichiara la propria lingua, ha ogni chiave di `en.xml` e nessuna chiave sconosciuta, mantiene ogni segnaposto `{0}`, non ha testi vuoti |
| 5) Catalogo dei testi | Ogni lingua si carica, una lingua sconosciuta ricade sull'inglese, una chiave mancante restituisce la chiave |
| 6) Icone | I tre file icona esistono e sono veri file PNG |

Opzioni: `--addin <name>` e `--path <folder>` indirizzano il test su un'altra cartella di add-in.

`test_blocks.py` controlla:

| Sezione | Controlli |
| --- | --- |
| 1) File della libreria | L'unità è `mm`, 74 elementi, id e nomi univoci, id utilizzabili come nomi di file |
| 2) Solidi | Ogni elemento è un solido chiuso con facce piane, i contorni girano nel verso giusto, il volume è possibile, l'angolo è nell'origine, dimensioni e punti concordano, le dimensioni corrispondono al nome di catalogo, non ci sono due elementi con la stessa forma |
| 3) Immagini | Ogni elemento ha un PNG, nessuna immagine avanzata |
| 4) Add-in | L'add-in legge ogni elemento; ogni famiglia, ancoraggio e nome di punto ha un testo in tutte e cinque le lingue; l'elemento predefinito e l'ancoraggio predefinito esistono |
| 5) Punti da cliccare | L'altezza di impilamento di `S1 WP` è 250 e quella di `EU 200 W` è 200; posizioni degli ancoraggi; dodici punti con nome per elemento, tutti in posti diversi e sull'elemento; `make_body()` trasforma ogni punto in un vertice, definisce ogni faccia, usa ogni spigolo una volta in ciascuna direzione e converte i mm in cm |

Che cosa i test non possono dire: se Fusion accetta un corpo, crea i punti di costruzione o posiziona
correttamente l'occorrenza. Questo si sa solo dentro Fusion.

Stato dei test dentro Fusion: il posizionamento degli elementi è stato usato dall'autore. I dodici punti, **Posiziona da** e
gli spostamenti X/Y/Z sono stati testati solo offline. Le correzioni della 1.0.0.1 non sono ancora confermate dentro Fusion.

## Rigenerare la libreria degli elementi

`blocks/blocks.json` e le immagini sono generati. Non modificarli a mano.

Origine: il file 3D del produttore `assets/system3e/SYSTEM 3E START.3ds`. **Non fa parte del repository**.
Senza di esso la libreria non può essere rigenerata; lo script si ferma con "Source file missing".

```bash
python tools/system3e/build_library.py
```

```bash
python tools/system3e/build_library.py --no-pictures
```

Le immagini richiedono il pacchetto Python Pillow. `--no-pictures` le salta. L'add-in stesso non ha bisogno di nessuno dei due.

Che cosa fa la generazione:

1. `mesh_to_solid.read_3ds()` legge ogni mesh di triangoli del file e la converte in mm.
2. `mesh_to_solid.solid_from_mesh()` unisce i punti più vicini di 0,3 mm, ordina i triangoli in piani, riunisce
   tutti i triangoli di un piano in contorni (con fori), elimina i punti a metà di spigoli rettilinei e
   controlla che ogni spigolo sia usato una volta in ciascuna direzione. L'angolo più basso del riquadro di ingombro diventa l'origine.
3. La tabella `NAMES` dà a ogni numero di mesh il suo nome di catalogo. Il file 3D non contiene nomi.
4. I quattro elementi per parete divisoria vengono aggiunti come semplici parallelepipedi con le dimensioni della tabella `PARTITION`.
5. `S0/2 200 P` viene ricostruito (vedere sotto).
6. `straighten()` dà ai punti che devono condividere una coordinata esattamente lo stesso valore, a 0,1 mm.
7. `bend()` ricalcola la normale di ogni faccia dal suo contorno. `stack_level()` trova l'altezza di impilamento.
8. `blocks.json` viene scritto nell'ordine della tabella `FAMILIES`, e viene disegnata un'immagine per elemento.

La generazione si ferma se un elemento non è un solido chiuso, se due elementi condividono un id o se il controllo della ricostruzione non riesce.

Per esaminare solo il file di origine:

```bash
python tools/system3e/mesh_to_solid.py "assets/system3e/SYSTEM 3E START.3ds" --report
```

Stampa una riga per mesh con dimensioni, numero di punti e di facce, volume e stato.

### Altri strumenti

| Strumento | Scopo |
| --- | --- |
| `python tools/system3e/points_sheet.py "S1 WP" docs/system3e/s1-wp-punkte.svg` | Disegna un elemento con ogni punto come SVG. I punti sono presi dall'add-in stesso. Le scritte sono in tedesco. |
| `python tools/system3e/make_icon.py` | Genera i PNG dell'icona del pulsante a 16, 32 e 64 px |

## Numeri di versione

Una versione ha quattro parti, `v.x.y.z`: versione, rilascio, funzione, build. Esempio: `1.1.0.0`.

Il numero è tenuto in due posti: `apps/desktop-system3e/VERSION` e la voce `version` del manifest. Fusion
e il titolo della finestra di dialogo leggono il manifest. Non modificare mai i due a mano; usare lo strumento:

```bash
python tools/set_version.py system3e 1.1.0.1
```

```bash
python tools/set_version.py --check
```

`--check` elenca ogni add-in del repository e segnala quelli i cui due numeri differiscono o non sono `v.x.y.z`.
`all` al posto di `system3e` imposta ogni add-in.

Annotare ogni versione in `docs/system3e/CHANGELOG.md`.

## Creare il pacchetto di rilascio

```bash
python tools/release.py system3e
```

- Scrive `dist/System3E-<version>.zip`.
- Lo ZIP contiene la cartella `System3E` esattamente come la vuole Fusion.
- `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db` e `.DS_Store` vengono esclusi.
- La compressione è Deflate al livello più alto, così ogni programma di estrazione può leggerlo.
- Dopo la scrittura lo ZIP viene riletto e testato.
- Lo strumento rifiuta di creare il pacchetto quando `VERSION` e il manifest non concordano.

Lo ZIP viene poi allegato a un rilascio su <https://github.com/sorglos-it/fusion360/releases>. Questo caricamento non
fa parte dello strumento.

Prima di un rilascio: eseguire entrambi i test, eseguire `set_version.py --check`, aggiornare il registro delle modifiche e questa documentazione.

## Aggiungere o modificare testi

- `lang/en.xml` è il riferimento. Ogni altro file di lingua deve avere le stesse chiavi e gli stessi segnaposto.
- Una chiave mancante in una lingua viene servita dall'inglese durante l'esecuzione, ma `test_addin.py` la segnala come errore.
- I nomi dei campi della finestra di dialogo, delle famiglie (`family.<id>`), degli ancoraggi (`anchor.<id>`) e dei punti (`point.<...>`) vengono tutti
  da questi file.
- Per supportare un'altra lingua, aggiungerla a `SUPPORTED_LANGUAGES` e `FUSION_LANGUAGE_MAP` in
  `system3e_core.py` e aggiungere il file di lingua.

## Decisioni e loro motivi

Sono prese dai commenti nel codice.

| Decisione | Motivo |
| --- | --- |
| Il modulo core viene rimosso da `sys.modules` prima dell'importazione. | Fusion tiene in cache i moduli importati. Senza questo, una funzione di supporto modificata manterrebbe la vecchia versione fino al riavvio di Fusion. |
| Il modulo core ha un nome proprio, `system3e_core`. | Due add-in costruiti dallo stesso modello altrimenti si sovrascriverebbero a vicenda il modulo core. |
| L'id del comando ha un prefisso proprio (`thwSystem3ECmd`). | Un id usato due volte si impossessa in silenzio del pulsante dell'altro add-in. |
| Una definizione di comando obsoleta viene eliminata all'avvio. | Una definizione lasciata da un'esecuzione precedente manterrebbe la vecchia etichetta e il vecchio handler. |
| Il pannello viene cercato a partire da un elenco di id. | Gli id dei pannelli cambiano tra le versioni di Fusion. |
| Tutti gli handler di eventi sono tenuti in un registro. | Fusion mantiene solo un riferimento debole. Un handler non conservato dal lato Python viene eliminato e il suo evento smette in silenzio di scattare. |
| Gli handler vengono collegati prima che il punto preselezionato venga ripreso. | Qualunque cosa fallisca dopo, la finestra di dialogo deve comunque funzionare. |
| La selezione fatta prima di premere il pulsante viene letta prima che esistano i campi di input. | Così cliccare un punto e poi il pulsante funziona e basta. |
| Tutti i valori della finestra di dialogo vengono letti in un'unica funzione. | Esecuzione, anteprima e validazione guardano allora esattamente gli stessi valori. |
| L'anteprima tace in caso di errori. | Scatta a ogni tasto premuto, anche per valori digitati a metà. La validazione disattiva invece **OK**. |
| L'anteprima imposta `isValidResult` su false. | Fusion esegue allora di nuovo la vera esecuzione per il risultato finale. |
| Gli errori previsti sono un tipo di errore proprio con una chiave indipendente dalla lingua. | La validazione può decidere senza analizzare testo. Gli errori imprevisti vengono mostrati con il loro traceback. |
| Un'esecuzione non riuscita imposta `executeFailed`. | Fusion annulla allora ciò che era stato costruito fino a quel momento, invece di lasciare un componente vuoto. |
| Lo stesso elemento di nuovo è un'altra occorrenza dello stesso componente. | Altrimenti una distinta dei pezzi mostra "S1 WP", "S1 WP (1)", "S1 WP (2)" come tre pezzi invece di un pezzo tre volte. |
| I componenti vengono trovati tramite un attributo, non tramite il nome. | Rinominare un componente allora non fa danni. Gli elementi di prima che esistesse l'attributo vengono trovati tramite il nome. |
| I componenti di un progetto collegato vengono saltati. | Non possono essere modificati dal progetto corrente. |
| Nei progetti parametrici corpo e punti vanno in una base feature. | Con la timeline attiva, un corpo già pronto e un punto a coordinate semplici devono stare in una base feature. |
| Il corpo riceve il nome mentre la sua base feature è ancora aperta. | Indicato nel codice; la versione 1.0.0.1 ha spostato lì l'assegnazione del nome. |
| A un componente esistente vengono aggiunti solo i punti mancanti. | I componenti creati da una versione precedente non ne hanno o ne hanno meno. |
| Lo spostamento viene applicato dopo la rotazione. | Corre lungo X, Y e Z del progetto, non lungo l'elemento ruotato. |
| I campi di spostamento mostrano mm, il valore è in cm. | Il cm è l'unità propria di Fusion. |
| La versione viene letta dal manifest, non scritta fissa nel codice. | La finestra di dialogo non può discostarsi dal manifest, e c'è un solo posto in cui aumentarla. |
| La versione fa parte del nome del comando. | Fusion usa il nome del comando come titolo della finestra di dialogo; è l'unico posto in cui una versione è visibile mentre la finestra di dialogo è aperta. |
| I membri dell'enumerazione delle lingue vengono cercati con `getattr`. | Un valore che questa versione di Fusion non conosce non può rompere l'add-in. L'inglese è la lingua di ripiego. |
| La libreria salva punti e facce piane, non file di Fusion. | Il file del produttore contiene mesh di triangoli slegate (triangoli che si toccano lungo una parte di uno spigolo, punti doppi, schegge). Fusion non può ricavarne un corpo. |
| `S0/2 200 P` è ricostruito da `S0/2 250 P`, abbassato di 50 mm. | La sua mesh è danneggiata in modo irreparabile (aperta su un lato). Gli elementi di partenza differiscono solo nell'altezza del corpo semplice sotto il profilo superiore. `check_lowering()` dimostra il metodo su una coppia in cui entrambe le mesh sono integre (`S0/2 250 W` e `S0/2 200 W`). |
| I numeri di mesh sono abbinati ai nomi da una tabella fatta a mano. | Il file 3D non contiene nomi. La tabella è stata fatta confrontando ogni solido con il disegno sulla sua scheda di catalogo. La lunghezza distingue le estremità: 704 o 352 mm è "W", 3 mm in più è un maschio ("P"). |
| Gli elementi per parete divisoria sono semplici parallelepipedi. | Non sono nel file 3D; le loro dimensioni vengono dalle schede di catalogo. |
| Le coordinate sono raddrizzate a 0,1 mm. | L'origine ha rumore da virgola mobile (106,4 accanto a 106,5 mm), che lascia le facce leggermente piegate. |
| L'altezza di impilamento è 50 mm sotto la cima negli elementi profilati. | Portano il corso successivo sul fondo tra le nervature; gli elementi piatti lo portano in cima. |
| Le immagini di anteprima sono disegnate con un buffer di profondità. | Le superfici nascoste vengono rimosse pixel per pixel. Un metodo precedente mostrava le facce nell'ordine sbagliato in 16 immagini. |
| Le immagini di anteprima sono disegnate dai solidi. | Non sono prese dal catalogo del produttore. |

## Punti aperti

- I nomi sinistra/destra degli elementi d'angolo e per finestra nella tabella `NAMES` sono stati abbinati a occhio alle
  schede di catalogo. Devono ancora essere controllati da qualcuno che conosce il sistema.
- I punti, **Posiziona da** e gli spostamenti hanno bisogno di un test dentro Fusion.

## Licenza

MIT, Copyright (c) 2026 Sorglos Thomas Weirich. Vedere [LICENSE](../LICENSE). L'add-in non è affiliato a
SYSTEM 3E.
