# Fonctionnement

## Fichiers

Tout ce dont l'add-in a besoin se trouve dans un seul dossier, `Dovetail` :

| Fichier | Rôle |
|---|---|
| `Dovetail.py` | Le programme entier : langue, géométrie, dessin, boîte de dialogue, démarrage et arrêt |
| `Dovetail.manifest` | Description pour Fusion : nom, auteur, version, systèmes pris en charge, démarrage avec Fusion |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Tous les textes, un fichier par langue |
| `resources/Dovetail/` | Icône de la barre d'outils en 16, 32 et 64 pixels |
| `resources/nudge_left/`, `nudge_center/`, `nudge_right/` | Icônes des trois boutons **Déplacer** |

L'add-in ne lit que ces fichiers. Il n'écrit aucun fichier et n'ouvre aucune connexion réseau.

## Démarrage et arrêt

Au démarrage, l'add-in :

1. choisit la langue (voir [settings.md](settings.md#langue)),
2. enregistre la commande sous le nom « Queue d'aronde » suivi de la version du manifeste entre parenthèses,
3. cherche un panneau de barre d'outils et y place le bouton (voir [installation.md](installation.md#premier-démarrage-dans-fusion)).

À l'arrêt, il retire de nouveau le bouton et la commande.

## De la ligne à la bande

### 1. Une règle le long de la ligne

Pour chaque ligne sélectionnée, l'add-in met en place son propre système de mesure :

- **s** court le long de la ligne, du point de départ (0) au point d'arrivée (la longueur de la ligne).
- **h** court à angle droit par rapport à la ligne, du côté vers lequel pointent les dents.

Sans **Inverser la direction**, h pointe vers la gauche quand on regarde du point de départ vers le point d'arrivée.
Avec **Inverser la direction**, h pointe vers la droite.

### 2. Où se trouvent les dents

Le milieu du groupe se trouve à : longueur de la ligne ÷ 2 + Décalage.
Les dents sont placées de part et d'autre, chacune à un **Entraxe** de la suivante.

### 3. Le contour nominal

Le contour nominal est le bord commun que les deux pièces auraient sans aucun espace. C'est une ligne en zigzag ouverte :

1. elle commence au point de départ de la ligne,
2. suit la ligne jusqu'à la première dent,
3. monte le long d'un côté de la dent, traverse la pointe et redescend de l'autre côté,
4. continue le long de la ligne jusqu'à la dent suivante,
5. se termine au point d'arrivée de la ligne.

La pointe est un seul point pour un triangle et deux points pour un trapèze ou un rectangle.

Avec **Refléter la géométrie**, la première moitié des dents pointe du côté opposé (moins h), la seconde moitié du
côté normal (plus h).

### 4. Répartir la tolérance

Deux copies du contour nominal sont créées, chacune déplacée de côté d'une distance fixe (un décalage parallèle) :

- le contour de la **mortaise** est déplacé du côté des dents. La mortaise s'agrandit.
- le contour du **tenon** est déplacé de l'autre côté. Le tenon rétrécit.

**La ligne est** décide de combien chacun est déplacé :

| Entrée | Mortaise déplacée de | Tenon déplacé de |
|---|---|---|
| Ligne médiane | ½ × Tolérance | ½ × Tolérance |
| Bord de la mortaise | 0 (reste sur le contour nominal) | Tolérance |
| Bord du tenon | Tolérance | 0 (reste sur le contour nominal) |

La somme des deux parts donne toujours la tolérance entière. Comme les deux contours sont des copies parallèles du même contour,
l'espace entre eux est le même partout : à la base, sur les côtés et à la pointe.

Comment le déplacement est fait :

- Chaque segment droit est déplacé de côté de cette distance.
- À chaque angle, les deux segments déplacés sont prolongés ou raccourcis jusqu'à ce qu'ils se rejoignent (un angle en onglet).
- Les deux extrémités sont déplacées tout droit de côté, de sorte que les deux contours commencent à s = 0 et finissent à s = longueur de la ligne.

### 5. La bande fermée

Les deux contours sont réunis en une seule boucle fermée :

1. le long du contour de la mortaise, du début à la fin de la ligne,
2. en travers jusqu'au contour du tenon, à la fin de la ligne,
3. en retour le long du contour du tenon,
4. en travers jusqu'au point de départ.

L'intérieur de cette boucle est l'espace lui-même. C'est une bande d'exactement la tolérance, qui suit le contour des dents.
La découper dans un solide laisse deux pièces qui s'emboîtent.

### 6. Dessin

- La bande est dessinée comme une chaîne de lignes d'esquisse droites. Chaque ligne commence au point d'arrivée de la précédente, et
  la dernière se referme sur la première. Le contour est donc d'un seul tenant.
- Les lignes vont dans l'esquisse à laquelle appartient la ligne sélectionnée.
- Pendant le dessin, l'esquisse reçoit l'ordre de ne pas se recalculer après chaque ligne. Elle se recalcule une fois à la fin.
- À l'appui sur OK, et seulement si la case est cochée, la ligne d'origine est d'abord convertie en géométrie de construction. Une ligne normale
  traverserait la bande et la découperait en deux zones.
- L'add-in n'ajoute ni cotes ni contraintes.

## Les contrôles

Avant de dessiner quoi que ce soit, toute la sélection est calculée une fois. Le dessin ne commence que si chaque ligne passe les contrôles.
Une mauvaise ligne à la fin de la sélection ne peut donc pas laisser l'esquisse à moitié dessinée.

Les contrôles s'exécutent dans cet ordre pour chaque ligne :

| N° | Contrôle | Clé du message en cas d'échec |
|---|---|---|
| 1 | La ligne a une longueur | `err.zero_length` |
| 2 | La largeur est supérieure à 0 | `err.width` |
| 3 | La profondeur est supérieure à 0 | `err.depth` |
| 4 | La tolérance est supérieure à 0 | `err.tolerance_zero` |
| 5 | Le nombre vaut au moins 1 | `err.count` |
| 6 | Reflet : le nombre est pair | `err.mirror_even` |
| 7 | Reflet : la ligne médiane est choisie | `err.mirror_center` |
| 8 | Reflet : le décalage vaut 0 | `err.mirror_offset` |
| 9 | Trapèze : l'angle de flanc est dans la plage ±89 degrés | `err.angle_range` |
| 10 | Trapèze : la pointe garde une largeur | `err.angle_negative` |
| 11 | Deux dents ou plus : l'entraxe est supérieur à 0 | `err.spacing_positive` |
| 12 | Deux dents ou plus : l'entraxe vaut au moins le minimum | `err.spacing_too_small` |
| 13 | Les dents plus la distance aux extrémités tiennent sur la ligne | `err.offset_range` ou `err.does_not_fit` |
| 14 | Aucun angle en onglet ne s'éloigne de plus de 12 × la distance de déplacement | `err.miter_runaway` |
| 15 | Les deux contours commencent et finissent exactement aux extrémités de la ligne et restent entre elles | `err.does_not_fit` |
| 16 | Aucun segment d'un contour ne s'est réduit à néant | `err.tolerance_eats_tooth` |
| 17 | Aucun contour ne se croise lui-même | `err.tolerance_eats_tooth` |
| 18 | Il reste une hauteur de dent | `err.tolerance_eats_tooth` |
| 19 | La hauteur de dent restante vaut au moins 5 % de la profondeur | `err.tolerance_vs_depth` |
| 20 | Le double de la tolérance est inférieur à la largeur | `err.tolerance_vs_width` |

Avec plusieurs lignes, un échec est enveloppé dans `err.on_line`, qui indique la position de la ligne dans la sélection.

Les textes de tous les messages sont listés dans [troubleshooting.md](troubleshooting.md).

### Ce que la boîte de dialogue fait d'un contrôle en échec

- Tant que la boîte de dialogue est ouverte : l'aperçu disparaît et **OK** est grisé. Le texte du message n'est **pas** affiché.
- Si l'exécution elle-même échoue après OK : une boîte de message affiche le texte, et l'exécution est signalée à Fusion comme échouée, afin
  que Fusion annule les lignes déjà dessinées. Cette annulation n'a pas été confirmée dans Fusion.

## Unités

| Où | Unité |
|---|---|
| Champs de la boîte de dialogue pour les longueurs | millimètres |
| Champ de la boîte de dialogue pour l'angle | degrés |
| Nombres dans les messages | millimètres, deux décimales |
| À l'intérieur du programme | centimètres et radians (les unités internes de Fusion) |

Petites valeurs fixes dans le code :

| Valeur | Taille | Usage |
|---|---|---|
| Distance supplémentaire | 0,01 mm | ajoutée à l'entraxe minimal et à la distance aux extrémités de la ligne |
| Segment le plus court | 0,00001 mm | un segment de contour plus court que cela compte comme « sans longueur » |
| Limite d'onglet | 12 × distance de déplacement | au-delà, un angle est considéré comme dérapant |
| Angle de flanc maximal | moins de 89 degrés | |

## La hauteur est ignorée

L'add-in ne lit que les valeurs X et Y des extrémités de la ligne dans l'esquisse et dessine la bande à la hauteur 0 de
l'esquisse. Une ligne dans une esquisse 3D, ou une ligne qui sort du plan d'esquisse, est traitée comme si elle était à plat.

## Ce qui a changé dans la 1.1.0.0

La version 1.1.0.0 a modifié la géométrie (construite d'abord comme 1.0.0.1) :

- Les dents gardent la tolérance plus 0,01 mm de distance par rapport aux extrémités de la ligne. Tout au bout, le contour de la mortaise
  dépassait auparavant la ligne et revenait en arrière, ce qui donnait une boucle qui se croisait elle-même. Le décalage maximal est réduit d'autant.
- Deux dents ont besoin de 0,01 mm d'entraxe en plus. Exactement à l'ancien minimum, un segment du contour n'avait aucune longueur.
- Un contour qui se croiserait lui-même est refusé au lieu d'être dessiné.
- Une exécution échouée est annulée.

Ces modifications ont été testées **hors ligne uniquement**, y compris sur 34 317 contours valides aléatoires, dont aucun ne se croisait lui-même.
Elles ne sont **pas encore confirmées dans Fusion**.
