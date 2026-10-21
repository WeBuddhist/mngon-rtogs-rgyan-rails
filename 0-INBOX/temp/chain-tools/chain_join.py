"""Append tree_part_KK.md to tree-so-far.md after checking it continues the numbering.

usage: chain_join.py <seg-dir> <KK>

Checks every new line: `<3*(depth-1) spaces>* <decimal> <title>`; the decimal follows the
previous line (a first child N.1, the next sibling of the node or of one of its ancestors);
no repeated decimal; the title's leading Tibetan ordinal (if any) equals the last segment.
Prints the problems and exits 1 without appending when any check fails.
"""
import re
import sys
from pathlib import Path

ORD = {"དང་པོ": 1, "གཉིས་པ": 2, "གསུམ་པ": 3, "བཞི་པ": 4, "ལྔ་པ": 5, "དྲུག་པ": 6,
       "བདུན་པ": 7, "བརྒྱད་པ": 8, "དགུ་པ": 9, "བཅུ་པ": 10}
LINE = re.compile(r"^( *)\* ((?:\d+\.)*\d+)\.? (.+)$")

seg, k = Path(sys.argv[1]), int(sys.argv[2])
part = seg / f"tree_part_{k:02d}.md"
sofar = seg / "tree-so-far.md"
prev_lines = sofar.read_text(encoding="utf-8").splitlines() if k > 1 else []
new = [l for l in part.read_text(encoding="utf-8").splitlines()
       if l.strip() and not l.startswith("## ")]

def parse(l):
    m = LINE.match(l)
    if not m:
        return None
    return len(m.group(1)), [int(x) for x in m.group(2).split(".")], m.group(3)

seen = set()
last = None
for l in prev_lines:
    p = parse(l)
    if p:
        seen.add(tuple(p[1]))
        last = p[1]
errs = []
for i, l in enumerate(new, 1):
    p = parse(l)
    if not p:
        errs.append(f"L{i}: bad line format: {l[:80]}")
        continue
    ind, dec, title = p
    if ind != 3 * (len(dec) - 1):
        errs.append(f"L{i}: indent {ind} wrong for depth {len(dec)}: {l[:60]}")
    if tuple(dec) in seen:
        errs.append(f"L{i}: repeats {'.'.join(map(str, dec))}")
    ok = (last is None and len(dec) == 1) or (last is not None and (
        dec == last + [1] or
        any(dec == last[:j] + [last[j] + 1] for j in range(len(last)))))
    if not ok:
        errs.append(f"L{i}: {'.'.join(map(str, dec))} does not follow "
                    f"{'.'.join(map(str, last)) if last else '(start)'}")
    for w, n in ORD.items():
        if title.startswith(w) and n != dec[-1]:
            errs.append(f"L{i}: ordinal {w} ≠ decimal {'.'.join(map(str, dec))}")
            break
    seen.add(tuple(dec))
    last = dec

if errs:
    print(f"part {k:02d}: {len(errs)} problem(s), NOT appended")
    print("\n".join(errs[:40]))
    sys.exit(1)
with sofar.open("a" if k > 1 else "w", encoding="utf-8") as f:
    f.write("\n".join(new) + "\n")
print(f"part {k:02d}: {len(new)} nodes appended; tree-so-far now "
      f"{len(prev_lines) + len(new)} nodes; last {'.'.join(map(str, last))}")
