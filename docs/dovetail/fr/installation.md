# Installation

## Prérequis

- Autodesk Fusion 360 sous Windows ou macOS. L'add-in déclare exactement ces deux systèmes.
- Rien d'autre. L'add-in fonctionne avec le Python fourni par Fusion et n'utilise aucun paquet supplémentaire.

Le code n'indique aucune version minimale de Fusion. L'add-in n'a pas été testé avec une liste de versions de Fusion.

## Installer à partir du ZIP de la version

1. Ouvrir <https://github.com/sorglos-it/fusion360/releases>.
2. Télécharger le fichier `Dovetail-<version>.zip`, par exemple `Dovetail-1.1.0.0.zip`.
3. Décompresser le ZIP dans le dossier des add-ins de Fusion :

   | Système | Dossier |
   |---|---|
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Vérifier le résultat. Le ZIP contient un dossier nommé `Dovetail`. Après la décompression, ceci doit exister :

   ```
   AddIns/Dovetail/Dovetail.py
   AddIns/Dovetail/Dovetail.manifest
   AddIns/Dovetail/lang/
   AddIns/Dovetail/resources/
   ```

   Si le programme de décompression a créé un dossier supplémentaire autour (par exemple `AddIns/Dovetail-1.1.0.0/Dovetail/`), remonter le
   dossier intérieur `Dovetail` d'un niveau.

Ne pas renommer le dossier ni les fichiers. Le dossier, le fichier `.py` et le fichier `.manifest` doivent tous porter le même nom.

## Premier démarrage dans Fusion

1. Démarrer Fusion.
2. Ouvrir la liste des add-ins : **Utilities → ADD-INS → Add-Ins**.
   (Le libellé de ce menu vient de Fusion et peut varier selon la version de Fusion.)
3. Sélectionner l'entrée **Dovetail**.
4. Cocher **Run on Startup** si ce n'est pas déjà coché. L'add-in le demande lui-même dans son manifeste.
5. Appuyer sur **Run**.

L'add-in ajoute alors un bouton à la barre d'outils. Son nom est **Queue d'aronde**, suivi de la version entre parenthèses,
par exemple *Queue d'aronde (1.1.0.0)*.

Où le bouton apparaît :

| Ordre | Emplacement |
|---|---|
| 1 | le panneau **Create** de la barre d'outils d'esquisse |
| 2 | s'il manque : le panneau **Modify** de la barre d'outils d'esquisse |
| 3 | s'il manque aussi : le panneau **Create** de l'onglet Solid |

L'add-in prend le premier de ces emplacements qui existe. Le bouton est placé directement sur la barre d'outils, pas seulement dans le
menu déroulant du panneau.

Si aucun des trois n'existe, le message « Aucun panneau de barre d'outils approprié n'a été trouvé. » s'affiche. Voir
[troubleshooting.md](troubleshooting.md).

## Mise à jour

1. Dans Fusion, ouvrir la liste des add-ins et **arrêter** Dovetail. Sinon, l'ancienne version reste en mémoire.
2. Supprimer l'ancien dossier `Dovetail` du dossier des add-ins.
3. Décompresser le nouveau ZIP dans le dossier des add-ins, comme décrit plus haut.
4. Appuyer de nouveau sur **Run**, ou redémarrer Fusion.
5. Vérifier la version dans le nom du bouton ou dans le titre de la boîte de dialogue.

L'add-in n'enregistre aucun réglage sur le disque. Supprimer l'ancien dossier ne fait rien perdre.

Remarque tirée de l'ancien README, non vérifiable dans le code actuel : de très anciennes versions s'appelaient `Schwalbenschwanz`.
Si un tel dossier se trouve encore dans le dossier des add-ins, arrêter cet add-in et supprimer le dossier. Sinon, deux boutons apparaissent.

## Suppression

1. Dans Fusion, ouvrir la liste des add-ins et **arrêter** Dovetail. Cela retire le bouton et la commande.
2. Fermer Fusion.
3. Supprimer le dossier `Dovetail` du dossier des add-ins.

L'add-in n'écrit aucun autre fichier ni aucun réglage. Les assemblages déjà dessinés restent dans les esquisses ; ce sont des
lignes d'esquisse ordinaires.
