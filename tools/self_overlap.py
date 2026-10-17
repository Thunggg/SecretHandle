#!/usr/bin/env python3
"""Self-overlap (text-reuse) checker for the SecretHandle manuscripts.

Estimates reused prose between document groups (the Emerging Ideas short paper,
the full paper, and the idea note) using word-level maximal matching blocks.
This supports a self-plagiarism / redundancy review before submission: it does
not compare against external corpora (that needs a plagiarism service), but it
does surface long verbatim spans shared across our own documents.

Usage:
  python tools/self_overlap.py --root .
  python tools/self_overlap.py --root . --ngram 12 --top 15 --report self_overlap_report.md
"""
from __future__ import annotations

import argparse
import json
import re
from difflib import SequenceMatcher
from pathlib import Path

# LaTeX tokens stripped before word extraction. Order matters.
_STRIP = [
    (re.compile(r"(?<!\\)%.*"), " "),            # comments (not \%)
    (re.compile(r"\\(begin|end)\{[^}]*\}"), " "),  # environments
    (re.compile(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?"), " "),  # commands + optional arg
    (re.compile(r"\$[^$]*\$"), " "),             # inline math
    (re.compile(r"[{}~^_&]"), " "),              # structural chars
]
_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")

# Words that carry little reuse meaning; kept minimal on purpose.
_STOP = {
    "the", "a", "an", "of", "and", "or", "to", "in", "on", "for", "with", "is",
    "are", "be", "as", "by", "that", "this", "it", "we", "our", "not", "but",
}


def load_words(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    for pat, repl in _STRIP:
        text = pat.sub(repl, text)
    return [w.lower() for w in _WORD.findall(text)]


def group_words(files: list[Path]) -> list[str]:
    """Concatenate file words with a unique boundary token so matches cannot
    cross file boundaries."""
    words: list[str] = []
    for idx, f in enumerate(files):
        words.append(f"\x00b{idx}\x00")
        words.extend(load_words(f))
    return words


def ngrams_ratio(a: list[str], b: list[str], n: int) -> float:
    if len(a) < n or len(b) < n:
        return 0.0
    set_a = {tuple(a[i : i + n]) for i in range(len(a) - n + 1)}
    set_b = {tuple(b[i : i + n]) for i in range(len(b) - n + 1)}
    if not set_a or not set_b:
        return 0.0
    inter = len(set_a & set_b)
    return inter / min(len(set_a), len(set_b))


def matching_spans(a: list[str], b: list[str], n: int, top: int) -> list[dict[str, object]]:
    sm = SequenceMatcher(a=a, b=b, autojunk=False)
    spans = []
    for block in sm.get_matching_blocks():
        if block.size < n:
            continue
        seg = a[block.a : block.a + block.size]
        if any(w.startswith("\x00b") for w in seg):
            continue
        spans.append(
            {
                "words": block.size,
                "a_start": block.a,
                "b_start": block.b,
                "text": " ".join(seg[:60]) + (" ..." if block.size > 60 else ""),
            }
        )
    spans.sort(key=lambda s: s["words"], reverse=True)
    return spans[:top]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--ngram", type=int, default=12, help="minimum verbatim span length in words")
    parser.add_argument("--top", type=int, default=15, help="top spans to report per pair")
    parser.add_argument("--report", help="write a markdown report to this path")
    parser.add_argument("--json", dest="json_out", help="write a JSON summary to this path")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    groups = {
        "short (mobisys)": sorted((root / "mobisys").rglob("*.tex")),
        "full (sections)": sorted((root / "sections").rglob("*.tex")) + sorted((root / "appendix").rglob("*.tex")),
        "idea note": [root / "idea.tex"] if (root / "idea.tex").exists() else [],
    }
    words = {name: group_words(files) for name, files in groups.items() if files}

    names = list(words)
    result: dict[str, object] = {"ngram": args.ngram, "groups": {k: len(v) for k, v in words.items()}, "pairs": []}
    lines = ["# Self-overlap report", "", f"Minimum verbatim span: **{args.ngram} words**.", ""]
    lines.append("Word counts: " + ", ".join(f"{k}={len(v)}" for k, v in words.items()) + ".")
    lines.append("")

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a_name, b_name = names[i], names[j]
            a, b = words[a_name], words[b_name]
            ratio = ngrams_ratio(a, b, args.ngram)
            spans = matching_spans(a, b, args.ngram, args.top)
            result["pairs"].append({"a": a_name, "b": b_name, "ngram_ratio": round(ratio, 4), "spans": spans})
            lines.append(f"## {a_name}  vs  {b_name}")
            lines.append("")
            lines.append(f"- {args.ngram}-gram share (of the smaller doc): **{ratio:.1%}**")
            lines.append(f"- verbatim spans >= {args.ngram} words: **{len(spans)}** (showing top {args.top})")
            lines.append("")
            if spans:
                lines.append("| words | span |")
                lines.append("|---:|---|")
                for s in spans:
                    text = str(s["text"]).replace("|", "\\|")
                    lines.append(f"| {s['words']} | {text} |")
                lines.append("")

    lines.append("> Method: LaTeX commands/math/comments stripped, words lower-cased, maximal")
    lines.append("> matching blocks via `difflib.SequenceMatcher`, file boundaries marked so spans")
    lines.append("> cannot cross files. This is an internal reuse check, not an external plagiarism scan.")

    report = "\n".join(lines) + "\n"
    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
