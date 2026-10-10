# Uso

## El comando de demostración

El comando de demostración dibuja una línea corta (una «marca») en el punto medio de una línea de boceto. La marca queda en ángulo recto respecto a esa línea.
Su única tarea es mostrar que la selección, la vista previa, las comprobaciones y la traducción funcionan. Hay que sustituirlo por un comando propio.

En la plantilla sin cambios, el comando se llama **Plantilla de complemento**. Su información sobre herramientas dice:

> Punto de partida para un complemento de Fusion 360.
> Dibuja una marca en el punto medio de la línea seleccionada.

### El cuadro de diálogo

| Campo | Tipo | Significado | Valor inicial |
| --- | --- | --- | --- |
| **Línea** | selección, indicación "Selecciona una línea de boceto" | La línea de boceto que recibe la marca. Exactamente una línea. Solo se pueden seleccionar líneas de boceto | vacío, o la línea que estaba seleccionada antes |
| **Longitud** | valor en mm | Longitud de la marca. Acepta expresiones como `2 * 3 mm` | 10 mm |
| **Invertir la dirección** | casilla de verificación | Dibuja la marca hacia el otro lado de la línea | desactivada |

### Probarlo

1. Abrir un boceto y dibujar una línea.
2. Hacer clic en la línea.
3. Pulsar el botón **Plantilla de complemento**. La línea ya está introducida en **Línea**.
4. Introducir una **Longitud**. La vista previa muestra la marca al instante.
5. Marcar **Invertir la dirección** para pasar la marca al otro lado.
6. Pulsar **OK**.

También se puede pulsar primero el botón y seleccionar la línea después.

### Reglas que comprueba el comando

| Regla | Mensaje cuando no se cumple |
| --- | --- |
| Hay exactamente una línea de boceto seleccionada | "Selecciona exactamente una línea de boceto." |
| La longitud es mayor que 0 | "La longitud debe ser mayor que 0." |
| La línea seleccionada mide más de 0 | "La línea seleccionada no tiene longitud." |
| La marca no es más larga que la línea seleccionada | "La longitud supera la línea seleccionada ({0} mm)." |

Mientras no se cumple una regla, **OK** aparece atenuado en gris y la vista previa se queda vacía. El cuadro de diálogo **no** dice por qué.
El texto del mensaje solo aparece como cuadro de mensaje si el error se produce cuando se ejecuta el comando.

### Otros comportamientos

- **Longitud** e **Invertir la dirección** se recuerdan para la próxima llamada. Se olvidan cuando Fusion se cierra o el complemento se reinicia.
- El comando es repetible (`isRepeatable` está activado), así que la función «repetir el último comando» de Fusion puede iniciarlo otra vez.
- Detalles de la geometría: solo se usan los valores X e Y de los puntos finales de la línea en el boceto. La marca se dibuja en Z = 0 del boceto.

El comportamiento dentro de Fusion está descrito a partir del código. No se probó en Fusion para esta documentación.

## Convertirlo en un complemento propio

Primero hay que crear una copia con el script, véase [installation.md](installation.md). Después se trabaja en `<name>.py`.

El archivo de entrada tiene tres zonas:

| Zona | Contenido | ¿Editar? |
| --- | --- | --- |
| encima de `CONFIGURE` | carga el módulo central | solo cuando se añaden más módulos propios |
| de `CONFIGURE` a `END OF TEMPLATE` | ajustes y las funciones propias | **sí – esta es la zona propia** |
| debajo de `END OF TEMPLATE` | los manejadores de eventos, `run` y `stop` | normalmente no |

### Paso a paso

1. **Ajustar los ids.** Comprobar `CMD_ID`, `WORKSPACE_ID` y `PANEL_IDS`. Véase [settings.md](settings.md).
2. **Dar nombre a los campos de entrada.** Sustituir `IN_LINE`, `IN_LENGTH`, `IN_FLIP` por ids para los campos propios.
3. **Ajustar los valores iniciales.** Poner en `_last` el valor inicial de cada campo que se recuerda. Las longitudes están en cm.
4. **Construir el cuadro de diálogo** en `build_inputs(inputs)`.
5. **Leer el cuadro de diálogo** en `read_inputs(inputs)`.
6. **Comprobar los valores** en `validate(values)`.
7. **Hacer el trabajo** en `build_result(values)`.
8. **Recordar los valores** en `remember(values)`.
9. **Reaccionar a los cambios** en `on_input_changed(inputs, changed)`, si un campo debe cambiar otro.
10. **Escribir los textos.** Añadir las claves propias a `lang/en.xml` y después traducir los demás archivos. Sustituir la información sobre herramientas `TODO`.
11. **Adaptar la preselección.** `CommandCreatedHandler` (debajo de `END OF TEMPLATE`) recoge las líneas de boceto que estaban seleccionadas antes de pulsar el botón. Si el comando necesita otro tipo de objeto, hay que cambiar allí la comprobación del tipo, o quitar el bloque.
12. **Dibujar un icono**, véase [development.md](development.md).
13. **Rellenar el manifiesto**: descripción, autor, versión. Véase [settings.md](settings.md).
14. **Ejecutar la comprobación sin conexión**, véase [development.md](development.md).
15. **Probarlo en Fusion.** Después de cada cambio, detener el complemento y ejecutarlo otra vez.

### Las funciones que se editan

| Función | Para qué sirve | Reglas |
| --- | --- | --- |
| `build_inputs(inputs)` | Dispone el cuadro de diálogo. Cada rótulo sale del catálogo de textos mediante `T('key')` | Devuelve el campo de selección. Quien la llama pone en él la línea preseleccionada. Devolver `None` si no hay campo de selección |
| `read_inputs(inputs)` | Lee todos los valores del cuadro de diálogo en un solo lugar y devuelve un `dict` | La ejecución, la vista previa y la validación la llaman todas, así que ven los mismos números |
| `validate(values)` | Se detiene con `fail('err.key')` ante todo lo que el usuario debe corregir | Se ejecuta antes de dibujar y otra vez para el botón OK. Una entrada imposible atenúa en gris OK en lugar de fallar a medio camino |
| `build_result(values)` | Hace el trabajo de verdad | Cuando se ejecuta, todo está ya comprobado. Se ejecuta para la vista previa **y** para el resultado real |
| `remember(values)` | Copia los valores en `_last` para la próxima llamada | Solo se llama después de una ejecución que salió bien |
| `on_input_changed(inputs, changed)` | Activa, desactiva o ajusta un campo a partir de otro | Vacía en la plantilla. Hay que activar `_updating` alrededor de cada valor que se escriba de vuelta; de lo contrario, la escritura llama otra vez a esta función |

### Ayudas que se llaman

| Ayuda | Qué hace |
| --- | --- |
| `T(key, *args)` | Devuelve el texto de `key` en el idioma activo. `args` rellenan `{0}`, `{1}`, … |
| `fail(key, *args)` | Lanza un `AddInError` con el texto de `key`. Se usa para todo lo que el usuario puede corregir |
| `core.report(ui, S, key)` | Muestra un error inesperado con su traceback. Solo para lo realmente inesperado |

### Añadir un texto

1. Añadir una línea a `lang/en.xml`: `<string key="in.width">Width</string>`
2. Usarla en el código: `T('in.width')`
3. Añadir la misma clave a los demás archivos de idioma.

Las claves que faltan en otro idioma se muestran en inglés. Los marcadores de posición como `{0}` deben conservarse en todas las traducciones.
