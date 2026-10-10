# Instalación

Volver al [resumen](index.md).

## Requisitos

| Qué | Detalle |
| --- | --- |
| Programa | Autodesk Fusion 360 |
| Sistema operativo | Windows o macOS (el complemento declara ambos como compatibles) |
| Software adicional | Ninguno. El complemento usa solo lo que Fusion trae consigo. |
| Internet | Solo para descargar el archivo ZIP. El complemento en sí no abre ninguna conexión. |

## Instalar desde el ZIP de la publicación

1. Abrir <https://github.com/sorglos-it/fusion360/releases>.
2. Descargar el archivo `System3E-<version>.zip`, por ejemplo `System3E-1.1.0.0.zip`.
3. Descomprimir el ZIP en la carpeta de complementos de Fusion:

   | Sistema | Carpeta |
   | --- | --- |
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Comprobar el resultado. El ZIP contiene una carpeta llamada `System3E`. Después de descomprimir debe existir este archivo:

   `AddIns/System3E/System3E.py`

   Si aparece `AddIns/System3E/System3E/System3E.py`, la carpeta está un nivel demasiado abajo. Hay que subir un nivel la carpeta interior.

Consejo para Windows: escribir `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` en la barra de direcciones del Explorador y pulsar Intro.

## Primer inicio en Fusion

1. Iniciar Fusion.
2. Abrir **Utilities → ADD-INS → Add-Ins**.
3. Seleccionar **System3E** en la lista.
4. Pulsar **Run**.
5. Abrir la pestaña **SOLID**. El botón **Elemento SYSTEM 3E** está en el panel **Create**.

El botón muestra la versión entre paréntesis, por ejemplo **Elemento SYSTEM 3E (1.1.0.0)**.

El complemento está marcado para iniciarse junto con Fusion (`runOnStartup` en su archivo de manifiesto). Después del primer inicio, normalmente no hace falta volver a pulsar **Run**.

Nota: la ruta de menú del paso 2 está tomada del README del proyecto. No se puede comprobar en el código del complemento, y las versiones de Fusion pueden nombrarla de otra forma.

## Actualización

1. En Fusion, detener el complemento (**Utilities → ADD-INS → Add-Ins**, seleccionar **System3E**, **Stop**), o cerrar Fusion.
2. Borrar la carpeta antigua `System3E` de la carpeta de complementos.
3. Descomprimir el ZIP nuevo en la carpeta de complementos, como se describe arriba.
4. Iniciar Fusion, o pulsar **Run** otra vez.

Qué pasa con los diseños:

- Los elementos ya colocados se quedan como están. Son componentes normales de Fusion.
- Un elemento colocado con una versión anterior puede tener menos de doce puntos. Los puntos que faltan se añaden la próxima vez que se coloque el mismo elemento en ese diseño.
- Los valores recordados del cuadro de diálogo se pierden. Véase [settings.md](settings.md).

## Eliminación

1. En Fusion, detener el complemento, o cerrar Fusion.
2. Borrar la carpeta `System3E` de la carpeta de complementos.

Cuando el complemento se detiene, quita su botón de la barra de herramientas. No guarda nada fuera de su propia carpeta. Los elementos de los diseños se quedan; no necesitan el complemento.
