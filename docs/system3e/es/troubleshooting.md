# Solución de problemas

Volver al [resumen](index.md).

## Mensajes

Estos son todos los mensajes que puede mostrar el complemento. Los textos se citan del archivo de idioma español. En otros idiomas el texto está traducido. Los cuadros de mensaje llevan el título "Elemento SYSTEM 3E".

### "Elija un elemento."

| | |
| --- | --- |
| Causa | No hay ninguna entrada seleccionada en **Elemento**. |
| Qué se ve | Normalmente no el mensaje en sí: en su lugar, el botón **OK** aparece atenuado en gris. |
| Qué hacer | Elegir una entrada en **Elemento**. Si la lista está vacía, elegir otra vez la **Familia**. |

### "Abra primero un diseño."

| | |
| --- | --- |
| Causa | El documento activo no es un diseño, así que no hay nada donde colocar el elemento. |
| Qué hacer | Abrir o crear un diseño y cambiar al espacio de trabajo de diseño. Después, iniciar el comando otra vez. |

### "No se pudo crear el elemento {0}:" seguido de un motivo

`{0}` es el nombre del elemento. La segunda línea es el motivo que da Fusion.

| | |
| --- | --- |
| Causa | Fusion se negó a construir el cuerpo a partir de los puntos y las caras del elemento. |
| Qué hacer | 1. Probar con otro elemento para ver si solo está afectado este. 2. Instalar el complemento otra vez desde un ZIP nuevo; el archivo `blocks/blocks.json` puede estar dañado. 3. Si sigue fallando, comunicar el nombre del elemento y el motivo que aparece en el mensaje. |
| Efecto | No queda nada atrás. Fusion deshace el paso. |

### "No se encontró ningún panel de barra de herramientas adecuado."

| | |
| --- | --- |
| Causa | Al iniciarse, el complemento no encontró el panel **Create** de las herramientas de sólidos. No se añadió ningún botón. |
| Qué hacer | Actualizar Fusion e iniciar el complemento otra vez. Si el mensaje sigue apareciendo, comunicar la versión de Fusion. El complemento solo conoce este panel. |

### "Error al crear la geometría:" seguido de texto técnico

| | |
| --- | --- |
| Causa | Un error inesperado después de pulsar **OK**. El texto que hay debajo de la primera línea es un informe técnico (un "traceback") que muestra dónde ocurrió. |
| Qué hacer | 1. Probar otra vez con otro punto o con otro elemento. 2. Detener el complemento y ejecutarlo otra vez. 3. Si sigue igual, copiar todo el texto y comunicarlo. |
| Efecto | Fusion deshace lo que se había construido hasta ese momento. No queda ningún componente a medio hacer. |

### "Error al construir el cuadro de diálogo:" seguido de texto técnico

| | |
| --- | --- |
| Causa | No se pudo construir el cuadro de diálogo. Un motivo que se ve en el código es que falte o no se pueda leer el archivo `blocks/blocks.json`: el cuadro de diálogo lee la biblioteca de elementos al abrirse. |
| Qué hacer | Instalar el complemento otra vez desde el ZIP, para que la carpeta `blocks` esté completa. Véase [installation.md](installation.md). |

### "Error al iniciar:" seguido de texto técnico

| | |
| --- | --- |
| Causa | Un error inesperado mientras el complemento se iniciaba. |
| Qué hacer | 1. Comprobar que la carpeta está descomprimida correctamente: `AddIns/System3E/System3E.py`. 2. Reiniciar Fusion. 3. Instalar el complemento otra vez. 4. Si sigue igual, copiar el texto y comunicarlo. |

### "Error al detener:" seguido de texto técnico

| | |
| --- | --- |
| Causa | Un error inesperado mientras el complemento se detenía y quitaba su botón. |
| Qué hacer | Reiniciar Fusion. Los diseños no se ven afectados. |

## Otros problemas

| Problema | Causa | Qué hacer |
| --- | --- | --- |
| **System3E** no está en la lista de complementos de Fusion. | La carpeta está en el lugar equivocado o un nivel demasiado abajo. | Comprobar que existe `AddIns/System3E/System3E.py`. Véase [installation.md](installation.md). |
| Falta el botón. | El complemento no está en ejecución. | Abrir el cuadro de diálogo de complementos, seleccionar **System3E**, pulsar **Run**. |
| El cuadro de diálogo está en inglés aunque Fusion usa otro idioma. | Solo existen alemán, inglés, español, francés e italiano. Los demás idiomas recurren al inglés. | – |
| El cuadro de diálogo está en el idioma equivocado después de cambiar el idioma de Fusion. | El idioma se elige cuando el complemento se inicia. | Detener el complemento y ejecutarlo otra vez, o reiniciar Fusion. |
| La imagen no cambia al elegir otro elemento. | Falta el archivo de imagen `blocks/<id>.png` de ese elemento. Se queda la imagen anterior. | Instalar el complemento otra vez. |
| No aparece ninguna vista previa del elemento mientras el cuadro de diálogo está abierto. | Ocurrió un error durante la vista previa. Los errores de la vista previa no se muestran. | Pulsar **OK**. Un error real se muestra entonces como mensaje. |
| No se puede hacer clic en un lugar determinado. | Solo se pueden seleccionar puntos de boceto, esquinas de cuerpos y puntos de construcción. Las caras, las aristas y los puntos medios de las aristas no. | Crear allí un punto de boceto o un punto de construcción, o usar los desplazamientos. |
| El elemento está en el origen. | No se seleccionó ningún punto. | Hacer clic en un punto para **Punto**. |
| El elemento está girado hacia el lado equivocado. | Un **Giro** positivo gira en sentido contrario a las agujas del reloj, visto desde arriba. | Escribir el ángulo con el otro signo. |
| Los desplazamientos mueven el elemento en una dirección inesperada. | Los desplazamientos van a lo largo de los ejes del diseño, no a lo largo del elemento girado. | Usar el eje que corresponde a la dirección en el diseño. |
| Los nombres de los puntos están en otro idioma que el cuadro de diálogo. | Los nombres de los puntos se escriben cuando un elemento se coloca por primera vez en un diseño y se conservan. | Cambiar el nombre de los puntos a mano si hace falta. |
| Un elemento más antiguo tiene menos de doce puntos. | Se colocó con una versión anterior. | Colocar el mismo elemento una vez más en ese diseño. Los puntos que faltan se añaden a todas sus copias. |
| El cuadro de diálogo empieza otra vez con los valores por defecto. | Los valores recordados duran solo hasta que Fusion se cierra o el complemento se detiene. | – |
| Una lista de piezas muestra el mismo elemento en varias líneas. | Los elementos se colocaron con la versión 0.2.0, que creaba un componente nuevo cada vez. A partir de ahora solo se reutiliza el primero de ellos. | Sustituir los antiguos por elementos colocados de nuevo. |

## Límites conocidos

- **Sin probar dentro de Fusion:** los doce puntos, las opciones de **Colocar por** y los desplazamientos X/Y/Z están probados solo sin conexión. La colocación de elementos como tal ha sido usada dentro de Fusion por el autor.
- **Sin probar dentro de Fusion:** las correcciones de la versión 1.0.0.1 (véase el [registro de cambios](../CHANGELOG.md)).
- **Izquierda y derecha:** los nombres izquierda/derecha de los elementos de esquina y de ventana se compararon a ojo con las fichas del catálogo del fabricante. No están confirmados.
- **`S0/2 200 P`:** este elemento está dañado en el archivo 3D del fabricante. Se reconstruye a partir de `S0/2 250 P`.
- **Eje vertical:** el complemento trata siempre el eje Z del diseño como «arriba». No tiene en cuenta un ajuste de orientación distinto en Fusion.
- **Solo nivel superior:** los elementos se crean siempre en el nivel superior del diseño (el componente raíz), no en el componente que está activo en ese momento.
- **Diseños vinculados:** un elemento que está dentro de un diseño vinculado no se reutiliza. El complemento crea su propio componente.
- **Sin comprobación de encaje:** el complemento no comprueba si los elementos se solapan, si una junta encaja o si un muro se puede construir.
- **Un elemento por ejecución:** no hay ninguna función para hiladas o muros enteros.
- **Giro:** solo alrededor del eje vertical. Los elementos no se pueden inclinar en el cuadro de diálogo.
- **Cuerpo compartido:** todas las copias de un elemento comparten un solo cuerpo. Cambiar una las cambia todas.
- **Tamaños:** las formas proceden del archivo 3D del fabricante y están redondeadas a 0,1 mm. Los cuatro elementos de tabique son bloques lisos sin perfil.
- **Sin afiliación:** el complemento no está afiliado a SYSTEM 3E. No sustituye a los documentos de planificación del fabricante.
