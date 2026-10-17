# Manuscript tooling

## tools/manuscript_check.py
- Scans LaTeX sources for placeholder markers (TODO/FIXME/TBD/PLACEHOLDER/????/\\todo)
- Optionally builds (XeLaTeX + BibTeX) and parses logs for undefined refs/cites, overfull boxes, errors
- Use `--allow-commented` to ignore TODOs in `%` comments when auditing; final pre-submission should have zero markers in body

```bash
python tools/manuscript_check.py --scan-only mobisys
python tools/manuscript_check.py mobisys/main.tex --build --bibtex --passes 3
```

## tools/self_overlap.py
- Internal text-reuse checker between short paper (mobisys), full paper (sections/appendix), and idea.tex
- Reports word n-gram share and maximal verbatim spans (>=n words); file boundaries prevent cross-file spurious matches
- Not an external plagiarism scan

```bash
python tools/self_overlap.py --root . --ngram 15 --report self_overlap_report.md
```

Both scripts write a human-readable report; use `--json` to emit machine-readable summaries.
