# Dépannage

Les textes ci-dessous sont les textes français de `lang/fr.xml`. Dans une autre langue, le complément affiche la traduction.
Chaque boîte de message a le nom de la commande pour titre.

## Messages de la commande de démonstration

Ces quatre messages viennent de `validate()`. Tant que l'un d'eux s'applique, **OK** est grisé et aucun aperçu n'est affiché – sans aucun texte.
Le texte lui-même n'apparaît sous forme de boîte de message que si l'erreur se produit au moment où la commande est exécutée.

| Message | Cause | Que faire |
| --- | --- | --- |
| « Sélectionnez exactement une ligne d'esquisse. » | Le champ **Ligne** est vide, ou l'objet sélectionné n'est pas une ligne d'esquisse | Choisir une seule ligne d'esquisse droite |
| « La longueur doit être supérieure à 0. » | **Longueur** vaut 0 ou est négative | Saisir une longueur supérieure à 0 |
| « La ligne sélectionnée n'a aucune longueur. » | Le point de départ et le point d'arrivée de la ligne sont au même endroit (seuls X et Y sont comparés) | Choisir une autre ligne |
| « La longueur dépasse la ligne sélectionnée ({0} mm). » | **Longueur** est plus grande que la ligne sélectionnée. `{0}` est la longueur de la ligne en mm avec deux décimales | Saisir une longueur allant jusqu'à cette valeur, ou choisir une ligne plus longue |

## Messages du complément lui-même

Les quatre messages avec `{0}` affichent un traceback Python à la place de `{0}`. Le traceback nomme le fichier et la ligne de l'erreur.

| Message | Quand | Cause | Que faire |
| --- | --- | --- | --- |
| « Aucun panneau de barre d'outils approprié n'a été trouvé. » | au démarrage | Aucun des ids de `PANEL_IDS` n'existe, ni dans l'espace de travail `WORKSPACE_ID` ni ailleurs dans Fusion. Le complément tourne mais n'a pas de bouton | Mettre dans `PANEL_IDS` des ids de panneaux qui existent dans la version de Fusion utilisée. Voir [settings.md](settings.md) |
| « Erreur lors de la création de la géométrie : {0} » | après OK | Une erreur inattendue dans `read_inputs()`, `validate()`, `build_result()` ou `remember()` – un bogue, pas une mauvaise saisie | Lire les dernières lignes du traceback et corriger le code. Si l'utilisateur peut la provoquer, intercepter le cas dans `validate()` avec `fail('err.key')` |
| « Erreur lors de la construction de la boîte de dialogue : {0} » | à l'appui sur le bouton | Une erreur inattendue dans `build_inputs()` ou pendant la liaison des gestionnaires | Lire le traceback. Typique : le même id de champ utilisé deux fois, ou un mauvais texte d'unité |
| « Échec du démarrage : {0} » | au démarrage du complément | Une erreur inattendue dans `run()` | Lire le traceback |
| « Échec de l'arrêt : {0} » | à l'arrêt du complément | Une erreur inattendue dans `stop()` | Lire le traceback. Redémarrer Fusion si le bouton reste sur la barre d'outils |

Les causes « typiques » de ce tableau sont des exemples. Elles n'ont pas été reproduites dans Fusion pour cette documentation.

## Messages du script de génération

| Message | Cause | Que faire |
| --- | --- | --- |
| `The name must start with a letter and contain only letters and digits - it becomes a Python module name. Got: '…'` | Le nom contient un espace, un trait d'union, un tiret bas, un autre signe, ou commence par un chiffre | Utiliser un nom tel que `MyAddIn` |
| `Pick a name other than AddInTemplate.` | Le nom est celui du modèle lui-même | Choisir un autre nom |
| `Template folder not found: …` | `apps/desktop-template/AddInTemplate` manque. Le script a été déplacé, ou le dépôt est incomplet | Lancer le script depuis une copie complète du dépôt |
| `… already exists. Pass --force to overwrite it.` | Le dossier cible existe | Choisir un autre nom ou un autre dossier. `--force` supprime le dossier existant avec tout ce qu'il contient |
| `Use either --install or --out, not both.` | Les deux options ont été données | Utiliser l'une des deux |

Sur un système qui n'est pas macOS, `--install` construit le chemin à partir de la variable d'environnement `APPDATA`. Si elle n'est pas définie (par exemple sous Linux), le dossier est créé par rapport au dossier courant. Utiliser `--out` dans ce cas.

## Messages des outils de version et d'empaquetage

| Message | Cause | Que faire |
| --- | --- | --- |
| `The version needs four numbers, like 1.0.0.0 - got '…'` | La version n'a pas quatre parties | Utiliser `v.x.y.z`, par exemple `1.0.0.1` |
| `No add-in "…". There are: …` | Le nom n'est pas un dossier `apps/desktop-<name>` avec exactement un manifeste | Utiliser un nom de la liste. Le modèle s'appelle `template` |
| `No "version" entry in …` | Le manifeste n'a pas de champ `version` | Ajouter le champ au manifeste |
| `DIFFERENT OR NOT v.x.y.z` (de `--check`) | `VERSION` et le manifeste diffèrent, ou le numéro n'a pas quatre parties | Lancer `python tools/set_version.py template <version>` |
| `template: VERSION and manifest disagree - run tools/set_version.py first.` | Comme ci-dessus, remarqué pendant l'empaquetage | Comme ci-dessus, puis empaqueter à nouveau |
| `template: … is damaged in the ZIP` | Le test du ZIP après l'empaquetage a échoué | Empaqueter à nouveau ; vérifier le disque |

## Contrôle hors ligne : FAIL et warn

Le contrôle est décrit dans [development.md](development.md). Une ligne `FAIL` nomme ce qui ne va pas. Les lignes `warn` ne font pas échouer le contrôle.

| Avertissement | Signification |
| --- | --- |
| `id is not the placeholder GUID` | Le manifeste a encore les zéros comme `id` |
| `author has been filled in` | L'auteur est encore `Your Name` |
| `CMD_ID is no longer the template default` | `CMD_ID` vaut encore `thwAddInTemplateCmd` |
| `the core module was renamed, so it cannot clash with another add-in` | Un complément autre que le modèle utilise encore `addin_core` |
| `cmd.tooltip no longer says TODO` | L'info-bulle anglaise contient encore `TODO` |

Pour le modèle lui-même, les trois premiers avertissements sont normaux.

## Pièges

Ils viennent des commentaires du code.

| Symptôme | Cause | Que faire |
| --- | --- | --- |
| Une modification du code n'a aucun effet | Fusion garde en cache les modules importés. Un module modifié garde son ancienne version jusqu'au redémarrage de Fusion | Arrêter le complément et le relancer. Cela fonctionne pour le module central, car le fichier d'entrée le retire de `sys.modules` avant de l'importer. Appliquer le même traitement à chaque autre module personnel |
| Le bouton d'un autre complément fait quelque chose d'étrange, ou le sien | Deux compléments utilisent le même `CMD_ID`. La collision est silencieuse | Utiliser son propre préfixe et un id unique |
| Deux compléments issus du modèle se gênent | Les deux utilisent un module central du même nom | Garder le module central renommé `<name>_core.py` |
| Un événement cesse de se déclencher, sans erreur | Fusion ne tient les gestionnaires que faiblement. Un gestionnaire auquel Python ne fait plus référence est supprimé | Relier chaque gestionnaire avec `_handlers.add(event, handler)` |
| Le bouton garde un ancien libellé ou un ancien comportement | Une définition de commande d'une exécution précédente est encore là | `run()` la supprime d'abord. Garder ce code |
| OK est gris et personne ne sait pourquoi | La validation et l'aperçu n'affichent pas de raison | C'est voulu. Garder des règles simples et les nommer dans l'info-bulle ou dans les libellés |
| L'aperçu ne montre rien | L'aperçu avale toutes les erreurs, même les vrais bogues | Appuyer sur OK avec des saisies valides. L'exécution affiche l'erreur avec le traceback |
| Un message surgit à chaque frappe | L'affichage des erreurs a été déplacé dans l'aperçu | Laisser l'aperçu muet. Il se déclenche à chaque frappe, aussi pour des valeurs à moitié saisies |
| Les valeurs sont dix fois trop grandes ou trop petites | Fusion compte en cm, quoi que le champ affiche. `createByReal(1.0)` affiché en `mm` donne 10 mm | Calculer en cm. Ne multiplier par 10 que pour l'affichage en mm |
| L'esquisse ne se met plus à jour après une erreur | `isComputeDeferred` a été mis à `True` et jamais remis à sa valeur | Le remettre à sa valeur dans un bloc `finally`, comme le fait `build_result()` |
| `on_input_changed()` s'exécute sans fin ou deux fois | Une valeur qui y est réécrite déclenche à nouveau l'événement | Mettre `_updating` à `True` avant l'écriture et à `False` après. C'est une variable de module : déclarer `global _updating` dans la fonction |
| Le bouton manque après une mise à jour de Fusion | Les ids des panneaux changent d'une version de Fusion à l'autre | Indiquer plusieurs ids dans `PANEL_IDS`, le préféré en premier |
| Le bouton n'a pas d'icône | Le dossier `resources/<name>` manque. Le complément ne transmet alors aucun dossier d'icônes | Créer les icônes, voir [development.md](development.md) |
| Un texte affiche une clé telle que `in.width` | La clé manque dans le fichier de langue **et** dans `en.xml` | Ajouter la clé à `en.xml` |
| Un texte affiche `{0}` au lieu d'une valeur | Les espaces réservés du texte ne correspondent pas aux valeurs données | Comparer le texte avec l'appel `T('key', value)` |
| Tous les textes sont en anglais | La langue n'est pas dans `SUPPORTED_LANGUAGES`, ou son fichier manque ou n'est pas du XML valide | Vérifier le fichier et les tables dans le module central |
| Une correction du modèle n'apparaît pas dans mon complément | Chaque complément a sa propre copie du module central | Copier la correction à la main dans `<name>_core.py` |
| Fusion ne liste pas le complément | Le dossier, le `.py` et le `.manifest` ne portent pas le même nom | Donner le même nom aux trois. Le contrôle hors ligne le vérifie |
