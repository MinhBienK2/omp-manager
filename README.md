# omp-manager — Quota Dashboard & Multi-Account Manager cho `omp`

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](#)

**`omp-manager`** (trước đây gọi là `ompagy`) là công cụ dòng lệnh (CLI) nhẹ, độc lập giúp giám sát, xếp hạng và tối ưu hóa việc phân bổ hạn mức (quota) của nhiều tài khoản AI trong `omp` (đặc biệt là Google Antigravity, Gemini, Claude & GPT).

Được viết bằng Python thuần (thư viện chuẩn), không cần cài thêm thư viện phụ thuộc (`zero-dependencies`), khởi động tức thì.

---

## 📸 Giao diện minh họa

```
╭─ ANTIGRAVITY QUOTA · 3 accounts ─────────────────────────── snapshot 0m30s ago ─╮
│ GEMINI 5H ███████████░   6.1% (3/3 ready) │ ★ Best Gemini : alice@example.com   │
│ GEMINI 1W █████░░░░░░░  54.9% (3/3 ready) │ ★ Best Claude : bob@example.com     │
│ C&G 5H    ████████████   0.0% (3/3 ready) │ ⚡ Next relief : alice (+2% in 4h49m)│
│ C&G 1W    █████░░░░░░░  56.6% (3/3 ready) │ ⟳ Pool Cap    : 2.7x 5h · 0.9x 1w   │
╰───────────────────────────────────────────┴─────────────────────────────────────╯

RANKING  (best -> worst · ranked by gemini)
╭─ 1. alice@example.com ────────────────────────────  82.6 · A · ready ─╮
│ GEMINI 5H ██████   2.0% 4h49m    │ C&G 5H ██████   0.0% 4h54m        │
│ GEMINI 1W █████░   9.1%  2d5h    │ C&G 1W ██░░░░  65.9% 19h59m       │
╰──────────────────────────────────┴───────────────────────────────────╯

score weights (gemini): GEMINI 5H 0.30  GEMINI 1W 0.40  C&G 5H 0.10  C&G 1W 0.20
```

---

## ✨ Tính năng nổi bật

- 📊 **Tự động gộp & phân nhóm meter**: Nhận diện các quota riêng biệt và dùng chung (`Gemini 5h`, `Gemini 1w`, `Claude & GPT 5h`, `Claude & GPT 1w`).
- 🎯 **Chấm điểm thông minh**: Tự động đánh giá chất lượng từng tài khoản theo thang điểm từ `0` đến `100` và xếp hạng từ `S` (nguyên vẹn), `A`, `B`, `C`, `D` đến `F` (hết quota).
- 🏆 **Gợi ý tài khoản tối ưu**: Hiển thị ngay `★ Best Gemini` và `★ Best Claude` giúp bạn chọn tài khoản phù hợp nhất cho từng tác vụ.
- ⚡ **Dự báo hồi phục hạn mức (`Next relief`)**: Biết chính xác tài khoản nào sẽ được reset hạn mức sớm nhất và hồi phục bao nhiêu %.
- 🚀 **Chế độ Mini (`--mini`)**: Xuất một dòng tóm tắt cực nhẹ để gắn vào status bar của **tmux**, **starship**, hoặc prompt shell.
- 🔄 **Xuất dữ liệu chuẩn JSON (`--json`)**: Tích hợp với các script tự động hóa, pipeline hoặc cronjob khác.
- 💡 **Khả năng tương thích ngược**: Tự động hỗ trợ cả hai lệnh `omp-manager` và `ompagy`.

---

## 🛠️ Yêu cầu hệ thống

| Thành phần | Yêu cầu | Ghi chú |
|---|---|---|
| **Python** | ≥ 3.9 | Chỉ dùng thư viện chuẩn (Standard Library) |
| **`omp` CLI** | Khuyên dùng | Cung cấp dữ liệu từ lệnh `omp usage --json` (hoặc dùng offline với `--input FILE`) |

Kiểm tra trên máy:
```bash
python3 --version
omp --version
```

---

## 📦 Cài đặt

### Cách 1: Sử dụng script cài đặt tự động (Khuyên dùng)

```bash
# Clone hoặc tải repository về máy
cd omp-manager

# Cài đặt vào ~/.local/bin (mặc định)
./install.sh

# Hoặc cài đặt cho toàn hệ thống (cần quyền root):
PREFIX=/usr/local sudo ./install.sh
```

Script sẽ:
1. Sao lưu phiên bản cũ nếu đã tồn tại.
2. Cài đặt file thực thi vào `~/.local/bin/omp-manager`.
3. Tạo symbolic link `~/.local/bin/ompagy -> ~/.local/bin/omp-manager` để bạn có thể dùng cả 2 lệnh.
4. Tự động kiểm tra `$PATH` và cảnh báo nếu cần cấu hình thêm.

### Cách 2: Cài đặt thủ công

```bash
chmod +x omp-manager ompagy
mkdir -p ~/.local/bin
cp omp-manager ~/.local/bin/omp-manager
ln -sf ~/.local/bin/omp-manager ~/.local/bin/ompagy

# Đảm bảo ~/.local/bin có trong PATH (thêm vào ~/.bashrc hoặc ~/.zshrc nếu chưa có):
export PATH="$HOME/.local/bin:$PATH"
```

---

## 🚀 Hướng dẫn sử dụng

### 1. Dùng thử offline với dữ liệu mẫu

Thư mục `examples/` có sẵn snapshot mẫu để bạn kiểm tra giao diện mà không cần tài khoản hay kết nối mạng:

```bash
omp-manager --input examples/sample-usage.json
```

Làm mới thời gian của snapshot mẫu:
```bash
python3 examples/make_sample.py
```

### 2. Các lệnh thường dùng

```bash
# Chạy xem bảng đầy đủ (tự căn chỉnh theo độ rộng terminal)
omp-manager

# Làm mới cache của omp trước khi đọc để lấy dữ liệu mới nhất
omp-manager --refresh

# Ưu tiên tài khoản còn quota Claude / GPT
omp-manager --by claude

# Ưu tiên cân bằng cả hai nguồn Gemini & Claude/GPT
omp-manager --by balanced

# Sắp xếp theo tài khoản sắp reset quota sớm nhất
omp-manager --sort reset

# Một dòng ngắn gọn cho tmux / prompt status
omp-manager --mini

# Xuất kết quả dạng JSON để xử lý tiếp bằng jq
omp-manager --json | jq '.accounts[] | {email, score, grade}'

# Terminal màn hình hẹp (dạng thẻ dọc)
omp-manager --narrow

# Không sử dụng mã màu ANSI (phù hợp ghi vào log file)
omp-manager --color never
```

---

## ⚙️ Bảng tham số đầy đủ

| Tùy chọn | Mặc định | Ý nghĩa |
|---|---|---|
| `--refresh` | `False` | Xóa cache của `omp` trước khi đọc để lấy dữ liệu mới nhất từ máy chủ |
| `--input FILE` | `-` | Đọc dữ liệu từ file JSON snapshot thay vì gọi `omp usage` |
| `--profile NAME` | `$OMP_MANAGER_PROFILE` | Profile cụ thể của `omp` cần truy vấn |
| `--by {gemini,balanced,claude}` | `gemini` | Chế độ tính trọng số điểm số |
| `--sort {score,reset,name}` | `score` | Tiêu chí sắp xếp danh sách tài khoản |
| `--narrow` | `False` | Ép giao diện hiển thị dạng card xếp chồng (dành cho màn hình hẹp) |
| `--mini`, `-1` | `False` | Xuất 1 dòng tóm tắt trạng thái (statusline / tmux) |
| `--json` | `False` | Xuất toàn bộ dữ liệu đã phân tích dưới dạng JSON |
| `--color {auto,always,never}` | `auto` | Bật / tắt màu sắc ANSI |
| `--stale SEC` | `900` | Ngưỡng cảnh báo dữ liệu cũ (giây, mặc định 15 phút) |
| `--timeout SEC` | `180` | Thời gian timeout tối đa khi gọi lệnh `omp usage` |

---

## 🧮 Cơ chế tính điểm & Xếp loại

### 1. Các nhóm hạn mức (Buckets)

Hệ thống gom các hạn mức từ `omp usage --json` về 4 nhóm chính:
- **`gemini-5h`**: Cửa sổ 5 giờ của Gemini.
- **`gemini-1w`**: Hạn mức tuần của Gemini.
- **`shared-5h`**: Hạn mức 5 giờ dùng chung cho Claude & OpenAI GPT.
- **`shared-1w`**: Hạn mức tuần dùng chung cho Claude & OpenAI GPT.

### 2. Trọng số theo preset (`--by`)

| Preset | GEMINI 5H | GEMINI 1W | C&G 5H | C&G 1W | Thích hợp khi |
|---|---|---|---|---|---|
| **`gemini`** *(mặc định)* | 0.30 | 0.40 | 0.10 | 0.20 | Chủ yếu dùng Gemini |
| **`balanced`** | 0.20 | 0.30 | 0.20 | 0.30 | Dùng đều cả Gemini và Claude/GPT |
| **`claude`** | 0.10 | 0.20 | 0.30 | 0.40 | Ưu tiên dùng Claude / GPT |

*Bạn có thể tùy biến trọng số riêng bằng biến môi trường `OMP_MANAGER_WEIGHTS` (4 số cách nhau bởi dấu phẩy):*
```bash
export OMP_MANAGER_WEIGHTS="0.4,0.4,0.1,0.1"
omp-manager
```

### 3. Thang xếp loại (Grades)

| Điểm số | Hạng | Trạng thái | Ý nghĩa |
|---|---|---|---|
| **≥ 90** | `S` | `fresh` | Hạn mức còn nguyên, tối ưu sử dụng |
| **≥ 75** | `A` | `ready` | Hạn mức dồi dào, sẵn sàng cho công việc nặng |
| **≥ 55** | `B` | `ok` | Hạn mức ổn định |
| **≥ 35** | `C` | `tired` | Hạn mức đang cạn dần |
| **≥ 15** | `D` | `critical` | Sắp cạn kiệt toàn bộ |
| **< 15** | `F` | `dead` | Đã hết quota hoàn toàn |

---

## 🖥️ Tích hợp Cron & Tmux Statusline

### Statusline trong Tmux
Thêm vào `~/.tmux.conf`:
```tmux
set -g status-right '#(omp-manager --mini)'
```

### Cronjob cập nhật định kỳ mỗi 5 phút
```cron
*/5 * * * * /home/$USER/.local/bin/omp-manager --refresh --mini > ~/.cache/omp-status.txt 2>/dev/null
```

---

## 📂 Cấu trúc thư mục

```
omp-manager/
├── omp-manager              # Script chính (Python 3 thuần, executable)
├── ompagy                   # Wrapper script tương thích ngược
├── install.sh               # Script cài đặt tự động vào ~/.local/bin
├── .gitignore               # Cấu hình bỏ qua file rác, file tạm
├── README.md                # Tài liệu hướng dẫn sử dụng
├── examples/
│   ├── sample-usage.json    # Snapshot JSON giả lập để kiểm tra offline
│   └── make_sample.py       # Script sinh dữ liệu giả lập mẫu mới
└── tests/
    └── test_recoveries.py   # Unit test (stdlib unittest) cho logic recovery
```

---

## 🧪 Chạy test

```bash
python3 -m unittest discover -s tests -v
```

---

## 🔒 Lưu ý về quyền riêng tư

`omp-manager` đọc và hiển thị địa chỉ email tài khoản Google Antigravity của bạn để quản lý. Khi chia sẻ ảnh chụp màn hình terminal hoặc các file log JSON ra bên ngoài, hãy lưu ý che đi các thông tin nhạy cảm. Thư mục `examples/` sử dụng tên miền giả định `@example.com` nên hoàn toàn an toàn khi chia sẻ công khai.

---

## 📄 License

Dự án được phân phối dưới giấy phép [MIT License](LICENSE).
# probe
