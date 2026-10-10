# Usage

All field names below are written exactly as they appear in the English dialog. Details on every field: [settings.md](settings.md).

## Draw a grid

1. Open or edit a sketch.
2. Click one sketch point. This can be the sketch origin or a point you placed yourself.
3. Click the button **Sketch Grid**. The dialog opens. The point you clicked is already entered in **Point**.
4. If **Point** is empty, click a sketch point now. The prompt reads "Select a sketch point".
5. Set the values. The **Result** line shows what you will get, for example `8 × 4 = 32 shapes, 94.00 × 26.00 mm overall`.
6. Look at the preview in the sketch.
7. Press **OK**.

Only sketch points can be picked. Exactly one point is needed.

**OK** is greyed out as long as a value is not allowed. In most cases the **Result** line then shows the reason. See [troubleshooting.md](troubleshooting.md).

The grid lies along the X and Y axes of the sketch. It cannot be rotated in the dialog. Words like "left", "right", "top", "bottom" and "up" in this documentation mean the sketch axes: right is +X, up is +Y.

Taking over a point that was clicked before the dialog opened (step 3) was changed in version 1.1.0.0 and tested offline only, not inside Fusion. If the point is not taken over, pick it in the dialog (step 4).

## Example

These are the values the dialog starts with:

| Field | Value |
| --- | --- |
| **Shape** | Rectangle |
| **Length (X)** | 10 mm |
| **Depth (Y)** | 5 mm |
| **Gap X** / **Gap Y** | 2 mm |
| **Columns** / **Rows** | 8 / 4 |

Result: 32 rectangles. The grid is 94 × 26 mm (8 × 10 + 7 × 2 = 94, 4 × 5 + 3 × 2 = 26). With **Point sits in the grid** set to **In the middle**, the point is the centre of the grid.

## Choose how the shapes are counted

Field **Count from**.

### Columns and rows

1. Set **Count from** to **Columns and rows**.
2. Enter **Columns** and **Rows**.

You get exactly that many. The grid is as large as it needs to be.

### Fitting an area

1. Set **Count from** to **Fitting an area**.
2. Enter **Area width** and **Area height**.

The add-in draws as many shapes as fit **completely** into the area. A partly fitting shape is never drawn.

- Example: area width 100 mm, length 10 mm, gap 2 mm gives 8 columns. They use 94 mm. A ninth column would need 106 mm.
- The grid is usually a little smaller than the area. The area is only used for counting. It is not drawn.
- The rest of the area stays empty on the side away from the point. With **In the middle** it is split evenly on both sides.
- An area of exactly 94 mm gives 8 columns; 93.9 mm gives 7.

The fields **Columns** and **Rows** are shown only in the first mode, **Area width** and **Area height** only in the second.

## Choose the shape

Field **Shape**.

| Entry | What you get |
| --- | --- |
| **Rectangle** | A rectangle of length × depth. Its corners can be changed, see below. |
| **Circle / ellipse** | An ellipse with length and depth as its two diameters. Equal values give a circle. |
| **Slot** | A rectangle with two half-round ends. The ends are on the longer direction: if length is larger than depth, the left and right ends are round. Equal values give a circle. |
| **Polygon** | A shape with 3 to 24 straight sides. One corner always points up. |

### Rectangle: corners

1. Set **Shape** to **Rectangle**. The field **Corners** appears.
2. Choose **Sharp**, **Rounded** or **Chamfered**. (Chamfered means: the corner is cut off with a straight line.)
3. For **Rounded** and **Chamfered**, the field **Radius / chamfer** appears. Enter the radius of the rounding, or how far the cut starts from the corner along each edge.

The largest allowed value is half of the shorter edge. At exactly that value:

| Rectangle | Value | Rounded becomes | Chamfered becomes |
| --- | --- | --- | --- |
| 10 × 5 mm | 2.5 mm | a slot | a six-sided shape |
| 10 × 10 mm | 5 mm | a circle | a diamond |

The corners do not change the number of shapes, the spacing or the overall size.

### Polygon: sides and Regular

1. Set **Shape** to **Polygon**. The fields **Sides** and **Regular** appear.
2. Enter **Sides** (3 to 24).
3. Leave **Regular** off, or tick it.

| **Regular** | Result |
| --- | --- |
| off | The polygon is stretched so that it is exactly length × depth. Its sides are then usually not equally long. |
| on | All sides are equally long. The smaller of length and depth sets the size. The spacing follows the real size of the polygon, so the gap is still the gap you entered. |

Example with 6 sides, length 10 mm, depth 5 mm, gap 2 mm:

| **Regular** | Size of one shape | Distance from one shape to the next |
| --- | --- | --- |
| off | 10.00 × 5.00 mm | 12.00 × 7.00 mm |
| on | 4.33 × 5.00 mm | 6.33 × 7.00 mm |

## Set size and gap

- **Length (X)** and **Depth (Y)**: size of one shape.
- **Gap X** and **Gap Y**: free space between two neighbours. 0 is allowed; the shapes then touch. Negative values are not allowed.

## Decide where the point sits

Field **Point sits in the grid**. It says where the point you clicked ends up inside the finished grid. It does not say in which direction the grid grows.

Example: **Bottom left** puts the point on the bottom left corner of the grid. The grid then extends to the right and upwards.

Three of the nine positions, with a grid of 3 × 2 shapes (`X` is the point, `#` the shapes):

```
  In the middle        Bottom left          Top centre
  #####.#####.#####    #####.#####.#####    #####.##X##.#####
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  ........X........    .................    .................
  #####.#####.#####    #####.#####.#####    #####.#####.#####
  #####.#####.#####    X####.#####.#####    #####.#####.#####
```

All nine entries are listed in [settings.md](settings.md#point-sits-in-the-grid).

## Shift the grid away from the point

Fields **Offset X** and **Offset Y**.

1. Choose the position in **Point sits in the grid** first.
2. Enter how far the whole grid should move. Positive values move it along the X and Y axis of the sketch. Negative values move it the other way.

Use it to keep a margin: the point stays at a corner of your part, and the grid starts, for example, 2 mm further in. The offset does not change the number of shapes or the size of the grid.

## Read the Result line

**Result** cannot be edited. It shows either

- `{columns} × {rows} = {number} shapes, {width} × {height} mm overall`, always in millimetres with two decimals, or
- a message that says which value is not allowed.

## Draw another grid

- The dialog opens with the values of the last grid you finished with **OK**. See [settings.md](settings.md#what-is-remembered).
- The command is marked as repeatable, so Fusion's own "repeat last command" function can start it again.

## What you get in the sketch

- Plain sketch lines, arcs, circles and ellipses. No Fusion pattern feature is created.
- The shapes are not linked to the dialog. To change the grid later, delete the shapes and draw a new grid.
- The add-in adds no dimensions and no constraints of its own between the shapes and the point.
