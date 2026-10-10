# Réglages

L'add-in n'a ni fichier de réglages ni page de réglages. Tout se règle dans la boîte de dialogue de la commande **Grille d'esquisse**. Les noms de champs sont écrits exactement comme dans la boîte de dialogue en français.

## Champs de la boîte de dialogue

Les longueurs sont saisies en millimètres par défaut (les champs sont créés avec l'unité `mm`). « Pas de limite » signifie : l'add-in lui-même ne contrôle rien de plus.

| Champ | Signification | Valeur par défaut | Valeurs autorisées |
| --- | --- | --- | --- |
| **Point** | Le point d'esquisse autour duquel la grille est construite. | Le point d'esquisse sélectionné avant l'ouverture de la boîte de dialogue, sinon vide | Exactement un point d'esquisse. Les autres objets ne peuvent pas être sélectionnés. |
| **Nombre selon** | Comment le nombre de formes est fixé. | Colonnes et lignes | **Colonnes et lignes**, **Remplissage d'une zone** |
| **Forme** | La forme qui est répétée. | Rectangle | **Rectangle**, **Cercle / ellipse**, **Trou oblong**, **Polygone** |
| **Côtés** | Nombre de côtés du polygone. | 6 | Nombre entier, 3 à 24 |
| **Régulier** | Case à cocher. Activé : tous les côtés du polygone ont la même longueur. Désactivé : le polygone est étiré à longueur × profondeur. | désactivé | activé, désactivé |
| **Coins** | Ce qu'il advient des quatre coins du rectangle. | Vifs | **Vifs**, **Arrondis**, **Chanfreinés** |
| **Rayon / chanfrein** | Rayon de l'arrondi, ou longueur de la coupe le long de chaque côté. | 1 mm | Supérieur à 0, au plus la moitié de la plus petite des deux valeurs, longueur et profondeur |
| **Longueur (X)** | Taille d'une forme en X. | 10 mm | Supérieure à 0, pas de limite supérieure |
| **Profondeur (Y)** | Taille d'une forme en Y. | 5 mm | Supérieure à 0, pas de limite supérieure |
| **Écart X** | Espace libre entre voisines en X. | 2 mm | 0 ou plus, pas de limite supérieure |
| **Écart Y** | Espace libre entre voisines en Y. | 2 mm | 0 ou plus, pas de limite supérieure |
| **Colonnes** | Nombre de formes côte à côte. | 8 | Nombre entier, 1 à 2000 |
| **Lignes** | Nombre de formes les unes au-dessus des autres. | 4 | Nombre entier, 1 à 2000 |
| **Largeur de la zone** | Largeur de la zone à remplir. | 100 mm | Supérieure à 0, et assez grande pour une forme |
| **Hauteur de la zone** | Hauteur de la zone à remplir. | 40 mm | Supérieure à 0, et assez grande pour une forme |
| **Le point est dans la grille** | Où le point sélectionné se trouve dans la grille terminée. | Au centre | Neuf entrées, voir plus bas |
| **Décalage X** | Déplace toute la grille en X, en plus de la position choisie ci-dessus. | 0 mm | Toute valeur, y compris négative |
| **Décalage Y** | Déplace toute la grille en Y. | 0 mm | Toute valeur, y compris négative |
| **Résultat** | Affiche le nombre de formes et la taille totale, ou un message. | – | Lecture seule |

Une limite de plus s'applique à toute la grille : colonnes × lignes ne doit pas dépasser **2000**. Cela vaut dans les deux modes de comptage.

## Quand un champ est affiché

| Champ | Affiché quand |
| --- | --- |
| **Côtés**, **Régulier** | **Forme** est **Polygone** |
| **Coins** | **Forme** est **Rectangle** |
| **Rayon / chanfrein** | **Forme** est **Rectangle** et **Coins** n'est pas **Vifs** |
| **Colonnes**, **Lignes** | **Nombre selon** est **Colonnes et lignes** |
| **Largeur de la zone**, **Hauteur de la zone** | **Nombre selon** est **Remplissage d'une zone** |
| tous les autres champs | toujours |

Un champ masqué garde sa valeur. Une valeur masquée n'est ni utilisée ni contrôlée.

## Le point est dans la grille

| Entrée | Le point se trouve |
| --- | --- |
| **Au centre** | au centre de la grille |
| **En bas à gauche** | sur le coin inférieur gauche |
| **En bas à droite** | sur le coin inférieur droit |
| **En haut à gauche** | sur le coin supérieur gauche |
| **En haut à droite** | sur le coin supérieur droit |
| **En bas au centre** | au milieu du bord inférieur |
| **En haut au centre** | au milieu du bord supérieur |
| **À gauche au centre** | au milieu du bord gauche |
| **À droite au centre** | au milieu du bord droit |

« Grille » désigne ici le plus petit rectangle autour de toutes les formes. La gauche et la droite suivent l'axe X de l'esquisse, le bas et le haut son axe Y.

## Textes d'aide dans la boîte de dialogue

Trois textes d'aide (infobulles) sont attachés à des champs :

| Champ | Texte |
| --- | --- |
| **Régulier** | « Garde le polygone équilatéral au lieu de l'étirer à la longueur × la profondeur. La plus petite des deux fixe alors sa taille et le pas suit la forme réelle - l'écart demandé est respecté dans les deux cas. » |
| **Coins**, **Rayon / chanfrein** | « Enlève les quatre angles droits du rectangle, sous forme d'un congé ou d'un chanfrein droit. Au plus la moitié du côté le plus court : ce rayon exact transforme le rectangle en trou oblong, ce chanfrein en losange. Le rectangle englobant ne change pas, le nombre, le pas et l'écart restent donc les mêmes. » |
| **Décalage X**, **Décalage Y** | « Déplace toute la grille par rapport au point sélectionné, en plus de ce que le point d'ancrage a déjà fixé. Permet de garder une marge par rapport à un bord sans déplacer le point lui-même. Les valeurs négatives vont dans l'autre sens. » |

Remarque sur le deuxième texte : un chanfrein d'exactement la moitié du côté le plus court ne donne un losange que si la longueur et la profondeur sont égales. Avec des valeurs inégales, il donne une forme à six côtés.

Le bouton lui-même a le texte d'aide : « Construit une grille de formes autour d'un point d'esquisse. Nombre fixe de colonnes et de lignes, ou autant qu'il en tient dans une zone. »

## Ce qui est mémorisé

- Quand une grille est terminée par **OK**, l'add-in mémorise toutes les valeurs sauf le point : mode de comptage, forme, côtés, Régulier, coins, rayon / chanfrein, longueur, profondeur, les deux écarts, colonnes, lignes, largeur de la zone, hauteur de la zone, position du point, les deux décalages.
- À l'ouverture suivante de la boîte de dialogue, ces valeurs sont préremplies.
- Les valeurs ne sont **pas** mémorisées quand la boîte de dialogue est annulée, ou quand OK se termine par un message d'erreur.
- Les valeurs sont gardées en mémoire uniquement, jamais sur le disque. Elles durent jusqu'à l'arrêt de l'add-in ou la fermeture de Fusion. Ensuite, les valeurs par défaut du tableau ci-dessus s'appliquent de nouveau.
- Les valeurs sont les mêmes pour tous les documents ouverts dans cette session Fusion.

## Langue

L'add-in a cinq langues : allemand, anglais, espagnol, français, italien.

Comment la langue est choisie, dans cet ordre :

1. La langue réglée dans Fusion sous **Preferences → General → User Language**, si elle fait partie des cinq.
2. Sinon, la langue du système d'exploitation, si elle fait partie des cinq. (L'add-in lit les variables d'environnement `LANG`, `LANGUAGE`, `LC_ALL`, puis les paramètres régionaux du système.)
3. Sinon, l'anglais.

Autres détails :

- Il n'y a pas de sélecteur de langue dans l'add-in.
- La langue est lue une seule fois, au démarrage de l'add-in. Après un changement de langue dans Fusion, arrêter puis démarrer l'add-in, ou redémarrer Fusion.
- Si un texte manque dans une langue, le texte anglais est affiché à sa place.
- La ligne **Résultat** affiche toujours des millimètres, dans toutes les langues.
