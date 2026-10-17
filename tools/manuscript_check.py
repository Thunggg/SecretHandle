#!/usr/bin/env python3
"""Pre-submission / camera-ready checker for the SecretHandle papers.

Two independent checks:

1. Placeholder scan (always on): searches the LaTeX sources for TODO/FIXME/XXX/
   TKTK/TBD/PLACEHOLDER/``WIP``/``????`` markers and ``\\todo``/``\\fixme`` macros.
2. Build check (``--build``): runs XeLaTeX (+BibTeX when requested) on a document
   and parses the log for undefined references, undefined citations, overfull
   boxes, and hard errors.

Exit code is non-zero when any blocking problem is found (placeholder hit,
undefined reference/citation, or a hard error), so it can gate a release.

Usage:
  python tools/manuscript_check.py mobisys/main.tex --build --bibtex
  python tools/manuscript_check.py --scan-only mobisys/sections sections
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

PLACEHOLDER_PATTERNS = [
    (r"\bTODO\b", "TODO"),
    (r"\bFIXME\b", "FIXME"),
    (r"\bXXX\b", "XXX"),
    (r"\bTKTK\b", "TKTK"),
    (r"\bTBD\b", "TBD"),
    (r"\bPLACEHOLDER\b", "PLACEHOLDER"),
    (r"\bLorem ipsum\b", "Lorem ipsum"),
    (r"\bWIP\b", "WIP"),
    (r"\?\?\?\?", "????"),
    (r"\\todo\b", "\\todo"),
    (r"\\fixme\b", "\\fixme"),
]

REF_RE = re.compile(r"LaTeX Warning: Reference `([^']+)'")
CITE_RE = re.compile(r"LaTeX Warning: Citation `([^']+)'")
OVERFULL_RE = re.compile(r"Overfull \\hbox \(([\d.]+)pt")
UNDERFULL_RE = re.compile(r"Underfull \\hbox")
ERROR_RE = re.compile(r"^! .*$", re.MULTILINE)


def tex_files(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            out.extend(sorted(p.rglob("*.tex")))
        elif p.suffix == ".tex":
            out.append(p)
    # de-duplicate while preserving order
    seen: set[str] = set()
    uniq: list[Path] = []
    for f in out:
        key = str(f.resolve())
        if key not in seen:
            seen.add(key)
            uniq.append(f)
    return uniq


def scan_placeholders(paths: list[str]) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    compiled = [(re.compile(pat), label) for pat, label in PLACEHOLDER_PATTERNS]
    for f in tex_files(paths):
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for cre, label in compiled:
                if cre.search(line):
                    commented = line.lstrip().startswith("%")
                    # Skip false positives for conceptual API tokens like type(PLACEHOLDER)
                    line_lower = line.lower()
                    if label == "PLACEHOLDER" and "type(placeholder)" in line_lower:
                        continue
                    if label == "PLACEHOLDER" and "\\texttt" in line and "placeholder" in line_lower:
                        continue
                    hits.append(
                        {
                            "file": str(f),
                            "line": i,
                            "marker": label,
                            "commented": commented,
                            "text": line.strip()[:160],
                        }
                    )
                    break
    return hits


def run(cmd: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def build(tex: Path, bibtex: bool, passes: int, engine: str, timeout: int) -> tuple[Path, list[str]]:
    notes: list[str] = []
    log = tex.with_suffix(".log")
    for n in range(passes):
        try:
            proc = run([engine, "-interaction=nonstopmode", "-file-line-error", tex.name], tex.parent, timeout)
        except subprocess.TimeoutExpired:
            notes.append(f"{engine} timed out after {timeout}s on pass {n + 1}")
            break
        if proc.returncode != 0 and n == passes - 1:
            notes.append(f"{engine} returned exit code {proc.returncode} on pass {n + 1}")
        if bibtex and n == 0:
            try:
                bproc = run([bibtex, str(tex.stem)], tex.parent, timeout)
            except subprocess.TimeoutExpired:
                notes.append(f"bibtex timed out after {timeout}s")
                continue
            if bproc.returncode != 0:
                notes.append(f"bibtex returned exit code {bproc.returncode}")
    return log, notes


def parse_log(log: Path) -> dict[str, object]:
    text = log.read_text(encoding="utf-8", errors="replace") if log.exists() else ""
    overfull = [float(x) for x in OVERFULL_RE.findall(text)]
    return {
        "log": str(log),
        "undefined_refs": sorted(set(REF_RE.findall(text))),
        "undefined_cites": sorted(set(CITE_RE.findall(text))),
        "overfull_count": len(overfull),
        "overfull_max_pt": round(max(overfull), 3) if overfull else 0.0,
        "underfull_hbox": len(UNDERFULL_RE.findall(text)),
        "rerun_needed": "Rerun to get" in text,
        "errors": ERROR_RE.findall(text)[:20],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("targets", nargs="+", help=".tex files or directories to scan")
    parser.add_argument("--build", action="store_true", help="compile the .tex targets and parse the log")
    parser.add_argument("--scan-only", action="store_true", help="only run the placeholder scan")
    parser.add_argument("--bibtex", action="store_true", help="run bibtex between XeLaTeX passes")
    parser.add_argument("--engine", default="xelatex")
    parser.add_argument("--passes", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--json", dest="json_out", help="write a JSON summary to this path")
    parser.add_argument("--allow-commented", action="store_true", help="do not fail on markers in % comments")
    args = parser.parse_args(argv)

    summary: dict[str, object] = {"targets": args.targets}
    blocking = False

    hits = scan_placeholders(args.targets)
    summary["placeholder_hits"] = hits
    blocking_markers = [h for h in hits if not (args.allow_commented and h["commented"])]
    if blocking_markers:
        blocking = True
        print(f"[placeholders] {len(blocking_markers)} marker(s) found:")
        for h in blocking_markers:
            tag = "comment" if h["commented"] else "text"
            print(f"  {h['file']}:{h['line']} [{h['marker']}/{tag}] {h['text']}")
    else:
        print("[placeholders] none found")

    if args.build and not args.scan_only:
        build_reports = []
        for t in args.targets:
            tex = Path(t)
            if tex.suffix != ".tex":
                continue
            log, notes = build(tex, args.bibtex, args.passes, args.engine, args.timeout)
            report = parse_log(log)
            report["notes"] = notes
            build_reports.append(report)
            bad = report["undefined_refs"] or report["undefined_cites"] or report["errors"]
            if bad:
                blocking = True
            print(f"[build] {tex}: refs_undef={len(report['undefined_refs'])} "
                  f"cites_undef={len(report['undefined_cites'])} "
                  f"overfull={report['overfull_count']} (max {report['overfull_max_pt']}pt) "
                  f"errors={len(report['errors'])}")
            for note in notes:
                print(f"  note: {note}")
        summary["builds"] = build_reports

    summary["blocking"] = blocking
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[result] {'FAIL' if blocking else 'PASS'}")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
