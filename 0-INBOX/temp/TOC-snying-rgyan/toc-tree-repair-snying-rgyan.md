# TOC tree repair — snying-rgyan

Round restriction: titles only; no node added, removed, moved or renumbered.

Input: `toc-tree-snying-rgyan.md` (1606 nodes), QC report `toc-tree-qc-snying-rgyan.md` (34 issues, all "ordinal not attested for this title"). Authority: `0-INBOX/commentary/snying-rgyan.units.md`.

## Summary

- kept (checker false positive): 34
- title fixed: 0
- possible numbering error: 0

The tree file was not changed: no flagged title needed correcting.

Why the checker flagged them: each title is generic (དངོས་ཀྱི་དོན, སོ་སོའི་ངོ་བོ, རྒྱས་པར་བཤད་པ, མཐའ་དཔྱད་པ, དོན་བསྡུ་བ …) and recurs at other ordinals, or the attested string carries the PARENT's ordinal (e.g. "གཉིས་པ་ལ། X་དང་། Y" announces the second node's children X, Y), so the checker read the parent ordinal as the child's. In every case the text's enumeration lists the title at exactly the node's position, and the part opens with the matching ordinal.

Text lines: "enum" = the line where the parent announces its parts; "opens" = the line where this part begins.

## Flagged nodes

| tree line | decimal | title | verdict | text: enum | text: opens |
|---|---|---|---|---|---|
| L32 | 2.2.1.2.2.1 | དང་པོ་གོ་རིམས་ངེས་པ | kept | L255 | L257 |
| L89 | 2.2.2.1.1.2.4 | བཞི་པ་དོན་བསྡུ་བ | kept | L485 | no ordinal heading; position 4 of 4 in "གཉིས་པ་ལ་བཞི" at L485 |
| L110 | 2.2.2.2.2.1.2.1.3 | གསུམ་པ་རང་གི་ལུགས | kept | L781 | L825 |
| L133 | 2.2.2.2.2.2.1.1.1.3.2.2.1 | དང་པོ་སྒྲུབ་པའི་དམིགས་པ | kept | L959 | L961 |
| L137 | 2.2.2.2.2.2.1.1.3 | གསུམ་པ་གོ་རིམས་ངེས་པ | kept | L931 | L987 |
| L163 | 2.2.2.2.2.2.1.3.1.4 | བཞི་པ་གཞི་ཤེས་ཀྱི་སྦྱོར་བ | kept | L1031 | L1055 |
| L206 | 2.2.2.3.1.1.2.1.1.3 | གསུམ་པ་ངོ་བོ | kept | L1209 | L1221 |
| L210 | 2.2.2.3.1.1.2.1.1.4 | བཞི་པ་ཕན་ཡོན | kept | L1209 | L1255 |
| L404 | 2.2.2.3.1.1.2.3.1.1.3 | གསུམ་པ་རྩོད་པ་སྤང་བ | kept | L2509 | L2589 |
| L424 | 2.2.2.3.1.1.2.3.1.2.2.2.1.1 | དང་པོ་མཐའ་དཔྱད་པ | kept | L2717 | L2719 |
| L441 | 2.2.2.3.1.1.2.3.2.3.2 | གཉིས་པ་སོ་སོར་བཤད་པ | kept | L2851 | L2857 |
| L470 | 2.2.2.3.1.1.2.3.4.2.2.3.2.2.1 | དང་པོ་དངོས་ཀྱི་དོན | kept | L3073 | L3075 |
| L620 | 2.2.2.3.1.2.2.2.3.2 | གཉིས་པ་སོ་སོའི་ངོ་བོ | kept | L4070 | L4072 |
| L627 | 2.2.2.3.1.2.2.2.3.2.1.1.2.3 | གསུམ་པ་མཐའ་དཔྱད་པ | kept | L4084 | L4092 |
| L657 | 2.2.2.3.1.2.2.2.3.2.2.2.2.2 | གཉིས་པ་སོ་སོའི་ངོ་བོ | kept | L4274 | L4280 |
| L681 | 2.2.2.3.1.2.2.2.3.2.2.2.2.2.2.2 | གཉིས་པ་སོ་སོའི་ངོ་བོ | kept | L4364 | L4368 |
| L699 | 2.2.2.3.1.2.2.2.3.2.2.2.2.2.2.2.2.4 | བཞི་པ་ངོ་བོའི་ཁྱད་པར | kept | L4384 | L4430 |
| L820 | 2.2.2.3.2.1.1.2.1.1.1.2.1.3.2 | གཉིས་པ་ལམ་བདེན་གྱི་རྣམ་པ | kept | L4914 | L4928 |
| L833 | 2.2.2.3.2.1.1.2.1.1.1.2.2.3.2 | གཉིས་པ་སོ་སོར་བཤད | kept | L4970 | L4976 |
| L848 | 2.2.2.3.2.1.1.2.1.1.1.2.3.2 | གཉིས་པ་རྒྱས་པར་བཤད་པ | kept | L5014 | L5036 |
| L870 | 2.2.2.3.2.1.1.2.1.1.1.2.3.2.3.2 | གཉིས་པ་རྒྱས་པར་བཤད་པ | kept | L5162 | L5166 |
| L908 | 2.2.2.3.2.1.1.2.1.2.2.3.2 | གཉིས་པ་གྲངས་བསྡུ་བ | kept | L5324 | L5336 |
| L913 | 2.2.2.3.2.1.1.2.1.3.1.2.1 | དང་པོ་མཚན་གཞི | kept | L5392 | L5394 |
| L986 | 2.2.2.3.2.1.1.2.2.2.1 | དང་པོ་དངོས་ཀྱི་དོན | kept | L5744 | L5746 |
| L1026 | 2.2.2.3.2.1.1.2.2.3.1.2.2.2.2 | གཉིས་པ་རྒྱས་པར་བཤད་པ | kept | L5940 | L5948 |
| L1102 | 2.2.2.3.2.1.1.2.2.3.2.1.2.1 | དང་པོ་དངོས་ཀྱི་དོན | kept | L6160 | L6162 |
| L1118 | 2.2.2.3.2.1.1.2.2.3.2.1.2.2.4.2.1 | དང་པོ་རབ་འབྱོར་རང་ཉིད་ཀྱི་ལན་དོན་གྱིས་བཏབ་ཟིན་པ | kept | L6212 | L6214 |
| L1121 | 2.2.2.3.2.1.1.2.2.3.2.1.3.1 | དང་པོ་དངོས་ཀྱི་དོན | kept | L6222 | L6224 |
| L1325 | 2.2.2.3.2.1.2.2.3.2.2 | གཉིས་པ་སོ་སོའི་ངོ་བོ | kept | L6902 | L6906 |
| L1345 | 2.2.2.3.2.1.2.2.3.2.2.2.2.2 | གཉིས་པ་རྒྱས་པར་བཤད་པ | kept | L6986 | L6994 |
| L1422 | 2.2.2.3.3.2.1.2.2.1 | དང་པོ་དངོས་ཀྱི་དོན | kept | L7312 | L7314 |
| L1436 | 2.2.2.3.3.2.1.2.2.2.1 | དང་པོ་ཉོན་མོངས་མེད་པའི་ཏིང་ངེ་འཛིན | kept | L7478 | L7480 |
| L1497 | 2.2.2.3.3.2.2.1 | དང་པོ་དངོས་ཀྱི་དོན | kept | L7790 | L7792 |
| L1575 | 2.2.2.3.3.2.2.1.3.1.1.4.6.3.3.1 | དང་པོ་ཕྱིན་ཅི་ལོག་ཟད་པ | kept | L7978 | L7980 |

## Notes (not flagged, not changed)

- 2.2.2.2.2.2.1.1.1.3.2.2.3 སྒྲུབ་པའི་དབྱེ་བ has no leading ordinal; it is the third part announced at L959. Left alone (titles-only round, and the rules say not to invent an ordinal).
- 2.2.2.3.2.1.1.2.1.1.1.2.1.3.3 གསུམ་པ་དོན་བསྡུ་བ: the enumeration at L4914 words it གྲངས་ཀྱི་དོན་བསྡུ་བ. 2.2.2.3.2.1.1.2.1.1.1.2.2.3.3 གསུམ་པ་དོན་བསྡུ་བ: L4970 words it སྤྱིའི་དོན་བསྡུ་བ. Both are shortened, not wrong; left alone.
