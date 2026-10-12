# System3E – documentación

System3E es un complemento para Autodesk Fusion 360. Coloca en un diseño elementos de muro del sistema de
construcción de apilado en seco SYSTEM 3E. Se hace clic en un punto, se elige uno de los 74 elementos de una lista
y el elemento se crea allí como cuerpo sólido.

Esta documentación describe la versión 1.2.0.0.

## Contenido

| Archivo | Qué se encuentra allí |
| --- | --- |
| [installation.md](installation.md) | Requisitos, instalación, primer inicio, actualización, eliminación |
| [usage.md](usage.md) | Colocar elementos paso a paso, construir un muro a matajunta, lista de piezas |
| [settings.md](settings.md) | Cada campo del cuadro de diálogo, valores por defecto, qué se recuerda, idioma |
| [how-it-works.md](how-it-works.md) | Archivos, biblioteca de elementos, cómo se construye un cuerpo, puntos, unidades |
| [troubleshooting.md](troubleshooting.md) | Cada mensaje, su causa y qué hacer; límites conocidos |
| [development.md](development.md) | Carpetas, pruebas, reconstruir la biblioteca, versiones, publicación |

Otros archivos: [registro de cambios](../CHANGELOG.md), [licencia](../LICENSE),
[dibujo de los puntos](../s1-wp-punkte.svg).

## Qué hace el complemento

- Añade a Fusion un botón, **Elemento SYSTEM 3E**.
- El botón abre un cuadro de diálogo con ocho campos y una imagen de vista previa.
- El elemento se crea como un componente con un cuerpo sólido.
- Cada elemento lleva doce puntos propios. Se puede hacer clic en ellos para colocar el elemento siguiente.
- El mismo elemento colocado otra vez es otra copia del mismo componente. Una lista de piezas cuenta juntos los
  elementos iguales.

## Qué está probado y qué no

| Parte | Estado |
| --- | --- |
| Colocar elementos | Usado dentro de Fusion por el autor |
| Los doce puntos para hacer clic | Usado dentro de Fusion por el autor |
| Puntos mostrados sobre la superficie y corregidos después de crear un elemento (desde la 1.1.0.1) | Usado dentro de Fusion por el autor |
| Las opciones de **Colocar por** | Usado dentro de Fusion por el autor |
| **Desplazamiento X**, **Desplazamiento Y**, **Desplazamiento Z** | Usado dentro de Fusion por el autor |
| Correcciones de la versión 1.0.0.1 (véase el [registro de cambios](../CHANGELOG.md)) | Aún no confirmadas dentro de Fusion |
| Nombres izquierda/derecha de los elementos de esquina y de ventana | Comparados a ojo con las fichas del catálogo del fabricante, **no confirmados** |
| Elemento `S0/2 200 P` | Dañado en el archivo 3D del fabricante, reconstruido a partir de `S0/2 250 P` |

## Aspectos legales

- El complemento **no está afiliado a SYSTEM 3E**.
- Licencia: MIT. Véase [LICENSE](../LICENSE).
- Autor: Sorglos Thomas Weirich.
