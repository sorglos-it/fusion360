# How it works

## Files

Everything the add-in needs lies in one folder, `Dovetail`:

| File | Purpose |
|---|---|
| `Dovetail.py` | The whole program: language, geometry, drawing, dialog, start and stop |
| `Dovetail.manifest` | Description for Fusion: name, author, version, supported systems, start with Fusion |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | All texts, one file per language |
| `resources/Dovetail/` | Toolbar icon in 16, 32 and 64 pixels |
| `resources/nudge_left/`, `nudge_center/`, `nudge_right/` | Icons of the three **Move** buttons |

The add-in reads only these files. It writes no files and opens no network connection.

## Start and stop

On start the add-in:

1. picks the language (see [settings.md](settings.md#language)),
2. registers the command with the name "Dovetail" plus the version from the manifest in brackets,
3. looks for a toolbar panel and puts the button there (see [installation.md](installation.md#first-start-in-fusion)).

On stop it removes the button and the command again.

## From the line to the band

### 1. A ruler along the line

For every selected line the add-in sets up its own measuring system:

- **s** runs along the line, from the start point (0) to the end point (the line length).
- **h** runs at a right angle to the line, to the side the teeth point to.

Without **Flip direction**, h points to the left when you look from the start point to the end point.
With **Flip direction**, h points to the right.

### 2. Where the teeth sit

The middle of the group is at: line length ÷ 2 + Offset.
The teeth are placed to both sides of it, each one **Spacing** apart from the next.

### 3. The nominal outline

The nominal outline is the shared edge the two parts would have with no gap at all. It is one open zigzag line:

1. it starts at the start point of the line,
2. runs along the line to the first tooth,
3. goes up one side of the tooth, across the tip, and down the other side,
4. continues along the line to the next tooth,
5. ends at the end point of the line.

The tip is one point for a triangle and two points for a trapezoid or rectangle.

With **Mirror geometry**, the first half of the teeth points to the opposite side (minus h), the second half to
the normal side (plus h).

### 4. Splitting the tolerance

Two copies of the nominal outline are made, each shifted sideways by a fixed distance (a parallel offset):

- the **pocket** contour is shifted to the tooth side. The pocket gets larger.
- the **pin** contour is shifted to the other side. The pin gets smaller.

**The line is** decides how far each one is shifted:

| Entry | Pocket shifted by | Pin shifted by |
|---|---|---|
| Centre line | ½ × Tolerance | ½ × Tolerance |
| Pocket edge | 0 (stays on the nominal outline) | Tolerance |
| Pin edge | Tolerance | 0 (stays on the nominal outline) |

The two shares always add up to the full tolerance. Because both contours are parallel copies of the same outline,
the gap between them is the same everywhere: at the base, on the sides and at the tip.

How the shift is done:

- Every straight piece is moved sideways by the distance.
- At each corner the two moved pieces are extended or shortened until they meet (a mitre corner).
- The two ends are moved straight sideways, so both contours begin at s = 0 and end at s = line length.

### 5. The closed band

The two contours are joined into one closed loop:

1. along the pocket contour from the start to the end of the line,
2. across to the pin contour at the end of the line,
3. back along the pin contour,
4. across to the starting point.

The inside of this loop is the gap itself. It is a band of exactly the tolerance that follows the tooth outline.
Cutting it out of one solid leaves two parts that fit.

### 6. Drawing

- The band is drawn as a chain of straight sketch lines. Each line starts at the end point of the previous one, and
  the last one closes back to the first. The outline is therefore connected.
- The lines go into the sketch the selected line belongs to.
- While drawing, the sketch is told not to recalculate after every single line. It recalculates once at the end.
- On OK, and only if the box is ticked, the original line is turned into construction geometry first. A normal line
  would run through the band and split it into two areas.
- The add-in adds no dimensions and no constraints.

## The checks

Before anything is drawn, the whole selection is calculated once. Only if every line passes, drawing starts.
A bad line at the end of the selection can therefore not leave half the sketch drawn.

The checks run in this order for each line:

| # | Check | Message key if it fails |
|---|---|---|
| 1 | The line has a length | `err.zero_length` |
| 2 | Width is greater than 0 | `err.width` |
| 3 | Depth is greater than 0 | `err.depth` |
| 4 | Tolerance is greater than 0 | `err.tolerance_zero` |
| 5 | Count is at least 1 | `err.count` |
| 6 | Mirror: count is even | `err.mirror_even` |
| 7 | Mirror: the centre line is chosen | `err.mirror_center` |
| 8 | Mirror: offset is 0 | `err.mirror_offset` |
| 9 | Trapezoid: flank angle is inside ±89 degrees | `err.angle_range` |
| 10 | Trapezoid: the tip keeps a width | `err.angle_negative` |
| 11 | Two or more teeth: spacing is greater than 0 | `err.spacing_positive` |
| 12 | Two or more teeth: spacing is at least the minimum | `err.spacing_too_small` |
| 13 | The teeth plus the end distance fit on the line | `err.offset_range` or `err.does_not_fit` |
| 14 | No mitre corner moves further than 12 × the shift distance | `err.miter_runaway` |
| 15 | Both contours start and end exactly at the line ends and stay between them | `err.does_not_fit` |
| 16 | No piece of a contour has shrunk to nothing | `err.tolerance_eats_tooth` |
| 17 | No contour crosses itself | `err.tolerance_eats_tooth` |
| 18 | A tooth height remains | `err.tolerance_eats_tooth` |
| 19 | The remaining tooth height is at least 5 % of the depth | `err.tolerance_vs_depth` |
| 20 | Twice the tolerance is smaller than the width | `err.tolerance_vs_width` |

With several lines, a failure is wrapped in `err.on_line`, which names the position of the line in the selection.

The texts of all messages are listed in [troubleshooting.md](troubleshooting.md).

### What the dialog does with a failed check

- While the dialog is open: the preview disappears and **OK** is greyed out. The message text is **not** shown.
- If the run itself fails after OK: a message box shows the text, and the run is reported to Fusion as failed so
  that Fusion undoes the lines already drawn. This undo was not confirmed inside Fusion.

## Units

| Where | Unit |
|---|---|
| Dialog fields for lengths | millimetres |
| Dialog field for the angle | degrees |
| Numbers in messages | millimetres, two decimals |
| Inside the program | centimetres and radians (Fusion's internal units) |

Fixed small values in the code:

| Value | Size | Use |
|---|---|---|
| Extra distance | 0.01 mm | added to the minimum spacing and to the distance from the line ends |
| Shortest piece | 0.00001 mm | a contour piece shorter than this counts as "no length" |
| Mitre limit | 12 × shift distance | beyond this a corner counts as running away |
| Largest flank angle | below 89 degrees | |

## Height is ignored

The add-in only reads the X and Y values of the line ends in the sketch and draws the band at height 0 of the
sketch. A line in a 3D sketch, or one that leaves the sketch plane, is treated as if it were flat.

## What changed in 1.1.0.0

Version 1.1.0.0 changed the geometry (first built as 1.0.0.1):

- Teeth keep the tolerance plus 0.01 mm away from the ends of the line. Right at the end the pocket contour used to
  run past the line and turn back, which gave a loop crossing itself. The largest offset is smaller by that amount.
- Two teeth need 0.01 mm more spacing. At exactly the old minimum a piece of the contour had no length.
- A contour that would cross itself is refused instead of drawn.
- A failed run is undone.

These changes were tested **offline only**, including 34,317 random valid contours, none of which crossed itself.
They are **not yet confirmed inside Fusion**.
