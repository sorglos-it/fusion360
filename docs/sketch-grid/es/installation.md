# Instalación

## Requisitos

- Autodesk Fusion 360 en Windows o macOS. El complemento declara estos dos sistemas y ningún otro.
- Nada más. El complemento usa solo el Python que viene integrado en Fusion.

El código no nombra ninguna versión mínima de Fusion.

## Instalar desde el ZIP de la versión

1. Abrir <https://github.com/sorglos-it/fusion360/releases>.
2. Descargar el archivo `SketchGrid-<version>.zip`, por ejemplo `SketchGrid-1.1.0.0.zip`.
3. Descomprimirlo en la carpeta de complementos de Fusion:

   | Sistema | Carpeta |
   | --- | --- |
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Comprobar el resultado. Dentro de la carpeta de complementos debe haber ahora una carpeta `SketchGrid`, y directamente dentro de ella los archivos `SketchGrid.py` y `SketchGrid.manifest`.

No cambiar el nombre de la carpeta. Fusion espera que la carpeta, el archivo `.py` y el archivo `.manifest` tengan el mismo nombre.

## Primer inicio en Fusion

1. Iniciar Fusion.
2. Abrir **Utilities → ADD-INS → Add-Ins**.
3. Seleccionar **SketchGrid** en la lista.
4. Pulsar **Run**.

El complemento está marcado en su manifiesto para ejecutarse al inicio (`runOnStartup` está activado). Si la próxima vez no se inicia solo, marcar **Run on Startup** en la misma lista.

Después del inicio aparece un botón llamado **Rejilla de boceto (1.1.0.0)**. El número entre paréntesis es la versión instalada. El complemento busca primero el panel **CREATE** de la barra de herramientas de boceto y, si no existe, el panel **CREATE** de la pestaña **SOLID**.

## Actualización

1. En Fusion, abrir **Utilities → ADD-INS → Add-Ins**, seleccionar **SketchGrid** y pulsar **Stop**. Si no, la versión antigua sigue en memoria.
2. Borrar la carpeta `SketchGrid` de la carpeta de complementos.
3. Descomprimir el ZIP nuevo en la carpeta de complementos, como arriba.
4. Pulsar **Run** de nuevo.
5. Comprobar la versión entre paréntesis en el botón.

El complemento no guarda ajustes en el disco. Al borrar la carpeta no se pierde nada.

## Desinstalación

1. En Fusion, detener el complemento (**Utilities → ADD-INS → Add-Ins**, seleccionar **SketchGrid**, **Stop**). Esto quita el botón.
2. Borrar la carpeta `SketchGrid` de la carpeta de complementos.

El complemento no deja ningún otro archivo. Las rejillas ya dibujadas se quedan en los bocetos; son geometría de boceto normal.
