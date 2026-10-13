"""Fill the pass-1 candidate chunk files in parallel with extract_toc_tree's own functions.

usage: prefill_pass1.py <vault> <units.md> <commentary-id> <workers>

Same chunking (DEFAULT_CHUNK_SIZE / DEFAULT_OVERLAP) and the same file format as the main
script, so its later run skips every chunk written here. Files are written atomically.
"""
import importlib.util
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

vault, src, cid, workers = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
spec = importlib.util.spec_from_file_location(
    "ett", vault / "4-SYSTEM/Skills/seg-toc-lib/toc_tree_extractor/extract_toc_tree.py")
ett = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ett)

lines = src.read_text(encoding="utf-8").splitlines(keepends=True)
chunks = ett.make_chunks(lines, ett.DEFAULT_CHUNK_SIZE, ett.DEFAULT_OVERLAP)
cdir = vault / "0-INBOX/temp" / f"TOC-{cid}" / "candidates"
cdir.mkdir(parents=True, exist_ok=True)
client = ett.get_client()


def job(idx, start, end, numbered):
    out = cdir / f"chunk_{idx:03d}.md"
    if out.exists():
        return "skip"
    r = ett.extract_from_chunk(client, ett.DEFAULT_MODEL, numbered,
                               fallback_model=ett.DEFAULT_FALLBACK_MODEL)
    head = f"<!-- chunk {idx:03d} | lines {start}–{end} | source: {cid} -->\n\n"
    body = "<!-- no candidates -->\n" if (not r or r.strip().upper() == "NO CANDIDATES") \
        else r.rstrip() + "\n"
    tmp = out.with_suffix(".tmp")
    tmp.write_text(head + body, encoding="utf-8")
    tmp.rename(out)
    return "ok"


todo = [c for c in chunks if not (cdir / f"chunk_{c[0]:03d}.md").exists()]
print(f"{cid}: {len(chunks)} chunks, {len(todo)} to do, {workers} workers", flush=True)
ok = fail = 0
with ThreadPoolExecutor(workers) as ex:
    futs = {ex.submit(job, i, s, e, num): i for i, s, e, _t, num in todo}
    for f in as_completed(futs):
        try:
            f.result()
            ok += 1
        except Exception as e:  # leave the chunk missing; the main script retries it
            fail += 1
            print(f"FAIL chunk_{futs[f]:03d}: {type(e).__name__}: {str(e)[:150]}", flush=True)
        if (ok + fail) % 10 == 0:
            print(f"progress {ok + fail}/{len(todo)} (fail {fail})", flush=True)
print(f"prefill done: ok={ok} fail={fail}", flush=True)
