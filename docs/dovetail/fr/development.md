# Développement

Dovetail est l'un des add-ins du dépôt <https://github.com/sorglos-it/fusion360>.
Tous les chemins ci-dessous sont relatifs à la racine du dépôt.

## Dossiers

| Chemin | Contenu |
|---|---|
| `apps/desktop-dovetail/Dovetail/` | L'add-in exactement tel que Fusion le veut : `Dovetail.py`, `Dovetail.manifest`, `lang/`, `resources/` |
| `apps/desktop-dovetail/VERSION` | Le numéro de version, une ligne |
| `apps/desktop-dovetail/tests/test_geometry.py` | Les tests hors ligne |
| `tools/dovetail/make_icons.py` | Écrit l'icône de la barre d'outils (16, 32, 64 px) dans `resources/Dovetail/` |
| `tools/dovetail/make_arrow_icons.py` | Écrit les icônes des boutons **Déplacer** dans `resources/nudge_left`, `nudge_center`, `nudge_right` |
| `tools/dovetail/test_geometry.py` | Renvoi vers le fichier de test déplacé, pour que l'ancienne commande continue de fonctionner |
| `tools/set_version.py` | Règle la version d'un add-in ou de tous (commun à tous les add-ins) |
| `tools/release.py` | Crée le ZIP de la version (commun à tous les add-ins) |
| `docs/dovetail/` | README, CHANGELOG, LICENSE et cette documentation |
| `dist/` | Sortie de `tools/release.py` ; pas dans Git |

Fusion exige que le dossier, le fichier `.py` et le fichier `.manifest` portent le même nom. Ne pas renommer l'un d'eux seul.

## Structure de `Dovetail.py`

| Section | Parties principales |
|---|---|
| Langue | `Strings`, `T()`, `detect_language()`, `read_version()`, `display_name()` |
| Géométrie | `GeometryError`, `_offset_polyline()`, `_top_half()`, `_check_contour()`, `end_room()`, `max_offset()`, `tooth_directions()`, `build_contours()`, `closed_band()` |
| Dessin | `_to_world()`, `_draw_closed_polyline()`, `line_length()`, `create_geometry()` |
| Gestionnaires | `_read_inputs()`, `_selected_lines()`, `_check_lines()`, `_run()`, `ExecuteHandler`, `PreviewHandler`, `ValidateHandler`, `InputChangedHandler`, `CommandCreatedHandler`, `_apply_nudge()`, `_apply_mirror()` |
| Démarrage / arrêt | `_find_panel()`, `run()`, `stop()` |

La section géométrie est du calcul pur. Elle n'utilise rien de Fusion et peut fonctionner dans n'importe quel Python 3.

## Exécuter les tests

Prérequis : Python 3, bibliothèque standard uniquement. Fusion n'est pas nécessaire ; le fichier de test met en place de petits substituts des
modules `adsk` avant d'importer l'add-in.

```bash
python apps/desktop-dovetail/tests/test_geometry.py
```

L'ancienne commande fonctionne toujours et donne la même sortie et le même code de sortie :

```bash
python tools/dovetail/test_geometry.py
```

- Chaque contrôle affiche `ok` ou `FAIL`.
- La dernière ligne est `all tests passed`, ou le nombre d'échecs.
- Le code de sortie vaut 1 si quelque chose a échoué.

Ce que couvrent les sections :

| Section | Contenu |
|---|---|
| 1–4 | Les trois formes ; les points du contour ; le contour décalé est parallèle et à la bonne distance |
| 5 | Alignement : le groupe est centré sur le milieu de la ligne |
| 6 | Décalage, décalage maximal, distance aux extrémités de la ligne |
| 7 | Qui paie le jeu (les trois entrées de **La ligne est**) |
| 8 | Géométrie reflétée : les deux pièces identiques ; acceptée et refusée de la même façon dans les deux sens |
| 9 | Les échecs signalent la bonne clé ; un assemblage par ligne sélectionnée ; une mauvaise ligne se nomme elle-même |
| 10 | Chaque entrée de liste déroulante et chaque clé d'infobulle existe dans `en.xml` |
| 11 | Fichiers de langue : complets, aucune clé inconnue, paramètres de substitution conservés, aucun texte vide |
| 12 | Catalogue de textes, repli sur l'anglais, détection de la langue sans Fusion |

Pour tester une copie installée au lieu de celle du dépôt, régler la variable d'environnement
`DOVETAIL_ADDIN_DIR` sur son dossier. Les deux scripts d'icônes lisent la même variable.

Non couvert par le fichier de test :

- Tout ce qui a besoin de Fusion : la boîte de dialogue, l'aperçu, le dessin, la conversion en géométrie de construction, l'annulation
  après une exécution échouée.
- L'exécution avec 34 317 contours aléatoires citée dans le changelog. C'était un contrôle ponctuel ; elle ne fait pas partie de
  `test_geometry.py`.

## Icônes

```bash
python tools/dovetail/make_icons.py
python tools/dovetail/make_arrow_icons.py
```

Les deux écrivent des fichiers PNG avec la bibliothèque standard uniquement. Ne les exécuter que lorsque les icônes doivent changer.

## Numéros de version

Les versions ont quatre parties, `v.x.y.z` : version, release, feature, build. Exemple : `1.1.0.0`.

Le numéro est conservé à deux endroits :

- `apps/desktop-dovetail/VERSION`
- l'entrée `"version"` de `Dovetail.manifest` (c'est ce que lisent Fusion et le titre de la boîte de dialogue)

Ne jamais les modifier à la main. Utiliser le script, qui écrit les deux :

```bash
python tools/set_version.py dovetail 1.1.0.1    # set one add-in
python tools/set_version.py all 1.0.0.0         # set all add-ins of the repository
python tools/set_version.py --check             # report add-ins whose two numbers differ
```

Le script refuse un numéro qui n'a pas quatre parties. `--check` se termine avec le code de sortie 1 si un add-in diffère.

## Créer une version

```bash
python tools/release.py dovetail
```

- Écrit `dist/Dovetail-<version>.zip`.
- Le ZIP contient le dossier `Dovetail/` exactement tel que Fusion le veut.
- Laissés de côté : `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compression : Deflate au niveau le plus élevé, pour que tout programme de décompression puisse le lire.
- Après l'écriture, le ZIP est relu et testé.
- Le script refuse de créer le ZIP si `VERSION` et le manifeste ne concordent pas.

`python tools/release.py all` crée le ZIP de chaque add-in du dépôt.

Ordre conseillé pour une version :

1. Exécuter les tests.
2. Régler la version avec `tools/set_version.py`.
3. Ajouter l'entrée dans `docs/dovetail/CHANGELOG.md`.
4. Mettre à jour cette documentation.
5. Créer le ZIP avec `tools/release.py`.
6. Joindre `dist/Dovetail-<version>.zip` à la version sur GitHub.

## Ajouter une langue

1. Copier `lang/en.xml` et nommer la copie d'après le code de langue à deux lettres.
2. Régler `language="<code>"` dans l'élément racine et traduire les valeurs.
3. Conserver chaque paramètre de substitution (`{0}`, `{1}`, …).
4. Ajouter le code à `SUPPORTED_LANGUAGES` et le nom de langue Fusion correspondant à `FUSION_LANGUAGE_MAP` dans
   `Dovetail.py`.
5. Exécuter les tests. Ils contrôlent dans chaque fichier l'exhaustivité, les clés inconnues, les paramètres de substitution et les textes vides.

`en.xml` est le fichier de référence. Chaque clé y existe. Une clé absente ailleurs se replie sur lui ; une clé absente
partout est affichée telle quelle, sous forme de clé.

## Décisions et leurs raisons

Tirées des commentaires du code.

| Décision | Raison |
|---|---|
| Les textes se trouvent dans `lang/<code>.xml` ; les erreurs portent une clé, pas un texte | La raison d'une erreur reste indépendante de la langue ; les tests peuvent comparer des clés |
| La forme et la répartition sont enregistrées comme index dans la liste | La valeur enregistrée ne dépend pas de la langue d'affichage |
| Les valeurs de langue de Fusion sont recherchées avec `getattr` | Une valeur que cette version de Fusion ne connaît pas ne peut pas casser l'add-in |
| La version est lue dans le manifeste | La boîte de dialogue ne peut pas s'écarter du manifeste |
| La version fait partie du nom de la commande | Fusion utilise le nom de la commande comme titre de la boîte de dialogue ; c'est donc là qu'une version est visible tant que la boîte de dialogue est ouverte |
| Le décalage n'est pas mémorisé | Il appartient à la ligne en cours, pas aux réglages |
| La ligne d'origine devient une géométrie de construction au lieu d'être supprimée | Elle cesse de créer des profils mais conserve ses cotes et ses contraintes |
| L'aperçu ne touche pas à la ligne d'origine | La sélection ne peut pas être invalidée sous la boîte de dialogue ouverte |
| Toutes les lignes sont contrôlées avant qu'une seule soit dessinée | Une mauvaise ligne à la fin ne peut pas laisser l'esquisse à moitié dessinée |
| Un échec sur l'une de plusieurs lignes est enveloppé avec sa position | Une ligne courte au milieu échoue alors que les autres conviendraient ; le message dit laquelle |
| Les boutons **Déplacer** prennent la ligne la plus courte comme limite | Un décalage qui sort d'une ligne ne vaut rien, même si les autres pouvaient le supporter |
| Avec le reflet, le nombre, la répartition et le décalage sont réglés et grisés | Chacun d'eux rompt la symétrie à 180 degrés ; les fixer vaut mieux que les laisser échouer à la validation |
| Le reflet exige un nombre pair | Une dent au milieu devrait pointer des deux côtés à la fois |
| L'entraxe minimal a 0,01 mm en plus | Exactement au minimum, le tronçon entre deux mortaises n'a plus aucune longueur |
| Les dents gardent tolérance + 0,01 mm par rapport aux extrémités de la ligne | La mortaise s'ouvre d'autant que la tolérance ; sinon le contour dépasse l'extrémité et doit revenir en arrière |
| Un contour est contrôlé pour les segments de longueur nulle et pour les croisements avec lui-même | Le décalage traite chaque angle en onglet séparément ; rien d'autre n'empêche donc un segment court de se réduire à néant ou de se retourner |
| Un angle en onglet plus éloigné que 12 × le décalage est refusé | Le contour d'accouplement déraperait dans un angle aigu |
| Une exécution échouée règle `executeFailed` | Fusion annule alors ce qui a été dessiné jusque-là |
| Le dessin s'exécute avec `isComputeDeferred` | L'esquisse se recalcule une seule fois, pas après chaque ligne |
| `set_version.py` écrit VERSION et le manifeste ensemble | Le numéro n'est jamais modifié à la main à deux endroits |
| Le ZIP utilise Deflate au niveau le plus élevé | Tout programme de décompression peut le lire |

## Points ouverts connus

- Quand OK est grisé, la boîte de dialogue n'affiche aucune raison. Les textes existent (`err.*`) mais seule la boîte de message après une
  exécution échouée les affiche.
- Les lignes d'esquisse sont lues avec X et Y seulement et la bande est dessinée à Z = 0 de l'esquisse.
- Les modifications de géométrie de la 1.1.0.0 sont testées hors ligne uniquement, pas dans Fusion.

## Licence

MIT, voir [LICENSE](../LICENSE). Auteur : Sorglos Thomas Weirich.
