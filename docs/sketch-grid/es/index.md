# SketchGrid

SketchGrid es un complemento (add-in) para Autodesk Fusion 360. Se hace clic en un punto de un boceto y se obtiene una rejilla de formas iguales a su alrededor: rectángulos, círculos o elipses, ranuras o polígonos.

Esta documentación describe la versión 1.1.0.0.

## Contenido

| Archivo | Qué contiene |
| --- | --- |
| [installation.md](installation.md) | Requisitos, instalación, primer inicio, actualización, desinstalación |
| [usage.md](usage.md) | Todas las funciones, paso a paso |
| [settings.md](settings.md) | Todos los campos del cuadro de diálogo con valor por defecto y límites, qué se recuerda, idioma |
| [how-it-works.md](how-it-works.md) | Archivos, cómo se calcula la rejilla, cómo se dibujan las formas |
| [troubleshooting.md](troubleshooting.md) | Todos los mensajes, su causa y qué hacer; límites conocidos |
| [development.md](development.md) | Carpetas, pruebas, números de versión, empaquetar una versión |

## Qué hace, en resumen

- Dos maneras de fijar el número de formas: **Columnas y filas**, o **Relleno de un área** (tantas como quepan por completo).
- Cuatro formas: **Rectángulo** (esquinas vivas, redondeadas o achaflanadas), **Círculo / elipse**, **Ranura**, **Polígono** (3 a 24 lados).
- Nueve posiciones para el punto dentro de la rejilla, más un desfase en X y en Y.
- Una separación propia para X y para Y.
- Una línea **Resultado** que muestra el número de formas y el tamaño total mientras se escribe.
- Como máximo 2000 formas por rejilla.

## Estado de las pruebas

- El cálculo de la rejilla, los contornos de las esquinas, los mensajes y los cinco archivos de idioma se comprueban con una prueba automática que funciona sin Fusion.
- El cambio de la versión 1.1.0.0 (el cuadro de diálogo sigue funcionando cuando el punto seleccionado de antemano no se puede tomar) se probó solo sin conexión, **no dentro de Fusion**.
- Dos límites conocidos proceden de una revisión del código y **no están confirmados dentro de Fusion**. Ver [troubleshooting.md](troubleshooting.md#límites-conocidos).

## Licencia y autor

Licencia MIT, ver [LICENSE](../LICENSE). Autor: Sorglos Thomas Weirich.

Historial de cambios: [CHANGELOG.md](../CHANGELOG.md).
