# Ajustes

El complemento no tiene archivo de ajustes ni página de ajustes. Todo se ajusta en el cuadro de diálogo del comando **Rejilla de boceto**. Los nombres de campo están escritos exactamente como en el cuadro de diálogo en español.

## Campos del cuadro de diálogo

Las longitudes se introducen por defecto en milímetros (los campos se crean con la unidad `mm`). "Sin límite" significa: el propio complemento no comprueba nada más.

| Campo | Significado | Valor por defecto | Valores permitidos |
| --- | --- | --- | --- |
| **Punto** | El punto de boceto alrededor del cual se construye la rejilla. | El punto de boceto seleccionado antes de abrir el cuadro de diálogo; si no, vacío | Exactamente un punto de boceto. Otros objetos no se pueden seleccionar. |
| **Cantidad según** | Cómo se fija el número de formas. | Columnas y filas | **Columnas y filas**, **Relleno de un área** |
| **Forma** | La forma que se repite. | Rectángulo | **Rectángulo**, **Círculo / elipse**, **Ranura**, **Polígono** |
| **Lados** | Número de lados del polígono. | 6 | Número entero, 3 a 24 |
| **Regular** | Casilla. Activada: todos los lados del polígono son igual de largos. Desactivada: el polígono se estira a longitud × profundidad. | desactivada | activada, desactivada |
| **Esquinas** | Qué pasa con las cuatro esquinas del rectángulo. | Vivas | **Vivas**, **Redondeadas**, **Achaflanadas** |
| **Radio / chaflán** | Radio del redondeo, o longitud del corte a lo largo de cada lado. | 1 mm | Mayor que 0, como máximo la mitad de la menor de longitud y profundidad |
| **Longitud (X)** | Tamaño de una forma en X. | 10 mm | Mayor que 0, sin límite superior |
| **Profundidad (Y)** | Tamaño de una forma en Y. | 5 mm | Mayor que 0, sin límite superior |
| **Separación X** | Espacio libre entre vecinas en X. | 2 mm | 0 o mayor, sin límite superior |
| **Separación Y** | Espacio libre entre vecinas en Y. | 2 mm | 0 o mayor, sin límite superior |
| **Columnas** | Número de formas una al lado de otra. | 8 | Número entero, 1 a 2000 |
| **Filas** | Número de formas una encima de otra. | 4 | Número entero, 1 a 2000 |
| **Ancho del área** | Anchura del área que se rellena. | 100 mm | Mayor que 0, y lo bastante grande para una forma |
| **Alto del área** | Altura del área que se rellena. | 40 mm | Mayor que 0, y lo bastante grande para una forma |
| **El punto está en la rejilla** | Dónde está el punto seleccionado dentro de la rejilla terminada. | En el centro | Nueve entradas, ver abajo |
| **Desfase X** | Mueve toda la rejilla en X, además de la posición elegida arriba. | 0 mm | Cualquier valor, también negativo |
| **Desfase Y** | Mueve toda la rejilla en Y. | 0 mm | Cualquier valor, también negativo |
| **Resultado** | Muestra el número de formas y el tamaño total, o un mensaje. | – | Solo lectura |

Un límite más vale para toda la rejilla: columnas × filas no debe ser más de **2000**. Esto vale en los dos modos de recuento.

## Cuándo se muestra un campo

| Campo | Se muestra cuando |
| --- | --- |
| **Lados**, **Regular** | **Forma** es **Polígono** |
| **Esquinas** | **Forma** es **Rectángulo** |
| **Radio / chaflán** | **Forma** es **Rectángulo** y **Esquinas** no es **Vivas** |
| **Columnas**, **Filas** | **Cantidad según** es **Columnas y filas** |
| **Ancho del área**, **Alto del área** | **Cantidad según** es **Relleno de un área** |
| todos los demás campos | siempre |

Un campo oculto conserva su valor. Un valor oculto no se usa ni se comprueba.

## El punto está en la rejilla

| Entrada | El punto está en |
| --- | --- |
| **En el centro** | el centro de la rejilla |
| **Abajo a la izquierda** | la esquina inferior izquierda |
| **Abajo a la derecha** | la esquina inferior derecha |
| **Arriba a la izquierda** | la esquina superior izquierda |
| **Arriba a la derecha** | la esquina superior derecha |
| **Abajo al centro** | el centro del borde inferior |
| **Arriba al centro** | el centro del borde superior |
| **A la izquierda al centro** | el centro del borde izquierdo |
| **A la derecha al centro** | el centro del borde derecho |

"Rejilla" significa aquí el rectángulo más pequeño alrededor de todas las formas. Izquierda y derecha van a lo largo del eje X del boceto, abajo y arriba a lo largo de su eje Y.

## Textos de ayuda en el cuadro de diálogo

Hay tres textos de ayuda (tooltips) asociados a campos:

| Campo | Texto |
| --- | --- |
| **Regular** | "Mantiene el polígono equilátero en lugar de estirarlo a longitud × profundidad. La menor de las dos fija su tamaño y el paso sigue la forma real: la separación indicada se respeta en ambos casos." |
| **Esquinas**, **Radio / chaflán** | "Elimina las cuatro esquinas en ángulo recto del rectángulo, como un redondeo o como un chaflán recto. Como máximo la mitad del lado más corto: ese radio exacto convierte el rectángulo en una ranura, y ese chaflán en un rombo. El rectángulo envolvente no cambia, así que la cantidad, el paso y la separación se mantienen." |
| **Desfase X**, **Desfase Y** | "Desplaza toda la rejilla respecto al punto seleccionado, además de lo que ya determina el punto de referencia. Sirve para mantener un margen con un borde sin mover el punto. Los valores negativos van en sentido contrario." |

Nota sobre el segundo texto: un chaflán de exactamente la mitad del lado más corto da un rombo solo cuando la longitud y la profundidad son iguales. Con valores distintos da una forma de seis lados.

El propio botón tiene el texto de ayuda: "Construye una rejilla de formas alrededor de un punto de boceto. Número fijo de columnas y filas, o tantas como quepan en un área."

## Qué se recuerda

- Al terminar una rejilla con **OK**, el complemento recuerda todos los valores excepto el punto: modo de recuento, forma, lados, Regular, esquinas, radio / chaflán, longitud, profundidad, las dos separaciones, columnas, filas, ancho del área, alto del área, posición del punto, los dos desfases.
- La próxima vez que se abre el cuadro de diálogo, estos valores ya están puestos.
- Los valores **no** se recuerdan cuando se cancela el cuadro de diálogo, o cuando OK termina con un mensaje de error.
- Los valores se guardan solo en memoria, nunca en el disco. Duran hasta que se detiene el complemento o se cierra Fusion. Después vuelven a valer los valores por defecto de la tabla de arriba.
- Los valores son los mismos para todos los documentos abiertos en esta sesión de Fusion.

## Idioma

El complemento tiene cinco idiomas: alemán, inglés, español, francés, italiano.

Cómo se elige el idioma, en este orden:

1. El idioma ajustado en Fusion en **Preferences → General → User Language**, si es uno de los cinco.
2. Si no, el idioma del sistema operativo, si es uno de los cinco. (El complemento lee las variables de entorno `LANG`, `LANGUAGE`, `LC_ALL`, y después la configuración regional del sistema.)
3. Si no, el inglés.

Más detalles:

- No hay ningún selector de idioma en el complemento.
- El idioma se lee una sola vez, cuando se inicia el complemento. Después de cambiar el idioma en Fusion, detener e iniciar el complemento, o reiniciar Fusion.
- Si falta un texto en un idioma, se muestra en su lugar el texto en inglés.
- La línea **Resultado** muestra siempre milímetros, en todos los idiomas.
