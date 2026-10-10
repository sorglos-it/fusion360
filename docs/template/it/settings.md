# Impostazioni

L'add-in non ha una finestra di impostazioni né un file di impostazioni. Tutto si imposta in tre posti:

1. il file di ingresso `<name>.py`, blocco `CONFIGURE`
2. il manifest `<name>.manifest`
3. i file di lingua in `lang/`

## File di ingresso

| Nome | Valore nel modello | Significato | Valori ammessi |
| --- | --- | --- | --- |
| `CMD_ID` | `thwAddInTemplateCmd` | Id del comando | Qualsiasi testo. Deve essere univoco tra **tutti** gli add-in installati in Fusion. Una collisione si impossessa in silenzio del pulsante dell'altro add-in. Lo script lo imposta su `<prefix><name>Cmd` |
| `WORKSPACE_ID` | `FusionSolidEnvironment` | Area di lavoro che riceve il pulsante. Questa è l'area di lavoro di progettazione | Un id di un'area di lavoro di Fusion |
| `PANEL_IDS` | `('SketchCreatePanel', 'SolidCreatePanel')` | Pannelli della barra degli strumenti, provati in quest'ordine. Il primo che esiste riceve il pulsante | Un elenco di id di pannelli, il più desiderato per primo |
| `IN_LINE` | `tplLine` | Id del campo di selezione | Qualsiasi testo, univoco all'interno di questo comando |
| `IN_LENGTH` | `tplLength` | Id del campo della lunghezza | come sopra |
| `IN_FLIP` | `tplFlip` | Id della casella di controllo | come sopra |
| `RESOURCE_FOLDER` | `resources/<name>` nella cartella dell'add-in | Cartella con le icone. Se non esiste, il pulsante non riceve alcuna icona | Una cartella con `16x16.png`, `32x32.png`, `64x64.png` |
| `LANG_DIR` | `lang` nella cartella dell'add-in | Cartella con i file di lingua | Una cartella con file `<code>.xml` |
| `_last` | `{IN_LENGTH: 1.0, IN_FLIP: False}` | Valori iniziali e valori ricordati dall'ultima chiamata | Una voce per ogni campo ricordato |
| `_CORE_MODULE` | `addin_core` | Nome del modulo core. Sta sopra `CONFIGURE` | Impostato dallo script su `<name in lower case>_core`. Lasciarlo così |

### Id dei pannelli nominati nel codice

| Id | Scheda |
| --- | --- |
| `SketchCreatePanel`, `SketchModifyPanel` | SKETCH |
| `SolidCreatePanel`, `SolidModifyPanel` | SOLID |
| `InspectPanel`, `ToolsPanel` | UTILITIES |

Ogni pannello viene cercato prima nell'area di lavoro, poi tra tutti i pannelli di Fusion.
Il pulsante viene aggiunto come "promoted", cioè viene mostrato direttamente sul pannello.

### Valori ricordati

- `_last` contiene i valori per la chiamata successiva del comando.
- Esistono solo in memoria. Spariscono quando Fusion si chiude o l'add-in viene riavviato.
- Le lunghezze sono in **cm**, l'unità interna di Fusion, qualunque cosa mostri il campo. `1.0` in un campo mostrato in `mm` vale 10 mm.
- Un valore viene ricordato solo se `remember()` lo copia e `build_inputs()` lo usa come valore iniziale.

## Manifest

Il manifest è un file JSON. Lo legge Fusion.

| Campo | Valore nel modello | Significato | Impostato dallo script? |
| --- | --- | --- | --- |
| `autodeskProduct` | `Fusion360` | Il prodotto. Il controllo offline richiede questo valore | no |
| `type` | `addin` | Il tipo di estensione. Il controllo offline richiede questo valore | no |
| `id` | `00000000-0000-0000-0000-000000000000` | GUID dell'add-in. Gli zeri sono un segnaposto | sì, un nuovo GUID casuale |
| `author` | `Your Name` | Autore | sì, da `--author` |
| `description` | un testo ciascuno per `""` (predefinito), `de-DE`, `es-ES`, `fr-FR`, `it-IT` | Descrizione dell'add-in | **no – descrive ancora il modello. Modificarla** |
| `version` | `1.0.0.0` | Versione. L'add-in la legge e la mostra tra parentesi dopo il nome del comando | **no – mantiene il numero del modello. Impostare il proprio** |
| `runOnStartup` | `true` | Avvia l'add-in insieme a Fusion | no |
| `supportedOS` | `windows\|mac` | Sistemi a cui l'add-in è destinato | no |
| `editEnabled` | `true` | Un campo di Fusion. Il codice del modello non lo usa | no |

La versione è scritta in un solo posto, il manifest. Il codice la legge da lì, quindi il titolo della finestra di dialogo non può differire dal manifest.
Se il manifest non può essere letto o non ha una versione, il nome viene mostrato senza parentesi.

## File di lingua

### Formato

Un file per lingua: `lang/<code>.xml`.

```xml
<strings language="en">
  <string key="in.length">Length</string>
</strings>
```

- `en.xml` è il riferimento. Lì esiste ogni chiave.
- L'attributo `language` deve essere uguale al codice nel nome del file.
- I segnaposto `{0}`, `{1}`, … vengono riempiti dall'add-in. Devono restare in ogni traduzione.
- Gli altri file possono tralasciare delle chiavi. Le chiavi mancanti vengono mostrate in inglese.

### Chiavi nel modello

| Chiave | Testo italiano |
| --- | --- |
| `cmd.name` | Modello di add-in |
| `cmd.tooltip` | Punto di partenza per un add-in di Fusion 360. / Traccia un segno a metà della linea selezionata. (due righe) |
| `in.line` | Linea |
| `in.line.prompt` | Seleziona una linea di schizzo |
| `in.length` | Lunghezza |
| `in.flip` | Inverti direzione |
| `err.no_selection` | Seleziona esattamente una linea di schizzo. |
| `err.length_positive` | La lunghezza deve essere maggiore di 0. |
| `err.zero_length` | La linea selezionata ha lunghezza zero. |
| `err.too_long` | La lunghezza supera la linea selezionata ({0} mm). |
| `msg.panel_missing` | Nessun pannello della barra degli strumenti adatto trovato. |
| `msg.exec_failed` | Errore durante la creazione della geometria: {0} |
| `msg.dialog_failed` | Errore durante la costruzione della finestra di dialogo: {0} |
| `msg.run_failed` | Avvio non riuscito: {0} |
| `msg.stop_failed` | Arresto non riuscito: {0} |

`cmd.name` è anche il titolo di ogni finestra di messaggio.

### Come viene scelta la lingua

La lingua viene scelta una volta sola, all'avvio dell'add-in. Nell'add-in non c'è un selettore.

1. La lingua impostata nelle preferenze di Fusion (la lingua dell'utente).
2. Se questa non dà una lingua supportata: le variabili d'ambiente `LANG`, `LANGUAGE`, `LC_ALL`, in quest'ordine.
3. Se questo non dà nulla: la lingua del sistema operativo.
4. Altrimenti l'inglese.

Codici supportati: `de`, `en`, `es`, `fr`, `it`.

Dopo aver cambiato la lingua in Fusion, arrestare l'add-in ed eseguirlo di nuovo.

### Aggiungere una lingua

1. Copiare `lang/en.xml` e dare alla copia il nome del codice di due lettere, per esempio `ja.xml`.
2. Impostare `language="ja"` nel primo tag.
3. Tradurre i valori. Mantenere le chiavi e i segnaposto.
4. Nel modulo core (`<name>_core.py`) aggiungere il codice a `SUPPORTED_LANGUAGES`.
5. Nel modulo core aggiungere la lingua di Fusion a `FUSION_LANGUAGE_MAP`, per esempio `'JapaneseLanguage': 'ja'`.
6. Eseguire il controllo offline, vedere [development.md](development.md).
