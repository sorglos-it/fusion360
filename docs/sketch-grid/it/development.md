# Sviluppo

SketchGrid è uno dei vari add-in del repository <https://github.com/sorglos-it/fusion360>. Tutti i percorsi qui sotto partono dalla radice del repository.

## Cartelle

| Percorso | Contenuto |
| --- | --- |
| `apps/desktop-sketch-grid/SketchGrid/` | L'add-in esattamente come serve a Fusion: `SketchGrid.py`, `sketchgrid_core.py`, `SketchGrid.manifest`, `lang/`, `resources/SketchGrid/` |
| `apps/desktop-sketch-grid/VERSION` | Il numero di versione, una riga |
| `apps/desktop-sketch-grid/tests/test_sketchgrid.py` | I test |
| `tools/sketch-grid/make_icon.py` | Disegna l'icona del pulsante (16, 32 e 64 pixel) |
| `tools/sketch-grid/test_sketchgrid.py` | Rimanda soltanto ai test qui sopra, così il vecchio comando continua a funzionare |
| `tools/set_version.py` | Imposta il numero di versione (condiviso da tutti gli add-in) |
| `tools/release.py` | Crea lo ZIP di rilascio (condiviso da tutti gli add-in) |
| `docs/sketch-grid/` | README, CHANGELOG, LICENSE e questa documentazione |
| `dist/` | Creata da `tools/release.py`; non è in Git |

La cartella, il file `.py` e il file `.manifest` devono avere in comune il nome `SketchGrid`. Lo richiede Fusion.

Tutti gli script richiedono solo un normale Python 3 con la sua libreria standard. Non c'è nulla da compilare; l'add-in gira così com'è.

## Eseguire i test

```
python apps/desktop-sketch-grid/tests/test_sketchgrid.py
python apps/desktop-template/tests/test_addin.py --path apps/desktop-sketch-grid/SketchGrid
```

Il primo comando gira senza Fusion. Il file di test mette al loro posto dei sostituti vuoti dei moduli `adsk` di Fusion e poi importa `SketchGrid.py`. Stampa una riga per controllo (`ok` oppure `FAIL`) e termina con `all tests passed` e codice di uscita 0, oppure con il numero di errori e codice di uscita 1.

Cosa controlla:

| Sezione | Argomento |
| --- | --- |
| 1 | L'esempio standard: 10 × 5 mm, distanza 2 mm, 8 colonne, 4 righe danno 94 × 26 mm e 32 celle |
| 2, 2b | Ogni voce del punto di riferimento ha i fattori che il suo nome promette (ricavati dal nome della chiave, per esempio `bottom_left`), e il punto finisce dove dice la voce |
| 3 | Posizioni delle celle |
| 4 | La modalità "Riempimento di un'area" conta solo ciò che entra per intero |
| 5 | Ogni rifiuto riporta la chiave di messaggio giusta |
| 6 | File di lingua: tutti e cinque sono completi e conservano i loro segnaposto |
| 7 | Scostamento dal punto selezionato |
| 8 | La distanza resta la distanza per ogni forma: riquadro del poligono misurato, allungamento, dimensione reale nella modalità di riempimento |
| 9 | Spigoli del rettangolo: limiti e contorno di linee e archi |
| 10 | Ogni voce degli elenchi a discesa ha un testo |
| 11 | Catalogo dei testi: caricamento di ogni lingua, ripiego sull'inglese, i messaggi seguono la lingua |

Il secondo comando è il controllo di struttura dell'add-in modello dello stesso repository. Controlla manifest, id, id del comando e icone.

Per impostazione predefinita i test e lo script dell'icona usano `apps/desktop-sketch-grid/SketchGrid`. Impostare la variabile d'ambiente `SKETCHGRID_ADDIN_DIR` per provare un'altra copia, per esempio una installata.

Cosa i test non coprono: tutto ciò che richiede Fusion. Cioè la finestra di dialogo, la selezione, l'anteprima e le chiamate di disegno vere e proprie. Queste parti si possono provare solo all'interno di Fusion.

## Provare una modifica in Fusion

1. Copiare `apps/desktop-sketch-grid/SketchGrid` nella cartella degli add-in di Fusion (vedere [installation.md](installation.md)).
2. In Fusion, arrestare l'add-in ed eseguirlo di nuovo.

`SketchGrid.py` toglie `sketchgrid_core` dalla cache dei moduli di Python prima di importarlo. Motivo dal commento nel codice: Fusion tiene in cache i moduli importati, quindi un modulo di supporto modificato continuerebbe a fornire la sua vecchia versione fino al riavvio di Fusion.

## Numeri di versione

Quattro parti: `v.x.y.z` (versione, rilascio, funzione, build), per esempio `1.1.0.0`.

Il numero è tenuto in due posti:

- `apps/desktop-sketch-grid/VERSION`
- la voce `"version"` in `SketchGrid.manifest` (Fusion e il nome del pulsante leggono questa)

Non modificarli mai a mano. Usare lo script, che li scrive entrambi:

```
python tools/set_version.py sketch-grid 1.1.0.1
python tools/set_version.py --check
```

- Il primo comando imposta la versione. Rifiuta tutto ciò che non è fatto di quattro numeri separati da punti.
- `--check` elenca ogni add-in con entrambi i numeri e dice `ok` oppure `DIFFERENT OR NOT v.x.y.z`. Codice di uscita 1 se un add-in non è a posto.
- `all` al posto di `sketch-grid` imposta lo stesso numero per ogni add-in del repository.

Aggiungere una voce a `docs/sketch-grid/CHANGELOG.md` per ogni nuovo numero.

## Creare il pacchetto di rilascio

```
python tools/release.py sketch-grid
```

- Scrive `dist/SketchGrid-<version>.zip`.
- Lo ZIP contiene la cartella `SketchGrid` come livello più alto, pronta per essere estratta nella cartella degli add-in di Fusion.
- Esclusi: le cartelle `__pycache__` e i file che finiscono in `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compressione: Deflate al livello più alto, "così ogni programma di estrazione può leggerlo" (commento nello script).
- Lo script rifiuta di creare il pacchetto quando `VERSION` e il manifest differiscono o il numero non ha quattro parti.
- Dopo la scrittura rilegge lo ZIP e si ferma se un file al suo interno è danneggiato.
- `all` al posto di `sketch-grid` crea il pacchetto di ogni add-in.

Lo ZIP viene poi allegato a un rilascio su <https://github.com/sorglos-it/fusion360/releases>. Lo script non carica nulla.

## Ridisegnare l'icona

```
python tools/sketch-grid/make_icon.py
```

Scrive `16x16.png`, `32x32.png` e `64x64.png` in `resources/SketchGrid/`. L'immagine è una griglia di 3 × 3 celle con una croce al centro per il punto selezionato. Lo script scrive da solo i file PNG, senza una libreria di immagini.

## Aggiungere una lingua

1. Copiare `lang/en.xml` in `lang/<code>.xml` (codice di due lettere) e tradurre i testi. Conservare le chiavi e i segnaposto `{0}`, `{1}`.
2. In `sketchgrid_core.py`, aggiungere il codice a `SUPPORTED_LANGUAGES` e il nome di lingua di Fusion corrispondente a `FUSION_LANGUAGE_MAP`.
3. Eseguire i test. Controllano ogni lingua presente in `SUPPORTED_LANGUAGES`.

## Decisioni e loro motivi

Presi dai commenti nel codice.

| Decisione | Motivo indicato |
| --- | --- |
| Il calcolo della griglia (`grid_layout`, `cell_centres`, `corner_outline`) non usa chiamate a Fusion. | È la parte che vale la pena di testare, e così i test possono girare senza avviare Fusion. |
| Le scelte degli elenchi a discesa sono salvate come posizione nell'elenco, non come testo. | Il valore salvato non si sposta quando cambia la lingua dell'interfaccia. |
| Al massimo 2000 forme (`MAX_SHAPES`). | Un numero fuori controllo nella modalità di riempimento blocca Fusion per minuti. Meglio rifiutare. |
| Un raggio / smusso sopra la metà del lato più corto viene rifiutato, non ridotto. | Esattamente alla metà i due tagli su un lato si incontrano; oltre, si scavalcherebbero. Viene assorbito solo il rumore di arrotondamento. |
| Gli spigoli non partecipano alla disposizione. | L'ingombro è ancora lunghezza × profondità, quindi passo, numero e distanza restano com'erano. |
| Un poligono regolare comunica la propria dimensione misurata e il passo la segue. | Non può riempire una cella di altre proporzioni; altrimenti la distanza richiesta non è la distanza ottenuta. |
| Il riquadro del poligono viene misurato, non presunto. | Un poligono ha un vertice su ogni estremo solo per numeri di lati adatti; un pentagono sta in basso nel proprio riquadro. |
| Un quadrato completamente raccordato viene disegnato come cerchio. | Un cerchio non è una catena di segmenti. |
| Per un'ellisse, il punto dell'asse principale viene messo sull'asse più lungo. | Altrimenti Fusion rifiuta l'ellisse. |
| `isComputeDeferred` viene impostato durante il disegno e ripristinato in un blocco `finally`. | Tiene fermo il risolutore finché ogni forma non è disegnata; con qualche centinaio di celle è la differenza tra immediato e inutilizzabile. |
| Il gestore dell'anteprima inghiotte ogni errore. | Scatta a ogni pressione di tasto, anche con valori scritti a metà. Segnalare è compito della convalida dei dati inseriti. |
| I gestori degli eventi vengono registrati prima di riprendere il punto preselezionato, e la ripresa può fallire in silenzio. | Qualunque cosa fallisca dopo, la finestra di dialogo deve funzionare lo stesso; l'utente seleziona allora il punto nella finestra di dialogo. |
| Tutti i gestori degli eventi sono tenuti in un registro (`HandlerRegistry`). | Fusion tiene solo un riferimento debole a un gestore. Senza un riferimento dal lato Python, l'evento smette di scattare in silenzio. |
| Vengono provati in ordine più id di pannello. | Gli id dei pannelli cambiano da una versione di Fusion all'altra. |
| I valori di lingua di Fusion vengono cercati per nome con un ripiego. | Un valore che questa versione di Fusion non conosce non può mandare in errore l'add-in; ripiega sull'inglese invece di fallire. |
| Una chiave che manca in una traduzione viene fornita dall'inglese. | Una traduzione finita a metà degrada verso l'inglese invece di mostrare chiavi nude. |
| I problemi previsti vengono sollevati come `AddInError` con una chiave di messaggio. | La chiave è indipendente dalla lingua; ciò che l'utente può correggere deve bloccare OK invece di aprire una finestra. |
| La versione viene letta dal manifest, non scritta nel codice. | La finestra di dialogo non può scostarsi dal manifest, e c'è un solo posto da cambiare. |
| La versione fa parte del nome del comando. | Fusion usa il nome del comando come titolo della finestra di dialogo, quindi è qui che la versione è visibile; c'è solo quell'unico nome. |
| Gli ultimi valori sono tenuti in memoria in centimetri. | I centimetri sono l'unità interna di Fusion, indipendentemente dall'unità di visualizzazione. |

## Punti aperti

- La versione 1.1.0.0 (il punto preselezionato non può essere ripreso) è verificata solo offline, non all'interno di Fusion.
- Le asole e i rettangoli raccordati o smussati vengono disegnati come curve separate a partire dalle coordinate, senza punti finali condivisi. Se restino collegati quando vengono trascinati va verificato all'interno di Fusion.
- Il limite di 2000 conta le forme, non le curve. Se debba contare le curve va verificato all'interno di Fusion.

## Licenza

MIT, vedere [LICENSE](../LICENSE). Autore: Sorglos Thomas Weirich.
