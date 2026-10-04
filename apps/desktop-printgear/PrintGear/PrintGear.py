# -*- coding: utf-8 -*-
"""
PrintGear - involute gears sized for the nozzle they will be printed with.

The module is not asked for directly. A printed tooth fails at the root, and
what the root can carry is decided by how many extrusions fit across it, so the
module follows the nozzle: module = nozzle * factor, 2.5 by default.

Pick one point and get a gear, or a meshing pair. Pick several and get a train:
first point drives, last point is driven, the ratio is held between those two
and the gears in between are sized to reach the points they were dropped on.

Geometry lives in printgear_math.py (no Fusion imports, testable offline) and
printgear_build.py (everything that touches the API).
"""

import os
import sys
import math
import importlib

import adsk.core
import adsk.fusion

# --- module loading ---------------------------------------------------------
# Fusion caches imported modules, so an edited helper keeps serving its old
# version until Fusion restarts. Dropping them before the import makes
# "stop, run" pick up changes.
_MODULES = ('printgear_core', 'printgear_math', 'printgear_build')

_DIR = os.path.dirname(os.path.abspath(__file__))
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)
for _name in _MODULES:
    if _name in sys.modules:
        del sys.modules[_name]
core = importlib.import_module('printgear_core')
pg = importlib.import_module('printgear_math')
build = importlib.import_module('printgear_build')


# ============================================================== CONFIGURE ====

CMD_ID = 'thwPrintGearCmd'
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_IDS = ('SolidCreatePanel', 'SketchCreatePanel')

IN_POINTS = 'pgPoints'
IN_NOZZLE = 'pgNozzle'
IN_FACTOR = 'pgFactor'
IN_MODULE = 'pgModule'
IN_STYLE = 'pgStyle'
IN_HELIX = 'pgHelix'
IN_PRESSURE = 'pgPressure'
IN_WIDTH = 'pgWidth'
IN_BACKLASH = 'pgBacklash'
IN_SHIFT = 'pgShift'
IN_SIZE_MODE = 'pgSizeMode'
IN_FIRST = 'pgFirst'
IN_FIRST_DIA = 'pgFirstDia'
IN_RATIO = 'pgRatio'
IN_MODE = 'pgMode'
IN_PAIR = 'pgPair'
IN_PAIR_ANGLE = 'pgPairAngle'
IN_BORE = 'pgBore'
IN_COMPONENTS = 'pgComponents'
IN_PREVIEW = 'pgPreview'
IN_INFO = 'pgInfo'

GROUP_PRINT = 'pgGroupPrint'
GROUP_TEETH = 'pgGroupTeeth'
GROUP_TRAIN = 'pgGroupTrain'
GROUP_OUTPUT = 'pgGroupOutput'

RESOURCE_FOLDER = os.path.join(_DIR, 'resources', 'PrintGear')
LANG_DIR = os.path.join(_DIR, 'lang')

NOZZLE_CUSTOM = 'custom'
SIZE_TEETH = 'teeth'
SIZE_DIAMETER = 'diameter'
PREVIEW_CIRCLES = 'circles'
PREVIEW_FULL = 'full'
PREVIEW_OFF = 'off'

MAX_POINTS = 20

# Last used values, kept for the duration of the Fusion session. Lengths are in
# centimetres, Fusion's internal unit, regardless of what the input displays.
_last = {
    IN_NOZZLE: '0.4',
    IN_FACTOR: pg.DEFAULT_MODULE_FACTOR,
    IN_MODULE: pg.module_for_nozzle(0.4) * build.MM,
    IN_STYLE: pg.TEETH_STRAIGHT,
    IN_HELIX: math.radians(pg.DEFAULT_HELIX_ANGLE_DEG),
    IN_PRESSURE: math.radians(pg.DEFAULT_PRESSURE_ANGLE_DEG),
    IN_WIDTH: 0.8,                                  # 8 mm
    IN_BACKLASH: pg.DEFAULT_BACKLASH * build.MM,
    IN_SHIFT: True,
    IN_SIZE_MODE: SIZE_TEETH,
    IN_FIRST: 17.0,
    IN_FIRST_DIA: 1.7,                              # 17 mm
    IN_RATIO: 3.0,
    IN_MODE: pg.MODE_RATIO,
    IN_PAIR: False,
    IN_PAIR_ANGLE: math.radians(pg.DEFAULT_PAIR_ANGLE_DEG),
    IN_BORE: 0.5,                                   # 5 mm
    IN_COMPONENTS: True,
    IN_PREVIEW: PREVIEW_CIRCLES,
}

# =============================================================================

S = core.Strings(LANG_DIR)
S.load(core.FALLBACK_LANGUAGE)
_handlers = core.HandlerRegistry()
_control = None
_updating = False


def T(key, *args):
    return S.get(key, *args)


def fail(key, *args):
    raise core.AddInError(S, key, *args)


# ================================================================= reading ===

def _dropdown_key(dropdown, keys, default):
    """Key behind the selected row. Names are translated, so index is the link."""
    item = dropdown.selectedItem
    if item is None:
        return default
    for index in range(dropdown.listItems.count):
        if dropdown.listItems.item(index) == item:
            return keys[index] if index < len(keys) else default
    return default


NOZZLE_KEYS = [str(size) for size in pg.NOZZLE_SIZES] + [NOZZLE_CUSTOM]
STYLE_KEYS = [pg.TEETH_STRAIGHT, pg.TEETH_HELICAL, pg.TEETH_HERRINGBONE]
SIZE_KEYS = [SIZE_TEETH, SIZE_DIAMETER]
MODE_KEYS = [pg.MODE_RATIO, pg.MODE_POSITION]
PREVIEW_KEYS = [PREVIEW_CIRCLES, PREVIEW_FULL, PREVIEW_OFF]


def _entity_point(entity):
    """World position of a selected point, in millimetres.

    Sketch points carry both a sketch-local and a world position; the world one
    is what places gears consistently no matter which sketch a point came from.
    """
    geometry = None
    if hasattr(entity, 'worldGeometry'):
        geometry = entity.worldGeometry
    if geometry is None and hasattr(entity, 'geometry'):
        geometry = entity.geometry
    if geometry is None:
        return None
    return (geometry.x / build.MM, geometry.y / build.MM, geometry.z / build.MM)


def read_inputs(inputs):
    """Pull every value out of the dialog in one place.

    Doing this once keeps execute, executePreview and validateInputs looking at
    exactly the same numbers.
    """
    selection = inputs.itemById(IN_POINTS)
    points = []
    for index in range(selection.selectionCount):
        point = _entity_point(selection.selection(index).entity)
        if point is not None:
            points.append(point)

    nozzle_key = _dropdown_key(inputs.itemById(IN_NOZZLE), NOZZLE_KEYS, '0.4')
    factor = inputs.itemById(IN_FACTOR).value
    if nozzle_key == NOZZLE_CUSTOM:
        module = inputs.itemById(IN_MODULE).value / build.MM
        # No nozzle was named, but tip truncation still needs an extrusion
        # width to work to, so read one back out of the module.
        nozzle = module / factor if factor > 1e-6 else 0.4
    else:
        nozzle = float(nozzle_key)
        module = pg.module_for_nozzle(nozzle, factor)

    return dict(
        points=points,
        nozzle=nozzle,
        module=module,
        custom_module=nozzle_key == NOZZLE_CUSTOM,
        tooth_style=_dropdown_key(inputs.itemById(IN_STYLE), STYLE_KEYS,
                                  pg.TEETH_STRAIGHT),
        helix_angle_deg=math.degrees(inputs.itemById(IN_HELIX).value),
        pressure_angle_deg=math.degrees(inputs.itemById(IN_PRESSURE).value),
        face_width=inputs.itemById(IN_WIDTH).value / build.MM,
        backlash=inputs.itemById(IN_BACKLASH).value / build.MM,
        auto_profile_shift=inputs.itemById(IN_SHIFT).value,
        size_mode=_dropdown_key(inputs.itemById(IN_SIZE_MODE), SIZE_KEYS, SIZE_TEETH),
        first_teeth_value=inputs.itemById(IN_FIRST).value,
        first_diameter=inputs.itemById(IN_FIRST_DIA).value / build.MM,
        ratio=inputs.itemById(IN_RATIO).value,
        mode=_dropdown_key(inputs.itemById(IN_MODE), MODE_KEYS, pg.MODE_RATIO),
        pair=inputs.itemById(IN_PAIR).value,
        pair_angle_deg=math.degrees(inputs.itemById(IN_PAIR_ANGLE).value),
        bore_diameter=inputs.itemById(IN_BORE).value / build.MM,
        as_components=inputs.itemById(IN_COMPONENTS).value,
        preview=_dropdown_key(inputs.itemById(IN_PREVIEW), PREVIEW_KEYS,
                              PREVIEW_CIRCLES),
        clearance_factor=pg.DEFAULT_CLEARANCE_FACTOR,
        fillet_factor=pg.DEFAULT_FILLET_FACTOR,
    )


def first_teeth(values):
    """Tooth count of the first gear, whichever way the size was given.

    Two separate inputs rather than one: a value input carries a fixed unit, so
    a field that is teeth one moment and millimetres the next would misread
    every entry in a document whose units are not millimetres.
    """
    if values['size_mode'] == SIZE_DIAMETER:
        if values['module'] <= 1e-9:
            return 0
        return int(round(values['first_diameter'] / values['module']))
    return int(round(values['first_teeth_value']))


def plan(values):
    """Everything the build needs, or an AddInError explaining why not."""
    validate(values)
    flat = [(x, y) for x, y, _ in values['points']]
    placements, warnings = pg.plan_train(
        flat, values['module'], first_teeth(values), values['ratio'], values)

    # Checks that need the finished train: the smallest gear is not necessarily
    # either end of it, and it is the one the bore has to fit inside.
    bore_radius = values['bore_diameter'] / 2.0
    for placement in placements:
        spec = placement.spec
        if bore_radius >= spec.root_radius - spec.module * 0.5:
            fail('err.bore_too_big')
        if spec.teeth < pg.MIN_TEETH:
            fail('err.teeth_low', pg.MIN_TEETH)
    return placements, warnings


# ============================================================== validation ===

def validate(values):
    """Raise an AddInError for anything the user has to fix.

    Called before drawing and again from validateInputs, so an impossible
    combination disables OK instead of failing halfway through.
    """
    if not values['points']:
        fail('err.no_points')
    if len(values['points']) > MAX_POINTS:
        fail('err.too_many_points', MAX_POINTS)
    if values['module'] <= 1e-6:
        fail('err.module_positive')
    if values['face_width'] <= 1e-6:
        fail('err.width_positive')
    if values['ratio'] <= 1e-6:
        fail('err.ratio_positive')
    if values['backlash'] < 0.0:
        fail('err.backlash_negative')

    count = first_teeth(values)
    if count < pg.MIN_TEETH:
        fail('err.teeth_low', pg.MIN_TEETH)
    if count > pg.MAX_TEETH:
        fail('err.teeth_high', pg.MAX_TEETH)

    angle = values['pressure_angle_deg']
    if angle < 10.0 or angle > 35.0:
        fail('err.pressure_range')
    if values['tooth_style'] != pg.TEETH_STRAIGHT:
        helix = values['helix_angle_deg']
        if helix <= 0.0 or helix >= 80.0:
            fail('err.helix_range')

    # Points on different heights cannot mesh - gears have to be coplanar.
    base = values['points'][0][2]
    for _, _, z in values['points']:
        if abs(z - base) > 1e-4:
            fail('err.points_not_coplanar')

    if len(values['points']) > 1:
        for index in range(len(values['points']) - 1):
            here = values['points'][index]
            following = values['points'][index + 1]
            gap = math.hypot(following[0] - here[0], following[1] - here[1])
            if gap < values['module'] * pg.MIN_TEETH:
                fail('err.points_too_close')

    if values['bore_diameter'] < 0.0:
        fail('err.bore_negative')
    if values['backlash'] >= values['module'] * math.pi / 2.0:
        fail('err.backlash_too_big')


# ================================================================ building ===

def build_result(values, is_preview=False):
    """Do the actual work. Everything is already validated at this point."""
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        fail('err.no_design')

    placements, _warnings = plan(values)
    base_z = values['points'][0][2]

    if is_preview and values['preview'] == PREVIEW_CIRCLES:
        build.preview_circles(design, placements, base_z)
        return

    try:
        _bodies, notes = build.build(design, placements, values, base_z)
    except build.BuildError as error:
        fail(error.key, *error.params)

    # Things worth telling the user about that are not failures. Only on the
    # real run - a preview popping up a dialog per keystroke would be torture.
    if notes and not is_preview:
        app.userInterface.messageBox('\n'.join(T(key) for key in notes),
                                     T('cmd.name'))


# ============================================================== the dialog ===

def _add_dropdown(inputs, input_id, label, keys, label_keys, selected):
    dropdown = inputs.addDropDownCommandInput(
        input_id, label, adsk.core.DropDownStyles.TextListDropDownStyle)
    for index, key in enumerate(keys):
        dropdown.listItems.add(T(label_keys[index]), key == selected)
    if dropdown.selectedItem is None and dropdown.listItems.count:
        dropdown.listItems.item(0).isSelected = True
    return dropdown


def build_inputs(inputs):
    """Lay out the dialog. Every label comes from the text catalogue."""
    selection = inputs.addSelectionInput(IN_POINTS, T('in.points'), T('in.points.prompt'))
    for filter_name in ('SketchPoints', 'ConstructionPoints', 'Vertices'):
        selection.addSelectionFilter(filter_name)
    selection.setSelectionLimits(1, MAX_POINTS)
    selection.tooltip = T('in.points.tip')

    real = adsk.core.ValueInput.createByReal

    # -- print setup --------------------------------------------------------
    group = inputs.addGroupCommandInput(GROUP_PRINT, T('grp.print')).children
    _add_dropdown(group, IN_NOZZLE, T('in.nozzle'), NOZZLE_KEYS,
                  ['in.nozzle.%s' % key for key in NOZZLE_KEYS], _last[IN_NOZZLE])
    factor = group.addValueInput(IN_FACTOR, T('in.factor'), '',
                                 real(_last[IN_FACTOR]))
    factor.tooltip = T('in.factor.tip')
    module = group.addValueInput(IN_MODULE, T('in.module'), 'mm',
                                 real(_last[IN_MODULE]))
    module.isEnabled = _last[IN_NOZZLE] == NOZZLE_CUSTOM
    group.addValueInput(IN_BACKLASH, T('in.backlash'), 'mm',
                        real(_last[IN_BACKLASH])).tooltip = T('in.backlash.tip')
    group.addValueInput(IN_WIDTH, T('in.width'), 'mm', real(_last[IN_WIDTH]))

    # -- teeth --------------------------------------------------------------
    group = inputs.addGroupCommandInput(GROUP_TEETH, T('grp.teeth')).children
    _add_dropdown(group, IN_STYLE, T('in.style'), STYLE_KEYS,
                  ['in.style.%s' % key for key in STYLE_KEYS], _last[IN_STYLE])
    helix = group.addValueInput(IN_HELIX, T('in.helix'), 'deg', real(_last[IN_HELIX]))
    helix.isEnabled = _last[IN_STYLE] != pg.TEETH_STRAIGHT
    helix.tooltip = T('in.helix.tip')
    group.addValueInput(IN_PRESSURE, T('in.pressure'), 'deg',
                        real(_last[IN_PRESSURE])).tooltip = T('in.pressure.tip')
    group.addBoolValueInput(IN_SHIFT, T('in.shift'), True, '',
                            _last[IN_SHIFT]).tooltip = T('in.shift.tip')

    # -- the train ----------------------------------------------------------
    group = inputs.addGroupCommandInput(GROUP_TRAIN, T('grp.train')).children
    _add_dropdown(group, IN_SIZE_MODE, T('in.size_mode'), SIZE_KEYS,
                  ['in.size_mode.%s' % key for key in SIZE_KEYS], _last[IN_SIZE_MODE])
    teeth_input = group.addValueInput(IN_FIRST, T('in.first'), '',
                                      real(_last[IN_FIRST]))
    diameter_input = group.addValueInput(IN_FIRST_DIA, T('in.first_dia'), 'mm',
                                         real(_last[IN_FIRST_DIA]))
    teeth_input.isVisible = _last[IN_SIZE_MODE] == SIZE_TEETH
    diameter_input.isVisible = _last[IN_SIZE_MODE] == SIZE_DIAMETER
    group.addValueInput(IN_RATIO, T('in.ratio'), '',
                        real(_last[IN_RATIO])).tooltip = T('in.ratio.tip')
    _add_dropdown(group, IN_MODE, T('in.mode'), MODE_KEYS,
                  ['in.mode.%s' % key for key in MODE_KEYS], _last[IN_MODE])
    pair = group.addBoolValueInput(IN_PAIR, T('in.pair'), True, '', _last[IN_PAIR])
    pair.tooltip = T('in.pair.tip')
    pair_angle = group.addValueInput(IN_PAIR_ANGLE, T('in.pair_angle'), 'deg',
                                     real(_last[IN_PAIR_ANGLE]))
    pair_angle.tooltip = T('in.pair_angle.tip')

    # -- output -------------------------------------------------------------
    group = inputs.addGroupCommandInput(GROUP_OUTPUT, T('grp.output')).children
    group.addValueInput(IN_BORE, T('in.bore'), 'mm',
                        real(_last[IN_BORE])).tooltip = T('in.bore.tip')
    group.addBoolValueInput(IN_COMPONENTS, T('in.components'), True, '',
                            _last[IN_COMPONENTS])
    _add_dropdown(group, IN_PREVIEW, T('in.preview'), PREVIEW_KEYS,
                  ['in.preview.%s' % key for key in PREVIEW_KEYS], _last[IN_PREVIEW])

    info = inputs.addTextBoxCommandInput(IN_INFO, '', '', 8, True)
    info.isFullWidth = True
    return selection


def _summary(values):
    """The read-only report under the dialog: what will actually be built."""
    try:
        placements, warnings = plan(values)
    except core.AddInError as error:
        return '<div>%s</div>' % str(error)
    except Exception:
        return ''

    rows = ['<b>%s</b> %.3f mm &nbsp; <b>%s</b> %.2f mm'
            % (T('info.module'), values['module'],
               T('info.nozzle'), values['nozzle'])]
    if placements[0].spec.profile_shift > 1e-6:
        rows[0] += ' &nbsp; <b>x</b> %.2f' % placements[0].spec.profile_shift

    parts = []
    for index, placement in enumerate(placements):
        spec = placement.spec
        piece = '%d: z=%d, &#8960;%.1f' % (index + 1, spec.teeth,
                                           2.0 * spec.pitch_radius)
        if index:
            previous = placements[index - 1]
            gap = math.hypot(placement.x - previous.x, placement.y - previous.y)
            piece += ' (a=%.2f)' % gap
        parts.append(piece)
    rows.append('&nbsp;&nbsp;'.join(parts))

    if len(placements) > 1:
        achieved = placements[-1].spec.teeth / float(placements[0].spec.teeth)
        rows.append('<b>%s</b> %.4f : 1' % (T('info.ratio'), achieved))

    # Asking the tip radius rather than building the outline: the answer is the
    # same and the report is redrawn on every keystroke.
    warnings = list(warnings)
    for placement in placements:
        if pg.truncated_tip_radius(placement.spec)[1]:
            warnings.append('warn.tip_truncated')
            break
    for key in warnings:
        rows.append('<i>%s</i>' % T(key))
    return '<div>%s</div>' % '<br/>'.join(rows)


def remember(values, inputs):
    """Carry settings over to the next invocation within this session."""
    for input_id in (IN_FACTOR, IN_MODULE, IN_HELIX, IN_PRESSURE, IN_WIDTH,
                     IN_BACKLASH, IN_SHIFT, IN_FIRST, IN_FIRST_DIA, IN_RATIO,
                     IN_PAIR, IN_PAIR_ANGLE, IN_BORE, IN_COMPONENTS):
        item = inputs.itemById(input_id)
        if item is not None:
            _last[input_id] = item.value
    _last[IN_NOZZLE] = _dropdown_key(inputs.itemById(IN_NOZZLE), NOZZLE_KEYS, '0.4')
    _last[IN_STYLE] = values['tooth_style']
    _last[IN_SIZE_MODE] = values['size_mode']
    _last[IN_MODE] = values['mode']
    _last[IN_PREVIEW] = values['preview']


def on_input_changed(inputs, changed):
    """React to one field to enable, disable or adjust another."""
    global _updating
    nozzle_key = _dropdown_key(inputs.itemById(IN_NOZZLE), NOZZLE_KEYS, '0.4')
    custom = nozzle_key == NOZZLE_CUSTOM

    module_input = inputs.itemById(IN_MODULE)
    module_input.isEnabled = custom
    inputs.itemById(IN_FACTOR).isEnabled = not custom

    style = _dropdown_key(inputs.itemById(IN_STYLE), STYLE_KEYS, pg.TEETH_STRAIGHT)
    inputs.itemById(IN_HELIX).isEnabled = style != pg.TEETH_STRAIGHT

    size_mode = _dropdown_key(inputs.itemById(IN_SIZE_MODE), SIZE_KEYS, SIZE_TEETH)
    inputs.itemById(IN_FIRST).isVisible = size_mode == SIZE_TEETH
    inputs.itemById(IN_FIRST_DIA).isVisible = size_mode == SIZE_DIAMETER

    # A second gear only makes sense when there is no second point to put one
    # on; with a train the points already say how many gears there are.
    single = inputs.itemById(IN_POINTS).selectionCount <= 1
    inputs.itemById(IN_PAIR).isEnabled = single
    inputs.itemById(IN_PAIR_ANGLE).isEnabled = single and inputs.itemById(IN_PAIR).value
    inputs.itemById(IN_MODE).isEnabled = not single

    _updating = True
    try:
        # Keep the module box showing what the nozzle implies while it is the
        # nozzle driving it, so the number is never a stale leftover.
        if not custom and changed.id in (IN_NOZZLE, IN_FACTOR):
            derived = pg.module_for_nozzle(float(nozzle_key),
                                           inputs.itemById(IN_FACTOR).value)
            module_input.value = derived * build.MM
        info = inputs.itemById(IN_INFO)
        if info is not None:
            info.formattedText = _summary(read_inputs(inputs))
    finally:
        _updating = False


# ========================================================= END OF TEMPLATE ====

def _run_command(inputs, is_preview=False):
    values = read_inputs(inputs)
    build_result(values, is_preview)      # validates by way of plan()
    return values


class ExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        ui = adsk.core.Application.get().userInterface
        try:
            inputs = args.firingEvent.sender.commandInputs
            values = _run_command(inputs)
            remember(values, inputs)
        except core.AddInError as err:
            ui.messageBox(str(err), T('cmd.name'))
        except Exception:
            core.report(ui, S, 'msg.exec_failed')


class PreviewHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        try:
            inputs = args.firingEvent.sender.commandInputs
            values = read_inputs(inputs)
            if values['preview'] == PREVIEW_OFF:
                return
            validate(values)
            build_result(values, is_preview=True)
            # False makes Fusion run execute again for the real result. The
            # circle preview is never the final answer, and rebuilding the full
            # geometry once more on OK is cheaper than getting this wrong.
            args.isValidResult = False
        except Exception:
            # Fires on every keystroke, including half-typed values. Staying
            # silent is deliberate; validateInputs is what explains the problem.
            pass


class ValidateHandler(adsk.core.ValidateInputsEventHandler):
    def notify(self, args):
        try:
            # plan() rather than validate(): the checks that need the finished
            # train live there, and planning is cheap - no profile is built.
            plan(read_inputs(args.firingEvent.sender.commandInputs))
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
            command.okButtonText = T('cmd.ok')
            inputs = command.commandInputs

            # Whatever was selected before the button was pressed, in the order
            # it was picked - which is the order the train is built in.
            preselected = []
            for index in range(ui.activeSelections.count):
                entity = ui.activeSelections.item(index).entity
                if entity and _entity_point(entity) is not None:
                    preselected.append(entity)

            selection = build_inputs(inputs)
            for entity in preselected[:MAX_POINTS]:
                try:
                    selection.addSelection(entity)
                except Exception:
                    pass

            _handlers.add(command.execute, ExecuteHandler())
            _handlers.add(command.executePreview, PreviewHandler())
            _handlers.add(command.validateInputs, ValidateHandler())
            _handlers.add(command.inputChanged, InputChangedHandler())

            # Fill the report straight away, so the dialog opens describing
            # what the preselection is about to produce.
            try:
                inputs.itemById(IN_INFO).formattedText = _summary(read_inputs(inputs))
            except Exception:
                pass
        except Exception:
            core.report(ui, S, 'msg.dialog_failed')


def run(context):
    global _control
    ui = None
    try:
        ui = adsk.core.Application.get().userInterface
        S.load(core.detect_language())

        stale = ui.commandDefinitions.itemById(CMD_ID)
        if stale:
            stale.deleteMe()

        icons = RESOURCE_FOLDER if os.path.isdir(RESOURCE_FOLDER) else ''
        definition = ui.commandDefinitions.addButtonDefinition(
            CMD_ID,
            core.display_name(T('cmd.name'), core.read_version(_DIR, 'PrintGear')),
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
