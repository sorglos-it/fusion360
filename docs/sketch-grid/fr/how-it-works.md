# Fonctionnement

## Fichiers

L'add-in installé est un seul dossier, `SketchGrid` :

| Fichier | Rôle |
| --- | --- |
| `SketchGrid.py` | L'add-in lui-même : boîte de dialogue, calcul de la grille, contrôles, dessin. |
| `sketchgrid_core.py` | Fonctions d'aide communes qui ne sont pas propres à cet add-in : lire les fichiers de langue, trouver la langue, trouver le panneau de barre d'outils, garder en vie les gestionnaires d'événements, afficher les erreurs inattendues, lire la version. |
| `SketchGrid.manifest` | Description pour Fusion : auteur, version, systèmes pris en charge (Windows et macOS), démarrage avec Fusion. |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Tous les textes, un fichier par langue. `en.xml` est la référence. |
| `resources/SketchGrid/16x16.png`, `32x32.png`, `64x64.png` | L'icône du bouton en trois tailles. |

L'add-in ne lit que son propre dossier. Il n'écrit aucun fichier et n'ouvre aucune connexion réseau.

## Démarrage et arrêt

Au démarrage (`run`) :

1. La langue est détectée et le fichier de langue correspondant est chargé.
2. Une définition de commande restée d'un démarrage précédent est supprimée.
3. La commande est créée. Son nom est le texte **Grille d'esquisse** suivi de la version du manifeste entre parenthèses.
4. L'add-in cherche un panneau de barre d'outils : d'abord le panneau portant l'id `SketchCreatePanel`, puis `SolidCreatePanel` ; chacun d'abord dans l'espace de travail Design, puis parmi tous les panneaux. S'il n'en existe aucun, le message « Aucun panneau de barre d'outils approprié n'a été trouvé. » apparaît et aucun bouton n'est ajouté.
5. Le bouton est ajouté au panneau et affiché directement sur la barre d'outils.

À l'arrêt (`stop`), le bouton et la commande sont retirés et les gestionnaires d'événements sont libérés.

## Ce qui se passe tant que la boîte de dialogue est ouverte

| Événement | Ce que fait l'add-in |
| --- | --- |
| La boîte de dialogue s'ouvre | Construit tous les champs avec les valeurs mémorisées. Essaie de reprendre un point d'esquisse sélectionné au préalable. Si cela échoue, la boîte de dialogue reste utilisable et le point est sélectionné dans la boîte de dialogue. (Testé hors ligne uniquement, pas dans Fusion.) |
| Un champ change | Affiche ou masque les champs qui appartiennent au mode et à la forme choisis. Recalcule la ligne **Résultat**. |
| Fusion demande si les saisies sont valides | Exécute tous les contrôles. Si l'un échoue, **OK** est désactivé. |
| Fusion demande un aperçu | Exécute tous les contrôles et dessine la grille en aperçu. Si un contrôle échoue, rien n'est dessiné et rien n'est signalé. |
| **OK** | Exécute de nouveau tous les contrôles, dessine la grille, puis mémorise les valeurs. |

L'aperçu n'est pas réutilisé comme résultat final. À l'appui sur **OK**, la grille est dessinée de nouveau.

## Unités

- En interne, toutes les longueurs sont en centimètres. C'est l'unité interne de Fusion, quelle que soit l'unité affichée par le document.
- Les champs de longueur de la boîte de dialogue sont créés avec l'unité `mm`.
- Pour la ligne **Résultat** et pour les messages, les valeurs sont converties en millimètres (× 10) et affichées avec deux décimales.
- Les comparaisons admettent une tolérance minuscule de 0,000000001 cm, pour que le bruit d'arrondi ne déclenche pas de message.

## Comment la grille est calculée

Le calcul est fait par `grid_layout()`. Il n'utilise aucune fonction de Fusion.

### Étape 1 : taille d'une forme

Normalement, une forme occupe exactement longueur × profondeur.

Exception : un polygone avec **Régulier** coché. Il prend moins de place. Sa taille réelle est mesurée :

1. Les sommets du polygone sont placés sur un cercle de rayon 1, le premier sommet pointant vers le haut.
2. La largeur et la hauteur du plus petit rectangle autour de ces sommets sont mesurées.
3. Les deux sont multipliées par la moitié de la plus petite des deux valeurs, longueur et profondeur.

Exemple : 6 côtés, longueur 10 mm, profondeur 5 mm donnent 4,33 × 5,00 mm.

### Étape 2 : pas

Le pas est la distance entre une forme et le même endroit sur la forme suivante.

- pas X = taille d'une forme en X + **Écart X**
- pas Y = taille d'une forme en Y + **Écart Y**

### Étape 3 : nombre de colonnes et de lignes

**Colonnes et lignes :** les nombres de la boîte de dialogue sont utilisés.

**Remplissage d'une zone :** n formes ont besoin de n tailles et de n − 1 écarts. Donc :

- colonnes = (largeur de la zone + écart X) ÷ pas X, arrondi à l'entier inférieur
- lignes = (hauteur de la zone + écart Y) ÷ pas Y, arrondi à l'entier inférieur

Exemple : (100 + 2) ÷ 12 = 8,5, donc 8 colonnes.

Si colonnes × lignes dépasse 2000, la grille est refusée.

### Étape 4 : taille totale

- largeur totale = colonnes × pas X − écart X
- hauteur totale = lignes × pas Y − écart Y

Exemple : 8 × 12 − 2 = 94 mm.

### Étape 5 : position (point d'ancrage et décalage)

Le point d'ancrage est l'entrée choisie dans **Le point est dans la grille**. Chaque entrée correspond à deux facteurs entre 0 et 1 : la distance du point au bord gauche et au bord inférieur de la grille, en proportion de la taille totale.

| Entrée | Facteur X | Facteur Y |
| --- | --- | --- |
| Au centre | 0,5 | 0,5 |
| En bas à gauche | 0 | 0 |
| En bas à droite | 1 | 0 |
| En haut à gauche | 0 | 1 |
| En haut à droite | 1 | 1 |
| En bas au centre | 0,5 | 0 |
| En haut au centre | 0,5 | 1 |
| À gauche au centre | 0 | 0,5 |
| À droite au centre | 1 | 0,5 |

Le coin inférieur gauche de la grille, mesuré à partir du point sélectionné :

- X = −facteur X × largeur totale + **Décalage X**
- Y = −facteur Y × hauteur totale + **Décalage Y**

Exemple : grille de 94 × 26 mm, **Au centre**, sans décalage : le coin inférieur gauche se trouve à 47 mm à gauche et à 13 mm en dessous du point.

Les décalages ne sont ajoutés qu'à ce stade. Ils ne changent pas le nombre de formes, pas non plus dans le mode **Remplissage d'une zone**.

### Étape 6 : les formes une à une

`cell_centres()` parcourt la grille ligne par ligne, de la ligne du bas vers le haut, et dans chaque ligne de gauche à droite. Pour chaque forme, elle renvoie le coin inférieur gauche de son emplacement :

- X = coin de la grille X + numéro de colonne × pas X
- Y = coin de la grille Y + numéro de ligne × pas Y

Les numéros de colonne et de ligne commencent à 0. Le nom de la fonction est historique ; elle renvoie des coins, pas des centres.

Le code de dessin ajoute la moitié de la taille d'une forme pour obtenir le centre, et ajoute la position du point sélectionné dans l'esquisse.

Toutes les positions sont dans les coordonnées de l'esquisse à laquelle le point appartient. La grille est donc toujours parallèle aux axes X et Y de cette esquisse.

## Comment chaque forme est dessinée

| Forme | Cas | Dessinée comme |
| --- | --- | --- |
| Rectangle | coins **Vifs** | le rectangle par deux points de Fusion, du coin inférieur gauche au coin supérieur droit |
| Rectangle | **Arrondis**, rayon égal à la moitié des deux côtés | un cercle |
| Rectangle | **Arrondis**, sinon | jusqu'à 4 lignes et 4 arcs |
| Rectangle | **Chanfreinés** | jusqu'à 4 lignes pour les côtés et 4 lignes pour les coupes |
| Cercle / ellipse | la longueur est égale à la profondeur | un cercle |
| Cercle / ellipse | sinon | une ellipse ; la plus longue des deux valeurs est donnée à Fusion comme axe principal, car sinon Fusion rejette l'ellipse |
| Trou oblong | la longueur est égale à la profondeur | un cercle |
| Trou oblong | sinon | 2 lignes et 2 arcs en demi-cercle ; les arcs se trouvent aux deux extrémités de la direction la plus longue, leur rayon est la moitié de la plus courte |
| Polygone | toujours | une ligne par côté |

Détails :

- **Rectangle arrondi ou chanfreiné :** `corner_outline()` renvoie le contour sous forme d'une liste de lignes et d'arcs, parcourue dans le sens inverse des aiguilles d'une montre à partir du bord inférieur. Chaque arc est donné par trois points : début, un point au milieu de l'arc, fin. Quand le rayon ou le chanfrein vaut exactement la moitié d'un côté, le segment droit de ce côté n'a aucune longueur et il est omis.
- **Polygone :** le premier sommet pointe vers le haut. Sans **Régulier**, les sommets sont étirés pour que le plus petit rectangle autour d'eux mesure exactement longueur × profondeur. Avec **Régulier**, les deux directions sont mises à l'échelle par la moitié de la plus petite des deux valeurs, longueur et profondeur. Dans les deux cas, le polygone est centré sur son propre rectangle, pas sur son cercle. Cela compte pour les nombres de côtés impairs : une forme à cinq côtés a un sommet en haut mais un bas plat.
- **Liaison des courbes :** le polygone est dessiné comme une chaîne. Chaque ligne commence au point d'arrivée de la ligne précédente, et la dernière se referme sur le point de départ de la première. Le trou oblong et le rectangle arrondi ou chanfreiné sont dessinés autrement : chaque ligne et chaque arc est créé séparément à partir de coordonnées. Leurs extrémités se trouvent au même endroit, mais elles ne sont pas créées comme des points partagés. Voir [limites connues](troubleshooting.md#limites-connues).
- L'add-in lui-même n'ajoute ni cotes ni contraintes. Ce n'est pas l'add-in qui décide si Fusion en ajoute de son côté au rectangle par deux points.

Pendant le dessin de la grille, l'esquisse reçoit l'ordre de ne pas se recalculer après chaque courbe (`isComputeDeferred`). Elle se recalcule une fois à la fin. Le réglage est rétabli dans tous les cas, même après une erreur.

## Les contrôles

Ordre dans lequel les contrôles s'exécutent :

1. Exactement un point d'esquisse est sélectionné.
2. Si la forme est un polygone : côtés entre 3 et 24.
3. Longueur supérieure à 0.
4. Profondeur supérieure à 0.
5. Aucun des deux écarts n'est négatif.
6. Mode **Remplissage d'une zone** : les deux valeurs de la zone supérieures à 0 ; ensuite, au moins une colonne et une ligne tiennent.
7. Mode **Colonnes et lignes** : au moins une colonne, au moins une ligne.
8. Colonnes × lignes au plus 2000.
9. Si la forme est un rectangle et que les coins ne sont pas **Vifs** : rayon / chanfrein supérieur à 0, et au plus la moitié du côté le plus court. Une valeur trop grande est refusée, pas réduite en silence.

Le premier contrôle qui échoue décide du message. Les textes sont listés dans [troubleshooting.md](troubleshooting.md).

La ligne **Résultat** n'exécute que les contrôles 3 à 9. Un échec du contrôle 1 ou 2 désactive donc **OK** sans texte dans la ligne **Résultat**.

## Textes et langue

- Chaque fichier de langue est une liste de clés et de textes. Le code ne connaît que les clés.
- Les emplacements des valeurs sont écrits `{0}`, `{1}` et ainsi de suite dans les textes et sont remplis par l'add-in.
- L'anglais est chargé en premier comme repli. Une clé qui manque dans la langue active est prise dans l'anglais. Une clé absente partout est affichée telle quelle, sous forme de clé.
- Comment la langue est choisie : voir [settings.md](settings.md#langue).
