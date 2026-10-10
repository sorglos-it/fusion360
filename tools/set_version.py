# -*- coding: utf-8 -*-
"""Set the version of one add-in, or of all, in every place it is kept.

    python tools/set_version.py system3e 1.0.0.1
    python tools/set_version.py all 1.0.0.0
    python tools/set_version.py --check

The number lives in apps/desktop-<name>/VERSION; the add-in's manifest carries
a copy, because that is what Fusion and the dialog title read. This script
writes both, so they are never edited by hand in two places. --check reports
any add-in whose two numbers differ. Four numbers, v.x.y.z. Standard library
only.
"""
import io
import os
import re
import sys
import glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(REPO, 'apps')
PATTERN = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
IN_MANIFEST = re.compile(r'("version"\s*:\s*")[^"]*(")')


def addins():
    """{name: (version file, manifest file)} for every apps/desktop-<name>."""
    found = {}
    for folder in sorted(glob.glob(os.path.join(APPS, 'desktop-*'))):
        manifests = glob.glob(os.path.join(folder, '*', '*.manifest'))
        if len(manifests) == 1:
            found[os.path.basename(folder)[len('desktop-'):]] = (
                os.path.join(folder, 'VERSION'), manifests[0])
    return found


def read(path):
    with io.open(path, encoding='utf-8') as handle:
        return handle.read()


def write(path, text):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as handle:
        handle.write(text)


def manifest_version(path):
    match = IN_MANIFEST.search(read(path))
    return match.group(0).split('"')[-2] if match else ''


def check():
    wrong = 0
    for name, (version_file, manifest) in addins().items():
        version = read(version_file).strip() if os.path.isfile(version_file) else ''
        same = version == manifest_version(manifest) and PATTERN.match(version)
        wrong += not same
        print('%-12s VERSION %-10s manifest %-10s %s' % (
            name, version, manifest_version(manifest), 'ok' if same else 'DIFFERENT OR NOT v.x.y.z'))
    return 1 if wrong else 0


def main():
    if sys.argv[1:] == ['--check']:
        raise SystemExit(check())
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    which, version = sys.argv[1], sys.argv[2]
    if not PATTERN.match(version):
        raise SystemExit('The version needs four numbers, like 1.0.0.0 - got %r' % version)
    known = addins()
    names = sorted(known) if which == 'all' else [which]
    for name in names:
        if name not in known:
            raise SystemExit('No add-in "%s". There are: %s' % (name, ', '.join(sorted(known))))
    for name in names:
        version_file, manifest = known[name]
        text = read(manifest)
        if not IN_MANIFEST.search(text):
            raise SystemExit('No "version" entry in %s' % manifest)
        write(version_file, version + '\n')
        write(manifest, IN_MANIFEST.sub(lambda m: m.group(1) + version + m.group(2), text, count=1))
        print('%-12s %s' % (name, version))


if __name__ == '__main__':
    main()
