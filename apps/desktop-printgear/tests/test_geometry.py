# -*- coding: utf-8 -*-
"""Offline test suite for PrintGear.

    python apps/desktop-printgear/tests/test_geometry.py

The gear mathematics has no Fusion dependency, so all of it runs in a normal
Python installation. The Fusion side is imported against stub adsk modules,
which is enough to catch import errors, missing text keys and typos in the API
surface - not enough to prove the geometry lands in the document, which is what
Fusion itself is for.

Set PRINTGEAR_ADDIN_DIR to test an installed copy instead of the one in the
repository.
"""

import io
import os
import re
import sys
import math
import types
import xml.etree.ElementTree as ElementTree

HERE = os.path.dirname(os.path.abspath(__file__))
ADDINS = os.path.dirname(HERE)  # apps/desktop-printgear, where the add-in lives
ADDIN = os.environ.get('PRINTGEAR_ADDIN_DIR') or os.path.join(ADDINS, 'PrintGear')
LANG = os.path.join(ADDIN, 'lang')

sys.path.insert(0, ADDIN)

_failures = []
_checks = [0]


def check(condition, message):
    _checks[0] += 1
    if not condition:
        _failures.append(message)


def section(title):
    print('\n== %s' % title)


# ------------------------------------------------------------- adsk stubs ---

def install_stubs():
    """Just enough adsk for the Fusion modules to import.

    Names have to resolve to real classes, not placeholder instances: the event
    handlers subclass adsk.core.CommandEventHandler, and you cannot inherit
    from an instance. A metaclass gives the class attributes (enum members,
    Point3D.create and so on) the same open-ended treatment.
    """
    class AnyMeta(type):
        def __getattr__(cls, name):
            return _Anything()

    class _Anything(object, metaclass=AnyMeta):
        def __init__(self, *args, **kwargs):
            pass

        def __getattr__(self, name):
            return _Anything()

        def __call__(self, *args, **kwargs):
            return _Anything()

    def module_attributes(module_name):
        cache = {}

        def getter(name):
            if name.startswith('__'):
                raise AttributeError(name)
            if name not in cache:
                cache[name] = AnyMeta(name, (_Anything,), {})
            return cache[name]
        return getter

    core_module = types.ModuleType('adsk.core')
    fusion_module = types.ModuleType('adsk.fusion')
    adsk_module = types.ModuleType('adsk')
    core_module.__getattr__ = module_attributes('adsk.core')
    fusion_module.__getattr__ = module_attributes('adsk.fusion')
    adsk_module.core = core_module
    adsk_module.fusion = fusion_module
    sys.modules['adsk'] = adsk_module
    sys.modules['adsk.core'] = core_module
    sys.modules['adsk.fusion'] = fusion_module


# --------------------------------------------------------------- geometry ---

def polygon_crossings(first, second):
    """How many edges of one outline cut through the other. Zero means clear."""
    def intersects(p1, p2, p3, p4):
        denominator = ((p2[0] - p1[0]) * (p4[1] - p3[1])
                       - (p2[1] - p1[1]) * (p4[0] - p3[0]))
        if abs(denominator) < 1e-15:
            return False
        t = ((p3[0] - p1[0]) * (p4[1] - p3[1])
             - (p3[1] - p1[1]) * (p4[0] - p3[0])) / denominator
        u = ((p3[0] - p1[0]) * (p2[1] - p1[1])
             - (p3[1] - p1[1]) * (p2[0] - p1[0])) / denominator
        return 1e-9 < t < 1.0 - 1e-9 and 1e-9 < u < 1.0 - 1e-9

    count = 0
    for i in range(len(first)):
        a1, a2 = first[i], first[(i + 1) % len(first)]
        for j in range(len(second)):
            b1, b2 = second[j], second[(j + 1) % len(second)]
            if intersects(a1, a2, b1, b2):
                count += 1
    return count


def placed_outline(spec, rotation, centre_x, centre_y, spin=0.0):
    import printgear_math as pg
    angle = rotation + spin
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return [(x * cos_a - y * sin_a + centre_x, x * sin_a + y * cos_a + centre_y)
            for x, y in pg.tooth_profile(spec)]


def test_involute():
    import printgear_math as pg
    section('involute')

    for angle in (0.05, 0.1, 0.2, 0.35, 0.5, 0.7):
        back = pg.inv_inverse(pg.inv(angle))
        check(abs(back - angle) < 1e-9,
              'inv_inverse(inv(%.2f)) = %.12f' % (angle, back))
    print('   inv / inv_inverse round trip over the useful range')

    check(abs(pg.min_teeth_without_undercut(math.radians(20)) - 17.097) < 0.01,
          'undercut limit at 20 deg should be about 17')
    check(pg.auto_profile_shift(40, math.radians(20)) == 0.0,
          'no shift needed on a 40 tooth gear')
    check(pg.auto_profile_shift(10, math.radians(20)) > 0.3,
          '10 teeth needs a serious shift')
    print('   undercut limit and automatic profile shift')


def test_module_from_nozzle():
    import printgear_math as pg
    section('module follows the nozzle')

    expected = {0.2: 0.5, 0.4: 1.0, 0.6: 1.5, 0.8: 2.0, 1.0: 2.5}
    for nozzle in pg.NOZZLE_SIZES:
        value = pg.module_for_nozzle(nozzle)
        check(abs(value - expected[nozzle]) < 1e-12,
              'nozzle %.1f should give module %.1f, got %.3f'
              % (nozzle, expected[nozzle], value))
    print('   0.2/0.4/0.6/0.8/1.0 -> 0.5/1.0/1.5/2.0/2.5 at the default factor')


def test_profile():
    import printgear_math as pg
    section('tooth outline')

    for teeth in (6, 8, 12, 17, 24, 40, 60, 90, 150):
        spec = pg.GearSpec(1.0, teeth,
                           profile_shift=pg.auto_profile_shift(teeth, math.radians(20)))
        points = pg.tooth_profile(spec)
        radii = [math.hypot(x, y) for x, y in points]

        check(min(radii) >= spec.root_radius - 1e-6,
              'z=%d: outline dips below the root circle' % teeth)
        check(max(radii) <= spec.tip_radius + 1e-6,
              'z=%d: outline runs past the tip circle' % teeth)
        check(len(points) <= pg.MAX_PROFILE_POINTS,
              'z=%d: %d points exceeds the ceiling' % (teeth, len(points)))
        check(len(points) >= teeth * 8,
              'z=%d: only %d points, too coarse' % (teeth, len(points)))

        # Every tooth has to be the same tooth: the outline is one cycle
        # repeated, so the radius profile has to repeat with it.
        per_tooth = len(points) // teeth
        check(len(points) % teeth == 0, 'z=%d: outline is not a whole number '
                                        'of tooth cycles' % teeth)
        for index in range(per_tooth):
            first = math.hypot(*points[index])
            other = math.hypot(*points[index + per_tooth * (teeth // 2)])
            check(abs(first - other) < 1e-9,
                  'z=%d: teeth are not identical at sample %d' % (teeth, index))
    print('   9 sizes: inside root/tip, point count bounded, all teeth identical')

    # The tip is only ever cut back when the tooth would otherwise be a knife
    # edge - that is a small pinion behaviour, not something normal gears see.
    spec = pg.GearSpec(1.0, 40)
    pg.tooth_profile(spec)
    check(not spec.tip_truncated, 'a 40 tooth gear should keep its full tip')
    spec = pg.GearSpec(1.0, 8, profile_shift=pg.auto_profile_shift(8, math.radians(20)))
    pg.tooth_profile(spec)
    check(spec.tip_truncated, 'a shifted 8 tooth pinion needs its tip cut back')
    print('   tip truncation fires on sharp pinions and nowhere else')


def test_tolerance():
    import printgear_math as pg
    section('chord tolerance')

    for teeth in (12, 30, 80):
        spec = pg.GearSpec(1.0, teeth)
        coarse = len(pg.tooth_profile(spec, tolerance=0.1))
        fine = len(pg.tooth_profile(spec, tolerance=0.002))
        check(fine > coarse,
              'z=%d: a tighter tolerance has to add points (%d vs %d)'
              % (teeth, fine, coarse))
    print('   a tighter tolerance buys more points, a looser one fewer')


def test_meshing():
    import printgear_math as pg
    section('meshing')

    combinations = ((17, 17), (12, 36), (20, 31), (9, 44), (15, 15), (30, 11))
    for first, second in combinations:
        alpha = math.radians(20)
        gear_a = pg.GearSpec(1.0, first, profile_shift=pg.auto_profile_shift(first, alpha))
        gear_b = pg.GearSpec(1.0, second, profile_shift=pg.auto_profile_shift(second, alpha))
        distance = pg.working_center_distance(gear_a, gear_b)
        rotation_b = pg.mesh_rotation(gear_a, 0.0, gear_b, 0.0)

        # Roll the pair through a full tooth pitch. If the phasing were out the
        # teeth would collide somewhere in there.
        worst = 0
        for step in range(9):
            spin = step * gear_a.pitch_angle / 8.0
            outline_a = placed_outline(gear_a, 0.0, 0.0, 0.0, spin)
            outline_b = placed_outline(gear_b, rotation_b, distance, 0.0,
                                       -spin * first / float(second))
            worst = max(worst, polygon_crossings(outline_a, outline_b))
        check(worst == 0,
              'z=%d/%d: teeth collide (%d crossings) - phasing is wrong'
              % (first, second, worst))

        # ... and they do have to actually engage, not just miss each other.
        check(gear_a.tip_radius + gear_b.tip_radius > distance,
              'z=%d/%d: tip circles do not reach each other' % (first, second))
    print('   6 pairs roll through a full pitch without touching, and do engage')

    # A profile shifted pair has to be pushed apart, or it binds.
    small = pg.GearSpec(1.0, 10, profile_shift=pg.auto_profile_shift(10, math.radians(20)))
    plain = pg.GearSpec(1.0, 40)
    shifted = pg.working_center_distance(small, plain)
    check(shifted > 1.0 * (10 + 40) / 2.0 + 0.05,
          'a shifted pair has to sit further apart than the reference distance')
    print('   profile shift widens the centre distance')


def test_backlash():
    import printgear_math as pg
    section('backlash')

    tight = pg.GearSpec(1.0, 20, backlash=0.0)
    loose = pg.GearSpec(1.0, 20, backlash=0.4)
    difference = tight.tooth_thickness - loose.tooth_thickness
    check(abs(difference - 0.2) < 1e-12,
          'each gear should give up half the backlash, got %.4f' % difference)

    # Same centre distance either way - backlash is thinner teeth, not a wider
    # gap, which is what keeps a train on its points.
    partner = pg.GearSpec(1.0, 30, backlash=0.4)
    other = pg.GearSpec(1.0, 30, backlash=0.0)
    check(abs(pg.working_center_distance(loose, partner)
              - pg.working_center_distance(tight, other)) < 1e-12,
          'backlash must not move the axes')
    print('   half off each gear, and the centre distance stays put')


def test_train():
    import printgear_math as pg
    section('gear trains')

    module = pg.module_for_nozzle(0.4)
    options = dict(nozzle=0.4, backlash=0.25, mode=pg.MODE_RATIO)

    placements, warnings = pg.plan_train([(0.0, 0.0)], module, 17, 3.0, options)
    check(len(placements) == 1, 'one point without a pair is one gear')
    check(not warnings, 'a single gear has nothing to warn about')

    placements, _ = pg.plan_train(
        [(0.0, 0.0)], module, 17, 3.0,
        dict(options, pair=True, pair_angle_deg=180.0))
    check(len(placements) == 2, 'one point with a pair is two gears')
    check(placements[1].spec.teeth == 51, 'ratio 3 on 17 teeth is 51')
    check(placements[1].y < 1e-9 and placements[1].x < 0.0,
          '180 degrees should put the second gear on the -X side')
    gap = math.hypot(placements[1].x - placements[0].x,
                     placements[1].y - placements[0].y)
    check(abs(gap - pg.working_center_distance(placements[0].spec,
                                               placements[1].spec)) < 1e-9,
          'the pair has to sit at the meshing distance')

    placements, _ = pg.plan_train(
        [(0.0, 0.0)], module, 17, 2.0,
        dict(options, pair=True, pair_angle_deg=90.0))
    check(abs(placements[1].x) < 1e-9 and placements[1].y > 0.0,
          '90 degrees should put the second gear round the corner')
    print('   single gear, pair in line, pair round a corner')

    points = [(0.0, 0.0), (30.0, 0.0), (65.0, 10.0), (100.0, 10.0)]

    placements, warnings = pg.plan_train(points, module, 15, 4.0,
                                         dict(options, mode=pg.MODE_RATIO))
    check(len(placements) == 4, 'four points, four gears')
    check(placements[-1].spec.teeth == 60, 'ratio 4 on 15 teeth is 60 at the end')
    check('warn.ratio_off' not in warnings, 'ratio mode should hit the ratio')
    for index in range(1, len(placements)):
        here, before = placements[index], placements[index - 1]
        actual = math.hypot(here.x - before.x, here.y - before.y)
        wanted = pg.working_center_distance(before.spec, here.spec)
        check(abs(actual - wanted) < 1e-9,
              'ratio mode: gear %d does not sit at the meshing distance' % index)
    print('   ratio mode: exact ratio, every pair at its meshing distance')

    placements, warnings = pg.plan_train(points, module, 15, 4.0,
                                         dict(options, mode=pg.MODE_POSITION))
    for index, point in enumerate(points):
        check(abs(placements[index].x - point[0]) < 1e-9
              and abs(placements[index].y - point[1]) < 1e-9,
              'position mode: gear %d has left its point' % index)
    print('   position mode: every gear lands on its point')

    # Alternating helix, or two helical gears would have flanks that fight.
    signs = [placement.helix_sign for placement in placements]
    check(all(signs[i] != signs[i + 1] for i in range(len(signs) - 1)),
          'the helix hand has to alternate along the train')
    print('   helix hand alternates down the train')

    # And the phasing has to survive being chained, not just for one pair.
    for index in range(1, len(placements)):
        before, here = placements[index - 1], placements[index]
        direction = math.atan2(here.y - before.y, here.x - before.x)
        distance = math.hypot(here.x - before.x, here.y - before.y)
        outline_a = placed_outline(before.spec, before.rotation, 0.0, 0.0)
        outline_b = placed_outline(here.spec, here.rotation,
                                   distance * math.cos(0.0), 0.0)
        # Compare in the frame where the pair lies on the X axis.
        outline_a = [(x * math.cos(-direction) - y * math.sin(-direction),
                      x * math.sin(-direction) + y * math.cos(-direction))
                     for x, y in placed_outline(before.spec,
                                                before.rotation - direction, 0.0, 0.0)]
        outline_b = placed_outline(here.spec, here.rotation - direction, distance, 0.0)
        crossings = polygon_crossings(
            placed_outline(before.spec, before.rotation - direction, 0.0, 0.0),
            outline_b)
        check(crossings == 0,
              'train: gears %d and %d collide (%d crossings)'
              % (index, index + 1, crossings))
    print('   every neighbouring pair in the train meshes cleanly')


def test_helix():
    import printgear_math as pg
    section('helix')

    spec = pg.GearSpec(1.0, 20)
    check(pg.helix_twist(spec, 10.0, 0.0) == 0.0, 'no angle means no twist')
    twist = pg.helix_twist(spec, 10.0, math.radians(45.0))
    check(abs(twist - 10.0 / spec.pitch_radius) < 1e-12,
          '45 degrees should twist by width/r, got %.6f' % twist)
    check(pg.helix_twist(spec, 20.0, math.radians(30.0))
          > pg.helix_twist(spec, 10.0, math.radians(30.0)),
          'a wider face has to twist further')
    print('   twist follows width * tan(beta) / r')


# ------------------------------------------------------------- text files ---

def read_keys(path):
    root = ElementTree.parse(path).getroot()
    return dict((node.get('key'), node.text or '') for node in root.findall('string'))


def test_languages():
    section('language files')

    reference = read_keys(os.path.join(LANG, 'en.xml'))
    check(len(reference) > 60, 'en.xml looks too small: %d keys' % len(reference))

    for code in ('de', 'en', 'es', 'fr', 'it'):
        path = os.path.join(LANG, '%s.xml' % code)
        check(os.path.isfile(path), 'missing language file %s.xml' % code)
        if not os.path.isfile(path):
            continue
        keys = read_keys(path)
        missing = sorted(set(reference) - set(keys))
        extra = sorted(set(keys) - set(reference))
        check(not missing, '%s.xml is missing: %s' % (code, ', '.join(missing)))
        check(not extra, '%s.xml has keys en.xml does not: %s' % (code, ', '.join(extra)))
        empty = sorted(key for key, text in keys.items() if not text.strip())
        check(not empty, '%s.xml has empty strings: %s' % (code, ', '.join(empty)))
        for key, text in keys.items():
            check(text.count('{0}') == reference.get(key, '').count('{0}'),
                  '%s.xml: placeholder mismatch in %s' % (code, key))
    print('   5 files, same keys, no empties, placeholders line up')


def test_keys_used():
    """Every key the code asks for has to exist in en.xml, and vice versa."""
    section('text keys against the code')

    reference = read_keys(os.path.join(LANG, 'en.xml'))
    used = set()
    for name in ('PrintGear.py', 'printgear_build.py', 'printgear_math.py'):
        with io.open(os.path.join(ADDIN, name), encoding='utf-8') as handle:
            source = handle.read()
        # Any literal shaped like a catalogue key, whoever it is passed to.
        # Keys assembled with % never match, which is what the list below is for.
        for match in re.finditer(
                r"""'((?:cmd|grp|in|info|warn|err|msg)\.[a-z_0-9.]+)'""", source):
            used.add(match.group(1))

    # Keys assembled at run time from a list rather than written out.
    import printgear_math as pg
    for size in pg.NOZZLE_SIZES:
        used.add('in.nozzle.%s' % size)
    used.add('in.nozzle.custom')
    for key in (pg.TEETH_STRAIGHT, pg.TEETH_HELICAL, pg.TEETH_HERRINGBONE):
        used.add('in.style.%s' % key)
    for key in ('teeth', 'diameter'):
        used.add('in.size_mode.%s' % key)
    for key in (pg.MODE_RATIO, pg.MODE_POSITION):
        used.add('in.mode.%s' % key)
    for key in ('circles', 'full', 'off'):
        used.add('in.preview.%s' % key)
    used.update(('cmd.name', 'cmd.tooltip', 'cmd.ok'))

    missing = sorted(used - set(reference))
    check(not missing, 'used in code but not in en.xml: %s' % ', '.join(missing))

    unused = sorted(set(reference) - used)
    check(not unused, 'in en.xml but never used: %s' % ', '.join(unused))
    print('   %d keys, all defined and all reachable' % len(reference))


def test_imports():
    """The Fusion modules have to at least import against the stubs."""
    section('Fusion modules')

    install_stubs()
    import printgear_build
    check(hasattr(printgear_build, 'build'), 'printgear_build.build is missing')
    check(hasattr(printgear_build, 'preview_circles'),
          'printgear_build.preview_circles is missing')
    check(abs(printgear_build.MM - 0.1) < 1e-12,
          'MM should convert millimetres to centimetres')

    import PrintGear
    for name in ('run', 'stop', 'read_inputs', 'validate', 'plan', 'build_result'):
        check(hasattr(PrintGear, name), 'PrintGear.%s is missing' % name)
    print('   printgear_build and PrintGear import, entry points present')


def test_manifest():
    section('manifest')

    import json
    path = os.path.join(ADDIN, 'PrintGear.manifest')
    with io.open(path, encoding='utf-8') as handle:
        manifest = json.load(handle)
    check(manifest.get('id') and manifest['id'] != '0' * 8 + '-0000-0000-0000-' + '0' * 12,
          'the manifest still carries the template GUID')
    check(manifest.get('version'), 'the manifest needs a version')
    check(os.path.isfile(os.path.join(ADDIN, 'PrintGear.py')),
          'Fusion needs PrintGear/PrintGear.py to match the folder name')
    print('   version %s, own GUID, file names match the folder'
          % manifest.get('version'))


def main():
    print('PrintGear test suite')
    print('add-in: %s' % ADDIN)

    test_involute()
    test_module_from_nozzle()
    test_profile()
    test_tolerance()
    test_meshing()
    test_backlash()
    test_train()
    test_helix()
    test_languages()
    test_keys_used()
    test_imports()
    test_manifest()

    print('\n' + '-' * 60)
    if _failures:
        print('FAILED - %d of %d checks' % (len(_failures), _checks[0]))
        for failure in _failures:
            print('  * %s' % failure)
        return 1
    print('OK - %d checks passed' % _checks[0])
    return 0


if __name__ == '__main__':
    sys.exit(main())
