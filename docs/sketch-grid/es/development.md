# Desarrollo

SketchGrid es uno de varios complementos del repositorio <https://github.com/sorglos-it/fusion360>. Todas las rutas de abajo parten de la raíz del repositorio.

## Carpetas

| Ruta | Contenido |
| --- | --- |
| `apps/desktop-sketch-grid/SketchGrid/` | El complemento exactamente como lo necesita Fusion: `SketchGrid.py`, `sketchgrid_core.py`, `SketchGrid.manifest`, `lang/`, `resources/SketchGrid/` |
| `apps/desktop-sketch-grid/VERSION` | El número de versión, una línea |
| `apps/desktop-sketch-grid/tests/test_sketchgrid.py` | Las pruebas |
| `tools/sketch-grid/make_icon.py` | Dibuja el icono del botón (16, 32 y 64 píxeles) |
| `tools/sketch-grid/test_sketchgrid.py` | Solo reenvía a las pruebas de arriba, para que el comando antiguo siga funcionando |
| `tools/set_version.py` | Fija el número de versión (compartido por todos los complementos) |
| `tools/release.py` | Empaqueta el ZIP de la versión (compartido por todos los complementos) |
| `docs/sketch-grid/` | README, CHANGELOG, LICENSE y esta documentación |
| `dist/` | Lo crea `tools/release.py`; no está en Git |

La carpeta, el archivo `.py` y el archivo `.manifest` deben compartir el nombre `SketchGrid`. Fusion lo exige.

Todos los scripts necesitan solo un Python 3 normal con su biblioteca estándar. No hay nada que compilar; el complemento funciona tal como está.

## Ejecutar las pruebas

```
python apps/desktop-sketch-grid/tests/test_sketchgrid.py
python apps/desktop-template/tests/test_addin.py --path apps/desktop-sketch-grid/SketchGrid
```

El primer comando funciona sin Fusion. El archivo de pruebas coloca sustitutos vacíos de los módulos `adsk` de Fusion y después importa `SketchGrid.py`. Imprime una línea por comprobación (`ok` o `FAIL`) y termina con `all tests passed` y el código de salida 0, o con el número de fallos y el código de salida 1.

Qué comprueba:

| Sección | Tema |
| --- | --- |
| 1 | El ejemplo estándar: 10 × 5 mm, separación 2 mm, 8 columnas, 4 filas da 94 × 26 mm y 32 celdas |
| 2, 2b | Cada entrada de punto de referencia tiene los factores que promete su nombre (derivados del nombre de la clave, por ejemplo `bottom_left`), y el punto cae donde dice la entrada |
| 3 | Posiciones de las celdas |
| 4 | El modo "Relleno de un área" cuenta solo lo que cabe por completo |
| 5 | Cada rechazo comunica la clave de mensaje correcta |
| 6 | Archivos de idioma: los cinco están completos y conservan sus marcadores |
| 7 | Desfase respecto al punto seleccionado |
| 8 | La separación sigue siendo la separación para todas las formas: caja medida del polígono, estiramiento, tamaño real en el modo de relleno |
| 9 | Esquinas del rectángulo: límites y el contorno de líneas y arcos |
| 10 | Cada entrada de lista desplegable tiene un texto |
| 11 | Catálogo de textos: carga de cada idioma, recurso al inglés, los mensajes siguen el idioma |

El segundo comando es la comprobación de estructura del complemento plantilla del mismo repositorio. Comprueba el manifiesto, el id, el id del comando y los iconos.

Por defecto, las pruebas y el script del icono usan `apps/desktop-sketch-grid/SketchGrid`. Poner la variable de entorno `SKETCHGRID_ADDIN_DIR` para probar otra copia, por ejemplo una instalada.

Lo que las pruebas no cubren: todo lo que necesita Fusion. Es decir, el cuadro de diálogo, la selección, la vista previa y las llamadas de dibujo en sí. Estas partes solo se pueden probar dentro de Fusion.

## Probar un cambio en Fusion

1. Copiar `apps/desktop-sketch-grid/SketchGrid` en la carpeta de complementos de Fusion (ver [installation.md](installation.md)).
2. En Fusion, detener el complemento y ejecutarlo de nuevo.

`SketchGrid.py` quita `sketchgrid_core` de la caché de módulos de Python antes de importarlo. Motivo según el comentario del código: Fusion guarda en caché los módulos importados, así que un módulo auxiliar editado seguiría sirviendo su versión antigua hasta que se reinicie Fusion.

## Números de versión

Cuatro partes: `v.x.y.z` (versión, entrega, función, compilación), por ejemplo `1.1.0.0`.

El número se guarda en dos sitios:

- `apps/desktop-sketch-grid/VERSION`
- la entrada `"version"` de `SketchGrid.manifest` (Fusion y el nombre del botón leen esta)

No editarlos nunca a mano. Usar el script, que escribe los dos:

```
python tools/set_version.py sketch-grid 1.1.0.1
python tools/set_version.py --check
```

- El primer comando fija la versión. Rechaza todo lo que no sean cuatro números separados por puntos.
- `--check` enumera cada complemento con ambos números y dice `ok` o `DIFFERENT OR NOT v.x.y.z`. Código de salida 1 si algún complemento está mal.
- `all` en lugar de `sketch-grid` fija el mismo número para todos los complementos del repositorio.

Añadir una entrada a `docs/sketch-grid/CHANGELOG.md` por cada número nuevo.

## Empaquetar una versión

```
python tools/release.py sketch-grid
```

- Escribe `dist/SketchGrid-<version>.zip`.
- El ZIP contiene la carpeta `SketchGrid` como nivel superior, lista para descomprimirse en la carpeta de complementos de Fusion.
- Se dejan fuera: las carpetas `__pycache__` y los archivos que terminan en `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compresión: Deflate al nivel más alto, "para que cualquier programa de descompresión pueda leerlo" (comentario del script).
- El script se niega a empaquetar cuando `VERSION` y el manifiesto difieren o el número no tiene cuatro partes.
- Después de escribirlo, vuelve a leer el ZIP y se detiene si un archivo de dentro está dañado.
- `all` en lugar de `sketch-grid` empaqueta todos los complementos.

El ZIP se adjunta después a una versión en <https://github.com/sorglos-it/fusion360/releases>. El script no sube nada.

## Volver a dibujar el icono

```
python tools/sketch-grid/make_icon.py
```

Escribe `16x16.png`, `32x32.png` y `64x64.png` en `resources/SketchGrid/`. La imagen es una rejilla de 3 × 3 celdas con una cruz en el centro para el punto seleccionado. El script escribe los archivos PNG por sí mismo, sin biblioteca de imágenes.

## Añadir un idioma

1. Copiar `lang/en.xml` a `lang/<code>.xml` (código de dos letras) y traducir los textos. Conservar las claves y los marcadores `{0}`, `{1}`.
2. En `sketchgrid_core.py`, añadir el código a `SUPPORTED_LANGUAGES`, y el nombre de idioma de Fusion correspondiente a `FUSION_LANGUAGE_MAP`.
3. Ejecutar las pruebas. Comprueban cada idioma de `SUPPORTED_LANGUAGES`.

## Decisiones y sus motivos

Tomado de los comentarios del código.

| Decisión | Motivo indicado |
| --- | --- |
| El cálculo de la rejilla (`grid_layout`, `cell_centres`, `corner_outline`) no usa llamadas a Fusion. | Es la parte que merece la pena probar, y así las pruebas pueden ejecutarse sin iniciar Fusion. |
| Las opciones de las listas desplegables se guardan como su posición en la lista, no como texto. | El valor guardado no se mueve cuando cambia el idioma de la interfaz. |
| Como máximo 2000 formas (`MAX_SHAPES`). | Una cantidad desbocada en el modo de relleno bloquea Fusion durante minutos. Mejor rechazar. |
| Un radio / chaflán por encima de la mitad del lado más corto se rechaza, no se reduce. | Con exactamente la mitad, los dos cortes de un lado se encuentran; más allá se cruzarían. Solo se absorbe el ruido de redondeo. |
| Las esquinas no intervienen en la distribución. | El rectángulo envolvente sigue siendo longitud × profundidad, así que el paso, la cantidad y la separación se quedan como estaban. |
| Un polígono regular comunica su propio tamaño medido y el paso lo sigue. | No puede llenar una celda de otras proporciones; si no, la separación que se pide no es la separación que se obtiene. |
| La caja del polígono se mide, no se supone. | Un polígono tiene una esquina en cada extremo solo con números de lados adecuados; un pentágono queda bajo dentro de su propia caja. |
| Un cuadrado totalmente redondeado se dibuja como un círculo. | Un círculo no es una cadena de segmentos. |
| En una elipse, el punto del eje principal se pone sobre el eje más largo. | Si no, Fusion rechaza la elipse. |
| `isComputeDeferred` se activa mientras se dibuja y se restablece en un bloque `finally`. | Mantiene quieto el solucionador hasta que todas las formas están dibujadas; con unos cientos de celdas es la diferencia entre instantáneo e inutilizable. |
| El manejador de la vista previa se traga todos los errores. | Se dispara con cada pulsación de tecla, también con valores a medio escribir. Comunicar es tarea de la validación de entradas. |
| Los manejadores de eventos se registran antes de tomar el punto preseleccionado, y tomarlo puede fallar en silencio. | Falle lo que falle después, el cuadro de diálogo debe seguir funcionando; el usuario selecciona entonces el punto en el cuadro de diálogo. |
| Todos los manejadores de eventos se guardan en un registro (`HandlerRegistry`). | Fusion solo mantiene una referencia débil a un manejador. Sin una referencia en el lado de Python, el evento deja de dispararse en silencio. |
| Se prueban varios ids de panel por orden. | Los ids de panel cambian entre versiones de Fusion. |
| Los valores de idioma de Fusion se consultan por nombre con un recurso. | Un valor que esta versión de Fusion no conoce no puede romper el complemento; pasa al inglés en lugar de fallar. |
| Una clave que falta en una traducción se sirve desde el inglés. | Una traducción a medio hacer pasa al inglés en lugar de mostrar claves en bruto. |
| Los problemas esperados se lanzan como `AddInError` con una clave de mensaje. | La clave es independiente del idioma; lo que el usuario puede arreglar debe bloquear OK en lugar de abrir una ventana. |
| La versión se lee del manifiesto, no se escribe en el código. | El cuadro de diálogo no puede desviarse del manifiesto, y solo hay un sitio que cambiar. |
| La versión forma parte del nombre del comando. | Fusion usa el nombre del comando como título del cuadro de diálogo, así que ahí es donde se ve la versión; solo existe ese único nombre. |
| Los últimos valores se guardan en memoria en centímetros. | Los centímetros son la unidad interna de Fusion, sea cual sea la unidad de visualización. |

## Puntos abiertos

- La versión 1.1.0.0 (el punto preseleccionado no se puede tomar) está probada solo sin conexión, no dentro de Fusion.
- Las ranuras y los rectángulos redondeados o achaflanados se dibujan como curvas separadas a partir de coordenadas, sin puntos finales compartidos. Si siguen conectados al arrastrarlos tiene que comprobarse dentro de Fusion.
- El límite de 2000 cuenta formas, no curvas. Si tiene que contar curvas tiene que comprobarse dentro de Fusion.

## Licencia

MIT, ver [LICENSE](../LICENSE). Autor: Sorglos Thomas Weirich.
