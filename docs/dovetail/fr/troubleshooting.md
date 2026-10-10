# Dépannage

## OK est grisé

La boîte de dialogue grise **OK** et n'affiche aucun aperçu quand les valeurs ne conviennent pas. **Elle ne dit pas pourquoi.** Les textes
de message ci-dessous existent dans l'add-in, mais ils ne sont affichés dans une boîte de message que si l'exécution elle-même échoue après OK.

Parcourir cette liste de haut en bas :

1. Y a-t-il au moins une ligne sous **Lignes** ?
2. **Largeur (base)**, **Profondeur** et **Tolérance** sont-elles toutes supérieures à 0 ?
3. **Tolérance** est-elle inférieure à la moitié de **Largeur (base)** ?
4. Trapèze : **Angle de flanc** est-il compris entre −89 et 89 degrés ? Avec un angle négatif : la pointe est-elle encore plus large que 0 ?
5. Deux dents ou plus : **Entraxe (centre à centre)** est-il assez grand ? Voir
   [settings.md](settings.md#entraxe-centre-à-centre) pour la formule.
6. La ligne est-elle assez longue pour toutes les dents ? Avec plusieurs lignes, vérifier d'abord la plus courte.
7. Un **Décalage** a-t-il été saisi ? Appuyer sur le bouton **Centrer** de la rangée **Déplacer** pour le remettre à 0.
8. Triangle ou dent très pointue : réduire **Tolérance**, réduire **Profondeur** ou augmenter **Largeur (base)**.
9. Pointe de trapèze étroite avec une grande tolérance : réduire **Tolérance** ou modifier **Angle de flanc**.

Conseil : modifier une seule valeur à la fois. La dernière valeur modifiée est le premier suspect.

## Messages sur les valeurs

Toutes les boîtes de message portent le titre « Queue d'aronde ». `{0}`, `{1}` et `{2}` dans le tableau représentent des nombres ou des textes que
l'add-in insère. Les longueurs dans les messages sont en millimètres.

| Message | Cause | Que faire |
|---|---|---|
| « Sélectionnez au moins une ligne d'esquisse. » | L'exécution a été lancée sans ligne sous **Lignes**. | Cliquer sur au moins une ligne d'esquisse droite. |
| « Ligne {0} sur {1} : {2} » | Plusieurs lignes sont sélectionnées et l'une d'elles ne peut pas recevoir les valeurs. {0} est la position de cette ligne dans l'ordre de sélection, {1} le nombre de lignes, {2} le message proprement dit. | Lire le message après les deux-points et le chercher dans ce tableau. Modifier les valeurs, ou retirer cette ligne de la sélection. |
| « La ligne sélectionnée n'a aucune longueur. » | Le point de départ et le point d'arrivée de la ligne se trouvent au même endroit (vus à plat dans l'esquisse). | Choisir une autre ligne ou l'allonger. |
| « La largeur doit être supérieure à 0. » | **Largeur (base)** vaut 0 ou est négative. | Saisir une largeur supérieure à 0. |
| « La profondeur doit être supérieure à 0. » | **Profondeur** vaut 0 ou est négative. | Saisir une profondeur supérieure à 0. |
| « Une bande fermée exige une tolérance supérieure à 0. » | **Tolérance** vaut 0 ou est négative. La bande est constituée de l'espace ; sans espace, il n'y a pas de bande. | Saisir une tolérance supérieure à 0. |
| « Une géométrie reflétée exige un nombre pair de dents. » | **Refléter la géométrie** est activé et **Nombre** est impair. La boîte de dialogue corrige normalement cela elle-même. | Régler un nombre pair. |
| « Une géométrie reflétée ne fonctionne qu’avec la ligne médiane, la seule où les deux pièces cèdent autant l’une que l’autre. » | **Refléter la géométrie** est activé et **La ligne est** n'est pas la ligne médiane. La boîte de dialogue corrige normalement cela elle-même. | Choisir « Ligne médiane - la moitié de la tolérance de chaque côté » ou désactiver le reflet. |
| « Une géométrie reflétée exige un décalage nul, sinon le motif n’est plus symétrique par rapport au milieu de la ligne. » | **Refléter la géométrie** est activé et **Décalage** n'est pas à 0. La boîte de dialogue corrige normalement cela elle-même. | Mettre le décalage à 0 ou désactiver le reflet. |
| « Au moins une queue d'aronde est nécessaire. » | **Nombre** est inférieur à 1. Le champ de la boîte de dialogue ne le permet pas. | Régler un nombre de 1 ou plus. |
| « L'angle de flanc doit être compris entre -89 et 89 degrés. » | Trapèze : **Angle de flanc** vaut 89 degrés ou plus, ou −89 degrés ou moins. | Saisir un angle dans cette plage. |
| « Angle de flanc trop négatif - la dent se réduit à néant. » | Trapèze avec un angle négatif : les côtés se rejoignent avant que la pointe soit atteinte. | Utiliser un angle moins négatif, moins de profondeur ou plus de largeur. |
| « L'entraxe doit être supérieur à 0. » | Deux dents ou plus et **Entraxe (centre à centre)** vaut 0 ou est négatif. | Saisir un entraxe supérieur à 0. |
| « L'entraxe est trop faible - les queues d'aronde se chevaucheraient. Il faut au moins {0} mm. » | Deux dents ou plus sont trop rapprochées. {0} est l'entraxe minimal pour les valeurs saisies. | Saisir au moins l'entraxe indiqué, ou réduire la largeur, l'angle de flanc ou la tolérance. |
| « Le décalage pousse la denture au-delà de l'extrémité de la ligne. Au maximum +/- {0} mm est possible. » | **Décalage** est plus grand que la ligne ne le permet. {0} est le décalage maximal possible. | Réduire le décalage à la valeur indiquée, ou appuyer sur **Centrer**. |
| « La denture est plus large que la ligne sélectionnée ({0} mm). Réduisez le nombre, la largeur ou l'entraxe. » | Les dents plus la distance aux extrémités de la ligne ne tiennent pas sur la ligne. {0} est la longueur de la ligne. Le même texte apparaît si un contour dépassait une extrémité de la ligne. | Réduire **Nombre**, **Largeur (base)** ou **Entraxe (centre à centre)**, ou utiliser une ligne plus longue. |
| « Le contour d'accouplement dérape dans un angle aigu. Aplatissez la dent (moins de profondeur / plus de largeur) ou réduisez la tolérance. » | Dans un angle très aigu, le contour déplacé partirait loin de la dent (plus de 12 fois la distance de déplacement). | Moins de profondeur, plus de largeur, ou moins de tolérance. |
| « La tolérance dévore toute la dent. Réduisez la tolérance ou augmentez la profondeur. » | Une fois la tolérance retirée, il ne reste rien de la dent, ou un segment du contour se réduit à néant, ou le contour se croiserait lui-même. | Réduire **Tolérance** ou augmenter **Profondeur**. Avec une pointe de trapèze étroite, essayer aussi une largeur plus grande ou un autre angle de flanc. |
| « La tolérance est trop grande par rapport à la profondeur. » | Il reste moins de 5 % de **Profondeur** comme hauteur de dent. | Réduire **Tolérance** ou augmenter **Profondeur**. |
| « La tolérance est trop grande par rapport à la largeur. » | Le double de **Tolérance** est aussi grand que **Largeur (base)** ou plus grand. | Réduire **Tolérance** ou augmenter **Largeur (base)**. |
| « Le contour est dégénéré. » | Un filet de sécurité : le contour a trop peu de points, ou les deux contours n'ont pas le même nombre de points. Avec les autres contrôles en place, cela ne devrait pas apparaître en usage normal. | Modifier légèrement les valeurs. Si le message réapparaît, le signaler avec les valeurs utilisées. |

## Messages sur le programme

Ces messages contiennent un rapport d'erreur technique (un « traceback ») à la place de `{0}`. Ils signifient une erreur inattendue,
pas une valeur incorrecte.

| Message | Quand | Que faire |
|---|---|---|
| « Aucun panneau de barre d'outils approprié n'a été trouvé. » | Au démarrage. Aucun des trois emplacements de la barre d'outils n'existe dans ce Fusion (voir [installation.md](installation.md#premier-démarrage-dans-fusion)). Le bouton n'est pas créé. | Mettre Fusion à jour. Si le message persiste, le signaler avec la version de Fusion. |
| « Erreur lors de la création de la géométrie : {0} » | Après OK, une erreur inattendue s'est produite pendant le dessin. L'exécution est signalée à Fusion comme échouée. | Vérifier l'esquisse ; utiliser Undo si des lignes sont restées. Réessayer. Si cela se répète, signaler le texte complet. |
| « Erreur lors de la construction de la boîte de dialogue : {0} » | La boîte de dialogue n'a pas pu être construite au clic sur le bouton. | Arrêter puis démarrer l'add-in. Vérifier que les dossiers `lang` et `resources` sont complets. Si cela se répète, signaler le texte complet. |
| « Échec du démarrage : {0} » | L'add-in n'a pas pu démarrer. | Vérifier que le dossier est entièrement décompressé et nommé `Dovetail`. Le réinstaller. Si cela se répète, signaler le texte complet. |
| « Échec de l'arrêt : {0} » | L'add-in n'a pas pu être arrêté proprement. | Redémarrer Fusion. |

Signalements : <https://github.com/sorglos-it/fusion360/issues>

## Autres problèmes

| Problème | Cause | Que faire |
|---|---|---|
| Pas de bouton après l'installation | L'add-in ne fonctionne pas, ou le dossier est imbriqué un niveau trop bas | Suivre de nouveau [installation.md](installation.md) ; vérifier que `AddIns/Dovetail/Dovetail.py` existe |
| Une ligne ne peut pas être cliquée dans la boîte de dialogue | Seules les lignes d'esquisse droites sont acceptées | Utiliser une ligne droite ; les arcs, les cercles et les splines ne sont pas pris en charge |
| La bande montre deux zones au lieu d'une | La ligne d'origine traverse encore la bande comme une ligne normale | Cocher **Convertir la ligne d'origine en géométrie de construction**, ou convertir la ligne en géométrie de construction à la main |
| L'aperçu montre encore la ligne d'origine comme une ligne normale | L'aperçu ne modifie jamais la ligne d'origine | Rien ; la ligne est convertie à l'appui sur OK |
| Les dents sont du mauvais côté | Le côté dépend du sens dans lequel la ligne a été dessinée | Cocher **Inverser la direction** |
| Certaines lignes ont les dents d'un côté, d'autres de l'autre | Les lignes ont été dessinées dans des sens opposés | Exécuter la commande séparément pour les deux groupes, une fois avec et une fois sans **Inverser la direction** |
| Les boutons **Déplacer** ne font rien | **Pas de déplacement** vaut 0, ou la limite est atteinte, ou **Refléter la géométrie** est activé | Régler un pas de déplacement, ou vérifier la place sur la ligne |
| **Décalage**, **La ligne est**, **Pas de déplacement** sont grisés | **Refléter la géométrie** est coché | Retirer la coche |
| La mauvaise langue est affichée | La langue est choisie au démarrage de l'add-in ; les langues autres que les cinq prises en charge retombent sur l'anglais | Voir [settings.md](settings.md#langue) |
| Les valeurs sont revenues aux valeurs par défaut | Elles ne sont mémorisées que tant que Fusion fonctionne | Les saisir de nouveau |

## Limites connues

- **Aucune raison n'est affichée quand OK est grisé.** Les textes de message ne sont affichés que si l'exécution elle-même échoue.
- **La hauteur est ignorée.** Les lignes dans une esquisse 3D ou les lignes hors du plan d'esquisse sont traitées comme si elles étaient à plat.
- **Lignes droites uniquement.** Les arcs, les cercles et les splines ne peuvent pas être sélectionnés.
- **Un seul jeu de valeurs pour toutes les lignes.** Avec plusieurs lignes, chaque ligne reçoit les mêmes valeurs. Il n'y a pas de réglage par
  ligne.
- **Au plus 100 lignes et 500 dents par ligne.**
- **Un triangle ne s'accroche pas.** Seul le trapèze avec un angle de flanc positif résiste à la séparation.
- **La tolérance est un espace, rien de plus.** L'add-in ne compense pas les effets du procédé de fabrication.
- **Non confirmé dans Fusion :** les modifications de géométrie de la version 1.1.0.0 (distance aux extrémités de la ligne, entraxe
  minimal plus grand, refus des contours qui se croisent eux-mêmes, annulation après une exécution échouée). Elles ont été testées hors ligne uniquement.
