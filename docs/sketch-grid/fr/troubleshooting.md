# Dépannage

Tous les textes sont cités d'après le fichier de langue français. `{0}` et `{1}` représentent des valeurs que l'add-in insère.

## Où les messages apparaissent

| Endroit | Quand |
| --- | --- |
| Ligne **Résultat** dans la boîte de dialogue | Une valeur n'est pas autorisée. **OK** est désactivé en même temps. |
| **OK** désactivé sans texte | Aucun point d'esquisse n'est sélectionné (voir la première ligne ci-dessous). |
| Fenêtre de message avec le titre **Grille d'esquisse** | Un contrôle n'échoue qu'au moment où **OK** est pressé, ou quelque chose d'inattendu s'est mal passé. |

## Messages sur la saisie

| Message | Cause | Que faire |
| --- | --- | --- |
| « Sélectionnez exactement un point d'esquisse. » | **Point** est vide, ou l'objet sélectionné n'est pas un point d'esquisse. Ce texte n'est normalement pas affiché ; **OK** est simplement désactivé. | Cliquer sur **Point** et sélectionner un point d'esquisse : l'origine de l'esquisse ou un point placé soi-même. Les points sur des corps ne peuvent pas être sélectionnés. |
| « La longueur doit être supérieure à 0. » | **Longueur (X)** vaut 0 ou est négative. | Saisir une valeur supérieure à 0. |
| « La profondeur doit être supérieure à 0. » | **Profondeur (Y)** vaut 0 ou est négative. | Saisir une valeur supérieure à 0. |
| « L'écart ne peut pas être négatif. » | **Écart X** ou **Écart Y** est inférieur à 0. | Saisir 0 ou plus. Des formes qui se chevauchent ne sont pas possibles. |
| « Au moins une colonne est nécessaire. » | **Colonnes** est inférieur à 1. | Saisir 1 ou plus. Le champ lui-même n'accepte que 1 à 2000 ; ce message ne devrait donc normalement pas apparaître. |
| « Au moins une ligne est nécessaire. » | **Lignes** est inférieur à 1. | Saisir 1 ou plus. Le champ lui-même n'accepte que 1 à 2000 ; ce message ne devrait donc normalement pas apparaître. |
| « La zone doit être supérieure à 0 dans les deux directions. » | Mode **Remplissage d'une zone** : **Largeur de la zone** ou **Hauteur de la zone** vaut 0 ou est négative. | Saisir des valeurs supérieures à 0 dans les deux champs. |
| « Pas même une forme ne tient dans cette zone. Il faut au moins {0} × {1} mm. » | Mode **Remplissage d'une zone** : la zone est plus petite qu'une forme. Les deux nombres sont la taille d'une forme. | Rendre **Largeur de la zone** et **Hauteur de la zone** au moins aussi grandes que les nombres du message, ou réduire la forme. |
| « Un polygone a besoin de {0} à {1} côtés. » | **Côtés** est en dehors de 3 à 24. | Saisir 3 à 24. Le champ lui-même n'accepte que cette plage ; ce message ne devrait donc normalement pas apparaître. |
| « Le rayon / chanfrein doit être supérieur à 0. » | **Coins** est **Arrondis** ou **Chanfreinés**, et **Rayon / chanfrein** vaut 0 ou est négatif. | Saisir une valeur supérieure à 0, ou régler **Coins** sur **Vifs**. |
| « Le rayon / chanfrein peut valoir au plus {0} mm, la moitié du côté le plus court. » | **Rayon / chanfrein** est plus grand que la moitié de la plus petite des deux valeurs **Longueur (X)** et **Profondeur (Y)**. Le nombre est la plus grande valeur autorisée. | Saisir au plus la valeur du message, ou agrandir le rectangle. |
| « Cela ferait {0} formes. Au maximum {1} sont autorisées - au-delà, Fusion se bloque. » | Colonnes × lignes dépasse 2000. Le premier nombre est ce que les valeurs saisies donneraient. | Utiliser moins de colonnes ou de lignes. Dans le mode **Remplissage d'une zone** : une zone plus petite, des formes plus grandes ou des écarts plus grands. Pour plus de formes, dessiner plusieurs grilles. |

Si plusieurs valeurs sont fausses, seul le premier problème est affiché. Le corriger, puis le suivant apparaît.

## Messages sur l'add-in lui-même

Ils apparaissent dans une fenêtre de message. `{0}` est remplacé par un rapport d'erreur technique (un traceback Python).

| Message | Cause | Que faire |
| --- | --- | --- |
| « Aucun panneau de barre d'outils approprié n'a été trouvé. » | Au démarrage, l'add-in n'a trouvé ni le panneau CREATE de la barre d'outils d'esquisse ni le panneau CREATE de l'onglet SOLID. Aucun bouton n'est ajouté. | Passer à l'espace de travail **Design**, puis arrêter et relancer l'add-in. Si le message persiste, le signaler avec la version de Fusion. |
| « Erreur lors de la création de la géométrie : {0} » | Quelque chose d'inattendu a échoué pendant le dessin après **OK**. | Réessayer. Si cela persiste, le signaler avec le texte complet. |
| « Erreur lors de la construction de la boîte de dialogue : {0} » | Quelque chose d'inattendu a échoué pendant la construction de la boîte de dialogue. | Arrêter et relancer l'add-in. Si cela persiste, le signaler avec le texte complet. |
| « Échec du démarrage : {0} » | Quelque chose d'inattendu a échoué pendant le démarrage de l'add-in. | Vérifier que le dossier est complet et qu'il s'appelle toujours `SketchGrid` (voir [installation.md](installation.md)). Le relancer. |
| « Échec de l'arrêt : {0} » | Quelque chose d'inattendu a échoué pendant l'arrêt de l'add-in. | Redémarrer Fusion. |

Les signalements se font sur <https://github.com/sorglos-it/fusion360/issues>.

## Autres problèmes

| Problème | Cause | Que faire |
| --- | --- | --- |
| **OK** est gris et **Résultat** affiche un résultat normal | Aucun point n'est sélectionné. | Sélectionner un point d'esquisse dans **Point**. |
| Le point cliqué auparavant n'est pas dans la boîte de dialogue | Le point n'a pas pu être repris. Depuis la version 1.1.0.0, la boîte de dialogue continue de fonctionner dans ce cas (testé hors ligne uniquement, pas dans Fusion). | Sélectionner le point dans la boîte de dialogue. |
| Pas d'aperçu pendant la saisie | Une valeur n'est pas autorisée à ce moment-là. L'aperçu reste vide, sans message. | Lire la ligne **Résultat** et corriger la valeur. |
| Le bouton manque | L'add-in ne fonctionne pas, ou aucun panneau n'a été trouvé. | Ouvrir **Utilities → ADD-INS → Add-Ins**, sélectionner **SketchGrid**, appuyer sur **Run**. |
| Le bouton affiche un ancien numéro de version | L'ancien add-in est encore en mémoire. | Arrêter l'add-in, remplacer le dossier, le relancer. |
| La boîte de dialogue est en anglais alors que Fusion est réglé sur une autre langue | Seuls l'allemand, l'anglais, l'espagnol, le français et l'italien existent. Ou la langue a été changée pendant que l'add-in fonctionnait. | Arrêter et relancer l'add-in. Voir [settings.md](settings.md#langue). |
| Un texte apparaît sous forme de clé, comme `in.point` | Les fichiers de langue manquent ou sont endommagés. | Réinstaller l'add-in à partir du ZIP. |
| La grille ne remplit pas la zone | Seules des formes complètes sont dessinées. | C'est voulu. Voir [usage.md](usage.md#remplissage-dune-zone). |
| Un polygone régulier est bien plus petit que longueur × profondeur | Avec **Régulier**, la plus petite des deux valeurs, longueur et profondeur, fixe la taille. | Utiliser des valeurs proches pour la longueur et la profondeur, ou décocher **Régulier**. |
| La boîte de dialogue redémarre avec les valeurs standard | Les valeurs mémorisées ne durent que jusqu'à l'arrêt de l'add-in ou la fermeture de Fusion. | Les saisir de nouveau. |

## Limites connues

Non confirmé dans Fusion (trouvé lors d'une relecture du code) :

- **Les trous oblongs et les rectangles à coins arrondis ou chanfreinés** sont dessinés comme des lignes et des arcs séparés. Leurs extrémités se trouvent au même endroit, mais il se peut qu'elles ne restent pas liées quand on fait glisser une partie de la forme. Les polygones et les rectangles à coins vifs ne sont pas concernés de cette façon.
- **La limite de 2000 compte les formes, pas les courbes.** Un polygone à 24 côtés, ce sont 24 lignes. Une grande grille de polygones, de trous oblongs ou de rectangles coupés peut donc être lente bien qu'elle soit dans la limite.

D'après le code :

- Seuls des points d'esquisse peuvent être sélectionnés. Les coins de corps ou les points sur des arêtes ne le peuvent pas.
- La grille est toujours parallèle aux axes X et Y de l'esquisse. Elle ne peut pas être tournée dans la boîte de dialogue.
- Le polygone a toujours un sommet qui pointe vers le haut. La boîte de dialogue n'a pas de champ pour le tourner.
- Seul le rectangle peut avoir des coins arrondis ou chanfreinés.
- Les écarts ne peuvent pas être négatifs. Les formes ne peuvent pas se chevaucher.
- Les formes sont de simples géométries d'esquisse. Modifier une valeur plus tard ne met pas à jour une grille existante.
- L'add-in n'ajoute ni cotes ni contraintes. La grille n'est pas liée au point une fois dessinée.
- Les valeurs mémorisées sont perdues quand l'add-in s'arrête ou que Fusion se ferme.
- Dans le mode **Remplissage d'une zone**, le reste vide n'est centré que si **Le point est dans la grille** est **Au centre** (ou une entrée « au centre » pour cette seule direction).
