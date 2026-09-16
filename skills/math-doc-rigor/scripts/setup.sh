#!/usr/bin/env bash
# 环境准备：Python 依赖（markdown2 / weasyprint）+ MathJax（node）
set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[1/2] Python 依赖 markdown2 / weasyprint ..."
python3 -m pip install --quiet markdown2 weasyprint

echo "[2/2] MathJax (node) ..."
if [ ! -d "$HERE/node_modules/mathjax-full" ]; then
  ( cd "$HERE" && npm init -y >/dev/null 2>&1 && npm install --silent mathjax-full )
fi

echo
echo "完成。导出 PDF 时用："
echo "  MATHJAX_NODE_PATH=$HERE/node_modules python3 $HERE/md2pdf.py --outdir pdf 文档.md"
