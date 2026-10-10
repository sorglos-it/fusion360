# -*- coding: utf-8 -*-
"""Build the element library of the System3E add-in.

    python tools/system3e/build_library.py

Reads the manufacturer's 3D file from assets/system3e/ (kept local, not in
Git), turns every mesh into a clean solid (mesh_to_solid.py), gives it its
catalogue name and writes

    apps/desktop-system3e/System3E/blocks/blocks.json   every element as points + flat faces
    apps/desktop-system3e/System3E/blocks/<id>.png      one preview picture per element

The preview pictures are drawn here from the solids - they are not taken from
the manufacturer's catalogue. Needs Pillow for the pictures; --no-pictures
skips them. The add-in itself needs neither.
"""
import json
import math
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import mesh_to_solid as ms

REPO = os.path.dirname(os.path.dirname(_HERE))
SOURCE = os.path.join(REPO, 'assets', 'system3e', 'SYSTEM 3E START.3ds')
TARGET = os.path.join(REPO, 'apps', 'desktop-system3e', 'System3E', 'blocks')

# Which mesh of the 3D file is which catalogue element. The file carries no
# names; this table was made by comparing every solid with the drawing on its
# catalogue card (family, height, length, tongue ends, left/right hand).
# Length tells the ends apart: 704/352 mm = "W", 3 mm more = a tongue ("P").
NAMES = {
    0: 'S0 200 W', 1: 'S0 200 WP', 2: 'S0/2 200 W', 3: 'S0/2 200 P',
    5: 'S0 250 W', 4: 'S0 250 WP', 6: 'S0/2 250 W', 7: 'S0/2 250 P',
    8: 'S0 300 W', 9: 'S0 300 WP', 10: 'S0/2 300 W', 11: 'S0/2 300 P',
    13: 'S1 W', 12: 'S1 WP', 14: 'S1/2 W', 15: 'S1/2 P', 16: 'ST W', 17: 'ST P',
    51: 'EU 150 W', 52: 'EU 150 WP', 56: 'EU/2 150 W', 55: 'EU/2 150 P',
    53: 'EU 200 W', 54: 'EU 200 WP', 58: 'EU/2 200 W', 57: 'EU/2 200 P',
    70: 'EN W', 69: 'EN WP', 71: 'EN/2 W', 72: 'EN/2 P',
    36: 'EPN WP L', 34: 'EPN W L', 37: 'EPN WP P', 35: 'EPN W P',
    22: 'EO/2 WP L', 23: 'EO/2 WP P', 77: 'EO/2 W P',
    24: 'EO/2 200 WP L', 25: 'EO/2 200 WP P', 78: 'EO/2 200 W P',
    41: 'EWN WP L', 40: 'EWN W L', 42: 'EWN WP P', 39: 'EWN W P',
    48: 'SZ/EO WP', 47: 'SZ/EO W', 49: 'SZ/2 W', 50: 'SZ/2 P',
    44: 'SZ/EO 200 WP', 43: 'SZ/EO 200 W', 45: 'SZ/2 200 W', 46: 'SZ/2 200 P',
    31: 'SNL', 32: 'SNL/2', 30: 'SNP', 33: 'SNP/2',
    75: 'ENL', 76: 'ENP', 59: 'SZL', 60: 'SZP', 74: 'EWNL', 38: 'EWNP',
    27: 'EO/2 LT', 21: 'EO/2 LP', 20: 'EO/2 PT', 26: 'EO/2 PP',
    28: 'EO/2 200 LT', 19: 'EO/2 200 LP', 18: 'EO/2 200 PT', 29: 'EO/2 200 PP',
}

# Catalogue order, family by family. Partition elements are plain blocks and
# are not in the 3D file; their sizes (mm) come from the catalogue cards.
FAMILIES = (
    ('starter', ['S0 200 WP', 'S0 200 W', 'S0/2 200 W', 'S0/2 200 P', 'S0 250 WP', 'S0 250 W',
                 'S0/2 250 W', 'S0/2 250 P', 'S0 300 WP', 'S0 300 W', 'S0/2 300 W', 'S0/2 300 P']),
    ('basic', ['S1 WP', 'S1 W', 'S1/2 W', 'S1/2 P', 'ST W', 'ST P']),
    ('complementary', ['EU 150 WP', 'EU 150 W', 'EU/2 150 W', 'EU/2 150 P',
                       'EU 200 WP', 'EU 200 W', 'EU/2 200 W', 'EU/2 200 P']),
    ('lintel', ['EN WP', 'EN W', 'EN/2 W', 'EN/2 P', 'EPN WP L', 'EPN W L', 'EPN WP P', 'EPN W P']),
    ('window', ['EO/2 WP L', 'EO/2 WP P', 'EO/2 W P', 'EO/2 200 WP L', 'EO/2 200 WP P', 'EO/2 200 W P']),
    ('top', ['EWN WP L', 'EWN W L', 'EWN WP P', 'EWN W P', 'SZ/EO WP', 'SZ/EO W', 'SZ/2 W', 'SZ/2 P',
             'SZ/EO 200 WP', 'SZ/EO 200 W', 'SZ/2 200 W', 'SZ/2 200 P']),
    ('corner', ['SNL', 'SNL/2', 'SNP', 'SNP/2', 'ENL', 'ENP', 'SZL', 'SZP', 'EWNL', 'EWNP',
                'EO/2 LT', 'EO/2 LP', 'EO/2 PT', 'EO/2 PP',
                'EO/2 200 LT', 'EO/2 200 LP', 'EO/2 200 PT', 'EO/2 200 PP']),
    ('partition', ['D1 115', 'D1/2 115', 'D1 175', 'D1/2 175']),
)
PARTITION = {'D1 115': (704, 115, 250), 'D1/2 115': (352, 115, 250),
             'D1 175': (704, 175, 200), 'D1/2 175': (352, 175, 200)}

# One mesh of the file is damaged beyond repair (open on one side). The starter
# elements differ only in the height of the plain body under the top profile,
# so the damaged one is rebuilt from its taller twin. check_lowering() proves
# the method on a pair where both meshes are sound.
REBUILD = {'S0/2 200 P': ('S0/2 250 P', 50.0)}


def block_id(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def box(size):
    x, y, z = size
    points = [(0, 0, 0), (x, 0, 0), (x, y, 0), (0, y, 0), (0, 0, z), (x, 0, z), (x, y, z), (0, y, z)]
    faces = [((0, 0, -1), [0, 3, 2, 1]), ((0, 0, 1), [4, 5, 6, 7]), ((0, -1, 0), [0, 1, 5, 4]),
             ((1, 0, 0), [1, 2, 6, 5]), ((0, 1, 0), [2, 3, 7, 6]), ((-1, 0, 0), [3, 0, 4, 7])]
    return {'points': [tuple(float(c) for c in p) for p in points],
            'faces': [{'normal': n, 'loops': [loop]} for n, loop in faces], 'problems': []}


def lowered(solid, by):
    """The same element with a plain body that is `by` mm lower."""
    top = max(p[2] for p in solid['points'])
    levels = sorted({p[2] for p in solid['points']})
    profile = [z for z in levels if z > 0]           # everything above the flat underside
    if not profile or profile[0] <= by:
        raise ValueError('nothing plain to remove')
    points = [(p[0], p[1], p[2] - by if p[2] > 0 else p[2]) for p in solid['points']]
    return {'points': points, 'faces': solid['faces'], 'problems': [],
            'height': top - by}


def straighten(solid, within=0.25):
    """Give points that are meant to share a coordinate exactly the same one.

    The source has float noise (106.4 next to 106.5 mm), which leaves faces
    slightly bent. Per axis, values closer than `within` become one value: the
    one most points use, to a tenth of a millimetre.
    """
    points = [list(p) for p in solid['points']]
    for axis in range(3):
        values = sorted({p[axis] for p in points})
        groups = [[values[0]]]
        for value in values[1:]:
            if value - groups[-1][-1] < within:
                groups[-1].append(value)
            else:
                groups.append([value])
        snap = {}
        for group in groups:
            best = max(group, key=lambda v: sum(1 for p in points if p[axis] == v))
            for value in group:
                snap[value] = round(best, 1)
        for p in points:
            p[axis] = snap[p[axis]]
    solid['points'] = [tuple(p) for p in points]
    return solid


def bend(solid):
    """How far the worst point lies off its face, in mm.

    Also replaces every face normal by the one its straightened outline
    really has - that is the normal blocks.json gets.
    """
    worst = 0.0
    points = solid['points']
    for face in solid['faces']:
        loop = face['loops'][0]
        normal = (0.0, 0.0, 0.0)
        for i in range(len(loop)):                      # Newell: the outline's own normal
            a, b = points[loop[i]], points[loop[(i + 1) % len(loop)]]
            normal = (normal[0] + (a[1] - b[1]) * (a[2] + b[2]),
                      normal[1] + (a[2] - b[2]) * (a[0] + b[0]),
                      normal[2] + (a[0] - b[0]) * (a[1] + b[1]))
        normal = _unit(normal)
        face['normal'] = normal
        for part in face['loops']:
            for index in part:
                offset = [points[index][i] - points[loop[0]][i] for i in range(3)]
                worst = max(worst, abs(_dot(offset, normal)))
    return worst


def stack_level(solid):
    """The height at which the next course stands on this element, in mm.

    Elements with the raised top profile carry the next course 50 mm below
    their highest point, on the floor between the ridges; flat ones on top.
    """
    top = max(p[2] for p in solid['points'])
    for face in solid['faces']:
        if face['normal'][2] > 0.999 and abs(solid['points'][face['loops'][0][0]][2] - (top - 50.0)) < 0.01:
            return top - 50.0
    return top


def outline_key(solid):
    return sorted(tuple(round(c) for c in p) for p in solid['points'])


def closed(solid):
    seen = {}
    for face in solid['faces']:
        for loop in face['loops']:
            for i, index in enumerate(loop):
                edge = (index, loop[(i + 1) % len(loop)])
                seen[edge] = seen.get(edge, 0) + 1
    return all(count == 1 and seen.get((b, a), 0) == 1 for (a, b), count in seen.items())


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _unit(v):
    length = math.sqrt(_dot(v, v))
    return (v[0] / length, v[1] / length, v[2] / length)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def picture(solid, path, width=280, height=200):
    """A shaded view from the front left, with hidden surfaces removed per pixel.

    Every face that looks towards the eye is filled row by row where it is
    nearer than what is already there (a depth buffer). An outline is drawn
    only where its own face is the visible one. Drawn three times as large and
    scaled down for smooth lines.
    """
    from PIL import Image
    over = 3
    w, h = width * over, height * over
    eye = _unit((-1.0, -1.0, 0.8))
    right = _unit(_cross((0.0, 0.0, 1.0), eye))
    up = _cross(eye, right)
    points = solid['points']
    mid = [(max(p[i] for p in points) + min(p[i] for p in points)) / 2.0 for i in range(3)]
    rel = [tuple(p[i] - mid[i] for i in range(3)) for p in points]
    scale = (w - 24 * over) / 830.0
    screen = [(w / 2.0 + _dot(p, right) * scale, h / 2.0 - _dot(p, up) * scale) for p in rel]

    nearest = [-1e9] * (w * h)          # mm towards the eye, per pixel
    shade = bytearray([255]) * (w * h)
    front = []
    for face in solid['faces']:
        n = face['normal']
        facing = _dot(n, eye)
        if facing <= 1e-6:
            continue
        # Nearness of the face's plane at pixel (x, y): kx * x + ky * y + k0.
        kx = -_dot(n, right) / facing / scale
        ky = _dot(n, up) / facing / scale
        k0 = _dot(n, rel[face['loops'][0][0]]) / facing - kx * w / 2.0 - ky * h / 2.0
        front.append((face, kx, ky, k0))
        grey = int(168 + 72 * max(0.0, n[2]) + 28 * max(0.0, _dot(n, right)))
        edges = []
        for loop in face['loops']:
            for i in range(len(loop)):
                a, b = screen[loop[i]], screen[loop[(i + 1) % len(loop)]]
                if a[1] != b[1]:
                    edges.append((a, b) if a[1] < b[1] else (b, a))
        if not edges:
            continue
        top = max(0, int(math.ceil(min(a[1] for a, b in edges) - 0.5)))
        bottom = min(h - 1, int(math.floor(max(b[1] for a, b in edges) - 0.5)))
        for row in range(top, bottom + 1):
            y = row + 0.5
            crossings = sorted(a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                               for a, b in edges if a[1] <= y < b[1])
            for left, stop in zip(crossings[0::2], crossings[1::2]):
                first = max(0, int(math.ceil(left - 0.5)))
                last = min(w - 1, int(math.floor(stop - 0.5)))
                at = row * w + first
                near = kx * (first + 0.5) + ky * y + k0
                for column in range(first, last + 1):
                    if near > nearest[at]:
                        nearest[at] = near
                        shade[at] = grey
                    at += 1
                    near += kx

    reach = over // 2
    for face, kx, ky, k0 in front:
        for loop in face['loops']:
            for i in range(len(loop)):
                a, b = screen[loop[i]], screen[loop[(i + 1) % len(loop)]]
                steps = int(max(abs(b[0] - a[0]), abs(b[1] - a[1]))) + 1
                for step in range(steps + 1):
                    x = a[0] + (b[0] - a[0]) * step / steps
                    y = a[1] + (b[1] - a[1]) * step / steps
                    near = kx * x + ky * y + k0
                    column, row = int(x), int(y)
                    for dy in range(-reach, reach + 1):
                        for dx in range(-reach, reach + 1):
                            cx, cy = column + dx, row + dy
                            # 2 mm of slack: an edge is shared by two faces
                            if 0 <= cx < w and 0 <= cy < h and near > nearest[cy * w + cx] - 2.0:
                                shade[cy * w + cx] = 40

    Image.frombytes('L', (w, h), bytes(shade)).resize((width, height), Image.LANCZOS).save(path)


def build():
    meshes = ms.read_3ds(SOURCE)
    solids = {}
    for index, name in NAMES.items():
        solids[name] = ms.solid_from_mesh(meshes[index])
    for name, size in PARTITION.items():
        solids[name] = box(size)
    for name, (twin, by) in REBUILD.items():
        solids[name] = lowered(solids[twin], by)
    for solid in solids.values():
        straighten(solid)
    return solids


def check_lowering(solids):
    """The rebuild method must reproduce a sound mesh exactly."""
    return outline_key(lowered(solids['S0/2 250 W'], 50.0)) == outline_key(solids['S0/2 200 W'])


def main():
    pictures = '--no-pictures' not in sys.argv
    if not os.path.isfile(SOURCE):
        raise SystemExit('Source file missing: %s' % SOURCE)
    solids = build()
    if not check_lowering(solids):
        raise SystemExit('The rebuild check failed - S0/2 200 P cannot be trusted.')

    if not os.path.isdir(TARGET):
        os.makedirs(TARGET)
    blocks, bad = [], []
    for family, names in FAMILIES:
        for name in names:
            solid = solids[name]
            off = bend(solid)
            if off > 1e-6:
                print('  %-14s worst point %.4f mm off its face' % (name, off))
            if solid['problems'] or not closed(solid) or ms.volume(solid) <= 0:
                bad.append(name)
            size = [round(max(p[i] for p in solid['points'])) for i in range(3)]
            blocks.append({
                'id': block_id(name), 'name': name, 'family': family, 'size': size,
                'stack': round(stack_level(solid), 1),
                'points': [[round(c, 1) for c in p] for p in solid['points']],
                'faces': [{'normal': [round(c, 9) for c in face['normal']], 'loops': face['loops']}
                          for face in solid['faces']],
            })
            if pictures:
                picture(solid, os.path.join(TARGET, block_id(name) + '.png'))
    if bad:
        raise SystemExit('Not closed solids: %s' % ', '.join(bad))
    if len({b['id'] for b in blocks}) != len(blocks):
        raise SystemExit('Two elements share an id.')

    with open(os.path.join(TARGET, 'blocks.json'), 'w', encoding='utf-8', newline='\n') as handle:
        json.dump({'unit': 'mm', 'blocks': blocks}, handle, separators=(',', ':'))
        handle.write('\n')
    print('%d elements written to %s' % (len(blocks), TARGET))


if __name__ == '__main__':
    main()
