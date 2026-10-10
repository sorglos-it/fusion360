# Ajustes

El complemento no tiene archivo de ajustes ni página de ajustes. Todo se ajusta en el cuadro de diálogo del comando.
Los campos se enumeran en el orden en que los muestra el cuadro de diálogo.

## Campos del cuadro de diálogo

| Campo | Significado | Valor por defecto | Valores permitidos |
|---|---|---|---|
| **Líneas** | Las líneas de boceto que reciben una unión. Texto de indicación: "Selecciona una o varias líneas de boceto". | las líneas seleccionadas antes de iniciar el comando | 1 a 100 líneas de boceto rectas |
| **Cantidad** | Número de dientes por línea | 1 | número entero, 1 a 500 |
| **Reflejar la geometría** | Hace idénticas las dos piezas, ver [usage.md](usage.md#dos-piezas-idénticas-reflejar-la-geometría) | desactivado | activado / desactivado |
| **Forma** | Forma del diente | Trapecio (cola de milano) | Trapecio (cola de milano), Triángulo, Rectángulo (unión de caja) |
| **Anchura (base)** | Anchura del diente donde toca la línea | 10 mm | mayor que 0, y mayor que el doble de la tolerancia |
| **Profundidad** | Cuánto sobresale el diente de la línea | 6 mm | mayor que 0 |
| **Ángulo de flanco** | Solo trapecio: cuánto se inclina hacia fuera cada lado del diente | 15 deg | más de −89 y menos de 89 grados; ver abajo |
| **Separación (centro a centro)** | Distancia del centro de un diente al centro del siguiente. Solo se usa con 2 o más dientes. | 20 mm | mayor que 0 y al menos la separación mínima, ver abajo |
| **Desplazamiento** | Desplazamiento de todo el grupo de dientes a lo largo de la línea. Positivo: hacia el punto final. | 0 mm, siempre | entre menos y más el desplazamiento máximo, ver abajo |
| **Incremento** | Cuánto mueve los dientes un clic en un botón de **Desplazar** | 1 mm | el complemento no lo comprueba, ver abajo |
| **Desplazar** | Tres botones: **A la izquierda (hacia el punto inicial)**, **Centrar**, **A la derecha (hacia el punto final)** | – | – |
| **Tolerancia** | Holgura entre las dos piezas | 0.25 mm | mayor que 0; más límites abajo |
| **La línea es** | Qué pieza cede material para la holgura | Línea media - media tolerancia por lado | las tres entradas enumeradas abajo |
| **Invertir la dirección** | Pone los dientes en el otro lado de la línea | desactivado | activado / desactivado |
| **Convertir la línea original en geometría de construcción** | Convierte la línea seleccionada en una línea auxiliar con OK | activado | activado / desactivado |

Entradas de **La línea es**:

| Entrada | La caja crece | La espiga se reduce |
|---|---|---|
| **Línea media - media tolerancia por lado** | media tolerancia | media tolerancia |
| **Borde de la caja - toda la tolerancia en la espiga** | nada | la tolerancia completa |
| **Borde de la espiga - toda la tolerancia en la caja** | la tolerancia completa | nada |

## Campos que quedan atenuados

| Campo | Atenuado cuando |
|---|---|
| **Ángulo de flanco** | **Forma** no es Trapecio (cola de milano). El valor se ignora entonces. |
| **Separación (centro a centro)** | **Cantidad** es 1. El valor se ignora entonces. |
| **La línea es**, **Desplazamiento**, **Incremento**, **Desplazar** | **Reflejar la geometría** está marcado |

## Los límites en detalle

Todos los límites salen del código. Las longitudes de abajo están en milímetros.

La "media anchura de la punta" se usa en varios límites. Depende de la forma:

| Forma | Media anchura de la punta |
|---|---|
| Rectángulo (unión de caja) | Anchura ÷ 2 |
| Triángulo | 0 |
| Trapecio (cola de milano) | Anchura ÷ 2 + Profundidad × tan(Ángulo de flanco) |

La "mitad más ancha" es el mayor de Anchura ÷ 2 y la media anchura de la punta.

### Ángulo de flanco

- Debe ser mayor que −89 y menor que 89 grados. Exactamente 89 o −89 se rechaza.
- Con un ángulo negativo la punta se estrecha. La media anchura de la punta debe seguir por encima de 0. Si no, el
  diente se reduciría a cero y se rechaza.
- 0 grados da un rectángulo.

### Separación (centro a centro)

Solo se comprueba con 2 o más dientes.

Separación mínima = 2 × mitad más ancha + 2 × Tolerancia + 0.01 mm

Ejemplo con los valores por defecto (Anchura 10 mm, Profundidad 6 mm, Ángulo de flanco 15 deg, Tolerancia 0.25 mm):
la media anchura de la punta es de unos 6.61 mm, así que la separación mínima es de unos 13.73 mm.

### Sitio en la línea

Los dientes deben guardar una distancia con ambos extremos de la línea: la tolerancia más 0.01 mm.

Longitud necesaria = (Cantidad − 1) × Separación + 2 × mitad más ancha + 2 × (Tolerancia + 0.01 mm)

Ejemplo con los valores por defecto y un diente: se necesitan unos 13.74 mm de línea.

### Desplazamiento

Desplazamiento máximo = Longitud de la línea ÷ 2 − ( (Cantidad − 1) ÷ 2 × Separación + mitad más ancha + Tolerancia + 0.01 mm )

- El desplazamiento puede estar entre menos y más este valor.
- Los botones de **Desplazar** se detienen en este valor. Con varias líneas decide la línea más corta.
- Un desplazamiento escrito a mano no se corrige. Si es demasiado grande, OK queda atenuado.
- Con **Reflejar la geometría** el desplazamiento debe ser 0.

### Tolerancia

- Debe ser mayor que 0. La banda consiste en la holgura; con 0 no hay banda.
- El doble de la tolerancia debe ser menor que **Anchura (base)**.
- Después de quitar la tolerancia, debe quedar al menos el 5 % de **Profundidad** como altura del diente. Esto importa
  sobre todo en dientes puntiagudos, donde la punta pierde más altura que la tolerancia.
- La banda no debe cruzarse a sí misma y ninguno de sus tramos puede reducirse a nada. Esto puede ocurrir con puntas de
  trapecio estrechas y una tolerancia grande.
- En una esquina afilada, la esquina desplazada no debe alejarse más de 12 veces la distancia de desplazamiento.

### Cantidad

- 1 a 500.
- Con **Reflejar la geometría** la cantidad debe ser par. El cuadro de diálogo sube en 1 una cantidad impar.

### Incremento

El complemento no comprueba este valor. Según el código: con 0 los botones de **Desplazar** no hacen nada; un valor
negativo invierte el sentido de los botones izquierdo y derecho.

### Líneas

- Solo se pueden seleccionar líneas de boceto rectas.
- Al menos 1, como máximo 100.
- Una línea debe tener una longitud mayor que 0.

## Unidades

- Los campos de longitud se muestran en milímetros, el ángulo en grados.
- Los números dentro de los mensajes de error están siempre en milímetros con dos decimales.
- Por dentro, el complemento calcula en centímetros y radianes, las unidades que Fusion usa internamente.

## Qué se recuerda

El complemento recuerda los valores de la última ejecución que se terminó con **OK** y salió bien.

| Se recuerda | No se recuerda |
|---|---|
| Cantidad | Líneas |
| Reflejar la geometría | Desplazamiento (siempre empieza en 0) |
| Forma | |
| Anchura (base) | |
| Profundidad | |
| Ángulo de flanco | |
| Separación (centro a centro) | |
| Incremento | |
| Tolerancia | |
| La línea es | |
| Invertir la dirección | |
| Convertir la línea original en geometría de construcción | |

Durante cuánto tiempo:

- Los valores se guardan solo en memoria. No se escribe nada en el disco.
- Duran mientras la sesión de Fusion esté abierta. Después de cerrar Fusion vuelven a valer los valores por defecto de la tabla de arriba.
- Cerrar el cuadro de diálogo con Cancel no cambia los valores recordados.

El desplazamiento se deja fuera a propósito: pertenece a la línea en cuestión, no a los ajustes.

## Idioma

El complemento tiene textos en cinco idiomas: alemán, inglés, español, francés, italiano.

El idioma se elige una sola vez, cuando se inicia el complemento:

1. Se usa el idioma ajustado en las preferencias de Fusion (idioma del usuario) si es uno de los cinco.
2. Si no, el complemento mira las variables de entorno `LANG`, `LANGUAGE` y `LC_ALL`, en este orden.
3. Si eso no da nada, mira el idioma del sistema operativo.
4. Si eso tampoco da nada, se usa el inglés.

No hay ningún selector de idioma en el cuadro de diálogo. Después de cambiar el idioma en Fusion, hay que iniciar de
nuevo el complemento (reiniciar Fusion lo hace).

Si falta un texto suelto en un archivo de idioma, se muestra en su lugar el texto en inglés.
