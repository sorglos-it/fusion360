# Utilisation

Tous les noms de champs ci-dessous sont écrits exactement tels qu'ils apparaissent dans la boîte de dialogue en français. Détails sur chaque champ : [settings.md](settings.md).

## Dessiner une grille

1. Ouvrir ou modifier une esquisse.
2. Cliquer sur un point d'esquisse. Ce peut être l'origine de l'esquisse ou un point placé soi-même.
3. Cliquer sur le bouton **Grille d'esquisse**. La boîte de dialogue s'ouvre. Le point cliqué est déjà inscrit dans **Point**.
4. Si **Point** est vide, cliquer maintenant sur un point d'esquisse. L'invite indique « Sélectionner un point d'esquisse ».
5. Régler les valeurs. La ligne **Résultat** montre ce qui sera obtenu, par exemple `8 × 4 = 32 formes, 94.00 × 26.00 mm au total`.
6. Regarder l'aperçu dans l'esquisse.
7. Appuyer sur **OK**.

Seuls des points d'esquisse peuvent être sélectionnés. Il faut exactement un point.

**OK** est grisé tant qu'une valeur n'est pas autorisée. Dans la plupart des cas, la ligne **Résultat** en donne alors la raison. Voir [troubleshooting.md](troubleshooting.md).

La grille est alignée sur les axes X et Y de l'esquisse. Elle ne peut pas être tournée dans la boîte de dialogue. Les mots comme « gauche », « droite », « haut », « bas » et « vers le haut » dans cette documentation désignent les axes de l'esquisse : la droite est +X, le haut est +Y.

La reprise d'un point cliqué avant l'ouverture de la boîte de dialogue (étape 3) a été modifiée dans la version 1.1.0.0 et testée hors ligne uniquement, pas dans Fusion. Si le point n'est pas repris, le sélectionner dans la boîte de dialogue (étape 4).

## Exemple

Voici les valeurs avec lesquelles la boîte de dialogue démarre :

| Champ | Valeur |
| --- | --- |
| **Forme** | Rectangle |
| **Longueur (X)** | 10 mm |
| **Profondeur (Y)** | 5 mm |
| **Écart X** / **Écart Y** | 2 mm |
| **Colonnes** / **Lignes** | 8 / 4 |

Résultat : 32 rectangles. La grille mesure 94 × 26 mm (8 × 10 + 7 × 2 = 94, 4 × 5 + 3 × 2 = 26). Avec **Le point est dans la grille** réglé sur **Au centre**, le point est le centre de la grille.

## Choisir comment les formes sont comptées

Champ **Nombre selon**.

### Colonnes et lignes

1. Régler **Nombre selon** sur **Colonnes et lignes**.
2. Saisir **Colonnes** et **Lignes**.

On obtient exactement ce nombre. La grille est aussi grande qu'il le faut.

### Remplissage d'une zone

1. Régler **Nombre selon** sur **Remplissage d'une zone**.
2. Saisir **Largeur de la zone** et **Hauteur de la zone**.

L'add-in dessine autant de formes qu'il en tient **entièrement** dans la zone. Une forme qui ne tient qu'en partie n'est jamais dessinée.

- Exemple : largeur de la zone 100 mm, longueur 10 mm, écart 2 mm donnent 8 colonnes. Elles occupent 94 mm. Une neuvième colonne demanderait 106 mm.
- La grille est en général un peu plus petite que la zone. La zone ne sert qu'à compter. Elle n'est pas dessinée.
- Le reste de la zone demeure vide du côté opposé au point. Avec **Au centre**, il est réparti également des deux côtés.
- Une zone d'exactement 94 mm donne 8 colonnes ; 93,9 mm en donnent 7.

Les champs **Colonnes** et **Lignes** ne sont affichés que dans le premier mode, **Largeur de la zone** et **Hauteur de la zone** que dans le second.

## Choisir la forme

Champ **Forme**.

| Entrée | Ce qu'on obtient |
| --- | --- |
| **Rectangle** | Un rectangle de longueur × profondeur. Ses coins peuvent être modifiés, voir plus bas. |
| **Cercle / ellipse** | Une ellipse dont la longueur et la profondeur sont les deux diamètres. Des valeurs égales donnent un cercle. |
| **Trou oblong** | Un rectangle avec deux extrémités en demi-cercle. Les extrémités sont dans la direction la plus longue : si la longueur est plus grande que la profondeur, les extrémités gauche et droite sont rondes. Des valeurs égales donnent un cercle. |
| **Polygone** | Une forme à 3 à 24 côtés droits. Un sommet pointe toujours vers le haut. |

### Rectangle : coins

1. Régler **Forme** sur **Rectangle**. Le champ **Coins** apparaît.
2. Choisir **Vifs**, **Arrondis** ou **Chanfreinés**. (Chanfreinés signifie : le coin est coupé par une ligne droite.)
3. Pour **Arrondis** et **Chanfreinés**, le champ **Rayon / chanfrein** apparaît. Saisir le rayon de l'arrondi, ou la distance entre le coin et le début de la coupe le long de chaque côté.

La plus grande valeur autorisée est la moitié du côté le plus court. Exactement à cette valeur :

| Rectangle | Valeur | Arrondis devient | Chanfreinés devient |
| --- | --- | --- | --- |
| 10 × 5 mm | 2,5 mm | un trou oblong | une forme à six côtés |
| 10 × 10 mm | 5 mm | un cercle | un losange |

Les coins ne changent ni le nombre de formes, ni l'espacement, ni la taille totale.

### Polygone : côtés et Régulier

1. Régler **Forme** sur **Polygone**. Les champs **Côtés** et **Régulier** apparaissent.
2. Saisir **Côtés** (3 à 24).
3. Laisser **Régulier** désactivé, ou le cocher.

| **Régulier** | Résultat |
| --- | --- |
| désactivé | Le polygone est étiré pour mesurer exactement longueur × profondeur. Ses côtés n'ont alors en général pas la même longueur. |
| activé | Tous les côtés ont la même longueur. La plus petite des deux valeurs, longueur et profondeur, fixe la taille. L'espacement suit la taille réelle du polygone, l'écart reste donc l'écart saisi. |

Exemple avec 6 côtés, longueur 10 mm, profondeur 5 mm, écart 2 mm :

| **Régulier** | Taille d'une forme | Distance d'une forme à la suivante |
| --- | --- | --- |
| désactivé | 10,00 × 5,00 mm | 12,00 × 7,00 mm |
| activé | 4,33 × 5,00 mm | 6,33 × 7,00 mm |

## Régler la taille et l'écart

- **Longueur (X)** et **Profondeur (Y)** : taille d'une forme.
- **Écart X** et **Écart Y** : espace libre entre deux voisines. 0 est autorisé ; les formes se touchent alors. Les valeurs négatives ne sont pas autorisées.

## Décider où se trouve le point

Champ **Le point est dans la grille**. Il indique où le point cliqué se retrouve dans la grille terminée. Il n'indique pas dans quelle direction la grille grandit.

Exemple : **En bas à gauche** place le point sur le coin inférieur gauche de la grille. La grille s'étend alors vers la droite et vers le haut.

Trois des neuf positions, avec une grille de 3 × 2 formes (`X` est le point, `#` les formes) :

```
  Au centre            En bas à gauche      En haut au centre
  #####.#####.#####    #####.#####.#####    #####.##X##.#####
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  ........X........    .................    .................
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  #####.#####.#####    X####.#####.#####    #####.#####.#####
```

Les neuf entrées sont listées dans [settings.md](settings.md#le-point-est-dans-la-grille).

## Décaler la grille par rapport au point

Champs **Décalage X** et **Décalage Y**.

1. Choisir d'abord la position dans **Le point est dans la grille**.
2. Saisir de combien toute la grille doit se déplacer. Les valeurs positives la déplacent le long des axes X et Y de l'esquisse. Les valeurs négatives la déplacent dans l'autre sens.

Cela sert à garder une marge : le point reste sur un coin de la pièce, et la grille commence, par exemple, 2 mm plus à l'intérieur. Le décalage ne change ni le nombre de formes ni la taille de la grille.

## Lire la ligne Résultat

**Résultat** ne peut pas être modifié. Il affiche soit

- `{colonnes} × {lignes} = {nombre} formes, {largeur} × {hauteur} mm au total`, toujours en millimètres avec deux décimales, soit
- un message qui indique quelle valeur n'est pas autorisée.

## Dessiner une autre grille

- La boîte de dialogue s'ouvre avec les valeurs de la dernière grille terminée par **OK**. Voir [settings.md](settings.md#ce-qui-est-mémorisé).
- La commande est marquée comme répétable ; la fonction « répéter la dernière commande » de Fusion peut donc la relancer.

## Ce qu'on obtient dans l'esquisse

- De simples lignes, arcs, cercles et ellipses d'esquisse. Aucune fonction de réseau de Fusion n'est créée.
- Les formes ne sont pas liées à la boîte de dialogue. Pour modifier la grille plus tard, supprimer les formes et dessiner une nouvelle grille.
- L'add-in n'ajoute de lui-même ni cotes ni contraintes entre les formes et le point.
