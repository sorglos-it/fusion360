# Utilisation

Tous les noms de champs ci-dessous sont écrits exactement tels qu'ils apparaissent dans la boîte de dialogue en français. Chaque champ est expliqué en détail dans
[settings.md](settings.md).

## Mots employés ici

| Mot | Signification |
|---|---|
| Dent | Une queue d'aronde, un triangle ou un rectangle qui dépasse de la ligne |
| Tenon | La dent en tant que partie de l'une des pièces |
| Mortaise | Le creux correspondant dans l'autre pièce |
| Tolérance | L'espace entre le tenon et la mortaise (le jeu) |
| Bande | Le contour fermé que l'add-in dessine. Son intérieur est exactement l'espace. |
| Point de départ, point d'arrivée | Les deux extrémités d'une ligne d'esquisse, dans l'ordre où la ligne a été dessinée |

## Dessiner un assemblage sur une ligne

1. Ouvrir une esquisse ou en modifier une existante.
2. Dessiner une ligne droite là où les deux pièces doivent se rejoindre.
3. Cliquer sur la ligne.
4. Cliquer sur le bouton **Queue d'aronde**. La boîte de dialogue s'ouvre. La ligne est déjà inscrite sous **Lignes**.
   Il est aussi possible de lancer d'abord la commande, puis de cliquer sur la ligne.
5. Régler **Nombre**, **Forme**, **Largeur (base)**, **Profondeur** et **Tolérance**.
6. Observer l'aperçu dans l'esquisse.
7. Appuyer sur **OK**.

Résultat :

- Une bande fermée est dessinée dans la même esquisse que la ligne.
- La ligne d'origine devient une géométrie de construction (une ligne auxiliaire en pointillés), si
  **Convertir la ligne d'origine en géométrie de construction** est coché. Cela ne se produit qu'à l'appui sur OK, pas dans l'aperçu.
- L'add-in n'ajoute ni cotes ni contraintes aux nouvelles lignes.

Si **OK** est grisé et qu'aucun aperçu n'est affiché, les valeurs ne conviennent pas. La boîte de dialogue ne dit pas pourquoi.
Voir [troubleshooting.md](troubleshooting.md#ok-est-grisé).

## Obtenir deux pièces qui s'emboîtent à partir de la bande

1. Dessiner le contour de la pièce entière. Faire passer la ligne d'assemblage en travers, d'un bord à l'autre.
2. Exécuter Dovetail sur la ligne d'assemblage.
3. Extruder le contour pour obtenir un corps solide.
4. Extruder la bande en enlèvement de matière à travers ce corps.

Il reste deux corps. Ils s'emboîtent l'un dans l'autre avec l'espace réglé sous **Tolérance**.

Les étapes 3 et 4 sont des fonctions ordinaires de Fusion. L'add-in lui-même ne dessine que la bande.

## Choisir la forme

Utiliser la liste **Forme** :

| Entrée | Résultat |
|---|---|
| **Trapèze (queue d'aronde)** | La dent s'élargit vers sa pointe. Elle s'accroche et ne peut pas être retirée tout droit. |
| **Triangle** | La dent se termine en pointe. Elle n'a pas d'accroche et peut être séparée. |
| **Rectangle (assemblage à peigne)** | Dent droite, de même largeur à la base et à la pointe. |

**Angle de flanc** n'est actif que pour **Trapèze (queue d'aronde)**. Il règle de combien la dent s'élargit. À 0 degré, le
trapèze est identique à un rectangle. Un angle négatif rend la dent plus étroite vers sa pointe.

## Plusieurs dents sur une ligne

1. Régler **Nombre** sur 2 ou plus. Le champ **Entraxe (centre à centre)** devient actif.
2. Régler **Entraxe (centre à centre)** : la distance entre le milieu d'une dent et le milieu de la suivante.

Le groupe de dents est toujours placé symétriquement autour du milieu de la ligne :

| Nombre | Position des dents par rapport au milieu (entraxe 30 mm) |
|---|---|
| 1 | 0 |
| 2 | −15 / +15 |
| 3 | −30 / 0 / +30 |
| 4 | −45 / −15 / +15 / +45 |
| 5 | −60 / −30 / 0 / +30 / +60 |

Un nombre impair place une dent au milieu. Un nombre pair y place un vide.

## Déplacer les dents le long de la ligne

Deux façons :

- Saisir une valeur dans **Décalage**. Une valeur positive déplace les dents vers le point d'arrivée de la ligne, une valeur négative
  vers le point de départ. 0 signifie centré.
- Utiliser les trois boutons de la rangée **Déplacer** :

  | Bouton | Effet |
  |---|---|
  | **Vers la gauche (vers le point de départ)** | déplace les dents d'un **Pas de déplacement** vers le point de départ |
  | **Centrer** | remet **Décalage** à 0 |
  | **Vers la droite (vers le point d'arrivée)** | déplace les dents d'un **Pas de déplacement** vers le point d'arrivée |

Les boutons s'arrêtent là où les dents ne tiendraient plus sur la ligne. Avec plusieurs lignes, la ligne la plus courte fixe cette
limite. Une valeur saisie n'est pas corrigée : si elle est trop grande, OK est grisé.

**Décalage** repart de 0 à chaque ouverture de la boîte de dialogue.

## Choisir quelle pièce cède de la matière

L'espace doit bien venir de quelque part. La liste **La ligne est** en décide :

| Entrée | Bord de la mortaise | Bord du tenon | À utiliser quand |
|---|---|---|---|
| **Ligne médiane - la moitié de la tolérance de chaque côté** | recule vers l'extérieur de la moitié de la tolérance | recule vers l'intérieur de la moitié de la tolérance | les deux pièces doivent rester égales |
| **Bord de la mortaise - toute la tolérance sur le tenon** | exactement sur la forme dessinée | recule vers l'intérieur de toute la tolérance | la pièce avec les mortaises doit garder sa taille exacte |
| **Bord du tenon - toute la tolérance sur la mortaise** | recule vers l'extérieur de toute la tolérance | exactement sur la forme dessinée | la pièce avec les tenons doit garder sa taille exacte |

L'espace entre les pièces vaut toute la tolérance dans les trois cas.

Exemple avec une tolérance de 0,25 mm :

| Entrée | Mortaise | Tenon | Espace |
|---|---|---|---|
| Ligne médiane | +0,125 mm | −0,125 mm | 0,25 mm |
| Bord de la mortaise | 0 | −0,25 mm | 0,25 mm |
| Bord du tenon | +0,25 mm | 0 | 0,25 mm |

## Placer les dents de l'autre côté

Cocher **Inverser la direction**.

Sans la coche, les dents se trouvent du côté gauche de la ligne quand on regarde de son point de départ vers son point d'arrivée
(dans le plan X/Y de l'esquisse). Avec la coche, elles se trouvent du côté droit.

Avec plusieurs lignes, chaque ligne suit sa propre direction. Des lignes dessinées dans des sens opposés reçoivent leurs dents sur des
côtés opposés. **Inverser la direction** les retourne toutes ensemble.

## Plusieurs lignes à la fois

1. Sélectionner plusieurs lignes avant de lancer la commande. Ou lancer la commande et cliquer sur les lignes l'une après l'autre.
   Jusqu'à 100 lignes sont possibles.
2. Régler les valeurs une seule fois.
3. Appuyer sur **OK**.

Chaque ligne reçoit son propre assemblage à partir des mêmes valeurs. Chaque ligne est mesurée séparément et ses dents sont centrées sur
son propre milieu. Les lignes peuvent avoir des longueurs différentes.

Les valeurs doivent convenir à chaque ligne. Si une ligne est trop courte, rien n'est dessiné du tout et OK est grisé. Regarder
d'abord la ligne la plus courte ; c'est elle qui manque de place en premier.

Seules des lignes d'esquisse droites peuvent être sélectionnées. Les arcs, les cercles et les splines ne le peuvent pas.

## Deux pièces identiques : Refléter la géométrie

Cocher **Refléter la géométrie**.

La moitié des dents pointe alors d'un côté et l'autre moitié de l'autre. Si l'on tourne la bande de 180 degrés autour du
milieu de la ligne, elle retombe sur elle-même. Les deux pièces de la coupe sont donc identiques. Il suffit de modéliser une pièce et
de la fabriquer deux fois ; la seconde est retournée.

La boîte de dialogue règle trois choses automatiquement, car chacune d'elles romprait la symétrie :

| Quoi | Pourquoi |
|---|---|
| **Nombre** est porté au nombre pair suivant | Une dent au milieu devrait pointer des deux côtés à la fois. |
| **La ligne est** est réglé sur la ligne médiane et grisé | C'est le seul cas où les deux pièces cèdent autant l'une que l'autre. |
| **Décalage** est mis à 0 ; **Décalage**, **Pas de déplacement** et **Déplacer** sont grisés | Un groupe décalé n'est plus symétrique par rapport au milieu. |

Quand la coche est retirée, les champs redeviennent actifs. Les valeurs modifiées par la boîte de dialogue restent telles quelles.

Avec plusieurs lignes, chaque ligne est reflétée par rapport à son propre milieu.

## Conserver ou convertir la ligne d'origine

Le champ **Convertir la ligne d'origine en géométrie de construction** est coché par défaut.

- Coché : la ligne sélectionnée devient une géométrie de construction à l'appui sur OK. Elle conserve ses cotes et ses contraintes, mais
  ne divise plus la bande en deux zones.
- Non coché : la ligne reste une ligne normale. Elle traverse la bande et la découpe en deux zones (profils).

Une ligne qui est déjà une géométrie de construction est laissée telle quelle.

## Aperçu

Tant que la boîte de dialogue est ouverte, l'add-in dessine la bande en aperçu après chaque modification.

- L'aperçu ne modifie jamais la ligne d'origine. C'est pourquoi l'aperçu montre encore la ligne comme une ligne normale.
- Si les valeurs ne conviennent pas, aucun aperçu n'est affiché.

## Relancer la commande

Fusion peut répéter la commande avec sa propre fonction « répéter la dernière commande » ; l'add-in le permet.
La boîte de dialogue s'ouvre de nouveau avec les valeurs de la dernière exécution réussie. Voir
[settings.md](settings.md#ce-qui-est-mémorisé).
