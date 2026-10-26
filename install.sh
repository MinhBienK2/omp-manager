#!/usr/bin/env bash
# Cài omp-manager vào thư mục bin của bạn.
#
#   ./install.sh                 -> cài vào ~/.local/bin (mặc định)
#   PREFIX=/usr/local ./install.sh -> cài vào /usr/local/bin
#
# Chỉ cần Python 3.8+; lệnh `omp` phải có trong PATH để chạy omp-manager.
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREFIX="${PREFIX:-$HOME/.local}"
BIN_DIR="$PREFIX/bin"
TARGET="$BIN_DIR/omp-manager"
ALIAS_TARGET="$BIN_DIR/ompagy"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Lỗi: không tìm thấy python3 trong PATH." >&2
  exit 1
fi

mkdir -p "$BIN_DIR"

if [ -e "$TARGET" ]; then
  BACKUP="$TARGET.bak.$(date +%Y%m%d-%H%M%S)"
  cp -p "$TARGET" "$BACKUP"
  echo "Đã sao lưu bản cũ: $BACKUP"
fi

SRC_SCRIPT="$SRC_DIR/omp-manager"
if [ ! -f "$SRC_SCRIPT" ]; then
  SRC_SCRIPT="$SRC_DIR/ompagy"
fi

install -m 0755 "$SRC_SCRIPT" "$TARGET"
ln -sf "$TARGET" "$ALIAS_TARGET"
echo "Đã cài: $TARGET"
echo "Đã tạo alias: $ALIAS_TARGET -> $TARGET"

case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *) echo "Cảnh báo: $BIN_DIR chưa nằm trong PATH. Thêm dòng sau vào ~/.bashrc hoặc ~/.zshrc:"
     echo "  export PATH=\"$BIN_DIR:\$PATH\"" ;;
esac

if ! command -v omp >/dev/null 2>&1; then
  echo "Cảnh báo: không tìm thấy lệnh 'omp' trong PATH - omp-manager cần 'omp usage --json' để lấy dữ liệu."
fi

echo
echo "Thử ngay:  $TARGET --help"
