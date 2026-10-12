# -*- coding: utf-8 -*-
"""
System3E - Fusion 360 add-in entry point.

Everything you edit lives between the CONFIGURE and END OF TEMPLATE markers.
The reusable machinery sits in system3e_core.py next to this file.

The command places one SYSTEM 3E wall element: pick a point, pick the element
from the list - a picture shows which one it is - and it is created as a new
component. Which spot of the element lands on the point can be chosen, and
every element carries twelve points of its own to click for the next one.
"""

import os
import sys
import json
import importlib

import adsk.core
import adsk.fusion

# --- module loading ---------------------------------------------------------
# Fusion caches imported modules, so an edited helper would keep serving its
# old version until Fusion restarts. Dropping it from sys.modules before the
# import makes "stop, run" pick up changes.
#
# The name is renamed per add-in by tools/template/new_addin.py, which is what stops two
# add-ins built from this template from overwriting each other's core module.
_CORE_MODULE = 'system3e_core'

_DIR = os.path.dirname(os.path.abspath(__file__))
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)
if _CORE_MODULE in sys.modules:
    del sys.modules[_CORE_MODULE]
core = importlib.import_module(_CORE_MODULE)


# ============================================================== CONFIGURE ====

# Unique across every add-in installed in Fusion. Prefix it with something of
# your own; a collision silently hijacks the other add-in's button.
CMD_ID = 'thwSystem3ECmd'

# Where the button goes. FusionSolidEnvironment is the design workspace.
WORKSPACE_ID = 'FusionSolidEnvironment'

# Tried in order, first one that exists wins.
PANEL_IDS = ('SolidCreatePanel',)

# Command input ids. They only have to be unique inside this command.
IN_POINT = 's3ePoint'
IN_FAMILY = 's3eFamily'
IN_BLOCK = 's3eBlock'
IN_IMAGE = 's3eImage'
IN_ANGLE = 's3eAngle'
IN_ANCHOR = 's3eAnchor'
IN_DX = 's3eDx'
IN_DY = 's3eDy'
IN_DZ = 's3eDz'

RESOURCE_FOLDER = os.path.join(_DIR, 'resources', 'System3E')
LANG_DIR = os.path.join(_DIR, 'lang')
BLOCK_DIR = os.path.join(_DIR, 'blocks')

# The mark on a component that says which element it is.
ATTRIBUTE_GROUP = 'System3E'
ATTRIBUTE_BLOCK = 'block'
ATTRIBUTE_POINT = 'point'
ATTRIBUTE_SHIFT = 'shift'       # on a point: from where it is shown to what it means, mm
ATTRIBUTE_ASIS = 'asis'         # on a point: Fusion put it elsewhere and it could not be put right

# Last used values, kept for the duration of the Fusion session.
_last = {
    IN_FAMILY: 'basic',
    IN_BLOCK: 's1-wp',
    IN_ANGLE: 0.0,      # radians
    IN_ANCHOR: 'corner',
    IN_DX: 0.0,         # cm
    IN_DY: 0.0,
    IN_DZ: 0.0,
}

# =============================================================================

S = core.Strings(LANG_DIR)
S.load(core.FALLBACK_LANGUAGE)
_handlers = core.HandlerRegistry()
_control = None
_updating = False       # re-entrancy guard for inputChanged


def T(key, *args):
    return S.get(key, *args)


def fail(key, *args):
    """Raise an explainable error carrying a language-independent key."""
    raise core.AddInError(S, key, *args)


# ============================================================ YOUR CODE HERE ==

# How far one course reaches into the next, mm.
INTERLOCK = 50.0

# The points every element carries for clicking, in the order they are made.
POINT_KEYS = ('point.bottom.front', 'point.bottom.centre', 'point.bottom.back',
              'point.top.front', 'point.top.centre', 'point.top.back',
              'point.top.right', 'point.top.left',
              'point.bottom.right', 'point.bottom.left',
              'point.low.right', 'point.low.left')

# Which spot of the element lands on the clicked point ("Placed by"): three
# corners of the front end - right and left as seen from that end looking
# along the wall - and every point that can be clicked.
CORNERS = ('corner', 'top-right', 'top-left')
ANCHORS = CORNERS + POINT_KEYS


def anchor_text(anchor):
    """The text key of an anchor."""
    return 'anchor.' + anchor if anchor in CORNERS else anchor


def anchor_position(block, anchor):
    """The anchor in the element's own coordinates, mm."""
    if anchor == 'top-right':
        return (0.0, 0.0, float(block['size'][2]))
    if anchor == 'top-left':
        return (0.0, float(block['size'][1]), float(block['size'][2]))
    for key, position in snap_points(block):
        if key == anchor:
            return position
    return (0.0, 0.0, 0.0)


def snap_points(block):
    """The points every element carries for clicking: (text key, position in mm).

    Three on the underside and three at the height where the next course
    stands - front end, middle and back end, each in the middle of the wall
    thickness. A wall in bond is built by putting the bottom middle of the
    next element on the upper front or back point of the one below.

    Six more in the middle of the length on the two wall faces: at that
    height, on the underside and INTERLOCK mm above the underside. Right and
    left are as seen from the front end looking along the wall.
    """
    length, width = block['size'][0], block['size'][1]
    level = block.get('stack', block['size'][2])
    spots = (('front', 0.0), ('centre', length / 2.0), ('back', float(length)))
    return ([('point.bottom.' + key, (x, width / 2.0, 0.0)) for key, x in spots]
            + [('point.top.' + key, (x, width / 2.0, float(level))) for key, x in spots]
            + [('point.top.right', (length / 2.0, 0.0, float(level))),
               ('point.top.left', (length / 2.0, float(width), float(level))),
               ('point.bottom.right', (length / 2.0, 0.0, 0.0)),
               ('point.bottom.left', (length / 2.0, float(width), 0.0)),
               ('point.low.right', (length / 2.0, 0.0, INTERLOCK)),
               ('point.low.left', (length / 2.0, float(width), INTERLOCK))])     # same order as POINT_KEYS


NEAR = 0.01     # mm; closer than this counts as touching


def _in_face(face, points, p):
    """Whether p, already in the face's plane, lies on the face. Its outline counts."""
    normal = face['normal']
    drop = max(range(3), key=lambda i: abs(normal[i]))
    a, b = [i for i in range(3) if i != drop]
    u, v = p[a], p[b]
    inside = False
    for loop in face['loops']:
        for i, start in enumerate(loop):
            p0, p1 = points[start], points[loop[(i + 1) % len(loop)]]
            u0, v0, u1, v1 = p0[a], p0[b], p1[a], p1[b]
            length = max(abs(u1 - u0), abs(v1 - v0), 1.0)
            if (abs((u1 - u0) * (v - v0) - (v1 - v0) * (u - u0)) <= NEAR * length
                    and min(u0, u1) - NEAR <= u <= max(u0, u1) + NEAR
                    and min(v0, v1) - NEAR <= v <= max(v0, v1) + NEAR):
                return True
            if (v0 > v) != (v1 > v) and u < (u1 - u0) * (v - v0) / (v1 - v0) + u0:
                inside = not inside
    return inside


def _surface_along(block, p, axis):
    """How far from p, along one axis, the surface of the element is met: signed mm."""
    points = block['points']
    others = [i for i in range(3) if i != axis]
    found = []
    for face in block['faces']:
        normal = face['normal']
        origin = points[face['loops'][0][0]]
        distance = sum((origin[i] - p[i]) * normal[i] for i in range(3))
        if abs(normal[axis]) > 1e-6:
            t = distance / normal[axis]
            q = list(p)
            q[axis] += t
            if _in_face(face, points, q):
                found.append(t)
        elif abs(distance) < NEAR:
            # The line runs in the plane of the face: it meets the face at its outline.
            for loop in face['loops']:
                for i, start in enumerate(loop):
                    p0, p1 = points[start], points[loop[(i + 1) % len(loop)]]
                    k = max(others, key=lambda j: abs(p1[j] - p0[j]))
                    if abs(p1[k] - p0[k]) < 1e-6:
                        continue
                    s = (p[k] - p0[k]) / (p1[k] - p0[k])
                    if -1e-6 <= s <= 1.0 + 1e-6 and all(
                            abs(p0[j] + s * (p1[j] - p0[j]) - p[j]) < NEAR for j in others):
                        found.append(p0[axis] + s * (p1[axis] - p0[axis]) - p[axis])
    return found


def _nearest_on_surface(block, p, level=None):
    """The place on the element's surface closest to p; with `level`, only at that height.

    Of two places equally far away the one further along the length wins.
    Returns p itself when there is none.
    """
    points = block['points']
    best, best_distance = tuple(p), None
    for face in block['faces']:
        normal = face['normal']
        origin = points[face['loops'][0][0]]
        t = sum((origin[i] - p[i]) * normal[i] for i in range(3)) / sum(n * n for n in normal)
        foot = tuple(p[i] + t * normal[i] for i in range(3))
        spots = [foot] if _in_face(face, points, foot) else []
        for loop in face['loops']:
            for i, start in enumerate(loop):
                p0, p1 = points[start], points[loop[(i + 1) % len(loop)]]
                edge = [p1[j] - p0[j] for j in range(3)]
                length = sum(e * e for e in edge)
                s = sum((p[j] - p0[j]) * edge[j] for j in range(3)) / length if length else 0.0
                s = min(1.0, max(0.0, s))
                spots.append(tuple(p0[j] + s * edge[j] for j in range(3)))
        for spot in spots:
            if level is not None and abs(spot[2] - level) > NEAR:
                continue
            distance = sum((spot[j] - p[j]) ** 2 for j in range(3))
            if (best_distance is None or distance < best_distance - 1e-9
                    or (abs(distance - best_distance) <= 1e-9 and spot[0] > best[0])):
                best, best_distance = spot, distance
    return best


def on_surface(block, position, taken=()):
    """The place on the element's surface that stands for a point.

    The points are worked out from the outer dimensions. On an element with a
    tongue, a groove or a recess that place can be inside the material, where
    it cannot be seen, or in the air. Such a point moves straight up or down
    to the surface. Where there is none above or below, or another point sits
    there already (`taken`), it moves along the length, then to the closest
    place on the surface, then across the wall, and last to the closest place
    at its own height.
    """
    position = tuple(float(c) for c in position)
    reach = [_surface_along(block, position, axis) for axis in range(3)]
    if any(abs(t) < NEAR for hits in reach for t in hits):
        return position
    places = []
    for axis in (2, 0, None, 1):
        if axis is None:
            places.append(_nearest_on_surface(block, position))
            continue
        for t in sorted(reach[axis], key=lambda t: (abs(t), -t)):
            places.append(tuple(c + t if i == axis else c for i, c in enumerate(position)))
    places.append(_nearest_on_surface(block, position, level=position[2]))
    for place in places:
        if all(max(abs(place[i] - other[i]) for i in range(3)) > 1.0 for other in taken):
            return place
    return position


_shown = {}


def shown_points(block):
    """The points as they are put on the element: (text key, where it is shown, what it means).

    Both in mm. Clicking a point places by what it means, so a wall in bond
    comes out the same wherever the point had to move to be seen. A point
    that has to move never lands on another one.
    """
    if block['id'] not in _shown:
        meant = [(key, tuple(float(c) for c in position)) for key, position in snap_points(block)]
        shown = dict((key, position) for key, position in meant
                     if on_surface(block, position) == position)
        for key, position in meant:
            if key not in shown:
                shown[key] = on_surface(block, position, list(shown.values()))
        _shown[block['id']] = [(key, shown[key], position) for key, position in meant]
    return _shown[block['id']]


def point_types():
    """What may be clicked as the place for the element."""
    return (adsk.fusion.SketchPoint.classType(),
            adsk.fusion.BRepVertex.classType(),
            adsk.fusion.ConstructionPoint.classType())


_library = None


def library():
    """The elements from blocks/blocks.json, read once.

    Returns (families, by_id): the family ids in catalogue order with their
    elements, and every element by its id. Lengths in the file are mm.
    """
    global _library
    if _library is None:
        with open(os.path.join(BLOCK_DIR, 'blocks.json'), 'r', encoding='utf-8') as handle:
            blocks = json.load(handle)['blocks']
        families, by_id = [], {}
        for block in blocks:
            by_id[block['id']] = block
            if not families or families[-1][0] != block['family']:
                families.append((block['family'], []))
            families[-1][1].append(block)
        _library = (families, by_id)
    return _library


def block_label(block):
    return '%s   %d x %d x %d' % ((block['name'],) + tuple(block['size']))


def selected_family(inputs):
    item = inputs.itemById(IN_FAMILY).selectedItem
    families = library()[0]
    return families[item.index][0] if item else families[0][0]


def selected_block(inputs):
    item = inputs.itemById(IN_BLOCK).selectedItem
    if not item:
        return None
    for family, blocks in library()[0]:
        if family == selected_family(inputs):
            return blocks[item.index] if item.index < len(blocks) else None
    return None


def selected_anchor(inputs):
    item = inputs.itemById(IN_ANCHOR).selectedItem
    return ANCHORS[item.index] if item and item.index < len(ANCHORS) else ANCHORS[0]


def point_of(entity):
    """Where a clicked sketch point, body corner or construction point is in the design."""
    if entity.objectType == adsk.fusion.SketchPoint.classType():
        return entity.worldGeometry
    if entity.objectType == adsk.fusion.ConstructionPoint.classType():
        try:
            return meant_place(entity)
        except Exception:
            pass        # then the point counts where Fusion says it is
    return entity.geometry


def meant_place(point):
    """The place a construction point stands for, in the design, cm.

    Worked out from the point inside its own component and from where that
    copy of the component sits, rather than asked from Fusion for the copy.
    One of the add-in's points that had to move onto the surface to be seen
    still stands for the place it was worked out for.
    """
    occurrence = point.assemblyContext
    native = point.nativeObject if occurrence else point
    place = native.geometry
    mark = native.attributes.itemByName(ATTRIBUTE_GROUP, ATTRIBUTE_SHIFT)
    if mark:
        x, y, z = json.loads(mark.value)
        place.translateBy(adsk.core.Vector3D.create(x / 10.0, y / 10.0, z / 10.0))
    if occurrence:
        place.transformBy(occurrence.transform2)
    return place


def read_inputs(inputs):
    """Pull every value out of the dialog in one place.

    Doing this once keeps execute, executePreview and validateInputs looking at
    exactly the same values.
    """
    selection = inputs.itemById(IN_POINT)
    point = None
    if selection.selectionCount == 1:
        entity = selection.selection(0).entity
        if entity and entity.objectType in point_types():
            point = point_of(entity)
    return dict(
        point=point,            # None: the origin
        family=selected_family(inputs),
        block=selected_block(inputs),
        angle=inputs.itemById(IN_ANGLE).value,
        anchor=selected_anchor(inputs),
        dx=inputs.itemById(IN_DX).value,      # cm
        dy=inputs.itemById(IN_DY).value,
        dz=inputs.itemById(IN_DZ).value,
    )


def validate(values):
    """Raise an AddInError for anything the user has to fix."""
    if values['block'] is None:
        fail('err.no_block')


def make_body(block):
    """A solid body from the element's points and flat faces.

    Every face is a plane bounded by straight edges; an edge is defined once
    and used by its two faces in opposite directions. Fusion works in cm.
    """
    definition = adsk.fusion.BRepBodyDefinition.create()
    definition.doFullCheck = True
    points = [adsk.core.Point3D.create(p[0] / 10.0, p[1] / 10.0, p[2] / 10.0)
              for p in block['points']]
    vertices = [definition.createVertexDefinition(p) for p in points]
    shell = definition.lumpDefinitions.add().shellDefinitions.add()
    edges = {}
    for face in block['faces']:
        normal = adsk.core.Vector3D.create(*face['normal'])
        plane = adsk.core.Plane.create(points[face['loops'][0][0]], normal)
        face_definition = shell.faceDefinitions.add(plane, False)
        for loop in face['loops']:
            loop_definition = face_definition.loopDefinitions.add()
            for i, start in enumerate(loop):
                end = loop[(i + 1) % len(loop)]
                low, high = min(start, end), max(start, end)
                if (low, high) not in edges:
                    edges[(low, high)] = definition.createEdgeDefinitionByCurve(
                        vertices[low], vertices[high],
                        adsk.core.Line3D.create(points[low], points[high]))
                loop_definition.bRepCoEdgeDefinitions.add(edges[(low, high)], start > end)
    body = definition.createBody()
    if body is None:
        fail('err.body_failed', block['name'], '; '.join(definition.outcomeInfo))
    return body


def component_name(block):
    return 'SYSTEM 3E %s' % block['name']


def own_components(design):
    """Every component of this design that can hold an element: (component, its mark or None).

    Components without a body are left out, and so are those of a linked
    design, which cannot be changed from here.
    """
    components = design.allComponents
    for i in range(components.count):
        component = components.item(i)
        if component.bRepBodies.count == 0:
            continue
        try:
            if component.parentDesign != design:
                continue
        except Exception:
            pass
        yield component, component.attributes.itemByName(ATTRIBUTE_GROUP, ATTRIBUTE_BLOCK)


def find_component(design, block):
    """The component of this element, if the design already has one.

    Found by the mark the add-in leaves on it, so renaming it does no harm.
    Elements placed before the mark existed are found by their name.
    """
    by_name = None
    for component, mark in own_components(design):
        if mark and mark.value == block['id']:
            return component
        if by_name is None and not mark and component.name == component_name(block):
            by_name = component
    return by_name


def remove_point(point):
    """Take one construction point away; False when Fusion will not let go of it."""
    try:
        base = point.baseFeature
        if base:
            base.startEdit()
        try:
            return bool(point.deleteMe())
        finally:
            if base:
                base.finishEdit()
    except Exception:
        return False


def _off(place, wanted):
    """Whether a place Fusion reports (cm) is not the wanted one (mm)."""
    return max(abs(place.x * 10.0 - wanted[0]), abs(place.y * 10.0 - wanted[1]),
               abs(place.z * 10.0 - wanted[2])) > NEAR


def used_frame(design, component, wanted, got):
    """The placement Fusion read a point's coordinates in, if it was not the component itself.

    A point made at plain coordinates in a component that is placed away from
    the origin can end up as if the coordinates were the design's: it then
    sits off the element by the placement of one of the component's copies.
    Returns that placement, or None when none of them explains the place.
    """
    copies = design.rootComponent.allOccurrencesByComponent(component)
    for i in range(copies.count):
        frame = copies.item(i).transform2
        back = frame.copy()
        if not back.invert():
            continue
        seen = adsk.core.Point3D.create(wanted[0] / 10.0, wanted[1] / 10.0, wanted[2] / 10.0)
        seen.transformBy(back)
        if not _off(got, (seen.x * 10.0, seen.y * 10.0, seen.z * 10.0)):
            return frame
    return None


def add_snap_points(design, component, block, base):
    """Give the component the clickable points it does not have yet.

    A component made by an older version has none or fewer, or has them where
    they cannot be seen; only what is missing or misplaced is made. With the
    timeline on, a point at plain coordinates has to live in a base feature:
    `base` while it is open for editing, otherwise one of its own.
    """
    points = component.constructionPoints
    wanted = dict((key, shown) for key, shown, meant in shown_points(block))
    present, misplaced = set(), []
    for i in range(points.count):
        point = points.item(i)
        mark = point.attributes.itemByName(ATTRIBUTE_GROUP, ATTRIBUTE_POINT)
        if not mark:
            continue
        shown = wanted.get(mark.value)
        if (shown and _off(point.geometry, shown)
                and not point.attributes.itemByName(ATTRIBUTE_GROUP, ATTRIBUTE_ASIS)):
            misplaced.append((mark.value, point))
        else:
            present.add(mark.value)
    for key, point in misplaced:
        if key in present or not remove_point(point):
            present.add(key)        # better in the old place than twice
    missing = [entry for entry in shown_points(block) if entry[0] not in present]
    if not missing:
        return
    own = None
    if base is None and design.designType == adsk.fusion.DesignTypes.ParametricDesignType:
        own = base = component.features.baseFeatures.add()
        own.startEdit()

    def make(shown, frame):
        place = adsk.core.Point3D.create(shown[0] / 10.0, shown[1] / 10.0, shown[2] / 10.0)
        if frame is not None:
            place.transformBy(frame)
        definition = points.createInput()
        definition.setByPoint(place)
        if base is not None:
            definition.targetBaseOrFormFeature = base
        return points.add(definition)

    frame = None
    try:
        for key, shown, meant in missing:
            point = make(shown, frame)
            if frame is None and _off(point.geometry, shown):
                # Fusion took the coordinates for the design's, not the component's.
                frame = used_frame(design, component, shown, point.geometry)
                if frame is not None:
                    point.deleteMe()
                    point = make(shown, frame)
            point.name = T(key)
            point.attributes.add(ATTRIBUTE_GROUP, ATTRIBUTE_POINT, key)
            point.attributes.add(ATTRIBUTE_GROUP, ATTRIBUTE_SHIFT,
                                 json.dumps([meant[i] - shown[i] for i in range(3)]))
            if _off(point.geometry, shown):
                # Not to be made again on every placement: each try costs a timeline entry.
                point.attributes.add(ATTRIBUTE_GROUP, ATTRIBUTE_ASIS, '1')
    finally:
        if own is not None:
            own.finishEdit()


def complete_snap_points(design):
    """Give every element in the design the points it does not have yet.

    The points arrived over several versions, so a design holds elements with
    none, six, eight, ten or all twelve, and before 1.1.0.1 some of them sat
    inside the material. Topping up only the element being placed would leave
    the others short.
    """
    by_id = library()[1]
    by_name = dict((component_name(block), block) for block in by_id.values())
    for component, mark in own_components(design):
        block = by_id.get(mark.value) if mark else by_name.get(component.name)
        if block:
            add_snap_points(design, component, block, None)


def build_result(values):
    """Create the element as a new component. Everything is validated by now."""
    block = values['block']
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    if not design:
        fail('err.no_design')
    complete_snap_points(design)

    # Bring the anchor to the origin, turn about the vertical axis, then move
    # to the clicked point plus the offset. The offset runs along the design's
    # X, Y and Z, not along the turned element.
    anchor = anchor_position(block, values['anchor'])
    placement = adsk.core.Matrix3D.create()
    placement.translation = adsk.core.Vector3D.create(
        -anchor[0] / 10.0, -anchor[1] / 10.0, -anchor[2] / 10.0)
    turn = adsk.core.Matrix3D.create()
    turn.setToRotation(values['angle'], adsk.core.Vector3D.create(0, 0, 1),
                       adsk.core.Point3D.create(0, 0, 0))
    placement.transformBy(turn)
    target = values['point']
    move = adsk.core.Matrix3D.create()
    move.translation = adsk.core.Vector3D.create(
        (target.x if target else 0.0) + values['dx'],
        (target.y if target else 0.0) + values['dy'],
        (target.z if target else 0.0) + values['dz'])
    placement.transformBy(move)

    # The same element again is another copy of the same component, not a new
    # one - otherwise a parts list shows "S1 WP", "S1 WP (1)", "S1 WP (2)"
    # as three different parts instead of one part, three times.
    known = find_component(design, block)
    if known:
        design.rootComponent.occurrences.addExistingComponent(known, placement)
        return

    body = make_body(block)
    occurrence = design.rootComponent.occurrences.addNewComponent(placement)
    component = occurrence.component
    component.name = component_name(block)
    component.attributes.add(ATTRIBUTE_GROUP, ATTRIBUTE_BLOCK, block['id'])
    if design.designType == adsk.fusion.DesignTypes.ParametricDesignType:
        # With the timeline on, a ready-made body has to arrive inside a base feature.
        base = component.features.baseFeatures.add()
        base.startEdit()
        try:
            created = component.bRepBodies.add(body, base)
            if created:
                created.name = block['name']    # while the base feature is still open
            add_snap_points(design, component, block, base)
        finally:
            base.finishEdit()
    else:
        created = component.bRepBodies.add(body)
        if created:
            created.name = block['name']
        add_snap_points(design, component, block, None)


def fill_blocks(inputs, family, wanted=None):
    """Put the elements of one family into the element list."""
    items = inputs.itemById(IN_BLOCK).listItems
    items.clear()
    for known, blocks in library()[0]:
        if known == family:
            chosen = wanted if any(b['id'] == wanted for b in blocks) else blocks[0]['id']
            for block in blocks:
                items.add(block_label(block), block['id'] == chosen, '')


def show_picture(inputs):
    block = selected_block(inputs)
    if block:
        picture = os.path.join(BLOCK_DIR, block['id'] + '.png')
        if os.path.isfile(picture):
            inputs.itemById(IN_IMAGE).imageFile = picture


def build_inputs(inputs):
    """Lay out the dialog. Every label comes from the text catalogue."""
    selection = inputs.addSelectionInput(IN_POINT, T('in.point'), T('in.point.prompt'))
    for kind in ('SketchPoints', 'Vertices', 'ConstructionPoints'):
        selection.addSelectionFilter(kind)
    selection.setSelectionLimits(0, 1)

    families = library()[0]
    known = [family for family, blocks in families]
    family = _last[IN_FAMILY] if _last[IN_FAMILY] in known else known[0]
    dropdown = inputs.addDropDownCommandInput(
        IN_FAMILY, T('in.family'), adsk.core.DropDownStyles.TextListDropDownStyle)
    for name in known:
        dropdown.listItems.add(T('family.' + name), name == family, '')

    inputs.addDropDownCommandInput(
        IN_BLOCK, T('in.block'), adsk.core.DropDownStyles.TextListDropDownStyle)
    fill_blocks(inputs, family, _last[IN_BLOCK])

    first = os.path.join(BLOCK_DIR, (selected_block(inputs) or families[0][1][0])['id'] + '.png')
    image = inputs.addImageCommandInput(IN_IMAGE, '', first)
    image.isFullWidth = True

    anchors = inputs.addDropDownCommandInput(
        IN_ANCHOR, T('in.anchor'), adsk.core.DropDownStyles.TextListDropDownStyle)
    for name in ANCHORS:
        anchors.listItems.add(T(anchor_text(name)), name == _last[IN_ANCHOR], '')

    inputs.addValueInput(IN_ANGLE, T('in.angle'), 'deg',
                         adsk.core.ValueInput.createByReal(_last[IN_ANGLE]))
    # 'mm' is what the field shows; the value itself is cm, Fusion's own unit.
    inputs.addValueInput(IN_DX, T('in.dx'), 'mm', adsk.core.ValueInput.createByReal(_last[IN_DX]))
    inputs.addValueInput(IN_DY, T('in.dy'), 'mm', adsk.core.ValueInput.createByReal(_last[IN_DY]))
    inputs.addValueInput(IN_DZ, T('in.dz'), 'mm', adsk.core.ValueInput.createByReal(_last[IN_DZ]))
    return selection


def remember(values):
    """Carry settings over to the next invocation within this session."""
    _last[IN_FAMILY] = values['family']
    _last[IN_BLOCK] = values['block']['id']
    _last[IN_ANGLE] = values['angle']
    _last[IN_ANCHOR] = values['anchor']
    _last[IN_DX] = values['dx']
    _last[IN_DY] = values['dy']
    _last[IN_DZ] = values['dz']


def on_input_changed(inputs, changed):
    """A new family refills the element list; a new element changes the picture."""
    global _updating
    if changed.id not in (IN_FAMILY, IN_BLOCK):
        return
    _updating = True
    try:
        if changed.id == IN_FAMILY:
            fill_blocks(inputs, selected_family(inputs))
        show_picture(inputs)
    finally:
        _updating = False


# ========================================================= END OF TEMPLATE ====

def _run_command(inputs):
    values = read_inputs(inputs)
    validate(values)
    build_result(values)
    return values


class ExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        ui = adsk.core.Application.get().userInterface
        try:
            remember(_run_command(args.firingEvent.sender.commandInputs))
        except core.AddInError as err:
            args.executeFailed = True       # Fusion undoes what was built so far
            ui.messageBox(str(err), T('cmd.name'))
        except Exception:
            args.executeFailed = True
            core.report(ui, S, 'msg.exec_failed')


class PreviewHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        try:
            _run_command(args.firingEvent.sender.commandInputs)
            # False makes Fusion run execute again for the real result. Set it
            # to True only when the preview already produced the final feature.
            args.isValidResult = False
        except Exception:
            # The preview fires on every keystroke, including half-typed
            # values. Staying silent here is deliberate; validateInputs greys
            # out OK instead. Neither of them shows the user why.
            pass


class ValidateHandler(adsk.core.ValidateInputsEventHandler):
    def notify(self, args):
        try:
            validate(read_inputs(args.firingEvent.sender.commandInputs))
            args.areInputsValid = True
        except Exception:
            args.areInputsValid = False


class InputChangedHandler(adsk.core.InputChangedEventHandler):
    def notify(self, args):
        if _updating:
            return
        try:
            changed = args.input
            on_input_changed(changed.parentCommand.commandInputs, changed)
        except Exception:
            pass


class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        ui = adsk.core.Application.get().userInterface
        try:
            command = args.command
            command.isRepeatable = True
            inputs = command.commandInputs

            # Whatever was selected before the button was pressed. Read it
            # before the inputs exist, then hand it to the selection input, so
            # clicking a point and then the button just works.
            preselected = []
            for i in range(ui.activeSelections.count):
                entity = ui.activeSelections.item(i).entity
                if entity and entity.objectType in point_types():
                    preselected.append(entity)

            selection = build_inputs(inputs)

            # Handlers first: whatever fails below, the dialog must still work.
            _handlers.add(command.execute, ExecuteHandler())
            _handlers.add(command.executePreview, PreviewHandler())
            _handlers.add(command.validateInputs, ValidateHandler())
            _handlers.add(command.inputChanged, InputChangedHandler())

            if preselected and selection and selection.selectionCount == 0:
                try:
                    selection.addSelection(preselected[0])
                except Exception:
                    pass        # then the user picks the point in the dialog
        except Exception:
            core.report(ui, S, 'msg.dialog_failed')


def run(context):
    global _control
    ui = None
    try:
        ui = adsk.core.Application.get().userInterface
        S.load(core.detect_language())

        # A definition left behind by a previous run would keep its old label
        # and its old handler, so drop it first.
        stale = ui.commandDefinitions.itemById(CMD_ID)
        if stale:
            stale.deleteMe()

        icons = RESOURCE_FOLDER if os.path.isdir(RESOURCE_FOLDER) else ''
        definition = ui.commandDefinitions.addButtonDefinition(
            CMD_ID,
            core.display_name(T('cmd.name'), core.read_version(_DIR, 'System3E')),
            T('cmd.tooltip'), icons)
        _handlers.add(definition.commandCreated, CommandCreatedHandler())

        panel = core.find_panel(ui, WORKSPACE_ID, PANEL_IDS)
        if not panel:
            ui.messageBox(T('msg.panel_missing'), T('cmd.name'))
            return
        _control = core.add_button(ui, panel, definition)
    except Exception:
        if ui:
            core.report(ui, S, 'msg.run_failed')


def stop(context):
    global _control
    ui = None
    try:
        ui = adsk.core.Application.get().userInterface
        core.remove_button(ui, WORKSPACE_ID, PANEL_IDS, CMD_ID)
        _control = None
        _handlers.clear()
    except Exception:
        if ui:
            core.report(ui, S, 'msg.stop_failed')
