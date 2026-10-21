# Pass 5 in segments — anchoring contract

The tree is anchored segment by segment. Follow
`4-SYSTEM/Skills/seg-toc-lib/prompts/pass5-anchors.md` for where a node begins and how to copy
the context, with these changes:

1. **Input.** The nodes of your segment: `TOC-<id>/seg/tree_part_KK.md` (decimal + title per
   line — for gser-phreng-smad use the decimals exactly as written in that file), and your
   stretch of `0-INBOX/commentary/<id>.units.md` (line range given in your instructions; it
   already includes 25 lines of overlap on each side — a node may begin slightly before your
   range starts if the previous segment ended mid-section, so read 60 lines earlier too).
   You may read `TOC-<id>/seg/tree-so-far.md` (read-only) for the parents of your nodes.

2. **Output** — write ONLY `TOC-<id>/seg/anchors_KK.tsv`, one line per node of your part, in
   the part's order, tab-separated:

       <decimal>	<source line number where the node begins>	<context>

   `<context>` = the first 12–20 syllables at the node's beginning, copied character for
   character from the units file (no `[[ ]]`). The line number is that of the line holding
   the context's first character. Every node gets a line; a node that truly cannot be found
   gets `?` as line and context.

3. **Order.** Line numbers must not go down through the part, except for a sibling group the
   commentary treats in a different order from the announcement (pass5-anchors.md exception)
   — note any such group in your reply.

4. **Frame nodes** — only the agent of segment 01 adds front-matter frame lines, and only the
   agent of the last segment adds back-matter ones, with the decimals `I.`, `II.`, `a.`,
   `b.`, `b.1`, `b.2` and the titles from pass5-anchors.md, as extra TSV lines in a second
   file `TOC-<id>/seg/frame_KK.tsv`: `<frame id>	<title>	<line>	<context>`.

5. Check every context occurs in the units file (whitespace ignored) before you finish.
   Reply with the path(s), the count of nodes anchored / `?`, and any out-of-order groups.
