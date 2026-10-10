# -*- coding: utf-8 -*-
"""Check the documentation under docs/<name>/<language>/ - and repair jump marks.

    python tools/check_docs.py
    python tools/check_docs.py --fix

The English files are the ones that are maintained; de, it, es and fr are
produced from them. This checks for every add-in that all five languages hold
the same files with the same number of headings, table rows and code blocks,
and that every link leads somewhere - the file and, where given, the heading
behind the '#'.

A heading changes with the language and its jump mark with it. --fix rewrites
a jump mark that still names the English heading to the heading at the same
place in the translated file. Standard library only.
"""
import io
import os
import re
import sys
import glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
LANGUAGES = ('en', 'de', 'it', 'es', 'fr')
LINK = re.compile(r'\]\(([^)\s]+)\)')


def read(path):
    with io.open(path, encoding='utf-8') as handle:
        return handle.read()


def outside_code(text):
    """The lines that are not inside a ``` block."""
    lines, inside = [], False
    for line in text.splitlines():
        if line.lstrip().startswith('```'):
            inside = not inside
            continue
        if not inside:
            lines.append(line)
    return lines


def slug(heading):
    """The jump mark GitHub gives a heading."""
    text = re.sub(r'[`*_]', '', heading.strip().lower())
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'[^\w\- ]', '', text, flags=re.UNICODE)
    return text.replace(' ', '-')


def slugs(path):
    found, seen = [], {}
    for line in outside_code(read(path)):
        match = re.match(r'^(#{1,6})\s+(.*?)\s*#*$', line)
        if match:
            name = slug(match.group(2))
            count = seen.get(name, 0)
            seen[name] = count + 1
            found.append(name if count == 0 else '%s-%d' % (name, count))
    return found


def shape(path):
    text = read(path)
    lines = outside_code(text)
    return (sum(1 for l in lines if re.match(r'^#{1,6}\s', l)),
            sum(1 for l in lines if l.lstrip().startswith('|')),
            text.count('```') // 2)


def main():
    fix = '--fix' in sys.argv
    problems, repaired = [], 0
    for folder in sorted(glob.glob(os.path.join(DOCS, '*', 'en'))):
        addin = os.path.dirname(folder)
        name = os.path.basename(addin)
        names = sorted(f for f in os.listdir(folder) if f.endswith('.md'))
        for language in LANGUAGES:
            there = os.path.join(addin, language)
            have = sorted(f for f in os.listdir(there) if f.endswith('.md')) if os.path.isdir(there) else []
            if have != names:
                problems.append('%s/%s: files differ from en (%s)' % (name, language, ', '.join(
                    sorted(set(names) ^ set(have))) or 'folder missing'))
                continue
            for entry in names:
                path = os.path.join(there, entry)
                if language != 'en' and shape(path) != shape(os.path.join(folder, entry)):
                    problems.append('%s/%s/%s: headings, table rows or code blocks differ from en %s -> %s' % (
                        name, language, entry, shape(os.path.join(folder, entry)), shape(path)))
                text = read(path)
                changed = text
                for target in LINK.findall(text):
                    if re.match(r'^(https?:|mailto:)', target):
                        continue
                    file_part, _, mark = target.partition('#')
                    goal = os.path.normpath(os.path.join(there, file_part)) if file_part else path
                    if not os.path.exists(goal):
                        problems.append('%s/%s/%s: link to a missing file: %s' % (name, language, entry, target))
                        continue
                    if not mark or not goal.endswith('.md'):
                        continue
                    marks = slugs(goal)
                    if mark in marks:
                        continue
                    # still the English heading? then the heading at the same place is meant
                    english = os.path.join(folder, os.path.basename(goal))
                    source = slugs(english) if os.path.dirname(goal) == there and os.path.isfile(english) else []
                    if mark in source and len(source) == len(marks):
                        new = '%s#%s' % (file_part, marks[source.index(mark)])
                        if fix:
                            changed = changed.replace('](%s)' % target, '](%s)' % new)
                            repaired += 1
                        else:
                            problems.append('%s/%s/%s: jump mark still English: %s (--fix makes it %s)' % (
                                name, language, entry, target, new))
                    else:
                        problems.append('%s/%s/%s: jump mark leads nowhere: %s' % (name, language, entry, target))
                if changed != text:
                    with io.open(path, 'w', encoding='utf-8', newline='\n') as handle:
                        handle.write(changed)
        index = os.path.join(addin, 'index.md')
        if not os.path.isfile(index):
            problems.append('%s: index.md with the languages is missing' % name)
    for line in problems:
        print('  ' + line)
    if repaired:
        print('%d jump marks repaired' % repaired)
    print('%d problem(s)' % len(problems) if problems else 'documentation complete in %s' % ', '.join(LANGUAGES))
    raise SystemExit(1 if problems else 0)


if __name__ == '__main__':
    main()
