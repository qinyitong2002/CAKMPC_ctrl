#!/usr/bin/env bash
# Render docs/ into CA-KMPC_supplementary.pdf (pandoc + xelatex).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build
python3 scripts/assemble_markdown.py > build/supplementary.md
pandoc build/supplementary.md -s -o build/supplementary.tex \
  -V geometry:margin=2cm -V fontsize=10pt -V mainfont="DejaVu Serif" \
  -V mathfont="DejaVu Math TeX Gyre" -V colorlinks=true -H scripts/pdf_header.tex
# some TeX installations lack lmodern.sty, which the pandoc template loads
kpsewhich lmodern.sty >/dev/null || : > build/lmodern.sty
cp -r figures build/
(cd build && xelatex -interaction=nonstopmode supplementary.tex >/dev/null && \
             xelatex -interaction=nonstopmode supplementary.tex >/dev/null) || true
cp build/supplementary.pdf CA-KMPC_supplementary.pdf
echo "wrote CA-KMPC_supplementary.pdf"
