# -*- coding: utf-8 -*-
"""
System3E - Fusion 360 add-in entry point.

Everything you edit lives between the CONFIGURE and END OF TEMPLATE markers.
The reusable machinery sits in addin_core.py next to this file.

The command places one SYSTEM 3E wall element: pick a point, pick the element
from the list - a picture shows which one it is - and it is created as a new
component. Which spot of the element lands on the point can be chosen, and
every element carries ten points of its own to click for the next one.
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

# Which spot of the element lands on the clicked point. The three "bottom"
# spots lie on the underside, in the middle of the wall thickness.
ANCHORS = ('corner', 'front', 'centre', 'back')


def anchor_position(block, anchor):
    """The anchor in the element's own coordinates, mm."""
    length, width = block['size'][0], block['size'][1]
    if anchor == 'front':
        return (0.0, width / 2.0, 0.0)
    if anchor == 'centre':
        return (length / 2.0, width / 2.0, 0.0)
    if anchor == 'back':
        return (float(length), width / 2.0, 0.0)
    return (0.0, 0.0, 0.0)


def snap_points(block):
    """The points every element carries for clicking: (text key, position in mm).

    Three on the underside and three at the height where the next course
    stands - front end, middle and back end, each in the middle of the wall
    thickness. A wall in bond is built by putting the bottom middle of the
    next element on the upper front or back point of the one below.

    Four more in the middle of the length on the two wall faces, at that
    height and on the underside: right and left as seen from the front end
    looking along the wall.
    """
    length, width = block['size'][0], block['size'][1]
    level = block.get('stack', block['size'][2])
    spots = (('front', 0.0), ('centre', length / 2.0), ('back', float(length)))
    return ([('point.bottom.' + key, (x, width / 2.0, 0.0)) for key, x in spots]
            + [('point.top.' + key, (x, width / 2.0, float(level))) for key, x in spots]
            + [('point.top.right', (length / 2.0, 0.0, float(level))),
               ('point.top.left', (length / 2.0, float(width), float(level))),
               ('point.bottom.right', (length / 2.0, 0.0, 0.0)),
               ('point.bottom.left', (length / 2.0, float(width), 0.0))])


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
    return entity.geometry


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


def find_component(design, block):
    """The component of this element, if the design already has one.

    Found by the mark the add-in leaves on it, so renaming it does no harm.
    Elements placed before the mark existed are found by their name.
    """
    by_name = None
    components = design.allComponents
    for i in range(components.count):
        component = components.item(i)
        if component.bRepBodies.count == 0:
            continue
        mark = component.attributes.itemByName(ATTRIBUTE_GROUP, ATTRIBUTE_BLOCK)
        if mark and mark.value == block['id']:
            return component
        if by_name is None and not mark and component.name == component_name(block):
            by_name = component
    return by_name


def add_snap_points(design, component, block, base):
    """Give the component the clickable points it does not have yet.

    A component made by an older version has none or fewer; only the missing
    ones are added. With the timeline on, a point at plain coordinates has to
    live in a base feature: `base` while it is open for editing, otherwise one
    of its own.
    """
    points = component.constructionPoints
    present = set()
    for i in range(points.count):
        mark = points.item(i).attributes.itemByName(ATTRIBUTE_GROUP, ATTRIBUTE_POINT)
        if mark:
            present.add(mark.value)
    missing = [(key, position) for key, position in snap_points(block) if key not in present]
    if not missing:
        return
    own = None
    if base is None and design.designType == adsk.fusion.DesignTypes.ParametricDesignType:
        own = base = component.features.baseFeatures.add()
        own.startEdit()
    try:
        for key, position in missing:
            definition = points.createInput()
            definition.setByPoint(adsk.core.Point3D.create(
                position[0] / 10.0, position[1] / 10.0, position[2] / 10.0))
            if base is not None:
                definition.targetBaseOrFormFeature = base
            point = points.add(definition)
            point.name = T(key)
            point.attributes.add(ATTRIBUTE_GROUP, ATTRIBUTE_POINT, key)
    finally:
        if own is not None:
            own.finishEdit()


def build_result(values):
    """Create the element as a new component. Everything is validated by now."""
    block = values['block']
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    if not design:
        fail('err.no_design')

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
        add_snap_points(design, known, block, None)     # elements from before 0.3.0 have none
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
            add_snap_points(design, component, block, base)
        finally:
            base.finishEdit()
    else:
        created = component.bRepBodies.add(body)
        add_snap_points(design, component, block, None)
    if created:
        created.name = block['name']


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
        anchors.listItems.add(T('anchor.' + name), name == _last[IN_ANCHOR], '')

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
            ui.messageBox(str(err), T('cmd.name'))
        except Exception:
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
            if preselected and selection and selection.selectionCount == 0:
                selection.addSelection(preselected[0])

            _handlers.add(command.execute, ExecuteHandler())
            _handlers.add(command.executePreview, PreviewHandler())
            _handlers.add(command.validateInputs, ValidateHandler())
            _handlers.add(command.inputChanged, InputChangedHandler())
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
