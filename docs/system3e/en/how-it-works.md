# How it works

Back to the [overview](index.md).

## The files of the add-in

The installed folder `System3E` contains:

| File or folder | Purpose |
| --- | --- |
| `System3E.py` | The command: dialog, placing, points |
| `system3e_core.py` | General helpers: language, toolbar button, error messages, version |
| `System3E.manifest` | Tells Fusion the name, author, version and that the add-in starts with Fusion |
| `lang/de.xml`, `en.xml`, `es.xml`, `fr.xml`, `it.xml` | All texts, one file per language |
| `blocks/blocks.json` | The element library: the shape of all 74 elements |
| `blocks/<id>.png` | One preview picture per element, 74 in total |
| `resources/System3E/16x16.png`, `32x32.png`, `64x64.png` | The icon of the button |

The add-in reads only these files. It writes no files and opens no network connection.

## Start and stop

When the add-in starts:

1. It detects the language (see [settings.md](settings.md)) and loads the texts.
2. It removes a leftover button definition of an earlier run, if there is one.
3. It creates the button **SYSTEM 3E element**. The version from the manifest is added in brackets.
4. It looks for the **Create** panel of the solid tools in the design workspace and puts the button there.
   If the panel is not found, it shows a message and adds no button.

When the add-in stops, it removes the button again.

## The element library

`blocks/blocks.json` is one text file in JSON format. It holds:

- `unit`: always `mm`. All lengths in the file are millimetres.
- `blocks`: a list of 74 elements in catalogue order.

Each element has these entries:

| Entry | Content | Example |
| --- | --- | --- |
| `id` | Short name for files, lower case | `s1-wp` |
| `name` | Catalogue name | `S1 WP` |
| `family` | One of `starter`, `basic`, `complementary`, `lintel`, `window`, `top`, `corner`, `partition` | `basic` |
| `size` | Length, width, height in whole mm | `[707, 352, 300]` |
| `stack` | Height at which the next course stands, mm | `250.0` |
| `points` | The corner points of the shape, each as x, y, z in mm | `[0.0, 271.0, 200.0]` |
| `faces` | The flat faces. Each has a direction (`normal`) and one or more outlines (`loops`). | – |

An outline is a list of numbers. Each number names one of the `points`. The first outline of a face is its outer
border. Further outlines are holes in the face.

Every element lies with its lowest corner at 0, 0, 0. Its length runs along x, its width (the wall thickness)
along y, its height along z.

The library is read once, the first time the dialog opens. The preview picture of an element is the file
`blocks/<id>.png`.

## How a body is built

The elements are not stored as Fusion files. The add-in builds each body from the points and faces:

1. Every point of the element becomes a corner of the body.
2. Every face becomes a flat face. Its position comes from its first point and its direction.
3. Every outline becomes a closed chain of straight edges.
4. Each edge is defined once and used by its two neighbouring faces, in opposite directions. This makes the
   body closed (a solid).
5. Fusion checks the result fully and creates the body. If Fusion refuses it, the add-in shows the message
   "The element {0} could not be created:" with Fusion's reason.

All faces are flat and all edges are straight. There are no curved surfaces.

## Components and reuse

When you press **OK**:

1. The add-in goes through every element already in the design. Points that are missing are added. Points that
   are not where they belong are taken away and made again. So elements placed by an older version are brought
   up to date.
2. The add-in searches the design for a component of this element.
   - It looks for an invisible mark (a Fusion attribute, group `System3E`, name `block`) with the element's `id`.
   - Elements placed before the mark existed are found by the name `SYSTEM 3E <name>`.
   - Components without a body and components of a linked design are skipped.
3. **Found:** the add-in inserts another copy of that component at the new place.
4. **Not found:** the add-in builds the body, creates a new component named `SYSTEM 3E <name>` in the top level
   of the design, marks it, puts the body named `<name>` into it and adds the twelve points.

Because equal elements are copies of one component, a parts list counts them together.

In a design with timeline (Fusion calls this a parametric design) a ready-made body must arrive inside a
"base feature". The add-in creates one, puts the body and the points into it and closes it. In a design without
timeline the body and the points are added directly.

If something fails while an element is created, the add-in tells Fusion that the command failed. Fusion then
undoes what was built so far.

## The construction points

Each component gets twelve construction points. With L = length, W = width and S = `stack` of the element, they
stand for these places in the element's own coordinates (mm):

| Name | x | y | z |
| --- | --- | --- | --- |
| bottom front | 0 | W/2 | 0 |
| bottom middle | L/2 | W/2 | 0 |
| bottom back | L | W/2 | 0 |
| top front | 0 | W/2 | S |
| top middle | L/2 | W/2 | S |
| top back | L | W/2 | S |
| top middle right | L/2 | 0 | S |
| top middle left | L/2 | W | S |
| bottom middle right | L/2 | 0 | 0 |
| bottom middle left | L/2 | W | 0 |
| middle right, 50 mm up | L/2 | 0 | 50 |
| middle left, 50 mm up | L/2 | W | 50 |

The three corners offered under **Placed by** are not construction points. With H = height they lie at:

| Entry | x | y | z |
| --- | --- | --- | --- |
| Bottom corner, front right | 0 | 0 | 0 |
| Top corner, front right | 0 | 0 | H |
| Top corner, front left | 0 | W | H |

These places come from the outer dimensions. On an element with a tongue, a groove or a recess such a place can
be inside the material, where the point cannot be seen, or in the air. Then the point is shown somewhere else:

1. straight above or below, on the closest face;
2. if there is no face above or below, or another point sits there already: along the length;
3. otherwise at the closest place on the surface, then across the wall.

Example `S1 WP`: "top middle" stands for the height 250 mm and is shown on top of the tongue at 300 mm. "bottom
middle" stands for the height 0 and is shown in the groove at 50 mm. On the half corner elements `SNL/2` and
`SNP/2` no free place is left for "bottom middle left"; it stays in the air.

Each point carries invisible marks (attribute group `System3E`):

| Name | Content |
| --- | --- |
| `point` | The key of the point. By it the add-in knows which points a component already has. |
| `shift` | The way from where the point is shown to the place it stands for, in mm. |
| `asis` | Set when Fusion put the point somewhere else and this could not be corrected. Such a point is left alone. |

When you click one of these points, the add-in adds `shift` and so places by the place the point stands for. A
wall in bond therefore comes out the same wherever a point is shown.

After a point is made, the add-in reads back where Fusion put it. For a new kind of element placed away from the
origin Fusion took the coordinates as those of the whole design; the points then lay beside the element. In that
case the add-in finds the copy of the component whose placement explains the difference, removes the point and
makes it again with corrected coordinates.

The point belongs to the component. So every copy of an element shows the same twelve points at its own place.

## How the place is computed

1. The spot chosen under **Placed by** is moved to the origin.
2. The element is turned about the Z axis by **Rotation**.
3. The element is moved to the clicked point plus **Offset X**, **Offset Y**, **Offset Z**.
   Without a clicked point the origin (0, 0, 0) is used.

The offsets are applied after the turn. So they run along the axes of the design, not along the turned element.

The position of a clicked sketch point is taken in the coordinates of the whole design, not of its sketch.
The position of a clicked construction point is worked out from the point inside its component and from the
placement of the copy that was clicked.

## Units

| Where | Unit |
| --- | --- |
| Element library `blocks.json` | mm |
| Fields **Offset X**, **Offset Y**, **Offset Z** | shown in mm |
| Field **Rotation** | shown in degrees |
| Inside Fusion's programming interface | cm and radians |

The add-in divides every library value by 10 when it hands it to Fusion. You do not have to convert anything.

## The preview

While the dialog is open, Fusion asks the add-in for a preview after every change. The add-in then runs the same
steps as for **OK**. Fusion discards this preview and runs the steps again when you press **OK**.
Errors during the preview are not shown.
