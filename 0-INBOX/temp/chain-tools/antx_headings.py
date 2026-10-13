"""Transfer TOC heading lines from a headed source onto a human-edited target with antx.

usage: antx_headings.py <headed-source.md> <human-target.md> <out.md> [--snap-log <file>]

antx locates each heading (`#…# title ^N-…-0`) of the source in the target. The target's
own characters (letters, line breaks, spacing) are never changed and its paragraphs are
never split: a heading that antx places inside a human paragraph is moved to the start
of that paragraph (logged). Checks: target text unchanged once headings are removed,
heading count and order identical to the source.
"""
import re
import sys

import antx.core
from antx import transfer
from diff_match_patch import diff_match_patch


class _PyDMP:
    """Pure-Python backend for antx (its bundled node binary is x86-only)."""

    def diff_main(self, text1, text2):
        dmp = diff_match_patch()
        dmp.Diff_Timeout = 0  # exact diff, no time cap
        return dmp.diff_main(text1, text2)


antx.core.optimized_diff_match_patch = _PyDMP

HEAD = r"#{2,6} [^\n]*?\^[0-9A-Za-z]+(?:-[0-9A-Za-z]+)*-0"
HEAD_LINE = re.compile(rf"^{HEAD}[ \t]*$", re.M)
strip = lambda s: re.sub(r"\s+", "", s)

args = sys.argv[1:]
log_path = None
if "--snap-log" in args:
    i = args.index("--snap-log")
    log_path = args[i + 1]
    del args[i:i + 2]
src_path, tgt_path, out_path = args
src = open(src_path, encoding="utf-8").read()
tgt = open(tgt_path, encoding="utf-8").read()
if HEAD_LINE.search(tgt):
    sys.exit("target already carries TOC headings — refusing")
src_heads = [h.strip() for h in HEAD_LINE.findall(src)]

res = transfer(src, [["heading", f"({HEAD})"]], tgt, output="txt")

# where antx put each heading, as an index into the target (the next non-space char)
pos = [i for i, c in enumerate(tgt) if not c.isspace()]
parts = re.split(f"({HEAD})", res)
marks = []  # (target index, heading)
n = 0
for i, p in enumerate(parts):
    if i % 2:
        marks.append((pos[n] if n < len(pos) else len(tgt), p.strip()))
    else:
        n += len(strip(p))
assert [h for _, h in marks] == src_heads, "antx lost or reordered headings"

# human paragraph starts: first non-space char of the file and after every blank line
starts = sorted({pos[0]} | {m.end() for m in re.finditer(r"\n[ \t]*\n\s*", tgt)})
starts = [s for s in starts if s < len(tgt)]
import bisect

snapped, log, last = [], [], 0
for b, h in marks:
    k = bisect.bisect_right(starts, b) - 1
    if b == len(tgt) or starts[k] == b:
        p = b
    else:
        # the lead-in before a mid-paragraph section start (typically the sentence
        # that introduces the quoted verse) goes with the new section
        p = a = starts[k]
        log.append(f"{h}\n  antx: …{tgt[max(a, b - 60):b]!r} ⟦here⟧ {tgt[b:b + 40]!r}…\n"
                   f"  moved to paragraph start")
    p = max(p, last)  # keep heading order
    snapped.append((p, h))
    last = p

out, cur = [], 0
for p, h in snapped:
    out.append(tgt[cur:p])
    if p == len(tgt) and not tgt.endswith("\n\n"):
        out.append("\n" if tgt.endswith("\n") else "\n\n")
    out.append(h + "\n\n")
    cur = p
out.append(tgt[cur:])
res = "".join(out)

assert HEAD_LINE.sub("", res).replace("\n\n", "") == tgt.replace("\n\n", "") or \
    strip(HEAD_LINE.sub("", res)) == strip(tgt), "target text changed"
assert [h.strip() for h in HEAD_LINE.findall(res)] == src_heads, "headings differ"

open(out_path, "w", encoding="utf-8").write(res)
if log_path:
    open(log_path, "w", encoding="utf-8").write("\n".join(log) + "\n")
print(f"transferred {len(snapped)} headings → {out_path}; "
      f"{len(log)} moved to a paragraph edge (human paragraphs never split)")
