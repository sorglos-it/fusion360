# Desarrollo

## Carpetas

| Ruta | Contenido |
| --- | --- |
| `apps/desktop-template/AddInTemplate/` | El complemento de plantilla, tal como lo necesita Fusion |
| `apps/desktop-template/AddInTemplate/AddInTemplate.py` | Archivo de entrada |
| `apps/desktop-template/AddInTemplate/addin_core.py` | Módulo central |
| `apps/desktop-template/AddInTemplate/AddInTemplate.manifest` | Manifiesto |
| `apps/desktop-template/AddInTemplate/lang/` | `de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` |
| `apps/desktop-template/AddInTemplate/resources/AddInTemplate/` | Iconos `16x16.png`, `32x32.png`, `64x64.png` |
| `apps/desktop-template/VERSION` | Número de versión de esta parte |
| `apps/desktop-template/tests/test_addin.py` | Comprobación sin conexión |
| `tools/template/new_addin.py` | Script generador, véase [installation.md](installation.md) |
| `tools/template/make_icon.py` | Herramienta de iconos |
| `tools/template/test_addin.py` | Reenvía a la comprobación sin conexión (ruta antigua) |
| `tools/set_version.py` | Ajusta los números de versión, para todos los complementos del repositorio |
| `tools/release.py` | Empaqueta un complemento en un ZIP, para todos los complementos del repositorio |
| `docs/template/` | README, CHANGELOG, LICENSE y esta documentación |
| `dist/` | Archivos ZIP empaquetados. No están en Git |

No hay paso de compilación. El complemento funciona tal como está. Todas las herramientas usan solo la biblioteca estándar de Python.

## Comprobación sin conexión

La comprobación prueba un complemento sin iniciar Fusion. El comentario del código dice que es el único ciclo de respuesta que no necesita reinicio.

```bash
python apps/desktop-template/tests/test_addin.py                    # the template itself
python apps/desktop-template/tests/test_addin.py --path ../MyAddIn  # an add-in next to the repository
```

| Opción | Valor por defecto | Efecto |
| --- | --- | --- |
| `--addin NAME` | `AddInTemplate` | Nombre de la carpeta dentro de `apps/desktop-template` de este repositorio |
| `--path DIR` | – | Ruta completa a una carpeta de complemento. Tiene prioridad sobre `--addin` |

Para un complemento creado con `--install`, hay que dar a `--path` su carpeta dentro de la carpeta de complementos de Fusion.

El comando antiguo `python tools/template/test_addin.py` sigue funcionando. Reenvía a la comprobación con los mismos argumentos, la misma salida y el mismo código de salida.

### Cómo funciona

Pone sustitutos vacíos en el lugar de los módulos `adsk`, `adsk.core` y `adsk.fusion` y después importa el complemento.
Solo las clases base de los manejadores son clases reales (vacías). Así, la comprobación demuestra que el archivo se importa y que los textos están en orden. **No** ejecuta ninguna llamada de Fusion: ni cuadro de diálogo, ni geometría, ni `run()`.

### Qué comprueba

| Sección | Comprobaciones |
| --- | --- |
| 1) Layout | La carpeta existe. `<name>.py` y `<name>.manifest` coinciden con el nombre de la carpeta. `lang/` existe |
| 2) Manifest | JSON válido. `type` es `addin`. `autodeskProduct` es `Fusion360`. `id` tiene aspecto de GUID. Avisos: GUID de marcador de posición, autor `Your Name` |
| 3) Import | El complemento se importa. `run` y `stop` existen. `CMD_ID` está definido. `_CORE_MODULE` tiene un archivo que le corresponde. Avisos: `CMD_ID` sigue siendo el valor de la plantilla, módulo central sin cambiar de nombre |
| 4) Language files | `SUPPORTED_LANGUAGES` está disponible. `en.xml` existe y tiene claves. Para cada idioma admitido: el archivo existe, declara el `language` correcto, tiene todas las claves, no tiene ninguna clave desconocida, conserva cada marcador de posición, no tiene ningún texto vacío |
| 5) Text catalogue | Cada idioma se carga y devuelve un `cmd.name`. Un idioma desconocido recurre al inglés. Una clave que falta devuelve la clave. Aviso: la información sobre herramientas sigue diciendo `TODO` |
| 6) Icons | `resources/<name>/` existe. Los tres archivos PNG existen y empiezan por la firma PNG |

### Resultado

- Las líneas empiezan por `ok`, `FAIL` o `warn`.
- Con al menos un `FAIL`, el script termina con el código de salida 1 e imprime el número de fallos.
- Los avisos no cambian el código de salida.
- Sin fallos, imprime `all checks passed`.

Ejecutada para esta documentación sobre la plantilla, versión 1.0.0.0: `3 warning(s)`, `all checks passed`. Los tres avisos (GUID de marcador de posición, autor, id del comando) son normales para la plantilla.

## Herramienta de iconos

Fusion quiere tres archivos PNG con transparencia: 16x16, 32x32 y 64x64 píxeles, en la carpeta que se pasa a la definición del botón.

```bash
python tools/template/make_icon.py                            # the template's placeholder
python tools/template/make_icon.py --root .. --addin MyAddIn  # an add-in next to the repository
```

| Opción | Valor por defecto | Efecto |
| --- | --- | --- |
| `--addin NAME` | `AddInTemplate` | Nombre de la carpeta del complemento |
| `--root DIR` | `apps/desktop-template` de este repositorio | Carpeta que contiene el complemento |

Los archivos se escriben en `<root>/<addin>/resources/<addin>/`. La carpeta se crea si hace falta. Los iconos existentes se sobrescriben.

Para dibujar un icono propio, hay que editar el script:

| Nombre | Significado |
| --- | --- |
| `SHAPES` | Lista de `(colour, polygon)`. Los puntos van de 0 a 1, con y apuntando hacia **arriba**. Donde las formas se solapan, la que figura primero en la lista queda encima |
| `DARK`, `ACCENT` | Los dos colores como valores RGB |
| `SS` | Muestras por lado de píxel para bordes suaves. 4 da bordes limpios hasta 16 px |

El marcador de posición muestra cuatro escuadras en las esquinas y una diagonal. Parece un marcador de posición a propósito. Hay que sustituirlo antes de entregar el complemento a otros.

## Números de versión

Las versiones tienen cuatro partes: `v.x.y.z` (versión, publicación, función, compilación). Actual: `1.0.0.0`.

El número se guarda en dos lugares:

- `apps/desktop-template/VERSION`
- el campo `version` del manifiesto – este es el que leen Fusion y el título del cuadro de diálogo

Nunca hay que editarlos a mano. Se usa la herramienta, que escribe los dos:

```bash
python tools/set_version.py template 1.0.0.1   # this part
python tools/set_version.py all 1.0.0.0        # every add-in of the repository
python tools/set_version.py --check            # report differences
```

- `template` es el nombre de la carpeta `apps/desktop-template` sin `desktop-`.
- `--check` imprime una línea por complemento, termina con `ok` o `DIFFERENT OR NOT v.x.y.z`, y devuelve el código de salida 1 si alguna línea está mal.
- La herramienta solo trabaja con los complementos de este repositorio. En un complemento propio fuera del repositorio, hay que cambiar directamente el campo `version` de su manifiesto: allí es el único lugar.

## Empaquetado

```bash
python tools/release.py template
python tools/release.py all
```

- Escribe `dist/AddInTemplate-<version>.zip`.
- El ZIP contiene la carpeta `AddInTemplate` como la quiere Fusion. Hay que descomprimirlo en la carpeta de complementos de Fusion.
- Se deja fuera: `__pycache__`, `.pyc`, `.pyo`, `Thumbs.db`, `.DS_Store`.
- Compresión: Deflate al nivel más alto, para que cualquier descompresor pueda leerlo.
- Se niega a empaquetar si `VERSION` y el manifiesto difieren o si el número no tiene cuatro partes.
- Después de empaquetar, prueba el ZIP e imprime el número de archivos y el tamaño.
- Las herramientas (`tools/`) no están en el ZIP. Solo existen en el repositorio.

No se ha publicado ningún ZIP de la versión 1.0.0.0. La plantilla se usa desde el repositorio.

## Decisiones y sus motivos

| Decisión | Motivo que da el código |
| --- | --- |
| El archivo de entrada y el módulo central están separados | El módulo central contiene lo que todo complemento necesita y aquello en lo que es fácil equivocarse. El código propio se queda entre dos marcas |
| El módulo central cambia de nombre en cada complemento | Dos complementos hechos con esta plantilla no deben sobrescribir cada uno el módulo central del otro en `sys.modules` |
| El módulo central se quita de `sys.modules` antes de importarlo | Fusion guarda los módulos en caché. De este modo, «detener, ejecutar» recoge los cambios |
| Todos los manejadores pasan por `HandlerRegistry` | Fusion sujeta los manejadores de forma débil. Los que no tienen referencia se eliminan y el evento deja de dispararse en silencio |
| `PANEL_IDS` es una lista, con una búsqueda global como segundo intento | Los ids de los paneles cambian entre versiones de Fusion |
| Una definición de comando obsoleta se borra al inicio | Conservaría su rótulo antiguo y su manejador antiguo |
| `read_inputs()` es el único lugar que lee el cuadro de diálogo | La ejecución, la vista previa y la validación miran exactamente los mismos números |
| `validate()` se ejecuta antes de dibujar y otra vez para el botón OK | Una entrada imposible desactiva OK en lugar de fallar a medio camino |
| La vista previa se traga los errores | Se dispara con cada pulsación de tecla, también con valores a medio escribir |
| La vista previa pone `isValidResult` en `False` | Fusion lanza entonces la ejecución para el resultado real |
| Los errores llevan una clave, no solo un texto | El motivo se conoce sin analizar texto en algún idioma |
| `report()` es solo para errores inesperados | Lo que el usuario puede corregir debe ser un `AddInError`, para que OK quede bloqueado en lugar de que salte un cuadro de diálogo |
| El inglés es la reserva para todos los textos | Una traducción a medio hacer muestra inglés en lugar de claves en bruto |
| Los valores de idioma de Fusion se buscan por el nombre | Un valor que esta versión de Fusion no conoce no puede romper el complemento |
| La detección del idioma nunca lanza un error | Una compilación de Fusion con un valor inesperado sigue iniciando el complemento |
| La versión se lee del manifiesto | El cuadro de diálogo no puede apartarse del manifiesto. Un solo lugar donde subirla |
| La versión forma parte del nombre del comando | Fusion usa ese nombre como título del cuadro de diálogo. Es el único lugar donde se ve una versión mientras el cuadro de diálogo está abierto. También se muestra en el botón: solo existe ese único nombre |
| `isComputeDeferred` se restablece en `finally` | De lo contrario, después de un error el boceto dejaría de actualizarse |
| La selección se lee antes de que existan los campos de entrada | «Hacer clic en una línea y después pulsar el botón» funciona |
| El icono de marcador de posición parece un marcador de posición | Un icono que no se ha sustituido se detecta con facilidad |
| El script escribe los archivos con finales de línea `\n` y en UTF-8 | No se explica en el código |
| Las claves, los identificadores y los comentarios están en inglés | No se explica en el código; el README existente dice que así un traductor nunca tiene que abrir un archivo `.py` |

## Licencia

MIT. Autor: Sorglos Thomas Weirich. Véase [LICENSE](../LICENSE).
