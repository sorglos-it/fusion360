# Cómo funciona

## Archivos

Todo lo que necesita el complemento está en una carpeta, `Dovetail`:

| Archivo | Finalidad |
|---|---|
| `Dovetail.py` | El programa completo: idioma, geometría, dibujo, cuadro de diálogo, inicio y parada |
| `Dovetail.manifest` | Descripción para Fusion: nombre, autor, versión, sistemas compatibles, inicio con Fusion |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Todos los textos, un archivo por idioma |
| `resources/Dovetail/` | Icono de la barra de herramientas en 16, 32 y 64 píxeles |
| `resources/nudge_left/`, `nudge_center/`, `nudge_right/` | Iconos de los tres botones de **Desplazar** |

El complemento solo lee estos archivos. No escribe ningún archivo y no abre ninguna conexión de red.

## Inicio y parada

Al iniciarse, el complemento:

1. elige el idioma (ver [settings.md](settings.md#idioma)),
2. registra el comando con el nombre "Cola de milano" más la versión del manifiesto entre paréntesis,
3. busca un panel de la barra de herramientas y pone allí el botón (ver [installation.md](installation.md#primer-inicio-en-fusion)).

Al detenerse, vuelve a quitar el botón y el comando.

## De la línea a la banda

### 1. Una regla a lo largo de la línea

Para cada línea seleccionada el complemento prepara su propio sistema de medida:

- **s** corre a lo largo de la línea, desde el punto inicial (0) hasta el punto final (la longitud de la línea).
- **h** corre en ángulo recto respecto a la línea, hacia el lado al que apuntan los dientes.

Sin **Invertir la dirección**, h apunta a la izquierda mirando desde el punto inicial hacia el punto final.
Con **Invertir la dirección**, h apunta a la derecha.

### 2. Dónde quedan los dientes

El centro del grupo está en: longitud de la línea ÷ 2 + Desplazamiento.
Los dientes se colocan a ambos lados de él, cada uno a una **Separación** del siguiente.

### 3. El contorno nominal

El contorno nominal es el borde común que tendrían las dos piezas sin ninguna holgura. Es una sola línea abierta en zigzag:

1. empieza en el punto inicial de la línea,
2. sigue la línea hasta el primer diente,
3. sube por un lado del diente, cruza la punta y baja por el otro lado,
4. continúa por la línea hasta el siguiente diente,
5. termina en el punto final de la línea.

La punta es un punto en un triángulo y dos puntos en un trapecio o un rectángulo.

Con **Reflejar la geometría**, la primera mitad de los dientes apunta al lado contrario (menos h), la segunda mitad al
lado normal (más h).

### 4. Reparto de la tolerancia

Se hacen dos copias del contorno nominal, cada una desplazada hacia un lado una distancia fija (un desplazamiento paralelo):

- el contorno de la **caja** se desplaza hacia el lado de los dientes. La caja se hace más grande.
- el contorno de la **espiga** se desplaza hacia el otro lado. La espiga se hace más pequeña.

**La línea es** decide cuánto se desplaza cada uno:

| Entrada | La caja se desplaza | La espiga se desplaza |
|---|---|---|
| Línea media | ½ × Tolerancia | ½ × Tolerancia |
| Borde de la caja | 0 (se queda sobre el contorno nominal) | Tolerancia |
| Borde de la espiga | Tolerancia | 0 (se queda sobre el contorno nominal) |

Las dos partes suman siempre la tolerancia completa. Como ambos contornos son copias paralelas del mismo contorno,
la holgura entre ellos es igual en todas partes: en la base, en los lados y en la punta.

Cómo se hace el desplazamiento:

- Cada tramo recto se mueve hacia un lado esa distancia.
- En cada esquina, los dos tramos movidos se alargan o se acortan hasta que se encuentran (una esquina a inglete).
- Los dos extremos se mueven en línea recta hacia un lado, de modo que ambos contornos empiezan en s = 0 y terminan en s = longitud de la línea.

### 5. La banda cerrada

Los dos contornos se unen en un solo bucle cerrado:

1. a lo largo del contorno de la caja, del inicio al final de la línea,
2. cruzando hasta el contorno de la espiga en el final de la línea,
3. de vuelta a lo largo del contorno de la espiga,
4. cruzando hasta el punto de partida.

El interior de este bucle es la propia holgura. Es una banda de exactamente la tolerancia que sigue el contorno de los dientes.
Al cortarla de un sólido quedan dos piezas que encajan.

### 6. Dibujo

- La banda se dibuja como una cadena de líneas de boceto rectas. Cada línea empieza en el punto final de la anterior, y
  la última cierra sobre la primera. Por eso el contorno queda conectado.
- Las líneas van al boceto al que pertenece la línea seleccionada.
- Mientras se dibuja, se indica al boceto que no recalcule después de cada línea suelta. Recalcula una sola vez al final.
- Con OK, y solo si la casilla está marcada, la línea original se convierte primero en geometría de construcción. Una
  línea normal atravesaría la banda y la partiría en dos áreas.
- El complemento no añade cotas ni restricciones.

## Las comprobaciones

Antes de dibujar nada, se calcula una vez toda la selección. Solo si todas las líneas pasan, empieza el dibujo.
Así, una línea mala al final de la selección no puede dejar medio boceto dibujado.

Las comprobaciones se ejecutan en este orden para cada línea:

| # | Comprobación | Clave del mensaje si falla |
|---|---|---|
| 1 | La línea tiene longitud | `err.zero_length` |
| 2 | La anchura es mayor que 0 | `err.width` |
| 3 | La profundidad es mayor que 0 | `err.depth` |
| 4 | La tolerancia es mayor que 0 | `err.tolerance_zero` |
| 5 | La cantidad es al menos 1 | `err.count` |
| 6 | Reflejo: la cantidad es par | `err.mirror_even` |
| 7 | Reflejo: está elegida la línea media | `err.mirror_center` |
| 8 | Reflejo: el desplazamiento es 0 | `err.mirror_offset` |
| 9 | Trapecio: el ángulo de flanco está dentro de ±89 grados | `err.angle_range` |
| 10 | Trapecio: la punta conserva una anchura | `err.angle_negative` |
| 11 | Dos o más dientes: la separación es mayor que 0 | `err.spacing_positive` |
| 12 | Dos o más dientes: la separación es al menos la mínima | `err.spacing_too_small` |
| 13 | Los dientes más la distancia a los extremos caben en la línea | `err.offset_range` o `err.does_not_fit` |
| 14 | Ninguna esquina a inglete se aleja más de 12 × la distancia de desplazamiento | `err.miter_runaway` |
| 15 | Ambos contornos empiezan y terminan exactamente en los extremos de la línea y se quedan entre ellos | `err.does_not_fit` |
| 16 | Ningún tramo de un contorno se ha reducido a nada | `err.tolerance_eats_tooth` |
| 17 | Ningún contorno se cruza a sí mismo | `err.tolerance_eats_tooth` |
| 18 | Queda una altura de diente | `err.tolerance_eats_tooth` |
| 19 | La altura de diente que queda es al menos el 5 % de la profundidad | `err.tolerance_vs_depth` |
| 20 | El doble de la tolerancia es menor que la anchura | `err.tolerance_vs_width` |

Con varias líneas, un fallo se envuelve en `err.on_line`, que nombra la posición de la línea en la selección.

Los textos de todos los mensajes están en [troubleshooting.md](troubleshooting.md).

### Qué hace el cuadro de diálogo con una comprobación fallida

- Mientras el cuadro de diálogo está abierto: la vista previa desaparece y **OK** queda atenuado. El texto del mensaje **no** se muestra.
- Si la propia ejecución falla después de OK: una ventana de mensaje muestra el texto, y la ejecución se comunica a Fusion como
  fallida para que Fusion deshaga las líneas ya dibujadas. Este deshacer no se confirmó dentro de Fusion.

## Unidades

| Dónde | Unidad |
|---|---|
| Campos del cuadro de diálogo para longitudes | milímetros |
| Campo del cuadro de diálogo para el ángulo | grados |
| Números en los mensajes | milímetros, dos decimales |
| Dentro del programa | centímetros y radianes (unidades internas de Fusion) |

Valores pequeños fijos en el código:

| Valor | Tamaño | Uso |
|---|---|---|
| Distancia adicional | 0.01 mm | se suma a la separación mínima y a la distancia a los extremos de la línea |
| Tramo más corto | 0.00001 mm | un tramo de contorno más corto que esto cuenta como "sin longitud" |
| Límite de inglete | 12 × distancia de desplazamiento | más allá de esto, una esquina cuenta como descontrolada |
| Ángulo de flanco máximo | por debajo de 89 grados | |

## La altura se ignora

El complemento solo lee los valores X e Y de los extremos de la línea en el boceto y dibuja la banda a la altura 0 del
boceto. Una línea en un boceto 3D, o una que sale del plano del boceto, se trata como si fuera plana.

## Qué cambió en 1.1.0.0

La versión 1.1.0.0 cambió la geometría (construida primero como 1.0.0.1):

- Los dientes guardan la tolerancia más 0.01 mm de distancia con los extremos de la línea. Justo en el extremo, el contorno
  de la caja antes pasaba de la línea y volvía, lo que daba un bucle que se cruzaba a sí mismo. El desplazamiento máximo es menor en esa cantidad.
- Dos dientes necesitan 0.01 mm más de separación. Con exactamente el mínimo antiguo, un tramo del contorno no tenía longitud.
- Un contorno que se cruzaría a sí mismo se rechaza en lugar de dibujarse.
- Una ejecución fallida se deshace.

Estos cambios se probaron **solo sin conexión**, incluidos 34 317 contornos válidos aleatorios, ninguno de los cuales se cruzó a sí mismo.
**Todavía no están confirmados dentro de Fusion**.
