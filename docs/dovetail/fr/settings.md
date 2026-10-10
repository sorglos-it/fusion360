# Réglages

L'add-in n'a ni fichier de réglages ni page de réglages. Tout se règle dans la boîte de dialogue de la commande.
Les champs sont listés dans l'ordre où la boîte de dialogue les affiche.

## Champs de la boîte de dialogue

| Champ | Signification | Valeur par défaut | Valeurs autorisées |
|---|---|---|---|
| **Lignes** | Les lignes d'esquisse qui reçoivent un assemblage. Texte d'invite : « Sélectionner une ou plusieurs lignes d'esquisse ». | les lignes sélectionnées avant le lancement de la commande | 1 à 100 lignes d'esquisse droites |
| **Nombre** | Nombre de dents par ligne | 1 | nombre entier, 1 à 500 |
| **Refléter la géométrie** | Rend les deux pièces identiques, voir [usage.md](usage.md#deux-pièces-identiques--refléter-la-géométrie) | désactivé | activé / désactivé |
| **Forme** | Forme de la dent | Trapèze (queue d'aronde) | Trapèze (queue d'aronde), Triangle, Rectangle (assemblage à peigne) |
| **Largeur (base)** | Largeur de la dent là où elle rejoint la ligne | 10 mm | supérieure à 0, et supérieure au double de la tolérance |
| **Profondeur** | De combien la dent dépasse de la ligne | 6 mm | supérieure à 0 |
| **Angle de flanc** | Trapèze seulement : de combien chaque côté de la dent penche vers l'extérieur | 15 deg | plus de −89 et moins de 89 degrés ; voir plus bas |
| **Entraxe (centre à centre)** | Distance entre le milieu d'une dent et le milieu de la suivante. Utilisé seulement avec 2 dents ou plus. | 20 mm | supérieur à 0 et au moins égal à l'entraxe minimal, voir plus bas |
| **Décalage** | Déplacement de tout le groupe de dents le long de la ligne. Positif : vers le point d'arrivée. | 0 mm, à chaque fois | entre moins et plus le décalage maximal, voir plus bas |
| **Pas de déplacement** | De combien un clic sur un bouton **Déplacer** déplace les dents | 1 mm | non contrôlé par l'add-in, voir plus bas |
| **Déplacer** | Trois boutons : **Vers la gauche (vers le point de départ)**, **Centrer**, **Vers la droite (vers le point d'arrivée)** | – | – |
| **Tolérance** | Espace entre les deux pièces | 0,25 mm | supérieure à 0 ; autres limites plus bas |
| **La ligne est** | Quelle pièce cède de la matière pour l'espace | Ligne médiane - la moitié de la tolérance de chaque côté | les trois entrées listées plus bas |
| **Inverser la direction** | Place les dents de l'autre côté de la ligne | désactivé | activé / désactivé |
| **Convertir la ligne d'origine en géométrie de construction** | Convertit la ligne sélectionnée en ligne auxiliaire à l'appui sur OK | activé | activé / désactivé |

Entrées de **La ligne est** :

| Entrée | La mortaise grandit de | Le tenon rétrécit de |
|---|---|---|
| **Ligne médiane - la moitié de la tolérance de chaque côté** | la moitié de la tolérance | la moitié de la tolérance |
| **Bord de la mortaise - toute la tolérance sur le tenon** | rien | toute la tolérance |
| **Bord du tenon - toute la tolérance sur la mortaise** | toute la tolérance | rien |

## Champs grisés

| Champ | Grisé quand |
|---|---|
| **Angle de flanc** | **Forme** n'est pas Trapèze (queue d'aronde). La valeur est alors ignorée. |
| **Entraxe (centre à centre)** | **Nombre** vaut 1. La valeur est alors ignorée. |
| **La ligne est**, **Décalage**, **Pas de déplacement**, **Déplacer** | **Refléter la géométrie** est coché |

## Les limites en détail

Toutes les limites viennent du code. Les longueurs ci-dessous sont en millimètres.

La « demi-largeur de pointe » sert dans plusieurs limites. Elle dépend de la forme :

| Forme | Demi-largeur de pointe |
|---|---|
| Rectangle (assemblage à peigne) | Largeur ÷ 2 |
| Triangle | 0 |
| Trapèze (queue d'aronde) | Largeur ÷ 2 + Profondeur × tan(Angle de flanc) |

La « moitié la plus large » est la plus grande des deux valeurs Largeur ÷ 2 et demi-largeur de pointe.

### Angle de flanc

- Doit être supérieur à −89 et inférieur à 89 degrés. Exactement 89 ou −89 est refusé.
- Avec un angle négatif, la pointe devient plus étroite. La demi-largeur de pointe doit rester supérieure à 0. Sinon, la dent se
  réduirait à néant et elle est refusée.
- 0 degré donne un rectangle.

### Entraxe (centre à centre)

Contrôlé seulement avec 2 dents ou plus.

Entraxe minimal = 2 × moitié la plus large + 2 × Tolérance + 0,01 mm

Exemple avec les valeurs par défaut (Largeur 10 mm, Profondeur 6 mm, Angle de flanc 15 deg, Tolérance 0,25 mm) :
la demi-largeur de pointe vaut environ 6,61 mm, l'entraxe minimal vaut donc environ 13,73 mm.

### Place sur la ligne

Les dents doivent garder une distance par rapport aux deux extrémités de la ligne : la tolérance plus 0,01 mm.

Longueur nécessaire = (Nombre − 1) × Entraxe + 2 × moitié la plus large + 2 × (Tolérance + 0,01 mm)

Exemple avec les valeurs par défaut et une dent : il faut environ 13,74 mm de ligne.

### Décalage

Décalage maximal = Longueur de la ligne ÷ 2 − ( (Nombre − 1) ÷ 2 × Entraxe + moitié la plus large + Tolérance + 0,01 mm )

- Le décalage peut se situer entre moins et plus cette valeur.
- Les boutons **Déplacer** s'arrêtent à cette valeur. Avec plusieurs lignes, la ligne la plus courte décide.
- Un décalage saisi n'est pas corrigé. S'il est trop grand, OK est grisé.
- Avec **Refléter la géométrie**, le décalage doit valoir 0.

### Tolérance

- Doit être supérieure à 0. La bande est constituée de l'espace ; à 0, il n'y a pas de bande.
- Le double de la tolérance doit être inférieur à **Largeur (base)**.
- Une fois la tolérance retirée, il doit rester au moins 5 % de **Profondeur** comme hauteur de dent. Cela compte surtout pour
  les dents pointues, dont la pointe perd plus de hauteur que la tolérance.
- La bande ne doit pas se croiser elle-même et aucun de ses segments ne doit se réduire à néant. Cela peut arriver avec des pointes de trapèze
  étroites et une grande tolérance.
- Dans un angle aigu, l'angle décalé ne doit pas s'éloigner de plus de 12 fois la distance de décalage.

### Nombre

- 1 à 500.
- Avec **Refléter la géométrie**, le nombre doit être pair. La boîte de dialogue augmente de 1 un nombre impair.

### Pas de déplacement

L'add-in ne contrôle pas cette valeur. D'après le code : à 0, les boutons **Déplacer** ne font rien ; une valeur négative
inverse le sens des boutons gauche et droite.

### Lignes

- Seules des lignes d'esquisse droites peuvent être sélectionnées.
- Au moins 1, au plus 100.
- Une ligne doit avoir une longueur supérieure à 0.

## Unités

- Les champs de longueur sont affichés en millimètres, l'angle en degrés.
- Les nombres dans les messages d'erreur sont toujours en millimètres avec deux décimales.
- En interne, l'add-in calcule en centimètres et en radians, les unités que Fusion utilise en interne.

## Ce qui est mémorisé

L'add-in mémorise les valeurs de la dernière exécution terminée par **OK** et réussie.

| Mémorisé | Non mémorisé |
|---|---|
| Nombre | Lignes |
| Refléter la géométrie | Décalage (repart toujours de 0) |
| Forme | |
| Largeur (base) | |
| Profondeur | |
| Angle de flanc | |
| Entraxe (centre à centre) | |
| Pas de déplacement | |
| Tolérance | |
| La ligne est | |
| Inverser la direction | |
| Convertir la ligne d'origine en géométrie de construction | |

Pendant combien de temps :

- Les valeurs sont gardées en mémoire uniquement. Rien n'est écrit sur le disque.
- Elles durent le temps de la session Fusion en cours. Après la fermeture de Fusion, les valeurs par défaut du tableau ci-dessus s'appliquent de nouveau.
- Fermer la boîte de dialogue avec Cancel ne modifie pas les valeurs mémorisées.

Le décalage est laissé de côté volontairement : il appartient à la ligne en cours, pas aux réglages.

## Langue

L'add-in a des textes en cinq langues : allemand, anglais, espagnol, français, italien.

La langue est choisie une seule fois, au démarrage de l'add-in :

1. La langue réglée dans les préférences de Fusion (langue de l'utilisateur) est utilisée si elle fait partie des cinq.
2. Sinon, l'add-in regarde les variables d'environnement `LANG`, `LANGUAGE` et `LC_ALL`, dans cet ordre.
3. Si cela ne donne rien, il regarde la langue du système d'exploitation.
4. Si cela ne donne rien non plus, l'anglais est utilisé.

Il n'y a pas de sélecteur de langue dans la boîte de dialogue. Après un changement de langue dans Fusion, l'add-in doit être démarré
de nouveau (redémarrer Fusion le fait).

Si un seul texte manque dans un fichier de langue, le texte anglais est affiché à sa place.
