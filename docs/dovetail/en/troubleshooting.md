# Troubleshooting

## OK is greyed out

The dialog greys out **OK** and shows no preview when the values do not fit. **It does not say why.** The message
texts below exist in the add-in, but they are only shown in a message box if the run itself fails after OK.

Go through this list from top to bottom:

1. Is at least one line listed under **Lines**?
2. Are **Width (base)**, **Depth** and **Tolerance** all greater than 0?
3. Is **Tolerance** smaller than half of **Width (base)**?
4. Trapezoid: is **Flank angle** between −89 and 89 degrees? With a negative angle: is the tip still wider than 0?
5. Two or more teeth: is **Spacing (centre to centre)** large enough? See
   [settings.md](settings.md#spacing-centre-to-centre) for the formula.
6. Is the line long enough for all teeth? With several lines, check the shortest one first.
7. Did you type an **Offset**? Press the **Centre** button in the row **Move** to set it back to 0.
8. Triangle or very pointed tooth: reduce **Tolerance**, reduce **Depth** or increase **Width (base)**.
9. Narrow trapezoid tip with a large tolerance: reduce **Tolerance** or change **Flank angle**.

Tip: change one value at a time. The value you changed last is the first suspect.

## Messages about the values

All message boxes carry the title "Dovetail". `{0}`, `{1}` and `{2}` in the table stand for numbers or texts the
add-in fills in. Lengths in messages are in millimetres.

| Message | Cause | What to do |
|---|---|---|
| "Please select at least one sketch line." | The run was started with no line under **Lines**. | Click at least one straight sketch line. |
| "Line {0} of {1}: {2}" | Several lines are selected and one of them cannot take the values. {0} is the position of that line in the order you picked them, {1} the number of lines, {2} the actual message. | Read the message after the colon and look it up in this table. Change the values, or remove that line from the selection. |
| "The selected line has no length." | Start point and end point of the line lie on the same spot (seen flat in the sketch). | Pick another line or lengthen it. |
| "The width must be greater than 0." | **Width (base)** is 0 or negative. | Enter a width above 0. |
| "The depth must be greater than 0." | **Depth** is 0 or negative. | Enter a depth above 0. |
| "A closed band needs a tolerance greater than 0." | **Tolerance** is 0 or negative. The band consists of the gap; without a gap there is no band. | Enter a tolerance above 0. |
| "Mirrored geometry needs an even number of teeth." | **Mirror geometry** is on and **Count** is odd. The dialog normally corrects this itself. | Set an even count. |
| "Mirrored geometry only works with the centre line, where both parts give up the same amount." | **Mirror geometry** is on and **The line is** is not the centre line. The dialog normally corrects this itself. | Choose "Centre line - half the tolerance each side" or switch mirroring off. |
| "Mirrored geometry needs the offset at 0, otherwise the pattern is no longer symmetric about the midpoint of the line." | **Mirror geometry** is on and **Offset** is not 0. The dialog normally corrects this itself. | Set the offset to 0 or switch mirroring off. |
| "At least one dovetail is required." | **Count** is below 1. The dialog field does not allow this. | Set a count of 1 or more. |
| "The flank angle must be between -89 and 89 degrees." | Trapezoid: **Flank angle** is 89 degrees or more, or −89 degrees or less. | Enter an angle inside this range. |
| "The flank angle is too steeply negative - the tooth tapers away to nothing." | Trapezoid with a negative angle: the sides meet before the tip is reached. | Use a less negative angle, less depth or more width. |
| "The spacing must be greater than 0." | Two or more teeth and **Spacing (centre to centre)** is 0 or negative. | Enter a spacing above 0. |
| "The spacing is too small - the dovetails would overlap. At least {0} mm is required." | Two or more teeth stand too close. {0} is the minimum spacing for your values. | Enter at least the spacing named, or reduce width, flank angle or tolerance. |
| "The offset pushes the teeth past the end of the line. At most +/- {0} mm is possible." | **Offset** is larger than the line allows. {0} is the largest possible offset. | Reduce the offset to the value named, or press **Centre**. |
| "The teeth are wider than the selected line ({0} mm). Reduce the count, the width or the spacing." | The teeth plus the distance to the line ends do not fit on the line. {0} is the length of the line. The same text appears if a contour would run past an end of the line. | Reduce **Count**, **Width (base)** or **Spacing (centre to centre)**, or use a longer line. |
| "The mating contour runs away at a sharp corner. Make the tooth flatter (less depth / more width) or reduce the tolerance." | At a very sharp corner the shifted contour would shoot far away from the tooth (more than 12 times the shift distance). | Less depth, more width, or less tolerance. |
| "The tolerance eats the whole tooth. Reduce the tolerance or increase the depth." | After taking off the tolerance, nothing of the tooth remains, or a piece of the contour shrinks to nothing, or the contour would cross itself. | Reduce **Tolerance** or increase **Depth**. With a narrow trapezoid tip, also try a larger width or another flank angle. |
| "The tolerance is too large compared to the depth." | Less than 5 % of **Depth** remains as tooth height. | Reduce **Tolerance** or increase **Depth**. |
| "The tolerance is too large compared to the width." | Twice the **Tolerance** is as large as **Width (base)** or larger. | Reduce **Tolerance** or increase **Width (base)**. |
| "The contour is degenerate." | A safety net: the outline has too few points, or the two contours do not have the same number of points. With the other checks in place this should not appear in normal use. | Change the values slightly. If it appears again, report it with the values you used. |

## Messages about the program

These messages contain a technical error report (a "traceback") in place of `{0}`. They mean an unexpected error,
not a wrong value.

| Message | When | What to do |
|---|---|---|
| "No suitable toolbar panel was found." | On start. None of the three toolbar places exists in this Fusion (see [installation.md](installation.md#first-start-in-fusion)). The button is not created. | Update Fusion. If the message stays, report it together with your Fusion version. |
| "Error while creating the geometry: {0}" | After OK, an unexpected error occurred while drawing. The run is reported to Fusion as failed. | Check the sketch; use Undo if lines were left behind. Try again. If it repeats, report the full text. |
| "Error while building the dialog: {0}" | The dialog could not be built when the button was clicked. | Stop and start the add-in. Check that the folders `lang` and `resources` are complete. If it repeats, report the full text. |
| "Start-up failed: {0}" | The add-in could not start. | Check that the folder is unpacked completely and named `Dovetail`. Reinstall it. If it repeats, report the full text. |
| "Shutdown failed: {0}" | The add-in could not be stopped cleanly. | Restart Fusion. |

Reports: <https://github.com/sorglos-it/fusion360/issues>

## Other problems

| Problem | Cause | What to do |
|---|---|---|
| No button after installing | The add-in is not running, or the folder is nested one level too deep | Follow [installation.md](installation.md) again; check that `AddIns/Dovetail/Dovetail.py` exists |
| A line cannot be clicked in the dialog | Only straight sketch lines are accepted | Use a straight line; arcs, circles and splines are not supported |
| The band shows two areas instead of one | The original line still runs through the band as a normal line | Tick **Turn the original line into construction geometry**, or turn the line into construction geometry by hand |
| The preview still shows the original line as a normal line | The preview never changes the original line | Nothing; the line is converted on OK |
| Teeth are on the wrong side | The side depends on the direction in which the line was drawn | Tick **Flip direction** |
| Some lines have teeth on one side, some on the other | The lines were drawn in opposite directions | Run the command separately for the two groups, once with and once without **Flip direction** |
| The **Move** buttons do nothing | **Step size** is 0, or the limit is reached, or **Mirror geometry** is on | Set a step size, or check the room on the line |
| **Offset**, **The line is**, **Step size** are greyed out | **Mirror geometry** is ticked | Remove the tick |
| The wrong language is shown | The language is chosen when the add-in starts; languages other than the five supported fall back to English | See [settings.md](settings.md#language) |
| The values are back to the defaults | They are remembered only while Fusion is running | Enter them again |

## Known limits

- **No reason is shown when OK is greyed out.** The message texts are only shown if the run itself fails.
- **Height is ignored.** Lines in a 3D sketch or lines off the sketch plane are handled as if they were flat.
- **Straight lines only.** Arcs, circles and splines cannot be selected.
- **One set of values for all lines.** With several lines, every line gets the same values. There is no setting per
  line.
- **At most 100 lines and 500 teeth per line.**
- **A triangle does not hook in.** Only the trapezoid with a positive flank angle holds against pulling apart.
- **The tolerance is a gap, nothing more.** The add-in does not compensate for effects of the manufacturing process.
- **Not confirmed inside Fusion:** the geometry changes of version 1.1.0.0 (distance from the line ends, larger
  minimum spacing, refusing contours that cross themselves, undo after a failed run). They were tested offline only.
