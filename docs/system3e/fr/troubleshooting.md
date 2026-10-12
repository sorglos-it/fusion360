# Dépannage

Retour à la [vue d'ensemble](index.md).

## Messages

Voici tous les messages que le complément peut afficher. Les textes sont cités d'après le fichier de langue
français. Dans les autres langues, le texte est traduit. Les boîtes de message portent le titre
« Élément SYSTEM 3E ».

### « Veuillez choisir un élément. »

| | |
| --- | --- |
| Cause | Aucune entrée n'est sélectionnée sous **Élément**. |
| Ce que l'on voit | Normalement pas le message lui-même : c'est le bouton **OK** qui est grisé. |
| Que faire | Choisir une entrée sous **Élément**. Si la liste est vide, choisir à nouveau la **Famille**. |

### « Veuillez d'abord ouvrir une conception. »

| | |
| --- | --- |
| Cause | Le document actif n'est pas une conception ; il n'y a donc rien où placer l'élément. |
| Que faire | Ouvrir ou créer une conception et passer à l'espace de travail de conception. Puis relancer la commande. |

### « L'élément {0} n'a pas pu être créé : » suivi d'une raison

`{0}` est le nom de l'élément. La deuxième ligne est la raison donnée par Fusion.

| | |
| --- | --- |
| Cause | Fusion a refusé de construire le corps à partir des points et des faces de l'élément. |
| Que faire | 1. Essayer un autre élément pour voir si seul celui-ci est touché. 2. Réinstaller le complément à partir d'un ZIP neuf ; le fichier `blocks/blocks.json` est peut-être endommagé. 3. Si l'échec persiste, signaler le nom de l'élément et la raison indiquée dans le message. |
| Effet | Il ne reste rien. Fusion annule l'étape. |

### « Aucun panneau de barre d'outils approprié n'a été trouvé. »

| | |
| --- | --- |
| Cause | Au démarrage, le complément n'a pas trouvé le panneau **Create** des outils de solide. Aucun bouton n'a été ajouté. |
| Que faire | Mettre Fusion à jour et redémarrer le complément. Si le message reste, signaler la version de Fusion. Le complément ne connaît que ce seul panneau. |

### « Erreur lors de la création de la géométrie : » suivi d'un texte technique

| | |
| --- | --- |
| Cause | Une erreur inattendue après l'appui sur **OK**. Le texte sous la première ligne est un rapport technique (un « traceback ») qui montre où elle s'est produite. |
| Que faire | 1. Réessayer avec un autre point ou un autre élément. 2. Arrêter le complément et le relancer. 3. Si l'erreur reste, copier le texte entier et le signaler. |
| Effet | Fusion annule ce qui avait été construit jusque-là. Aucun composant à moitié fini ne reste. |

### « Erreur lors de la construction de la boîte de dialogue : » suivi d'un texte technique

| | |
| --- | --- |
| Cause | La boîte de dialogue n'a pas pu être construite. Une raison visible dans le code est un fichier `blocks/blocks.json` manquant ou illisible : la boîte de dialogue lit la bibliothèque d'éléments à son ouverture. |
| Que faire | Réinstaller le complément à partir du ZIP, pour que le dossier `blocks` soit complet. Voir [installation.md](installation.md). |

### « Échec du démarrage : » suivi d'un texte technique

| | |
| --- | --- |
| Cause | Une erreur inattendue pendant le démarrage du complément. |
| Que faire | 1. Vérifier que le dossier est correctement décompressé : `AddIns/System3E/System3E.py`. 2. Redémarrer Fusion. 3. Réinstaller le complément. 4. Si l'erreur reste, copier le texte et le signaler. |

### « Échec de l'arrêt : » suivi d'un texte technique

| | |
| --- | --- |
| Cause | Une erreur inattendue pendant que le complément s'arrêtait et retirait son bouton. |
| Que faire | Redémarrer Fusion. Les conceptions ne sont pas touchées. |

## Autres problèmes

| Problème | Cause | Que faire |
| --- | --- | --- |
| **System3E** n'est pas dans la liste des compléments de Fusion. | Le dossier est au mauvais endroit ou un niveau trop bas. | Vérifier que `AddIns/System3E/System3E.py` existe. Voir [installation.md](installation.md). |
| Le bouton manque. | Le complément ne tourne pas. | Ouvrir la boîte de dialogue des compléments, sélectionner **System3E**, appuyer sur **Run**. |
| La boîte de dialogue est en anglais alors que Fusion utilise une autre langue. | Seuls l'allemand, l'anglais, l'espagnol, le français et l'italien existent. Les autres langues se rabattent sur l'anglais. | – |
| La boîte de dialogue est dans la mauvaise langue après un changement de langue de Fusion. | La langue est choisie au démarrage du complément. | Arrêter le complément et le relancer, ou redémarrer Fusion. |
| L'image ne change pas quand on choisit un autre élément. | Le fichier image `blocks/<id>.png` de cet élément manque. L'ancienne image reste. | Réinstaller le complément. |
| Aucun aperçu de l'élément n'apparaît tant que la boîte de dialogue est ouverte. | Une erreur s'est produite pendant l'aperçu. Les erreurs d'aperçu ne sont pas affichées. | Appuyer sur **OK**. Une vraie erreur est alors affichée sous forme de message. |
| Impossible de cliquer sur un certain endroit. | Seuls les points d'esquisse, les coins de corps et les points de construction peuvent être choisis. Les faces, les arêtes et les milieux d'arêtes ne le peuvent pas. | Créer à cet endroit un point d'esquisse ou un point de construction, ou utiliser les décalages. |
| L'élément se trouve à l'origine. | Aucun point n'a été sélectionné. | Cliquer sur un point pour **Point**. |
| L'élément est tourné dans le mauvais sens. | Une **Rotation** positive tourne dans le sens inverse des aiguilles d'une montre, vu d'en haut. | Saisir l'angle avec le signe opposé. |
| Les décalages déplacent l'élément dans une direction inattendue. | Les décalages suivent les axes de la conception, pas ceux de l'élément tourné. | Utiliser l'axe qui correspond à la direction dans la conception. |
| Les noms des points sont dans une autre langue que la boîte de dialogue. | Les noms des points sont écrits quand un élément est placé pour la première fois dans une conception, et ils sont conservés. | Renommer les points à la main si nécessaire. |
| Un élément plus ancien a moins de douze points. | Il a été placé avec une version plus ancienne. | Placer une fois de plus un élément quelconque dans cette conception. Chaque élément reçoit ses points manquants. |
| Les points se trouvent à côté de l'élément, pas dessus. | L'élément a été placé loin de l'origine avec une version antérieure à la 1.1.0.1. | Placer une fois de plus un élément quelconque dans cette conception. Les points sont créés à nouveau au bon endroit. |
| Un point n'est pas exactement à la moitié de la largeur ou sur la face inférieure. | L'endroit exact est dans la matière ou dans le vide ; le point est donc montré sur la surface voisine. | Rien. Au clic, c'est toujours l'endroit exact qui compte. Voir [usage.md](usage.md). |
| Après une mise à jour, Fusion affiche encore l'ancienne version sur le bouton. | Fusion exécute la copie qui se trouve dans son dossier des compléments, pas celle qui a été téléchargée. | Décompresser le nouveau ZIP par-dessus l'ancien dossier, puis arrêter le complément et le relancer. Voir [installation.md](installation.md). |
| La boîte de dialogue démarre à nouveau avec les valeurs par défaut. | Les valeurs mémorisées ne durent que jusqu'à la fermeture de Fusion ou l'arrêt du complément. | – |
| Une liste de pièces montre le même élément sur plusieurs lignes. | Les éléments ont été placés avec la version 0.2.0, qui créait un nouveau composant à chaque fois. Seul le premier d'entre eux est réutilisé désormais. | Remplacer les anciens par des éléments nouvellement placés. |

## Limites connues

- **Non testé dans Fusion :** les corrections de la version 1.0.0.1 (voir le [journal des modifications](../CHANGELOG.md)).
- **Un point dans le vide :** sur les demi-éléments d'angle `SNL/2` et `SNP/2`, le point « dessous milieu gauche »
  n'a aucun endroit libre sur la surface et reste dans le vide.
- **Gauche et droite :** les noms gauche/droite des éléments d'angle et de fenêtre ont été comparés à l'œil avec
  les fiches du catalogue du fabricant. Ils ne sont pas confirmés.
- **`S0/2 200 P` :** cet élément est endommagé dans le fichier 3D du fabricant. Il est reconstruit à partir de
  `S0/2 250 P`.
- **Axe vertical :** le complément considère toujours l'axe Z de la conception comme le « haut ». Il ne tient pas
  compte d'un réglage d'orientation différent dans Fusion.
- **Niveau supérieur seulement :** les éléments sont toujours créés au niveau supérieur de la conception (le
  composant racine), pas dans le composant actif à ce moment-là.
- **Conceptions liées :** un élément situé dans une conception liée n'est pas réutilisé. Le complément crée son
  propre composant.
- **Pas de contrôle d'ajustement :** le complément ne vérifie pas si des éléments se chevauchent, si un joint
  convient ni si un mur est constructible.
- **Un élément par exécution :** il n'y a pas de fonction pour des rangs ou des murs entiers.
- **Rotation :** seulement autour de l'axe vertical. Les éléments ne peuvent pas être inclinés dans la boîte de
  dialogue.
- **Corps partagé :** toutes les copies d'un élément partagent un seul corps. En modifier une les modifie toutes.
- **Tailles :** les formes viennent du fichier 3D du fabricant et sont arrondies à 0,1 mm. Les quatre éléments de
  cloison sont de simples blocs sans profil.
- **Aucune affiliation :** le complément n'est pas affilié à SYSTEM 3E. Il ne remplace pas les documents de
  planification du fabricant.
