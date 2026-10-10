# Ajustes

El complemento no tiene cuadro de diálogo de ajustes ni archivo de ajustes. Todo se ajusta en tres lugares:

1. el archivo de entrada `<name>.py`, bloque `CONFIGURE`
2. el manifiesto `<name>.manifest`
3. los archivos de idioma de `lang/`

## Archivo de entrada

| Nombre | Valor en la plantilla | Significado | Valores permitidos |
| --- | --- | --- | --- |
| `CMD_ID` | `thwAddInTemplateCmd` | Id del comando | Cualquier texto. Debe ser único entre **todos** los complementos instalados en Fusion. Una coincidencia se apodera en silencio del botón del otro complemento. El script lo pone en `<prefix><name>Cmd` |
| `WORKSPACE_ID` | `FusionSolidEnvironment` | Espacio de trabajo que recibe el botón. Este es el espacio de trabajo de diseño | Un id de un espacio de trabajo de Fusion |
| `PANEL_IDS` | `('SketchCreatePanel', 'SolidCreatePanel')` | Paneles de la barra de herramientas, probados en este orden. El primero que existe recibe el botón | Una lista de ids de paneles, el más deseado primero |
| `IN_LINE` | `tplLine` | Id del campo de selección | Cualquier texto, único dentro de este comando |
| `IN_LENGTH` | `tplLength` | Id del campo de longitud | como arriba |
| `IN_FLIP` | `tplFlip` | Id de la casilla de verificación | como arriba |
| `RESOURCE_FOLDER` | `resources/<name>` en la carpeta del complemento | Carpeta con los iconos. Si no existe, el botón no recibe icono | Una carpeta con `16x16.png`, `32x32.png`, `64x64.png` |
| `LANG_DIR` | `lang` en la carpeta del complemento | Carpeta con los archivos de idioma | Una carpeta con archivos `<code>.xml` |
| `_last` | `{IN_LENGTH: 1.0, IN_FLIP: False}` | Valores iniciales y valores recordados de la última llamada | Una entrada por cada campo que se recuerda |
| `_CORE_MODULE` | `addin_core` | Nombre del módulo central. Está encima de `CONFIGURE` | El script lo pone en `<name en minúsculas>_core`. Hay que conservarlo |

### Ids de paneles nombrados en el código

| Id | Pestaña |
| --- | --- |
| `SketchCreatePanel`, `SketchModifyPanel` | SKETCH |
| `SolidCreatePanel`, `SolidModifyPanel` | SOLID |
| `InspectPanel`, `ToolsPanel` | UTILITIES |

Cada panel se busca primero en el espacio de trabajo y después entre todos los paneles de Fusion.
El botón se añade como "promoted", lo que significa que se muestra directamente en el panel.

### Valores recordados

- `_last` guarda los valores para la próxima llamada del comando.
- Viven solo en la memoria. Desaparecen cuando Fusion se cierra o el complemento se reinicia.
- Las longitudes están en **cm**, la unidad interna de Fusion, muestre lo que muestre el campo. `1.0` en un campo que se muestra en `mm` se lee como 10 mm.
- Un valor solo se recuerda si `remember()` lo copia y `build_inputs()` lo usa como valor inicial.

## Manifiesto

El manifiesto es un archivo JSON. Fusion lo lee.

| Campo | Valor en la plantilla | Significado | ¿Lo ajusta el script? |
| --- | --- | --- | --- |
| `autodeskProduct` | `Fusion360` | El producto. La comprobación sin conexión exige este valor | no |
| `type` | `addin` | El tipo de extensión. La comprobación sin conexión exige este valor | no |
| `id` | `00000000-0000-0000-0000-000000000000` | GUID del complemento. Los ceros son un marcador de posición | sí, un GUID nuevo aleatorio |
| `author` | `Your Name` | Autor | sí, a partir de `--author` |
| `description` | un texto para cada uno de `""` (por defecto), `de-DE`, `es-ES`, `fr-FR`, `it-IT` | Descripción del complemento | **no – sigue describiendo la plantilla. Hay que editarla** |
| `version` | `1.0.0.0` | Versión. El complemento la lee y la muestra entre paréntesis después del nombre del comando | **no – conserva el número de la plantilla. Hay que poner el propio** |
| `runOnStartup` | `true` | Iniciar el complemento junto con Fusion | no |
| `supportedOS` | `windows\|mac` | Sistemas para los que está hecho el complemento | no |
| `editEnabled` | `true` | Un campo de Fusion. El código de la plantilla no lo usa | no |

La versión está escrita en un solo lugar, el manifiesto. El código la lee de allí, así que el título del cuadro de diálogo no puede diferir del manifiesto.
Si el manifiesto no se puede leer o no tiene versión, el nombre se muestra sin paréntesis.

## Archivos de idioma

### Formato

Un archivo por idioma: `lang/<code>.xml`.

```xml
<strings language="en">
  <string key="in.length">Length</string>
</strings>
```

- `en.xml` es la referencia. Todas las claves existen allí.
- El atributo `language` debe ser igual al código del nombre del archivo.
- Los marcadores de posición `{0}`, `{1}`, … los rellena el complemento. Deben conservarse en todas las traducciones.
- Los demás archivos pueden omitir claves. Las claves que faltan se muestran en inglés.

### Claves de la plantilla

| Clave | Texto en español |
| --- | --- |
| `cmd.name` | Plantilla de complemento |
| `cmd.tooltip` | Punto de partida para un complemento de Fusion 360. / Dibuja una marca en el punto medio de la línea seleccionada. (dos líneas) |
| `in.line` | Línea |
| `in.line.prompt` | Selecciona una línea de boceto |
| `in.length` | Longitud |
| `in.flip` | Invertir la dirección |
| `err.no_selection` | Selecciona exactamente una línea de boceto. |
| `err.length_positive` | La longitud debe ser mayor que 0. |
| `err.zero_length` | La línea seleccionada no tiene longitud. |
| `err.too_long` | La longitud supera la línea seleccionada ({0} mm). |
| `msg.panel_missing` | No se encontró ningún panel de barra de herramientas adecuado. |
| `msg.exec_failed` | Error al crear la geometría: {0} |
| `msg.dialog_failed` | Error al construir el cuadro de diálogo: {0} |
| `msg.run_failed` | Error al iniciar: {0} |
| `msg.stop_failed` | Error al detener: {0} |

`cmd.name` es también el título de todos los cuadros de mensaje.

### Cómo se elige el idioma

El idioma se elige una sola vez, cuando el complemento se inicia. No hay ningún selector en el complemento.

1. El idioma ajustado en las preferencias de Fusion (el idioma del usuario).
2. Si eso no da un idioma admitido: las variables de entorno `LANG`, `LANGUAGE`, `LC_ALL`, en este orden.
3. Si eso no da nada: el idioma del sistema operativo.
4. Si no, el inglés.

Códigos admitidos: `de`, `en`, `es`, `fr`, `it`.

Después de cambiar el idioma en Fusion, hay que detener el complemento y ejecutarlo otra vez.

### Añadir un idioma

1. Copiar `lang/en.xml` y dar a la copia el nombre del código de dos letras, por ejemplo `ja.xml`.
2. Poner `language="ja"` en la primera etiqueta.
3. Traducir los valores. Conservar las claves y los marcadores de posición.
4. En el módulo central (`<name>_core.py`), añadir el código a `SUPPORTED_LANGUAGES`.
5. En el módulo central, añadir el idioma de Fusion a `FUSION_LANGUAGE_MAP`, por ejemplo `'JapaneseLanguage': 'ja'`.
6. Ejecutar la comprobación sin conexión, véase [development.md](development.md).
