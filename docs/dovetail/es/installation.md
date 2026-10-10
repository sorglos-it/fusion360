# Instalación

## Requisitos

- Autodesk Fusion 360 en Windows o macOS. El complemento declara exactamente estos dos sistemas.
- Nada más. El complemento funciona con el Python que trae Fusion y no usa paquetes adicionales.

En el código no se indica ninguna versión mínima de Fusion. El complemento no se probó con una lista de versiones de Fusion.

## Instalar desde el ZIP de la versión

1. Abrir <https://github.com/sorglos-it/fusion360/releases>.
2. Descargar el archivo `Dovetail-<version>.zip`, por ejemplo `Dovetail-1.1.0.0.zip`.
3. Descomprimir el ZIP en la carpeta de complementos de Fusion:

   | Sistema | Carpeta |
   |---|---|
   | Windows | `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns` |
   | macOS | `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns` |

4. Comprobar el resultado. El ZIP contiene una carpeta llamada `Dovetail`. Después de descomprimir debe existir esto:

   ```
   AddIns/Dovetail/Dovetail.py
   AddIns/Dovetail/Dovetail.manifest
   AddIns/Dovetail/lang/
   AddIns/Dovetail/resources/
   ```

   Si el programa de descompresión creó una carpeta adicional alrededor (por ejemplo `AddIns/Dovetail-1.1.0.0/Dovetail/`),
   mover la carpeta interior `Dovetail` un nivel hacia arriba.

No cambiar el nombre de la carpeta ni de los archivos. La carpeta, el archivo `.py` y el archivo `.manifest` deben llevar todos el mismo nombre.

## Primer inicio en Fusion

1. Iniciar Fusion.
2. Abrir la lista de complementos: **Utilities → ADD-INS → Add-Ins**.
   (El texto de este menú viene de Fusion y puede variar entre versiones de Fusion.)
3. Seleccionar la entrada **Dovetail**.
4. Marcar **Run on Startup** si no está marcado. El complemento lo solicita por sí mismo en su manifiesto.
5. Pulsar **Run**.

El complemento añade entonces un botón a la barra de herramientas. Su nombre es **Cola de milano** seguido de la versión
entre paréntesis, por ejemplo *Cola de milano (1.1.0.0)*.

Dónde aparece el botón:

| Orden | Lugar |
|---|---|
| 1 | el panel **Create** de la barra de herramientas de boceto |
| 2 | si falta: el panel **Modify** de la barra de herramientas de boceto |
| 3 | si también falta: el panel **Create** de la pestaña Solid |

El complemento toma el primero de ellos que exista. El botón se coloca directamente en la barra de herramientas, no solo
en el menú desplegable del panel.

Si no existe ninguno de los tres, aparece el mensaje "No se encontró ningún panel de barra de herramientas adecuado." Ver
[troubleshooting.md](troubleshooting.md).

## Actualización

1. En Fusion, abrir la lista de complementos y **detener** Dovetail. Si no, la versión antigua sigue en memoria.
2. Borrar la carpeta antigua `Dovetail` de la carpeta de complementos.
3. Descomprimir el ZIP nuevo en la carpeta de complementos, como se describe arriba.
4. Pulsar **Run** de nuevo, o reiniciar Fusion.
5. Comprobar la versión en el nombre del botón o en el título del cuadro de diálogo.

El complemento no guarda ajustes en el disco. Al borrar la carpeta antigua no se pierde nada.

Nota del README anterior, no comprobable en el código actual: las versiones muy antiguas se llamaban `Schwalbenschwanz`.
Si una carpeta así sigue en la carpeta de complementos, detener ese complemento y borrar la carpeta. Si no, aparecen dos botones.

## Desinstalación

1. En Fusion, abrir la lista de complementos y **detener** Dovetail. Esto quita el botón y el comando.
2. Cerrar Fusion.
3. Borrar la carpeta `Dovetail` de la carpeta de complementos.

El complemento no escribe ningún otro archivo ni ningún ajuste. Las uniones ya dibujadas se quedan en los bocetos; son
líneas de boceto normales.
