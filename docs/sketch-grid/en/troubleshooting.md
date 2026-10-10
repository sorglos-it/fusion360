# Troubleshooting

All texts are quoted from the English language file. `{0}` and `{1}` stand for values that the add-in fills in.

## Where messages appear

| Place | When |
| --- | --- |
| **Result** line in the dialog | A value is not allowed. **OK** is disabled at the same time. |
| Disabled **OK** without a text | No sketch point is selected (see first row below). |
| Message window with the title **Sketch Grid** | A check fails only at the moment **OK** is pressed, or something unexpected went wrong. |

## Messages about your input

| Message | Cause | What to do |
| --- | --- | --- |
| "Please select exactly one sketch point." | **Point** is empty, or the selected object is not a sketch point. This text is normally not shown; **OK** is just disabled. | Click **Point** and pick one sketch point: the sketch origin or a point you placed. Points on bodies cannot be picked. |
| "The length must be greater than 0." | **Length (X)** is 0 or negative. | Enter a value above 0. |
| "The depth must be greater than 0." | **Depth (Y)** is 0 or negative. | Enter a value above 0. |
| "The gap must not be negative." | **Gap X** or **Gap Y** is below 0. | Enter 0 or more. Overlapping shapes are not possible. |
| "At least one column is required." | **Columns** is below 1. | Enter 1 or more. The field itself only accepts 1 to 2000, so this message should not normally appear. |
| "At least one row is required." | **Rows** is below 1. | Enter 1 or more. The field itself only accepts 1 to 2000, so this message should not normally appear. |
| "The area must be greater than 0 in both directions." | Mode **Fitting an area**: **Area width** or **Area height** is 0 or negative. | Enter values above 0 in both fields. |
| "Not even one shape fits into that area. It needs at least {0} × {1} mm." | Mode **Fitting an area**: the area is smaller than one shape. The two numbers are the size of one shape. | Make **Area width** and **Area height** at least as large as the numbers in the message, or make the shape smaller. |
| "A polygon needs between {0} and {1} sides." | **Sides** is outside 3 to 24. | Enter 3 to 24. The field itself only accepts this range, so this message should not normally appear. |
| "The radius / chamfer must be greater than 0." | **Corners** is **Rounded** or **Chamfered**, and **Radius / chamfer** is 0 or negative. | Enter a value above 0, or set **Corners** to **Sharp**. |
| "The radius / chamfer can be at most {0} mm, half of the shorter edge." | **Radius / chamfer** is larger than half of the shorter of **Length (X)** and **Depth (Y)**. The number is the largest allowed value. | Enter at most the value from the message, or make the rectangle larger. |
| "That would be {0} shapes. At most {1} are allowed - more would lock Fusion up." | Columns × rows is more than 2000. The first number is what your values would give. | Use fewer columns or rows. In the mode **Fitting an area**: a smaller area, larger shapes or larger gaps. For more shapes, draw several grids. |

If several values are wrong, only the first problem is shown. Fix it, then the next one appears.

## Messages about the add-in itself

These appear in a message window. `{0}` is replaced by a technical error report (a Python traceback).

| Message | Cause | What to do |
| --- | --- | --- |
| "No suitable toolbar panel was found." | On start, the add-in found neither the CREATE panel of the sketch toolbar nor the CREATE panel of the SOLID tab. No button is added. | Switch to the **Design** workspace, then stop and run the add-in again. If it stays, report it with your Fusion version. |
| "Error while creating the geometry: {0}" | Something unexpected failed while drawing after **OK**. | Try again. If it stays, report it with the full text. |
| "Error while building the dialog: {0}" | Something unexpected failed while the dialog was built. | Stop and run the add-in again. If it stays, report it with the full text. |
| "Start-up failed: {0}" | Something unexpected failed while the add-in started. | Check that the folder is complete and still named `SketchGrid` (see [installation.md](installation.md)). Run it again. |
| "Shutdown failed: {0}" | Something unexpected failed while the add-in stopped. | Restart Fusion. |

Reports go to <https://github.com/sorglos-it/fusion360/issues>.

## Other problems

| Problem | Cause | What to do |
| --- | --- | --- |
| **OK** is grey and **Result** shows a normal result | No point is selected. | Pick a sketch point in **Point**. |
| The point clicked before is not in the dialog | The point could not be taken over. Since version 1.1.0.0 the dialog keeps working in this case (tested offline only, not inside Fusion). | Pick the point in the dialog. |
| No preview while typing | A value is not allowed at that moment. The preview stays empty without a message. | Read the **Result** line and correct the value. |
| The button is missing | The add-in is not running, or no panel was found. | Open **Utilities → ADD-INS → Add-Ins**, select **SketchGrid**, press **Run**. |
| The button shows an old version number | The old add-in is still in memory. | Stop the add-in, replace the folder, run it again. |
| The dialog is in English although Fusion is set to another language | Only German, English, Spanish, French and Italian exist. Or the language was changed while the add-in was running. | Stop and run the add-in again. See [settings.md](settings.md#language). |
| A text appears as a key such as `in.point` | The language files are missing or damaged. | Install the add-in again from the ZIP. |
| The grid does not fill the area | Only complete shapes are drawn. | This is intended. See [usage.md](usage.md#fitting-an-area). |
| A regular polygon is much smaller than length × depth | With **Regular**, the smaller of length and depth sets the size. | Use similar values for length and depth, or untick **Regular**. |
| The dialog starts with the standard values again | Remembered values last only until the add-in stops or Fusion closes. | Enter them again. |

## Known limits

Not confirmed inside Fusion (found in a code review):

- **Slots and rectangles with rounded or chamfered corners** are drawn as separate lines and arcs. Their ends lie on the same spot, but they may not stay connected when you drag a part of the shape. Polygons and sharp rectangles are not affected in this way.
- **The limit of 2000 counts shapes, not curves.** One polygon with 24 sides is 24 lines. A large grid of polygons, slots or cut rectangles can therefore be slow although it is within the limit.

From the code:

- Only sketch points can be picked. Corners of bodies or points on edges cannot.
- The grid is always parallel to the X and Y axes of the sketch. It cannot be rotated in the dialog.
- The polygon always has one corner pointing up. The dialog has no field to turn it.
- Only the rectangle can have rounded or chamfered corners.
- Gaps cannot be negative. Shapes cannot overlap.
- The shapes are plain sketch geometry. Changing a value later does not update an existing grid.
- The add-in adds no dimensions and no constraints. The grid is not tied to the point after it is drawn.
- The remembered values are lost when the add-in stops or Fusion closes.
- In the mode **Fitting an area**, the empty rest is only centred when **Point sits in the grid** is **In the middle** (or a "centre" entry for that one direction).
