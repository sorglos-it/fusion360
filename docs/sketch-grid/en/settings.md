# Settings

The add-in has no settings file and no settings page. Everything is set in the dialog of the command **Sketch Grid**. Field names are written exactly as in the English dialog.

## Dialog fields

Lengths are entered in millimetres by default (the fields are created with the unit `mm`). "No limit" means: the add-in itself checks nothing more.

| Field | Meaning | Default | Allowed values |
| --- | --- | --- | --- |
| **Point** | The sketch point the grid is built around. | The sketch point selected before the dialog opened, otherwise empty | Exactly one sketch point. Other objects cannot be picked. |
| **Count from** | How the number of shapes is set. | Columns and rows | **Columns and rows**, **Fitting an area** |
| **Shape** | The shape that is repeated. | Rectangle | **Rectangle**, **Circle / ellipse**, **Slot**, **Polygon** |
| **Sides** | Number of sides of the polygon. | 6 | Whole number, 3 to 24 |
| **Regular** | Tick box. On: all sides of the polygon are equally long. Off: the polygon is stretched to length × depth. | off | on, off |
| **Corners** | What happens to the four corners of the rectangle. | Sharp | **Sharp**, **Rounded**, **Chamfered** |
| **Radius / chamfer** | Radius of the rounding, or length of the cut along each edge. | 1 mm | Greater than 0, at most half of the shorter of length and depth |
| **Length (X)** | Size of one shape in X. | 10 mm | Greater than 0, no upper limit |
| **Depth (Y)** | Size of one shape in Y. | 5 mm | Greater than 0, no upper limit |
| **Gap X** | Free space between neighbours in X. | 2 mm | 0 or greater, no upper limit |
| **Gap Y** | Free space between neighbours in Y. | 2 mm | 0 or greater, no upper limit |
| **Columns** | Number of shapes side by side. | 8 | Whole number, 1 to 2000 |
| **Rows** | Number of shapes above each other. | 4 | Whole number, 1 to 2000 |
| **Area width** | Width of the area to fill. | 100 mm | Greater than 0, and large enough for one shape |
| **Area height** | Height of the area to fill. | 40 mm | Greater than 0, and large enough for one shape |
| **Point sits in the grid** | Where the picked point is inside the finished grid. | In the middle | Nine entries, see below |
| **Offset X** | Moves the whole grid in X, on top of the position chosen above. | 0 mm | Any value, also negative |
| **Offset Y** | Moves the whole grid in Y. | 0 mm | Any value, also negative |
| **Result** | Shows the number of shapes and the overall size, or a message. | – | Read-only |

One more limit applies to the whole grid: columns × rows must not be more than **2000**. This holds in both counting modes.

## When a field is shown

| Field | Shown when |
| --- | --- |
| **Sides**, **Regular** | **Shape** is **Polygon** |
| **Corners** | **Shape** is **Rectangle** |
| **Radius / chamfer** | **Shape** is **Rectangle** and **Corners** is not **Sharp** |
| **Columns**, **Rows** | **Count from** is **Columns and rows** |
| **Area width**, **Area height** | **Count from** is **Fitting an area** |
| all other fields | always |

A hidden field keeps its value. A hidden value is not used and not checked.

## Point sits in the grid

| Entry | The point is at |
| --- | --- |
| **In the middle** | the centre of the grid |
| **Bottom left** | the bottom left corner |
| **Bottom right** | the bottom right corner |
| **Top left** | the top left corner |
| **Top right** | the top right corner |
| **Bottom centre** | the middle of the bottom edge |
| **Top centre** | the middle of the top edge |
| **Left centre** | the middle of the left edge |
| **Right centre** | the middle of the right edge |

"Grid" here means the smallest rectangle around all shapes. Left and right are along the X axis of the sketch, bottom and top along its Y axis.

## Help texts in the dialog

Three help texts (tooltips) are attached to fields:

| Field | Text |
| --- | --- |
| **Regular** | "Keeps the polygon equilateral instead of stretching it to length x depth. The smaller of the two then sets its size, and the pitch follows the actual shape - so the gap you set is the gap you get either way." |
| **Corners**, **Radius / chamfer** | "Takes the four right-angled corners off the rectangle, either as a fillet arc or as a straight chamfer. At most half of the shorter edge - a radius of exactly that turns the rectangle into a slot, a chamfer of it into a diamond. The bounding box is unchanged, so the count, the pitch and the gap stay as they are." |
| **Offset X**, **Offset Y** | "Shifts the whole grid away from the picked point, on top of whatever the anchor already decided. Use it to hold a margin from an edge without moving the point itself. Negative values go the other way." |

Note on the second text: a chamfer of exactly half the shorter edge gives a diamond only when length and depth are equal. With unequal values it gives a six-sided shape.

The button itself has the help text: "Builds a grid of shapes around a sketch point. Fixed number of columns and rows, or as many as fit into an area."

## What is remembered

- When you finish a grid with **OK**, the add-in remembers all values except the point: counting mode, shape, sides, Regular, corners, radius / chamfer, length, depth, both gaps, columns, rows, area width, area height, position of the point, both offsets.
- The next time the dialog opens, these values are filled in.
- Values are **not** remembered when you cancel the dialog, or when OK ends with an error message.
- The values are kept in memory only, never on disk. They last until the add-in is stopped or Fusion is closed. After that the defaults from the table above apply again.
- The values are the same for all documents that are open in this Fusion session.

## Language

The add-in has five languages: German, English, Spanish, French, Italian.

How the language is chosen, in this order:

1. The language set in Fusion under **Preferences → General → User Language**, if it is one of the five.
2. Otherwise the language of the operating system, if it is one of the five. (The add-in reads the environment variables `LANG`, `LANGUAGE`, `LC_ALL`, then the system locale.)
3. Otherwise English.

More details:

- There is no language switch in the add-in.
- The language is read once, when the add-in starts. After changing the language in Fusion, stop and start the add-in, or restart Fusion.
- If a text is missing in one language, the English text is shown instead.
- The **Result** line always shows millimetres, in every language.
