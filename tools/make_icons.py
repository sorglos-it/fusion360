# -*- coding: utf-8 -*-
"""Generate the toolbar icons for the PrintGear add-in (standard library only).

    python tools/make_icons.py

The icon is not a drawing of a gear - it is a gear, rasterised straight from
printgear_math. A meshing pair, because the pair is the point of the add-in.
"""

import os
import sys
import math
import zlib
import struct

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
ADDIN = os.environ.get('PRINTGEAR_ADDIN_DIR') or os.path.join(REPO, 'apps', 'desktop', 'PrintGear')
OUT = os.path.join(ADDIN, 'resources', 'PrintGear')

sys.path.insert(0, ADDIN)
import printgear_math as pg          # noqa: E402

DARK = (0x2E, 0x3A, 0x45)
ACCENT = (0xE8, 0x8A, 0x1E)

SS = 4                  # subpixel rows, and horizontal coverage is exact
SIZES = (16, 32, 64)

# Few teeth, or a 16 pixel icon turns into a smudge.
BIG_TEETH = 14
SMALL_TEETH = 8
BORE_FRACTION = 0.30    # of the root radius


def gear_outlines():
    """Outlines of a meshing pair, in millimetres, centred on their own axes."""
    module = 1.0
    alpha = math.radians(20.0)
    big = pg.GearSpec(module, BIG_TEETH, backlash=0.0,
                      profile_shift=pg.auto_profile_shift(BIG_TEETH, alpha))
    small = pg.GearSpec(module, SMALL_TEETH, backlash=0.0,
                        profile_shift=pg.auto_profile_shift(SMALL_TEETH, alpha))
    distance = pg.working_center_distance(big, small)
    rotation = pg.mesh_rotation(big, 0.0, small, 0.0)

    def placed(spec, angle, cx, cy):
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        outline = [(x * cos_a - y * sin_a + cx, x * sin_a + y * cos_a + cy)
                   for x, y in pg.tooth_profile(spec)]
        bore = spec.root_radius * BORE_FRACTION
        circle = [(cx + bore * math.cos(2.0 * math.pi * i / 24.0),
                   cy + bore * math.sin(2.0 * math.pi * i / 24.0))
                  for i in range(24)]
        return [outline, circle]

    # Tilt the pair so the small gear sits up and to the right, which reads
    # better in a square than a dead horizontal pair.
    bearing = math.radians(35.0)
    small_x = distance * math.cos(bearing)
    small_y = distance * math.sin(bearing)
    return (placed(big, 0.0, 0.0, 0.0),
            placed(small, pg.mesh_rotation(big, 0.0, small, bearing),
                   small_x, small_y))


def fit(shapes, size, margin):
    """Scale every loop into a size x size image, y flipped for image space."""
    points = [point for group in shapes for loop in group for point in loop]
    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)
    span = max(max_x - min_x, max_y - min_y)
    scale = (size - 2.0 * margin) / span
    offset_x = margin + ((max_y - min_y) - (max_x - min_x)) * scale / 2.0
    offset_y = margin + ((max_x - min_x) - (max_y - min_y)) * scale / 2.0

    def convert(loop):
        return [((x - min_x) * scale + max(offset_x, margin),
                 size - ((y - min_y) * scale + max(offset_y, margin)))
                for x, y in loop]
    return [[convert(loop) for loop in group] for group in shapes]


def coverage(loops, size):
    """Even-odd rasterisation of a set of loops. Returns one alpha per pixel.

    Scanline rather than testing every subpixel against every edge: at icon
    sizes that is the difference between instant and a coffee break.
    """
    alpha = [0.0] * (size * size)
    edges = []
    for loop in loops:
        for index in range(len(loop)):
            x0, y0 = loop[index]
            x1, y1 = loop[(index + 1) % len(loop)]
            if y0 != y1:
                edges.append((x0, y0, x1, y1))

    weight = 1.0 / SS
    for row in range(size):
        for sub in range(SS):
            y = row + (sub + 0.5) / SS
            crossings = []
            for x0, y0, x1, y1 in edges:
                if (y0 <= y < y1) or (y1 <= y < y0):
                    crossings.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            if not crossings:
                continue
            crossings.sort()
            for pair in range(0, len(crossings) - 1, 2):
                left, right = crossings[pair], crossings[pair + 1]
                if right <= 0.0 or left >= size:
                    continue
                left, right = max(left, 0.0), min(right, float(size))
                first, last = int(left), min(int(right), size - 1)
                for column in range(first, last + 1):
                    covered = min(right, column + 1.0) - max(left, float(column))
                    if covered > 0.0:
                        alpha[row * size + column] += covered * weight
    return [min(1.0, value) for value in alpha]


def render(size):
    margin = max(1.0, size * 0.06)
    big, small = fit(list(gear_outlines()), size, margin)
    layers = ((coverage(big, size), DARK), (coverage(small, size), ACCENT))

    buffer = bytearray(size * size * 4)
    for index in range(size * size):
        red = green = blue = 0.0
        total = 0.0
        # Painted back to front: the accent gear sits on top of the dark one.
        for values, colour in layers:
            a = values[index]
            if a <= 0.0:
                continue
            red = colour[0] * a + red * (1.0 - a)
            green = colour[1] * a + green * (1.0 - a)
            blue = colour[2] * a + blue * (1.0 - a)
            total = a + total * (1.0 - a)
        if total <= 0.0:
            continue
        offset = index * 4
        buffer[offset] = int(round(red))
        buffer[offset + 1] = int(round(green))
        buffer[offset + 2] = int(round(blue))
        buffer[offset + 3] = int(round(total * 255))
    return bytes(buffer)


def write_png(path, size, rgba):
    raw = b''.join(b'\x00' + rgba[y * size * 4:(y + 1) * size * 4]
                   for y in range(size))

    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data
                + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(raw, 9))
           + chunk(b'IEND', b''))
    with open(path, 'wb') as handle:
        handle.write(png)


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for size in SIZES:
        path = os.path.join(OUT, '%dx%d.png' % (size, size))
        write_png(path, size, render(size))
        print('wrote %s' % path)


if __name__ == '__main__':
    main()
