# Dovetail – documentation

Dovetail est un add-in pour Autodesk Fusion 360. Il transforme des lignes d'esquisse en assemblages : queue d'aronde, triangle ou assemblage à peigne.
Pour chaque ligne sélectionnée, il dessine une bande fermée. La bande est exactement aussi large que l'espace voulu entre les deux
pièces. Découper la bande dans un solide laisse deux pièces qui s'emboîtent.

Cette documentation décrit la version **1.1.0.0**.

## Sommaire

| Fichier | Ce qu'il contient |
|---|---|
| [installation.md](installation.md) | Prérequis, installation, premier démarrage, mise à jour, suppression |
| [usage.md](usage.md) | Chaque fonction, pas à pas |
| [settings.md](settings.md) | Chaque champ de la boîte de dialogue : signification, valeur par défaut, limites ; ce qui est mémorisé ; langue |
| [how-it-works.md](how-it-works.md) | Comment la bande est construite en interne, les contrôles, les unités |
| [troubleshooting.md](troubleshooting.md) | Chaque message, sa cause et ce qu'il faut faire ; limites connues |
| [development.md](development.md) | Dossiers, tests, numéros de version, création d'une version, décisions |

## En un coup d'œil

| | |
|---|---|
| Fonctionne dans | Autodesk Fusion 360 sous Windows et macOS |
| Formes | Trapèze (queue d'aronde), Triangle, Rectangle (assemblage à peigne) |
| Lignes par exécution | 1 à 100 |
| Dents par ligne | 1 à 500 |
| Langues de l'interface | allemand, anglais, espagnol, français, italien |
| Licence | MIT, voir [LICENSE](../LICENSE) |
| Auteur | Sorglos Thomas Weirich |

## État des tests

- Les calculs de géométrie et les fichiers de langue sont testés hors de Fusion avec un script de test hors ligne.
- La version 1.1.0.0 a modifié la géométrie (voir [how-it-works.md](how-it-works.md#ce-qui-a-changé-dans-la-1100)).
  Ces modifications ont été testées **hors ligne uniquement**, y compris sur 34 317 contours aléatoires. Elles ne sont **pas encore confirmées
  dans Fusion**.

## Voir aussi

- [README](../README.md) – courte page d'entrée
- [CHANGELOG](../CHANGELOG.md) – ce qui a changé dans quelle version
