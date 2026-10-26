#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

echo "=== 1. Khởi tạo Git repository ==="
if [ ! -d ".git" ]; then
  git init
  git branch -M main
fi

echo "=== 2. Commit mã nguồn ==="
git add .
if git diff --staged --quiet; then
  echo "Không có thay đổi mới để commit."
else
  git commit -m "feat: init omp-manager - Antigravity quota dashboard for omp"
fi

echo "=== 3. Tạo repo trên GitHub và Push ==="
# Kiểm tra nếu remote origin chưa tồn tại
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "Đang tạo repository 'omp-manager' trên GitHub..."
  gh repo create omp-manager --public --source=. --remote=origin --push
else
  echo "Đang push lên origin main..."
  git push -u origin main
fi

echo "=== Hoàn tất! ==="
