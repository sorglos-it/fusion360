# Cómo funciona

## Dos archivos

| Archivo | Papel |
| --- | --- |
| Archivo de entrada `AddInTemplate.py` (después `<name>.py`) | Lo que Fusion inicia. Contiene los ajustes, las funciones propias, los manejadores de eventos, `run` y `stop` |
| Módulo central `addin_core.py` (después `<name>_core.py`) | Partes que todo complemento necesita y en las que es fácil equivocarse. Nada de lo que contiene pertenece a un solo complemento |

Fusion encuentra un complemento por el nombre: la carpeta, el archivo `.py` y el archivo `.manifest` deben llevar el mismo nombre.

## Qué contiene el módulo central

| Parte | Tarea |
| --- | --- |
| `Strings` | Catálogo de textos leído de `lang/<code>.xml`, con el inglés como reserva |
| `detect_language()` | Averigua en qué idioma está ajustado Fusion |
| `AddInError` | Tipo de error para los fallos que el usuario puede corregir. Lleva una clave que no depende del idioma |
| `HandlerRegistry` | Mantiene vivos los manejadores de eventos |
| `find_panel()` | Encuentra el primer panel de la barra de herramientas de una lista que exista |
| `add_button()` | Pone el comando en un panel. Antes quita un control que haya quedado de una recarga |
| `remove_button()` | Vuelve a quitar de la barra de herramientas el control y la definición del comando |
| `report()` | Muestra un error inesperado con su traceback en un cuadro de mensaje |
| `read_version()` | Lee la versión del manifiesto |
| `display_name()` | Une nombre y versión: `Name (1.0.0.0)` |
| `FALLBACK_LANGUAGE`, `SUPPORTED_LANGUAGES`, `FUSION_LANGUAGE_MAP` | Las tablas de idiomas |

## Por qué el módulo central cambia de nombre en cada complemento

Todos los complementos se ejecutan en el mismo Python dentro de Fusion. Comparten una sola lista de módulos cargados (`sys.modules`).
Si dos complementos cargaran ambos un módulo llamado `addin_core`, cada uno sobrescribiría el módulo central del otro.

Por eso el script cambia el nombre del archivo a `<name en minúsculas>_core.py` y ajusta `_CORE_MODULE` en el archivo de entrada para que coincida.

Consecuencia: cada complemento tiene su **propia copia** del módulo central. Una corrección hecha más tarde en la plantilla no llega a los complementos creados antes. Hay que copiarla a mano.

## Cargar el módulo central

El archivo de entrada hace esto antes que cualquier otra cosa:

1. Añade su propia carpeta a la ruta de búsqueda de Python.
2. Quita el módulo central de `sys.modules`, si está allí.
3. Importa el módulo central por el nombre que hay en `_CORE_MODULE`.

Motivo del paso 2: Fusion guarda en caché los módulos importados. Sin él, un módulo central editado conservaría su versión antigua hasta que Fusion se reinicie. Con él, basta con detener y ejecutar el complemento.

## Registro de manejadores

Fusion solo mantiene una referencia débil a un manejador de eventos. Un manejador al que Python ya no hace referencia se elimina, y su evento deja de dispararse, sin ningún mensaje de error. El comentario del código dice que esta es la forma más habitual de que un complemento funcione a medias.

`HandlerRegistry.add(event, handler)` conecta el manejador con el evento **y** lo guarda en una lista. `clear()` vacía la lista cuando el complemento se detiene.

## Inicio y parada

### `run(context)`

1. Carga el idioma detectado en el catálogo de textos.
2. Borra una definición de comando con el mismo `CMD_ID` que haya quedado de una ejecución anterior. Conservaría su rótulo antiguo y su manejador antiguo.
3. Crea la definición del botón: nombre con versión, información sobre herramientas, carpeta de iconos (si existe).
4. Conecta `CommandCreatedHandler`.
5. Busca un panel. Si no encuentra ninguno, muestra "No se encontró ningún panel de barra de herramientas adecuado." y termina.
6. Añade el botón al panel.

Cualquier otro error se muestra como "Error al iniciar:" con el traceback.

### `stop(context)`

1. Quita el control del panel y borra la definición del comando.
2. Vacía el registro de manejadores.

Un error se muestra como "Error al detener:" con el traceback.

## Flujo de eventos

```
button pressed
   -> commandCreated   build the dialog, connect the four handlers below
        -> inputChanged     a field changed        -> on_input_changed()
        -> validateInputs   may OK be pressed?     -> read_inputs(), validate()
        -> executePreview   show a preview         -> read_inputs(), validate(), build_result()
        -> execute          OK pressed             -> read_inputs(), validate(), build_result(), remember()
```

| Evento | Manejador | Qué hace | En caso de error |
| --- | --- | --- | --- |
| creación | `CommandCreatedHandler` | Marca el comando como repetible. Recoge las líneas de boceto seleccionadas antes de pulsar el botón. Llama a `build_inputs()`. Pone la primera línea recogida en el campo de selección si este sigue vacío. Conecta los otros cuatro manejadores | Cuadro de mensaje "Error al construir el cuadro de diálogo:" con traceback |
| cambio de entrada | `InputChangedHandler` | Llama a `on_input_changed()`. No hace nada mientras `_updating` está activado | en silencio |
| validación | `ValidateHandler` | Llama a `read_inputs()` y a `validate()`. Pone `areInputsValid` en verdadero, o en falso ante cualquier error | OK aparece atenuado en gris, sin mensaje |
| vista previa | `PreviewHandler` | Ejecuta el comando entero. Después pone `isValidResult` en `False`, para que Fusion descarte la vista previa y lance la ejecución para el resultado real | en silencio, sin vista previa |
| ejecución | `ExecuteHandler` | Ejecuta el comando entero y después `remember()` | `AddInError`: cuadro de mensaje con el texto traducido. Cualquier otra cosa: "Error al crear la geometría:" con traceback |

«Ejecuta el comando entero» significa `_run_command()`: `read_inputs()`, después `validate()`, después `build_result()`.

Puntos que se deducen de esto:

- La selección se lee **antes** de crear los campos de entrada y se pasa después al campo de selección. Por eso funciona «hacer clic en una línea y después pulsar el botón».
- La vista previa se dispara con cada pulsación de tecla y ve valores a medio escribir. Por eso calla ante los errores a propósito.
- Ni la vista previa ni la validación dicen al usuario **por qué** algo está mal. Solo la ejecución muestra un texto.
- `build_result()` se ejecuta dos veces para un solo OK: una o más veces para la vista previa y una vez para el resultado real.
- `isValidResult` solo debe ponerse en `True` si la vista previa ya ha producido el resultado final.

## Dos tipos de errores

| Tipo | Cómo se lanza | Qué ve el usuario |
| --- | --- | --- |
| Esperado – el usuario puede corregirlo | `fail('err.key')` lanza `AddInError` | OK atenuado en gris; un cuadro de mensaje con el texto traducido solo en la ejecución |
| Inesperado – un fallo del programa | cualquier otra excepción | Un cuadro de mensaje con el traceback, mediante `core.report()` |

`AddInError` guarda la clave (`err.key`) y los parámetros (`err.params`). El texto se busca cuando se crea el error.
El código propio de la plantilla no lee la clave después; está ahí para el código de quien la use.

## Catálogo de textos y reserva

`S = core.Strings(LANG_DIR)` se crea cuando se importa el archivo de entrada. El inglés se carga al instante, así que hay textos incluso antes de `run()`.
Después, `run()` carga el idioma detectado.

Cómo funciona `load(code)`:

1. Un código que no está en `SUPPORTED_LANGUAGES` pasa a ser `en`.
2. `en.xml` se lee una vez y se guarda como reserva.
3. El archivo del idioma elegido se lee como conjunto actual.

Cómo se encuentra un texto (`get(key, *args)`):

1. el texto del idioma actual, si existe y no está vacío
2. si no, el texto en inglés
3. si no, la propia clave, por ejemplo `in.width`

Después se rellenan los marcadores de posición. Si el relleno falla – por ejemplo, una traducción pide `{1}` pero solo se dio un valor –, el texto se devuelve sin rellenar en lugar de lanzar un error.

Un archivo de idioma que falta o que no es XML válido cuenta como vacío. Entonces todos los textos salen del inglés.
Si `en.xml` también falta o está roto, se muestran las propias claves.

## Detección del idioma

Véase [settings.md](settings.md) para el orden. Dos detalles del código:

- Los valores de idioma de Fusion se buscan por el nombre con `getattr`. Un valor que esta versión de Fusion no conoce no puede romper el complemento.
- La función nunca lanza un error. En el peor de los casos devuelve el inglés.

## Unidades

Fusion cuenta las longitudes internamente en cm. La demostración lo muestra:

- el valor inicial `1.0` se muestra como 10 mm
- el valor leído del campo de longitud está en cm
- para el mensaje "La longitud supera la línea seleccionada ({0} mm)." la longitud de la línea se multiplica por 10 y se muestra con dos decimales

## Datos

El complemento lee su manifiesto y sus archivos de idioma. No escribe ningún archivo.
