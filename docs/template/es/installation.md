# Instalación

## Requisitos

| Qué | Para qué hace falta |
| --- | --- |
| Autodesk Fusion 360 en Windows o macOS | ejecutar el complemento |
| Python 3 en el ordenador | las herramientas de `tools/` (generación, comprobación sin conexión, iconos, versión, empaquetado) |

El complemento en sí no necesita nada más. Solo usa el Python que viene dentro de Fusion.
Las herramientas usan solo la biblioteca estándar de Python. No hay que instalar nada con `pip`.

## Obtener el repositorio

No hay ZIP de publicación para la versión 1.0.0.0. Hay que usar el repositorio.

1. Abrir <https://github.com/sorglos-it/fusion360>.
2. Clonarlo, o descargarlo como ZIP y descomprimirlo.
3. Abrir un terminal en la carpeta del repositorio.

## Crear un complemento nuevo

```bash
python tools/template/new_addin.py MyAddIn --install
```

Esto crea el complemento `MyAddIn` directamente en la carpeta de complementos de Fusion.

### Reglas para el nombre

- Debe empezar por una letra.
- Solo puede contener letras y cifras. Sin espacios, sin guiones, sin guiones bajos.
- No puede ser `AddInTemplate`.

El nombre pasa a ser un nombre de módulo de Python. Por eso las reglas son estrictas.

### Todas las opciones

| Opción | Valor por defecto | Efecto |
| --- | --- | --- |
| `name` (obligatorio) | – | Nombre del complemento, por ejemplo `MyAddIn` |
| `--install` | desactivado | Crearlo directamente en la carpeta de complementos de Fusion |
| `--out DIR` | la carpeta que contiene el repositorio | Crearlo en `DIR` en su lugar. `DIR` se crea si no existe |
| `--author NAME` | `Your Name` | Se escribe en el campo `author` del manifiesto |
| `--prefix STR` | `thw` | Prefijo del id del comando. El id pasa a ser `<prefix><name>Cmd` |
| `--force` | desactivado | Sobrescribir una carpeta existente con ese nombre |
| `-h`, `--help` | – | Mostrar el texto de ayuda |

Notas:

- `--install` y `--out` no se pueden usar juntos.
- Sin `--install` y sin `--out`, el complemento se crea **al lado** de la carpeta del repositorio, no dentro de ella.
- `--force` **borra primero toda la carpeta existente**, incluidos los cambios propios que haya en ella. Después crea una copia nueva.
- Conviene elegir un `--prefix` propio. `thw` es el prefijo del autor de la plantilla.

### Qué hace el script

1. Copia `apps/desktop-template/AddInTemplate` a `<target>/<name>` (sin `__pycache__` ni archivos `.pyc`).
2. Cambia el nombre de `AddInTemplate.py` a `<name>.py` y el de `AddInTemplate.manifest` a `<name>.manifest`.
3. Cambia el nombre de `addin_core.py` a `<name en minúsculas>_core.py`, por ejemplo `myaddin_core.py`.
4. Cambia el nombre de la carpeta de iconos `resources/AddInTemplate` a `resources/<name>`.
5. En el archivo de entrada: ajusta `_CORE_MODULE` y `CMD_ID`, y sustituye cada `AddInTemplate` por el nombre nuevo.
6. En el manifiesto: escribe un GUID nuevo aleatorio en `id` y el nombre del autor en `author`.
7. En cada `lang/*.xml`: pone en `cmd.name` el nombre nuevo y en `cmd.tooltip` el nombre más la línea `TODO: describe what this command does.`

El script **no** cambia la `description` ni la `version` del manifiesto. Hay que editarlas a mano, véase [settings.md](settings.md).

### Qué se obtiene

```
MyAddIn/
  MyAddIn.py            entry file - your code goes here
  myaddin_core.py       core module, renamed for this add-in
  MyAddIn.manifest      what Fusion reads, with a new GUID
  lang/
    en.xml              reference: every key exists here
    de.xml es.xml fr.xml it.xml
  resources/
    MyAddIn/            16x16.png 32x32.png 64x64.png
```

Al final, el script imprime la ruta creada, el archivo de entrada, el módulo central, el id del comando y los pasos siguientes.

## La carpeta de complementos de Fusion

| Sistema | Ruta |
| --- | --- |
| Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
| macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

Si el complemento se creó sin `--install`, hay que copiar toda la carpeta `MyAddIn` a esta carpeta.

La carpeta, el archivo de entrada y el manifiesto deben llevar el mismo nombre: `MyAddIn/MyAddIn.py` y `MyAddIn/MyAddIn.manifest`.

## Primer inicio en Fusion

1. Iniciar Fusion 360.
2. Abrir **Utilities → ADD-INS → Add-Ins** (esta es la ruta que imprime el script).
3. Seleccionar el complemento y pulsar **Run**.
4. Abrir un boceto. El botón está en la pestaña **SKETCH**, en el panel de creación. Si ese panel no existe, va al panel de creación de la pestaña **SOLID**.

El manifiesto tiene `runOnStartup` puesto en `true`.

El botón y el título del cuadro de diálogo muestran el nombre del comando con la versión entre paréntesis, por ejemplo `Plantilla de complemento (1.0.0.0)`.

Estos pasos siguen el código y la salida del script. No se probaron en Fusion para esta documentación.

### Probar la propia plantilla

También se puede ejecutar la plantilla sin cambios: copiar la carpeta `apps/desktop-template/AddInTemplate` a la carpeta de complementos de Fusion e iniciarla como se indica arriba. Su comando se llama `Plantilla de complemento`.

## Actualización

No hay función de actualización.

- Un complemento creado a partir de la plantilla tiene su propia copia de todos los archivos. Los cambios hechos más tarde en la plantilla no le llegan.
- Para incorporar una corrección, hay que copiar el cambio a mano en el `<name>_core.py` propio o en el archivo de entrada propio.
- Ejecutar el script otra vez con `--force` no es una actualización. Borra la carpeta del complemento y crea una copia nueva y vacía.

## Eliminación

1. En Fusion, abrir **Utilities → ADD-INS → Add-Ins**, seleccionar el complemento y detenerlo. Al detenerse, el complemento quita su botón y su comando de la barra de herramientas.
2. Cerrar Fusion.
3. Borrar la carpeta del complemento de la carpeta de complementos de Fusion.

El complemento no guarda nada fuera de su propia carpeta. Los valores recordados viven solo en la memoria hasta que Fusion se cierra.
