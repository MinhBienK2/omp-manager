#!/usr/bin/env bash
# Cài đặt omp-manager / ompagy vào thư mục bin của bạn.
#
#   ./install.sh                   -> cài vào ~/.local/bin (mặc định)
#   PREFIX=/usr/local ./install.sh -> cài vào /usr/local/bin
#
# Cả 2 lệnh `omp-manager` và `ompagy` đều được hỗ trợ song song đầy đủ.
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

# Sao lưu nếu đã tồn tại bản cũ
for existing in "$TARGET" "$ALIAS_TARGET"; do
  if [ -e "$existing" ] && [ ! -L "$existing" ]; then
    BACKUP="$existing.bak.$(date +%Y%m%d-%H%M%S)"
    cp -p "$existing" "$BACKUP"
    echo "✓ Đã sao lưu bản cũ: $BACKUP"
  fi
done

SRC_SCRIPT="$SRC_DIR/omp-manager"
if [ ! -f "$SRC_SCRIPT" ]; then
  echo "Lỗi: không tìm thấy file 'omp-manager' trong $SRC_DIR." >&2
  exit 1
fi

install -m 0755 "$SRC_SCRIPT" "$TARGET"

# The alias is installed as a real file (not a symlink) so the install also
# works when the project was downloaded as a zip archive.
if [ -f "$SRC_DIR/ompagy" ]; then
  install -m 0755 "$SRC_DIR/ompagy" "$ALIAS_TARGET"
  echo "✓ Đã cài đặt: $TARGET"
  echo "✓ Đã cài đặt: $ALIAS_TARGET (alias của $TARGET)"
else
  ln -sf "$TARGET" "$ALIAS_TARGET"
  echo "✓ Đã cài đặt: $TARGET"
  echo "✓ Đã tạo symlink: $ALIAS_TARGET -> $TARGET"
fi

case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *) echo
     echo "⚠️ Cảnh báo: $BIN_DIR chưa nằm trong PATH. Hãy thêm vào ~/.bashrc hoặc ~/.zshrc:"
     echo "  export PATH=\"$BIN_DIR:\$PATH\"" ;;
esac

if ! command -v omp >/dev/null 2>&1; then
  echo
  echo "ℹ️ Lưu ý: Không tìm thấy lệnh 'omp' trong PATH. Bạn có thể dùng snapshot qua cờ '--input FILE'."
fi

echo
echo "🎉 Hoàn tất! Bạn có thể sử dụng bất kỳ lệnh nào:"
echo "  omp-manager --help"
echo "  ompagy --help"
