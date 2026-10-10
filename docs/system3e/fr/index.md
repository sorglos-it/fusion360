# System3E – documentation

System3E est un complément pour Autodesk Fusion 360. Il place dans une conception des éléments de mur du système
de construction à sec SYSTEM 3E. On clique sur un point, on choisit l'un des 74 éléments dans une liste, et
l'élément est créé à cet endroit sous forme de corps solide.

Cette documentation décrit la version 1.1.0.0.

## Sommaire

| Fichier | Ce qu'on y trouve |
| --- | --- |
| [installation.md](installation.md) | Prérequis, installation, premier démarrage, mise à jour, suppression |
| [usage.md](usage.md) | Placer des éléments pas à pas, monter un mur à joints décalés, liste de pièces |
| [settings.md](settings.md) | Chaque champ de la boîte de dialogue, valeurs par défaut, ce qui est mémorisé, langue |
| [how-it-works.md](how-it-works.md) | Fichiers, bibliothèque d'éléments, construction d'un corps, points, unités |
| [troubleshooting.md](troubleshooting.md) | Chaque message, sa cause et ce qu'il faut faire ; limites connues |
| [development.md](development.md) | Dossiers, tests, reconstruction de la bibliothèque, versions, publication |

Autres fichiers : [journal des modifications](../CHANGELOG.md), [licence](../LICENSE), [dessin des points](../s1-wp-punkte.svg).

## Ce que fait le complément

- Il ajoute un seul bouton, **Élément SYSTEM 3E**, à Fusion.
- Le bouton ouvre une boîte de dialogue avec huit champs et une image d'aperçu.
- L'élément est créé sous forme de composant avec un seul corps solide.
- Chaque élément porte douze points qui lui sont propres. On peut cliquer dessus pour placer l'élément suivant.
- Le même élément placé à nouveau est une autre copie du même composant. Une liste de pièces compte ensemble les éléments identiques.

## Ce qui est testé et ce qui ne l'est pas

| Partie | État |
| --- | --- |
| Placement des éléments | Utilisé dans Fusion par l'auteur |
| Les douze points à cliquer | Testé hors ligne seulement, **pas dans Fusion** |
| Les choix sous **Poser par** | Testé hors ligne seulement, **pas dans Fusion** |
| **Décalage X**, **Décalage Y**, **Décalage Z** | Testé hors ligne seulement, **pas dans Fusion** |
| Corrections de la version 1.0.0.1 (voir le [journal des modifications](../CHANGELOG.md)) | Pas encore confirmé dans Fusion |
| Noms gauche/droite des éléments d'angle et de fenêtre | Comparés à l'œil avec les fiches du catalogue du fabricant, **non confirmés** |
| Élément `S0/2 200 P` | Endommagé dans le fichier 3D du fabricant, reconstruit à partir de `S0/2 250 P` |

« Hors ligne » signifie : vérifié par un programme de test sans Fusion. Voir [development.md](development.md).

## Mentions légales

- Le complément **n'est pas affilié à SYSTEM 3E**.
- Licence : MIT. Voir [LICENSE](../LICENSE).
- Auteur : Sorglos Thomas Weirich.
