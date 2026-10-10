# AddInTemplate

AddInTemplate est le point de départ pour écrire son propre complément Autodesk Fusion 360.
Il a deux parties :

- un **complément de démonstration** (`apps/desktop-template/AddInTemplate`) avec une commande, une boîte de dialogue traduite, un aperçu en direct et des contrôles de saisie
- un **script de génération** (`tools/template/new_addin.py`) qui copie le complément de démonstration et renomme tout ce qui doit être unique

| Fait | Valeur |
| --- | --- |
| Version | 1.0.0.0 |
| ZIP de version | aucun pour cette version – elle s'utilise depuis le dépôt |
| Fonctionne sur | Windows et macOS (manifeste : `windows\|mac`) |
| Langues de l'interface | allemand, anglais, espagnol, français, italien |
| Dépendances | aucune – bibliothèque standard de Python seulement |
| Licence | MIT |
| Auteur | Sorglos Thomas Weirich |
| Dépôt | <https://github.com/sorglos-it/fusion360> |

## Sommaire

| Fichier | Ce qu'on y trouve |
| --- | --- |
| [installation.md](installation.md) | Prérequis, obtenir le dépôt, créer un nouveau complément, dossier des compléments de Fusion, premier démarrage, suppression |
| [usage.md](usage.md) | Ce que fait la commande de démonstration, et comment faire de la copie son propre complément |
| [settings.md](settings.md) | Tout ce qui se règle dans le fichier d'entrée, dans le manifeste et dans les fichiers de langue |
| [how-it-works.md](how-it-works.md) | Fichier d'entrée, module central, registre des gestionnaires, déroulement des événements, catalogue de textes |
| [troubleshooting.md](troubleshooting.md) | Chaque message, sa cause et ce qu'il faut faire ; pièges connus |
| [development.md](development.md) | Dossiers, contrôle hors ligne, outil d'icône, numéros de version, empaquetage, décisions |

## Bon à savoir avant de commencer

- Chaque complément créé à partir du modèle reçoit sa **propre copie** du module central. Une correction faite plus tard dans le modèle n'atteint **pas** les compléments créés auparavant.
- Le contrôle hors ligne a été lancé pour cette documentation et a réussi. Le comportement dans Fusion 360 est décrit d'après le code ; il n'a **pas été testé dans Fusion** pour cette documentation.

Autres langues : [liste des langues](../index.md)
