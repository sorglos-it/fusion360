# Desarrollo

Dovetail es uno de varios complementos del repositorio <https://github.com/sorglos-it/fusion360>.
Todas las rutas de abajo son relativas a la raíz del repositorio.

## Carpetas

| Ruta | Contenido |
|---|---|
| `apps/desktop-dovetail/Dovetail/` | El complemento exactamente como lo quiere Fusion: `Dovetail.py`, `Dovetail.manifest`, `lang/`, `resources/` |
| `apps/desktop-dovetail/VERSION` | El número de versión, una línea |
| `apps/desktop-dovetail/tests/test_geometry.py` | Las pruebas sin conexión |
| `tools/dovetail/make_icons.py` | Escribe el icono de la barra de herramientas (16, 32, 64 px) en `resources/Dovetail/` |
| `tools/dovetail/make_arrow_icons.py` | Escribe los iconos de los botones de **Desplazar** en `resources/nudge_left`, `nudge_center`, `nudge_right` |
| `tools/dovetail/test_geometry.py` | Reenvío al archivo de pruebas trasladado, para que el comando antiguo siga funcionando |
| `tools/set_version.py` | Fija la versión de un complemento o de todos (compartido por todos los complementos) |
| `tools/release.py` | Empaqueta el ZIP de la versión (compartido por todos los complementos) |
| `docs/dovetail/` | README, CHANGELOG, LICENSE y esta documentación |
| `dist/` | Salida de `tools/release.py`; no está en Git |

Fusion exige que la carpeta, el archivo `.py` y el archivo `.manifest` lleven el mismo nombre. No cambiar el nombre de uno solo.

## Estructura de `Dovetail.py`

| Sección | Partes principales |
|---|---|
| Idioma | `Strings`, `T()`, `detect_language()`, `read_version()`, `display_name()` |
| Geometría | `GeometryError`, `_offset_polyline()`, `_top_half()`, `_check_contour()`, `end_room()`, `max_offset()`, `tooth_directions()`, `build_contours()`, `closed_band()` |
| Dibujo | `_to_world()`, `_draw_closed_polyline()`, `line_length()`, `create_geometry()` |
| Manejadores | `_read_inputs()`, `_selected_lines()`, `_check_lines()`, `_run()`, `ExecuteHandler`, `PreviewHandler`, `ValidateHandler`, `InputChangedHandler`, `CommandCreatedHandler`, `_apply_nudge()`, `_apply_mirror()` |
| Inicio / parada | `_find_panel()`, `run()`, `stop()` |

La sección de geometría es matemática pura. No usa nada de Fusion y puede ejecutarse en cualquier Python 3.

## Ejecutar las pruebas

Requisitos: Python 3, solo la biblioteca estándar. No hace falta Fusion; el archivo de pruebas coloca pequeños sustitutos
de los módulos `adsk` antes de importar el complemento.

```bash
python apps/desktop-dovetail/tests/test_geometry.py
```

El comando antiguo sigue funcionando y da la misma salida y el mismo código de salida:

```bash
python tools/dovetail/test_geometry.py
```

- Cada comprobación imprime `ok` o `FAIL`.
- La última línea es `all tests passed`, o el número de fallos.
- El código de salida es 1 si algo falló.

Qué cubren las secciones:

| Sección | Contenido |
|---|---|
| 1–4 | Las tres formas; puntos del contorno; el contorno desplazado es paralelo y está a la distancia correcta |
| 5 | Alineación: el grupo está centrado en el punto medio de la línea |
| 6 | Desplazamiento, desplazamiento máximo, distancia a los extremos de la línea |
| 7 | Quién paga el juego (las tres entradas de **La línea es**) |
| 8 | Geometría reflejada: ambas piezas idénticas; aceptada y rechazada del mismo modo en los dos sentidos |
| 9 | Los fallos comunican la clave correcta; una unión por línea seleccionada; una línea mala se nombra a sí misma |
| 10 | Cada entrada de lista desplegable y cada clave de texto de ayuda existe en `en.xml` |
| 11 | Archivos de idioma: completos, sin claves desconocidas, marcadores conservados, sin textos vacíos |
| 12 | Catálogo de textos, recurso al inglés, detección del idioma sin Fusion |

Para probar una copia instalada en lugar de la del repositorio, poner la variable de entorno
`DOVETAIL_ADDIN_DIR` en su carpeta. Los dos scripts de iconos leen la misma variable.

No cubierto por el archivo de pruebas:

- Todo lo que necesita Fusion: el cuadro de diálogo, la vista previa, el dibujo, la conversión en geometría de construcción, el deshacer
  tras una ejecución fallida.
- La ejecución con 34 317 contornos aleatorios mencionada en el registro de cambios. Fue una comprobación única; no forma parte de
  `test_geometry.py`.

## Iconos

```bash
python tools/dovetail/make_icons.py
python tools/dovetail/make_arrow_icons.py
```

Ambos escriben archivos PNG solo con la biblioteca estándar. Ejecutarlos solo cuando los iconos deban cambiar.

## Números de versión

Las versiones tienen cuatro partes, `v.x.y.z`: versión, entrega, función, compilación. Ejemplo: `1.1.0.0`.

El número se guarda en dos sitios:

- `apps/desktop-dovetail/VERSION`
- la entrada `"version"` de `Dovetail.manifest` (esto es lo que leen Fusion y el título del cuadro de diálogo)

No editarlos nunca a mano. Usar el script, que escribe los dos:

```bash
python tools/set_version.py dovetail 1.1.0.1    # set one add-in
python tools/set_version.py all 1.0.0.0         # set all add-ins of the repository
python tools/set_version.py --check             # report add-ins whose two numbers differ
```

El script rechaza un número que no tenga cuatro partes. `--check` termina con el código de salida 1 si algún complemento difiere.

## Empaquetar una versión

```bash
python tools/release.py dovetail
```

- Escribe `dist/Dovetail-<version>.zip`.
- El ZIP contiene la carpeta `Dovetail/` exactamente como la quiere Fusion.
- Se dejan fuera: `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compresión: Deflate al nivel más alto, para que cualquier programa de descompresión pueda leerlo.
- Después de escribirlo, el ZIP se vuelve a leer y se comprueba.
- El script se niega a empaquetar si `VERSION` y el manifiesto no coinciden.

`python tools/release.py all` empaqueta todos los complementos del repositorio.

Orden sugerido para una versión:

1. Ejecutar las pruebas.
2. Fijar la versión con `tools/set_version.py`.
3. Añadir la entrada a `docs/dovetail/CHANGELOG.md`.
4. Actualizar esta documentación.
5. Empaquetar con `tools/release.py`.
6. Adjuntar `dist/Dovetail-<version>.zip` a la versión en GitHub.

## Añadir un idioma

1. Copiar `lang/en.xml` y dar a la copia el nombre del código de idioma de dos letras.
2. Poner `language="<code>"` en el elemento raíz y traducir los valores.
3. Conservar todos los marcadores (`{0}`, `{1}`, …).
4. Añadir el código a `SUPPORTED_LANGUAGES` y el nombre de idioma de Fusion correspondiente a `FUSION_LANGUAGE_MAP` en
   `Dovetail.py`.
5. Ejecutar las pruebas. Comprueban en cada archivo que esté completo, que no tenga claves desconocidas, los marcadores y que no haya textos vacíos.

`en.xml` es el archivo de referencia. Todas las claves existen ahí. Una clave que falta en otro archivo recurre a él; una clave que falta
en todos se muestra como la propia clave.

## Decisiones y sus motivos

Tomado de los comentarios del código.

| Decisión | Motivo |
|---|---|
| Los textos están en `lang/<code>.xml`; los errores llevan una clave, no un texto | El motivo de un error sigue siendo independiente del idioma; las pruebas pueden comparar claves |
| La forma y el reparto se guardan como el índice en la lista | El valor guardado no depende del idioma de visualización |
| Los valores de idioma de Fusion se consultan con `getattr` | Un valor que esta versión de Fusion no conoce no puede romper el complemento |
| La versión se lee del manifiesto | El cuadro de diálogo no puede desviarse del manifiesto |
| La versión forma parte del nombre del comando | Fusion usa el nombre del comando como título del cuadro de diálogo, así que ahí es donde se ve una versión mientras el cuadro de diálogo está abierto |
| El desplazamiento no se recuerda | Pertenece a la línea en cuestión, no a los ajustes |
| La línea original se convierte en geometría de construcción en lugar de borrarse | Deja de crear perfiles pero conserva sus cotas y restricciones |
| La vista previa no toca la línea original | La selección no puede quedar invalidada por debajo del cuadro de diálogo abierto |
| Se comprueban todas las líneas antes de dibujar ninguna | Una línea mala al final no puede dejar medio boceto dibujado |
| Un fallo en una de varias líneas se envuelve con su posición | Una línea corta en medio falla mientras las demás irían bien; el mensaje dice cuál |
| Los botones de **Desplazar** usan la línea más corta como límite | Un desplazamiento que se sale de una línea no sirve aunque las demás pudieran admitirlo |
| Con el reflejo, la cantidad, el reparto y el desplazamiento se fijan y quedan atenuados | Cada uno de ellos rompe la simetría de 180 grados; fijarlos es mejor que dejar que fallen en la validación |
| El reflejo necesita una cantidad par | Un diente central tendría que apuntar a ambos lados a la vez |
| La separación mínima lleva 0.01 mm de más | Con exactamente el mínimo, al tramo entre dos cajas no le queda longitud |
| Los dientes guardan tolerancia + 0.01 mm con los extremos de la línea | La caja se abre tanto como la tolerancia; si no, el contorno pasa del extremo y tiene que volver |
| En un contorno se comprueba si hay tramos de longitud cero y si se cruza a sí mismo | El desplazamiento hace el inglete de cada esquina por separado, así que nada más impide que un tramo corto se reduzca a nada o se dé la vuelta |
| Una esquina a inglete más alejada de 12 × el desplazamiento se rechaza | El contorno de acoplamiento se descontrolaría en una esquina afilada |
| Una ejecución fallida pone `executeFailed` | Fusion deshace entonces lo dibujado hasta ese momento |
| El dibujo se ejecuta con `isComputeDeferred` | El boceto recalcula una sola vez, no después de cada línea |
| `set_version.py` escribe VERSION y el manifiesto juntos | El número nunca se edita a mano en dos sitios |
| El ZIP usa Deflate al nivel más alto | Cualquier programa de descompresión puede leerlo |

## Puntos abiertos conocidos

- Cuando OK está atenuado, el cuadro de diálogo no muestra ningún motivo. Los textos existen (`err.*`) pero solo los muestra
  la ventana de mensaje tras una ejecución fallida.
- Las líneas de boceto se leen solo con X e Y y la banda se dibuja en Z = 0 del boceto.
- Los cambios de geometría de 1.1.0.0 están probados solo sin conexión, no dentro de Fusion.

## Licencia

MIT, ver [LICENSE](../LICENSE). Autor: Sorglos Thomas Weirich.
