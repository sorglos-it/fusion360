# Solución de problemas

Los textos de abajo son los españoles de `lang/es.xml`. En otro idioma, el complemento muestra la traducción.
Todos los cuadros de mensaje tienen como título el nombre del comando.

## Mensajes del comando de demostración

Estos cuatro salen de `validate()`. Mientras se da uno de ellos, **OK** aparece atenuado en gris y no se muestra ninguna vista previa, sin ningún texto.
El texto en sí solo aparece como cuadro de mensaje si el error se produce en el momento en que se ejecuta el comando.

| Mensaje | Causa | Qué hacer |
| --- | --- | --- |
| "Selecciona exactamente una línea de boceto." | El campo **Línea** está vacío, o el objeto seleccionado no es una línea de boceto | Seleccionar una línea de boceto recta |
| "La longitud debe ser mayor que 0." | **Longitud** es 0 o negativa | Introducir una longitud mayor que 0 |
| "La línea seleccionada no tiene longitud." | El punto inicial y el punto final de la línea están en el mismo lugar (solo se comparan X e Y) | Seleccionar otra línea |
| "La longitud supera la línea seleccionada ({0} mm)." | **Longitud** es mayor que la línea seleccionada. `{0}` es la longitud de la línea en mm con dos decimales | Introducir una longitud de hasta ese valor, o seleccionar una línea más larga |

## Mensajes del propio complemento

Los cuatro mensajes con `{0}` muestran un traceback de Python en el lugar de `{0}`. El traceback nombra el archivo y la línea del error.

| Mensaje | Cuándo | Causa | Qué hacer |
| --- | --- | --- | --- |
| "No se encontró ningún panel de barra de herramientas adecuado." | al iniciar | No existe ninguno de los ids de `PANEL_IDS`, ni en el espacio de trabajo `WORKSPACE_ID` ni en ningún otro lugar de Fusion. El complemento funciona, pero no tiene botón | Poner en `PANEL_IDS` ids de paneles que existan en la versión de Fusion que se usa. Véase [settings.md](settings.md) |
| "Error al crear la geometría: {0}" | después de OK | Un error inesperado en `read_inputs()`, `validate()`, `build_result()` o `remember()`: un fallo del programa, no un dato mal introducido | Leer las últimas líneas del traceback y corregir el código. Si el usuario puede provocarlo, hay que atrapar el caso en `validate()` con `fail('err.key')` |
| "Error al construir el cuadro de diálogo: {0}" | al pulsar el botón | Un error inesperado en `build_inputs()` o al conectar los manejadores | Leer el traceback. Típico: el mismo id de campo de entrada usado dos veces, o un texto de unidad equivocado |
| "Error al iniciar: {0}" | cuando el complemento se inicia | Un error inesperado en `run()` | Leer el traceback |
| "Error al detener: {0}" | cuando el complemento se detiene | Un error inesperado en `stop()` | Leer el traceback. Reiniciar Fusion si el botón se queda en la barra de herramientas |

Las causas «típicas» de esta tabla son ejemplos. No se reprodujeron en Fusion para esta documentación.

## Mensajes del script generador

| Mensaje | Causa | Qué hacer |
| --- | --- | --- |
| `The name must start with a letter and contain only letters and digits - it becomes a Python module name. Got: '…'` | El nombre tiene un espacio, un guion, un guion bajo u otro signo, o empieza por una cifra | Usar un nombre como `MyAddIn` |
| `Pick a name other than AddInTemplate.` | El nombre es el nombre propio de la plantilla | Elegir otro nombre |
| `Template folder not found: …` | Falta `apps/desktop-template/AddInTemplate`. El script se movió de sitio, o el repositorio está incompleto | Ejecutar el script desde una copia completa del repositorio |
| `… already exists. Pass --force to overwrite it.` | La carpeta de destino existe | Elegir otro nombre u otra carpeta. `--force` borra la carpeta existente con todo lo que contiene |
| `Use either --install or --out, not both.` | Se dieron las dos opciones | Usar una de ellas |

En un sistema que no es macOS, `--install` construye la ruta a partir de la variable de entorno `APPDATA`. Si no está definida (por ejemplo en Linux), la carpeta se crea de forma relativa a la carpeta actual. Allí hay que usar `--out`.

## Mensajes de las herramientas de versión y de empaquetado

| Mensaje | Causa | Qué hacer |
| --- | --- | --- |
| `The version needs four numbers, like 1.0.0.0 - got '…'` | La versión no tiene cuatro partes | Usar `v.x.y.z`, por ejemplo `1.0.0.1` |
| `No add-in "…". There are: …` | El nombre no es una carpeta `apps/desktop-<name>` con exactamente un manifiesto | Usar un nombre de la lista. La plantilla se llama `template` |
| `No "version" entry in …` | El manifiesto no tiene campo `version` | Añadir el campo al manifiesto |
| `DIFFERENT OR NOT v.x.y.z` (de `--check`) | `VERSION` y el manifiesto difieren, o el número no tiene cuatro partes | Ejecutar `python tools/set_version.py template <version>` |
| `template: VERSION and manifest disagree - run tools/set_version.py first.` | Como arriba, detectado al empaquetar | Como arriba, y después empaquetar otra vez |
| `template: … is damaged in the ZIP` | Falló la prueba del ZIP después de empaquetar | Empaquetar otra vez; comprobar el disco |

## Comprobación sin conexión: FAIL y warn

La comprobación se describe en [development.md](development.md). Una línea `FAIL` nombra lo que está mal. Las líneas `warn` no hacen que la comprobación falle.

| Aviso | Significado |
| --- | --- |
| `id is not the placeholder GUID` | El manifiesto sigue teniendo los ceros como `id` |
| `author has been filled in` | El autor sigue siendo `Your Name` |
| `CMD_ID is no longer the template default` | `CMD_ID` sigue siendo `thwAddInTemplateCmd` |
| `the core module was renamed, so it cannot clash with another add-in` | Un complemento que no es la plantilla sigue usando `addin_core` |
| `cmd.tooltip no longer says TODO` | La información sobre herramientas en inglés sigue conteniendo `TODO` |

Para la propia plantilla, los tres primeros avisos son normales.

## Trampas

Proceden de los comentarios del código.

| Síntoma | Causa | Qué hacer |
| --- | --- | --- |
| Un cambio en el código no tiene efecto | Fusion guarda en caché los módulos importados. Un módulo editado conserva su versión antigua hasta que Fusion se reinicia | Detener el complemento y ejecutarlo otra vez. Esto funciona para el módulo central, porque el archivo de entrada lo quita de `sys.modules` antes de importarlo. Hay que dar el mismo trato a cada módulo propio adicional |
| El botón de otro complemento hace algo extraño, o lo hace el propio | Dos complementos usan el mismo `CMD_ID`. La coincidencia no avisa | Usar un prefijo propio y un id único |
| Dos complementos hechos con la plantilla se estorban entre sí | Los dos usan un módulo central con el mismo nombre | Conservar el módulo central con el nombre cambiado `<name>_core.py` |
| Un evento deja de dispararse, sin ningún error | Fusion solo sujeta los manejadores de forma débil. Un manejador al que Python ya no hace referencia se elimina | Conectar cada manejador con `_handlers.add(event, handler)` |
| El botón conserva un rótulo antiguo o un comportamiento antiguo | Sigue ahí una definición de comando de una ejecución anterior | `run()` la borra primero. Hay que conservar ese código |
| OK está en gris y nadie sabe por qué | La validación y la vista previa no muestran ningún motivo | Es así por diseño. Hay que mantener las reglas sencillas y nombrarlas en la información sobre herramientas o en los rótulos |
| La vista previa no muestra nada | La vista previa se traga todos los errores, también los fallos reales del programa | Pulsar OK con entradas válidas. La ejecución muestra el error con traceback |
| Aparece un mensaje con cada pulsación de tecla | La presentación de errores se trasladó a la vista previa | Dejar la vista previa en silencio. Se dispara con cada pulsación de tecla, también con valores a medio escribir |
| Los valores son diez veces demasiado grandes o pequeños | Fusion cuenta en cm, muestre lo que muestre el campo. `createByReal(1.0)` mostrado en `mm` se lee como 10 mm | Calcular en cm. Multiplicar por 10 solo para mostrar en mm |
| El boceto ya no se actualiza después de un error | `isComputeDeferred` se puso en `True` y nunca se restableció | Restablecerlo en un bloque `finally`, como hace `build_result()` |
| `on_input_changed()` se ejecuta sin fin o dos veces | Un valor escrito de vuelta allí dispara el evento otra vez | Poner `_updating` en `True` antes de la escritura y en `False` después. Es una variable del módulo: hay que declarar `global _updating` en la función |
| Falta el botón después de una actualización de Fusion | Los ids de los paneles cambian entre versiones de Fusion | Poner varios ids en `PANEL_IDS`, el más deseado primero |
| El botón no tiene icono | Falta la carpeta `resources/<name>`. Entonces el complemento no pasa ninguna carpeta de iconos | Crear los iconos, véase [development.md](development.md) |
| Un texto muestra una clave como `in.width` | La clave falta en el archivo de idioma **y** en `en.xml` | Añadir la clave a `en.xml` |
| Un texto muestra `{0}` en lugar de un valor | Los marcadores de posición del texto no encajan con los valores dados | Comparar el texto con la llamada `T('key', value)` |
| Todos los textos están en inglés | El idioma no está en `SUPPORTED_LANGUAGES`, o su archivo falta o no es XML válido | Comprobar el archivo y las tablas del módulo central |
| Una corrección de la plantilla no aparece en el complemento propio | Cada complemento tiene su propia copia del módulo central | Copiar la corrección a mano en `<name>_core.py` |
| Fusion no muestra el complemento en la lista | La carpeta, el `.py` y el `.manifest` no llevan el mismo nombre | Dar a los tres el mismo nombre. La comprobación sin conexión lo prueba |
