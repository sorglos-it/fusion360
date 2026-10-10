# SketchGrid

SketchGrid est un add-in pour Autodesk Fusion 360. Un clic sur un point d'une esquisse donne une grille de formes identiques autour de ce point : rectangles, cercles ou ellipses, trous oblongs ou polygones.

Cette documentation décrit la version 1.1.0.0.

## Sommaire

| Fichier | Ce qu'il contient |
| --- | --- |
| [installation.md](installation.md) | Prérequis, installation, premier démarrage, mise à jour, suppression |
| [usage.md](usage.md) | Chaque fonction, pas à pas |
| [settings.md](settings.md) | Chaque champ de la boîte de dialogue avec valeur par défaut et limites, ce qui est mémorisé, langue |
| [how-it-works.md](how-it-works.md) | Fichiers, comment la grille est calculée, comment les formes sont dessinées |
| [troubleshooting.md](troubleshooting.md) | Chaque message, sa cause et ce qu'il faut faire ; limites connues |
| [development.md](development.md) | Dossiers, tests, numéros de version, création d'une version |

## Ce qu'il fait, en bref

- Deux façons de fixer le nombre de formes : **Colonnes et lignes**, ou **Remplissage d'une zone** (autant qu'il en tient entièrement).
- Quatre formes : **Rectangle** (coins vifs, arrondis ou chanfreinés), **Cercle / ellipse**, **Trou oblong**, **Polygone** (3 à 24 côtés).
- Neuf positions pour le point dans la grille, plus un décalage en X et en Y.
- Un écart séparé pour X et pour Y.
- Une ligne **Résultat** qui affiche le nombre de formes et la taille totale pendant la saisie.
- Au plus 2000 formes par grille.

## État des tests

- Le calcul de la grille, les contours des coins, les messages et les cinq fichiers de langue sont contrôlés par un test automatique qui fonctionne sans Fusion.
- La modification de la version 1.1.0.0 (la boîte de dialogue continue de fonctionner quand le point sélectionné au préalable ne peut pas être repris) a été testée hors ligne uniquement, **pas dans Fusion**.
- Deux limites connues viennent d'une relecture du code et ne sont **pas confirmées dans Fusion**. Voir [troubleshooting.md](troubleshooting.md#limites-connues).

## Licence et auteur

Licence MIT, voir [LICENSE](../LICENSE). Auteur : Sorglos Thomas Weirich.

Historique des modifications : [CHANGELOG.md](../CHANGELOG.md).
