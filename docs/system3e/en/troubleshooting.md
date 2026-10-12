# Troubleshooting

Back to the [overview](index.md).

## Messages

These are all messages the add-in can show. The texts are quoted from the English language file. In other
languages the text is translated. Message boxes carry the title "SYSTEM 3E element".

### "Please choose an element."

| | |
| --- | --- |
| Cause | No entry is selected under **Element**. |
| What you see | Normally not the message itself: the **OK** button is greyed out instead. |
| What to do | Choose an entry under **Element**. If the list is empty, choose the **Family** again. |

### "Please open a design first."

| | |
| --- | --- |
| Cause | The active document is not a design, so there is nothing to place the element in. |
| What to do | Open or create a design and switch to the design workspace. Then start the command again. |

### "The element {0} could not be created:" followed by a reason

`{0}` is the name of the element. The second line is the reason Fusion gives.

| | |
| --- | --- |
| Cause | Fusion refused to build the body from the element's points and faces. |
| What to do | 1. Try another element to see whether only this one is affected. 2. Install the add-in again from a fresh ZIP; the file `blocks/blocks.json` may be damaged. 3. If it still fails, report the element name and the reason in the message. |
| Effect | Nothing is left behind. Fusion undoes the step. |

### "No suitable toolbar panel was found."

| | |
| --- | --- |
| Cause | When starting, the add-in did not find the **Create** panel of the solid tools. No button was added. |
| What to do | Update Fusion and start the add-in again. If the message stays, report your Fusion version. The add-in knows only this one panel. |

### "Error while creating the geometry:" followed by technical text

| | |
| --- | --- |
| Cause | An unexpected error after you pressed **OK**. The text below the first line is a technical report (a "traceback") that shows where it happened. |
| What to do | 1. Try again with another point or another element. 2. Stop the add-in and run it again. 3. If it stays, copy the whole text and report it. |
| Effect | Fusion undoes what was built so far. No half-finished component stays. |

### "Error while building the dialog:" followed by technical text

| | |
| --- | --- |
| Cause | The dialog could not be built. One reason visible in the code is a missing or unreadable file `blocks/blocks.json`: the dialog reads the element library when it opens. |
| What to do | Install the add-in again from the ZIP, so that the folder `blocks` is complete. See [installation.md](installation.md). |

### "Start-up failed:" followed by technical text

| | |
| --- | --- |
| Cause | An unexpected error while the add-in started. |
| What to do | 1. Check that the folder is unpacked correctly: `AddIns/System3E/System3E.py`. 2. Restart Fusion. 3. Install the add-in again. 4. If it stays, copy the text and report it. |

### "Shutdown failed:" followed by technical text

| | |
| --- | --- |
| Cause | An unexpected error while the add-in stopped and removed its button. |
| What to do | Restart Fusion. Your designs are not affected. |

## Other problems

| Problem | Cause | What to do |
| --- | --- | --- |
| **System3E** is not in Fusion's add-ins list. | The folder is in the wrong place or one level too deep. | Check that `AddIns/System3E/System3E.py` exists. See [installation.md](installation.md). |
| The button is missing. | The add-in is not running. | Open the add-ins dialog, select **System3E**, press **Run**. |
| The dialog is in English although Fusion uses another language. | Only German, English, Spanish, French and Italian exist. Other languages fall back to English. | – |
| The dialog is in the wrong language after changing Fusion's language. | The language is chosen when the add-in starts. | Stop the add-in and run it again, or restart Fusion. |
| The picture does not change when I choose another element. | The picture file `blocks/<id>.png` of that element is missing. The old picture stays. | Install the add-in again. |
| No preview of the element appears while the dialog is open. | An error happened during the preview. Preview errors are not shown. | Press **OK**. A real error is then shown as a message. |
| I cannot click a certain place. | Only sketch points, corners of bodies and construction points can be picked. Faces, edges and midpoints of edges cannot. | Create a sketch point or a construction point there, or use the offsets. |
| The element stands at the origin. | No point was selected. | Click a point for **Point**. |
| The element is turned the wrong way. | A positive **Rotation** turns counter-clockwise seen from above. | Type the angle with the other sign. |
| The offsets move the element in an unexpected direction. | Offsets run along the axes of the design, not along the turned element. | Use the axis that fits the direction in the design. |
| The point names are in another language than the dialog. | Point names are written when an element is first placed in a design and are kept. | Rename the points by hand if needed. |
| An older element has fewer than twelve points. | It was placed with an older version. | Place any element once more in that design. Every element gets its missing points. |
| The points lie beside the element, not on it. | The element was placed with a version before 1.1.0.1 away from the origin. | Place any element once more in that design. The points are made again in the right place. |
| A point is not exactly at half the width or at the underside. | The exact place is inside the material or in the air, so the point is shown on the surface next to it. | Nothing. Clicking it still places by the exact place. See [usage.md](usage.md). |
| After an update Fusion still shows the old version on the button. | Fusion runs the copy in its add-in folder, not the downloaded one. | Unpack the new ZIP over the old folder, then stop and run the add-in. See [installation.md](installation.md). |
| The dialog starts with the defaults again. | The remembered values last only until Fusion closes or the add-in stops. | – |
| A parts list shows the same element in several lines. | The elements were placed with version 0.2.0, which made a new component every time. Only the first of them is reused from now on. | Replace the old ones by newly placed elements. |

## Known limits

- **Left and right:** the left/right names of the corner and window elements were matched by eye against the
  manufacturer's catalogue cards. They are not confirmed.
- **`S0/2 200 P`:** this element is damaged in the manufacturer's 3D file. It is rebuilt from `S0/2 250 P`.
- **Vertical axis:** the add-in always treats the Z axis of the design as "up". It does not look at a different
  orientation setting in Fusion.
- **Top level only:** elements are always created in the top level of the design (the root component), not in the
  component that is active at the moment.
- **Linked designs:** an element inside a linked design is not reused. The add-in creates its own component.
- **No fit check:** the add-in does not check whether elements overlap, whether a joint fits or whether a wall
  is buildable.
- **One element per run:** there is no function for whole courses or walls.
- **Turning:** only about the vertical axis. Elements cannot be tilted in the dialog.
- **Shared body:** all copies of an element share one body. Changing one changes all.
- **Sizes:** the shapes come from the manufacturer's 3D file and are rounded to 0.1 mm. The four partition wall
  elements are plain blocks without profile.
- **No affiliation:** the add-in is not affiliated with SYSTEM 3E. It is no substitute for the manufacturer's
  planning documents.
