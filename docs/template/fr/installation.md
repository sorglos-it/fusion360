# Installation

## Prérequis

| Quoi | Nécessaire pour |
| --- | --- |
| Autodesk Fusion 360 sous Windows ou macOS | faire tourner le complément |
| Python 3 sur l'ordinateur | les outils de `tools/` (génération, contrôle hors ligne, icônes, version, empaquetage) |

Le complément lui-même n'a besoin de rien de plus. Il utilise seulement le Python fourni dans Fusion.
Les outils utilisent seulement la bibliothèque standard de Python. Il n'y a rien à installer avec `pip`.

## Obtenir le dépôt

Il n'y a pas de ZIP de version pour la version 1.0.0.0. Utiliser le dépôt.

1. Ouvrir <https://github.com/sorglos-it/fusion360>.
2. Le cloner, ou le télécharger sous forme de ZIP et le décompresser.
3. Ouvrir un terminal dans le dossier du dépôt.

## Créer un nouveau complément

```bash
python tools/template/new_addin.py MyAddIn --install
```

Cela crée le complément `MyAddIn` directement dans le dossier des compléments de Fusion.

### Règles pour le nom

- Il doit commencer par une lettre.
- Il ne peut contenir que des lettres et des chiffres. Pas d'espaces, pas de traits d'union, pas de tirets bas.
- Il ne doit pas être `AddInTemplate`.

Le nom devient un nom de module Python. C'est pourquoi les règles sont strictes.

### Toutes les options

| Option | Valeur par défaut | Effet |
| --- | --- | --- |
| `name` (obligatoire) | – | Nom du complément, par exemple `MyAddIn` |
| `--install` | désactivé | Le créer directement dans le dossier des compléments de Fusion |
| `--out DIR` | le dossier qui contient le dépôt | Le créer dans `DIR` à la place. `DIR` est créé s'il n'existe pas |
| `--author NAME` | `Your Name` | Écrit dans le champ `author` du manifeste |
| `--prefix STR` | `thw` | Préfixe de l'id de la commande. L'id devient `<prefix><name>Cmd` |
| `--force` | désactivé | Écraser un dossier existant de ce nom |
| `-h`, `--help` | – | Afficher le texte d'aide |

Remarques :

- `--install` et `--out` ne peuvent pas être utilisés ensemble.
- Sans `--install` et sans `--out`, le complément est créé **à côté** du dossier du dépôt, pas à l'intérieur.
- `--force` **supprime d'abord tout le dossier existant**, y compris les modifications personnelles qu'il contient. Puis il crée une copie neuve.
- Choisir son propre `--prefix`. `thw` est le préfixe de l'auteur du modèle.

### Ce que fait le script

1. Copie `apps/desktop-template/AddInTemplate` vers `<target>/<name>` (sans `__pycache__` ni fichiers `.pyc`).
2. Renomme `AddInTemplate.py` en `<name>.py` et `AddInTemplate.manifest` en `<name>.manifest`.
3. Renomme `addin_core.py` en `<name in lower case>_core.py`, par exemple `myaddin_core.py`.
4. Renomme le dossier d'icônes `resources/AddInTemplate` en `resources/<name>`.
5. Dans le fichier d'entrée : règle `_CORE_MODULE` et `CMD_ID`, et remplace chaque `AddInTemplate` par le nouveau nom.
6. Dans le manifeste : écrit un nouveau GUID aléatoire dans `id` et le nom de l'auteur dans `author`.
7. Dans chaque `lang/*.xml` : met `cmd.name` au nouveau nom et `cmd.tooltip` au nom suivi de la ligne `TODO: describe what this command does.`

Le script ne modifie **pas** la `description` ni la `version` dans le manifeste. Les modifier soi-même, voir [settings.md](settings.md).

### Ce que l'on obtient

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

À la fin, le script affiche le chemin créé, le fichier d'entrée, le module central, l'id de la commande et les étapes suivantes.

## Dossier des compléments de Fusion

| Système | Chemin |
| --- | --- |
| Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
| macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

Si le complément a été créé sans `--install`, copier tout le dossier `MyAddIn` dans ce dossier.

Le dossier, le fichier d'entrée et le manifeste doivent porter le même nom : `MyAddIn/MyAddIn.py` et `MyAddIn/MyAddIn.manifest`.

## Premier démarrage dans Fusion

1. Démarrer Fusion 360.
2. Ouvrir **Utilities → ADD-INS → Add-Ins** (c'est le chemin que le script affiche).
3. Sélectionner le complément et appuyer sur **Run**.
4. Ouvrir une esquisse. Le bouton se trouve dans l'onglet **SKETCH**, dans le panneau de création. Si ce panneau n'existe pas, il va dans le panneau de création de l'onglet **SOLID**.

Dans le manifeste, `runOnStartup` vaut `true`.

Le bouton et le titre de la boîte de dialogue affichent le nom de la commande avec la version entre parenthèses, par exemple `Modèle de complément (1.0.0.0)`.

Ces étapes suivent le code et la sortie du script. Elles n'ont pas été testées dans Fusion pour cette documentation.

### Essayer le modèle lui-même

Il est aussi possible de lancer le modèle non modifié : copier le dossier `apps/desktop-template/AddInTemplate` dans le dossier des compléments de Fusion et le démarrer comme ci-dessus. Sa commande s'appelle `Modèle de complément`.

## Mise à jour

Il n'y a pas de fonction de mise à jour.

- Un complément créé à partir du modèle contient sa propre copie de tous les fichiers. Les modifications faites plus tard dans le modèle ne l'atteignent pas.
- Pour reprendre une correction, copier la modification à la main dans son `<name>_core.py` ou dans son fichier d'entrée.
- Relancer le script avec `--force` n'est pas une mise à jour. Cela supprime le dossier du complément et crée une copie neuve et vide.

## Suppression

1. Dans Fusion, ouvrir **Utilities → ADD-INS → Add-Ins**, sélectionner le complément et l'arrêter. À l'arrêt, le complément retire son bouton et sa commande de la barre d'outils.
2. Fermer Fusion.
3. Supprimer le dossier du complément dans le dossier des compléments de Fusion.

Le complément n'enregistre rien en dehors de son propre dossier. Les valeurs mémorisées n'existent qu'en mémoire, jusqu'à la fermeture de Fusion.
