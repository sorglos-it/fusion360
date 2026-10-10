# Uso

Todos los nombres de campo de abajo están escritos exactamente como aparecen en el cuadro de diálogo en español. Cada
campo se explica en detalle en [settings.md](settings.md).

## Palabras que se usan aquí

| Palabra | Significado |
|---|---|
| Diente | Una cola de milano, un triángulo o un rectángulo que sobresale de la línea |
| Espiga | El diente como parte de una de las piezas |
| Caja | El hueco correspondiente en la otra pieza |
| Tolerancia | La holgura entre espiga y caja (el juego) |
| Banda | El contorno cerrado que dibuja el complemento. Su interior es exactamente la holgura. |
| Punto inicial, punto final | Los dos extremos de una línea de boceto, en el orden en que se dibujó la línea |

## Dibujar una unión sobre una línea

1. Abrir un boceto o editar uno existente.
2. Dibujar una línea recta donde deben encontrarse las dos piezas.
3. Hacer clic en la línea.
4. Hacer clic en el botón **Cola de milano**. Se abre el cuadro de diálogo. La línea ya está anotada en **Líneas**.
   También se puede iniciar primero el comando y después hacer clic en la línea.
5. Ajustar **Cantidad**, **Forma**, **Anchura (base)**, **Profundidad** y **Tolerancia**.
6. Observar la vista previa en el boceto.
7. Pulsar **OK**.

Resultado:

- Se dibuja una banda cerrada en el mismo boceto que la línea.
- La línea original se convierte en geometría de construcción (una línea auxiliar discontinua), si está marcado
  **Convertir la línea original en geometría de construcción**. Esto ocurre solo con OK, no en la vista previa.
- El complemento no añade cotas ni restricciones a las líneas nuevas.

Si **OK** está atenuado y no se muestra ninguna vista previa, los valores no encajan. El cuadro de diálogo no dice por qué.
Ver [troubleshooting.md](troubleshooting.md#ok-está-atenuado).

## Hacer dos piezas que encajan a partir de la banda

1. Dibujar el contorno de la pieza completa. Hacer que la línea de unión lo atraviese, de borde a borde.
2. Ejecutar Dovetail sobre la línea de unión.
3. Extruir el contorno para obtener un cuerpo sólido.
4. Extruir la banda como corte a través de ese cuerpo.

Quedan dos cuerpos. Encajan uno en otro con la holgura ajustada en **Tolerancia**.

Los pasos 3 y 4 son funciones normales de Fusion. El complemento solo dibuja la banda.

## Elegir la forma

Usar la lista **Forma**:

| Entrada | Resultado |
|---|---|
| **Trapecio (cola de milano)** | El diente se ensancha hacia la punta. Se engancha y no se puede sacar tirando en línea recta. |
| **Triángulo** | El diente termina en punta. No tiene gancho y se puede separar tirando. |
| **Rectángulo (unión de caja)** | Diente recto, misma anchura en la base y en la punta. |

**Ángulo de flanco** solo está activo con **Trapecio (cola de milano)**. Fija cuánto se ensancha el diente. Con 0 grados
el trapecio es igual que un rectángulo. Un ángulo negativo hace el diente más estrecho hacia la punta.

## Varios dientes sobre una línea

1. Poner **Cantidad** en 2 o más. El campo **Separación (centro a centro)** se activa.
2. Ajustar **Separación (centro a centro)**: la distancia del centro de un diente al centro del siguiente.

El grupo de dientes queda siempre simétrico alrededor del centro de la línea:

| Cantidad | Posición de los dientes respecto al centro (separación 30 mm) |
|---|---|
| 1 | 0 |
| 2 | −15 / +15 |
| 3 | −30 / 0 / +30 |
| 4 | −45 / −15 / +15 / +45 |
| 5 | −60 / −30 / 0 / +30 / +60 |

Una cantidad impar pone un diente en el centro. Una cantidad par deja allí un hueco.

## Mover los dientes a lo largo de la línea

Dos maneras:

- Escribir un valor en **Desplazamiento**. Un valor positivo mueve los dientes hacia el punto final de la línea, un valor
  negativo hacia el punto inicial. 0 significa centrado.
- Usar los tres botones de la fila **Desplazar**:

  | Botón | Efecto |
  |---|---|
  | **A la izquierda (hacia el punto inicial)** | mueve los dientes un **Incremento** hacia el punto inicial |
  | **Centrar** | vuelve a poner **Desplazamiento** en 0 |
  | **A la derecha (hacia el punto final)** | mueve los dientes un **Incremento** hacia el punto final |

Los botones se detienen donde los dientes ya no cabrían en la línea. Con varias líneas, la línea más corta fija este
límite. Un valor escrito a mano no se corrige: si es demasiado grande, OK queda atenuado.

**Desplazamiento** empieza en 0 cada vez que se abre el cuadro de diálogo.

## Elegir qué pieza cede material

La holgura tiene que salir de algún sitio. La lista **La línea es** lo decide:

| Entrada | Borde de la caja | Borde de la espiga | Usarla cuando |
|---|---|---|---|
| **Línea media - media tolerancia por lado** | se mueve hacia fuera media tolerancia | se mueve hacia dentro media tolerancia | las dos piezas deben seguir siendo iguales |
| **Borde de la caja - toda la tolerancia en la espiga** | exactamente sobre la forma dibujada | se mueve hacia dentro la tolerancia completa | la pieza con las cajas debe conservar su medida exacta |
| **Borde de la espiga - toda la tolerancia en la caja** | se mueve hacia fuera la tolerancia completa | exactamente sobre la forma dibujada | la pieza con las espigas debe conservar su medida exacta |

La holgura entre las piezas es la tolerancia completa en los tres casos.

Ejemplo con una tolerancia de 0.25 mm:

| Entrada | Caja | Espiga | Holgura |
|---|---|---|---|
| Línea media | +0.125 mm | −0.125 mm | 0.25 mm |
| Borde de la caja | 0 | −0.25 mm | 0.25 mm |
| Borde de la espiga | +0.25 mm | 0 | 0.25 mm |

## Poner los dientes en el otro lado

Marcar **Invertir la dirección**.

Sin la marca, los dientes quedan en el lado izquierdo de la línea mirando desde su punto inicial hacia su punto final
(en el plano X/Y del boceto). Con la marca, quedan en el lado derecho.

Con varias líneas, cada línea sigue su propia dirección. Las líneas dibujadas en sentidos opuestos reciben sus dientes en
lados opuestos. **Invertir la dirección** les da la vuelta a todas a la vez.

## Varias líneas a la vez

1. Seleccionar varias líneas antes de iniciar el comando. O iniciar el comando y hacer clic en las líneas una tras otra.
   Son posibles hasta 100 líneas.
2. Ajustar los valores una sola vez.
3. Pulsar **OK**.

Cada línea recibe su propia unión con los mismos valores. Cada línea se mide por separado y sus dientes se centran en
su propio centro. Las líneas pueden tener longitudes distintas.

Los valores deben caber en todas las líneas. Si una línea es demasiado corta, no se dibuja nada y OK queda atenuado.
Mirar primero la línea más corta; es la primera que se queda sin sitio.

Solo se pueden seleccionar líneas de boceto rectas. Arcos, círculos y splines no.

## Dos piezas idénticas: Reflejar la geometría

Marcar **Reflejar la geometría**.

La mitad de los dientes apunta entonces hacia un lado y la otra mitad hacia el otro. Si se gira la banda 180 grados
alrededor del centro de la línea, cae sobre sí misma. Por eso las dos piezas del corte son idénticas. Se puede modelar
una pieza y fabricarla dos veces; la segunda se coloca girada.

El cuadro de diálogo ajusta tres cosas por sí solo, porque cada una de ellas rompería la simetría:

| Qué | Por qué |
|---|---|
| **Cantidad** se sube al siguiente número par | Un diente en el centro tendría que apuntar a ambos lados a la vez. |
| **La línea es** se pone en la línea media y queda atenuado | Solo ahí ceden ambas piezas lo mismo. |
| **Desplazamiento** se pone en 0; **Desplazamiento**, **Incremento** y **Desplazar** quedan atenuados | Un grupo desplazado ya no es simétrico respecto al centro. |

Al quitar la marca, los campos vuelven a estar activos. Los valores que cambió el cuadro de diálogo se quedan como están.

Con varias líneas, cada línea se refleja respecto a su propio centro.

## Conservar o convertir la línea original

El campo **Convertir la línea original en geometría de construcción** está marcado por defecto.

- Marcado: la línea seleccionada se convierte en geometría de construcción con OK. Conserva sus cotas y restricciones,
  pero ya no divide la banda en dos áreas.
- Sin marcar: la línea sigue siendo una línea normal. Atraviesa la banda y la parte en dos áreas (perfiles).

Una línea que ya es geometría de construcción se deja como está.

## Vista previa

Mientras el cuadro de diálogo está abierto, el complemento dibuja la banda como vista previa después de cada cambio.

- La vista previa nunca cambia la línea original. Por eso la vista previa muestra la línea todavía como línea normal.
- Si los valores no encajan, no se muestra ninguna vista previa.

## Ejecutar el comando otra vez

Fusion puede repetir el comando con su propia función de "repetir el último comando"; el complemento lo permite.
El cuadro de diálogo se abre de nuevo con los valores de la última ejecución correcta. Ver
[settings.md](settings.md#qué-se-recuerda).
