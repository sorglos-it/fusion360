# Développement

## Dossiers

| Chemin | Contenu |
| --- | --- |
| `apps/desktop-template/AddInTemplate/` | Le complément modèle, tel que Fusion en a besoin |
| `apps/desktop-template/AddInTemplate/AddInTemplate.py` | Fichier d'entrée |
| `apps/desktop-template/AddInTemplate/addin_core.py` | Module central |
| `apps/desktop-template/AddInTemplate/AddInTemplate.manifest` | Manifeste |
| `apps/desktop-template/AddInTemplate/lang/` | `de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` |
| `apps/desktop-template/AddInTemplate/resources/AddInTemplate/` | Icônes `16x16.png`, `32x32.png`, `64x64.png` |
| `apps/desktop-template/VERSION` | Numéro de version de cette partie |
| `apps/desktop-template/tests/test_addin.py` | Contrôle hors ligne |
| `tools/template/new_addin.py` | Script de génération, voir [installation.md](installation.md) |
| `tools/template/make_icon.py` | Outil d'icône |
| `tools/template/test_addin.py` | Renvoie au contrôle hors ligne (ancien chemin) |
| `tools/set_version.py` | Règle les numéros de version, pour tous les compléments du dépôt |
| `tools/release.py` | Empaquette un complément dans un ZIP, pour tous les compléments du dépôt |
| `docs/template/` | README, CHANGELOG, LICENSE et cette documentation |
| `dist/` | Fichiers ZIP empaquetés. Pas dans Git |

Il n'y a pas d'étape de construction. Le complément tourne tel quel. Tous les outils utilisent seulement la bibliothèque standard de Python.

## Contrôle hors ligne

Le contrôle teste un complément sans démarrer Fusion. Le commentaire du code l'appelle la seule boucle de retour qui ne demande aucun redémarrage.

```bash
python apps/desktop-template/tests/test_addin.py                    # the template itself
python apps/desktop-template/tests/test_addin.py --path ../MyAddIn  # an add-in next to the repository
```

| Option | Valeur par défaut | Effet |
| --- | --- | --- |
| `--addin NAME` | `AddInTemplate` | Nom du dossier dans `apps/desktop-template` de ce dépôt |
| `--path DIR` | – | Chemin complet vers un dossier de complément. L'emporte sur `--addin` |

Pour un complément créé avec `--install`, donner à `--path` son dossier dans le dossier des compléments de Fusion.

L'ancienne commande `python tools/template/test_addin.py` fonctionne toujours. Elle renvoie au contrôle avec les mêmes arguments, la même sortie et le même code de sortie.

### Comment il fonctionne

Il met en place des substituts vides pour les modules `adsk`, `adsk.core` et `adsk.fusion`, puis importe le complément.
Seules les classes de base des gestionnaires sont de vraies classes (vides). Le contrôle prouve donc que le fichier s'importe et que les textes sont en ordre. Il n'exécute **aucun** appel à Fusion : pas de boîte de dialogue, pas de géométrie, pas de `run()`.

### Ce qu'il vérifie

| Section | Contrôles |
| --- | --- |
| 1) Layout | Le dossier existe. `<name>.py` et `<name>.manifest` correspondent au nom du dossier. `lang/` existe |
| 2) Manifest | JSON valide. `type` vaut `addin`. `autodeskProduct` vaut `Fusion360`. `id` ressemble à un GUID. Avertissements : GUID provisoire, auteur `Your Name` |
| 3) Import | Le complément s'importe. `run` et `stop` existent. `CMD_ID` est défini. `_CORE_MODULE` a un fichier correspondant. Avertissements : `CMD_ID` encore à la valeur du modèle, module central non renommé |
| 4) Language files | `SUPPORTED_LANGUAGES` est disponible. `en.xml` existe et a des clés. Pour chaque langue prise en charge : le fichier existe, déclare la bonne `language`, a toutes les clés, n'a aucune clé inconnue, garde chaque espace réservé, n'a aucun texte vide |
| 5) Text catalogue | Chaque langue se charge et renvoie un `cmd.name`. Une langue inconnue se rabat sur l'anglais. Une clé manquante renvoie la clé. Avertissement : l'info-bulle dit encore `TODO` |
| 6) Icons | `resources/<name>/` existe. Les trois fichiers PNG existent et commencent par la signature PNG |

### Résultat

- Les lignes commencent par `ok`, `FAIL` ou `warn`.
- Avec au moins un `FAIL`, le script se termine avec le code de sortie 1 et affiche le nombre d'échecs.
- Les avertissements ne changent pas le code de sortie.
- Sans échec, il affiche `all checks passed`.

Lancé pour cette documentation sur le modèle, version 1.0.0.0 : `3 warning(s)`, `all checks passed`. Les trois avertissements (GUID provisoire, auteur, id de la commande) sont normaux pour le modèle.

## Outil d'icône

Fusion veut trois fichiers PNG avec transparence : 16x16, 32x32 et 64x64 pixels, dans le dossier transmis à la définition du bouton.

```bash
python tools/template/make_icon.py                            # the template's placeholder
python tools/template/make_icon.py --root .. --addin MyAddIn  # an add-in next to the repository
```

| Option | Valeur par défaut | Effet |
| --- | --- | --- |
| `--addin NAME` | `AddInTemplate` | Nom du dossier du complément |
| `--root DIR` | `apps/desktop-template` de ce dépôt | Dossier qui contient le complément |

Les fichiers sont écrits dans `<root>/<addin>/resources/<addin>/`. Le dossier est créé si nécessaire. Les icônes existantes sont écrasées.

Pour dessiner sa propre icône, modifier le script :

| Nom | Signification |
| --- | --- |
| `SHAPES` | Liste de `(colour, polygon)`. Les points vont de 0 à 1, avec y dirigé **vers le haut**. Là où des formes se chevauchent, celle qui est listée en premier reste au-dessus |
| `DARK`, `ACCENT` | Les deux couleurs sous forme de valeurs RVB |
| `SS` | Échantillons par côté de pixel pour des bords lisses. 4 donne des bords nets jusqu'à 16 px |

L'icône provisoire montre quatre crochets d'angle et une diagonale. Elle ressemble volontairement à une icône provisoire. La remplacer avant de transmettre son complément à d'autres.

## Numéros de version

Les versions ont quatre parties : `v.x.y.z` (version, release, feature, build). Actuelle : `1.0.0.0`.

Le numéro est tenu à deux endroits :

- `apps/desktop-template/VERSION`
- le champ `version` du manifeste – c'est celui-ci que lisent Fusion et le titre de la boîte de dialogue

Ne jamais les modifier à la main. Utiliser l'outil, il écrit les deux :

```bash
python tools/set_version.py template 1.0.0.1   # this part
python tools/set_version.py all 1.0.0.0        # every add-in of the repository
python tools/set_version.py --check            # report differences
```

- `template` est le nom du dossier `apps/desktop-template` sans `desktop-`.
- `--check` affiche une ligne par complément, terminée par `ok` ou `DIFFERENT OR NOT v.x.y.z`, et renvoie le code de sortie 1 si une ligne est fausse.
- L'outil ne travaille que sur les compléments de ce dépôt. Dans un complément personnel hors du dépôt, modifier directement le champ `version` de son manifeste – c'est le seul endroit dans ce cas.

## Empaquetage

```bash
python tools/release.py template
python tools/release.py all
```

- Écrit `dist/AddInTemplate-<version>.zip`.
- Le ZIP contient le dossier `AddInTemplate` comme Fusion le veut. Le décompresser dans le dossier des compléments de Fusion.
- Laissés de côté : `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compression : Deflate au niveau le plus élevé, pour que tout outil de décompression puisse le lire.
- Il refuse d'empaqueter si `VERSION` et le manifeste diffèrent ou si le numéro n'a pas quatre parties.
- Après l'empaquetage, il teste le ZIP et affiche le nombre de fichiers et la taille.
- Les outils (`tools/`) ne sont pas dans le ZIP. Ils n'existent que dans le dépôt.

Aucun ZIP de la version 1.0.0.0 n'a été publié. Le modèle s'utilise depuis le dépôt.

## Décisions et leurs raisons

| Décision | Raison donnée dans le code |
| --- | --- |
| Le fichier d'entrée et le module central sont séparés | Le module central contient ce dont chaque complément a besoin et où l'on se trompe facilement. Le code personnel reste entre deux repères |
| Le module central est renommé pour chaque complément | Deux compléments issus de ce modèle ne doivent pas écraser chacun le module central de l'autre dans `sys.modules` |
| Le module central est retiré de `sys.modules` avant l'import | Fusion garde les modules en cache. De cette façon, « arrêter, relancer » prend en compte les modifications |
| Tous les gestionnaires passent par `HandlerRegistry` | Fusion tient les gestionnaires faiblement. Ceux qui ne sont plus référencés sont supprimés et l'événement cesse de se déclencher sans bruit |
| `PANEL_IDS` est une liste, avec une recherche globale comme second essai | Les ids des panneaux changent d'une version de Fusion à l'autre |
| Une définition de commande périmée est supprimée au démarrage | Elle garderait son ancien libellé et son ancien gestionnaire |
| `read_inputs()` est le seul endroit qui lit la boîte de dialogue | L'exécution, l'aperçu et la validation regardent exactement les mêmes nombres |
| `validate()` s'exécute avant le tracé et à nouveau pour le bouton OK | Une saisie impossible désactive OK au lieu d'échouer à mi-chemin |
| L'aperçu avale les erreurs | Il se déclenche à chaque frappe, aussi pour des valeurs à moitié saisies |
| L'aperçu met `isValidResult` à `False` | Fusion lance alors l'exécution pour le résultat réel |
| Les erreurs portent une clé, pas seulement un texte | La raison est connue sans analyser un texte dans une langue quelconque |
| `report()` est réservé aux erreurs inattendues | Ce que l'utilisateur peut corriger doit être une `AddInError`, pour que OK soit bloqué au lieu qu'une boîte de dialogue surgisse |
| L'anglais est la solution de repli pour chaque texte | Une traduction à moitié finie affiche de l'anglais au lieu de clés brutes |
| Les valeurs de langue de Fusion sont recherchées par leur nom | Une valeur que cette version de Fusion ne connaît pas ne peut pas casser le complément |
| La détection de la langue ne lève jamais d'erreur | Une version de Fusion avec une valeur inattendue démarre quand même le complément |
| La version est lue dans le manifeste | La boîte de dialogue ne peut pas s'écarter du manifeste. Un seul endroit où l'augmenter |
| La version fait partie du nom de la commande | Fusion utilise ce nom comme titre de la boîte de dialogue. C'est le seul endroit où une version est visible tant que la boîte de dialogue est ouverte. Elle apparaît aussi sur le bouton – il n'y a que ce seul nom |
| `isComputeDeferred` est remis à sa valeur dans `finally` | Sinon, après une erreur, l'esquisse cesserait de se mettre à jour |
| La sélection est lue avant que les champs existent | « Cliquer sur une ligne, puis appuyer sur le bouton » fonctionne |
| L'icône provisoire ressemble à une icône provisoire | Une icône qui n'a pas été remplacée se repère facilement |
| Le script écrit les fichiers avec des fins de ligne `\n` et en UTF-8 | Non expliqué dans le code |
| Les clés, les identifiants et les commentaires sont en anglais | Non expliqué dans le code ; le README existant dit qu'un traducteur n'a ainsi jamais à ouvrir un fichier `.py` |

## Licence

MIT. Auteur : Sorglos Thomas Weirich. Voir [LICENSE](../LICENSE).
