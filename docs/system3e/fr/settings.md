# Réglages

Retour à la [vue d'ensemble](index.md).

Le complément n'a ni page de réglages ni fichier de réglages. Tout ce qui peut être réglé se trouve dans la boîte
de dialogue de la commande **Élément SYSTEM 3E**.

## Les champs de la boîte de dialogue

| Champ | Signification | Valeur par défaut | Valeurs autorisées |
| --- | --- | --- | --- |
| **Point** | L'endroit prévu pour l'élément. | Vide, ou le point qui était sélectionné avant l'appui sur le bouton. | Rien ou exactement un point : un point d'esquisse, un coin d'un corps ou un point de construction. Rien signifie l'origine de la conception. |
| **Famille** | Le groupe d'éléments affiché sous **Élément**. | Base | Départ, Base, Complément, Linteau, Cadre de fenêtre, Couronnement, Angle, Cloison |
| **Élément** | L'élément à placer, avec sa taille en mm (longueur x largeur x hauteur). | S1 WP | Les éléments de la famille choisie. Voir les listes dans [usage.md](usage.md). |
| (image) | Montre l'élément choisi. Ne peut pas être modifiée. | Image de l'élément choisi | – |
| **Poser par** | Quel endroit de l'élément arrive sur le point. | Coin inférieur avant droit | 15 entrées : trois coins et les douze points. Voir plus bas. |
| **Rotation** | Tourne l'élément autour de l'axe vertical (Z), autour de l'endroit choisi sous **Poser par**. | 0 degré | N'importe quel angle. Positif : sens inverse des aiguilles d'une montre, vu d'en haut. |
| **Décalage X** | Déplace l'élément le long de l'axe X de la conception. | 0 mm | N'importe quelle longueur, aussi négative |
| **Décalage Y** | Déplace l'élément le long de l'axe Y de la conception. | 0 mm | N'importe quelle longueur, aussi négative |
| **Décalage Z** | Déplace l'élément le long de l'axe Z de la conception. | 0 mm | N'importe quelle longueur, aussi négative |

Le complément ne fixe aucune limite haute ou basse pour la rotation et les décalages.

### Les entrées sous « Poser par »

Dans cet ordre :

1. Coin inférieur avant droit
2. Coin supérieur avant droit
3. Coin supérieur avant gauche
4. dessous avant
5. dessous milieu
6. dessous arrière
7. dessus avant
8. dessus milieu
9. dessus arrière
10. dessus milieu droite
11. dessus milieu gauche
12. dessous milieu droite
13. dessous milieu gauche
14. milieu droite, 50 mm plus haut
15. milieu gauche, 50 mm plus haut

La signification de chaque entrée est expliquée dans [usage.md](usage.md).

État : **Poser par** et les trois décalages sont testés hors ligne seulement, **pas dans Fusion**.

## Ce qui est mémorisé

Après l'appui sur **OK**, une fois l'élément créé, le complément mémorise ces valeurs pour la fois suivante :

- **Famille**
- **Élément**
- **Poser par**
- **Rotation**
- **Décalage X**, **Décalage Y**, **Décalage Z**

Non mémorisé : le **Point**.

| Question | Réponse |
| --- | --- |
| Pendant combien de temps ? | Jusqu'à la fermeture de Fusion ou l'arrêt du complément. Les valeurs n'existent qu'en mémoire. |
| Sont-elles enregistrées dans un fichier ? | Non. |
| Sont-elles enregistrées dans la conception ? | Non. |
| Et si la boîte de dialogue est annulée ? | Rien n'est mémorisé. Les valeurs du dernier placement réussi restent. |
| Et après un redémarrage ? | Les valeurs par défaut du tableau ci-dessus s'appliquent à nouveau. |

## Langue

Le complément a ses textes en cinq langues : allemand, anglais, espagnol, français et italien.

La langue ne peut pas être choisie dans le complément. Elle est choisie au démarrage du complément :

1. Le complément demande à Fusion la langue réglée dans les préférences de Fusion. Si c'est l'une des cinq, elle
   est utilisée.
2. Sinon, il regarde les réglages de langue du système d'exploitation (les variables d'environnement `LANG`,
   `LANGUAGE`, `LC_ALL`, puis les paramètres régionaux du système).
3. Si rien de tout cela ne donne l'une des cinq langues, l'anglais est utilisé.

Plus de détails :

- Pour changer de langue, changer la langue dans les préférences de Fusion et redémarrer le complément.
- Si un texte manque dans une langue, le texte anglais est affiché à la place.
- Les noms des éléments (`S1 WP`) et des composants (`SYSTEM 3E S1 WP`) ne sont pas traduits.
- Les noms des douze points sont écrits dans la conception quand un élément est placé pour la première fois. Ils
  gardent cette langue, même si le complément fonctionne plus tard dans une autre langue.

## Valeurs fixes qui ne peuvent pas être modifiées dans la boîte de dialogue

| Valeur | Réglage |
| --- | --- |
| Emplacement du bouton | Espace de travail de conception, panneau **Create** des outils de solide |
| Démarrage avec Fusion | Oui (`runOnStartup` dans le fichier manifeste) |
| Points à 50 mm au-dessus de la face inférieure | Fixé à 50 mm |
