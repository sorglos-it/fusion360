# Solución de problemas

## OK está atenuado

El cuadro de diálogo atenúa **OK** y no muestra ninguna vista previa cuando los valores no encajan. **No dice por qué.**
Los textos de mensaje de abajo existen en el complemento, pero solo se muestran en una ventana de mensaje si la propia ejecución falla después de OK.

Repasar esta lista de arriba abajo:

1. ¿Hay al menos una línea en **Líneas**?
2. ¿Son **Anchura (base)**, **Profundidad** y **Tolerancia** todas mayores que 0?
3. ¿Es **Tolerancia** menor que la mitad de **Anchura (base)**?
4. Trapecio: ¿está **Ángulo de flanco** entre −89 y 89 grados? Con un ángulo negativo: ¿sigue siendo la punta más ancha que 0?
5. Dos o más dientes: ¿es **Separación (centro a centro)** lo bastante grande? Ver
   [settings.md](settings.md#separación-centro-a-centro) para la fórmula.
6. ¿Es la línea lo bastante larga para todos los dientes? Con varias líneas, comprobar primero la más corta.
7. ¿Se escribió un **Desplazamiento**? Pulsar el botón **Centrar** de la fila **Desplazar** para volver a ponerlo en 0.
8. Triángulo o diente muy puntiagudo: reducir **Tolerancia**, reducir **Profundidad** o aumentar **Anchura (base)**.
9. Punta de trapecio estrecha con una tolerancia grande: reducir **Tolerancia** o cambiar **Ángulo de flanco**.

Consejo: cambiar un solo valor cada vez. El valor cambiado en último lugar es el primer sospechoso.

## Mensajes sobre los valores

Todas las ventanas de mensaje llevan el título "Cola de milano". `{0}`, `{1}` y `{2}` en la tabla representan números o textos
que rellena el complemento. Las longitudes en los mensajes están en milímetros.

| Mensaje | Causa | Qué hacer |
|---|---|---|
| "Selecciona al menos una línea de boceto." | La ejecución se inició sin ninguna línea en **Líneas**. | Hacer clic en al menos una línea de boceto recta. |
| "Línea {0} de {1}: {2}" | Hay varias líneas seleccionadas y una de ellas no admite los valores. {0} es la posición de esa línea en el orden en que se seleccionaron, {1} el número de líneas, {2} el mensaje en sí. | Leer el mensaje que sigue a los dos puntos y buscarlo en esta tabla. Cambiar los valores, o quitar esa línea de la selección. |
| "La línea seleccionada no tiene longitud." | El punto inicial y el punto final de la línea están en el mismo sitio (vistos en plano en el boceto). | Seleccionar otra línea o alargarla. |
| "La anchura debe ser mayor que 0." | **Anchura (base)** es 0 o negativa. | Introducir una anchura por encima de 0. |
| "La profundidad debe ser mayor que 0." | **Profundidad** es 0 o negativa. | Introducir una profundidad por encima de 0. |
| "Una banda cerrada necesita una tolerancia mayor que 0." | **Tolerancia** es 0 o negativa. La banda consiste en la holgura; sin holgura no hay banda. | Introducir una tolerancia por encima de 0. |
| "La geometría reflejada necesita un número par de dientes." | **Reflejar la geometría** está activado y **Cantidad** es impar. Normalmente el cuadro de diálogo lo corrige por sí solo. | Poner una cantidad par. |
| "La geometría reflejada solo funciona con la línea media, la única en la que ambas piezas ceden lo mismo." | **Reflejar la geometría** está activado y **La línea es** no es la línea media. Normalmente el cuadro de diálogo lo corrige por sí solo. | Elegir "Línea media - media tolerancia por lado" o desactivar el reflejo. |
| "La geometría reflejada necesita el desplazamiento a 0; si no, el patrón deja de ser simétrico respecto al punto medio de la línea." | **Reflejar la geometría** está activado y **Desplazamiento** no es 0. Normalmente el cuadro de diálogo lo corrige por sí solo. | Poner el desplazamiento en 0 o desactivar el reflejo. |
| "Se necesita al menos una cola de milano." | **Cantidad** está por debajo de 1. El campo del cuadro de diálogo no lo permite. | Poner una cantidad de 1 o más. |
| "El ángulo de flanco debe estar entre -89 y 89 grados." | Trapecio: **Ángulo de flanco** es de 89 grados o más, o de −89 grados o menos. | Introducir un ángulo dentro de este rango. |
| "Ángulo de flanco demasiado negativo - el diente se reduce a cero." | Trapecio con un ángulo negativo: los lados se encuentran antes de llegar a la punta. | Usar un ángulo menos negativo, menos profundidad o más anchura. |
| "La separación debe ser mayor que 0." | Dos o más dientes y **Separación (centro a centro)** es 0 o negativa. | Introducir una separación por encima de 0. |
| "La separación es demasiado pequeña - las colas de milano se solaparían. Se necesitan al menos {0} mm." | Dos o más dientes están demasiado juntos. {0} es la separación mínima para los valores dados. | Introducir al menos la separación indicada, o reducir la anchura, el ángulo de flanco o la tolerancia. |
| "El desplazamiento empuja el dentado más allá del final de la línea. Como máximo son posibles +/- {0} mm." | **Desplazamiento** es mayor de lo que permite la línea. {0} es el desplazamiento máximo posible. | Reducir el desplazamiento al valor indicado, o pulsar **Centrar**. |
| "El dentado es más ancho que la línea seleccionada ({0} mm). Reduce la cantidad, la anchura o la separación." | Los dientes más la distancia a los extremos de la línea no caben en la línea. {0} es la longitud de la línea. El mismo texto aparece si un contorno pasara de un extremo de la línea. | Reducir **Cantidad**, **Anchura (base)** o **Separación (centro a centro)**, o usar una línea más larga. |
| "El contorno de acoplamiento se descontrola en una esquina afilada. Haz el diente más plano (menos profundidad / más anchura) o reduce la tolerancia." | En una esquina muy afilada, el contorno desplazado saldría disparado lejos del diente (más de 12 veces la distancia de desplazamiento). | Menos profundidad, más anchura o menos tolerancia. |
| "La tolerancia se come el diente entero. Reduce la tolerancia o aumenta la profundidad." | Después de quitar la tolerancia no queda nada del diente, o un tramo del contorno se reduce a nada, o el contorno se cruzaría a sí mismo. | Reducir **Tolerancia** o aumentar **Profundidad**. Con una punta de trapecio estrecha, probar también una anchura mayor u otro ángulo de flanco. |
| "La tolerancia es demasiado grande en relación con la profundidad." | Queda menos del 5 % de **Profundidad** como altura del diente. | Reducir **Tolerancia** o aumentar **Profundidad**. |
| "La tolerancia es demasiado grande en relación con la anchura." | El doble de **Tolerancia** es tan grande como **Anchura (base)** o mayor. | Reducir **Tolerancia** o aumentar **Anchura (base)**. |
| "El contorno está degenerado." | Una red de seguridad: el contorno tiene demasiado pocos puntos, o los dos contornos no tienen el mismo número de puntos. Con las demás comprobaciones en su sitio, no debería aparecer en el uso normal. | Cambiar ligeramente los valores. Si vuelve a aparecer, comunicarlo junto con los valores usados. |

## Mensajes sobre el programa

Estos mensajes contienen un informe técnico de error (un "traceback") en lugar de `{0}`. Significan un error inesperado,
no un valor incorrecto.

| Mensaje | Cuándo | Qué hacer |
|---|---|---|
| "No se encontró ningún panel de barra de herramientas adecuado." | Al iniciar. Ninguno de los tres lugares de la barra de herramientas existe en este Fusion (ver [installation.md](installation.md#primer-inicio-en-fusion)). El botón no se crea. | Actualizar Fusion. Si el mensaje sigue, comunicarlo junto con la versión de Fusion. |
| "Error al crear la geometría: {0}" | Después de OK, ocurrió un error inesperado al dibujar. La ejecución se comunica a Fusion como fallida. | Comprobar el boceto; usar Undo (Deshacer) si quedaron líneas. Intentarlo de nuevo. Si se repite, comunicar el texto completo. |
| "Error al construir el cuadro de diálogo: {0}" | No se pudo construir el cuadro de diálogo al hacer clic en el botón. | Detener e iniciar el complemento. Comprobar que las carpetas `lang` y `resources` están completas. Si se repite, comunicar el texto completo. |
| "Error al iniciar: {0}" | El complemento no pudo iniciarse. | Comprobar que la carpeta está descomprimida por completo y se llama `Dovetail`. Instalarlo de nuevo. Si se repite, comunicar el texto completo. |
| "Error al detener: {0}" | El complemento no pudo detenerse limpiamente. | Reiniciar Fusion. |

Avisos de errores: <https://github.com/sorglos-it/fusion360/issues>

## Otros problemas

| Problema | Causa | Qué hacer |
|---|---|---|
| No hay botón después de instalar | El complemento no está en ejecución, o la carpeta está anidada un nivel de más | Seguir de nuevo [installation.md](installation.md); comprobar que existe `AddIns/Dovetail/Dovetail.py` |
| No se puede hacer clic en una línea en el cuadro de diálogo | Solo se aceptan líneas de boceto rectas | Usar una línea recta; arcos, círculos y splines no son compatibles |
| La banda muestra dos áreas en lugar de una | La línea original sigue atravesando la banda como línea normal | Marcar **Convertir la línea original en geometría de construcción**, o convertir la línea en geometría de construcción a mano |
| La vista previa sigue mostrando la línea original como línea normal | La vista previa nunca cambia la línea original | Nada; la línea se convierte con OK |
| Los dientes están en el lado equivocado | El lado depende del sentido en que se dibujó la línea | Marcar **Invertir la dirección** |
| Unas líneas tienen los dientes en un lado y otras en el otro | Las líneas se dibujaron en sentidos opuestos | Ejecutar el comando por separado para los dos grupos, una vez con y otra sin **Invertir la dirección** |
| Los botones de **Desplazar** no hacen nada | **Incremento** es 0, o se alcanzó el límite, o **Reflejar la geometría** está activado | Poner un incremento, o comprobar el sitio en la línea |
| **Desplazamiento**, **La línea es**, **Incremento** están atenuados | **Reflejar la geometría** está marcado | Quitar la marca |
| Se muestra un idioma equivocado | El idioma se elige cuando se inicia el complemento; los idiomas distintos de los cinco compatibles pasan al inglés | Ver [settings.md](settings.md#idioma) |
| Los valores han vuelto a los valores por defecto | Solo se recuerdan mientras Fusion está abierto | Introducirlos de nuevo |

## Límites conocidos

- **No se muestra ningún motivo cuando OK está atenuado.** Los textos de mensaje solo se muestran si la propia ejecución falla.
- **La altura se ignora.** Las líneas en un boceto 3D o las líneas fuera del plano del boceto se tratan como si fueran planas.
- **Solo líneas rectas.** Arcos, círculos y splines no se pueden seleccionar.
- **Un solo juego de valores para todas las líneas.** Con varias líneas, cada línea recibe los mismos valores. No hay
  ajuste por línea.
- **Como máximo 100 líneas y 500 dientes por línea.**
- **Un triángulo no se engancha.** Solo el trapecio con un ángulo de flanco positivo resiste que se tire para separarlo.
- **La tolerancia es una holgura, nada más.** El complemento no compensa los efectos del proceso de fabricación.
- **No confirmado dentro de Fusion:** los cambios de geometría de la versión 1.1.0.0 (distancia a los extremos de la línea,
  separación mínima mayor, rechazo de contornos que se cruzan a sí mismos, deshacer tras una ejecución fallida). Se probaron solo sin conexión.
