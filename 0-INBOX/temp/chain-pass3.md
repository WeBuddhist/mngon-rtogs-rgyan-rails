# Pass 3 in segments — continuation contract

The commentary is too long for one pass-3 call, so its candidates and enumerations are cut
into consecutive segments (`TOC-<id>/seg/seg_KK.candidates.md` + `seg_KK.enumerations.md`,
in document order, chunk headers kept). One isolated agent builds the tree for one segment,
continuing the tree built so far. Follow `4-SYSTEM/Skills/seg-toc-lib/prompts/pass3-tree.md`
for everything (hierarchy, matching, ordinals, title cleaning, line format), with these
changes:

1. **Input.** Your segment's candidates and enumerations only. For segment 01 nothing else.
   For segment KK > 01, also `TOC-<id>/seg/tree-so-far.md` — the tree from all earlier
   segments. Read its LAST 150 lines and EVERY line whose indent is ≤ 12 spaces (depth ≤ 5),
   e.g. `grep -nE '^( {0,12})\* ' tree-so-far.md`, so you know the open path (the current
   node and all its ancestors) and which announced siblings have not been opened yet.

2. **Output = continuation only.** Write only the new tree lines (no `## དཀར་ཆག` header, no
   blank lines) to `TOC-<id>/seg/tree_part_KK.md`. The first line you write is the first
   NEW node after the last line of `tree-so-far.md`. Never repeat a node already in
   `tree-so-far.md`; chunks overlap by 25 lines, so candidates at the start of your segment
   may already be in the tree — skip them.

3. **Numbering continues.** Every line carries its full decimal path, consistent with
   `tree-so-far.md` (a new child of open node 2.3.1 after its last child 2.3.1.4 is
   2.3.1.5; returning to a higher level continues that level's counter). Indent = 3 spaces ×
   (depth − 1), exactly as in pass3-tree.md. The Tibetan ordinal of a title must equal the
   last decimal segment.

4. **Gap filling is local.** Insert a missing announced part only when a LATER sibling of
   it opens inside your segment (so the earlier one must exist before it). Parts announced
   but not yet reached by the end of your segment stay pending — a later segment opens them.
   Do not close or pad a division at the end of your segment.

5. **The text may settle placement.** The candidates are slimmed (no CONTEXT), so many are
   bare ordinals. You may read — read-only — the lines of
   `0-INBOX/commentary/<id>.units.md` that your segment covers (the line range is given in
   your instructions) to decide where a node sits and what it is called. The text is the
   final authority. Write nothing there.

6. Output Tibetan only, the tree lines only. Reply only with the path you wrote.
