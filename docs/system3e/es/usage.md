# Uso

Volver al [resumen](index.md).

El complemento tiene una sola función: el comando **Elemento SYSTEM 3E**. Coloca un elemento de muro cada vez que
se ejecuta.

## Colocar un elemento

1. Abrir un diseño en Fusion.
2. En la pestaña **SOLID**, en el panel **Create**, hacer clic en **Elemento SYSTEM 3E**.
3. **Punto**: hacer clic en el lugar para el elemento. Se puede hacer clic en
   - un punto de boceto,
   - una esquina de un cuerpo,
   - un punto de construcción; esto incluye los puntos de un elemento colocado antes.

   Si no se hace clic en nada, el elemento va al origen del diseño. La indicación lo dice:
   "Seleccione un punto (ninguno: origen)".
4. **Familia**: elegir el grupo de elementos.
5. **Elemento**: elegir el elemento. Cada entrada muestra el nombre y el tamaño en mm como largo x ancho x alto,
   por ejemplo `S1 WP   707 x 352 x 300`.
6. Mirar la imagen que hay debajo de la lista. Muestra el elemento elegido.
7. **Colocar por**: elegir qué lugar del elemento cae sobre el punto. Véase más abajo.
8. **Giro**: escribir un ángulo si el elemento debe girarse.
9. **Desplazamiento X**, **Desplazamiento Y**, **Desplazamiento Z**: escribir una distancia si el elemento debe
   alejarse del punto.
10. Pulsar **OK**.

También se puede hacer clic primero en el punto y después en el botón. El complemento pasa el punto al campo
**Punto**.

Mientras el cuadro de diálogo está abierto, Fusion muestra el elemento en su lugar como vista previa. Se crea de
forma definitiva al pulsar **OK**.

## Familia y elemento

Hay ocho familias con 74 elementos. El orden es el del catálogo del fabricante.

| Familia | Elementos |
| --- | --- |
| Arranque | 12 |
| Básico | 6 |
| Complementario | 8 |
| Dintel | 8 |
| Marco de ventana | 6 |
| Remate | 12 |
| Esquina | 18 |
| Tabique | 4 |

Al cambiar la familia, la lista de elementos se rellena de nuevo y queda seleccionado su primer elemento.

Todos los elementos, con su tamaño en mm (largo x ancho x alto):

**Arranque**

| Elemento | Tamaño |
| --- | --- |
| S0 200 WP | 707 x 352 x 200 |
| S0 200 W | 704 x 352 x 200 |
| S0/2 200 W | 352 x 352 x 200 |
| S0/2 200 P | 355 x 352 x 200 |
| S0 250 WP | 707 x 352 x 250 |
| S0 250 W | 704 x 352 x 250 |
| S0/2 250 W | 352 x 352 x 250 |
| S0/2 250 P | 355 x 352 x 250 |
| S0 300 WP | 707 x 352 x 300 |
| S0 300 W | 704 x 352 x 300 |
| S0/2 300 W | 352 x 352 x 300 |
| S0/2 300 P | 355 x 352 x 300 |

**Básico**

| Elemento | Tamaño |
| --- | --- |
| S1 WP | 707 x 352 x 300 |
| S1 W | 704 x 352 x 300 |
| S1/2 W | 352 x 352 x 300 |
| S1/2 P | 355 x 352 x 300 |
| ST W | 222 x 352 x 300 |
| ST P | 225 x 352 x 300 |

**Complementario**

| Elemento | Tamaño |
| --- | --- |
| EU 150 WP | 707 x 352 x 150 |
| EU 150 W | 704 x 352 x 150 |
| EU/2 150 W | 352 x 352 x 150 |
| EU/2 150 P | 355 x 352 x 150 |
| EU 200 WP | 707 x 352 x 200 |
| EU 200 W | 704 x 352 x 200 |
| EU/2 200 W | 352 x 352 x 200 |
| EU/2 200 P | 355 x 352 x 200 |

**Dintel**

| Elemento | Tamaño |
| --- | --- |
| EN WP | 707 x 352 x 170 |
| EN W | 704 x 352 x 170 |
| EN/2 W | 352 x 352 x 170 |
| EN/2 P | 355 x 352 x 170 |
| EPN WP L | 707 x 352 x 300 |
| EPN W L | 704 x 352 x 300 |
| EPN WP P | 707 x 352 x 300 |
| EPN W P | 704 x 352 x 300 |

**Marco de ventana**

| Elemento | Tamaño |
| --- | --- |
| EO/2 WP L | 707 x 352 x 300 |
| EO/2 WP P | 707 x 352 x 300 |
| EO/2 W P | 704 x 352 x 300 |
| EO/2 200 WP L | 707 x 352 x 300 |
| EO/2 200 WP P | 707 x 352 x 300 |
| EO/2 200 W P | 704 x 352 x 300 |

**Remate**

| Elemento | Tamaño |
| --- | --- |
| EWN WP L | 707 x 352 x 250 |
| EWN W L | 704 x 352 x 250 |
| EWN WP P | 707 x 352 x 250 |
| EWN W P | 704 x 352 x 250 |
| SZ/EO WP | 707 x 352 x 250 |
| SZ/EO W | 704 x 352 x 250 |
| SZ/2 W | 352 x 352 x 250 |
| SZ/2 P | 355 x 352 x 250 |
| SZ/EO 200 WP | 707 x 352 x 200 |
| SZ/EO 200 W | 704 x 352 x 200 |
| SZ/2 200 W | 352 x 352 x 200 |
| SZ/2 200 P | 355 x 352 x 200 |

**Esquina**

| Elemento | Tamaño |
| --- | --- |
| SNL | 704 x 352 x 300 |
| SNL/2 | 352 x 352 x 300 |
| SNP | 704 x 352 x 300 |
| SNP/2 | 352 x 352 x 300 |
| ENL | 704 x 352 x 300 |
| ENP | 704 x 352 x 300 |
| SZL | 704 x 352 x 250 |
| SZP | 704 x 352 x 250 |
| EWNL | 704 x 352 x 250 |
| EWNP | 704 x 352 x 250 |
| EO/2 LT | 704 x 352 x 300 |
| EO/2 LP | 698 x 352 x 300 |
| EO/2 PT | 704 x 352 x 300 |
| EO/2 PP | 704 x 352 x 300 |
| EO/2 200 LT | 704 x 352 x 300 |
| EO/2 200 LP | 704 x 352 x 300 |
| EO/2 200 PT | 704 x 352 x 300 |
| EO/2 200 PP | 704 x 352 x 300 |

**Tabique**

| Elemento | Tamaño |
| --- | --- |
| D1 115 | 704 x 115 x 250 |
| D1/2 115 | 352 x 115 x 250 |
| D1 175 | 704 x 175 x 200 |
| D1/2 175 | 352 x 175 x 200 |

Notas sobre la lista:

- Los tamaños son las medidas exteriores guardadas en la biblioteca de elementos, redondeadas a mm enteros.
- Los nombres son los nombres del catálogo. El complemento no los traduce.
- Los nombres izquierda/derecha de los elementos de esquina y de ventana se compararon a ojo con las fichas del
  catálogo del fabricante. **No están confirmados**. Conviene comprobar la imagen y el cuerpo colocado antes de
  fiarse del nombre.
- `S0/2 200 P` está dañado en el archivo 3D del fabricante. Su forma se reconstruye a partir de `S0/2 250 P`.
- Los cuatro elementos de tabique son bloques lisos. Sus tamaños proceden de las fichas del catálogo.

## La imagen de vista previa

- La imagen muestra el elemento elegido como vista sombreada en gris, visto desde delante a la izquierda y desde
  arriba.
- Cambia cuando se cambia **Familia** o **Elemento**.
- Las imágenes se dibujan a partir de la biblioteca de elementos. No están tomadas del catálogo del fabricante.

## Direcciones en un elemento

Estas palabras se usan para los puntos y en **Colocar por**.

| Palabra | Significado |
| --- | --- |
| delante | el extremo del elemento en la longitud 0 |
| detrás | el otro extremo |
| derecha, izquierda | visto desde el extremo delantero, mirando a lo largo del muro |
| abajo | la cara inferior |
| arriba | la altura donde se apoya la hilada siguiente (véase más abajo), o el punto más alto en el caso de las dos esquinas superiores |

Una hilada es una capa de elementos en un muro.

Con **Giro** 0, el largo va a lo largo del eje X del diseño, el espesor del muro a lo largo de Y y el alto a lo
largo de Z. «Derecha» es entonces el lado con el valor de Y más pequeño.

## Los doce puntos de un elemento

Cada elemento colocado lleva doce puntos de construcción. Un punto de construcción es un punto auxiliar de Fusion
en el que se puede hacer clic. Los puntos tienen nombre. Los nombres se escriben en el idioma que usaba el
complemento cuando el elemento se colocó por primera vez.

| Nombre | Dónde está |
| --- | --- |
| abajo delante | cara inferior, extremo delantero, centro del espesor del muro |
| abajo centro | cara inferior, mitad del largo, centro del espesor del muro |
| abajo detrás | cara inferior, extremo trasero, centro del espesor del muro |
| arriba delante | altura de la hilada siguiente, extremo delantero, centro del espesor del muro |
| arriba centro | altura de la hilada siguiente, mitad del largo, centro del espesor del muro |
| arriba detrás | altura de la hilada siguiente, extremo trasero, centro del espesor del muro |
| arriba centro derecha | altura de la hilada siguiente, mitad del largo, cara derecha del muro |
| arriba centro izquierda | altura de la hilada siguiente, mitad del largo, cara izquierda del muro |
| abajo centro derecha | cara inferior, mitad del largo, cara derecha del muro |
| abajo centro izquierda | cara inferior, mitad del largo, cara izquierda del muro |
| centro derecha, 50 mm arriba | 50 mm por encima de la cara inferior, mitad del largo, cara derecha del muro |
| centro izquierda, 50 mm arriba | 50 mm por encima de la cara inferior, mitad del largo, cara izquierda del muro |

«Altura de la hilada siguiente»: los elementos con el perfil en relieve en la parte superior sostienen la hilada
siguiente 50 mm por debajo de su punto más alto. Los elementos planos la sostienen arriba del todo. Ejemplo:
`S1 WP` mide 300 mm de alto, la hilada siguiente se apoya a 250 mm.

El dibujo muestra todos los puntos sobre el elemento básico `S1 WP`. Sus rótulos están en alemán. Amarillo: se
puede hacer clic. Rojo: se puede elegir en **Colocar por**. Verde: ambas cosas.

![Los puntos del elemento S1 WP](../s1-wp-punkte.svg)

Desde la 1.1.0.1 cada punto se muestra sobre la superficie del elemento. Si el lugar de la tabla está dentro del
material o en el aire – en una ranura, sobre una lengüeta, en un hueco – el punto pasa a la superficie de al lado:
primero hacia arriba o hacia abajo, si no a lo largo. Al hacer clic en él se sigue colocando por el lugar de la
tabla, así que un muro a matajunta sale igual. Los elementos colocados con una versión anterior reciben sus puntos
movidos la próxima vez que se coloque un elemento. Este movimiento ha sido usado dentro de Fusion por el autor.

Estado: los puntos han sido usados dentro de Fusion por el autor.

## Colocar por

**Colocar por** decide qué lugar del elemento nuevo cae sobre el punto en el que se hizo clic. La lista tiene 15
entradas:

| Entrada | Lugar del elemento |
| --- | --- |
| Esquina inferior delantera derecha | la esquina más baja del extremo delantero, lado derecho. Es el valor por defecto. |
| Esquina superior delantera derecha | la esquina más alta del extremo delantero, lado derecho |
| Esquina superior delantera izquierda | la esquina más alta del extremo delantero, lado izquierdo |
| abajo delante … centro izquierda, 50 mm arriba | uno de los doce puntos de la tabla de arriba |

Las dos esquinas superiores usan el alto completo del elemento, no la altura de la hilada siguiente.

Estado: las opciones de **Colocar por** han sido usadas dentro de Fusion por el autor.

## Giro

- **Giro** gira el elemento alrededor del eje vertical. Es el eje Z del diseño.
- El giro se hace alrededor del lugar elegido en **Colocar por**. Ese lugar se queda sobre el punto en el que se
  hizo clic.
- El ángulo se indica en grados. Un ángulo positivo gira en sentido contrario a las agujas del reloj, visto desde
  arriba.

## Desplazamientos

- **Desplazamiento X**, **Desplazamiento Y** y **Desplazamiento Z** alejan el elemento del punto en el que se hizo
  clic.
- Los valores están en mm.
- Van a lo largo de los ejes del diseño. No giran con el elemento.
- Los valores negativos mueven en la otra dirección.

Ejemplo: ningún punto seleccionado, **Desplazamiento Z** 300 mm. El elemento se coloca 300 mm por encima del origen.

Estado: los desplazamientos han sido usados dentro de Fusion por el autor.

## Construir un muro a matajunta

«A matajunta» significa: cada hilada está desplazada medio elemento respecto a la hilada de abajo.

1. Colocar el primer elemento de la hilada más baja. Usar **Colocar por**: **Esquina inferior delantera derecha**.
2. Iniciar el comando otra vez. Elegir **Colocar por**: **abajo delante**.
3. Hacer clic en el punto **abajo detrás** del elemento recién colocado. El elemento siguiente continúa la hilada.
4. Repetir esto hasta terminar la primera hilada.
5. Para la segunda hilada, iniciar el comando otra vez. Elegir **Colocar por**: **abajo centro**.
6. Hacer clic en el punto **arriba delante** o **arriba detrás** de un elemento de la hilada de abajo.
   El elemento nuevo queda entonces mitad sobre ese elemento y mitad al lado.
7. Continuar la segunda hilada como en los pasos 2 y 3.

Los ajustes se quedan como se dejaron, así que solo hay que hacer clic en el punto siguiente y pulsar **OK**.

Notas:

- El paso 6 es el camino que da la propia descripción del complemento para un muro a matajunta. Los pasos 2 a 4 se
  deducen de las posiciones de los puntos; **no están probados dentro de Fusion**.
- En los elementos con lengüeta en el extremo (3 mm más largos, nombres que terminan en `WP` o `P`), los puntos
  **abajo delante** y **abajo detrás** están en los extremos más exteriores. Conviene comprobar en el diseño la
  junta entre dos elementos.
- El complemento no comprueba si los elementos se solapan ni si un elemento cabe en un lugar.

## Lista de piezas: cómo cuentan los elementos iguales

- La primera vez que se coloca un elemento, el complemento crea un componente llamado `SYSTEM 3E <name>`,
  por ejemplo `SYSTEM 3E S1 WP`. El cuerpo que hay dentro se llama como el elemento, por ejemplo `S1 WP`.
- Cada vez más que se coloca el mismo elemento en ese diseño, el complemento añade otra copia de ese mismo
  componente. No crea un componente nuevo.
- Por eso una lista de piezas muestra una sola línea para el elemento con su cantidad, y no `S1 WP`, `S1 WP (1)`,
  `S1 WP (2)`.
- Se puede cambiar el nombre del componente. El complemento lo sigue encontrando, porque deja en él una marca
  invisible.
- Como las copias comparten un solo componente, un cambio en el cuerpo de una copia cambia todas las copias.
- Todos los elementos se crean directamente en el nivel superior del diseño (el componente raíz).
