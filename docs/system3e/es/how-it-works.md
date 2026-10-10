# Cómo funciona

Volver al [resumen](index.md).

## Los archivos del complemento

La carpeta instalada `System3E` contiene:

| Archivo o carpeta | Finalidad |
| --- | --- |
| `System3E.py` | El comando: cuadro de diálogo, colocación, puntos |
| `system3e_core.py` | Ayudas generales: idioma, botón de la barra de herramientas, mensajes de error, versión |
| `System3E.manifest` | Indica a Fusion el nombre, el autor, la versión y que el complemento se inicia con Fusion |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | Todos los textos, un archivo por idioma |
| `blocks/blocks.json` | La biblioteca de elementos: la forma de los 74 elementos |
| `blocks/<id>.png` | Una imagen de vista previa por elemento, 74 en total |
| `resources/System3E/16x16.png`, `32x32.png`, `64x64.png` | El icono del botón |

El complemento solo lee estos archivos. No escribe ningún archivo y no abre ninguna conexión de red.

## Inicio y parada

Cuando el complemento se inicia:

1. Detecta el idioma (véase [settings.md](settings.md)) y carga los textos.
2. Quita una definición de botón que haya quedado de una ejecución anterior, si la hay.
3. Crea el botón **Elemento SYSTEM 3E**. La versión del manifiesto se añade entre paréntesis.
4. Busca el panel **Create** de las herramientas de sólidos en el espacio de trabajo de diseño y pone allí el botón.
   Si no encuentra el panel, muestra un mensaje y no añade ningún botón.

Cuando el complemento se detiene, vuelve a quitar el botón.

## La biblioteca de elementos

`blocks/blocks.json` es un archivo de texto en formato JSON. Contiene:

- `unit`: siempre `mm`. Todas las longitudes del archivo son milímetros.
- `blocks`: una lista de 74 elementos en el orden del catálogo.

Cada elemento tiene estas entradas:

| Entrada | Contenido | Ejemplo |
| --- | --- | --- |
| `id` | Nombre corto para archivos, en minúsculas | `s1-wp` |
| `name` | Nombre del catálogo | `S1 WP` |
| `family` | Uno de `starter`, `basic`, `complementary`, `lintel`, `window`, `top`, `corner`, `partition` | `basic` |
| `size` | Largo, ancho, alto en mm enteros | `[707, 352, 300]` |
| `stack` | Altura a la que se apoya la hilada siguiente, en mm | `250.0` |
| `points` | Los puntos de esquina de la forma, cada uno como x, y, z en mm | `[0.0, 271.0, 200.0]` |
| `faces` | Las caras planas. Cada una tiene una dirección (`normal`) y uno o varios contornos (`loops`). | – |

Un contorno es una lista de números. Cada número nombra uno de los `points`. El primer contorno de una cara es su borde exterior. Los demás contornos son agujeros en la cara.

Cada elemento está con su esquina más baja en 0, 0, 0. Su largo va a lo largo de x, su ancho (el espesor del muro) a lo largo de y, su alto a lo largo de z.

La biblioteca se lee una sola vez, la primera vez que se abre el cuadro de diálogo. La imagen de vista previa de un elemento es el archivo `blocks/<id>.png`.

## Cómo se construye un cuerpo

Los elementos no están guardados como archivos de Fusion. El complemento construye cada cuerpo a partir de los puntos y las caras:

1. Cada punto del elemento pasa a ser una esquina del cuerpo.
2. Cada cara pasa a ser una cara plana. Su posición sale de su primer punto y de su dirección.
3. Cada contorno pasa a ser una cadena cerrada de aristas rectas.
4. Cada arista se define una vez y la usan sus dos caras vecinas, en sentidos opuestos. Esto hace que el cuerpo sea cerrado (un sólido).
5. Fusion comprueba el resultado por completo y crea el cuerpo. Si Fusion lo rechaza, el complemento muestra el mensaje "No se pudo crear el elemento {0}:" con el motivo que da Fusion.

Todas las caras son planas y todas las aristas son rectas. No hay superficies curvas.

## Componentes y reutilización

Al pulsar **OK**:

1. El complemento busca en el diseño un componente de este elemento.
   - Busca una marca invisible (un atributo de Fusion, grupo `System3E`, nombre `block`) con el `id` del elemento.
   - Los elementos colocados antes de que existiera la marca se encuentran por el nombre `SYSTEM 3E <name>`.
   - Los componentes sin cuerpo y los componentes de un diseño vinculado se saltan.
2. **Encontrado:** el complemento añade los que falten de los doce puntos e inserta otra copia de ese componente en el lugar nuevo.
3. **No encontrado:** el complemento construye el cuerpo, crea un componente nuevo llamado `SYSTEM 3E <name>` en el nivel superior del diseño, lo marca, pone dentro el cuerpo llamado `<name>` y añade los doce puntos.

Como los elementos iguales son copias de un solo componente, una lista de piezas los cuenta juntos.

En un diseño con línea de tiempo (Fusion lo llama diseño paramétrico), un cuerpo ya hecho tiene que llegar dentro de una "base feature". El complemento crea una, pone dentro el cuerpo y los puntos y la cierra. En un diseño sin línea de tiempo, el cuerpo y los puntos se añaden directamente.

Si algo falla mientras se crea un elemento, el complemento avisa a Fusion de que el comando ha fallado. Fusion deshace entonces lo que se había construido hasta ese momento.

## Los puntos de construcción

Cada componente recibe doce puntos de construcción. Con L = largo, W = ancho y S = `stack` del elemento, están en estos lugares en las coordenadas propias del elemento (mm):

| Nombre | x | y | z |
| --- | --- | --- | --- |
| abajo delante | 0 | W/2 | 0 |
| abajo centro | L/2 | W/2 | 0 |
| abajo detrás | L | W/2 | 0 |
| arriba delante | 0 | W/2 | S |
| arriba centro | L/2 | W/2 | S |
| arriba detrás | L | W/2 | S |
| arriba centro derecha | L/2 | 0 | S |
| arriba centro izquierda | L/2 | W | S |
| abajo centro derecha | L/2 | 0 | 0 |
| abajo centro izquierda | L/2 | W | 0 |
| centro derecha, 50 mm arriba | L/2 | 0 | 50 |
| centro izquierda, 50 mm arriba | L/2 | W | 50 |

Las tres esquinas que se ofrecen en **Colocar por** no son puntos de construcción. Con H = alto, están en:

| Entrada | x | y | z |
| --- | --- | --- | --- |
| Esquina inferior delantera derecha | 0 | 0 | 0 |
| Esquina superior delantera derecha | 0 | 0 | H |
| Esquina superior delantera izquierda | 0 | W | H |

Cada punto lleva una marca invisible (grupo de atributos `System3E`, nombre `point`) con su clave. Por esta marca el complemento sabe qué puntos tiene ya un componente y añade solo los que faltan.

El punto pertenece al componente. Por eso cada copia de un elemento muestra los mismos doce puntos en su propio lugar.

## Cómo se calcula el lugar

1. El lugar elegido en **Colocar por** se mueve al origen.
2. El elemento se gira alrededor del eje Z según **Giro**.
3. El elemento se mueve al punto en el que se hizo clic más **Desplazamiento X**, **Desplazamiento Y**, **Desplazamiento Z**.
   Si no se hizo clic en ningún punto, se usa el origen (0, 0, 0).

Los desplazamientos se aplican después del giro. Por eso van a lo largo de los ejes del diseño, no a lo largo del elemento girado.

La posición de un punto de boceto en el que se hizo clic se toma en las coordenadas de todo el diseño, no en las de su boceto.

## Unidades

| Dónde | Unidad |
| --- | --- |
| Biblioteca de elementos `blocks.json` | mm |
| Campos **Desplazamiento X**, **Desplazamiento Y**, **Desplazamiento Z** | se muestran en mm |
| Campo **Giro** | se muestra en grados |
| Dentro de la interfaz de programación de Fusion | cm y radianes |

El complemento divide entre 10 cada valor de la biblioteca cuando se lo pasa a Fusion. No hay que convertir nada.

## La vista previa

Mientras el cuadro de diálogo está abierto, Fusion pide al complemento una vista previa después de cada cambio. El complemento ejecuta entonces los mismos pasos que para **OK**. Fusion descarta esta vista previa y ejecuta los pasos otra vez al pulsar **OK**.
Los errores durante la vista previa no se muestran.
