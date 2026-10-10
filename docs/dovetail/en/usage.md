# Usage

All field names below are written exactly as they appear in the English dialog. Each field is explained in detail in
[settings.md](settings.md).

## Words used here

| Word | Meaning |
|---|---|
| Tooth | One dovetail, triangle or rectangle standing off the line |
| Pin | The tooth as part of the one workpiece |
| Pocket | The matching recess in the other workpiece |
| Tolerance | The gap between pin and pocket (the clearance) |
| Band | The closed outline the add-in draws. Its inside is exactly the gap. |
| Start point, end point | The two ends of a sketch line, in the order in which the line was drawn |

## Draw a joint on one line

1. Open a sketch or edit an existing one.
2. Draw a straight line where the two parts shall meet.
3. Click the line.
4. Click the **Dovetail** button. The dialog opens. The line is already entered under **Lines**.
   You can also start the command first and then click the line.
5. Set **Count**, **Shape**, **Width (base)**, **Depth** and **Tolerance**.
6. Watch the preview in the sketch.
7. Press **OK**.

Result:

- One closed band is drawn in the same sketch as the line.
- The original line becomes construction geometry (a dashed helper line), if
  **Turn the original line into construction geometry** is ticked. This happens only on OK, not in the preview.
- The add-in adds no dimensions and no constraints to the new lines.

If **OK** is greyed out and no preview is shown, the values do not fit. The dialog does not say why.
See [troubleshooting.md](troubleshooting.md#ok-is-greyed-out).

## Make two fitting parts from the band

1. Draw the outline of the whole piece. Let the joint line run across it, from edge to edge.
2. Run Dovetail on the joint line.
3. Extrude the outline into a solid body.
4. Extrude the band as a cut through that body.

Two bodies remain. They fit into each other with the gap you set under **Tolerance**.

Steps 3 and 4 are ordinary Fusion functions. The add-in itself only draws the band.

## Choose the shape

Use the list **Shape**:

| Entry | Result |
|---|---|
| **Trapezoid (dovetail)** | The tooth gets wider towards its tip. It hooks in and cannot be pulled straight out. |
| **Triangle** | The tooth runs to a point. It has no hook and can be pulled apart. |
| **Rectangle (box joint)** | Straight tooth, same width at base and tip. |

**Flank angle** is only active for **Trapezoid (dovetail)**. It sets how much the tooth widens. With 0 degrees the
trapezoid is the same as a rectangle. A negative angle makes the tooth narrower towards its tip.

## Several teeth on one line

1. Set **Count** to 2 or more. The field **Spacing (centre to centre)** becomes active.
2. Set **Spacing (centre to centre)**: the distance from the middle of one tooth to the middle of the next.

The group of teeth always sits symmetrically around the middle of the line:

| Count | Position of the teeth relative to the middle (spacing 30 mm) |
|---|---|
| 1 | 0 |
| 2 | −15 / +15 |
| 3 | −30 / 0 / +30 |
| 4 | −45 / −15 / +15 / +45 |
| 5 | −60 / −30 / 0 / +30 / +60 |

An odd count puts a tooth on the middle. An even count puts a gap there.

## Move the teeth along the line

Two ways:

- Type a value into **Offset**. A positive value moves the teeth towards the end point of the line, a negative value
  towards the start point. 0 means centred.
- Use the three buttons in the row **Move**:

  | Button | Effect |
  |---|---|
  | **Left (towards the start point)** | moves the teeth by one **Step size** towards the start point |
  | **Centre** | sets **Offset** back to 0 |
  | **Right (towards the end point)** | moves the teeth by one **Step size** towards the end point |

The buttons stop where the teeth would no longer fit on the line. With several lines the shortest line sets this
limit. A typed value is not corrected: if it is too large, OK is greyed out.

**Offset** starts at 0 every time the dialog opens.

## Choose which part gives up material

The gap has to come from somewhere. The list **The line is** decides:

| Entry | Pocket edge | Pin edge | Use it when |
|---|---|---|---|
| **Centre line - half the tolerance each side** | moves out by half the tolerance | moves in by half the tolerance | both parts shall stay equal |
| **Pocket edge - all the tolerance on the pin** | exactly on the drawn shape | moves in by the full tolerance | the part with the pockets must keep its exact size |
| **Pin edge - all the tolerance on the pocket** | moves out by the full tolerance | exactly on the drawn shape | the part with the pins must keep its exact size |

The gap between the parts is the full tolerance in all three cases.

Example with a tolerance of 0.25 mm:

| Entry | Pocket | Pin | Gap |
|---|---|---|---|
| Centre line | +0.125 mm | −0.125 mm | 0.25 mm |
| Pocket edge | 0 | −0.25 mm | 0.25 mm |
| Pin edge | +0.25 mm | 0 | 0.25 mm |

## Put the teeth on the other side

Tick **Flip direction**.

Without the tick, the teeth stand on the left side of the line when you look from its start point to its end point
(in the X/Y plane of the sketch). With the tick, they stand on the right side.

With several lines, each line follows its own direction. Lines drawn in opposite directions get their teeth on
opposite sides. **Flip direction** turns all of them over together.

## Several lines at once

1. Select several lines before you start the command. Or start the command and click the lines one after another.
   Up to 100 lines are possible.
2. Set the values once.
3. Press **OK**.

Every line gets its own joint from the same values. Each line is measured on its own and its teeth are centred on
its own middle. The lines may have different lengths.

The values must fit on every line. If one line is too short, nothing is drawn at all and OK is greyed out. Look at
the shortest line first; it runs out of room first.

Only straight sketch lines can be selected. Arcs, circles and splines cannot.

## Two identical parts: Mirror geometry

Tick **Mirror geometry**.

Half of the teeth then point to one side and half to the other. If you turn the band by 180 degrees around the
middle of the line, it lands on itself. Both parts of the cut are therefore identical. You can model one part and
make it twice; the second one is turned around.

The dialog sets three things for you, because each of them would break the symmetry:

| What | Why |
|---|---|
| **Count** is raised to the next even number | A tooth on the middle would have to point both ways at once. |
| **The line is** is set to the centre line and greyed out | Only there do both parts give up the same amount. |
| **Offset** is set to 0; **Offset**, **Step size** and **Move** are greyed out | A shifted group is no longer symmetric about the middle. |

When you remove the tick, the fields become active again. The values the dialog changed stay as they are.

With several lines, each line is mirrored about its own middle.

## Keep or convert the original line

The field **Turn the original line into construction geometry** is ticked by default.

- Ticked: the selected line becomes construction geometry on OK. It keeps its dimensions and constraints, but no
  longer divides the band into two areas.
- Not ticked: the line stays a normal line. It runs through the band and splits it into two areas (profiles).

A line that already is construction geometry is left as it is.

## Preview

While the dialog is open, the add-in draws the band as a preview after every change.

- The preview never changes the original line. Because of that, the preview shows the line still as a normal line.
- If the values do not fit, no preview is shown.

## Run the command again

Fusion can repeat the command with its own "repeat last command" function; the add-in allows that.
The dialog opens again with the values of your last successful run. See
[settings.md](settings.md#what-is-remembered).
