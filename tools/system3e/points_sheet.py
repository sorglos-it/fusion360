# -*- coding: utf-8 -*-
"""Draw one element with every point the add-in knows on it, as an SVG.

    python tools/system3e/points_sheet.py "S1 WP" docs/system3e/s1-wp-punkte.svg

Three plain views (from above, from the long side, from the end) and one
slanted view. The numbers are the same in every view. Colours:

    yellow  a point that can be clicked as the place for the next element
    red     a point the add-in can put on the clicked place ("Placed by")
    green   both

The points are taken from the add-in itself, so the sheet cannot drift from
what it really does. Standard library only.
"""
import os
import sys
import json
import math
import types

HERE = os.path.dirname(os.path.abspath(__file__))
ADDIN = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'apps', 'desktop-system3e', 'System3E')
S = 0.6     # pixels per mm
KINDS = {'click': ('y', 'anklickbar'), 'anchor': ('r', 'Ausrichtungspunkt'), 'both': ('g', 'beides')}


def addin_module():
    adsk = types.ModuleType('adsk')
    adsk.core = types.ModuleType('adsk.core')
    adsk.fusion = types.ModuleType('adsk.fusion')
    for name in ('CommandEventHandler', 'ValidateInputsEventHandler',
                 'InputChangedEventHandler', 'CommandCreatedEventHandler'):
        setattr(adsk.core, name, type(name, (object,), {}))
    sys.modules.update({'adsk': adsk, 'adsk.core': adsk.core, 'adsk.fusion': adsk.fusion})
    sys.path.insert(0, ADDIN)
    import System3E
    System3E.S.load('de')
    return System3E


def all_points(addin, block):
    """[(text, position, kind)] - clickable points and anchors, merged where they coincide."""
    found = []
    for key, shown, meant in addin.shown_points(block):
        found.append([addin.T(key), tuple(shown), 'click'])
    for anchor in addin.ANCHORS:
        position = tuple(addin.anchor_position(block, anchor))
        for entry in found:
            if entry[1] == position:
                entry[2] = 'both'
                break
        else:
            found.append([addin.T(addin.anchor_text(anchor)), position, 'anchor'])
    return found


def edges_of(block):
    seen = set()
    for face in block['faces']:
        for loop in face['loops']:
            for i, a in enumerate(loop):
                b = loop[(i + 1) % len(loop)]
                seen.add((min(a, b), max(a, b)))
    return sorted(seen)


def main():
    name, target = sys.argv[1], sys.argv[2]
    addin = addin_module()
    with open(os.path.join(ADDIN, 'blocks', 'blocks.json'), 'r', encoding='utf-8') as handle:
        block = [b for b in json.load(handle)['blocks'] if b['name'] == name][0]
    points = block['points']
    length, width, height = block['size']
    spots = all_points(addin, block)
    out = []

    def view(title, x0, y0, flat, h, axes):
        """One plain view: flat(p) gives (right, up) in mm."""
        out.append('<text x="%d" y="%d" class="t">%s</text>' % (x0, y0 - 14, title))
        for a, b in edges_of(block):
            (ax, ay), (bx, by) = flat(points[a]), flat(points[b])
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="e"/>' % (
                x0 + ax * S, y0 + (h - ay) * S, x0 + bx * S, y0 + (h - by) * S))
        out.append('<text x="%d" y="%.0f" class="a">%s →</text>' % (x0, y0 + h * S + 18, axes[0]))
        out.append('<text x="%d" y="%d" class="a">↑ %s</text>' % (x0 - 48, y0 + 12, axes[1]))
        placed = {}
        for number, (text, p, kind) in enumerate(spots, 1):
            px, py = flat(p)
            cx, cy = x0 + px * S, y0 + (h - py) * S
            stack = placed.setdefault((round(cx), round(cy)), [])
            stack.append(number)
            # Points lying behind one another in this view become rings.
            out.append('<circle cx="%.1f" cy="%.1f" r="%d" class="%s"/>' % (
                cx, cy, max(3, 10 - 3 * (len(stack) - 1)), KINDS[kind][0]))
        for (cx, cy), numbers in placed.items():
            out.append('<text x="%d" y="%d" class="n">%s</text>' % (
                cx + 13, cy - 11, ' + '.join(str(n) for n in numbers)))

    view('Von oben', 70, 60, lambda p: (p[0], p[1]), width, ('Länge (X)', 'Y'))
    view('Von der langen Seite', 70, 330, lambda p: (p[0], p[2]), height, ('Länge (X)', 'Höhe'))
    view('Vom vorderen Ende', 600, 330, lambda p: (p[1], p[2]), height, ('Wanddicke (Y)', 'Höhe'))

    # --- slanted view: faces towards the eye, far ones first -----------------
    eye = (-1.0, -1.0, 0.8)
    n = math.sqrt(sum(c * c for c in eye))
    eye = tuple(c / n for c in eye)
    right = (-eye[1], eye[0], 0.0)                       # across the view: up-axis x eye
    n = math.sqrt(sum(c * c for c in right))
    right = tuple(c / n for c in right)
    up = (eye[1] * right[2] - eye[2] * right[1], eye[2] * right[0] - eye[0] * right[2],
          eye[0] * right[1] - eye[1] * right[0])

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    ox, oy = 790, 170

    def slanted(p):
        q = (p[0] - length / 2.0, p[1] - width / 2.0, p[2] - height / 2.0)
        return ox + dot(q, right) * S * 0.62, oy - dot(q, up) * S * 0.62

    out.append('<text x="600" y="46" class="t">Schräg von vorne links</text>')
    faces = [f for f in block['faces'] if dot(f['normal'], eye) > 1e-6]
    faces.sort(key=lambda f: sum(dot(points[i], eye) for i in f['loops'][0]) / len(f['loops'][0]))
    for face in faces:
        out.append('<polygon points="%s" class="f"/>' % ' '.join(
            '%.1f,%.1f' % slanted(points[i]) for i in face['loops'][0]))
    for number, (text, p, kind) in enumerate(spots, 1):
        cx, cy = slanted(p)
        out.append('<circle cx="%.1f" cy="%.1f" r="8" class="%s" fill-opacity="0.85"/>' % (
            cx, cy, KINDS[kind][0]))
        out.append('<text x="%.0f" y="%.0f" class="n">%d</text>' % (cx + 11, cy - 9, number))

    # --- legend ---------------------------------------------------------------
    out.append('<text x="70" y="580" class="t">Punkte (mm: Länge / Wanddicke / Höhe)</text>')
    for number, (text, p, kind) in enumerate(spots, 1):
        y = 582 + number * 24
        out.append('<circle cx="80" cy="%d" r="8" class="%s"/>' % (y - 5, KINDS[kind][0]))
        out.append('<text x="98" y="%d" class="l">%d  %s  –  %g / %g / %g  –  %s</text>' % (
            y, number, text, p[0], p[1], p[2], KINDS[kind][1]))
    for row, (cls, text) in enumerate((
            ('y', 'Gelb: kann angeklickt werden (Ziel für den nächsten Stein)'),
            ('r', 'Rot: Ausrichtungspunkt des Plugins („Setzen an“)'),
            ('g', 'Grün: beides'))):
        out.append('<circle cx="560" cy="%d" r="8" class="%s"/>' % (601 + row * 24, cls))
        out.append('<text x="578" y="%d" class="l">%s</text>' % (606 + row * 24, text))
    out.append('<text x="560" y="690" class="l">„Vorne“ ist das Ende bei Länge 0, „hinten“ das andere Ende.</text>')
    out.append('<text x="560" y="714" class="l">Baustein %s: %d x %d x %d mm</text>' % (name, length, width, height))

    tall = max(790, 620 + len(spots) * 24)       # room for the legend
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 %d" font-family="Arial, sans-serif">\n'
           '<style>.e{stroke:#444;stroke-width:1}.f{fill:#f2f2f2;stroke:#444;stroke-width:1}'
           '.y{fill:#ffd400;stroke:#191919;stroke-width:1.5}.r{fill:#e02020;stroke:#191919;stroke-width:1.5}'
           '.g{fill:#2fb344;stroke:#191919;stroke-width:1.5}.t{font-size:17px;font-weight:bold;fill:#191919}'
           '.n{font-size:16px;font-weight:bold;fill:#191919}.l{font-size:15px;fill:#191919}'
           '.a{font-size:12px;fill:#777}</style>\n<rect width="1000" height="%d" fill="#fff"/>\n'
           ) % (tall, tall) + '\n'.join(out) + '\n</svg>\n'
    with open(target, 'w', encoding='utf-8', newline='\n') as handle:
        handle.write(svg)
    print('written %s, %d points' % (target, len(spots)))


if __name__ == '__main__':
    main()
