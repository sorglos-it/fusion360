# Solución de problemas

Todos los textos están citados del archivo de idioma español. `{0}` y `{1}` representan valores que rellena el complemento.

## Dónde aparecen los mensajes

| Lugar | Cuándo |
| --- | --- |
| Línea **Resultado** del cuadro de diálogo | Un valor no está permitido. Al mismo tiempo **OK** queda desactivado. |
| **OK** desactivado sin texto | No hay ningún punto de boceto seleccionado (ver la primera fila de abajo). |
| Ventana de mensaje con el título **Rejilla de boceto** | Una comprobación falla solo en el momento de pulsar **OK**, o algo inesperado salió mal. |

## Mensajes sobre las entradas

| Mensaje | Causa | Qué hacer |
| --- | --- | --- |
| "Selecciona exactamente un punto de boceto." | **Punto** está vacío, o el objeto seleccionado no es un punto de boceto. Este texto normalmente no se muestra; **OK** simplemente queda desactivado. | Hacer clic en **Punto** y seleccionar un punto de boceto: el origen del boceto o un punto colocado por uno mismo. Los puntos sobre cuerpos no se pueden seleccionar. |
| "La longitud debe ser mayor que 0." | **Longitud (X)** es 0 o negativa. | Introducir un valor por encima de 0. |
| "La profundidad debe ser mayor que 0." | **Profundidad (Y)** es 0 o negativa. | Introducir un valor por encima de 0. |
| "La separación no puede ser negativa." | **Separación X** o **Separación Y** está por debajo de 0. | Introducir 0 o más. No son posibles formas que se solapan. |
| "Se necesita al menos una columna." | **Columnas** está por debajo de 1. | Introducir 1 o más. El propio campo solo acepta de 1 a 2000, así que este mensaje normalmente no debería aparecer. |
| "Se necesita al menos una fila." | **Filas** está por debajo de 1. | Introducir 1 o más. El propio campo solo acepta de 1 a 2000, así que este mensaje normalmente no debería aparecer. |
| "El área debe ser mayor que 0 en ambas direcciones." | Modo **Relleno de un área**: **Ancho del área** o **Alto del área** es 0 o negativo. | Introducir valores por encima de 0 en ambos campos. |
| "En esa área no cabe ni una sola forma. Se necesitan al menos {0} × {1} mm." | Modo **Relleno de un área**: el área es más pequeña que una forma. Los dos números son el tamaño de una forma. | Hacer **Ancho del área** y **Alto del área** al menos tan grandes como los números del mensaje, o hacer la forma más pequeña. |
| "Un polígono necesita entre {0} y {1} lados." | **Lados** está fuera de 3 a 24. | Introducir de 3 a 24. El propio campo solo acepta este rango, así que este mensaje normalmente no debería aparecer. |
| "El radio / chaflán debe ser mayor que 0." | **Esquinas** es **Redondeadas** o **Achaflanadas**, y **Radio / chaflán** es 0 o negativo. | Introducir un valor por encima de 0, o poner **Esquinas** en **Vivas**. |
| "El radio / chaflán puede ser como máximo de {0} mm, la mitad del lado más corto." | **Radio / chaflán** es mayor que la mitad de la menor de **Longitud (X)** y **Profundidad (Y)**. El número es el valor máximo permitido. | Introducir como máximo el valor del mensaje, o hacer el rectángulo más grande. |
| "Serían {0} formas. Como máximo se permiten {1} - más bloquearía Fusion." | Columnas × filas es más de 2000. El primer número es lo que darían los valores introducidos. | Usar menos columnas o filas. En el modo **Relleno de un área**: un área más pequeña, formas más grandes o separaciones más grandes. Para más formas, dibujar varias rejillas. |

Si hay varios valores incorrectos, solo se muestra el primer problema. Corregirlo; después aparece el siguiente.

## Mensajes sobre el propio complemento

Aparecen en una ventana de mensaje. `{0}` se sustituye por un informe técnico de error (un traceback de Python).

| Mensaje | Causa | Qué hacer |
| --- | --- | --- |
| "No se encontró ningún panel de barra de herramientas adecuado." | Al iniciar, el complemento no encontró ni el panel CREATE de la barra de herramientas de boceto ni el panel CREATE de la pestaña SOLID. No se añade ningún botón. | Cambiar al espacio de trabajo **Design**, después detener y ejecutar de nuevo el complemento. Si sigue, comunicarlo junto con la versión de Fusion. |
| "Error al crear la geometría: {0}" | Algo inesperado falló al dibujar después de **OK**. | Intentarlo de nuevo. Si sigue, comunicarlo con el texto completo. |
| "Error al construir el cuadro de diálogo: {0}" | Algo inesperado falló mientras se construía el cuadro de diálogo. | Detener y ejecutar de nuevo el complemento. Si sigue, comunicarlo con el texto completo. |
| "Error al iniciar: {0}" | Algo inesperado falló mientras se iniciaba el complemento. | Comprobar que la carpeta está completa y sigue llamándose `SketchGrid` (ver [installation.md](installation.md)). Ejecutarlo de nuevo. |
| "Error al detener: {0}" | Algo inesperado falló mientras se detenía el complemento. | Reiniciar Fusion. |

Los avisos de errores van a <https://github.com/sorglos-it/fusion360/issues>.

## Otros problemas

| Problema | Causa | Qué hacer |
| --- | --- | --- |
| **OK** está en gris y **Resultado** muestra un resultado normal | No hay ningún punto seleccionado. | Seleccionar un punto de boceto en **Punto**. |
| El punto en el que se hizo clic antes no está en el cuadro de diálogo | El punto no se pudo tomar. Desde la versión 1.1.0.0 el cuadro de diálogo sigue funcionando en este caso (probado solo sin conexión, no dentro de Fusion). | Seleccionar el punto en el cuadro de diálogo. |
| No hay vista previa mientras se escribe | Un valor no está permitido en ese momento. La vista previa se queda vacía sin ningún mensaje. | Leer la línea **Resultado** y corregir el valor. |
| Falta el botón | El complemento no está en ejecución, o no se encontró ningún panel. | Abrir **Utilities → ADD-INS → Add-Ins**, seleccionar **SketchGrid**, pulsar **Run**. |
| El botón muestra un número de versión antiguo | El complemento antiguo sigue en memoria. | Detener el complemento, sustituir la carpeta, ejecutarlo de nuevo. |
| El cuadro de diálogo está en inglés aunque Fusion está puesto en otro idioma | Solo existen alemán, inglés, español, francés e italiano. O el idioma se cambió mientras el complemento estaba en ejecución. | Detener y ejecutar de nuevo el complemento. Ver [settings.md](settings.md#idioma). |
| Un texto aparece como una clave, por ejemplo `in.point` | Los archivos de idioma faltan o están dañados. | Instalar de nuevo el complemento desde el ZIP. |
| La rejilla no llena el área | Solo se dibujan formas completas. | Es intencionado. Ver [usage.md](usage.md#relleno-de-un-área). |
| Un polígono regular es mucho más pequeño que longitud × profundidad | Con **Regular**, la menor de longitud y profundidad fija el tamaño. | Usar valores parecidos para longitud y profundidad, o quitar la marca de **Regular**. |
| El cuadro de diálogo empieza otra vez con los valores estándar | Los valores recordados solo duran hasta que se detiene el complemento o se cierra Fusion. | Introducirlos de nuevo. |

## Límites conocidos

No confirmado dentro de Fusion (encontrado en una revisión del código):

- **Las ranuras y los rectángulos con esquinas redondeadas o achaflanadas** se dibujan como líneas y arcos separados. Sus extremos están en el mismo sitio, pero puede que no sigan conectados al arrastrar una parte de la forma. Los polígonos y los rectángulos de esquinas vivas no se ven afectados de este modo.
- **El límite de 2000 cuenta formas, no curvas.** Un polígono de 24 lados son 24 líneas. Por eso una rejilla grande de polígonos, ranuras o rectángulos recortados puede ser lenta aunque esté dentro del límite.

Según el código:

- Solo se pueden seleccionar puntos de boceto. Esquinas de cuerpos o puntos sobre aristas no.
- La rejilla es siempre paralela a los ejes X e Y del boceto. No se puede girar en el cuadro de diálogo.
- El polígono tiene siempre una esquina apuntando hacia arriba. El cuadro de diálogo no tiene ningún campo para girarlo.
- Solo el rectángulo puede tener esquinas redondeadas o achaflanadas.
- Las separaciones no pueden ser negativas. Las formas no pueden solaparse.
- Las formas son geometría de boceto sencilla. Cambiar un valor más tarde no actualiza una rejilla existente.
- El complemento no añade cotas ni restricciones. La rejilla no queda ligada al punto después de dibujarla.
- Los valores recordados se pierden cuando se detiene el complemento o se cierra Fusion.
- En el modo **Relleno de un área**, el resto vacío solo se centra cuando **El punto está en la rejilla** es **En el centro** (o una entrada "al centro" para esa única dirección).
