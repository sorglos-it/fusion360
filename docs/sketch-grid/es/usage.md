# Uso

Todos los nombres de campo de abajo están escritos exactamente como aparecen en el cuadro de diálogo en español. Detalles de cada campo: [settings.md](settings.md).

## Dibujar una rejilla

1. Abrir o editar un boceto.
2. Hacer clic en un punto de boceto. Puede ser el origen del boceto o un punto colocado por uno mismo.
3. Hacer clic en el botón **Rejilla de boceto**. Se abre el cuadro de diálogo. El punto en el que se hizo clic ya está anotado en **Punto**.
4. Si **Punto** está vacío, hacer clic ahora en un punto de boceto. La indicación dice "Selecciona un punto de boceto".
5. Ajustar los valores. La línea **Resultado** muestra lo que se va a obtener, por ejemplo `8 × 4 = 32 formas, 94.00 × 26.00 mm en total`.
6. Mirar la vista previa en el boceto.
7. Pulsar **OK**.

Solo se pueden seleccionar puntos de boceto. Hace falta exactamente un punto.

**OK** está atenuado mientras un valor no esté permitido. En la mayoría de los casos la línea **Resultado** muestra entonces el motivo. Ver [troubleshooting.md](troubleshooting.md).

La rejilla sigue los ejes X e Y del boceto. No se puede girar en el cuadro de diálogo. Palabras como "izquierda", "derecha", "arriba", "abajo" y "hacia arriba" en esta documentación se refieren a los ejes del boceto: derecha es +X, arriba es +Y.

Tomar un punto en el que se hizo clic antes de abrir el cuadro de diálogo (paso 3) se cambió en la versión 1.1.0.0 y se probó solo sin conexión, no dentro de Fusion. Si el punto no se toma, seleccionarlo en el cuadro de diálogo (paso 4).

## Ejemplo

Estos son los valores con los que empieza el cuadro de diálogo:

| Campo | Valor |
| --- | --- |
| **Forma** | Rectángulo |
| **Longitud (X)** | 10 mm |
| **Profundidad (Y)** | 5 mm |
| **Separación X** / **Separación Y** | 2 mm |
| **Columnas** / **Filas** | 8 / 4 |

Resultado: 32 rectángulos. La rejilla mide 94 × 26 mm (8 × 10 + 7 × 2 = 94, 4 × 5 + 3 × 2 = 26). Con **El punto está en la rejilla** puesto en **En el centro**, el punto es el centro de la rejilla.

## Elegir cómo se cuentan las formas

Campo **Cantidad según**.

### Columnas y filas

1. Poner **Cantidad según** en **Columnas y filas**.
2. Introducir **Columnas** y **Filas**.

Se obtiene exactamente esa cantidad. La rejilla es tan grande como haga falta.

### Relleno de un área

1. Poner **Cantidad según** en **Relleno de un área**.
2. Introducir **Ancho del área** y **Alto del área**.

El complemento dibuja tantas formas como quepan **por completo** en el área. Una forma que solo cabe en parte no se dibuja nunca.

- Ejemplo: ancho del área 100 mm, longitud 10 mm, separación 2 mm da 8 columnas. Ocupan 94 mm. Una novena columna necesitaría 106 mm.
- La rejilla suele ser un poco más pequeña que el área. El área solo se usa para contar. No se dibuja.
- El resto del área queda vacío en el lado alejado del punto. Con **En el centro** se reparte por igual a ambos lados.
- Un área de exactamente 94 mm da 8 columnas; 93.9 mm da 7.

Los campos **Columnas** y **Filas** se muestran solo en el primer modo, **Ancho del área** y **Alto del área** solo en el segundo.

## Elegir la forma

Campo **Forma**.

| Entrada | Qué se obtiene |
| --- | --- |
| **Rectángulo** | Un rectángulo de longitud × profundidad. Sus esquinas se pueden cambiar, ver abajo. |
| **Círculo / elipse** | Una elipse con la longitud y la profundidad como sus dos diámetros. Valores iguales dan un círculo. |
| **Ranura** | Un rectángulo con dos extremos semicirculares. Los extremos están en la dirección más larga: si la longitud es mayor que la profundidad, los extremos izquierdo y derecho son redondos. Valores iguales dan un círculo. |
| **Polígono** | Una forma con 3 a 24 lados rectos. Una esquina apunta siempre hacia arriba. |

### Rectángulo: esquinas

1. Poner **Forma** en **Rectángulo**. Aparece el campo **Esquinas**.
2. Elegir **Vivas**, **Redondeadas** o **Achaflanadas**. (Achaflanadas significa: la esquina se corta con una línea recta.)
3. Con **Redondeadas** y **Achaflanadas** aparece el campo **Radio / chaflán**. Introducir el radio del redondeo, o a qué distancia de la esquina empieza el corte a lo largo de cada lado.

El valor máximo permitido es la mitad del lado más corto. Con exactamente ese valor:

| Rectángulo | Valor | Redondeadas se convierte en | Achaflanadas se convierte en |
| --- | --- | --- | --- |
| 10 × 5 mm | 2.5 mm | una ranura | una forma de seis lados |
| 10 × 10 mm | 5 mm | un círculo | un rombo |

Las esquinas no cambian el número de formas, la distancia entre ellas ni el tamaño total.

### Polígono: lados y Regular

1. Poner **Forma** en **Polígono**. Aparecen los campos **Lados** y **Regular**.
2. Introducir **Lados** (3 a 24).
3. Dejar **Regular** desactivado, o marcarlo.

| **Regular** | Resultado |
| --- | --- |
| desactivado | El polígono se estira para que mida exactamente longitud × profundidad. Sus lados normalmente no son entonces igual de largos. |
| activado | Todos los lados son igual de largos. La menor de longitud y profundidad fija el tamaño. La distancia entre formas sigue el tamaño real del polígono, así que la separación sigue siendo la que se introdujo. |

Ejemplo con 6 lados, longitud 10 mm, profundidad 5 mm, separación 2 mm:

| **Regular** | Tamaño de una forma | Distancia de una forma a la siguiente |
| --- | --- | --- |
| desactivado | 10.00 × 5.00 mm | 12.00 × 7.00 mm |
| activado | 4.33 × 5.00 mm | 6.33 × 7.00 mm |

## Ajustar el tamaño y la separación

- **Longitud (X)** y **Profundidad (Y)**: tamaño de una forma.
- **Separación X** y **Separación Y**: espacio libre entre dos vecinas. Se permite 0; las formas se tocan entonces. No se permiten valores negativos.

## Decidir dónde queda el punto

Campo **El punto está en la rejilla**. Dice dónde acaba el punto en el que se hizo clic dentro de la rejilla terminada. No dice en qué dirección crece la rejilla.

Ejemplo: **Abajo a la izquierda** pone el punto en la esquina inferior izquierda de la rejilla. La rejilla se extiende entonces hacia la derecha y hacia arriba.

Tres de las nueve posiciones, con una rejilla de 3 × 2 formas (`X` es el punto, `#` las formas):

```
  En el centro         Abajo a la izquierda Arriba al centro
  #####.#####.#####    #####.#####.#####    #####.##X##.#####
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  ........X........    .................    .................
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  #####.#####.#####    X####.#####.#####    #####.#####.#####
```

Las nueve entradas están en [settings.md](settings.md#el-punto-está-en-la-rejilla).

## Alejar la rejilla del punto

Campos **Desfase X** y **Desfase Y**.

1. Elegir primero la posición en **El punto está en la rejilla**.
2. Introducir cuánto debe moverse toda la rejilla. Los valores positivos la mueven a lo largo de los ejes X e Y del boceto. Los valores negativos la mueven en sentido contrario.

Sirve para mantener un margen: el punto se queda en una esquina de la pieza, y la rejilla empieza, por ejemplo, 2 mm más adentro. El desfase no cambia el número de formas ni el tamaño de la rejilla.

## Leer la línea Resultado

**Resultado** no se puede editar. Muestra o bien

- `{columnas} × {filas} = {número} formas, {anchura} × {altura} mm en total`, siempre en milímetros con dos decimales, o bien
- un mensaje que dice qué valor no está permitido.

## Dibujar otra rejilla

- El cuadro de diálogo se abre con los valores de la última rejilla terminada con **OK**. Ver [settings.md](settings.md#qué-se-recuerda).
- El comando está marcado como repetible, así que la función propia de Fusion de "repetir el último comando" puede iniciarlo de nuevo.

## Qué se obtiene en el boceto

- Líneas, arcos, círculos y elipses de boceto sencillos. No se crea ninguna operación de patrón de Fusion.
- Las formas no están vinculadas al cuadro de diálogo. Para cambiar la rejilla más tarde, borrar las formas y dibujar una rejilla nueva.
- El complemento no añade por su cuenta cotas ni restricciones entre las formas y el punto.
