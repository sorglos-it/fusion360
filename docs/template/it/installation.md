# Installazione

## Requisiti

| Che cosa | Serve per |
| --- | --- |
| Autodesk Fusion 360 su Windows o macOS | eseguire l'add-in |
| Python 3 sul proprio computer | gli strumenti in `tools/` (generazione, controllo offline, icone, versione, creazione del pacchetto) |

L'add-in stesso non ha bisogno di nient'altro. Usa solo il Python incluso in Fusion.
Gli strumenti usano solo la libreria standard di Python. Non occorre installare nulla con `pip`.

## Ottenere il repository

Non esiste uno ZIP di rilascio per la versione 1.0.0.0. Usare il repository.

1. Aprire <https://github.com/sorglos-it/fusion360>.
2. Clonarlo, oppure scaricarlo come ZIP ed estrarlo.
3. Aprire un terminale nella cartella del repository.

## Creare un nuovo add-in

```bash
python tools/template/new_addin.py MyAddIn --install
```

Questo crea l'add-in `MyAddIn` direttamente nella cartella degli add-in di Fusion.

### Regole per il nome

- Deve iniziare con una lettera.
- Può contenere solo lettere e cifre. Niente spazi, niente trattini, niente trattini bassi.
- Non deve essere `AddInTemplate`.

Il nome diventa il nome di un modulo Python. Per questo le regole sono rigide.

### Tutte le opzioni

| Opzione | Valore predefinito | Effetto |
| --- | --- | --- |
| `name` (obbligatorio) | – | Nome dell'add-in, per esempio `MyAddIn` |
| `--install` | disattivata | Lo crea direttamente nella cartella degli add-in di Fusion |
| `--out DIR` | la cartella che contiene il repository | Lo crea invece in `DIR`. `DIR` viene creata se non esiste |
| `--author NAME` | `Your Name` | Viene scritto nel campo `author` del manifest |
| `--prefix STR` | `thw` | Prefisso dell'id del comando. L'id diventa `<prefix><name>Cmd` |
| `--force` | disattivata | Sovrascrive una cartella esistente con quel nome |
| `-h`, `--help` | – | Mostra il testo di aiuto |

Note:

- `--install` e `--out` non si possono usare insieme.
- Senza `--install` e senza `--out` l'add-in viene creato **accanto** alla cartella del repository, non al suo interno.
- `--force` **elimina prima l'intera cartella esistente**, comprese le proprie modifiche al suo interno. Poi crea una copia nuova.
- Scegliere un proprio `--prefix`. `thw` è il prefisso dell'autore del modello.

### Che cosa fa lo script

1. Copia `apps/desktop-template/AddInTemplate` in `<target>/<name>` (senza `__pycache__` e senza file `.pyc`).
2. Rinomina `AddInTemplate.py` in `<name>.py` e `AddInTemplate.manifest` in `<name>.manifest`.
3. Rinomina `addin_core.py` in `<name in lower case>_core.py`, per esempio `myaddin_core.py`.
4. Rinomina la cartella delle icone `resources/AddInTemplate` in `resources/<name>`.
5. Nel file di ingresso: imposta `_CORE_MODULE` e `CMD_ID`, e sostituisce ogni `AddInTemplate` con il nuovo nome.
6. Nel manifest: scrive un nuovo GUID casuale in `id` e il nome dell'autore in `author`.
7. In ogni `lang/*.xml`: imposta `cmd.name` sul nuovo nome e `cmd.tooltip` sul nome più la riga `TODO: describe what this command does.`

Lo script **non** modifica `description` e `version` nel manifest. Modificarli da sé, vedere [settings.md](settings.md).

### Che cosa si ottiene

```
MyAddIn/
  MyAddIn.py            entry file - your code goes here
  myaddin_core.py       core module, renamed for this add-in
  MyAddIn.manifest      what Fusion reads, with a new GUID
  lang/
    en.xml              reference: every key exists here
    de.xml es.xml fr.xml it.xml
  resources/
    MyAddIn/            16x16.png 32x32.png 64x64.png
```

Alla fine lo script stampa il percorso creato, il file di ingresso, il modulo core, l'id del comando e i passi successivi.

## La cartella degli add-in di Fusion

| Sistema | Percorso |
| --- | --- |
| Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
| macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

Se l'add-in è stato creato senza `--install`, copiare l'intera cartella `MyAddIn` in questa cartella.

Cartella, file di ingresso e manifest devono portare lo stesso nome: `MyAddIn/MyAddIn.py` e `MyAddIn/MyAddIn.manifest`.

## Primo avvio in Fusion

1. Avviare Fusion 360.
2. Aprire **Utilities → ADD-INS → Add-Ins** (è il percorso che lo script stampa).
3. Selezionare il proprio add-in e premere **Run**.
4. Aprire uno schizzo. Il pulsante si trova nella scheda **SKETCH**, nel pannello di creazione. Se quel pannello non esiste, va nel pannello di creazione della scheda **SOLID**.

Nel manifest `runOnStartup` è impostato su `true`.

Il pulsante e il titolo della finestra di dialogo mostrano il nome del comando con la versione tra parentesi, per esempio `Modello di add-in (1.0.0.0)`.

Questi passi seguono il codice e l'output dello script. Per questa documentazione non sono stati testati in Fusion.

### Provare il modello stesso

Si può anche eseguire il modello non modificato: copiare la cartella `apps/desktop-template/AddInTemplate` nella cartella degli add-in di Fusion e avviarlo come sopra. Il suo comando si chiama `Modello di add-in`.

## Aggiornamento

Non c'è una funzione di aggiornamento.

- Un add-in creato dal modello contiene la propria copia di tutti i file. Le modifiche fatte in seguito nel modello non lo raggiungono.
- Per riprendere una correzione, copiare la modifica a mano nel proprio `<name>_core.py` o nel proprio file di ingresso.
- Eseguire di nuovo lo script con `--force` non è un aggiornamento. Elimina la cartella del proprio add-in e crea una copia nuova e vuota.

## Rimozione

1. In Fusion aprire **Utilities → ADD-INS → Add-Ins**, selezionare l'add-in e arrestarlo. All'arresto l'add-in rimuove il suo pulsante e il suo comando dalla barra degli strumenti.
2. Chiudere Fusion.
3. Eliminare la cartella dell'add-in dalla cartella degli add-in di Fusion.

L'add-in non salva nulla fuori dalla propria cartella. I valori ricordati esistono solo in memoria finché Fusion non si chiude.
