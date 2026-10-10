# Développement

Retour à la [vue d'ensemble](index.md).

Toutes les commandes sont lancées depuis la racine du dépôt <https://github.com/sorglos-it/fusion360>.

## Dossiers

| Chemin | Contenu |
| --- | --- |
| `apps/desktop-system3e/System3E/` | Le complément tel que Fusion le charge (ce dossier va dans le ZIP de version) |
| `apps/desktop-system3e/System3E/System3E.py` | Commande, boîte de dialogue, placement, points |
| `apps/desktop-system3e/System3E/system3e_core.py` | Mécanique commune : catalogue de textes, détection de la langue, recherche du panneau, registre des gestionnaires, type d'erreur, version |
| `apps/desktop-system3e/System3E/System3E.manifest` | Manifeste Fusion : id, auteur, descriptions, version, `runOnStartup`, `supportedOS` |
| `apps/desktop-system3e/System3E/lang/` | `de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` ; `en.xml` est la référence |
| `apps/desktop-system3e/System3E/blocks/` | `blocks.json` et 74 images d'aperçu `<id>.png` (générés) |
| `apps/desktop-system3e/System3E/resources/System3E/` | Icône du bouton en 16, 32 et 64 px |
| `apps/desktop-system3e/VERSION` | Le numéro de version, une ligne |
| `apps/desktop-system3e/tests/` | `test_addin.py`, `test_blocks.py` |
| `tools/system3e/` | `build_library.py`, `mesh_to_solid.py`, `points_sheet.py`, `make_icon.py` |
| `tools/set_version.py`, `tools/release.py` | Outils de version et de publication pour tous les compléments du dépôt |
| `docs/system3e/` | README, journal des modifications, licence, le dessin des points, cette documentation |
| `assets/system3e/` | Le fichier 3D du fabricant. **Pas dans le dépôt**, conservé en local. |
| `dist/` | ZIP de version. Pas dans Git. |

`System3E.py` a deux zones marquées. Le code propre au complément se trouve entre `CONFIGURE` et `END OF TEMPLATE` ;
les gestionnaires d'événements et `run`/`stop` en dessous forment l'ossature. Le complément a été généré à partir
du modèle de complément du dépôt.

## Tests

Les deux tests fonctionnent sans Fusion. Ils placent des substituts des modules `adsk` dans `sys.modules` et
importent le complément. Bibliothèque standard seulement.

```bash
python apps/desktop-system3e/tests/test_addin.py
```

```bash
python apps/desktop-system3e/tests/test_blocks.py
```

Le code de sortie 1 signifie qu'au moins un contrôle a échoué.

`test_addin.py` vérifie :

| Section | Contrôles |
| --- | --- |
| 1) Layout | Le dossier, `System3E.py`, `System3E.manifest` et `lang/` existent et correspondent au nom du dossier |
| 2) Manifest | JSON valide, `type` vaut `addin`, `autodeskProduct` vaut `Fusion360`, l'id ressemble à un GUID |
| 3) Import | Le complément s'importe, `run` et `stop` existent, `CMD_ID` est défini, le fichier du module central existe |
| 4) Language files | Chaque fichier de langue existe, déclare sa langue, a toutes les clés de `en.xml` et aucune clé inconnue, garde chaque espace réservé `{0}`, n'a aucun texte vide |
| 5) Text catalogue | Chaque langue se charge, une langue inconnue se rabat sur l'anglais, une clé manquante renvoie la clé |
| 6) Icons | Les trois fichiers d'icône existent et sont de vrais fichiers PNG |

Options : `--addin <name>` et `--path <folder>` dirigent le test vers un autre dossier de complément.

`test_blocks.py` vérifie :

| Section | Contrôles |
| --- | --- |
| 1) Library file | L'unité est `mm`, 74 éléments, ids et noms uniques, ids utilisables comme noms de fichier |
| 2) Solids | Chaque élément est un solide fermé à faces planes, les contours tournent dans le bon sens, le volume est possible, le coin est à l'origine, la taille et les points concordent, la taille correspond au nom du catalogue, deux éléments n'ont jamais la même forme |
| 3) Pictures | Chaque élément a un PNG, aucune image en trop |
| 4) Add-in | Le complément lit chaque élément ; chaque nom de famille, d'ancrage et de point a un texte dans les cinq langues ; l'élément par défaut et l'ancrage par défaut existent |
| 5) Points for clicking | La hauteur d'empilement de `S1 WP` est 250 et celle de `EU 200 W` est 200 ; positions des ancrages ; douze points nommés par élément, tous à des endroits différents et sur l'élément ; `make_body()` transforme chaque point en sommet, définit chaque face, utilise chaque arête une fois dans chaque sens, et convertit les mm en cm |

Ce que les tests ne peuvent pas dire : si Fusion accepte un corps, crée les points de construction ou place
l'occurrence correctement. Cela ne se sait que dans Fusion.

État des tests dans Fusion : le placement des éléments a été utilisé par l'auteur. Les douze points, **Poser par**
et les décalages X/Y/Z n'ont été testés que hors ligne. Les corrections de la 1.0.0.1 ne sont pas encore
confirmées dans Fusion.

## Reconstruire la bibliothèque d'éléments

`blocks/blocks.json` et les images sont générés. Ne pas les modifier à la main.

Source : le fichier 3D du fabricant `assets/system3e/SYSTEM 3E START.3ds`. Il **ne fait pas partie du dépôt**.
Sans lui, la bibliothèque ne peut pas être reconstruite ; le script s'arrête avec « Source file missing ».

```bash
python tools/system3e/build_library.py
```

```bash
python tools/system3e/build_library.py --no-pictures
```

Les images ont besoin du paquet Python Pillow. `--no-pictures` les saute. Le complément lui-même n'a besoin ni de
l'un ni de l'autre.

Ce que fait la construction :

1. `mesh_to_solid.read_3ds()` lit chaque maillage de triangles du fichier et le convertit en mm.
2. `mesh_to_solid.solid_from_mesh()` soude les points distants de moins de 0,3 mm, trie les triangles par plans,
   réunit tous les triangles d'un même plan en contours (avec trous), supprime les points situés au milieu
   d'arêtes droites, et vérifie que chaque arête est utilisée une fois dans chaque sens. Le coin le plus bas de la
   boîte englobante devient l'origine.
3. La table `NAMES` donne à chaque numéro de maillage son nom de catalogue. Le fichier 3D ne contient aucun nom.
4. Les quatre éléments de cloison sont ajoutés comme de simples boîtes avec les tailles de la table `PARTITION`.
5. `S0/2 200 P` est reconstruit (voir plus bas).
6. `straighten()` donne exactement la même valeur, à 0,1 mm près, aux points censés partager une coordonnée.
7. `bend()` recalcule la normale de chaque face à partir de son contour. `stack_level()` trouve la hauteur
   d'empilement.
8. `blocks.json` est écrit dans l'ordre de la table `FAMILIES`, et une image par élément est dessinée.

La construction s'arrête si un élément n'est pas un solide fermé, si deux éléments partagent un id ou si le
contrôle de la reconstruction échoue.

Pour examiner le fichier source seul :

```bash
python tools/system3e/mesh_to_solid.py "assets/system3e/SYSTEM 3E START.3ds" --report
```

Il affiche une ligne par maillage avec la taille, le nombre de points et de faces, le volume et l'état.

### Autres outils

| Outil | Rôle |
| --- | --- |
| `python tools/system3e/points_sheet.py "S1 WP" docs/system3e/s1-wp-punkte.svg` | Dessine un élément avec tous ses points sous forme de SVG. Les points sont pris dans le complément lui-même. Les légendes sont en allemand. |
| `python tools/system3e/make_icon.py` | Génère les PNG de l'icône du bouton en 16, 32 et 64 px |

## Numéros de version

Une version a quatre parties, `v.x.y.z` : version, release, feature, build. Exemple : `1.1.0.0`.

Le numéro est tenu à deux endroits : `apps/desktop-system3e/VERSION` et l'entrée `version` du manifeste. Fusion et
le titre de la boîte de dialogue lisent le manifeste. Ne jamais modifier les deux à la main ; utiliser l'outil :

```bash
python tools/set_version.py system3e 1.1.0.1
```

```bash
python tools/set_version.py --check
```

`--check` liste chaque complément du dépôt et signale ceux dont les deux numéros diffèrent ou ne sont pas de la
forme `v.x.y.z`. `all` à la place de `system3e` règle tous les compléments.

Consigner chaque version dans `docs/system3e/CHANGELOG.md`.

## Empaqueter une version

```bash
python tools/release.py system3e
```

- Écrit `dist/System3E-<version>.zip`.
- Le ZIP contient le dossier `System3E` exactement comme Fusion le veut.
- `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db` et `.DS_Store` sont laissés de côté.
- La compression est Deflate au niveau le plus élevé, pour que tout outil de décompression puisse le lire.
- Le ZIP est relu et testé après l'écriture.
- L'outil refuse d'empaqueter quand `VERSION` et le manifeste ne concordent pas.

Le ZIP est ensuite joint à une version sur <https://github.com/sorglos-it/fusion360/releases>. Ce téléversement ne
fait pas partie de l'outil.

Avant une version : lancer les deux tests, lancer `set_version.py --check`, mettre à jour le journal des
modifications et cette documentation.

## Ajouter ou modifier des textes

- `lang/en.xml` est la référence. Chaque autre fichier de langue doit avoir les mêmes clés et les mêmes espaces
  réservés.
- Une clé manquante dans une langue est fournie par l'anglais à l'exécution, mais `test_addin.py` la signale comme
  un échec.
- Les noms des champs de la boîte de dialogue, des familles (`family.<id>`), des ancrages (`anchor.<id>`) et des
  points (`point.<...>`) viennent tous de ces fichiers.
- Pour prendre en charge une langue de plus, l'ajouter à `SUPPORTED_LANGUAGES` et à `FUSION_LANGUAGE_MAP` dans
  `system3e_core.py` et ajouter le fichier de langue.

## Décisions et leurs raisons

Elles sont reprises des commentaires du code.

| Décision | Raison |
| --- | --- |
| Le module central est retiré de `sys.modules` avant l'import. | Fusion garde en cache les modules importés. Sans cela, une aide modifiée garderait son ancienne version jusqu'au redémarrage de Fusion. |
| Le module central a un nom à lui, `system3e_core`. | Sinon, deux compléments construits à partir du même modèle écraseraient chacun le module central de l'autre. |
| L'id de la commande a un préfixe à lui (`thwSystem3ECmd`). | Un id utilisé deux fois détourne sans bruit le bouton de l'autre complément. |
| Une définition de commande périmée est supprimée au démarrage. | Une définition laissée par une exécution précédente garderait son ancien libellé et son ancien gestionnaire. |
| Le panneau est cherché à partir d'une liste d'ids. | Les ids des panneaux changent d'une version de Fusion à l'autre. |
| Tous les gestionnaires d'événements sont conservés dans un registre. | Fusion ne tient qu'une référence faible. Un gestionnaire non conservé côté Python est supprimé et son événement cesse de se déclencher sans bruit. |
| Les gestionnaires sont attachés avant la reprise du point présélectionné. | Quoi qu'il échoue ensuite, la boîte de dialogue doit continuer à fonctionner. |
| La sélection faite avant l'appui sur le bouton est lue avant que les champs existent. | Pour que cliquer sur un point puis sur le bouton fonctionne tout simplement. |
| Toutes les valeurs de la boîte de dialogue sont lues dans une seule fonction. | L'exécution, l'aperçu et la validation regardent alors exactement les mêmes valeurs. |
| L'aperçu reste muet en cas d'erreur. | Il se déclenche à chaque frappe, aussi pour des valeurs à moitié saisies. À la place, la validation grise **OK**. |
| L'aperçu met `isValidResult` à false. | Fusion relance alors la véritable exécution pour le résultat final. |
| Les erreurs attendues sont un type d'erreur à part avec une clé indépendante de la langue. | La validation peut décider sans analyser de texte. Les erreurs inattendues sont affichées avec leur traceback. |
| Une exécution qui échoue met `executeFailed`. | Fusion annule alors ce qui avait été construit jusque-là, au lieu de laisser un composant vide. |
| Le même élément à nouveau est une autre occurrence du même composant. | Sinon une liste de pièces affiche « S1 WP », « S1 WP (1) », « S1 WP (2) » comme trois pièces au lieu d'une pièce trois fois. |
| Les composants sont retrouvés par un attribut, pas par le nom. | Renommer un composant ne fait alors aucun mal. Les éléments d'avant l'existence de l'attribut sont retrouvés par le nom. |
| Les composants d'une conception liée sont ignorés. | Ils ne peuvent pas être modifiés depuis la conception courante. |
| Le corps et les points vont dans une fonction de base dans les conceptions paramétriques. | Quand la chronologie est active, un corps tout prêt et un point à coordonnées simples doivent se trouver dans une fonction de base. |
| Le corps est nommé pendant que sa fonction de base est encore ouverte. | Indiqué dans le code ; la version 1.0.0.1 y a déplacé le nommage. |
| Seuls les points manquants sont ajoutés à un composant existant. | Les composants créés par une version plus ancienne n'en ont aucun ou en ont moins. |
| Le décalage est appliqué après la rotation. | Il suit les axes X, Y et Z de la conception, pas ceux de l'élément tourné. |
| Les champs de décalage affichent des mm, la valeur est en cm. | Le cm est l'unité propre à Fusion. |
| La version est lue dans le manifeste, pas écrite en dur. | La boîte de dialogue ne peut pas s'écarter du manifeste, et il n'y a qu'un seul endroit à incrémenter. |
| La version fait partie du nom de la commande. | Fusion utilise le nom de la commande comme titre de la boîte de dialogue ; c'est le seul endroit où une version est visible tant que la boîte de dialogue est ouverte. |
| Les membres de l'énumération des langues sont recherchés avec `getattr`. | Une valeur que cette version de Fusion ne connaît pas ne peut pas casser le complément. L'anglais est la solution de repli. |
| La bibliothèque enregistre des points et des faces planes, pas des fichiers Fusion. | Le fichier du fabricant contient des maillages de triangles mal raccordés (triangles qui se touchent sur une partie d'une arête, points en double, éclats). Fusion ne peut pas en faire un corps. |
| `S0/2 200 P` est reconstruit à partir de `S0/2 250 P`, abaissé de 50 mm. | Son maillage est endommagé au point d'être irréparable (ouvert d'un côté). Les éléments de départ ne diffèrent que par la hauteur du corps simple sous le profil supérieur. `check_lowering()` prouve la méthode sur une paire dont les deux maillages sont sains (`S0/2 250 W` et `S0/2 200 W`). |
| Les numéros de maillage sont associés aux noms par une table faite à la main. | Le fichier 3D ne contient aucun nom. La table a été faite en comparant chaque solide avec le dessin de sa fiche de catalogue. La longueur distingue les extrémités : 704 ou 352 mm, c'est « W » ; 3 mm de plus, c'est une languette (« P »). |
| Les éléments de cloison sont de simples boîtes. | Ils ne sont pas dans le fichier 3D ; leurs tailles viennent des fiches du catalogue. |
| Les coordonnées sont redressées à 0,1 mm. | La source contient du bruit de virgule flottante (106,4 à côté de 106,5 mm), ce qui laisse des faces légèrement pliées. |
| La hauteur d'empilement est 50 mm sous le sommet pour les éléments profilés. | Ils portent le rang suivant sur le fond entre les nervures ; les éléments plats le portent sur le dessus. |
| Les images d'aperçu sont dessinées avec un tampon de profondeur. | Les surfaces cachées sont éliminées pixel par pixel. Une méthode antérieure montrait des faces dans le mauvais ordre sur 16 images. |
| Les images d'aperçu sont dessinées à partir des solides. | Elles ne sont pas reprises du catalogue du fabricant. |

## Points ouverts

- Les noms gauche/droite des éléments d'angle et de fenêtre dans la table `NAMES` ont été comparés à l'œil avec
  les fiches du catalogue. Ils doivent encore être vérifiés par quelqu'un qui connaît le système.
- Les points, **Poser par** et les décalages ont besoin d'un test dans Fusion.

## Licence

MIT, Copyright (c) 2026 Sorglos Thomas Weirich. Voir [LICENSE](../LICENSE). Le complément n'est pas affilié à
SYSTEM 3E.
