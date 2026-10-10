# Ajustes

Volver al [resumen](index.md).

El complemento no tiene página de ajustes ni archivo de ajustes. Todo lo que se puede ajustar está en el cuadro de diálogo del comando **Elemento SYSTEM 3E**.

## Los campos del cuadro de diálogo

| Campo | Significado | Valor por defecto | Valores permitidos |
| --- | --- | --- | --- |
| **Punto** | El lugar para el elemento. | Vacío, o el punto que estaba seleccionado antes de pulsar el botón. | Nada o exactamente un punto: un punto de boceto, una esquina de un cuerpo o un punto de construcción. Nada significa el origen del diseño. |
| **Familia** | El grupo de elementos que se muestra en **Elemento**. | Básico | Arranque, Básico, Complementario, Dintel, Marco de ventana, Remate, Esquina, Tabique |
| **Elemento** | El elemento que se va a colocar, con su tamaño en mm (largo x ancho x alto). | S1 WP | Los elementos de la familia elegida. Véanse las listas en [usage.md](usage.md). |
| (imagen) | Muestra el elemento elegido. No se puede cambiar. | Imagen del elemento elegido | – |
| **Colocar por** | Qué lugar del elemento cae sobre el punto. | Esquina inferior delantera derecha | 15 entradas: tres esquinas y los doce puntos. Véase más abajo. |
| **Giro** | Gira el elemento alrededor del eje vertical (Z), en torno al lugar elegido en **Colocar por**. | 0 grados | Cualquier ángulo. Positivo es en sentido contrario a las agujas del reloj, visto desde arriba. |
| **Desplazamiento X** | Mueve el elemento a lo largo del eje X del diseño. | 0 mm | Cualquier longitud, también negativa |
| **Desplazamiento Y** | Mueve el elemento a lo largo del eje Y del diseño. | 0 mm | Cualquier longitud, también negativa |
| **Desplazamiento Z** | Mueve el elemento a lo largo del eje Z del diseño. | 0 mm | Cualquier longitud, también negativa |

El complemento no pone ningún límite superior ni inferior al giro ni a los desplazamientos.

### Las entradas de "Colocar por"

En este orden:

1. Esquina inferior delantera derecha
2. Esquina superior delantera derecha
3. Esquina superior delantera izquierda
4. abajo delante
5. abajo centro
6. abajo detrás
7. arriba delante
8. arriba centro
9. arriba detrás
10. arriba centro derecha
11. arriba centro izquierda
12. abajo centro derecha
13. abajo centro izquierda
14. centro derecha, 50 mm arriba
15. centro izquierda, 50 mm arriba

Lo que significa cada entrada se explica en [usage.md](usage.md).

Estado: **Colocar por** y los tres desplazamientos están probados solo sin conexión, **no dentro de Fusion**.

## Qué se recuerda

Después de pulsar **OK** y de que el elemento se haya creado, el complemento recuerda estos valores para la próxima vez:

- **Familia**
- **Elemento**
- **Colocar por**
- **Giro**
- **Desplazamiento X**, **Desplazamiento Y**, **Desplazamiento Z**

No se recuerda: el **Punto**.

| Pregunta | Respuesta |
| --- | --- |
| ¿Durante cuánto tiempo? | Hasta que se cierra Fusion o se detiene el complemento. Los valores viven solo en la memoria. |
| ¿Se guardan en un archivo? | No. |
| ¿Se guardan en el diseño? | No. |
| ¿Y si se cancela el cuadro de diálogo? | No se recuerda nada. Se quedan los valores de la última colocación que salió bien. |
| ¿Y después de un reinicio? | Vuelven a valer los valores por defecto de la tabla de arriba. |

## Idioma

El complemento tiene sus textos en cinco idiomas: alemán, inglés, español, francés e italiano.

El idioma no se puede elegir en el complemento. Se elige cuando el complemento se inicia:

1. El complemento pregunta a Fusion por el idioma ajustado en las preferencias de Fusion. Si es uno de los cinco, se usa ese.
2. Si no, mira los ajustes de idioma del sistema operativo (las variables de entorno `LANG`, `LANGUAGE`, `LC_ALL`, y después la configuración regional del sistema).
3. Si nada de esto da uno de los cinco idiomas, se usa el inglés.

Más detalles:

- Para cambiar el idioma, hay que cambiar el idioma en las preferencias de Fusion e iniciar el complemento otra vez.
- Si falta un texto en un idioma, se muestra en su lugar el texto en inglés.
- Los nombres de los elementos (`S1 WP`) y de los componentes (`SYSTEM 3E S1 WP`) no se traducen.
- Los nombres de los doce puntos se escriben en el diseño cuando un elemento se coloca por primera vez. Conservan ese idioma, aunque el complemento funcione después en otro idioma.

## Valores fijos que no se pueden cambiar en el cuadro de diálogo

| Valor | Ajuste |
| --- | --- |
| Lugar del botón | Espacio de trabajo de diseño, panel **Create** de las herramientas de sólidos |
| Inicio con Fusion | Sí (`runOnStartup` en el archivo de manifiesto) |
| Puntos 50 mm por encima de la cara inferior | Fijo en 50 mm |
