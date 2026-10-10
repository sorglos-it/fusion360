# AddInTemplate

AddInTemplate es el punto de partida para escribir un complemento propio de Autodesk Fusion 360.
Tiene dos partes:

- un **complemento de demostración** (`apps/desktop-template/AddInTemplate`) con un comando, un cuadro de diálogo traducido, una vista previa en vivo y comprobaciones de los datos introducidos
- un **script generador** (`tools/template/new_addin.py`) que copia el complemento de demostración y cambia el nombre de todo lo que debe ser único

| Dato | Valor |
| --- | --- |
| Versión | 1.0.0.0 |
| ZIP de publicación | ninguno para esta versión – se usa desde el repositorio |
| Funciona en | Windows y macOS (manifiesto: `windows\|mac`) |
| Idiomas de la interfaz | alemán, inglés, español, francés, italiano |
| Dependencias | ninguna – solo la biblioteca estándar de Python |
| Licencia | MIT |
| Autor | Sorglos Thomas Weirich |
| Repositorio | <https://github.com/sorglos-it/fusion360> |

## Contenido

| Archivo | Qué se encuentra allí |
| --- | --- |
| [installation.md](installation.md) | Requisitos, obtener el repositorio, crear un complemento nuevo, carpeta de complementos de Fusion, primer inicio, eliminación |
| [usage.md](usage.md) | Qué hace el comando de demostración y cómo convertir la copia en un complemento propio |
| [settings.md](settings.md) | Todo lo que se ajusta en el archivo de entrada, en el manifiesto y en los archivos de idioma |
| [how-it-works.md](how-it-works.md) | Archivo de entrada, módulo central, registro de manejadores, flujo de eventos, catálogo de textos |
| [troubleshooting.md](troubleshooting.md) | Cada mensaje, su causa y qué hacer; trampas conocidas |
| [development.md](development.md) | Carpetas, comprobación sin conexión, herramienta de iconos, números de versión, empaquetado, decisiones |

## Conviene saberlo antes de empezar

- Cada complemento creado a partir de la plantilla recibe su **propia copia** del módulo central. Una corrección hecha más tarde en la plantilla **no** llega a los complementos creados antes.
- La comprobación sin conexión se ejecutó para esta documentación y se superó. El comportamiento dentro de Fusion 360 está descrito a partir del código; **no se probó en Fusion** para esta documentación.

Otros idiomas: [lista de idiomas](../index.md)
