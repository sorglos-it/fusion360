# -*- coding: utf-8 -*-
"""
Fusion geometry for PrintGear.

Every gear is modelled at the origin and only then moved to where it belongs.
That is not cosmetic: a sweep path has to run through the gear axis, and
keeping the axis on the origin means the component's own XZ plane already is
that path, with no construction planes per gear.

Lengths arriving from printgear_math are in millimetres; everything handed to
the API is in centimetres, which is Fusion's internal unit. MM is the only
place that conversion happens.
"""

import math

import adsk.core
import adsk.fusion

import printgear_math as pg

MM = 0.1        # millimetres -> centimetres


class BuildError(Exception):
    """Geometry that could not be created, carrying a message key."""

    def __init__(self, key, *params):
        self.key = key
        self.params = params
        Exception.__init__(self, key)


# ------------------------------------------------------------------ helpers --

def _point(x_mm, y_mm, z_mm=0.0):
    return adsk.core.Point3D.create(x_mm * MM, y_mm * MM, z_mm * MM)


def _outline_sketch(component, plane, placement, name):
    """The gear outline as one closed spline.

    A single closed spline rather than arc/spline segments per tooth: it cannot
    fail to close, and Fusion takes far longer over a few hundred separate
    curves than over one curve with a few hundred points.
    """
    sketch = component.sketches.add(plane)
    sketch.name = name
    sketch.isComputeDeferred = True
    try:
        profile_points = pg.tooth_profile(placement.spec)
        angle = placement.rotation
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        collection = adsk.core.ObjectCollection.create()
        for x, y in profile_points:
            collection.add(_point(x * cos_a - y * sin_a, x * sin_a + y * cos_a))
        spline = sketch.sketchCurves.sketchFittedSplines.add(collection)
        try:
            spline.isClosed = True
        except Exception:
            pass
    finally:
        # Never leave the sketch deferred - an exception here would otherwise
        # freeze the sketch for good.
        sketch.isComputeDeferred = False

    # Whether isClosed took is only visible once the sketch has recomputed, and
    # a build that silently did nothing is worse than one that failed loudly.
    # So judge it by the profile and close the seam by hand if there is none.
    if sketch.profiles.count == 0:
        try:
            sketch.sketchCurves.sketchLines.addByTwoPoints(
                spline.endSketchPoint, spline.startSketchPoint)
        except Exception:
            pass
    if sketch.profiles.count == 0:
        raise BuildError('err.profile_failed')
    return sketch


def _largest_profile(sketch):
    """The outer profile. With a closed outline there is normally just one."""
    best, best_area = None, -1.0
    for i in range(sketch.profiles.count):
        profile = sketch.profiles.item(i)
        try:
            area = profile.areaProperties(
                adsk.fusion.CalculationAccuracy.LowCalculationAccuracy).area
        except Exception:
            area = 0.0
        if area > best_area:
            best, best_area = profile, area
    return best


def _offset_plane(component, offset_mm, name):
    planes = component.constructionPlanes
    plane_input = planes.createInput()
    plane_input.setByOffset(component.xYConstructionPlane,
                            adsk.core.ValueInput.createByReal(offset_mm * MM))
    plane = planes.add(plane_input)
    plane.name = name
    plane.isLightBulbOn = False
    return plane


def _axis_path(component, from_mm, to_mm):
    """A straight path along the gear axis, for the swept helical bodies.

    Built on the component's XZ plane, which passes through the axis because
    the gear is modelled at the origin. modelToSketchSpace keeps this correct
    whatever the plane's own axis convention is.
    """
    sketch = component.sketches.add(component.xZConstructionPlane)
    sketch.name = 'PrintGear axis'
    start = sketch.modelToSketchSpace(_point(0.0, 0.0, from_mm))
    end = sketch.modelToSketchSpace(_point(0.0, 0.0, to_mm))
    line = sketch.sketchCurves.sketchLines.addByTwoPoints(start, end)
    sketch.isVisible = False
    return component.features.createPath(line, False)


# -------------------------------------------------------------- gear bodies --

def _extrude(component, profile, width_mm):
    extrudes = component.features.extrudeFeatures
    extrude_input = extrudes.createInput(
        profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setDistanceExtent(
        False, adsk.core.ValueInput.createByReal(width_mm * MM))
    return extrudes.add(extrude_input).bodies.item(0)


def _sweep_twisted(component, profile, from_mm, to_mm, twist):
    """Swept body with a twist - an exact helicoid, one sketch per gear."""
    path = _axis_path(component, from_mm, to_mm)
    sweeps = component.features.sweepFeatures
    sweep_input = sweeps.createInput(
        profile, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    sweep_input.twistAngle = adsk.core.ValueInput.createByReal(twist)
    return sweeps.add(sweep_input).bodies.item(0)


def _loft_twisted(component, placement, from_mm, to_mm, twist, sections=8):
    """Fallback for helical gears when the swept twist is refused.

    Approximates the helicoid by lofting through rotated copies of the outline.
    Costs one sketch per section, so it is the slow road, but it depends on
    nothing beyond loft itself.
    """
    lofts = component.features.loftFeatures
    loft_input = lofts.createInput(
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    base_rotation = placement.rotation
    try:
        for index in range(sections + 1):
            fraction = index / float(sections)
            height = from_mm + (to_mm - from_mm) * fraction
            plane = _offset_plane(component, height, 'PrintGear section')
            placement.rotation = base_rotation + twist * fraction
            sketch = _outline_sketch(component, plane, placement,
                                     'PrintGear section %d' % index)
            sketch.isVisible = False
            loft_input.loftSections.add(_largest_profile(sketch))
    finally:
        placement.rotation = base_rotation
    return lofts.add(loft_input).bodies.item(0)


def _mirror_join(component, body, plane):
    """Mirror a body about a plane and weld the two halves into one.

    This is how the herringbone is made. Mirroring is a geometric operation
    with no sign convention to get wrong, so the two helices are guaranteed to
    oppose each other and meet in a point at the joint.
    """
    entities = adsk.core.ObjectCollection.create()
    entities.add(body)
    mirrors = component.features.mirrorFeatures
    mirror = mirrors.add(mirrors.createInput(entities, plane))

    tools = adsk.core.ObjectCollection.create()
    for i in range(mirror.bodies.count):
        other = mirror.bodies.item(i)
        if other != body:
            tools.add(other)
    if tools.count == 0:
        return body
    combines = component.features.combineFeatures
    combine_input = combines.createInput(body, tools)
    combine_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    combine_input.isKeepToolBodies = False
    combines.add(combine_input)
    return body


def _gear_body(component, placement, options):
    """One finished gear body, sitting at the origin, base face on z = 0."""
    width = options['face_width']
    style = options['tooth_style']
    helix = math.radians(options.get('helix_angle_deg', 0.0))

    if style == pg.TEETH_STRAIGHT or abs(helix) < 1e-9:
        sketch = _outline_sketch(component, component.xYConstructionPlane,
                                 placement, 'PrintGear profile')
        return _extrude(component, _largest_profile(sketch), width)

    if style == pg.TEETH_HERRINGBONE:
        # Half the width per helix, so the overall face width is what was asked
        # for. The sketch sits on the joint plane and the lower half is the
        # mirror image of the upper one.
        half = width / 2.0
        twist = placement.helix_sign * pg.helix_twist(placement.spec, half, helix)
        plane = _offset_plane(component, half, 'PrintGear joint')
        sketch = _outline_sketch(component, plane, placement, 'PrintGear profile')
        profile = _largest_profile(sketch)
        try:
            body = _sweep_twisted(component, profile, half, width, twist)
        except Exception:
            body = _loft_twisted(component, placement, half, width, twist)
        return _mirror_join(component, body, plane)

    twist = placement.helix_sign * pg.helix_twist(placement.spec, width, helix)
    sketch = _outline_sketch(component, component.xYConstructionPlane,
                             placement, 'PrintGear profile')
    profile = _largest_profile(sketch)
    try:
        return _sweep_twisted(component, profile, 0.0, width, twist)
    except Exception:
        return _loft_twisted(component, placement, 0.0, width, twist)


def _bore(component, body, diameter_mm, width_mm):
    """Cut the shaft bore.

    Cut afterwards rather than as an island in the outline, so a helical gear
    gets a straight bore instead of a twisted one.
    """
    if diameter_mm <= 1e-6:
        return
    sketch = component.sketches.add(component.xYConstructionPlane)
    sketch.name = 'PrintGear bore'
    sketch.sketchCurves.sketchCircles.addByCenterRadius(
        _point(0.0, 0.0), diameter_mm * MM / 2.0)
    extrudes = component.features.extrudeFeatures
    extrude_input = extrudes.createInput(
        sketch.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
    # Restricted to this gear, so a run without components cannot bore through
    # a neighbour that happens to be in the way.
    extrude_input.participantBodies = [body]
    extrude_input.setAllExtent(adsk.fusion.ExtentDirections.SymmetricExtentDirection)
    extrudes.add(extrude_input)


# ----------------------------------------------------------------- assembly --

def _placement_matrix(placement, base_z_mm):
    matrix = adsk.core.Matrix3D.create()
    matrix.translation = adsk.core.Vector3D.create(
        placement.x * MM, placement.y * MM, base_z_mm * MM)
    return matrix


def build(design, placements, options, base_z_mm=0.0):
    """Build every planned gear. Returns (bodies, notes).

    as_components decides between one component per gear - which is what you
    want for an assembly, and what lets each gear be exported on its own - and
    plain bodies in whatever component is active.

    A part design document refuses to hold more than one component, and there
    is no property that says so in advance, so the first component is a probe:
    if Fusion turns it down, the whole run falls back to bodies and says so in
    notes rather than dying half built.
    """
    root = design.activeComponent
    as_components = options.get('as_components', True)
    bodies = []
    notes = []

    for index, placement in enumerate(placements):
        name = 'Gear %d (z%d)' % (index + 1, placement.spec.teeth)
        component = root
        if as_components:
            try:
                occurrence = root.occurrences.addNewComponent(
                    _placement_matrix(placement, base_z_mm))
                occurrence.component.name = name
                component = occurrence.component
            except Exception:
                as_components = False
                component = root
                notes.append('msg.single_component_doc')

        body = _gear_body(component, placement, options)
        _bore(component, body, options.get('bore_diameter', 0.0),
              options['face_width'])
        body.name = name
        bodies.append(body)

        if not as_components:
            _move_body(component, body, _placement_matrix(placement, base_z_mm))
    return bodies, notes


def _move_body(component, body, matrix):
    """Move a body by a matrix, across both generations of the move API.

    createInput2 is the current form; the older createInput took the transform
    directly and is still what some builds expose.
    """
    moves = component.features.moveFeatures
    entities = adsk.core.ObjectCollection.create()
    entities.add(body)
    try:
        move_input = moves.createInput2(entities)
        move_input.defineAsFreeMove(matrix)
    except Exception:
        move_input = moves.createInput(entities, matrix)
    moves.add(move_input)


def preview_circles(design, placements, base_z_mm=0.0):
    """Cheap preview: tip and pitch circle of every gear.

    The full geometry takes seconds per gear, which makes it useless as a live
    preview. Circles show the two things being tuned - how big each gear is and
    where it lands - and redraw instantly.
    """
    root = design.activeComponent
    sketch = root.sketches.add(root.xYConstructionPlane)
    sketch.name = 'PrintGear preview'
    sketch.isComputeDeferred = True
    try:
        circles = sketch.sketchCurves.sketchCircles
        for placement in placements:
            centre = _point(placement.x, placement.y, base_z_mm)
            spec = placement.spec
            circles.addByCenterRadius(centre, spec.tip_radius * MM)
            pitch = circles.addByCenterRadius(centre, spec.pitch_radius * MM)
            pitch.isConstruction = True
    finally:
        sketch.isComputeDeferred = False
    return sketch
