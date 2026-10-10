# Cómo funciona

## Archivos

El complemento instalado es una sola carpeta, `SketchGrid`:

| Archivo | Finalidad |
| --- | --- |
| `SketchGrid.py` | El complemento en sí: cuadro de diálogo, cálculo de la rejilla, comprobaciones, dibujo. |
| `sketchgrid_core.py` | Funciones auxiliares compartidas que no son específicas de este complemento: leer los archivos de idioma, determinar el idioma, encontrar el panel de la barra de herramientas, mantener vivos los manejadores de eventos, mostrar errores inesperados, leer la versión. |
| `SketchGrid.manifest` | Descripción para Fusion: autor, versión, sistemas compatibles (Windows y macOS), inicio con Fusion. |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Todos los textos, un archivo por idioma. `en.xml` es la referencia. |
| `resources/SketchGrid/16x16.png`, `32x32.png`, `64x64.png` | El icono del botón en tres tamaños. |

El complemento solo lee su propia carpeta. No escribe ningún archivo y no abre ninguna conexión de red.

## Inicio y parada

Al iniciar (`run`):

1. Se detecta el idioma y se carga el archivo de idioma correspondiente.
2. Se borra una definición de comando que haya quedado de un inicio anterior.
3. Se crea el comando. Su nombre es el texto **Rejilla de boceto** más la versión del manifiesto entre paréntesis.
4. El complemento busca un panel de la barra de herramientas: primero el panel con el id `SketchCreatePanel`, después `SolidCreatePanel`; cada uno primero en el espacio de trabajo Design, después entre todos los paneles. Si no existe ninguno, aparece el mensaje "No se encontró ningún panel de barra de herramientas adecuado." y no se añade ningún botón.
5. El botón se añade al panel y se muestra directamente en la barra de herramientas.

Al detener (`stop`), se quitan el botón y el comando y se liberan los manejadores de eventos.

## Qué pasa mientras el cuadro de diálogo está abierto

| Evento | Qué hace el complemento |
| --- | --- |
| Se abre el cuadro de diálogo | Construye todos los campos con los valores recordados. Intenta tomar un punto de boceto seleccionado de antemano. Si eso falla, el cuadro de diálogo sigue siendo utilizable y el punto se selecciona en el cuadro de diálogo. (Probado solo sin conexión, no dentro de Fusion.) |
| Cambia un campo | Muestra u oculta los campos que corresponden al modo y a la forma elegidos. Recalcula la línea **Resultado**. |
| Fusion pregunta si las entradas son válidas | Ejecuta todas las comprobaciones. Si una falla, **OK** se desactiva. |
| Fusion pide una vista previa | Ejecuta todas las comprobaciones y dibuja la rejilla como vista previa. Si una comprobación falla, no se dibuja nada y no se comunica nada. |
| **OK** | Ejecuta de nuevo todas las comprobaciones, dibuja la rejilla y después recuerda los valores. |

La vista previa no se reutiliza como resultado final. Con **OK** la rejilla se dibuja de nuevo.

## Unidades

- Por dentro, todas las longitudes son centímetros. Es la unidad interna de Fusion, sea cual sea la unidad que muestre el documento.
- Los campos de longitud del cuadro de diálogo se crean con la unidad `mm`.
- Para la línea **Resultado** y para los mensajes, los valores se convierten a milímetros (× 10) y se muestran con dos decimales.
- Las comparaciones admiten una tolerancia minúscula de 0.000000001 cm, para que el ruido de redondeo no provoque un mensaje.

## Cómo se calcula la rejilla

El cálculo lo hace `grid_layout()`. No usa ninguna función de Fusion.

### Paso 1: tamaño de una forma

Normalmente una forma ocupa exactamente longitud × profundidad.

Excepción: un polígono con **Regular** marcado. Ocupa menos sitio. Su tamaño real se mide:

1. Las esquinas del polígono se colocan sobre un círculo de radio 1, con la primera esquina apuntando hacia arriba.
2. Se miden la anchura y la altura de la caja más pequeña alrededor de estas esquinas.
3. Ambas se multiplican por la mitad de la menor de longitud y profundidad.

Ejemplo: 6 lados, longitud 10 mm, profundidad 5 mm da 4.33 × 5.00 mm.

### Paso 2: paso

Paso significa la distancia de una forma al mismo punto de la forma siguiente.

- paso X = tamaño de una forma en X + **Separación X**
- paso Y = tamaño de una forma en Y + **Separación Y**

### Paso 3: número de columnas y filas

**Columnas y filas:** se usan los números del cuadro de diálogo.

**Relleno de un área:** n formas necesitan n tamaños y n − 1 separaciones. Por tanto:

- columnas = (ancho del área + separación X) ÷ paso X, redondeado hacia abajo
- filas = (alto del área + separación Y) ÷ paso Y, redondeado hacia abajo

Ejemplo: (100 + 2) ÷ 12 = 8.5, así que 8 columnas.

Si columnas × filas es más de 2000, la rejilla se rechaza.

### Paso 4: tamaño total

- anchura total = columnas × paso X − separación X
- altura total = filas × paso Y − separación Y

Ejemplo: 8 × 12 − 2 = 94 mm.

### Paso 5: posición (punto de referencia y desfase)

El punto de referencia es la entrada elegida en **El punto está en la rejilla**. Cada entrada representa dos factores entre 0 y 1: a qué distancia está el punto del borde izquierdo y del borde inferior de la rejilla, como parte del tamaño total.

| Entrada | Factor X | Factor Y |
| --- | --- | --- |
| En el centro | 0.5 | 0.5 |
| Abajo a la izquierda | 0 | 0 |
| Abajo a la derecha | 1 | 0 |
| Arriba a la izquierda | 0 | 1 |
| Arriba a la derecha | 1 | 1 |
| Abajo al centro | 0.5 | 0 |
| Arriba al centro | 0.5 | 1 |
| A la izquierda al centro | 0 | 0.5 |
| A la derecha al centro | 1 | 0.5 |

La esquina inferior izquierda de la rejilla, medida desde el punto seleccionado:

- X = −factor X × anchura total + **Desfase X**
- Y = −factor Y × altura total + **Desfase Y**

Ejemplo: rejilla de 94 × 26 mm, **En el centro**, sin desfase: la esquina inferior izquierda está 47 mm a la izquierda del punto y 13 mm por debajo de él.

Los desfases solo se suman en este punto. No cambian el número de formas, tampoco en el modo **Relleno de un área**.

### Paso 6: las formas sueltas

`cell_centres()` recorre la rejilla fila por fila, desde la fila inferior hacia arriba, y en cada fila de izquierda a derecha. Para cada forma devuelve la esquina inferior izquierda de su sitio:

- X = esquina X de la rejilla + número de columna × paso X
- Y = esquina Y de la rejilla + número de fila × paso Y

Los números de columna y de fila empiezan en 0. El nombre de la función es histórico; devuelve esquinas, no centros.

El código de dibujo suma la mitad del tamaño de una forma para obtener el centro, y suma la posición del punto seleccionado en el boceto.

Todas las posiciones están en las coordenadas del boceto al que pertenece el punto. Por eso la rejilla es siempre paralela a los ejes X e Y de ese boceto.

## Cómo se dibuja cada forma

| Forma | Caso | Se dibuja como |
| --- | --- | --- |
| Rectángulo | esquinas **Vivas** | el rectángulo de dos puntos de Fusion, de la esquina inferior izquierda a la superior derecha |
| Rectángulo | **Redondeadas**, radio igual a la mitad de ambos lados | un círculo |
| Rectángulo | **Redondeadas**, en los demás casos | hasta 4 líneas y 4 arcos |
| Rectángulo | **Achaflanadas** | hasta 4 líneas para los lados y 4 líneas para los cortes |
| Círculo / elipse | la longitud es igual a la profundidad | un círculo |
| Círculo / elipse | en los demás casos | una elipse; la mayor de las dos se pasa a Fusion como eje principal, porque si no Fusion rechaza la elipse |
| Ranura | la longitud es igual a la profundidad | un círculo |
| Ranura | en los demás casos | 2 líneas y 2 arcos semicirculares; los arcos están en los dos extremos de la dirección más larga, su radio es la mitad de la más corta |
| Polígono | siempre | una línea por lado |

Detalles:

- **Rectángulo redondeado o achaflanado:** `corner_outline()` devuelve el contorno como una lista de líneas y arcos, en sentido antihorario desde el borde inferior. Cada arco se da con tres puntos: inicio, un punto en el medio del arco, final. Cuando el radio o el chaflán es exactamente la mitad de un lado, el tramo recto de ese lado no tiene longitud y se omite.
- **Polígono:** la primera esquina apunta hacia arriba. Sin **Regular**, las esquinas se estiran para que la caja más pequeña a su alrededor mida exactamente longitud × profundidad. Con **Regular**, ambas direcciones se escalan con la mitad de la menor de longitud y profundidad. En ambos casos el polígono se centra en su propia caja, no en su círculo. Esto importa con números impares de lados: una forma de cinco lados tiene una esquina arriba pero una base plana.
- **Conexión de las curvas:** el polígono se dibuja como una cadena. Cada línea empieza en el punto final de la línea anterior, y la última cierra sobre el punto inicial de la primera. La ranura y el rectángulo redondeado o achaflanado se dibujan de otra manera: cada línea y cada arco se crea por separado a partir de coordenadas. Sus extremos están en el mismo sitio, pero no se crean como puntos compartidos. Ver [límites conocidos](troubleshooting.md#límites-conocidos).
- El propio complemento no añade cotas ni restricciones. Que Fusion añada algunas por su cuenta al rectángulo de dos puntos no lo decide el complemento.

Mientras se dibuja la rejilla, se indica al boceto que no recalcule después de cada curva suelta (`isComputeDeferred`). Recalcula una sola vez al final. El ajuste se restablece en todos los casos, también después de un error.

## Las comprobaciones

Orden en que se ejecutan las comprobaciones:

1. Está seleccionado exactamente un punto de boceto.
2. Si la forma es un polígono: lados entre 3 y 24.
3. Longitud mayor que 0.
4. Profundidad mayor que 0.
5. Ninguna separación negativa.
6. Modo **Relleno de un área**: ambos valores del área mayores que 0; después, que quepan al menos una columna y una fila.
7. Modo **Columnas y filas**: al menos una columna, al menos una fila.
8. Columnas × filas como máximo 2000.
9. Si la forma es un rectángulo y las esquinas no son **Vivas**: radio / chaflán mayor que 0, y como máximo la mitad del lado más corto. Un valor demasiado grande se rechaza, no se reduce en silencio.

La primera comprobación que falla decide el mensaje. Los textos están en [troubleshooting.md](troubleshooting.md).

La línea **Resultado** solo ejecuta las comprobaciones 3 a 9. Por eso, si falla la comprobación 1 o la 2, **OK** se desactiva sin ningún texto en la línea **Resultado**.

## Textos e idioma

- Cada archivo de idioma es una lista de claves y textos. El código solo conoce las claves.
- Los lugares para valores se escriben como `{0}`, `{1}`, etc. en los textos y los rellena el complemento.
- El inglés se carga primero como recurso. Una clave que falta en el idioma activo se toma del inglés. Una clave que falta en todos se muestra como la propia clave.
- Cómo se elige el idioma: ver [settings.md](settings.md#idioma).
