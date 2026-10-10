# SketchGrid

SketchGrid è un add-in per Autodesk Fusion 360. Si fa clic su un punto in uno schizzo e si ottiene attorno a esso una griglia di forme uguali: rettangoli, cerchi o ellissi, asole oppure poligoni.

Questa documentazione descrive la versione 1.1.0.0.

## Contenuto

| File | Cosa contiene |
| --- | --- |
| [installation.md](installation.md) | Requisiti, installazione, primo avvio, aggiornamento, rimozione |
| [usage.md](usage.md) | Ogni funzione, passo per passo |
| [settings.md](settings.md) | Ogni campo della finestra di dialogo con valore predefinito e limiti, cosa viene ricordato, lingua |
| [how-it-works.md](how-it-works.md) | File, come viene calcolata la griglia, come vengono disegnate le forme |
| [troubleshooting.md](troubleshooting.md) | Ogni messaggio, la sua causa e cosa fare; limiti noti |
| [development.md](development.md) | Cartelle, test, numeri di versione, creazione del pacchetto di rilascio |

## Cosa fa, in breve

- Due modi per stabilire il numero di forme: **Colonne e righe**, oppure **Riempimento di un'area** (quante ne entrano per intero).
- Quattro forme: **Rettangolo** (spigoli vivi, raccordati o smussati), **Cerchio / ellisse**, **Asola**, **Poligono** (da 3 a 24 lati).
- Nove posizioni per il punto dentro la griglia, più uno scostamento in X e in Y.
- Una distanza separata per X e per Y.
- Una riga **Risultato** che mostra il numero di forme e la dimensione totale mentre si scrive.
- Al massimo 2000 forme per griglia.

## Stato dei test

- Il calcolo della griglia, i contorni degli spigoli, i messaggi e i cinque file di lingua sono controllati da un test automatico che gira senza Fusion.
- La modifica della versione 1.1.0.0 (la finestra di dialogo continua a funzionare quando il punto selezionato in precedenza non può essere ripreso) è stata verificata solo offline, **non all'interno di Fusion**.
- Due limiti noti vengono da una revisione del codice e **non sono confermati all'interno di Fusion**. Vedere [troubleshooting.md](troubleshooting.md#limiti-noti).

## Licenza e autore

Licenza MIT, vedere [LICENSE](../LICENSE). Autore: Sorglos Thomas Weirich.

Cronologia delle modifiche: [CHANGELOG.md](../CHANGELOG.md).
