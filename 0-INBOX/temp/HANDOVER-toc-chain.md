# Handover — TOC + block IDs onto the human-segmented sources (2026-10-13)

Goal: keep every human edit in `1-SOURCES/` (segmentation, letter fixes) and add the sa bcad
TOC headings and block IDs on top. Headings are built on our `0-INBOX/commentary/<id>.units.md`
copies, then carried onto the human file with antx; human paragraphs are never split.

## Done and pushed

| File | Result | Commit |
|---|---|---|
| grel-pa (`…འགྲེལ་པ།.md`) | verse tree 285 nodes + `## ཀླད་ཀྱི་དོན། ^I-0`, `## མཆོད་བརྗོད། ^II-0`; 875 blocks with IDs | c2bad0b, 3670ad9 |
| root text (`མངོན་རྟོགས་རྒྱན།.md`) | `# … ^0`, `^I`, 8 chapters `སྐབས་…` `^1–^8`, `## དོན་བསྡུས་གཞན། ^9-0`, `## མཇུག་བྱང། ^a-0` (`### མཛད་བྱང། ^a-1-0`, `### འགྱུར་བྱང། ^a-2-0`); 299 blocks | ade954d, 3670ad9 |

Both pass the strict gate (`verify_text.py`): letters and spacing identical to the human file.

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
| snying-rgyan | 01–04 / 7 | 888 | 05 was running (check for `tree_part_05.md`) |
| gser-phreng-smad | 01–03 / 5 | 632 | 04 was running |
| gser-phreng-stod | 01–03 / 6 | 654 | 04 was running |
| lung-gi-snye-ma | 01–03 / 11 | 722 | 04 was running |

To resume: if `tree_part_KK.md` exists but is not yet joined (tree-so-far's last line is
before it), run `chain_join.py` on it and write `pending_KK.md` from the part's end; then
launch the next segment with the same prompt shape (inputs: seg_KK.*, tree-so-far.md, the
latest pending file, the segment's text line range from `ranges.txt`; write ONLY
`tree_part_KK.md`). gser-phreng-smad's top node is `2.` (volume 2 continues volume 1's outline).

## After each tree is complete

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
