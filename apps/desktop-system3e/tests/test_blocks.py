# -*- coding: utf-8 -*-
"""Check the element library of the System3E add-in without starting Fusion.

    python apps/desktop-system3e/tests/test_blocks.py

Tests blocks/blocks.json (every element a closed solid with flat faces, sizes
that fit the catalogue name, a picture and a translated family) and runs
make_body() against a stand-in for Fusion's API that records what the add-in
asks for. Whether Fusion accepts the body is only known inside Fusion.
Standard library only.
"""
import os
import re
import sys
import json
import types
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ADDIN = os.path.join(os.path.dirname(HERE), 'System3E')
BLOCKS = os.path.join(ADDIN, 'blocks')

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)
        print('  FAIL  %s' % message)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def loop_area(loop, points, normal):
    total = (0.0, 0.0, 0.0)
    for i in range(1, len(loop) - 1):
        part = cross(sub(points[loop[i]], points[loop[0]]), sub(points[loop[i + 1]], points[loop[0]]))
        total = (total[0] + part[0], total[1] + part[1], total[2] + part[2])
    return dot(total, normal) / 2.0


def check_solid(block):
    name, points = block['name'], block['points']
    edges, volume = {}, 0.0
    for face in block['faces']:
        normal = face['normal']
        check(abs(dot(normal, normal) - 1.0) < 1e-4, '%s: a face normal is not of length 1' % name)
        origin = points[face['loops'][0][0]]
        for number, loop in enumerate(face['loops']):
            check(len(loop) >= 3 and len(set(loop)) == len(loop), '%s: a broken outline' % name)
            for index in loop:
                check(abs(dot(sub(points[index], origin), normal)) < 0.05, '%s: a face is not flat' % name)
            area = loop_area(loop, points, normal)
            check(area > 0 if number == 0 else area < 0, '%s: an outline runs the wrong way round' % name)
            for i, index in enumerate(loop):
                edge = (index, loop[(i + 1) % len(loop)])
                edges[edge] = edges.get(edge, 0) + 1
            for i in range(1, len(loop) - 1):
                volume += dot(points[loop[0]], cross(points[loop[i]], points[loop[i + 1]])) / 6.0
    loose = [e for e, count in edges.items() if count != 1 or edges.get((e[1], e[0]), 0) != 1]
    check(not loose, '%s: not a closed solid (%d loose edges)' % (name, len(loose)))
    size = block['size']
    check(0 < volume <= size[0] * size[1] * size[2] + 1.0, '%s: impossible volume' % name)
    low = [min(p[i] for p in points) for i in range(3)]
    high = [max(p[i] for p in points) for i in range(3)]
    check(all(abs(v) < 0.01 for v in low), '%s: the corner is not at the origin' % name)
    check(all(abs(high[i] - size[i]) < 0.6 for i in range(3)), '%s: size and points disagree' % name)


def check_name(block):
    """What the catalogue name says about the size must be true."""
    name, (length, width, height) = block['name'], block['size']
    if block['family'] == 'partition':
        check(width == int(name.split()[-1]), '%s: wrong thickness' % name)
        check(length == (352 if '/2' in name else 704), '%s: wrong length' % name)
        return
    check(width == 352, '%s: wall thickness is not 352 mm' % name)
    number = re.search(r'\b(150|200|250|300)\b', name)
    if number and not name.startswith('EO/2'):
        check(height == int(number.group(1)), '%s: height is not %s' % (name, number.group(1)))
    words = name.split()
    if words[0] in ('S0', 'S1', 'EU', 'EN', 'SZ/EO') or words[0] in ('S0/2', 'S1/2', 'EU/2', 'EN/2', 'SZ/2'):
        half = '/2' in words[0]
        tongue = words[-1] in ('WP', 'P')
        check(length == (352 if half else 704) + (3 if tongue else 0), '%s: length %d does not fit' % (name, length))


class Recorder(object):
    """Stands in for adsk: records the body definition the add-in builds."""

    def __init__(self):
        self.vertices, self.edges, self.faces, self.uses = [], [], [], {}

    def install(self):
        rec = self

        class Point3D(object):
            @staticmethod
            def create(x, y, z):
                return (x, y, z)

        class Vector3D(object):
            @staticmethod
            def create(x, y, z):
                return (x, y, z)

        class Plane(object):
            @staticmethod
            def create(origin, normal):
                return ('plane', origin, normal)

        class Line3D(object):
            @staticmethod
            def create(a, b):
                return ('line', a, b)

        class CoEdges(object):
            def add(self, edge, opposed):
                rec.uses.setdefault(edge, []).append(bool(opposed))

        class Loop(object):
            bRepCoEdgeDefinitions = CoEdges()

        class Loops(object):
            def add(self):
                return Loop()

        class Face(object):
            loopDefinitions = Loops()

        class Faces(object):
            def add(self, surface, reversed_):
                rec.faces.append((surface, reversed_))
                return Face()

        class Shell(object):
            faceDefinitions = Faces()

        class Shells(object):
            def add(self):
                return Shell()

        class Lump(object):
            shellDefinitions = Shells()

        class Lumps(object):
            def add(self):
                return Lump()

        class Definition(object):
            lumpDefinitions = Lumps()
            outcomeInfo = []
            doFullCheck = False

            def createVertexDefinition(self, point):
                rec.vertices.append(point)
                return len(rec.vertices) - 1

            def createEdgeDefinitionByCurve(self, start, end, curve):
                rec.edges.append((start, end, curve))
                return len(rec.edges) - 1

            def createBody(self):
                return 'body'

        class BRepBodyDefinition(object):
            @staticmethod
            def create():
                return Definition()

        adsk = types.ModuleType('adsk')
        core = types.ModuleType('adsk.core')
        fusion = types.ModuleType('adsk.fusion')
        for handler in ('CommandEventHandler', 'ValidateInputsEventHandler',
                        'InputChangedEventHandler', 'CommandCreatedEventHandler'):
            setattr(core, handler, type(handler, (object,), {}))
        core.Point3D, core.Vector3D, core.Plane, core.Line3D = Point3D, Vector3D, Plane, Line3D
        fusion.BRepBodyDefinition = BRepBodyDefinition
        adsk.core, adsk.fusion = core, fusion
        sys.modules['adsk'], sys.modules['adsk.core'], sys.modules['adsk.fusion'] = adsk, core, fusion


def main():
    print('1) Library file')
    with open(os.path.join(BLOCKS, 'blocks.json'), 'r', encoding='utf-8') as handle:
        data = json.load(handle)
    blocks = data['blocks']
    check(data.get('unit') == 'mm', 'the unit is mm')
    check(len(blocks) == 74, '74 elements (70 load-bearing + 4 partition), found %d' % len(blocks))
    check(len({b['id'] for b in blocks}) == len(blocks), 'every id is unique')
    check(len({b['name'] for b in blocks}) == len(blocks), 'every name is unique')
    check(all(re.fullmatch(r'[a-z0-9-]+', b['id']) for b in blocks), 'ids are plain file names')

    print('2) Solids')
    shapes = {}
    for block in blocks:
        check_solid(block)
        check_name(block)
        shape = tuple(sorted(tuple(round(c) for c in p) for p in block['points']))
        check(shape not in shapes, '%s has the same shape as %s' % (block['name'], shapes.get(shape)))
        shapes[shape] = block['name']

    print('3) Pictures')
    for block in blocks:
        path = os.path.join(BLOCKS, block['id'] + '.png')
        ok = os.path.isfile(path)
        if ok:
            with open(path, 'rb') as handle:
                ok = handle.read(8) == b'\x89PNG\r\n\x1a\n'
        check(ok, '%s has a picture' % block['name'])
    extra = {f for f in os.listdir(BLOCKS) if f.endswith('.png')} - {b['id'] + '.png' for b in blocks}
    check(not extra, 'no left-over pictures: %s' % ', '.join(sorted(extra)))

    print('4) Add-in')
    recorder = Recorder()
    recorder.install()
    if ADDIN not in sys.path:
        sys.path.insert(0, ADDIN)
    addin = importlib.import_module('System3E')
    families, by_id = addin.library()
    check(len(by_id) == len(blocks), 'the add-in reads every element')
    for code in ('de', 'en', 'es', 'fr', 'it'):
        addin.S.load(code)
        for family, members in families:
            text = addin.T('family.' + family)
            check(text and text != 'family.' + family, '%s: family "%s" has a name' % (code, family))
        for key in (['in.anchor', 'in.dx', 'in.dy', 'in.dz'] + ['anchor.' + a for a in addin.ANCHORS]
                    + [k for k, position in addin.snap_points(blocks[0])]):
            check(addin.T(key) != key, '%s: "%s" has a text' % (code, key))
    check(addin._last[addin.IN_BLOCK] in by_id, 'the default element exists')
    check(addin._last[addin.IN_ANCHOR] in addin.ANCHORS, 'the default anchor exists')

    print('5) Points for clicking')
    s1 = by_id['s1-wp']
    check(s1.get('stack') == 250, 'the next course stands 250 mm up on S1 WP, found %s' % s1.get('stack'))
    check(by_id['eu-200-w'].get('stack') == 200, 'a flat element carries the next course on top')
    check(addin.anchor_position(s1, 'corner') == (0.0, 0.0, 0.0), 'anchor corner')
    check(addin.anchor_position(s1, 'centre') == (353.5, 176.0, 0.0), 'anchor bottom middle')
    check(addin.anchor_position(s1, 'top-right') == (0.0, 0.0, 300.0), 'anchor top front right corner')
    check(addin.anchor_position(s1, 'top-left') == (0.0, 352.0, 300.0), 'anchor top front left corner')
    check(len({addin.anchor_position(s1, a) for a in addin.ANCHORS}) == len(addin.ANCHORS), 'every anchor is a place of its own')
    for block in blocks:
        spots = addin.snap_points(block)
        check(len(spots) == 12 and len({key for key, p in spots}) == 12, '%s: twelve named points' % block['name'])
        check(len({p for key, p in spots}) == 12, '%s: no two points in one place' % block['name'])
        check(all(0 <= p[i] <= block['size'][i] for key, p in spots for i in range(3)),
              '%s: every point lies on the element' % block['name'])
        check(0 < block.get('stack', 0) <= block['size'][2], '%s: a sensible stacking height' % block['name'])
        # Bond: bottom middle of the next element on the upper end point of this one.
        check([p for key, p in spots if key == 'point.bottom.centre'][0]
              == addin.anchor_position(block, 'centre'), '%s: anchor and point agree' % block['name'])
    for block in blocks:
        recorder.vertices, recorder.edges, recorder.faces, recorder.uses = [], [], [], {}
        addin.make_body(block)
        check(len(recorder.vertices) == len(block['points']), '%s: every point becomes a vertex' % block['name'])
        check(len(recorder.faces) == len(block['faces']), '%s: every face is defined' % block['name'])
        check(all(sorted(flags) == [False, True] for flags in recorder.uses.values())
              and len(recorder.uses) == len(recorder.edges),
              '%s: every edge is used once in each direction' % block['name'])
        scale = max(max(v) for v in recorder.vertices) * 10.0
        check(abs(scale - max(block['size'])) < 0.6, '%s: mm become cm' % block['name'])

    print()
    if failures:
        print('%d check(s) failed' % len(failures))
        sys.exit(1)
    print('all checks passed (%d elements)' % len(blocks))


if __name__ == '__main__':
    main()
