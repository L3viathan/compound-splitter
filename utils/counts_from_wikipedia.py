import fileinput
import sys
import re  # I wish I could use regex instead
from html import unescape
from collections import Counter

def log(*a, **k):
    print(*a, **k, file=sys.stderr)


counts = Counter()
INSIDE=False
starters = {'}}',
        '{{',
        '|',
        '!',
        '<!--',
        '* ',
        '==',
        ':',
        '-->',
        '[[Kategorie:',
        }
# Sadly, this is the only way of doing this in the standard library
# When the regex will replace the re module, one can use \p{L}.
word = re.compile(r'[A-Za-zäöüÄÖÜßÅåÁáÉéÍíÓóŐőÚúŰű]+')
xmlement = re.compile(r'<[^>]*?>.*</[^>]*?>')  # HE'S COMING
xmleton = re.compile(r'<[^>/]*?/>')
extlink = re.compile(r'\[\S+ ([^\]]*?)\]')
wikilink = re.compile(r'\[\[(?:[^\]]*?\|)?([^|\]]*?)\]\]')
template = re.compile(r'{{[^}]+?}}')


def count(line):
    for w in word.findall(line):
        counts[w.lower()] += 1

def cprint(line):
    line = unescape(unescape(line).replace('<text xml:space="preserve">', ''))
    line = line.strip().replace("'''", '').replace("''", '')
    if any(line.startswith(s) for s in starters):
        return
    line = xmlement.sub('', extlink.sub(r'\1', wikilink.sub(r'\1', line)))
    line = xmleton.sub('', template.sub('', line))
    if line: count(line)

log(">>> Reading wikipedia corpus")
for line in fileinput.input():
    if INSIDE:
        if "</text>" in line:
            INSIDE = False
        cprint(line)
    else:
        if "<text" in line:
            INSIDE = True
            cprint(line)

log(">>> Sorting...")
mc = counts.most_common()
log(">>> Printing...")
for w, c in mc:
    print("{}\t{}".format(w, c))
log(">>> Done")
