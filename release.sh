#!/usr/bin/env bash
# Phát hành phiên bản mới của omp-manager.
#
#   ./release.sh 1.3.0 "Mô tả ngắn cho bản cập nhật"
#
# Luôn phát hành từ nhánh `main`, vì client đọc version.json từ `main`
# để biết có bản mới. Phát hành từ nhánh khác sẽ khiến người dùng
# không nhận được thông báo cập nhật.
#
# Script sẽ:
#   1. Kiểm tra working tree sạch, chuyển về main và pull
#   2. Cập nhật __version__ trong omp-manager
#   3. Cập nhật version.json (version + description + updatedAt)
#   4. Chạy test, commit, push lên main và tạo Git tag
set -euo pipefail

VERSION="${1:-}"
DESCRIPTION="${2:-}"
RELEASE_BRANCH="main"

if [ -z "$VERSION" ]; then
  echo "Usage: ./release.sh <version> [description]" >&2
  echo "Example: ./release.sh 1.3.0 \"Thêm bộ lọc theo profile\"" >&2
  exit 1
fi

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SRC_DIR"

if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Lỗi: version phải có dạng MAJOR.MINOR.PATCH (ví dụ 1.3.0), nhận '$VERSION'." >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Lỗi: không tìm thấy python3 trong PATH." >&2
  exit 1
fi

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Lỗi: thư mục này không phải git repo." >&2
  exit 1
fi

# Working tree phải sạch, nếu không commit có thể lẫn thay đổi ngoài ý muốn.
if [ -n "$(git status --porcelain)" ]; then
  echo "Lỗi: working tree không sạch. Commit hoặc stash trước khi phát hành:" >&2
  git status --short >&2
  exit 1
fi

# Phát hành luôn từ main.
git checkout "$RELEASE_BRANCH"
git pull --ff-only origin "$RELEASE_BRANCH"

# Tag đã tồn tại -> dừng, tránh ghi đè lịch sử phát hành.
if git rev-parse "v${VERSION}" >/dev/null 2>&1; then
  echo "Lỗi: tag v${VERSION} đã tồn tại." >&2
  exit 1
fi

TODAY="$(date +%Y-%m-%d)"

python3 - "$VERSION" "$DESCRIPTION" "$TODAY" <<'PY'
import json
import re
import sys

version, description, today = sys.argv[1], sys.argv[2], sys.argv[3]

with open("omp-manager", "r", encoding="utf-8") as f:
    script = f.read()

new_script, count = re.subn(r'__version__ = "[^"]+"', f'__version__ = "{version}"', script, count=1)
if count != 1:
    sys.exit("Lỗi: không tìm thấy dòng __version__ trong omp-manager.")

with open("omp-manager", "w", encoding="utf-8") as f:
    f.write(new_script)

with open("version.json", "r", encoding="utf-8") as f:
    info = json.load(f)
info["version"] = version
info["updatedAt"] = today
if description:
    info["description"] = description

with open("version.json", "w", encoding="utf-8") as f:
    json.dump(info, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"✓ omp-manager  -> {version}")
print(f"✓ version.json -> {version} ({today})")
PY

python3 -m py_compile omp-manager
python3 -m unittest discover -s tests >/dev/null && echo "✓ test suite pass"

git add omp-manager version.json
git commit -m "release: v${VERSION}${DESCRIPTION:+ - $DESCRIPTION}"

git push origin "$RELEASE_BRANCH"
git tag -a "v${VERSION}" -m "v${VERSION}${DESCRIPTION:+ - $DESCRIPTION}"
git push origin "v${VERSION}"

echo
echo "🎉 Đã phát hành v${VERSION} trên nhánh ${RELEASE_BRANCH}."
echo "   Mọi máy người dùng sẽ tự động cập nhật trong tối đa 1 giờ tới."
