"""Check every ingested heading sits in the block that holds its anchor line.

usage: check_placement.py <units.md> <headed.md> <toc-tree-anchored.md> <anchors-dir> [--remap smad]
Maps each heading of <headed.md> back to the units-file line where its block begins and
compares with the anchor line from seg/anchors_*.tsv. Prints the misplaced ones.
"""
import glob, re, sys
units, headed, tree, adir = sys.argv[1:5]
REMAP = {"2": "2.2.2.1.2.2.2", "3": "2.2.2.1.2.2.3", "4": "2.2.2.2", "5": "2.2.2.3",
         "6": "2.2.3", "7": "3"} if "--remap" in sys.argv else None
rm = lambda d: d if not REMAP else REMAP[d.split(".")[0]] + ("." + ".".join(d.split(".")[1:]) if "." in d else "")
SKIP = re.compile(r"[\s།༎]")
U = open(units, encoding="utf-8").read().split("\n")
# canonical offset at the start of each units line
starts, n = [], 0
for l in U:
    starts.append(n); n += len(SKIP.sub("", l))
import bisect
anch = {}
for f in glob.glob(f"{adir}/anchors_*.tsv"):
    for l in open(f, encoding="utf-8"):
        p = l.rstrip("\n").split("\t")
        if len(p) >= 2 and p[1].isdigit():
            anch[rm(p[0].strip().rstrip("."))] = int(p[1])
H = open(headed, encoding="utf-8").read().split("\n")
HEAD = re.compile(r"^#{2,6} .*\^([0-9A-Za-z-]+)-0\s*$")
canon_before, bad, total = 0, [], 0
pending = []
for l in H:
    m = HEAD.match(l)
    if m:
        pending.append(m.group(1).replace("-", "."))
        continue
    if pending and l.strip():
        li = bisect.bisect_right(starts, canon_before) - 1  # units line where this block's text begins
        # block end: next blank line in units
        end = li
        while end + 1 < len(U) and U[end + 1].strip():
            end += 1
        for dec in pending:
            total += 1
            a = anch.get(dec)
            if a is not None and not (li + 1 <= a <= end + 1):
                bad.append((dec, a, li + 1))
        pending = []
    canon_before += len(SKIP.sub("", l))
print(f"{total} headings checked; {len(bad)} not in the block of their anchor line")
for b in bad[:25]:
    print("  ", b)
