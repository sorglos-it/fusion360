# Utilisation

## La commande de démonstration

La commande de démonstration trace une courte ligne (un « trait ») au milieu d'une ligne d'esquisse. Le trait est à angle droit par rapport à cette ligne.
Son seul rôle est de montrer que la sélection, l'aperçu, les contrôles et la traduction fonctionnent. La remplacer par sa propre commande.

Dans le modèle non modifié, la commande s'appelle **Modèle de complément**. Son info-bulle dit :

> Point de départ pour un complément Fusion 360.
> Trace un trait au milieu de la ligne sélectionnée.

### La boîte de dialogue

| Champ | Type | Signification | Valeur de départ |
| --- | --- | --- | --- |
| **Ligne** | sélection, invite « Sélectionner une ligne d'esquisse » | La ligne d'esquisse qui reçoit le trait. Exactement une ligne. Seules des lignes d'esquisse peuvent être choisies | vide, ou la ligne qui était sélectionnée auparavant |
| **Longueur** | valeur en mm | Longueur du trait. Accepte des expressions telles que `2 * 3 mm` | 10 mm |
| **Inverser la direction** | case à cocher | Trace le trait de l'autre côté de la ligne | désactivé |

### Essayer

1. Ouvrir une esquisse et tracer une ligne.
2. Cliquer sur la ligne.
3. Appuyer sur le bouton **Modèle de complément**. La ligne est déjà inscrite dans **Ligne**.
4. Saisir une **Longueur**. L'aperçu montre le trait aussitôt.
5. Cocher **Inverser la direction** pour tourner le trait de l'autre côté.
6. Appuyer sur **OK**.

Il est aussi possible d'appuyer d'abord sur le bouton et de choisir la ligne ensuite.

### Règles vérifiées par la commande

| Règle | Message quand elle n'est pas respectée |
| --- | --- |
| Exactement une ligne d'esquisse est sélectionnée | « Sélectionnez exactement une ligne d'esquisse. » |
| La longueur est supérieure à 0 | « La longueur doit être supérieure à 0. » |
| La ligne sélectionnée est plus longue que 0 | « La ligne sélectionnée n'a aucune longueur. » |
| Le trait n'est pas plus long que la ligne sélectionnée | « La longueur dépasse la ligne sélectionnée ({0} mm). » |

Tant qu'une règle n'est pas respectée, **OK** est grisé et l'aperçu reste vide. La boîte de dialogue ne dit **pas** pourquoi.
Le texte du message n'apparaît sous forme de boîte de message que si l'erreur se produit à l'exécution de la commande.

### Autres comportements

- **Longueur** et **Inverser la direction** sont mémorisés pour l'appel suivant. Ils sont oubliés quand Fusion se ferme ou que le complément est redémarré.
- La commande est répétable (`isRepeatable` est activé) ; la fonction « répéter la dernière commande » de Fusion peut donc la relancer.
- Détails de la géométrie : seules les valeurs X et Y des extrémités de la ligne dans l'esquisse sont utilisées. Le trait est tracé à Z = 0 de l'esquisse.

Le comportement dans Fusion est décrit d'après le code. Il n'a pas été testé dans Fusion pour cette documentation.

## En faire son propre complément

Créer d'abord une copie avec le script, voir [installation.md](installation.md). Travailler ensuite dans `<name>.py`.

Le fichier d'entrée a trois zones :

| Zone | Contenu | À modifier ? |
| --- | --- | --- |
| au-dessus de `CONFIGURE` | charge le module central | seulement pour ajouter d'autres modules personnels |
| de `CONFIGURE` à `END OF TEMPLATE` | les réglages et les fonctions personnelles | **oui – c'est la zone personnelle** |
| en dessous de `END OF TEMPLATE` | les gestionnaires d'événements, `run` et `stop` | normalement non |

### Pas à pas

1. **Régler les ids.** Vérifier `CMD_ID`, `WORKSPACE_ID` et `PANEL_IDS`. Voir [settings.md](settings.md).
2. **Nommer les champs.** Remplacer `IN_LINE`, `IN_LENGTH`, `IN_FLIP` par des ids pour ses propres champs.
3. **Régler les valeurs de départ.** Mettre dans `_last` la valeur de départ de chaque champ mémorisé. Les longueurs sont en cm.
4. **Construire la boîte de dialogue** dans `build_inputs(inputs)`.
5. **Lire la boîte de dialogue** dans `read_inputs(inputs)`.
6. **Vérifier les valeurs** dans `validate(values)`.
7. **Faire le travail** dans `build_result(values)`.
8. **Mémoriser les valeurs** dans `remember(values)`.
9. **Réagir aux modifications** dans `on_input_changed(inputs, changed)`, si un champ doit en modifier un autre.
10. **Écrire les textes.** Ajouter ses clés à `lang/en.xml`, puis traduire les autres fichiers. Remplacer l'info-bulle `TODO`.
11. **Adapter la présélection.** `CommandCreatedHandler` (en dessous de `END OF TEMPLATE`) recueille les lignes d'esquisse sélectionnées avant l'appui sur le bouton. Si la commande a besoin d'un autre genre d'objet, y modifier le test de type, ou supprimer le bloc.
12. **Dessiner une icône**, voir [development.md](development.md).
13. **Remplir le manifeste** : description, auteur, version. Voir [settings.md](settings.md).
14. **Lancer le contrôle hors ligne**, voir [development.md](development.md).
15. **Essayer dans Fusion.** Après chaque modification, arrêter le complément et le relancer.

### Les fonctions à modifier

| Fonction | À quoi elle sert | Règles |
| --- | --- | --- |
| `build_inputs(inputs)` | Met en place la boîte de dialogue. Chaque libellé vient du catalogue de textes par `T('key')` | Renvoie le champ de sélection. L'appelant y place la ligne présélectionnée. Renvoyer `None` s'il n'y a pas de champ de sélection |
| `read_inputs(inputs)` | Lit chaque valeur de la boîte de dialogue à un seul endroit et renvoie un `dict` | L'exécution, l'aperçu et la validation l'appellent tous ; ils voient donc les mêmes nombres |
| `validate(values)` | S'arrête avec `fail('err.key')` pour tout ce que l'utilisateur doit corriger | Elle s'exécute avant le tracé et à nouveau pour le bouton OK. Une saisie impossible grise OK au lieu d'échouer à mi-chemin |
| `build_result(values)` | Fait le travail proprement dit | Tout est déjà vérifié quand elle s'exécute. Elle s'exécute pour l'aperçu **et** pour le résultat réel |
| `remember(values)` | Copie les valeurs dans `_last` pour l'appel suivant | Appelée seulement après une exécution réussie |
| `on_input_changed(inputs, changed)` | Active, désactive ou ajuste un champ à partir d'un autre | Vide dans le modèle. Activer `_updating` autour de chaque valeur réécrite, sinon l'écriture appelle à nouveau cette fonction |

### Les aides à appeler

| Aide | Ce qu'elle fait |
| --- | --- |
| `T(key, *args)` | Renvoie le texte de `key` dans la langue active. `args` remplissent `{0}`, `{1}`, … |
| `fail(key, *args)` | Lève une `AddInError` avec le texte de `key`. À utiliser pour tout ce que l'utilisateur peut corriger |
| `core.report(ui, S, key)` | Affiche une erreur inattendue avec son traceback. Seulement pour le vraiment inattendu |

### Ajouter un texte

1. Ajouter une ligne à `lang/en.xml` : `<string key="in.width">Width</string>`
2. L'utiliser dans le code : `T('in.width')`
3. Ajouter la même clé aux autres fichiers de langue.

Les clés manquantes dans une autre langue sont affichées en anglais. Les espaces réservés tels que `{0}` doivent rester dans chaque traduction.
