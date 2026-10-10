# Settings

Back to the [overview](index.md).

The add-in has no settings page and no settings file. Everything you can set is in the dialog of the command
**SYSTEM 3E element**.

## The fields of the dialog

| Field | Meaning | Default | Allowed values |
| --- | --- | --- | --- |
| **Point** | The place for the element. | Empty, or the point you had selected before you pressed the button. | Nothing or exactly one point: a sketch point, a corner of a body, or a construction point. Nothing means the origin of the design. |
| **Family** | The group of elements shown under **Element**. | Basic | Starter, Basic, Complementary, Lintel, Window framing, Top, Corner, Partition wall |
| **Element** | The element to place, with its size in mm (length x width x height). | S1 WP | The elements of the chosen family. See the lists in [usage.md](usage.md). |
| (picture) | Shows the chosen element. Cannot be changed. | Picture of the chosen element | – |
| **Placed by** | Which spot of the element lands on the point. | Bottom corner, front right | 15 entries: three corners and the twelve points. See below. |
| **Rotation** | Turns the element about the vertical axis (Z) around the spot chosen under **Placed by**. | 0 degrees | Any angle. Positive is counter-clockwise seen from above. |
| **Offset X** | Moves the element along the X axis of the design. | 0 mm | Any length, also negative |
| **Offset Y** | Moves the element along the Y axis of the design. | 0 mm | Any length, also negative |
| **Offset Z** | Moves the element along the Z axis of the design. | 0 mm | Any length, also negative |

The add-in sets no upper or lower limit for the rotation and the offsets.

### The entries under "Placed by"

In this order:

1. Bottom corner, front right
2. Top corner, front right
3. Top corner, front left
4. bottom front
5. bottom middle
6. bottom back
7. top front
8. top middle
9. top back
10. top middle right
11. top middle left
12. bottom middle right
13. bottom middle left
14. middle right, 50 mm up
15. middle left, 50 mm up

What each entry means is explained in [usage.md](usage.md).

State: **Placed by** and the three offsets have been used inside Fusion by the author.

## What is remembered

After you press **OK** and the element was created, the add-in remembers these values for the next time:

- **Family**
- **Element**
- **Placed by**
- **Rotation**
- **Offset X**, **Offset Y**, **Offset Z**

Not remembered: the **Point**.

| Question | Answer |
| --- | --- |
| For how long? | Until Fusion is closed or the add-in is stopped. The values live only in memory. |
| Are they saved to a file? | No. |
| Are they saved in the design? | No. |
| What if I cancel the dialog? | Nothing is remembered. The values of the last successful placement stay. |
| What after a restart? | The defaults from the table above apply again. |

## Language

The add-in has its texts in five languages: German, English, Spanish, French and Italian.

You cannot choose the language in the add-in. It is chosen when the add-in starts:

1. The add-in asks Fusion for the language set in Fusion's preferences. If it is one of the five, it is used.
2. Otherwise it looks at the language settings of the operating system (the environment variables `LANG`,
   `LANGUAGE`, `LC_ALL`, then the system locale).
3. If none of these gives one of the five languages, English is used.

More details:

- To change the language, change the language in Fusion's preferences and start the add-in again.
- If a text is missing in a language, the English text is shown instead.
- Names of elements (`S1 WP`) and of components (`SYSTEM 3E S1 WP`) are not translated.
- The names of the twelve points are written into the design when an element is first placed. They keep that
  language, even if the add-in later runs in another language.

## Fixed values that cannot be changed in the dialog

| Value | Setting |
| --- | --- |
| Place of the button | Design workspace, **Create** panel of the solid tools |
| Start with Fusion | Yes (`runOnStartup` in the manifest file) |
| Points 50 mm above the underside | Fixed at 50 mm |
