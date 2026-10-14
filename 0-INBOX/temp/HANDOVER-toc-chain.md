# Handover — TOC + block IDs onto the human-segmented sources (2026-10-13)

Goal: keep every human edit in `1-SOURCES/` (segmentation, letter fixes) and add the sa bcad
TOC headings and block IDs on top. Headings are built on our `0-INBOX/commentary/<id>.units.md`
copies, then carried onto the human file with antx; human paragraphs are never split.

## Done and pushed

| File | Result | Commit |
|---|---|---|
| grel-pa | verse tree 285 nodes + `^I`/`^II` frames; 875 blocks; headings snapped to paragraph starts (9) | c2bad0b, 3670ad9 |
| root text | 8 chapters + `^9` summary + frames; 299 blocks | ade954d, 3670ad9 |
| gser-phreng-smad | 1082 nodes + frames; 2801 blocks; 916 human paragraphs split at section starts | 6ecb0bd |
| snying-rgyan | 1606 nodes + frames; 4071 blocks; 1088 paragraphs split | e5a8c58 |
| gser-phreng-stod | 1344 nodes + frames; 3808 blocks; 1140 paragraphs split | 5d02228 |

All pass the strict gate (`verify_text.py`) against the human file. For the big commentaries a
heading that starts inside a human paragraph splits it there (`antx_headings.py --split`);
every human break and letter is kept.

## In progress — sa bcad trees (Claude agents, Gemini dropped on request)

The four big commentaries are too long for one pass-3 call. Their candidates/enumerations
(Claude path, `TOC-<id>/candidates|enumerations/`) are cut into segments
(`TOC-<id>/seg/seg_KK.*`, line ranges in `seg/ranges.txt`) and the tree is built as a chain:
one isolated agent per segment, following `0-INBOX/temp/chain-pass3.md` +
`4-SYSTEM/Skills/seg-toc-lib/prompts/pass3-tree.md`, continuing `seg/tree-so-far.md`.
Each finished `tree_part_KK.md` is checked and appended with
`python3 0-INBOX/temp/chain-tools/chain_join.py 0-INBOX/temp/TOC-<id>/seg KK`
(continuity of decimals, indents, ordinals). The agent's reply (open path, pending parts,
decisions) is saved as `seg/pending_KK.md` and handed to the next segment.

State at handover (joined parts / total segments):

| id | joined | nodes | next |
|---|---|---|---|
| lung-gi-snye-ma | tree 01–10 / 11 joined; anchors 01–10 done | 2568 | **tree segment 11 (last, lines 19001–20479)** — its agent hit the usage limit and wrote nothing; relaunch it with `pending_10.md` (it must open every remaining announced part and report where the body ends and the closing matter). Then anchors_11 + back-matter `frame_11.tsv`, then the post-tree steps below. |

Fixes already applied to lung-gi-snye-ma's tree (from segment agents' reports, checked against the text):
`…3.1.2.1.1.4 བཞི་པ་ཐེག་ཆེན` / `.5 ལྔ་པ་ལམ` (six parts at 10471); `1.2.2.2.3.2.1 དང་པོ་རྒྱས་པ་ལ་དད་པ`
(division clause removed); anchors_08: `…1.2.3.2.1.5.4` stacked on `.5.3` (both treated at 14991).
Front-matter frame (anchors 01): `I. མཆོད་བརྗོད།` at 3, `II. ཤེར་ཕྱིན་དང་དེའི་དགོངས་པ་འགྲེལ་བའི་བསྟན་བཅོས།` at 91
(title built from line 93 — review). Title line 1 → `# … ^0`.

If a usage limit stops an agent: a part file it already wrote is complete only if it reaches the
end of its line range (check the last nodes against the text); otherwise delete it and rerun.

To resume: if `tree_part_KK.md` exists but is not yet joined (tree-so-far's last line is
before it), run `chain_join.py` on it and write `pending_KK.md` from the part's end; then
launch the next segment with the same prompt shape (inputs: seg_KK.*, tree-so-far.md, the
latest pending file, the segment's text line range from `ranges.txt`; write ONLY
`tree_part_KK.md`). gser-phreng-smad's top node is `2.` (volume 2 continues volume 1's outline).

## After each tree is complete (as done for smad / snying / stod)

Per segment: an anchoring agent (contract `0-INBOX/temp/chain-pass5.md`) writes
`seg/anchors_KK.tsv` (+ `frame_KK.tsv` for the first/last). Then:
`chain-tools/merge_anchors.py <TOC-dir> <id> <units>` (checks + disambiguates short contexts),
`toc_tree_ingest.py parse` / `ingest --split-frame-nodes` into a units copy,
`chain-tools/check_placement.py` (every heading in its anchor's block),
`chain-tools/antx_headings.py --split`, `ingest --stamp-body-ids --verify-against <human file>`,
title line → `# … ^0` (verify against a copy with `# ` prefixed), `chain-tools/idcheck.py`.

## Older notes on the steps

1. Add `## དཀར་ཆག / Table of Contents` header to tree-so-far → `toc-tree-<id>.md`; run
   `4-SYSTEM/Skills/seg-toc-lib/qc_check_tree.py` (corpus: merged candidates, enumerations,
   units file); repair with an isolated `pass4-qc-repair.md` agent per flagged stretch.
2. Pass 5 anchors (`pass5-anchors.md`) per segment, each agent reading only its line range of
   the units file; add frame nodes (front matter `I.`/`II.`, colophon `a.`) — see grel-pa and
   the root text for the labels used. Pass 6: `qc_tree_vs_source.py`.
3. `toc_tree_ingest.py parse` + `ingest --split-frame-nodes` into a copy of the units file
   (`0-INBOX/transfer/<id>.headed-units.md`).
4. `chain-tools/antx_headings.py <headed-units> <human 1-SOURCES file> <out> --snap-log …`
   (needs a venv with `antx`, `diff-match-patch`, `pyyaml`, `requests`; antx's bundled dmp
   binary is x86-only, the script swaps in Python diff-match-patch).
5. `toc_tree_ingest.py ingest --stamp-body-ids --verify-against <human file as pulled>`;
   `chain-tools/idcheck.py` (no block without ID, no duplicates).
6. Copy over the `1-SOURCES/` file, commit, push.

## Notes

- The Gemini runs were stopped; their partial candidates are kept as
  `TOC-<id>/candidates-gemini-partial/` (not used). Gemini key: `GEMINI_API_KEY` in `~/.zshrc`.
- `.env` is now git-ignored.
- Decisions recorded per segment in `seg/pending_KK.md` (content lists vs nodes, titles of
  bare-ordinal headers, excursus nodes, places where the text's ordinal departs from the
  announced order).
