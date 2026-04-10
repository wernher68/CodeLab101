#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if command -v open >/dev/null 2>&1; then
  open "index.html"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "index.html"
else
  echo "未找到可用的打开命令，请手动双击 index.html"
fi
