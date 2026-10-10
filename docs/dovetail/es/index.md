# Dovetail – documentación

Dovetail es un complemento (add-in) para Autodesk Fusion 360. Convierte líneas de boceto en uniones: cola de milano,
triángulo o unión de caja. Por cada línea seleccionada dibuja una banda cerrada. La banda es exactamente tan ancha
como la holgura deseada entre las dos piezas. Al cortar la banda de un sólido quedan dos piezas que encajan entre sí.

Esta documentación describe la versión **1.1.0.0**.

## Contenido

| Archivo | Qué contiene |
|---|---|
| [installation.md](installation.md) | Requisitos, instalación, primer inicio, actualización, desinstalación |
| [usage.md](usage.md) | Todas las funciones, paso a paso |
| [settings.md](settings.md) | Todos los campos del cuadro de diálogo: significado, valor por defecto, límites; qué se recuerda; idioma |
| [how-it-works.md](how-it-works.md) | Cómo se construye la banda por dentro, las comprobaciones, las unidades |
| [troubleshooting.md](troubleshooting.md) | Todos los mensajes, su causa y qué hacer; límites conocidos |
| [development.md](development.md) | Carpetas, pruebas, números de versión, empaquetar una versión, decisiones |

## De un vistazo

| | |
|---|---|
| Funciona en | Autodesk Fusion 360 en Windows y macOS |
| Formas | Trapecio (cola de milano), Triángulo, Rectángulo (unión de caja) |
| Líneas por ejecución | 1 a 100 |
| Dientes por línea | 1 a 500 |
| Idiomas de la interfaz | Alemán, inglés, español, francés, italiano |
| Licencia | MIT, ver [LICENSE](../LICENSE) |
| Autor | Sorglos Thomas Weirich |

## Estado de las pruebas

- Los cálculos de la geometría y los archivos de idioma se prueban fuera de Fusion con un script de pruebas sin conexión.
- La versión 1.1.0.0 cambió la geometría (ver [how-it-works.md](how-it-works.md#qué-cambió-en-1100)).
  Estos cambios se probaron **solo sin conexión**, incluidos 34 317 contornos aleatorios. **Todavía no están
  confirmados dentro de Fusion**.

## Ver también

- [README](../README.md) – página de entrada breve
- [CHANGELOG](../CHANGELOG.md) – qué cambió en cada versión
