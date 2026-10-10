# -*- coding: utf-8 -*-
"""Pack one add-in into a ZIP for a release.

    python tools/release.py system3e
    python tools/release.py all

Writes dist/<AddIn>-<version>.zip (dist/ is not in Git). The ZIP holds the
add-in folder exactly as Fusion wants it - unpack it into Fusion's add-in
directory. Deflate at the highest level, so every unpacker can read it.
Refuses to pack when VERSION and the manifest disagree. Standard library only.
"""
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import set_version

REPO = os.path.dirname(HERE)
DIST = os.path.join(REPO, 'dist')
SKIP_DIRS = ('__pycache__',)
SKIP_ENDS = ('.pyc', '.pyo', 'Thumbs.db', '.DS_Store')


def pack(name):
    version_file, manifest = set_version.addins()[name]
    version = set_version.read(version_file).strip()
    if version != set_version.manifest_version(manifest) or not set_version.PATTERN.match(version):
        raise SystemExit('%s: VERSION and manifest disagree - run tools/set_version.py first.' % name)
    folder = os.path.dirname(manifest)
    addin = os.path.basename(folder)
    if not os.path.isdir(DIST):
        os.makedirs(DIST)
    target = os.path.join(DIST, '%s-%s.zip' % (addin, version))
    count = 0
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for root, dirs, files in os.walk(folder):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for entry in sorted(files):
                if entry.endswith(SKIP_ENDS):
                    continue
                path = os.path.join(root, entry)
                inside = os.path.join(addin, os.path.relpath(path, folder)).replace(os.sep, '/')
                archive.write(path, inside)
                count += 1
    with zipfile.ZipFile(target) as archive:
        broken = archive.testzip()
        if broken:
            raise SystemExit('%s: %s is damaged in the ZIP' % (name, broken))
    print('%-12s %s  %d files, %d KB' % (name, os.path.relpath(target, REPO), count,
                                         os.path.getsize(target) // 1024))
    return target


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    known = set_version.addins()
    names = sorted(known) if sys.argv[1] == 'all' else [sys.argv[1]]
    for name in names:
        if name not in known:
            raise SystemExit('No add-in "%s". There are: %s' % (name, ', '.join(sorted(known))))
        pack(name)


if __name__ == '__main__':
    main()
