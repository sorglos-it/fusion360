# Installation

## Prérequis

- Autodesk Fusion 360 sous Windows ou macOS. L'add-in déclare ces deux systèmes et aucun autre.
- Rien d'autre. L'add-in n'utilise que le Python intégré à Fusion.

Le code n'indique aucune version minimale de Fusion.

## Installer à partir du ZIP de la version

1. Ouvrir <https://github.com/sorglos-it/fusion360/releases>.
2. Télécharger le fichier `SketchGrid-<version>.zip`, par exemple `SketchGrid-1.1.0.0.zip`.
3. Le décompresser dans le dossier des add-ins de Fusion :

   | Système | Dossier |
   | --- | --- |
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Vérifier le résultat. Le dossier des add-ins doit maintenant contenir un dossier `SketchGrid`, et directement dedans les fichiers `SketchGrid.py` et `SketchGrid.manifest`.

Ne pas renommer le dossier. Fusion attend que le dossier, le fichier `.py` et le fichier `.manifest` portent le même nom.

## Premier démarrage dans Fusion

1. Démarrer Fusion.
2. Ouvrir **Utilities → ADD-INS → Add-Ins**.
3. Sélectionner **SketchGrid** dans la liste.
4. Appuyer sur **Run**.

L'add-in est marqué dans son manifeste pour s'exécuter au démarrage (`runOnStartup` est défini). S'il ne démarre pas tout seul la fois suivante, cocher **Run on Startup** dans la même liste.

Après le démarrage, un bouton nommé **Grille d'esquisse (1.1.0.0)** apparaît. Le numéro entre parenthèses est la version installée. L'add-in cherche d'abord le panneau **CREATE** de la barre d'outils d'esquisse et, s'il n'existe pas, le panneau **CREATE** de l'onglet **SOLID**.

## Mise à jour

1. Dans Fusion, ouvrir **Utilities → ADD-INS → Add-Ins**, sélectionner **SketchGrid** et appuyer sur **Stop**. Sinon, l'ancienne version reste en mémoire.
2. Supprimer le dossier `SketchGrid` dans le dossier des add-ins.
3. Décompresser le nouveau ZIP dans le dossier des add-ins, comme ci-dessus.
4. Appuyer de nouveau sur **Run**.
5. Vérifier la version entre parenthèses sur le bouton.

L'add-in n'enregistre aucun réglage sur le disque. Supprimer le dossier ne fait rien perdre.

## Suppression

1. Dans Fusion, arrêter l'add-in (**Utilities → ADD-INS → Add-Ins**, sélectionner **SketchGrid**, **Stop**). Cela retire le bouton.
2. Supprimer le dossier `SketchGrid` dans le dossier des add-ins.

L'add-in ne laisse aucun autre fichier. Les grilles déjà dessinées restent dans les esquisses ; ce sont des géométries d'esquisse normales.
