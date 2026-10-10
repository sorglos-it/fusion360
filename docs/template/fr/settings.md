# Réglages

Le complément n'a ni boîte de dialogue de réglages ni fichier de réglages. Tout se règle à trois endroits :

1. le fichier d'entrée `<name>.py`, bloc `CONFIGURE`
2. le manifeste `<name>.manifest`
3. les fichiers de langue dans `lang/`

## Fichier d'entrée

| Nom | Valeur du modèle | Signification | Valeurs autorisées |
| --- | --- | --- | --- |
| `CMD_ID` | `thwAddInTemplateCmd` | Id de la commande | N'importe quel texte. Il doit être unique parmi **tous** les compléments installés dans Fusion. Une collision prend sans bruit le bouton de l'autre complément. Le script le règle sur `<prefix><name>Cmd` |
| `WORKSPACE_ID` | `FusionSolidEnvironment` | Espace de travail qui reçoit le bouton. Celui-ci est l'espace de travail de conception | Un id d'espace de travail de Fusion |
| `PANEL_IDS` | `('SketchCreatePanel', 'SolidCreatePanel')` | Panneaux de barre d'outils, essayés dans cet ordre. Le premier qui existe reçoit le bouton | Une liste d'ids de panneaux, le préféré en premier |
| `IN_LINE` | `tplLine` | Id du champ de sélection | N'importe quel texte, unique dans cette commande |
| `IN_LENGTH` | `tplLength` | Id du champ de longueur | comme ci-dessus |
| `IN_FLIP` | `tplFlip` | Id de la case à cocher | comme ci-dessus |
| `RESOURCE_FOLDER` | `resources/<name>` dans le dossier du complément | Dossier des icônes. S'il n'existe pas, le bouton n'a pas d'icône | Un dossier contenant `16x16.png`, `32x32.png`, `64x64.png` |
| `LANG_DIR` | `lang` dans le dossier du complément | Dossier des fichiers de langue | Un dossier contenant des fichiers `<code>.xml` |
| `_last` | `{IN_LENGTH: 1.0, IN_FLIP: False}` | Valeurs de départ, et valeurs mémorisées du dernier appel | Une entrée par champ mémorisé |
| `_CORE_MODULE` | `addin_core` | Nom du module central. Il se trouve au-dessus de `CONFIGURE` | Réglé par le script sur `<name in lower case>_core`. Le garder |

### Ids de panneaux nommés dans le code

| Id | Onglet |
| --- | --- |
| `SketchCreatePanel`, `SketchModifyPanel` | SKETCH |
| `SolidCreatePanel`, `SolidModifyPanel` | SOLID |
| `InspectPanel`, `ToolsPanel` | UTILITIES |

Chaque panneau est cherché d'abord dans l'espace de travail, puis parmi tous les panneaux de Fusion.
Le bouton est ajouté comme « promoted », ce qui signifie qu'il est affiché directement sur le panneau.

### Valeurs mémorisées

- `_last` contient les valeurs pour l'appel suivant de la commande.
- Elles n'existent qu'en mémoire. Elles disparaissent quand Fusion se ferme ou que le complément est redémarré.
- Les longueurs sont en **cm**, l'unité interne de Fusion, quoi que le champ affiche. `1.0` dans un champ affiché en `mm` donne 10 mm.
- Une valeur n'est mémorisée que si `remember()` la copie et que `build_inputs()` l'utilise comme valeur de départ.

## Manifeste

Le manifeste est un fichier JSON. Fusion le lit.

| Champ | Valeur du modèle | Signification | Réglé par le script ? |
| --- | --- | --- | --- |
| `autodeskProduct` | `Fusion360` | Le produit. Le contrôle hors ligne exige cette valeur | non |
| `type` | `addin` | Le genre d'extension. Le contrôle hors ligne exige cette valeur | non |
| `id` | `00000000-0000-0000-0000-000000000000` | GUID du complément. Les zéros sont une valeur provisoire | oui, un nouveau GUID aléatoire |
| `author` | `Your Name` | Auteur | oui, à partir de `--author` |
| `description` | un texte chacun pour `""` (par défaut), `de-DE`, `es-ES`, `fr-FR`, `it-IT` | Description du complément | **non – elle décrit encore le modèle. La modifier** |
| `version` | `1.0.0.0` | Version. Le complément la lit et l'affiche entre parenthèses après le nom de la commande | **non – elle garde le numéro du modèle. Mettre le sien** |
| `runOnStartup` | `true` | Démarrer le complément en même temps que Fusion | non |
| `supportedOS` | `windows\|mac` | Systèmes auxquels le complément est destiné | non |
| `editEnabled` | `true` | Un champ de Fusion. Le code du modèle ne l'utilise pas | non |

La version est écrite à un seul endroit, le manifeste. Le code la lit à cet endroit ; le titre de la boîte de dialogue ne peut donc pas différer du manifeste.
Si le manifeste ne peut pas être lu ou n'a pas de version, le nom est affiché sans parenthèses.

## Fichiers de langue

### Format

Un fichier par langue : `lang/<code>.xml`.

```xml
<strings language="en">
  <string key="in.length">Length</string>
</strings>
```

- `en.xml` est la référence. Chaque clé y existe.
- L'attribut `language` doit être identique au code du nom de fichier.
- Les espaces réservés `{0}`, `{1}`, … sont remplis par le complément. Ils doivent rester dans chaque traduction.
- Les autres fichiers peuvent omettre des clés. Les clés manquantes sont affichées en anglais.

### Clés du modèle

| Clé | Texte français |
| --- | --- |
| `cmd.name` | Modèle de complément |
| `cmd.tooltip` | Point de départ pour un complément Fusion 360. / Trace un trait au milieu de la ligne sélectionnée. (deux lignes) |
| `in.line` | Ligne |
| `in.line.prompt` | Sélectionner une ligne d'esquisse |
| `in.length` | Longueur |
| `in.flip` | Inverser la direction |
| `err.no_selection` | Sélectionnez exactement une ligne d'esquisse. |
| `err.length_positive` | La longueur doit être supérieure à 0. |
| `err.zero_length` | La ligne sélectionnée n'a aucune longueur. |
| `err.too_long` | La longueur dépasse la ligne sélectionnée ({0} mm). |
| `msg.panel_missing` | Aucun panneau de barre d'outils approprié n'a été trouvé. |
| `msg.exec_failed` | Erreur lors de la création de la géométrie : {0} |
| `msg.dialog_failed` | Erreur lors de la construction de la boîte de dialogue : {0} |
| `msg.run_failed` | Échec du démarrage : {0} |
| `msg.stop_failed` | Échec de l'arrêt : {0} |

`cmd.name` est aussi le titre de chaque boîte de message.

### Comment la langue est choisie

La langue est choisie une seule fois, au démarrage du complément. Il n'y a pas de sélecteur dans le complément.

1. La langue réglée dans les préférences de Fusion (la langue de l'utilisateur).
2. Si cela ne donne aucune langue prise en charge : les variables d'environnement `LANG`, `LANGUAGE`, `LC_ALL`, dans cet ordre.
3. Si cela ne donne rien : la langue du système d'exploitation.
4. Sinon l'anglais.

Codes pris en charge : `de`, `en`, `es`, `fr`, `it`.

Après un changement de langue dans Fusion, arrêter le complément et le relancer.

### Ajouter une langue

1. Copier `lang/en.xml` et nommer la copie d'après le code à deux lettres, par exemple `ja.xml`.
2. Mettre `language="ja"` dans la première balise.
3. Traduire les valeurs. Garder les clés et les espaces réservés.
4. Dans le module central (`<name>_core.py`), ajouter le code à `SUPPORTED_LANGUAGES`.
5. Dans le module central, ajouter la langue de Fusion à `FUSION_LANGUAGE_MAP`, par exemple `'JapaneseLanguage': 'ja'`.
6. Lancer le contrôle hors ligne, voir [development.md](development.md).
