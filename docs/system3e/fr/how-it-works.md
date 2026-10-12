# Fonctionnement

Retour à la [vue d'ensemble](index.md).

## Les fichiers du complément

Le dossier installé `System3E` contient :

| Fichier ou dossier | Rôle |
| --- | --- |
| `System3E.py` | La commande : boîte de dialogue, placement, points |
| `system3e_core.py` | Aides générales : langue, bouton de barre d'outils, messages d'erreur, version |
| `System3E.manifest` | Indique à Fusion le nom, l'auteur, la version et le fait que le complément démarre avec Fusion |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Tous les textes, un fichier par langue |
| `blocks/blocks.json` | La bibliothèque d'éléments : la forme des 74 éléments |
| `blocks/<id>.png` | Une image d'aperçu par élément, 74 au total |
| `resources/System3E/16x16.png`, `32x32.png`, `64x64.png` | L'icône du bouton |

Le complément ne lit que ces fichiers. Il n'écrit aucun fichier et n'ouvre aucune connexion réseau.

## Démarrage et arrêt

Quand le complément démarre :

1. Il détecte la langue (voir [settings.md](settings.md)) et charge les textes.
2. Il supprime une définition de bouton restée d'une exécution précédente, s'il y en a une.
3. Il crée le bouton **Élément SYSTEM 3E**. La version du manifeste est ajoutée entre parenthèses.
4. Il cherche le panneau **Create** des outils de solide dans l'espace de travail de conception et y place le
   bouton. Si le panneau est introuvable, il affiche un message et n'ajoute aucun bouton.

Quand le complément s'arrête, il retire le bouton.

## La bibliothèque d'éléments

`blocks/blocks.json` est un fichier texte au format JSON. Il contient :

- `unit` : toujours `mm`. Toutes les longueurs du fichier sont en millimètres.
- `blocks` : une liste de 74 éléments dans l'ordre du catalogue.

Chaque élément a ces entrées :

| Entrée | Contenu | Exemple |
| --- | --- | --- |
| `id` | Nom court pour les fichiers, en minuscules | `s1-wp` |
| `name` | Nom du catalogue | `S1 WP` |
| `family` | L'une des valeurs `starter`, `basic`, `complementary`, `lintel`, `window`, `top`, `corner`, `partition` | `basic` |
| `size` | Longueur, largeur, hauteur en mm entiers | `[707, 352, 300]` |
| `stack` | Hauteur à laquelle repose le rang suivant, en mm | `250.0` |
| `points` | Les sommets de la forme, chacun sous la forme x, y, z en mm | `[0.0, 271.0, 200.0]` |
| `faces` | Les faces planes. Chacune a une direction (`normal`) et un ou plusieurs contours (`loops`). | – |

Un contour est une liste de nombres. Chaque nombre désigne l'un des `points`. Le premier contour d'une face est sa
bordure extérieure. Les contours suivants sont des trous dans la face.

Chaque élément repose avec son coin le plus bas en 0, 0, 0. Sa longueur suit x, sa largeur (l'épaisseur du mur)
suit y, sa hauteur suit z.

La bibliothèque est lue une seule fois, à la première ouverture de la boîte de dialogue. L'image d'aperçu d'un
élément est le fichier `blocks/<id>.png`.

## Comment un corps est construit

Les éléments ne sont pas enregistrés sous forme de fichiers Fusion. Le complément construit chaque corps à partir
des points et des faces :

1. Chaque point de l'élément devient un sommet du corps.
2. Chaque face devient une face plane. Sa position vient de son premier point et de sa direction.
3. Chaque contour devient une chaîne fermée d'arêtes droites.
4. Chaque arête est définie une seule fois et utilisée par ses deux faces voisines, dans des sens opposés. Cela
   rend le corps fermé (un solide).
5. Fusion vérifie entièrement le résultat et crée le corps. Si Fusion le refuse, le complément affiche le message
   « L'élément {0} n'a pas pu être créé : » avec la raison donnée par Fusion.

Toutes les faces sont planes et toutes les arêtes sont droites. Il n'y a pas de surfaces courbes.

## Composants et réutilisation

Quand on appuie sur **OK** :

1. Le complément passe en revue tous les éléments déjà présents dans la conception. Les points qui manquent sont
   ajoutés. Les points qui ne sont pas à leur place sont retirés et créés à nouveau. Les éléments placés par une
   version plus ancienne sont ainsi mis à jour.
2. Le complément cherche dans la conception un composant de cet élément.
   - Il cherche une marque invisible (un attribut Fusion, groupe `System3E`, nom `block`) portant l'`id` de l'élément.
   - Les éléments placés avant l'existence de la marque sont retrouvés par le nom `SYSTEM 3E <name>`.
   - Les composants sans corps et les composants d'une conception liée sont ignorés.
3. **Trouvé :** le complément insère une autre copie de ce composant au nouvel endroit.
4. **Non trouvé :** le complément construit le corps, crée un nouveau composant nommé `SYSTEM 3E <name>` au niveau
   supérieur de la conception, le marque, y place le corps nommé `<name>` et ajoute les douze points.

Comme les éléments identiques sont des copies d'un seul composant, une liste de pièces les compte ensemble.

Dans une conception avec chronologie (Fusion appelle cela une conception paramétrique), un corps tout prêt doit
arriver à l'intérieur d'une « fonction de base ». Le complément en crée une, y place le corps et les points, puis
la ferme. Dans une conception sans chronologie, le corps et les points sont ajoutés directement.

Si quelque chose échoue pendant la création d'un élément, le complément indique à Fusion que la commande a échoué.
Fusion annule alors ce qui avait été construit jusque-là.

## Les points de construction

Chaque composant reçoit douze points de construction. Avec L = longueur, W = largeur et S = `stack` de l'élément,
ils représentent ces endroits dans les coordonnées propres de l'élément (mm) :

| Nom | x | y | z |
| --- | --- | --- | --- |
| dessous avant | 0 | W/2 | 0 |
| dessous milieu | L/2 | W/2 | 0 |
| dessous arrière | L | W/2 | 0 |
| dessus avant | 0 | W/2 | S |
| dessus milieu | L/2 | W/2 | S |
| dessus arrière | L | W/2 | S |
| dessus milieu droite | L/2 | 0 | S |
| dessus milieu gauche | L/2 | W | S |
| dessous milieu droite | L/2 | 0 | 0 |
| dessous milieu gauche | L/2 | W | 0 |
| milieu droite, 50 mm plus haut | L/2 | 0 | 50 |
| milieu gauche, 50 mm plus haut | L/2 | W | 50 |

Les trois coins proposés sous **Poser par** ne sont pas des points de construction. Avec H = hauteur, ils se
trouvent en :

| Entrée | x | y | z |
| --- | --- | --- | --- |
| Coin inférieur avant droit | 0 | 0 | 0 |
| Coin supérieur avant droit | 0 | 0 | H |
| Coin supérieur avant gauche | 0 | W | H |

Ces endroits viennent des dimensions extérieures. Sur un élément qui a une languette, une rainure ou un évidement,
un tel endroit peut être dans la matière, où le point ne se voit pas, ou dans le vide. Le point est alors montré
ailleurs :

1. juste au-dessus ou juste au-dessous, sur la face la plus proche ;
2. s'il n'y a pas de face au-dessus ni au-dessous, ou si un autre point s'y trouve déjà : dans la longueur ;
3. sinon à l'endroit le plus proche sur la surface, puis en travers du mur.

Exemple `S1 WP` : « dessus milieu » représente la hauteur 250 mm et est montré sur le dessus de la languette, à
300 mm. « dessous milieu » représente la hauteur 0 et est montré dans la rainure, à 50 mm. Sur les demi-éléments
d'angle `SNL/2` et `SNP/2`, il ne reste aucun endroit libre pour « dessous milieu gauche » ; il reste dans le vide.

Chaque point porte des marques invisibles (groupe d'attributs `System3E`) :

| Nom | Contenu |
| --- | --- |
| `point` | La clé du point. Grâce à elle, le complément sait quels points un composant possède déjà. |
| `shift` | Le chemin entre l'endroit où le point est montré et l'endroit qu'il représente, en mm. |
| `asis` | Posée quand Fusion a mis le point ailleurs et que cela n'a pas pu être corrigé. Un tel point est laissé tel quel. |

Quand on clique sur l'un de ces points, le complément ajoute `shift` et place ainsi d'après l'endroit que le point
représente. Un mur à joints décalés donne donc le même résultat, où que le point soit montré.

Après la création d'un point, le complément relit où Fusion l'a mis. Pour un nouveau type d'élément placé loin de
l'origine, Fusion prenait les coordonnées pour celles de la conception entière ; les points se trouvaient alors à
côté de l'élément. Dans ce cas, le complément trouve la copie du composant dont le placement explique l'écart,
retire le point et le crée à nouveau avec des coordonnées corrigées.

Le point appartient au composant. Chaque copie d'un élément montre donc les mêmes douze points à son propre
emplacement.

## Comment l'emplacement est calculé

1. L'endroit choisi sous **Poser par** est amené à l'origine.
2. L'élément est tourné autour de l'axe Z de la valeur de **Rotation**.
3. L'élément est déplacé vers le point cliqué plus **Décalage X**, **Décalage Y**, **Décalage Z**.
   Sans point cliqué, l'origine (0, 0, 0) est utilisée.

Les décalages sont appliqués après la rotation. Ils suivent donc les axes de la conception, pas ceux de l'élément
tourné.

La position d'un point d'esquisse cliqué est prise dans les coordonnées de la conception entière, pas dans celles
de son esquisse. La position d'un point de construction cliqué est calculée à partir du point dans son composant et
du placement de la copie sur laquelle on a cliqué.

## Unités

| Où | Unité |
| --- | --- |
| Bibliothèque d'éléments `blocks.json` | mm |
| Champs **Décalage X**, **Décalage Y**, **Décalage Z** | affichés en mm |
| Champ **Rotation** | affiché en degrés |
| Dans l'interface de programmation de Fusion | cm et radians |

Le complément divise chaque valeur de la bibliothèque par 10 quand il la transmet à Fusion. Il n'y a rien à
convertir soi-même.

## L'aperçu

Tant que la boîte de dialogue est ouverte, Fusion demande un aperçu au complément après chaque modification. Le
complément exécute alors les mêmes étapes que pour **OK**. Fusion rejette cet aperçu et exécute à nouveau les
étapes quand on appuie sur **OK**.
Les erreurs pendant l'aperçu ne sont pas affichées.
