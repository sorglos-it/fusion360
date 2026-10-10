# Fonctionnement

## Deux fichiers

| Fichier | Rôle |
| --- | --- |
| Fichier d'entrée `AddInTemplate.py` (plus tard `<name>.py`) | Ce que Fusion démarre. Contient les réglages, les fonctions personnelles, les gestionnaires d'événements, `run` et `stop` |
| Module central `addin_core.py` (plus tard `<name>_core.py`) | Les parties dont chaque complément a besoin et où l'on se trompe facilement. Rien de ce qu'il contient n'appartient à un complément en particulier |

Fusion trouve un complément par son nom : le dossier, le fichier `.py` et le fichier `.manifest` doivent porter le même nom.

## Ce que contient le module central

| Partie | Tâche |
| --- | --- |
| `Strings` | Catalogue de textes lu dans `lang/<code>.xml`, avec l'anglais comme solution de repli |
| `detect_language()` | Trouve la langue sur laquelle Fusion est réglé |
| `AddInError` | Type d'erreur pour les échecs que l'utilisateur peut corriger. Porte une clé qui ne dépend pas de la langue |
| `HandlerRegistry` | Garde les gestionnaires d'événements en vie |
| `find_panel()` | Trouve, dans une liste, le premier panneau de barre d'outils qui existe |
| `add_button()` | Place la commande sur un panneau. Supprime d'abord un contrôle resté d'un rechargement |
| `remove_button()` | Retire de la barre d'outils le contrôle et la définition de commande |
| `report()` | Affiche une erreur inattendue avec son traceback dans une boîte de message |
| `read_version()` | Lit la version dans le manifeste |
| `display_name()` | Réunit le nom et la version : `Name (1.0.0.0)` |
| `FALLBACK_LANGUAGE`, `SUPPORTED_LANGUAGES`, `FUSION_LANGUAGE_MAP` | Les tables de langues |

## Pourquoi le module central est renommé pour chaque complément

Tous les compléments tournent dans le même Python à l'intérieur de Fusion. Ils partagent une seule liste de modules chargés (`sys.modules`).
Si deux compléments chargeaient tous deux un module appelé `addin_core`, chacun écraserait le module central de l'autre.

Le script renomme donc le fichier en `<name in lower case>_core.py` et règle `_CORE_MODULE` dans le fichier d'entrée en conséquence.

Conséquence : chaque complément a sa **propre copie** du module central. Une correction faite plus tard dans le modèle n'atteint pas les compléments créés auparavant. Elle doit être copiée à la main.

## Chargement du module central

Le fichier d'entrée fait ceci avant toute autre chose :

1. Il ajoute son propre dossier au chemin de recherche de Python.
2. Il retire le module central de `sys.modules`, s'il s'y trouve.
3. Il importe le module central par le nom indiqué dans `_CORE_MODULE`.

Raison de l'étape 2 : Fusion garde en cache les modules importés. Sans elle, un module central modifié garderait son ancienne version jusqu'au redémarrage de Fusion. Avec elle, il suffit d'arrêter et de relancer le complément.

## Registre des gestionnaires

Fusion ne garde qu'une référence faible vers un gestionnaire d'événements. Un gestionnaire auquel Python ne fait plus référence est supprimé, et son événement cesse de se déclencher – sans aucun message d'erreur. Le commentaire du code appelle cela la façon la plus courante pour un complément de ne fonctionner qu'à moitié.

`HandlerRegistry.add(event, handler)` relie le gestionnaire à l'événement **et** le range dans une liste. `clear()` vide la liste quand le complément s'arrête.

## Démarrage et arrêt

### `run(context)`

1. Charge la langue détectée dans le catalogue de textes.
2. Supprime une définition de commande portant le même `CMD_ID`, restée d'une exécution précédente. Elle garderait son ancien libellé et son ancien gestionnaire.
3. Crée la définition du bouton : nom avec version, info-bulle, dossier d'icônes (s'il existe).
4. Relie `CommandCreatedHandler`.
5. Cherche un panneau. Si aucun n'est trouvé, il affiche « Aucun panneau de barre d'outils approprié n'a été trouvé. » et s'arrête là.
6. Ajoute le bouton au panneau.

Toute autre erreur est affichée sous la forme « Échec du démarrage : » avec le traceback.

### `stop(context)`

1. Retire le contrôle du panneau et supprime la définition de commande.
2. Vide le registre des gestionnaires.

Une erreur est affichée sous la forme « Échec de l'arrêt : » avec le traceback.

## Déroulement des événements

```
button pressed
   -> commandCreated   build the dialog, connect the four handlers below
        -> inputChanged     a field changed        -> on_input_changed()
        -> validateInputs   may OK be pressed?     -> read_inputs(), validate()
        -> executePreview   show a preview         -> read_inputs(), validate(), build_result()
        -> execute          OK pressed             -> read_inputs(), validate(), build_result(), remember()
```

| Événement | Gestionnaire | Ce qu'il fait | En cas d'erreur |
| --- | --- | --- | --- |
| création | `CommandCreatedHandler` | Marque la commande comme répétable. Recueille les lignes d'esquisse sélectionnées avant l'appui sur le bouton. Appelle `build_inputs()`. Place la première ligne recueillie dans le champ de sélection si celui-ci est encore vide. Relie les quatre autres gestionnaires | Boîte de message « Erreur lors de la construction de la boîte de dialogue : » avec traceback |
| champ modifié | `InputChangedHandler` | Appelle `on_input_changed()`. Ne fait rien tant que `_updating` est activé | muet |
| validation | `ValidateHandler` | Appelle `read_inputs()` et `validate()`. Met `areInputsValid` à vrai, ou à faux à la moindre erreur | OK est grisé, pas de message |
| aperçu | `PreviewHandler` | Exécute la commande entière. Met ensuite `isValidResult` à `False`, pour que Fusion rejette l'aperçu et lance l'exécution pour le résultat réel | muet, pas d'aperçu |
| exécution | `ExecuteHandler` | Exécute la commande entière, puis `remember()` | `AddInError` : boîte de message avec le texte traduit. Tout le reste : « Erreur lors de la création de la géométrie : » avec traceback |

« Exécute la commande entière » désigne `_run_command()` : `read_inputs()`, puis `validate()`, puis `build_result()`.

Points qui en découlent :

- La sélection est lue **avant** la création des champs, et remise ensuite au champ de sélection. C'est pourquoi « cliquer sur une ligne, puis appuyer sur le bouton » fonctionne.
- L'aperçu se déclenche à chaque frappe et voit des valeurs à moitié saisies. Il reste donc volontairement muet en cas d'erreur.
- Ni l'aperçu ni la validation ne disent à l'utilisateur **pourquoi** quelque chose ne va pas. Seule l'exécution affiche un texte.
- `build_result()` s'exécute deux fois pour un seul OK : une fois ou plus pour l'aperçu, une fois pour le résultat réel.
- Ne mettre `isValidResult` à `True` que si l'aperçu a déjà produit le résultat final.

## Deux sortes d'erreurs

| Sorte | Comment elle est levée | Ce que voit l'utilisateur |
| --- | --- | --- |
| Attendue – l'utilisateur peut la corriger | `fail('err.key')` lève `AddInError` | OK grisé ; une boîte de message avec le texte traduit seulement à l'exécution |
| Inattendue – un bogue | toute autre exception | Une boîte de message avec le traceback, par `core.report()` |

`AddInError` conserve la clé (`err.key`) et les paramètres (`err.params`). Le texte est recherché au moment où l'erreur est créée.
Le code du modèle lui-même ne lit pas la clé par la suite ; elle est là pour le code personnel.

## Catalogue de textes et solution de repli

`S = core.Strings(LANG_DIR)` est créé à l'import du fichier d'entrée. L'anglais est chargé aussitôt ; des textes existent donc même avant `run()`.
`run()` charge ensuite la langue détectée.

Comment fonctionne `load(code)` :

1. Un code qui n'est pas dans `SUPPORTED_LANGUAGES` devient `en`.
2. `en.xml` est lu une seule fois et gardé comme solution de repli.
3. Le fichier de la langue choisie est lu comme jeu courant.

Comment un texte est trouvé (`get(key, *args)`) :

1. le texte de la langue courante, s'il existe et n'est pas vide
2. sinon le texte anglais
3. sinon la clé elle-même, par exemple `in.width`

Les espaces réservés sont ensuite remplis. Si le remplissage échoue – par exemple une traduction demande `{1}` alors qu'une seule valeur a été donnée – le texte est renvoyé non rempli au lieu de lever une erreur.

Un fichier de langue manquant ou qui n'est pas du XML valide compte comme vide. Tous les textes viennent alors de l'anglais.
Si `en.xml` manque ou est abîmé lui aussi, ce sont les clés elles-mêmes qui sont affichées.

## Détection de la langue

Voir [settings.md](settings.md) pour l'ordre. Deux détails tirés du code :

- Les valeurs de langue de Fusion sont recherchées par leur nom avec `getattr`. Une valeur que cette version de Fusion ne connaît pas ne peut pas casser le complément.
- La fonction ne lève jamais d'erreur. Dans le pire des cas, elle renvoie l'anglais.

## Unités

En interne, Fusion compte les longueurs en cm. La démonstration le montre :

- la valeur de départ `1.0` est affichée comme 10 mm
- la valeur lue dans le champ de longueur est en cm
- pour le message « La longueur dépasse la ligne sélectionnée ({0} mm). », la longueur de la ligne est multipliée par 10 et affichée avec deux décimales

## Données

Le complément lit son manifeste et ses fichiers de langue. Il n'écrit aucun fichier.
