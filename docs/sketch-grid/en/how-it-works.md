# How it works

## Files

The installed add-in is one folder, `SketchGrid`:

| File | Purpose |
| --- | --- |
| `SketchGrid.py` | The add-in itself: dialog, grid calculation, checks, drawing. |
| `sketchgrid_core.py` | Shared helpers that are not specific to this add-in: reading the language files, finding the language, finding the toolbar panel, keeping the event handlers alive, showing unexpected errors, reading the version. |
| `SketchGrid.manifest` | Description for Fusion: author, version, supported systems (Windows and macOS), start with Fusion. |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | All texts, one file per language. `en.xml` is the reference. |
| `resources/SketchGrid/16x16.png`, `32x32.png`, `64x64.png` | The button icon in three sizes. |

The add-in reads only its own folder. It writes no files and opens no network connection.

## Start and stop

On start (`run`):

1. The language is detected and the matching language file is loaded.
2. A command definition left over from an earlier start is deleted.
3. The command is created. Its name is the text **Sketch Grid** plus the version from the manifest in brackets.
4. The add-in looks for a toolbar panel: first the panel with the id `SketchCreatePanel`, then `SolidCreatePanel`; each first in the Design workspace, then among all panels. If none exists, the message "No suitable toolbar panel was found." appears and no button is added.
5. The button is added to the panel and shown directly on the toolbar.

On stop (`stop`), the button and the command are removed and the event handlers are released.

## What happens while the dialog is open

| Event | What the add-in does |
| --- | --- |
| Dialog opens | Builds all fields with the remembered values. Tries to take over a sketch point that was selected beforehand. If that fails, the dialog stays usable and the point is picked in the dialog. (Tested offline only, not inside Fusion.) |
| A field changes | Shows or hides the fields that belong to the chosen mode and shape. Recalculates the **Result** line. |
| Fusion asks whether the inputs are valid | Runs all checks. If one fails, **OK** is disabled. |
| Fusion asks for a preview | Runs all checks and draws the grid as a preview. If a check fails, nothing is drawn and nothing is reported. |
| **OK** | Runs all checks again, draws the grid, then remembers the values. |

The preview is not reused as the final result. On **OK** the grid is drawn again.

## Units

- Inside, all lengths are centimetres. This is Fusion's internal unit, whatever unit the document shows.
- The length fields in the dialog are created with the unit `mm`.
- For the **Result** line and for messages, values are converted to millimetres (× 10) and shown with two decimals.
- Comparisons allow a tiny tolerance of 0.000000001 cm, so that rounding noise does not trigger a message.

## How the grid is calculated

The calculation is done by `grid_layout()`. It uses no Fusion functions.

### Step 1: size of one shape

Normally one shape takes exactly length × depth.

Exception: a polygon with **Regular** ticked. It takes less room. Its real size is measured:

1. The corners of the polygon are placed on a circle with radius 1, the first corner pointing up.
2. The width and height of the smallest box around these corners are measured.
3. Both are multiplied by half of the smaller of length and depth.

Example: 6 sides, length 10 mm, depth 5 mm gives 4.33 × 5.00 mm.

### Step 2: pitch

Pitch means the distance from one shape to the same spot on the next shape.

- pitch X = size of one shape in X + **Gap X**
- pitch Y = size of one shape in Y + **Gap Y**

### Step 3: number of columns and rows

**Columns and rows:** the numbers from the dialog are used.

**Fitting an area:** n shapes need n sizes and n − 1 gaps. So:

- columns = (area width + gap X) ÷ pitch X, rounded down
- rows = (area height + gap Y) ÷ pitch Y, rounded down

Example: (100 + 2) ÷ 12 = 8.5, so 8 columns.

If columns × rows is more than 2000, the grid is refused.

### Step 4: overall size

- overall width = columns × pitch X − gap X
- overall height = rows × pitch Y − gap Y

Example: 8 × 12 − 2 = 94 mm.

### Step 5: position (anchor and offset)

The anchor is the entry chosen in **Point sits in the grid**. Each entry stands for two factors between 0 and 1: how far the point is from the left edge and from the bottom edge of the grid, as a share of the overall size.

| Entry | Factor X | Factor Y |
| --- | --- | --- |
| In the middle | 0.5 | 0.5 |
| Bottom left | 0 | 0 |
| Bottom right | 1 | 0 |
| Top left | 0 | 1 |
| Top right | 1 | 1 |
| Bottom centre | 0.5 | 0 |
| Top centre | 0.5 | 1 |
| Left centre | 0 | 0.5 |
| Right centre | 1 | 0.5 |

The bottom left corner of the grid, measured from the picked point:

- X = −factor X × overall width + **Offset X**
- Y = −factor Y × overall height + **Offset Y**

Example: grid 94 × 26 mm, **In the middle**, no offset: the bottom left corner is 47 mm to the left of and 13 mm below the point.

The offsets are only added at this point. They do not change the number of shapes, also not in the mode **Fitting an area**.

### Step 6: the single shapes

`cell_centres()` walks through the grid row by row, from the bottom row upwards, in each row from left to right. For each shape it returns the bottom left corner of its place:

- X = grid corner X + column number × pitch X
- Y = grid corner Y + row number × pitch Y

Column and row numbers start at 0. The function name is historical; it returns corners, not centres.

The drawing code adds half the size of one shape to get the centre, and adds the position of the picked point in the sketch.

All positions are in the coordinates of the sketch that the point belongs to. The grid is therefore always parallel to the X and Y axes of that sketch.

## How each shape is drawn

| Shape | Case | Drawn as |
| --- | --- | --- |
| Rectangle | corners **Sharp** | Fusion's two-point rectangle, from the bottom left to the top right corner |
| Rectangle | **Rounded**, radius equal to half of both edges | one circle |
| Rectangle | **Rounded**, otherwise | up to 4 lines and 4 arcs |
| Rectangle | **Chamfered** | up to 4 lines for the edges and 4 lines for the cuts |
| Circle / ellipse | length equals depth | one circle |
| Circle / ellipse | otherwise | one ellipse; the longer of the two is given to Fusion as the main axis, because Fusion rejects the ellipse otherwise |
| Slot | length equals depth | one circle |
| Slot | otherwise | 2 lines and 2 half-round arcs; the arcs sit at the two ends of the longer direction, their radius is half of the shorter one |
| Polygon | always | one line per side |

Details:

- **Rounded or chamfered rectangle:** `corner_outline()` returns the outline as a list of lines and arcs, running counter-clockwise from the bottom edge. Each arc is given by three points: start, a point in the middle of the arc, end. When the radius or chamfer is exactly half of an edge, the straight piece on that side has no length and is left out.
- **Polygon:** the first corner points up. Without **Regular**, the corners are stretched so that the smallest box around them is exactly length × depth. With **Regular**, both directions are scaled by half of the smaller of length and depth. In both cases the polygon is centred on its own box, not on its circle. This matters for odd numbers of sides: a five-sided shape has a corner at the top but a flat bottom.
- **Connection of the curves:** the polygon is drawn as a chain. Each line starts at the end point of the line before, and the last one closes onto the start point of the first. The slot and the rounded or chamfered rectangle are drawn differently: each line and arc is created on its own from coordinates. Their ends lie at the same place, but they are not created as shared points. See [known limits](troubleshooting.md#known-limits).
- The add-in itself adds no dimensions and no constraints. Whether Fusion adds some of its own to the two-point rectangle is not decided by the add-in.

While the grid is drawn, the sketch is told not to recalculate after every single curve (`isComputeDeferred`). It recalculates once at the end. The setting is switched back in every case, also after an error.

## The checks

Order in which the checks run:

1. Exactly one sketch point is selected.
2. If the shape is a polygon: sides between 3 and 24.
3. Length greater than 0.
4. Depth greater than 0.
5. Neither gap negative.
6. Mode **Fitting an area**: both area values greater than 0; then at least one column and one row fit.
7. Mode **Columns and rows**: at least one column, at least one row.
8. Columns × rows at most 2000.
9. If the shape is a rectangle and the corners are not **Sharp**: radius / chamfer greater than 0, and at most half of the shorter edge. A value that is too large is refused, not silently reduced.

The first check that fails decides the message. The texts are listed in [troubleshooting.md](troubleshooting.md).

The **Result** line runs checks 3 to 9 only. A failed check 1 or 2 therefore disables **OK** without a text in the **Result** line.

## Texts and language

- Each language file is a list of keys and texts. The code only knows the keys.
- Places for values are written as `{0}`, `{1}` and so on in the texts and are filled in by the add-in.
- English is loaded first as a fallback. A key that is missing in the active language is taken from English. A key missing everywhere is shown as the key itself.
- How the language is chosen: see [settings.md](settings.md#language).
