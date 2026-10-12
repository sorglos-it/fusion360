# Desarrollo

Volver al [resumen](index.md).

Todos los comandos se ejecutan desde la raíz del repositorio <https://github.com/sorglos-it/fusion360>.

## Carpetas

| Ruta | Contenido |
| --- | --- |
| `apps/desktop-system3e/System3E/` | El complemento tal como lo carga Fusion (esta carpeta va dentro del ZIP de la publicación) |
| `apps/desktop-system3e/System3E/System3E.py` | Comando, cuadro de diálogo, colocación, puntos |
| `apps/desktop-system3e/System3E/system3e_core.py` | Mecanismos compartidos: catálogo de textos, detección del idioma, búsqueda del panel, registro de manejadores, tipo de error, versión |
| `apps/desktop-system3e/System3E/System3E.manifest` | Manifiesto de Fusion: id, autor, descripciones, versión, `runOnStartup`, `supportedOS` |
| `apps/desktop-system3e/System3E/lang/` | `de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml`; `en.xml` es la referencia |
| `apps/desktop-system3e/System3E/blocks/` | `blocks.json` y 74 imágenes de vista previa `<id>.png` (generadas) |
| `apps/desktop-system3e/System3E/resources/System3E/` | Icono del botón en 16, 32 y 64 px |
| `apps/desktop-system3e/VERSION` | El número de versión, una línea |
| `apps/desktop-system3e/tests/` | `test_addin.py`, `test_blocks.py` |
| `tools/system3e/` | `build_library.py`, `mesh_to_solid.py`, `points_sheet.py`, `make_icon.py` |
| `tools/set_version.py`, `tools/release.py` | Herramientas de versión y de publicación para todos los complementos del repositorio |
| `docs/system3e/` | README, registro de cambios, licencia, el dibujo de los puntos, esta documentación |
| `assets/system3e/` | El archivo 3D del fabricante. **No está en el repositorio**, se guarda en local. |
| `dist/` | Archivos ZIP de publicación. No están en Git. |

`System3E.py` tiene dos zonas marcadas. El código propio del complemento está entre `CONFIGURE` y `END OF TEMPLATE`;
los manejadores de eventos y `run`/`stop`, que están debajo, son el armazón. El complemento se generó a partir de
la plantilla de complementos del repositorio.

## Pruebas

Las dos pruebas funcionan sin Fusion. Ponen sustitutos de los módulos `adsk` en `sys.modules` e importan el
complemento. Solo biblioteca estándar.

```bash
python apps/desktop-system3e/tests/test_addin.py
```

```bash
python apps/desktop-system3e/tests/test_blocks.py
```

El código de salida 1 significa que ha fallado al menos una comprobación.

`test_addin.py` comprueba:

| Sección | Comprobaciones |
| --- | --- |
| 1) Layout | La carpeta, `System3E.py`, `System3E.manifest` y `lang/` existen y coinciden con el nombre de la carpeta |
| 2) Manifest | JSON válido, `type` es `addin`, `autodeskProduct` es `Fusion360`, el id tiene aspecto de GUID |
| 3) Import | El complemento se importa, `run` y `stop` existen, `CMD_ID` está definido, el archivo del módulo central existe |
| 4) Language files | Cada archivo de idioma existe, declara su idioma, tiene todas las claves de `en.xml` y ninguna clave desconocida, conserva cada marcador de posición `{0}`, no tiene ningún texto vacío |
| 5) Text catalogue | Cada idioma se carga, un idioma desconocido recurre al inglés, una clave que falta devuelve la clave |
| 6) Icons | Los tres archivos de icono existen y son archivos PNG de verdad |

Opciones: `--addin <name>` y `--path <folder>` dirigen la prueba a otra carpeta de complemento.

`test_blocks.py` comprueba:

| Sección | Comprobaciones |
| --- | --- |
| 1) Library file | La unidad es `mm`, 74 elementos, ids y nombres únicos, ids que sirven como nombres de archivo |
| 2) Solids | Cada elemento es un sólido cerrado con caras planas, los contornos van en el sentido correcto, el volumen es posible, la esquina está en el origen, el tamaño y los puntos concuerdan, el tamaño corresponde al nombre del catálogo, no hay dos elementos con la misma forma |
| 3) Pictures | Cada elemento tiene un PNG, no sobran imágenes |
| 4) Add-in | El complemento lee todos los elementos; cada familia, cada ancla y cada nombre de punto tiene un texto en los cinco idiomas; el elemento por defecto y el ancla por defecto existen |
| 5) Points for clicking | La altura de apilado de `S1 WP` es 250 y la de `EU 200 W` es 200; posiciones de las anclas; doce puntos con nombre por elemento, todos en lugares distintos y sobre el elemento; cada punto se muestra sobre la superficie sin que haya dos en un mismo lugar; los elementos de cualquier antigüedad acaban con los doce puntos; un elemento lejos del origen recibe sus puntos sobre el elemento; `make_body()` convierte cada punto en un vértice, define cada cara, usa cada arista una vez en cada sentido y convierte mm a cm |

Lo que las pruebas no pueden decir: si Fusion acepta un cuerpo, crea los puntos de construcción o coloca la
ocurrencia correctamente. Eso solo se sabe dentro de Fusion.

Estado de las pruebas dentro de Fusion: la colocación de elementos, los doce puntos, **Colocar por** y los
desplazamientos X/Y/Z han sido usados por el autor. Las correcciones de la 1.0.0.1 aún no están confirmadas dentro
de Fusion.

## Reconstruir la biblioteca de elementos

`blocks/blocks.json` y las imágenes se generan. No hay que editarlos a mano.

Origen: el archivo 3D del fabricante `assets/system3e/SYSTEM 3E START.3ds`. **No forma parte del repositorio**.
Sin él no se puede reconstruir la biblioteca; el script se detiene con "Source file missing".

```bash
python tools/system3e/build_library.py
```

```bash
python tools/system3e/build_library.py --no-pictures
```

Las imágenes necesitan el paquete de Python Pillow. `--no-pictures` las omite. El complemento en sí no necesita
ninguna de las dos cosas.

Qué hace la generación:

1. `mesh_to_solid.read_3ds()` lee cada malla de triángulos del archivo y la convierte a mm.
2. `mesh_to_solid.solid_from_mesh()` suelda los puntos que están a menos de 0,3 mm, ordena los triángulos en
   planos, une todos los triángulos de un plano en contornos (con agujeros), descarta los puntos que están en medio
   de aristas rectas y comprueba que cada arista se usa una vez en cada sentido. La esquina más baja de la caja
   envolvente pasa a ser el origen.
3. La tabla `NAMES` da a cada número de malla su nombre del catálogo. El archivo 3D no lleva nombres.
4. Los cuatro elementos de tabique se añaden como cajas lisas con los tamaños de la tabla `PARTITION`.
5. `S0/2 200 P` se reconstruye (véase más abajo).
6. `straighten()` da a los puntos que deben compartir una coordenada exactamente el mismo valor, con precisión de
   0,1 mm.
7. `bend()` vuelve a calcular la normal de cada cara a partir de su contorno. `stack_level()` halla la altura de
   apilado.
8. `blocks.json` se escribe en el orden de la tabla `FAMILIES`, y se dibuja una imagen por elemento.

La generación se detiene si un elemento no es un sólido cerrado, si dos elementos comparten un id o si falla la
comprobación de la reconstrucción.

Para inspeccionar solo el archivo de origen:

```bash
python tools/system3e/mesh_to_solid.py "assets/system3e/SYSTEM 3E START.3ds" --report
```

Imprime una línea por malla con el tamaño, el número de puntos y de caras, el volumen y el estado.

### Otras herramientas

| Herramienta | Finalidad |
| --- | --- |
| `python tools/system3e/points_sheet.py "S1 WP" docs/system3e/s1-wp-punkte.svg` | Dibuja un elemento con todos sus puntos como SVG. Los puntos se toman del propio complemento. Los rótulos están en alemán. |
| `python tools/system3e/make_icon.py` | Genera los PNG del icono del botón en 16, 32 y 64 px |

## Números de versión

Una versión tiene cuatro partes, `v.x.y.z`: versión, publicación, función, compilación. Ejemplo: `1.3.0.0`.

El número se guarda en dos lugares: `apps/desktop-system3e/VERSION` y la entrada `version` del manifiesto. Fusion
y el título del cuadro de diálogo leen el manifiesto. Nunca hay que editar los dos a mano; se usa la herramienta:

```bash
python tools/set_version.py system3e 1.1.0.1
```

```bash
python tools/set_version.py --check
```

`--check` enumera todos los complementos del repositorio e informa de aquellos cuyos dos números difieren o no son
`v.x.y.z`. `all` en lugar de `system3e` ajusta todos los complementos.

Hay que anotar cada versión en `docs/system3e/CHANGELOG.md`.

## Empaquetar una publicación

```bash
python tools/release.py system3e
```

- Escribe `dist/System3E-<version>.zip`.
- El ZIP contiene la carpeta `System3E` exactamente como la quiere Fusion.
- `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db` y `.DS_Store` se dejan fuera.
- La compresión es Deflate al nivel más alto, para que cualquier descompresor pueda leerlo.
- Después de escribirlo, el ZIP se vuelve a leer y se prueba.
- La herramienta se niega a empaquetar cuando `VERSION` y el manifiesto no coinciden.

Después, el ZIP se adjunta a una publicación en <https://github.com/sorglos-it/fusion360/releases>. Esta subida no
forma parte de la herramienta.

Antes de una publicación: ejecutar las dos pruebas, ejecutar `set_version.py --check`, actualizar el registro de
cambios y esta documentación.

## Añadir o cambiar textos

- `lang/en.xml` es la referencia. Todos los demás archivos de idioma deben tener las mismas claves y los mismos
  marcadores de posición.
- Una clave que falta en un idioma se sirve del inglés en tiempo de ejecución, pero `test_addin.py` la notifica
  como fallo.
- Los nombres de los campos del cuadro de diálogo, de las familias (`family.<id>`), de las anclas (`anchor.<id>`)
  y de los puntos (`point.<...>`) salen todos de estos archivos.
- Para admitir un idioma más, hay que añadirlo a `SUPPORTED_LANGUAGES` y a `FUSION_LANGUAGE_MAP` en
  `system3e_core.py` y añadir el archivo de idioma.

## Decisiones y sus motivos

Están tomadas de los comentarios del código.

| Decisión | Motivo |
| --- | --- |
| El módulo central se quita de `sys.modules` antes de importarlo. | Fusion guarda en caché los módulos importados. Sin esto, una ayuda editada conservaría su versión antigua hasta que Fusion se reinicie. |
| El módulo central tiene su propio nombre, `system3e_core`. | De lo contrario, dos complementos hechos con la misma plantilla sobrescribirían cada uno el módulo central del otro. |
| El id del comando tiene un prefijo propio (`thwSystem3ECmd`). | Un id usado dos veces se apodera en silencio del botón del otro complemento. |
| Una definición de comando obsoleta se borra al inicio. | Una definición dejada por una ejecución anterior conservaría su rótulo antiguo y su manejador antiguo. |
| El panel se busca a partir de una lista de ids. | Los ids de los paneles cambian entre versiones de Fusion. |
| Todos los manejadores de eventos se guardan en un registro. | Fusion solo mantiene una referencia débil. Un manejador que no está guardado en el lado de Python se elimina y su evento deja de dispararse en silencio. |
| Los manejadores se conectan antes de pasar el punto preseleccionado. | Falle lo que falle después, el cuadro de diálogo tiene que seguir funcionando. |
| La selección hecha antes de pulsar el botón se lee antes de que existan los campos de entrada. | Para que hacer clic en un punto y después en el botón funcione sin más. |
| Todos los valores del cuadro de diálogo se leen en una sola función. | Así la ejecución, la vista previa y la validación miran exactamente los mismos valores. |
| La vista previa calla ante los errores. | Se dispara con cada pulsación de tecla, también con valores a medio escribir. En su lugar, la validación atenúa en gris **OK**. |
| La vista previa pone `isValidResult` en falso. | Fusion ejecuta entonces otra vez la ejecución real para el resultado final. |
| Los errores esperados son un tipo de error propio con una clave independiente del idioma. | La validación puede decidir sin analizar texto. Los errores inesperados se muestran con su traceback. |
| Una ejecución fallida activa `executeFailed`. | Fusion deshace entonces lo construido hasta ese momento, en lugar de dejar atrás un componente vacío. |
| El mismo elemento otra vez es otra ocurrencia del mismo componente. | De lo contrario, una lista de piezas muestra "S1 WP", "S1 WP (1)", "S1 WP (2)" como tres piezas en lugar de una pieza tres veces. |
| Los componentes se encuentran por un atributo, no por el nombre. | Así cambiar el nombre de un componente no causa daño. Los elementos de antes de que existiera el atributo se encuentran por el nombre. |
| Los componentes de un diseño vinculado se saltan. | No se pueden cambiar desde el diseño actual. |
| El cuerpo y los puntos van dentro de una base feature en los diseños paramétricos. | Con la línea de tiempo activada, un cuerpo ya hecho y un punto en coordenadas simples tienen que vivir en una base feature. |
| El cuerpo recibe su nombre mientras su base feature sigue abierta. | Así consta en el código; la versión 1.0.0.1 trasladó allí la asignación del nombre. |
| A un componente existente solo se le añaden los puntos que faltan. | Los componentes hechos por una versión anterior no tienen ninguno o tienen menos. |
| El desplazamiento se aplica después del giro. | Va a lo largo de X, Y y Z del diseño, no a lo largo del elemento girado. |
| Los campos de desplazamiento muestran mm, el valor está en cm. | cm es la unidad propia de Fusion. |
| La versión se lee del manifiesto, no está escrita de forma fija en el código. | El cuadro de diálogo no puede apartarse del manifiesto, y hay un solo lugar donde subirla. |
| La versión forma parte del nombre del comando. | Fusion usa el nombre del comando como título del cuadro de diálogo; es el único lugar donde se ve una versión mientras el cuadro de diálogo está abierto. |
| Los miembros de la enumeración de idiomas se buscan con `getattr`. | Un valor que esta versión de Fusion no conoce no puede romper el complemento. El inglés es el idioma de reserva. |
| La biblioteca guarda puntos y caras planas, no archivos de Fusion. | El archivo del fabricante contiene mallas de triángulos sueltas (triángulos que se tocan a lo largo de parte de una arista, puntos duplicados, triángulos muy finos). Fusion no puede hacer un cuerpo con eso. |
| `S0/2 200 P` se reconstruye a partir de `S0/2 250 P`, rebajado 50 mm. | Su malla está dañada sin arreglo posible (abierta por un lado). Los elementos de arranque solo se diferencian en la altura del cuerpo liso que hay bajo el perfil superior. `check_lowering()` demuestra el método con una pareja en la que ambas mallas están bien (`S0/2 250 W` y `S0/2 200 W`). |
| Los números de malla se asignan a los nombres mediante una tabla hecha a mano. | El archivo 3D no lleva nombres. La tabla se hizo comparando cada sólido con el dibujo de su ficha del catálogo. El largo distingue los extremos: 704 o 352 mm es "W", 3 mm más es una lengüeta ("P"). |
| Los elementos de tabique son cajas lisas. | No están en el archivo 3D; sus tamaños proceden de las fichas del catálogo. |
| Las coordenadas se enderezan a 0,1 mm. | El origen tiene ruido de coma flotante (106,4 junto a 106,5 mm), que deja las caras ligeramente dobladas. |
| La altura de apilado está 50 mm por debajo de la parte superior en los elementos con perfil. | Sostienen la hilada siguiente sobre el fondo que hay entre los resaltes; los elementos planos la sostienen arriba del todo. |
| Las imágenes de vista previa se dibujan con un búfer de profundidad. | Las superficies ocultas se eliminan píxel a píxel. Un método anterior mostraba las caras en el orden equivocado en 16 imágenes. |
| Las imágenes de vista previa se dibujan a partir de los sólidos. | No están tomadas del catálogo del fabricante. |

## Puntos abiertos

- Los nombres izquierda/derecha de los elementos de esquina y de ventana de la tabla `NAMES` se compararon a ojo
  con las fichas del catálogo. Todavía necesitan que los revise alguien que conozca el sistema.

## Licencia

MIT, Copyright (c) 2026 Sorglos Thomas Weirich. Véase [LICENSE](../LICENSE). El complemento no está afiliado a
SYSTEM 3E.
