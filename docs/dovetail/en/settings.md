# Settings

The add-in has no settings file and no settings page. Everything is set in the dialog of the command.
The fields are listed in the order in which the dialog shows them.

## Dialog fields

| Field | Meaning | Default | Allowed values |
|---|---|---|---|
| **Lines** | The sketch lines that get a joint. Prompt text: "Select one or more sketch lines". | the lines selected before the command was started | 1 to 100 straight sketch lines |
| **Count** | Number of teeth per line | 1 | whole number, 1 to 500 |
| **Mirror geometry** | Makes both parts identical, see [usage.md](usage.md#two-identical-parts-mirror-geometry) | off | on / off |
| **Shape** | Shape of the tooth | Trapezoid (dovetail) | Trapezoid (dovetail), Triangle, Rectangle (box joint) |
| **Width (base)** | Width of the tooth where it meets the line | 10 mm | greater than 0, and greater than twice the tolerance |
| **Depth** | How far the tooth stands off the line | 6 mm | greater than 0 |
| **Flank angle** | Trapezoid only: how much each side of the tooth leans outwards | 15 deg | more than −89 and less than 89 degrees; see below |
| **Spacing (centre to centre)** | Distance from the middle of one tooth to the middle of the next. Only used with 2 or more teeth. | 20 mm | greater than 0 and at least the minimum spacing, see below |
| **Offset** | Shift of the whole group of teeth along the line. Positive: towards the end point. | 0 mm, every time | between minus and plus the largest offset, see below |
| **Step size** | How far one click on a **Move** button shifts the teeth | 1 mm | not checked by the add-in, see below |
| **Move** | Three buttons: **Left (towards the start point)**, **Centre**, **Right (towards the end point)** | – | – |
| **Tolerance** | Gap between the two parts | 0.25 mm | greater than 0; further limits below |
| **The line is** | Which part gives up material for the gap | Centre line - half the tolerance each side | the three entries listed below |
| **Flip direction** | Puts the teeth on the other side of the line | off | on / off |
| **Turn the original line into construction geometry** | Converts the selected line into a helper line on OK | on | on / off |

Entries of **The line is**:

| Entry | Pocket grows by | Pin shrinks by |
|---|---|---|
| **Centre line - half the tolerance each side** | half the tolerance | half the tolerance |
| **Pocket edge - all the tolerance on the pin** | nothing | the full tolerance |
| **Pin edge - all the tolerance on the pocket** | the full tolerance | nothing |

## Fields that are greyed out

| Field | Greyed out when |
|---|---|
| **Flank angle** | **Shape** is not Trapezoid (dovetail). The value is then ignored. |
| **Spacing (centre to centre)** | **Count** is 1. The value is then ignored. |
| **The line is**, **Offset**, **Step size**, **Move** | **Mirror geometry** is ticked |

## Limits in detail

All limits come from the code. Lengths below are in millimetres.

"Half tip width" is used in several limits. It depends on the shape:

| Shape | Half tip width |
|---|---|
| Rectangle (box joint) | Width ÷ 2 |
| Triangle | 0 |
| Trapezoid (dovetail) | Width ÷ 2 + Depth × tan(Flank angle) |

"Widest half" is the larger of Width ÷ 2 and the half tip width.

### Flank angle

- Must be more than −89 and less than 89 degrees. Exactly 89 or −89 is refused.
- With a negative angle the tip gets narrower. The half tip width must stay above 0. Otherwise the tooth would
  taper away to nothing and is refused.
- 0 degrees gives a rectangle.

### Spacing (centre to centre)

Only checked with 2 or more teeth.

Minimum spacing = 2 × widest half + 2 × Tolerance + 0.01 mm

Example with the defaults (Width 10 mm, Depth 6 mm, Flank angle 15 deg, Tolerance 0.25 mm):
the half tip width is about 6.61 mm, so the minimum spacing is about 13.73 mm.

### Room on the line

The teeth must keep a distance from both ends of the line: the tolerance plus 0.01 mm.

Length needed = (Count − 1) × Spacing + 2 × widest half + 2 × (Tolerance + 0.01 mm)

Example with the defaults and one tooth: about 13.74 mm of line are needed.

### Offset

Largest offset = Line length ÷ 2 − ( (Count − 1) ÷ 2 × Spacing + widest half + Tolerance + 0.01 mm )

- The offset may lie between minus and plus this value.
- The **Move** buttons stop at this value. With several lines the shortest line decides.
- A typed offset is not corrected. If it is too large, OK is greyed out.
- With **Mirror geometry** the offset must be 0.

### Tolerance

- Must be greater than 0. The band consists of the gap; with 0 there is no band.
- Twice the tolerance must be smaller than **Width (base)**.
- After the tolerance is taken off, at least 5 % of **Depth** must remain as tooth height. This mainly matters for
  pointed teeth, where the tip loses more height than the tolerance.
- The band must not cross itself and none of its pieces may shrink to nothing. This can happen with narrow trapezoid
  tips and a large tolerance.
- At a sharp corner the offset corner must not move away further than 12 times the offset distance.

### Count

- 1 to 500.
- With **Mirror geometry** the count must be even. The dialog raises an odd count by 1.

### Step size

The add-in does not check this value. From the code: with 0 the **Move** buttons do nothing; a negative value
reverses the direction of the left and right buttons.

### Lines

- Only straight sketch lines can be picked.
- At least 1, at most 100.
- A line must have a length greater than 0.

## Units

- Length fields are shown in millimetres, the angle in degrees.
- Numbers inside error messages are always in millimetres with two decimals.
- Inside, the add-in calculates in centimetres and radians, the units Fusion uses internally.

## What is remembered

The add-in remembers the values of the last run that was finished with **OK** and succeeded.

| Remembered | Not remembered |
|---|---|
| Count | Lines |
| Mirror geometry | Offset (always starts at 0) |
| Shape | |
| Width (base) | |
| Depth | |
| Flank angle | |
| Spacing (centre to centre) | |
| Step size | |
| Tolerance | |
| The line is | |
| Flip direction | |
| Turn the original line into construction geometry | |

For how long:

- The values are kept in memory only. Nothing is written to disk.
- They last for the running Fusion session. After Fusion is closed, the defaults from the table above apply again.
- Closing the dialog with Cancel does not change the remembered values.

The offset is left out on purpose: it belongs to the line at hand, not to the settings.

## Language

The add-in has texts in five languages: German, English, Spanish, French, Italian.

The language is chosen once, when the add-in starts:

1. The language set in Fusion's preferences (user language) is used if it is one of the five.
2. If not, the add-in looks at the environment variables `LANG`, `LANGUAGE` and `LC_ALL`, in this order.
3. If that gives nothing, it looks at the language of the operating system.
4. If that gives nothing either, English is used.

There is no language switch in the dialog. After changing the language in Fusion, the add-in has to be started
again (restarting Fusion does that).

If a single text is missing in a language file, the English text is shown instead.
