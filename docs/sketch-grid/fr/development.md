# Développement

SketchGrid est l'un des add-ins du dépôt <https://github.com/sorglos-it/fusion360>. Tous les chemins ci-dessous partent de la racine du dépôt.

## Dossiers

| Chemin | Contenu |
| --- | --- |
| `apps/desktop-sketch-grid/SketchGrid/` | L'add-in exactement tel que Fusion en a besoin : `SketchGrid.py`, `sketchgrid_core.py`, `SketchGrid.manifest`, `lang/`, `resources/SketchGrid/` |
| `apps/desktop-sketch-grid/VERSION` | Le numéro de version, une ligne |
| `apps/desktop-sketch-grid/tests/test_sketchgrid.py` | Les tests |
| `tools/sketch-grid/make_icon.py` | Dessine l'icône du bouton (16, 32 et 64 pixels) |
| `tools/sketch-grid/test_sketchgrid.py` | Renvoie seulement vers les tests ci-dessus, pour que l'ancienne commande continue de fonctionner |
| `tools/set_version.py` | Règle le numéro de version (commun à tous les add-ins) |
| `tools/release.py` | Crée le ZIP de la version (commun à tous les add-ins) |
| `docs/sketch-grid/` | README, CHANGELOG, LICENSE et cette documentation |
| `dist/` | Créé par `tools/release.py` ; pas dans Git |

Le dossier, le fichier `.py` et le fichier `.manifest` doivent partager le nom `SketchGrid`. Fusion l'exige.

Tous les scripts n'ont besoin que d'un Python 3 normal avec sa bibliothèque standard. Il n'y a rien à compiler ; l'add-in fonctionne tel quel.

## Exécuter les tests

```
python apps/desktop-sketch-grid/tests/test_sketchgrid.py
python apps/desktop-template/tests/test_addin.py --path apps/desktop-sketch-grid/SketchGrid
```

La première commande fonctionne sans Fusion. Le fichier de test met en place des substituts vides des modules `adsk` de Fusion, puis importe `SketchGrid.py`. Il affiche une ligne par contrôle (`ok` ou `FAIL`) et se termine par `all tests passed` et le code de sortie 0, ou par le nombre d'échecs et le code de sortie 1.

Ce qu'il contrôle :

| Section | Sujet |
| --- | --- |
| 1 | L'exemple standard : 10 × 5 mm, écart 2 mm, 8 colonnes, 4 lignes donnent 94 × 26 mm et 32 cellules |
| 2, 2b | Chaque entrée de point d'ancrage a les facteurs que son nom promet (déduits du nom de la clé, par exemple `bottom_left`), et le point arrive là où l'entrée le dit |
| 3 | Positions des cellules |
| 4 | Le mode « Remplissage d'une zone » ne compte que ce qui tient entièrement |
| 5 | Chaque refus signale la bonne clé de message |
| 6 | Fichiers de langue : les cinq sont complets et conservent leurs paramètres de substitution |
| 7 | Décalage par rapport au point sélectionné |
| 8 | L'écart reste l'écart pour chaque forme : rectangle mesuré du polygone, étirement, taille réelle en mode remplissage |
| 9 | Coins du rectangle : limites et contour fait de lignes et d'arcs |
| 10 | Chaque entrée de liste déroulante a un texte |
| 11 | Catalogue de textes : chargement de chaque langue, repli sur l'anglais, les messages suivent la langue |

La seconde commande est le contrôle de structure de l'add-in modèle du même dépôt. Elle contrôle le manifeste, l'id, l'id de commande et les icônes.

Par défaut, les tests et le script d'icône utilisent `apps/desktop-sketch-grid/SketchGrid`. Régler la variable d'environnement `SKETCHGRID_ADDIN_DIR` pour tester une autre copie, par exemple une copie installée.

Ce que les tests ne couvrent pas : tout ce qui a besoin de Fusion. C'est-à-dire la boîte de dialogue, la sélection, l'aperçu et les appels de dessin proprement dits. Ces parties ne peuvent être essayées que dans Fusion.

## Essayer une modification dans Fusion

1. Copier `apps/desktop-sketch-grid/SketchGrid` dans le dossier des add-ins de Fusion (voir [installation.md](installation.md)).
2. Dans Fusion, arrêter l'add-in et le relancer.

`SketchGrid.py` retire `sketchgrid_core` du cache de modules de Python avant de l'importer. Raison d'après le commentaire du code : Fusion met en cache les modules importés ; un module d'aide modifié continuerait donc de servir son ancienne version jusqu'au redémarrage de Fusion.

## Numéros de version

Quatre parties : `v.x.y.z` (version, release, feature, build), par exemple `1.1.0.0`.

Le numéro est conservé à deux endroits :

- `apps/desktop-sketch-grid/VERSION`
- l'entrée `"version"` dans `SketchGrid.manifest` (c'est celle que lisent Fusion et le nom du bouton)

Ne jamais les modifier à la main. Utiliser le script, qui écrit les deux :

```
python tools/set_version.py sketch-grid 1.1.0.1
python tools/set_version.py --check
```

- La première commande règle la version. Elle refuse tout ce qui n'est pas quatre nombres séparés par des points.
- `--check` liste chaque add-in avec ses deux numéros et indique `ok` ou `DIFFERENT OR NOT v.x.y.z`. Code de sortie 1 si un add-in est incorrect.
- `all` à la place de `sketch-grid` règle le même numéro pour chaque add-in du dépôt.

Ajouter une entrée dans `docs/sketch-grid/CHANGELOG.md` pour chaque nouveau numéro.

## Créer une version

```
python tools/release.py sketch-grid
```

- Écrit `dist/SketchGrid-<version>.zip`.
- Le ZIP contient le dossier `SketchGrid` comme niveau supérieur, prêt à être décompressé dans le dossier des add-ins de Fusion.
- Laissés de côté : les dossiers `__pycache__` et les fichiers se terminant par `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compression : Deflate au niveau le plus élevé, « pour que tout programme de décompression puisse le lire » (commentaire du script).
- Le script refuse de créer le ZIP quand `VERSION` et le manifeste diffèrent ou que le numéro n'a pas quatre parties.
- Après l'écriture, il relit le ZIP et s'arrête si un fichier qu'il contient est endommagé.
- `all` à la place de `sketch-grid` crée le ZIP de chaque add-in.

Le ZIP est ensuite joint à une version sur <https://github.com/sorglos-it/fusion360/releases>. Le script ne téléverse rien.

## Redessiner l'icône

```
python tools/sketch-grid/make_icon.py
```

Écrit `16x16.png`, `32x32.png` et `64x64.png` dans `resources/SketchGrid/`. L'image est une grille de 3 × 3 cellules avec une croix au milieu pour le point sélectionné. Le script écrit lui-même les fichiers PNG, sans bibliothèque d'images.

## Ajouter une langue

1. Copier `lang/en.xml` vers `lang/<code>.xml` (code à deux lettres) et traduire les textes. Conserver les clés et les paramètres de substitution `{0}`, `{1}`.
2. Dans `sketchgrid_core.py`, ajouter le code à `SUPPORTED_LANGUAGES`, et le nom de langue Fusion correspondant à `FUSION_LANGUAGE_MAP`.
3. Exécuter les tests. Ils contrôlent chaque langue de `SUPPORTED_LANGUAGES`.

## Décisions et leurs raisons

Tirées des commentaires du code.

| Décision | Raison donnée |
| --- | --- |
| Le calcul de la grille (`grid_layout`, `cell_centres`, `corner_outline`) n'utilise aucun appel à Fusion. | C'est la partie qui mérite d'être testée, et les tests peuvent ainsi s'exécuter sans démarrer Fusion. |
| Les choix des listes déroulantes sont enregistrés comme position dans la liste, pas comme texte. | La valeur enregistrée ne bouge pas quand la langue de l'interface change. |
| Au plus 2000 formes (`MAX_SHAPES`). | Un nombre qui s'emballe en mode remplissage bloque Fusion pendant des minutes. Mieux vaut refuser. |
| Un rayon / chanfrein supérieur à la moitié du côté le plus court est refusé, pas réduit. | Exactement à la moitié, les deux coupes d'un côté se rejoignent ; au-delà, elles se dépasseraient l'une l'autre. Seul le bruit d'arrondi est absorbé. |
| Les coins ne participent pas à la disposition. | Le rectangle englobant mesure toujours longueur × profondeur ; le pas, le nombre et l'écart restent donc ce qu'ils étaient. |
| Un polygone régulier annonce sa propre taille mesurée et le pas la suit. | Il ne peut pas remplir une cellule d'autres proportions ; sinon, l'écart demandé n'est pas l'écart obtenu. |
| Le rectangle du polygone est mesuré, pas supposé. | Un polygone n'a un sommet sur chaque extrême que pour des nombres de côtés adaptés ; un pentagone est placé bas dans son propre rectangle. |
| Un carré entièrement arrondi est dessiné comme un cercle. | Un cercle n'est pas une chaîne de segments. |
| Pour une ellipse, le point de l'axe principal est placé sur l'axe le plus long. | Sinon, Fusion rejette l'ellipse. |
| `isComputeDeferred` est activé pendant le dessin et rétabli dans un bloc `finally`. | Cela tient le solveur au repos jusqu'à ce que chaque forme soit dessinée ; avec quelques centaines de cellules, c'est la différence entre instantané et inutilisable. |
| Le gestionnaire d'aperçu avale toutes les erreurs. | Il se déclenche à chaque frappe, y compris sur des valeurs à moitié saisies. Signaler est le rôle de la validation des saisies. |
| Les gestionnaires d'événements sont enregistrés avant la reprise du point présélectionné, et cette reprise peut échouer en silence. | Quoi qu'il échoue ensuite, la boîte de dialogue doit encore fonctionner ; l'utilisateur sélectionne alors le point dans la boîte de dialogue. |
| Tous les gestionnaires d'événements sont conservés dans un registre (`HandlerRegistry`). | Fusion ne garde qu'une référence faible vers un gestionnaire. Sans référence du côté Python, l'événement cesse de se déclencher, en silence. |
| Plusieurs id de panneau sont essayés dans l'ordre. | Les id de panneau changent d'une version de Fusion à l'autre. |
| Les valeurs de langue de Fusion sont recherchées par nom, avec un repli. | Une valeur que cette version de Fusion ne connaît pas ne peut pas casser l'add-in ; il se replie sur l'anglais au lieu d'échouer. |
| Une clé absente d'une traduction est servie depuis l'anglais. | Une traduction à moitié faite se dégrade vers l'anglais au lieu de montrer des clés brutes. |
| Les problèmes attendus sont levés comme `AddInError` avec une clé de message. | La clé est indépendante de la langue ; ce que l'utilisateur peut corriger doit bloquer OK au lieu d'ouvrir une fenêtre. |
| La version est lue dans le manifeste, pas écrite dans le code. | La boîte de dialogue ne peut pas s'écarter du manifeste, et il n'y a qu'un seul endroit à modifier. |
| La version fait partie du nom de la commande. | Fusion utilise le nom de la commande comme titre de la boîte de dialogue ; c'est donc là que la version est visible ; il n'y a que ce seul nom. |
| Les dernières valeurs sont gardées en mémoire en centimètres. | Les centimètres sont l'unité interne de Fusion, quelle que soit l'unité d'affichage. |

## Points ouverts

- La version 1.1.0.0 (le point présélectionné ne peut pas être repris) est testée hors ligne uniquement, pas dans Fusion.
- Les trous oblongs et les rectangles arrondis ou chanfreinés sont dessinés comme des courbes séparées à partir de coordonnées, sans points d'extrémité partagés. Il faut vérifier dans Fusion s'ils restent liés quand on les fait glisser.
- La limite de 2000 compte les formes, pas les courbes. Il faut vérifier dans Fusion si elle doit compter les courbes.

## Licence

MIT, voir [LICENSE](../LICENSE). Auteur : Sorglos Thomas Weirich.
