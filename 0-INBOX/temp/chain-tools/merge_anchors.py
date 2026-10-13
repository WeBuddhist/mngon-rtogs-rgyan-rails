"""Merge per-segment anchors (seg/anchors_KK.tsv, seg/frame_KK.tsv) into the anchored tree.

usage: merge_anchors.py <TOC-dir> <id> <units.md> [--remap smad]

Reads the (repaired) tree <TOC-dir>/toc-tree-<id>.md for titles, the anchors by decimal,
and writes <TOC-dir>/toc-tree-anchored-<id>.md: front frame lines, every tree node as
`* <dec> <title> [[<context>]]`, back frame lines. Checks: every node anchored, every
context found in the units file (whitespace ignored), anchor line numbers in tree order
(violations listed — they are either sibling groups treated out of order or errors).
--remap smad maps gser-phreng-smad's local part decimals (2.–7.) to volume-1 paths.
"""
import glob
import re
import sys
from pathlib import Path

d, cid, units = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
REMAP = {"2": "2.2.2.1.2.2.2", "3": "2.2.2.1.2.2.3", "4": "2.2.2.2", "5": "2.2.2.3",
         "6": "2.2.3", "7": "3"} if "--remap" in sys.argv else None

def remap(dec):
    if not REMAP:
        return dec
    p = dec.split(".")
    return REMAP[p[0]] + ("." + ".".join(p[1:]) if len(p) > 1 else "")

LINE = re.compile(r"^( *)\* ((?:\d+\.)*\d+)\.? (.+?)\s*$")
nodes = []
for l in (d / f"toc-tree-{cid}.md").read_text(encoding="utf-8").splitlines():
    m = LINE.match(l)
    if m:
        nodes.append((m.group(2), m.group(3)))

anch = {}
for f in sorted(glob.glob(str(d / "seg" / "anchors_*.tsv"))):
    for l in Path(f).read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        dec, ln, ctx = (l.split("\t") + ["", ""])[:3]
        anch[remap(dec.strip().rstrip("."))] = (ln.strip(), ctx.strip())

front, back = [], []
for f in sorted(glob.glob(str(d / "seg" / "frame_*.tsv"))):
    for l in Path(f).read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        fid, title, ln, ctx = (l.split("\t") + ["", "", ""])[:4]
        fid = fid.strip().rstrip(".")
        (front if re.match(r"^[IVX]+$", fid) else back).append((fid, title.strip(), ln.strip(), ctx.strip()))

ulines = units.read_text(encoding="utf-8").split("\n")
SKIP = re.compile(r"[\s།༎]")
canon = lambda s: SKIP.sub("", s)
# canonical text (whitespace and shads removed, as toc_tree_ingest matches) with, for every
# canonical character, its (line index, column) in the units file
C, where = [], []
for li, l in enumerate(ulines):
    for col, ch in enumerate(l):
        if not SKIP.match(ch):
            C.append(ch)
            where.append((li, col))
C = "".join(C)
line_start = {}
for ci, (li, _) in enumerate(where):
    line_start.setdefault(li, ci)
text = C


def grow(ci, need):
    """Original text from canonical index ci until `need` canonical chars are covered."""
    li, col = where[ci]
    out, got = [], 0
    while li < len(ulines) and got < need:
        seg = ulines[li][col:]
        out.append(seg)
        got += len(canon(seg))
        li, col = li + 1, 0
    return " ".join(x.strip() for x in out if x.strip())


def disambiguate(seq):
    """seq: list of [dec, line, ctx] in tree order. Lengthen contexts whose first match after
    the previous node is not on the stated line. Returns the number changed and failures."""
    cur, changed, failed = 0, 0, []
    for item in seq:
        dec, ln, ctx = item
        if not ln.isdigit() or ctx in ("", "?"):
            continue
        li = int(ln) - 1
        c = canon(ctx)
        idx = C.find(c, cur)
        if idx >= 0 and where[idx][0] == li:
            cur = idx
            continue
        s0 = line_start.get(li)
        s1 = line_start.get(li + 1, len(C))
        j = C.find(c, s0, s1 + len(c)) if s0 is not None else -1
        if j < 0 or where[j][0] != li:
            failed.append(dec)
            continue
        need = len(c)
        while need < 400:
            need += 15
            new = grow(j, need)
            if C.find(canon(new), cur) == j:
                item[2] = new
                changed += 1
                break
        else:
            failed.append(dec)
            continue
        cur = j
    return changed, failed
seq = [[dec, *anch[dec]] for dec, _ in nodes if dec in anch]
n_changed, n_failed = disambiguate(seq)
for dec, ln, ctx in seq:
    anch[dec] = (ln, ctx)
missing = [dec for dec, _ in nodes if dec not in anch or anch[dec][1] in ("", "?")]
notfound = [dec for dec, _ in nodes if dec in anch and anch[dec][1] not in ("", "?")
            and canon(anch[dec][1]) not in text]
extra = sorted(set(anch) - {dec for dec, _ in nodes})
order, last = [], 0
for dec, _ in nodes:
    ln = anch.get(dec, ("", ""))[0]
    if ln.isdigit():
        if int(ln) < last:
            order.append(f"{dec} at {ln} < {last}")
        last = max(last, int(ln))

out = ["## དཀར་ཆག / Table of Contents", ""]
for fid, title, ln, ctx in front:
    out.append(f"* {fid}. {title} [[{ctx}]]")
for dec, title in nodes:
    depth = dec.count(".") + 1
    ctx = anch.get(dec, ("", "?"))[1] or "?"
    out.append(" " * 3 * (depth - 1) + f"* {dec}{'.' if depth == 1 else ''} {title} [[{ctx}]]")
for fid, title, ln, ctx in back:
    depth = fid.count(".") + 1
    out.append(" " * 3 * (depth - 1) + f"* {fid}{'.' if depth == 1 else ''} {title} [[{ctx}]]")
(d / f"toc-tree-anchored-{cid}.md").write_text("\n".join(out) + "\n", encoding="utf-8")

print(f"{cid}: {len(nodes)} nodes, {len(front)} front + {len(back)} back frame lines")
print(f"  unanchored: {len(missing)} {missing[:10]}")
print(f"  context not in text: {len(notfound)} {notfound[:10]}")
print(f"  anchors for unknown decimals: {len(extra)} {extra[:10]}")
print(f"  contexts lengthened to be unambiguous: {n_changed}; could not place on stated line: {len(n_failed)} {n_failed[:10]}")
print(f"  out of order: {len(order)}")
for o in order[:30]:
    print("   ", o)
