# Installation

Retour à la [vue d'ensemble](index.md).

## Prérequis

| Quoi | Détail |
| --- | --- |
| Programme | Autodesk Fusion 360 |
| Système d'exploitation | Windows ou macOS (le complément déclare les deux comme pris en charge) |
| Logiciel supplémentaire | Aucun. Le complément n'utilise que ce que Fusion apporte. |
| Internet | Seulement pour télécharger le fichier ZIP. Le complément lui-même n'ouvre aucune connexion. |

## Installer à partir du ZIP de la version

1. Ouvrir <https://github.com/sorglos-it/fusion360/releases>.
2. Télécharger le fichier `System3E-<version>.zip`, par exemple `System3E-1.2.0.0.zip`.
3. Décompresser le ZIP dans le dossier des compléments de Fusion :

   | Système | Dossier |
   | --- | --- |
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Vérifier le résultat. Le ZIP contient un seul dossier nommé `System3E`. Après la décompression, ce fichier doit
   exister :

   `AddIns/System3E/System3E.py`

   Si l'on voit `AddIns/System3E/System3E/System3E.py`, le dossier est un niveau trop bas. Remonter le dossier
   intérieur d'un niveau.

Astuce pour Windows : saisir `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` dans la barre d'adresse de
l'Explorateur et appuyer sur Entrée.

## Premier démarrage dans Fusion

1. Démarrer Fusion.
2. Ouvrir **Utilities → ADD-INS → Add-Ins**.
3. Sélectionner **System3E** dans la liste.
4. Appuyer sur **Run**.
5. Ouvrir l'onglet **SOLID**. Le bouton **Élément SYSTEM 3E** se trouve dans le panneau **Create**.

Le bouton affiche la version entre parenthèses, par exemple **Élément SYSTEM 3E (1.2.0.0)**.

Le complément est marqué pour démarrer en même temps que Fusion (`runOnStartup` dans son fichier manifeste). Après
le premier démarrage, il n'est normalement plus nécessaire d'appuyer sur **Run**.

Remarque : le chemin de menu de l'étape 2 est repris du README du projet. Il ne peut pas être vérifié dans le code
du complément, et les versions de Fusion peuvent le nommer autrement.

## Mise à jour

1. Dans Fusion, arrêter le complément (**Utilities → ADD-INS → Add-Ins**, sélectionner **System3E**, **Stop**), ou
   fermer Fusion.
2. Supprimer l'ancien dossier `System3E` dans le dossier des compléments.
3. Décompresser le nouveau ZIP dans le dossier des compléments, comme décrit plus haut.
4. Démarrer Fusion, ou appuyer à nouveau sur **Run**.

Ce qu'il advient des conceptions :

- Les éléments déjà placés restent tels quels. Ce sont des composants Fusion normaux.
- Un élément placé avec une version plus ancienne peut avoir moins de douze points. Les points manquants sont
  ajoutés la prochaine fois que le même élément est placé dans cette conception.
- Les valeurs mémorisées de la boîte de dialogue sont perdues. Voir [settings.md](settings.md).

## Suppression

1. Dans Fusion, arrêter le complément, ou fermer Fusion.
2. Supprimer le dossier `System3E` dans le dossier des compléments.

Quand le complément s'arrête, il retire son bouton de la barre d'outils. Il n'enregistre rien en dehors de son
propre dossier. Les éléments restent dans les conceptions ; ils n'ont pas besoin du complément.
