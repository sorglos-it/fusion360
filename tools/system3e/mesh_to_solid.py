# -*- coding: utf-8 -*-
"""Turn the triangle meshes of a .3ds file into clean solids with flat faces.

    python tools/system3e/mesh_to_solid.py "assets/system3e/SYSTEM 3E START.3ds" --report

The manufacturer's 3D file holds every element as a loose triangle mesh:
triangles that only touch along part of an edge, doubled points, slivers.
Fusion cannot make a body from that. This module welds the points, joins all
triangles lying in one plane into a single outline and checks that the result
is a closed solid - every edge used by exactly two faces, once in each
direction. Standard library only.
"""
import math
import struct
import sys

WELD = 0.3          # mm - points closer than this are one point
PLANE_FACING = 0.99 # cos of the angle a triangle may differ from its plane (8 degrees)
PLANE_DIST = 0.2    # mm - how far a triangle's points may lie off its plane
ON_EDGE = 0.05      # mm - a point this close to an edge splits it


def read_3ds(path):
    """Every mesh of the file as {'name', 'points' (mm), 'triangles'}."""
    with open(path, 'rb') as handle:
        data = handle.read()
    meshes = []
    scale = [1.0]

    def walk(start, end, current):
        pos = start
        while pos + 6 <= end:
            chunk, length = struct.unpack_from('<HI', data, pos)
            if length < 6 or pos + length > end:
                break
            body = pos + 6
            if chunk == 0x4000:                      # named object
                zero = data.index(b'\0', body)
                mesh = {'name': data[body:zero].decode('latin-1'),
                        'points': [], 'triangles': []}
                meshes.append(mesh)
                walk(zero + 1, pos + length, mesh)
            elif chunk in (0x4D4D, 0x3D3D, 0x4100):  # containers
                walk(body, pos + length, current)
            elif chunk == 0x0100:                    # master scale: units per inch
                scale[0] = struct.unpack_from('<f', data, body)[0]
            elif chunk == 0x4110 and current is not None:
                count = struct.unpack_from('<H', data, body)[0]
                flat = struct.unpack_from('<%df' % (count * 3), data, body + 2)
                current['points'] = [flat[i:i + 3] for i in range(0, count * 3, 3)]
            elif chunk == 0x4120 and current is not None:
                count = struct.unpack_from('<H', data, body)[0]
                flat = struct.unpack_from('<%dH' % (count * 4), data, body + 2)
                current['triangles'] = [flat[i:i + 3] for i in range(0, count * 4, 4)]
            pos += length

    walk(0, len(data), None)
    # 39.37 units per inch means the file is in metres.
    to_mm = 1000.0 if abs(scale[0] - 39.3701) < 0.01 else 1.0
    result = []
    for mesh in meshes:
        if not mesh['points']:
            continue
        mesh['points'] = [tuple(c * to_mm for c in p) for p in mesh['points']]
        result.append(mesh)
    return result


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _length(a):
    return math.sqrt(_dot(a, a))


def weld(points):
    """Merge points closer than WELD. Returns (points, old index -> new index)."""
    merged, remap, grid = [], [], {}
    for point in points:
        cell = tuple(int(math.floor(c / WELD)) for c in point)
        found = None
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for index in grid.get((cell[0] + dx, cell[1] + dy, cell[2] + dz), ()):
                        if _length(_sub(merged[index], point)) < WELD:
                            found = index
                            break
                    if found is not None:
                        break
                if found is not None:
                    break
            if found is not None:
                break
        if found is None:
            found = len(merged)
            merged.append(point)
            grid.setdefault(cell, []).append(found)
        remap.append(found)
    return merged, remap


def _split_edge(a, b, points, candidates):
    """The chain a .. b with every point lying on the open segment put in between."""
    pa, pb = points[a], points[b]
    direction = _sub(pb, pa)
    span = _length(direction)
    inside = []
    for index in candidates:
        if index == a or index == b:
            continue
        offset = _sub(points[index], pa)
        along = _dot(offset, direction) / span
        if along <= ON_EDGE or along >= span - ON_EDGE:
            continue
        if _length(_cross(offset, direction)) / span < ON_EDGE:
            inside.append((along, index))
    return [a] + [index for along, index in sorted(inside)] + [b]


def _area(loop, points, normal):
    """Signed area of a loop seen against its face normal."""
    total = (0.0, 0.0, 0.0)
    origin = points[loop[0]]
    for i in range(1, len(loop) - 1):
        part = _cross(_sub(points[loop[i]], origin), _sub(points[loop[i + 1]], origin))
        total = (total[0] + part[0], total[1] + part[1], total[2] + part[2])
    return _dot(total, normal) / 2.0


def _inside(point, loop, points, normal):
    """Is the point inside the loop? Both lie in the plane with this normal."""
    drop = max(range(3), key=lambda i: abs(normal[i]))
    u, v = [i for i in range(3) if i != drop]
    x, y = point[u], point[v]
    hit = False
    for i in range(len(loop)):
        p, q = points[loop[i]], points[loop[(i + 1) % len(loop)]]
        if (p[v] > y) != (q[v] > y):
            if x < p[u] + (y - p[v]) * (q[u] - p[u]) / (q[v] - p[v]):
                hit = not hit
    return hit


def solid_from_mesh(mesh):
    """{'points', 'faces': [{'normal', 'loops'}], 'problems': [...]}.

    The first loop of a face is its outline, counter-clockwise seen from
    outside; further loops are holes. Points are mm, moved so that the
    lowest corner of the bounding box is the origin.
    """
    problems = []
    points, remap = weld(mesh['points'])
    low = tuple(min(p[i] for p in points) for i in range(3))
    points = [tuple(round(p[i] - low[i], 3) for i in range(3)) for p in points]

    # --- sort the triangles into planes ---------------------------------------
    # Large triangles first: they give a plane its direction. A narrow one has
    # an unreliable normal of its own, so it joins the plane its three points
    # lie in instead of being compared by direction alone.
    sized = []
    for tri in mesh['triangles']:
        a, b, c = (remap[i] for i in tri)
        if len({a, b, c}) < 3:
            continue
        normal = _cross(_sub(points[b], points[a]), _sub(points[c], points[a]))
        size = _length(normal)
        longest = max(_length(_sub(points[b], points[a])), _length(_sub(points[c], points[b])),
                      _length(_sub(points[a], points[c])))
        if size / longest < ON_EDGE:   # a sliver: no area, its points split the neighbours
            continue
        sized.append((size, (a, b, c), tuple(n / size for n in normal)))
    sized.sort(key=lambda item: -item[0])

    planes = []          # [normal, distance, [triangles]]
    for size, tri, normal in sized:
        best = None
        for plane in planes:
            facing = _dot(plane[0], normal)
            if facing < PLANE_FACING:
                continue
            if max(abs(_dot(plane[0], points[i]) - plane[1]) for i in tri) < PLANE_DIST:
                if best is None or facing > best[0]:
                    best = (facing, plane)
        if best:
            best[1][2].append(tri)
        else:
            planes.append([normal, _dot(normal, points[tri[0]]), [tri]])

    # --- outline of every plane -----------------------------------------------
    everything = range(len(points))
    faces = []
    for normal, distance, triangles in planes:
        edges = {}
        for tri in triangles:
            for i in range(3):
                chain = _split_edge(tri[i], tri[(i + 1) % 3], points, everything)
                for start, end in zip(chain, chain[1:]):
                    edges[(start, end)] = edges.get((start, end), 0) + 1
        boundary = {}
        for (start, end), count in edges.items():
            rest = count - edges.get((end, start), 0)
            if rest > 0:
                boundary.setdefault(start, []).extend([end] * rest)
        loops = []
        while boundary:
            first = next(iter(boundary))
            loop, here = [first], first
            while True:
                exits = boundary.get(here)
                if not exits:
                    problems.append('open outline')
                    break
                if len(exits) > 1 and len(loop) > 1:
                    # two outlines touch in this point: take the sharpest left turn
                    came = _sub(points[here], points[loop[-2]])
                    exits.sort(key=lambda e: math.atan2(
                        _dot(_cross(came, _sub(points[e], points[here])), normal),
                        _dot(came, _sub(points[e], points[here]))))
                nxt = exits.pop()
                if not exits:
                    del boundary[here]
                if nxt == first:
                    break
                loop.append(nxt)
                here = nxt
            if len(loop) >= 3:
                loops.append(loop)
        outlines = [l for l in loops if _area(l, points, normal) > 0]
        holes = [l for l in loops if _area(l, points, normal) <= 0]
        group = [{'normal': normal, 'loops': [outline]} for outline in outlines]
        for hole in holes:
            for face in group:
                if _inside(points[hole[0]], face['loops'][0], points, normal):
                    face['loops'].append(hole)
                    break
            else:
                problems.append('hole without a face')
        faces.extend(group)

    # --- drop points that only sit in the middle of a straight edge -----------
    neighbours = {}
    for face in faces:
        for loop in face['loops']:
            for i, index in enumerate(loop):
                neighbours.setdefault(index, set()).update((loop[i - 1], loop[(i + 1) % len(loop)]))
    straight = set()
    for index, around in neighbours.items():
        if len(around) == 2:
            p, q = (points[i] for i in around)
            if _length(_cross(_sub(points[index], p), _sub(q, p))) / max(_length(_sub(q, p)), 1e-9) < ON_EDGE:
                straight.add(index)
    for face in faces:
        face['loops'] = [[i for i in loop if i not in straight] for loop in face['loops']]

    # --- closed? every edge once in each direction -----------------------------
    seen = {}
    for face in faces:
        for loop in face['loops']:
            for i, index in enumerate(loop):
                edge = (index, loop[(i + 1) % len(loop)])
                seen[edge] = seen.get(edge, 0) + 1
    loose = sum(1 for (a, b), count in seen.items() if count != 1 or seen.get((b, a), 0) != 1)
    if loose:
        problems.append('%d loose edges' % loose)

    # --- renumber the points that are still used ------------------------------
    used = sorted({i for face in faces for loop in face['loops'] for i in loop})
    number = {old: new for new, old in enumerate(used)}
    for face in faces:
        face['loops'] = [[number[i] for i in loop] for loop in face['loops']]
        face['normal'] = tuple(round(n, 6) for n in face['normal'])
    return {'points': [points[i] for i in used], 'faces': faces, 'problems': problems}


def volume(solid):
    """Volume in litres - positive when the faces point outwards."""
    points, total = solid['points'], 0.0
    for face in solid['faces']:
        for loop in face['loops']:
            origin = points[loop[0]]
            for i in range(1, len(loop) - 1):
                total += _dot(origin, _cross(points[loop[i]], points[loop[i + 1]])) / 6.0
    return total / 1e6


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    meshes = read_3ds(sys.argv[1])
    good = 0
    for index, mesh in enumerate(meshes):
        solid = solid_from_mesh(mesh)
        size = [max(p[i] for p in solid['points']) for i in range(3)]
        state = 'ok' if not solid['problems'] else '; '.join(sorted(set(solid['problems'])))
        good += not solid['problems']
        print('#%2d  %4.0f x %3.0f x %3.0f mm  points=%3d faces=%3d  %5.1f l  %s' % (
            index, size[0], size[1], size[2], len(solid['points']), len(solid['faces']),
            volume(solid), state))
    print('%d of %d meshes became closed solids' % (good, len(meshes)))


if __name__ == '__main__':
    main()
