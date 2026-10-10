# Usage

Back to the [overview](index.md).

The add-in has one function: the command **SYSTEM 3E element**. It places one wall element per run.

## Place an element

1. Open a design in Fusion.
2. On the **SOLID** tab, in the **Create** panel, click **SYSTEM 3E element**.
3. **Point**: click the place for the element. You may click
   - a sketch point,
   - a corner of a body,
   - a construction point – this includes the points of an element placed before.

   If you click nothing, the element goes to the origin of the design. The prompt says so:
   "Select a point (none: origin)".
4. **Family**: choose the group of elements.
5. **Element**: choose the element. Each entry shows the name and the size in mm as length x width x height,
   for example `S1 WP   707 x 352 x 300`.
6. Look at the picture below the list. It shows the chosen element.
7. **Placed by**: choose which spot of the element lands on the point. See below.
8. **Rotation**: type an angle if the element shall be turned.
9. **Offset X**, **Offset Y**, **Offset Z**: type a distance if the element shall be moved away from the point.
10. Press **OK**.

You can also click the point first and then the button. The add-in takes the point over into the field **Point**.

While the dialog is open, Fusion shows the element at its place as a preview. It is created for good when you
press **OK**.

## Family and element

There are eight families with 74 elements. The order is the order of the manufacturer's catalogue.

| Family | Elements |
| --- | --- |
| Starter | 12 |
| Basic | 6 |
| Complementary | 8 |
| Lintel | 8 |
| Window framing | 6 |
| Top | 12 |
| Corner | 18 |
| Partition wall | 4 |

When you change the family, the element list is filled again and its first element is selected.

All elements, with their size in mm (length x width x height):

**Starter**

| Element | Size |
| --- | --- |
| S0 200 WP | 707 x 352 x 200 |
| S0 200 W | 704 x 352 x 200 |
| S0/2 200 W | 352 x 352 x 200 |
| S0/2 200 P | 355 x 352 x 200 |
| S0 250 WP | 707 x 352 x 250 |
| S0 250 W | 704 x 352 x 250 |
| S0/2 250 W | 352 x 352 x 250 |
| S0/2 250 P | 355 x 352 x 250 |
| S0 300 WP | 707 x 352 x 300 |
| S0 300 W | 704 x 352 x 300 |
| S0/2 300 W | 352 x 352 x 300 |
| S0/2 300 P | 355 x 352 x 300 |

**Basic**

| Element | Size |
| --- | --- |
| S1 WP | 707 x 352 x 300 |
| S1 W | 704 x 352 x 300 |
| S1/2 W | 352 x 352 x 300 |
| S1/2 P | 355 x 352 x 300 |
| ST W | 222 x 352 x 300 |
| ST P | 225 x 352 x 300 |

**Complementary**

| Element | Size |
| --- | --- |
| EU 150 WP | 707 x 352 x 150 |
| EU 150 W | 704 x 352 x 150 |
| EU/2 150 W | 352 x 352 x 150 |
| EU/2 150 P | 355 x 352 x 150 |
| EU 200 WP | 707 x 352 x 200 |
| EU 200 W | 704 x 352 x 200 |
| EU/2 200 W | 352 x 352 x 200 |
| EU/2 200 P | 355 x 352 x 200 |

**Lintel**

| Element | Size |
| --- | --- |
| EN WP | 707 x 352 x 170 |
| EN W | 704 x 352 x 170 |
| EN/2 W | 352 x 352 x 170 |
| EN/2 P | 355 x 352 x 170 |
| EPN WP L | 707 x 352 x 300 |
| EPN W L | 704 x 352 x 300 |
| EPN WP P | 707 x 352 x 300 |
| EPN W P | 704 x 352 x 300 |

**Window framing**

| Element | Size |
| --- | --- |
| EO/2 WP L | 707 x 352 x 300 |
| EO/2 WP P | 707 x 352 x 300 |
| EO/2 W P | 704 x 352 x 300 |
| EO/2 200 WP L | 707 x 352 x 300 |
| EO/2 200 WP P | 707 x 352 x 300 |
| EO/2 200 W P | 704 x 352 x 300 |

**Top**

| Element | Size |
| --- | --- |
| EWN WP L | 707 x 352 x 250 |
| EWN W L | 704 x 352 x 250 |
| EWN WP P | 707 x 352 x 250 |
| EWN W P | 704 x 352 x 250 |
| SZ/EO WP | 707 x 352 x 250 |
| SZ/EO W | 704 x 352 x 250 |
| SZ/2 W | 352 x 352 x 250 |
| SZ/2 P | 355 x 352 x 250 |
| SZ/EO 200 WP | 707 x 352 x 200 |
| SZ/EO 200 W | 704 x 352 x 200 |
| SZ/2 200 W | 352 x 352 x 200 |
| SZ/2 200 P | 355 x 352 x 200 |

**Corner**

| Element | Size |
| --- | --- |
| SNL | 704 x 352 x 300 |
| SNL/2 | 352 x 352 x 300 |
| SNP | 704 x 352 x 300 |
| SNP/2 | 352 x 352 x 300 |
| ENL | 704 x 352 x 300 |
| ENP | 704 x 352 x 300 |
| SZL | 704 x 352 x 250 |
| SZP | 704 x 352 x 250 |
| EWNL | 704 x 352 x 250 |
| EWNP | 704 x 352 x 250 |
| EO/2 LT | 704 x 352 x 300 |
| EO/2 LP | 698 x 352 x 300 |
| EO/2 PT | 704 x 352 x 300 |
| EO/2 PP | 704 x 352 x 300 |
| EO/2 200 LT | 704 x 352 x 300 |
| EO/2 200 LP | 704 x 352 x 300 |
| EO/2 200 PT | 704 x 352 x 300 |
| EO/2 200 PP | 704 x 352 x 300 |

**Partition wall**

| Element | Size |
| --- | --- |
| D1 115 | 704 x 115 x 250 |
| D1/2 115 | 352 x 115 x 250 |
| D1 175 | 704 x 175 x 200 |
| D1/2 175 | 352 x 175 x 200 |

Notes on the list:

- The sizes are the outer sizes stored in the element library, rounded to whole mm.
- The names are the catalogue names. The add-in does not translate them.
- The left/right names of the corner and window elements were matched by eye against the manufacturer's catalogue
  cards. They are **not confirmed**. Check the picture and the placed body before you rely on the name.
- `S0/2 200 P` is damaged in the manufacturer's 3D file. Its shape is rebuilt from `S0/2 250 P`.
- The four partition wall elements are plain blocks. Their sizes come from the catalogue cards.

## The preview picture

- The picture shows the chosen element as a grey shaded view, seen from the front left and from above.
- It changes when you change **Family** or **Element**.
- The pictures are drawn from the element library. They are not taken from the manufacturer's catalogue.

## Directions on an element

These words are used for the points and under **Placed by**.

| Word | Meaning |
| --- | --- |
| front | the end of the element at length 0 |
| back | the other end |
| right, left | as seen from the front end, looking along the wall |
| bottom | the underside |
| top | the height where the next course stands (see below), or the highest point for the two top corners |

A course is one layer of elements in a wall.

With **Rotation** 0, the length runs along the X axis of the design, the wall thickness along Y and the height
along Z. "Right" is then the side with the smaller Y value.

## The twelve points of an element

Every placed element carries twelve construction points. A construction point is a helper point in Fusion that you
can click. The points have names. The names are written in the language the add-in used when the element was
first placed.

| Name | Where it is |
| --- | --- |
| bottom front | underside, front end, middle of the wall thickness |
| bottom middle | underside, half length, middle of the wall thickness |
| bottom back | underside, back end, middle of the wall thickness |
| top front | height of the next course, front end, middle of the wall thickness |
| top middle | height of the next course, half length, middle of the wall thickness |
| top back | height of the next course, back end, middle of the wall thickness |
| top middle right | height of the next course, half length, right wall face |
| top middle left | height of the next course, half length, left wall face |
| bottom middle right | underside, half length, right wall face |
| bottom middle left | underside, half length, left wall face |
| middle right, 50 mm up | 50 mm above the underside, half length, right wall face |
| middle left, 50 mm up | 50 mm above the underside, half length, left wall face |

"Height of the next course": elements with the raised profile on top carry the next course 50 mm below their
highest point. Flat elements carry it on top. Example: `S1 WP` is 300 mm high, the next course stands at 250 mm.

The drawing shows all points on the basic element `S1 WP`. Its labels are in German. Yellow: can be clicked.
Red: can be chosen under **Placed by**. Green: both.

![The points on the element S1 WP](../s1-wp-punkte.svg)

State: the points have been used inside Fusion by the author.

## Placed by

**Placed by** decides which spot of the new element lands on the clicked point. The list has 15 entries:

| Entry | Spot of the element |
| --- | --- |
| Bottom corner, front right | lowest corner of the front end, right side. This is the default. |
| Top corner, front right | highest corner of the front end, right side |
| Top corner, front left | highest corner of the front end, left side |
| bottom front … middle left, 50 mm up | one of the twelve points from the table above |

The two top corners use the full height of the element, not the height of the next course.

State: the choices under **Placed by** have been used inside Fusion by the author.

## Rotation

- **Rotation** turns the element about the vertical axis. This is the Z axis of the design.
- The turn happens around the spot chosen under **Placed by**. That spot stays on the clicked point.
- The angle is given in degrees. A positive angle turns counter-clockwise when you look from above.

## Offsets

- **Offset X**, **Offset Y** and **Offset Z** move the element away from the clicked point.
- The values are in mm.
- They run along the axes of the design. They do not turn with the element.
- Negative values move in the other direction.

Example: no point clicked, **Offset Z** 300 mm. The element is placed 300 mm above the origin.

State: the offsets have been used inside Fusion by the author.

## Build a wall in bond

"In bond" means: every course is shifted by half an element against the course below.

1. Place the first element of the lowest course. Use **Placed by**: **Bottom corner, front right**.
2. Start the command again. Choose **Placed by**: **bottom front**.
3. Click the point **bottom back** of the element just placed. The next element continues the course.
4. Repeat this until the first course is finished.
5. For the second course, start the command again. Choose **Placed by**: **bottom middle**.
6. Click the point **top front** or **top back** of an element of the course below.
   The new element then sits half on that element and half beside it.
7. Continue the second course as in steps 2 and 3.

The settings stay as you left them, so you only click the next point and press **OK**.

Notes:

- Step 6 is the way the add-in's own description gives for a wall in bond. Steps 2 to 4 follow from the positions
  of the points; they are **not tested inside Fusion**.
- On elements with a tongue at the end (3 mm longer, names ending in `WP` or `P`) the points **bottom front** and
  **bottom back** lie at the outermost ends. Check the joint between two elements in your design.
- The add-in does not check whether elements overlap or whether an element fits at a place.

## Parts list: how equal elements count

- The first time you place an element, the add-in creates a component named `SYSTEM 3E <name>`,
  for example `SYSTEM 3E S1 WP`. The body inside is named like the element, for example `S1 WP`.
- Every further time you place the same element in that design, the add-in adds another copy of that same
  component. It does not create a new component.
- A parts list therefore shows one line for the element with its quantity, not `S1 WP`, `S1 WP (1)`, `S1 WP (2)`.
- You may rename the component. The add-in still finds it, because it leaves an invisible mark on it.
- Because the copies share one component, a change to the body of one copy changes all copies.
- All elements are created directly in the top level of the design (the root component).
