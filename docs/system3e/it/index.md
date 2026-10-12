# System3E – documentazione

System3E è un add-in per Autodesk Fusion 360. Posiziona in un progetto gli elementi per pareti del sistema
costruttivo a secco SYSTEM 3E. Si fa clic su un punto, si sceglie uno dei 74 elementi da un elenco e l'elemento
viene creato lì come corpo solido.

Questa documentazione descrive la versione 1.2.0.0.

## Contenuto

| File | Che cosa vi si trova |
| --- | --- |
| [installation.md](installation.md) | Requisiti, installazione, primo avvio, aggiornamento, rimozione |
| [usage.md](usage.md) | Posizionare gli elementi passo per passo, costruire una parete a giunti sfalsati, distinta dei pezzi |
| [settings.md](settings.md) | Ogni campo della finestra di dialogo, valori predefiniti, che cosa viene ricordato, lingua |
| [how-it-works.md](how-it-works.md) | File, libreria degli elementi, come viene costruito un corpo, punti, unità |
| [troubleshooting.md](troubleshooting.md) | Ogni messaggio, la sua causa e che cosa fare; limiti noti |
| [development.md](development.md) | Cartelle, test, rigenerare la libreria, versioni, rilascio |

Altri file: [registro delle modifiche](../CHANGELOG.md), [licenza](../LICENSE), [disegno dei punti](../s1-wp-punkte.svg).

## Che cosa fa l'add-in

- Aggiunge a Fusion un solo pulsante, **Elemento SYSTEM 3E**.
- Il pulsante apre una finestra di dialogo con otto campi e un'immagine di anteprima.
- L'elemento viene creato come componente con un solo corpo solido.
- Ogni elemento porta dodici punti propri. Si possono cliccare per posizionare l'elemento successivo.
- Lo stesso elemento posizionato di nuovo è un'altra copia dello stesso componente. Una distinta dei pezzi conta insieme gli elementi uguali.

## Che cosa è testato e che cosa no

| Parte | Stato |
| --- | --- |
| Posizionamento degli elementi | Usato dall'autore dentro Fusion |
| I dodici punti da cliccare | Usati dall'autore dentro Fusion |
| Punti mostrati sulla superficie e corretti dopo la creazione di un elemento (dalla 1.1.0.1) | Usati dall'autore dentro Fusion |
| Le scelte sotto **Posiziona da** | Usate dall'autore dentro Fusion |
| **Spostamento X**, **Spostamento Y**, **Spostamento Z** | Usati dall'autore dentro Fusion |
| Correzioni della versione 1.0.0.1 (vedere il [registro delle modifiche](../CHANGELOG.md)) | Non ancora confermate dentro Fusion |
| Nomi sinistra/destra degli elementi d'angolo e per finestra | Abbinati a occhio alle schede di catalogo del produttore, **non confermati** |
| Elemento `S0/2 200 P` | Danneggiato nel file 3D del produttore, ricostruito da `S0/2 250 P` |

## Note legali

- L'add-in **non è affiliato a SYSTEM 3E**.
- Licenza: MIT. Vedere [LICENSE](../LICENSE).
- Autore: Sorglos Thomas Weirich.
