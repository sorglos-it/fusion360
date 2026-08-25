# -*- coding: utf-8 -*-
"""
Involute gear mathematics for PrintGear.

Deliberately free of any adsk import, so the whole geometry can be exercised
from a normal Python installation - see tools/test_geometry.py.

Everything in here is in MILLIMETRES and RADIANS unless a name says otherwise.
The Fusion side is the only place that converts to centimetres, which is what
the API expects internally.
"""

import math

# --------------------------------------------------------------- print rules --

# Nozzle diameters worth offering. Below 0.2 the extrusion width stops being
# the limiting factor for tooth strength, above 1.0 the module is so coarse
# that layer height decides the surface quality instead.
NOZZLE_SIZES = (0.2, 0.4, 0.6, 0.8, 1.0)

# module = nozzle * factor. 2.5 puts roughly five extrusions across the root of
# a 20 tooth gear, which is where printed gears stop shearing their teeth off.
# 2.0 is the fine end, 3.0 the sturdy end.
MODULE_FACTOR_MIN = 1.5
MODULE_FACTOR_MAX = 4.0
DEFAULT_MODULE_FACTOR = 2.5

# A tooth tip narrower than one extrusion has nothing the slicer can lay down,
# so the tip is truncated until it is at least this many nozzle widths across.
# A textbook tooth is around 0.65 * module at the tip, so at the recommended
# module factor this never fires; it is the safety net for the small tooth
# counts where profile shift sharpens the tooth to a point.
MIN_TIP_EXTRUSIONS = 1.0

# Largest chord error the outline may have against the true involute. Two
# hundredths of a millimetre is an order of magnitude below what any nozzle can
# resolve, and it is what keeps the point count sane.
CHORD_TOLERANCE = 0.02

# Hard ceiling on the outline. Fusion slows to a crawl on splines past a couple
# of thousand points, so beyond this the tolerance is relaxed instead.
MAX_PROFILE_POINTS = 1800

# z_min = 2 * addendum / sin^2(alpha): below it the involute is undercut and
# the root goes thin. Profile shift is what buys those teeth back.
UNDERCUT_LIMIT_FACTOR = 2.0

MIN_TEETH = 5
MAX_TEETH = 400

# Root clearance as a multiple of the module. The textbook value is 0.25; FDM
# wants a little more, because the mating tip prints slightly over size and the
# root slightly under.
DEFAULT_CLEARANCE_FACTOR = 0.35

# Root fillet radius as a multiple of the module. Rounder than the 0.25 of a
# cut gear - a printed tooth breaks at the root, and the fillet is free.
DEFAULT_FILLET_FACTOR = 0.38

DEFAULT_PRESSURE_ANGLE_DEG = 20.0
DEFAULT_BACKLASH = 0.25         # mm, total between two mating gears
DEFAULT_HELIX_ANGLE_DEG = 45.0

# Tooth flavours.
TEETH_STRAIGHT = 'straight'
TEETH_HELICAL = 'helical'
TEETH_HERRINGBONE = 'herringbone'

EPS = 1e-9


def module_for_nozzle(nozzle, factor=DEFAULT_MODULE_FACTOR):
    """Module a nozzle of that diameter can actually print.

    The whole point of the add-in: nobody cares what the module is, they care
    whether the teeth survive. Tying it to the nozzle makes that automatic.
    """
    return nozzle * factor


# ------------------------------------------------------------------ involute --

def inv(angle):
    """Involute function, inv(a) = tan(a) - a."""
    return math.tan(angle) - angle


def inv_inverse(value, guess=None):
    """Angle whose involute is value. Newton, converges in a handful of steps.

    Needed for the working pressure angle of a profile shifted pair, which is
    what sets the real centre distance.
    """
    if value <= 0.0:
        return 0.0
    angle = guess if guess is not None else max(0.05, (3.0 * value) ** (1.0 / 3.0))
    for _ in range(60):
        tan_a = math.tan(angle)
        f = tan_a - angle - value
        derivative = tan_a * tan_a           # d/da (tan a - a)
        if derivative < EPS:
            break
        step = f / derivative
        angle -= step
        angle = min(max(angle, 1e-6), 1.5533)        # stay clear of pi/2
        if abs(step) < 1e-14:
            break
    return angle


def min_teeth_without_undercut(pressure_angle):
    """Smallest tooth count that avoids undercut at this pressure angle."""
    sin_a = math.sin(pressure_angle)
    if sin_a < EPS:
        return MAX_TEETH
    return UNDERCUT_LIMIT_FACTOR / (sin_a * sin_a)


def auto_profile_shift(teeth, pressure_angle):
    """Profile shift factor that just avoids undercut, 0 when not needed.

    x = (z_min - z) / z_min is the standard rule of thumb, and it is what lets
    a printed gear go down to eight or nine teeth without a wasp waist.
    """
    z_min = min_teeth_without_undercut(pressure_angle)
    if teeth >= z_min:
        return 0.0
    return (z_min - teeth) / z_min


# ---------------------------------------------------------------- gear specs --

class GearSpec(object):
    """One gear, fully determined. Everything derived is computed on demand."""

    def __init__(self, module, teeth, pressure_angle_deg=DEFAULT_PRESSURE_ANGLE_DEG,
                 profile_shift=0.0, backlash=DEFAULT_BACKLASH,
                 clearance_factor=DEFAULT_CLEARANCE_FACTOR,
                 addendum_factor=1.0, fillet_factor=DEFAULT_FILLET_FACTOR,
                 nozzle=0.4):
        self.module = float(module)
        self.teeth = int(teeth)
        self.pressure_angle = math.radians(pressure_angle_deg)
        self.profile_shift = float(profile_shift)
        self.backlash = float(backlash)
        self.clearance_factor = float(clearance_factor)
        self.addendum_factor = float(addendum_factor)
        self.fillet_factor = float(fillet_factor)
        self.nozzle = float(nozzle)

        # set by tooth_profile() when the tip had to be cut back
        self.tip_truncated = False

    # -- diameters ----------------------------------------------------------

    @property
    def pitch_radius(self):
        return self.module * self.teeth / 2.0

    @property
    def base_radius(self):
        return self.pitch_radius * math.cos(self.pressure_angle)

    @property
    def tip_radius(self):
        return self.pitch_radius + self.module * (
            self.addendum_factor + self.profile_shift)

    @property
    def root_radius(self):
        return self.pitch_radius - self.module * (
            self.addendum_factor + self.clearance_factor - self.profile_shift)

    @property
    def pitch_angle(self):
        """Angle from one tooth centre to the next."""
        return 2.0 * math.pi / self.teeth

    @property
    def tooth_thickness(self):
        """Circular tooth thickness at the pitch circle, backlash already off.

        Half the backlash comes off this gear and half off the one it meets, so
        a pair ends up with exactly the requested play.
        """
        nominal = self.module * (
            math.pi / 2.0
            + 2.0 * self.profile_shift * math.tan(self.pressure_angle))
        return nominal - self.backlash / 2.0

    def half_tooth_angle(self, radius):
        """Half the tooth thickness, as an angle, at any radius on the flank.

        s_r = 2r (s/d + inv(alpha) - inv(alpha_r)) is the standard relation;
        this is half of it divided by r.
        """
        rb = self.base_radius
        if radius <= rb:
            alpha_r = 0.0
        else:
            alpha_r = math.acos(max(-1.0, min(1.0, rb / radius)))
        return (self.tooth_thickness / (2.0 * self.pitch_radius)
                + inv(self.pressure_angle) - inv(alpha_r))

    @property
    def min_tip_thickness(self):
        return MIN_TIP_EXTRUSIONS * self.nozzle


def working_center_distance(spec_a, spec_b):
    """Centre distance two gears actually run at.

    With no profile shift this is the textbook m (z1 + z2) / 2. With shift the
    pair rolls on a larger pressure angle and pushes apart; ignoring that is
    the classic reason a generated gear train binds.
    """
    module = spec_a.module
    z_sum = spec_a.teeth + spec_b.teeth
    reference = module * z_sum / 2.0
    shift_sum = spec_a.profile_shift + spec_b.profile_shift
    if abs(shift_sum) < 1e-12:
        return reference
    alpha = spec_a.pressure_angle
    inv_w = inv(alpha) + 2.0 * shift_sum * math.tan(alpha) / z_sum
    alpha_w = inv_inverse(inv_w, guess=alpha)
    return reference * math.cos(alpha) / math.cos(alpha_w)


# ------------------------------------------------------------ tooth outline --

def _flank_point(spec, radius, side):
    """One point on a flank. side=+1 is the leading flank, -1 the trailing."""
    angle = side * spec.half_tooth_angle(radius)
    return (radius * math.cos(angle), radius * math.sin(angle))


def _flank_direction(spec, radius, side):
    """Unit tangent of the involute at that radius, pointing outwards.

    In the local (radial, circumferential) frame the involute tangent is
    proportional to (1, -t) with t = tan(alpha_r). That stays well behaved
    right down to the base circle, where the tangent is purely radial, which is
    what makes the root fillet below work for small and large gears alike.
    """
    rb = spec.base_radius
    t = math.sqrt(max(0.0, (radius / rb) ** 2 - 1.0)) if rb > EPS else 0.0
    angle = side * spec.half_tooth_angle(radius)
    e_r = (math.cos(angle), math.sin(angle))
    e_t = (-math.sin(angle), math.cos(angle))
    norm = math.sqrt(1.0 + t * t)
    radial, circumferential = 1.0 / norm, side * (-t) / norm
    return (e_r[0] * radial + e_t[0] * circumferential,
            e_r[1] * radial + e_t[1] * circumferential)


def _root_fillet(spec, radius_form, side, fillet_radius):
    """Arc joining the bottom of the flank to the root circle.

    Solves for a circle of that radius tangent to the flank tangent line and
    tangent inside the root circle. Returns (centre, on_flank, on_root), or
    None when no such circle fits - the signal to try a smaller radius.
    """
    p0 = _flank_point(spec, radius_form, side)
    outward = _flank_direction(spec, radius_form, side)
    u = (-outward[0], -outward[1])                  # down the flank

    # normal pointing into the tooth space, away from the tooth centre
    n = (-u[1], u[0])
    if (n[0] * -p0[1] + n[1] * p0[0]) * side < 0.0:
        n = (u[1], -u[0])

    rf = spec.root_radius
    rho = fillet_radius
    # |p0 + s u + rho n| = rf + rho, solved for s
    pu = p0[0] * u[0] + p0[1] * u[1]
    pn = p0[0] * n[0] + p0[1] * n[1]
    p2 = p0[0] * p0[0] + p0[1] * p0[1]
    c0 = p2 + rho * rho + 2.0 * rho * pn - (rf + rho) ** 2
    disc = pu * pu - c0
    if disc < 0.0:
        return None
    root = math.sqrt(disc)
    candidates = [s for s in (-pu + root, -pu - root) if s >= -1e-7]
    if not candidates:
        return None
    s = min(candidates)

    centre = (p0[0] + s * u[0] + rho * n[0], p0[1] + s * u[1] + rho * n[1])
    length = math.hypot(centre[0], centre[1])
    if length < EPS:
        return None
    on_flank = (p0[0] + s * u[0], p0[1] + s * u[1])
    on_root = (centre[0] * rf / length, centre[1] * rf / length)
    if math.hypot(on_flank[0], on_flank[1]) < rf - 1e-6:
        return None                                  # tangent point below the root
    return centre, on_flank, on_root


def _arc_points(centre, start, end, count):
    """Points along the short arc from start to end about centre, ends included."""
    radius = math.hypot(start[0] - centre[0], start[1] - centre[1])
    a0 = math.atan2(start[1] - centre[1], start[0] - centre[0])
    a1 = math.atan2(end[1] - centre[1], end[0] - centre[0])
    sweep = a1 - a0
    while sweep > math.pi:
        sweep -= 2.0 * math.pi
    while sweep < -math.pi:
        sweep += 2.0 * math.pi
    out = []
    for i in range(count + 1):
        angle = a0 + sweep * i / float(count)
        out.append((centre[0] + radius * math.cos(angle),
                    centre[1] + radius * math.sin(angle)))
    return out


def truncated_tip_radius(spec):
    """Tip radius, pulled in if the teeth would otherwise come to a point.

    Small tooth counts with a lot of profile shift run out of tooth before they
    reach the nominal tip circle. Printing that leaves a knife edge no nozzle
    can lay down, so the tip is cut back to two extrusion widths.
    """
    ra = spec.tip_radius
    target = spec.min_tip_thickness
    if 2.0 * ra * spec.half_tooth_angle(ra) >= target:
        return ra, False
    low = spec.base_radius + 1e-4
    high = ra
    if 2.0 * low * spec.half_tooth_angle(low) < target:
        return low, True            # nothing fits; the caller validates the count
    for _ in range(80):
        mid = 0.5 * (low + high)
        if 2.0 * mid * spec.half_tooth_angle(mid) >= target:
            low = mid
        else:
            high = mid
    return low, True


def _arc_segments(radius, span, tolerance, minimum=1, maximum=60):
    """Segments an arc needs to stay within the chord tolerance.

    The sagitta of a chord subtending theta is r (1 - cos(theta/2)), so the
    largest angle allowed is 2 acos(1 - tol/r).
    """
    span = abs(span)
    if radius <= tolerance or span <= EPS:
        return minimum
    theta = 2.0 * math.acos(max(-1.0, 1.0 - tolerance / radius))
    if theta <= EPS:
        return maximum
    return max(minimum, min(maximum, int(math.ceil(span / theta))))


def _flank_segments(spec, r_form, r_tip, tolerance, minimum=3, maximum=24):
    """Segments one involute flank needs, sampled uniformly in the roll angle.

    The curvature radius of an involute at roll angle t is rb * t, and a step
    of dt there spans rb * t * dt, so the chord error is rb * t * dt^2 / 8 and
    is worst at the tip. Solving for dt gives the spacing below.
    """
    rb = spec.base_radius
    if rb <= EPS:
        return minimum
    t0 = math.sqrt(max(0.0, (r_form / rb) ** 2 - 1.0))
    t1 = math.sqrt(max(0.0, (r_tip / rb) ** 2 - 1.0))
    if t1 <= t0 + EPS:
        return minimum
    dt = math.sqrt(8.0 * tolerance / (rb * max(t1, EPS)))
    if dt <= EPS:
        return maximum
    return max(minimum, min(maximum, int(math.ceil((t1 - t0) / dt))))


def tooth_profile(spec, tolerance=None):
    """Closed outline of the whole gear, counter-clockwise, centred on origin.

    One tooth cycle runs root arc, fillet, flank, tip arc, mirrored flank,
    mirrored fillet, root arc, and is then repeated around. Tooth 0 is centred
    on the +X axis, which is what mesh_rotation() below assumes.

    Point density follows the chord tolerance rather than a fixed count, so a
    12 tooth pinion and a 120 tooth wheel both come out accurate without the
    big one drowning Fusion in spline points. If the total would still exceed
    MAX_PROFILE_POINTS the tolerance is relaxed until it fits.
    """
    if tolerance is None:
        tolerance = CHORD_TOLERANCE
    for _ in range(12):
        points = _profile_at_tolerance(spec, tolerance)
        if len(points) <= MAX_PROFILE_POINTS:
            return points
        tolerance *= 2.0
    return points


def _profile_at_tolerance(spec, tolerance):
    ra, truncated = truncated_tip_radius(spec)
    spec.tip_truncated = truncated
    rb = spec.base_radius
    rf = spec.root_radius
    r_form = max(rb, rf + 1e-6)
    if r_form >= ra:
        raise ValueError('tooth has no usable flank')

    # A fillet that does not fit is shrunk rather than dropped, so the root
    # never ends in a sharp notch.
    fillet = spec.fillet_factor * spec.module
    solution = None
    for _ in range(24):
        if fillet < 1e-4:
            break
        candidate = _root_fillet(spec, r_form, -1.0, fillet)
        if candidate is not None:
            angle = math.atan2(candidate[2][1], candidate[2][0])
            if abs(angle) < math.pi / spec.teeth - 1e-6:
                solution = candidate
                break
        fillet *= 0.75

    half_pitch = math.pi / spec.teeth
    cycle = []

    if solution is not None:
        gap_angle = math.atan2(solution[2][1], solution[2][0])    # negative side
    else:
        edge = _flank_point(spec, r_form, -1.0)
        gap_angle = math.atan2(edge[1], edge[0])

    # Resolution, once per gear, from the chord tolerance.
    flank_segments = _flank_segments(spec, r_form, ra, tolerance)
    tip_half = spec.half_tooth_angle(ra)
    tip_segments = _arc_segments(ra, 2.0 * tip_half, tolerance, minimum=1, maximum=12)
    root_steps = _arc_segments(rf, gap_angle + half_pitch, tolerance,
                               minimum=1, maximum=12)
    if solution is not None:
        centre, on_flank, on_root = solution
        fillet_radius = math.hypot(on_root[0] - centre[0], on_root[1] - centre[1])
        fillet_span = abs(math.atan2(on_flank[1] - centre[1], on_flank[0] - centre[0])
                          - math.atan2(on_root[1] - centre[1], on_root[0] - centre[0]))
        fillet_segments = _arc_segments(fillet_radius, fillet_span, tolerance,
                                        minimum=2, maximum=12)
    else:
        fillet_segments = 2

    # 1. root arc, from the middle of the gap up to the fillet
    for i in range(root_steps):
        angle = -half_pitch + (gap_angle + half_pitch) * i / float(root_steps)
        cycle.append((rf * math.cos(angle), rf * math.sin(angle)))

    # 2. trailing fillet
    if solution is not None:
        centre, on_flank, on_root = solution
        cycle.extend(_arc_points(centre, on_root, on_flank, fillet_segments)[:-1])

    # 3. trailing flank, outwards
    for i in range(flank_segments + 1):
        radius = r_form + (ra - r_form) * i / float(flank_segments)
        cycle.append(_flank_point(spec, radius, -1.0))

    # 4. tip arc
    for i in range(1, tip_segments):
        angle = -tip_half + 2.0 * tip_half * i / float(tip_segments)
        cycle.append((ra * math.cos(angle), ra * math.sin(angle)))

    # 5. leading flank, back down
    for i in range(flank_segments, -1, -1):
        radius = r_form + (ra - r_form) * i / float(flank_segments)
        cycle.append(_flank_point(spec, radius, 1.0))

    # 6. leading fillet, mirrored
    if solution is not None:
        centre, on_flank, on_root = solution
        cycle.extend(_arc_points((centre[0], -centre[1]),
                                 (on_flank[0], -on_flank[1]),
                                 (on_root[0], -on_root[1]), fillet_segments)[1:])

    # 7. root arc towards the next gap; the next tooth's step 1 continues it
    for i in range(1, root_steps):
        angle = -gap_angle + (half_pitch + gap_angle) * i / float(root_steps)
        cycle.append((rf * math.cos(angle), rf * math.sin(angle)))

    points = []
    for tooth in range(spec.teeth):
        rot = tooth * spec.pitch_angle
        cos_r, sin_r = math.cos(rot), math.sin(rot)
        for x, y in cycle:
            points.append((x * cos_r - y * sin_r, x * sin_r + y * cos_r))
    return points


# ----------------------------------------------------------------- meshing ---

def mesh_rotation(spec_a, angle_a, spec_b, direction):
    """Rotation for gear B that drops its teeth into gear A's gaps.

    direction is the bearing from A to B. Rolling the two pitch circles against
    each other gives z_a * u_a = -z_b * u_b + pi, where u is the local angle in
    the unrotated profile facing the contact point: a tooth centre on one side
    has to meet a gap centre, and the gap centre sits exactly half a pitch from
    the tooth centre whatever the profile shift does.
    """
    u_a = direction - angle_a
    u_b = (math.pi - spec_a.teeth * u_a) / float(spec_b.teeth)
    return direction + math.pi - u_b


def helix_twist(spec, face_width, helix_angle):
    """Total rotation over the face width of a helical gear, in radians.

    tan(beta) = r dphi / dz at the pitch circle, so the whole face turns
    through width * tan(beta) / r.
    """
    if abs(helix_angle) < EPS or spec.pitch_radius < EPS:
        return 0.0
    return face_width * math.tan(helix_angle) / spec.pitch_radius


# ------------------------------------------------------------------ layouts --

# How the selected points are read.
MODE_RATIO = 'ratio'        # points give direction, meshing gives the distance
MODE_POSITION = 'position'  # points give the exact axis positions

DEFAULT_PAIR_ANGLE_DEG = 180.0


class Placement(object):
    """One gear, ready to be built: what it is, where it goes, how it is turned."""

    def __init__(self, spec, x, y, rotation, helix_sign):
        self.spec = spec
        self.x = x
        self.y = y
        self.rotation = rotation        # radians, about its own axis
        self.helix_sign = helix_sign    # +1 / -1, alternating so flanks match

    @property
    def position(self):
        return (self.x, self.y)


def teeth_from_center_distance(module, distance, other_teeth):
    """Tooth count that puts a gear at that distance from one of other_teeth.

    a = m (z1 + z2) / 2, rearranged and rounded. The rounding is why
    MODE_POSITION cannot hit every distance exactly.
    """
    return int(round(2.0 * distance / module - other_teeth))


def _clamp_teeth(count):
    return max(MIN_TEETH, min(MAX_TEETH, int(count)))


def _make_spec(module, teeth, options):
    """GearSpec from the dialog options, with profile shift resolved."""
    alpha_deg = options.get('pressure_angle_deg', DEFAULT_PRESSURE_ANGLE_DEG)
    if options.get('auto_profile_shift', True):
        shift = auto_profile_shift(teeth, math.radians(alpha_deg))
    else:
        shift = 0.0
    return GearSpec(module, teeth,
                    pressure_angle_deg=alpha_deg,
                    profile_shift=shift,
                    backlash=options.get('backlash', DEFAULT_BACKLASH),
                    clearance_factor=options.get('clearance_factor',
                                                 DEFAULT_CLEARANCE_FACTOR),
                    fillet_factor=options.get('fillet_factor',
                                              DEFAULT_FILLET_FACTOR),
                    nozzle=options.get('nozzle', 0.4))


def plan_train(points, module, first_teeth, ratio, options):
    """Work out every gear of the train: size, position and phase.

    points  - axis positions in mm, in the order they were picked. One point
              means a single gear, or a pair when options['pair'] is set.
    ratio   - overall reduction, last gear over first. In a simple train the
              idlers in between only reverse direction, so the ratio is fixed
              by the two ends and the idlers are sized to reach the points.

    Two ways to read the points, because a point pattern and an exact ratio
    generally cannot both be satisfied with whole teeth:

      MODE_RATIO     the picked points set the direction from one axis to the
                     next, the meshing sets the distance. Ratio is exact, the
                     gears drift off the points.
      MODE_POSITION  the gears land exactly on the points and the tooth counts
                     are whatever reaches them, so the ratio is approximate.

    Returns (placements, warnings) where warnings holds message keys the UI
    turns into text.
    """
    mode = options.get('mode', MODE_RATIO)
    warnings = []

    counts = [_clamp_teeth(first_teeth)]
    if len(points) == 1:
        if options.get('pair', False):
            counts.append(_clamp_teeth(round(first_teeth * ratio)))
            angle = math.radians(options.get('pair_angle_deg', DEFAULT_PAIR_ANGLE_DEG))
            directions = [angle]
        else:
            directions = []
    else:
        directions = []
        for i in range(len(points) - 1):
            dx = points[i + 1][0] - points[i][0]
            dy = points[i + 1][1] - points[i][1]
            directions.append(math.atan2(dy, dx))
            gap = math.hypot(dx, dy)
            # Idlers are sized to reach the point they were dropped on; the
            # last gear is sized by the ratio instead, unless the points rule.
            wanted = teeth_from_center_distance(module, gap, counts[-1])
            counts.append(_clamp_teeth(wanted))
        if mode == MODE_RATIO:
            counts[-1] = _clamp_teeth(round(counts[0] * ratio))

    if len(counts) > 1:
        achieved = counts[-1] / float(counts[0])
        if abs(achieved - ratio) > 0.02 * max(ratio, 1.0):
            warnings.append('warn.ratio_off')

    specs = [_make_spec(module, count, options) for count in counts]

    placements = []
    x, y = points[0]
    previous_rotation = 0.0
    placements.append(Placement(specs[0], x, y, 0.0, 1))
    for i in range(1, len(specs)):
        direction = directions[i - 1]
        distance = working_center_distance(specs[i - 1], specs[i])
        if mode == MODE_POSITION and len(points) > 1:
            x, y = points[i]
            actual = math.hypot(x - placements[-1].x, y - placements[-1].y)
            if abs(actual - distance) > 0.02 * module:
                warnings.append('warn.distance_off')
            direction = math.atan2(y - placements[-1].y, x - placements[-1].x)
        else:
            x = placements[-1].x + distance * math.cos(direction)
            y = placements[-1].y + distance * math.sin(direction)
        rotation = mesh_rotation(specs[i - 1], previous_rotation, specs[i], direction)
        placements.append(Placement(specs[i], x, y, rotation % (2.0 * math.pi),
                                    -placements[-1].helix_sign))
        previous_rotation = rotation

    for placement in placements:
        if placement.spec.root_radius <= placement.spec.module:
            warnings.append('warn.teeth_low')
            break

    # A small pinion with a wide face and a steep helix turns into a screw:
    # the profile sweeps past a whole tooth before it reaches the far end.
    style = options.get('tooth_style', TEETH_STRAIGHT)
    if style != TEETH_STRAIGHT:
        helix = math.radians(options.get('helix_angle_deg', 0.0))
        width = options.get('face_width', 0.0)
        if style == TEETH_HERRINGBONE:
            width /= 2.0            # each half carries its own helix
        for placement in placements:
            if abs(helix_twist(placement.spec, width, helix)) > math.pi:
                warnings.append('warn.twist_high')
                break

    seen = set()
    unique = [w for w in warnings if not (w in seen or seen.add(w))]
    return placements, unique
