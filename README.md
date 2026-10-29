# omp-manager & ompagy — Quota Dashboard & Multi-Account Manager cho `omp`

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/MinhBienK2/omp-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/MinhBienK2/omp-manager/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](#)

**`omp-manager`** (cũng gọi là **`ompagy`**) là công cụ CLI nhẹ, độc lập và toàn diện giúp giám sát, xếp hạng và tối ưu hóa việc phân bổ hạn mức (quota) của nhiều tài khoản AI trong `omp` (Google Antigravity, Gemini, Claude & GPT).

Được viết bằng Python thuần (thư viện chuẩn), không phụ thuộc bất kỳ thư viện ngoài nào (`zero-dependencies`), khởi động tức thì (< 30ms).

---

## 📸 Giao diện minh họa

```
╭─ ANTIGRAVITY QUOTA · 3 accounts ─────────────────────────── snapshot 0m30s ago ─╮
│ GEMINI 5H █████████─  93.9% (3/3 ready) │ ★ Best Gemini : alice@example.com    │
│ GEMINI 1W █████─────  45.1% (3/3 ready) │ ★ Best Claude : bob@example.com      │
│ C&G 5H    ██████████ 100.0% (3/3 ready) │ ⚡ Next relief : All quotas 100% full │
│ C&G 1W    ████──────  43.4% (3/3 ready) │ ⟳ Pool Cap    : 2.7x 5h · 0.9x 1w    │
├─────────────────────────────────────────┴──────────────────────────────────────┤
│ ⚡ TODAY USAGE : 6,491 reqs  ·  In: 206.4M  ·  Out: 2.8M  ·  Total: 209.3M tokens │
╰────────────────────────────────────────────────────────────────────────────────╯

RANKING  (best -> worst · ranked by gemini)
╭────┬───────────────────┬────────────┬────────────┬────────────┬────────────┬───────┬───────╮
│ #  │ ACCOUNT           │ G5H        │ G1W        │ C5H        │ C1W        │ SCORE │ GRADE │
├────┼───────────────────┼────────────┼────────────┼────────────┼────────────┼───────┼───────┤
│  1 │ alice@example.com │ ████   98% │ ████   91% │ ████  100% │ █───   34% │  82.6 │ A     │
│  2 │ bob@example.com   │ ███─   84% │ ██──   44% │ ████  100% │ ██──   48% │  62.3 │ B     │
│  3 │ carol@example.com │ ████  100% │ ────    0% │ ████  100% │ ██──   48% │  49.8 │ C     │
╰────┴───────────────────┴────────────┴────────────┴────────────┴────────────┴───────┴───────╯

OTHER METERS  (not part of the score)
  alice@example.com     Gemini Pro 5h     87.5% left · reset now

bar & % = quota remaining  ·  grade: S≥90 A≥75 B≥55 C≥35 D≥15 F<15
weights (gemini): G5H 0.30 G1W 0.40 C5H 0.10 C1W 0.20 · n/r = not reported
```

---

## ✨ Tính năng nổi bật

- ⚡ **Thống kê Token & Request trong ngày (`TODAY USAGE`)**: Tự động scan session logs từ `~/.omp/agent/sessions/*.jsonl`, tổng hợp số request, lượng input/output tokens và tổng token đã dùng trong ngày với bộ nhớ cache `mtime` siêu tốc.
- 📏 **Hệ thống Responsive 4 tầng (`TIERS`)**: Tự động nhận diện độ rộng màn hình terminal (`full`, `compact`, `tight`, `micro`), co gọn email thông minh, không bao giờ vỡ hàng khi chia đôi màn hình trong tmux hay iTerm.
- 🔄 **Tự động phát hiện & cập nhật (`Self-Updater`)**: Khi repository trên GitHub có bản cập nhật mới, chương trình sẽ tự động phát hiện khi chạy và cập nhật phiên bản mới nhất (kèm re-exec ngay tức thì), hoặc bạn có thể chủ động chạy `--update`.
- 🤝 **Hỗ trợ song song 2 tên lệnh `omp-manager` và `ompagy`**: Tự động nhận diện tên file đang chạy (`sys.argv[0]`) để đổi tiêu đề, cờ giúp đỡ và biến môi trường tương ứng (`OMP_MANAGER_*` hoặc `OMPAGY_*`).
- 📊 **Thanh Quota Bar và % còn lại nhất quán**: Cả thanh đồ họa và con số % đều biểu thị lượng hạn mức còn lại (`remaining`), không gây nhầm lẫn giữa lượng đã dùng và lượng còn lại.
- 🎯 **Chấm điểm thông minh & Xếp hạng**: Đánh giá chất lượng tài khoản từ `0` đến `100` và phân loại từ hạng `S` (nguyên vẹn) tới `F` (hạn mức cạn kiệt).
- 🏆 **Gợi ý tài khoản tối ưu**: Hiển thị ngay `★ Best Gemini` và `★ Best Claude`.
- 🚀 **Chế độ Mini (`--mini`)**: Một dòng tóm tắt siêu nhẹ cho thanh trạng thái của **tmux**, **starship**, hoặc prompt shell.
- 🔄 **Xuất dữ liệu chuẩn JSON (`--json`)**: Tích hợp với automation pipeline hoặc cronjob.

---

## 🛠️ Yêu cầu hệ thống

| Thành phần | Yêu cầu | Ghi chú |
|---|---|---|
| **Python** | ≥ 3.9 | Chỉ dùng thư viện chuẩn (Standard Library) |
| **`omp` CLI** | Khuyên dùng | Cung cấp dữ liệu từ lệnh `omp usage --json` (hoặc dùng offline với `--input FILE`) |

---

## 📦 Cài đặt

### Cách 1: Sử dụng script cài đặt tự động (Khuyên dùng)

```bash
# Clone repository về máy
git clone https://github.com/MinhBienK2/omp-manager.git
cd omp-manager

# Cài đặt vào ~/.local/bin (mặc định cho người dùng hiện tại)
./install.sh

# Hoặc cài đặt cho toàn hệ thống (cần quyền root):
PREFIX=/usr/local sudo ./install.sh
```

Script sẽ tự động:
1. Sao lưu phiên bản cũ nếu đã tồn tại.
2. Cài đặt file thực thi chính vào `~/.local/bin/omp-manager`.
3. Tạo symbolic link `~/.local/bin/ompagy -> ~/.local/bin/omp-manager` để bạn gõ lệnh nào cũng được.
4. Kiểm tra biến `$PATH` và thông báo hướng dẫn cụ thể nếu cần.

### Cách 2: Cài đặt thủ công

```bash
chmod +x omp-manager ompagy
mkdir -p ~/.local/bin
cp omp-manager ~/.local/bin/omp-manager
ln -sf ~/.local/bin/omp-manager ~/.local/bin/ompagy

# Đảm bảo ~/.local/bin có trong PATH:
export PATH="$HOME/.local/bin:$PATH"
```

---

## 🚀 Hướng dẫn sử dụng

### 1. Dùng thử offline với dữ liệu mẫu

```bash
omp-manager --input examples/sample-usage.json
# hoặc
ompagy --input examples/sample-usage.json
```

Làm mới thời gian của snapshot mẫu:
```bash
python3 examples/make_sample.py
```

### 2. Các lệnh thường dùng

```bash
# Xem bảng đầy đủ (tự căn chỉnh theo độ rộng terminal)
ompagy

# Tự động cập nhật lên phiên bản mới nhất từ GitHub
ompagy --update

# Làm mới cache của omp trước khi đọc
ompagy --refresh

# Tùy chọn bố cục bảng hiển thị: full, compact, tight, micro, stack
ompagy --layout compact
ompagy --layout tight

# Ưu tiên tài khoản còn quota Claude / GPT
ompagy --by claude

# Sắp xếp theo tài khoản sắp reset quota sớm nhất
ompagy --sort reset

# Một dòng ngắn gọn cho tmux / prompt status
ompagy --mini

# Xuất toàn bộ dữ liệu dạng JSON (bao gồm cả today token usage)
ompagy --json | jq '.today'
```

---

## ⚙️ Bảng tham số đầy đủ

| Tùy chọn | Mặc định | Ý nghĩa |
|---|---|---|
| `--update` | `False` | Kiểm tra và cài đặt bản cập nhật mới nhất từ GitHub ngay lập tức |
| `--no-update` | `False` | Tắt tính năng tự động kiểm tra bản cập nhật chạy nền |
| `--layout {auto,full,compact,tight,micro,stack}` | `auto` | Mức độ hiển thị bảng (tự co dãn theo terminal) |
| `--refresh` | `False` | Xóa cache của `omp` trước khi đọc để lấy dữ liệu mới nhất từ máy chủ |
| `--input FILE` | `-` | Đọc dữ liệu từ file JSON snapshot thay vì gọi `omp usage` |
| `--profile NAME` | `$OMP_MANAGER_PROFILE` / `$OMPAGY_PROFILE` | Profile cụ thể của `omp` cần truy vấn |
| `--by {gemini,balanced,claude}` | `gemini` | Chế độ tính trọng số điểm số |
| `--sort {score,reset,name}` | `score` | Tiêu chí sắp xếp danh sách tài khoản |
| `--narrow` | `False` | Ép giao diện hiển thị dạng card xếp chồng (tương đương `--layout stack`) |
| `--mini`, `-1` | `False` | Xuất 1 dòng tóm tắt trạng thái (statusline / tmux) |
| `--json` | `False` | Xuất toàn bộ dữ liệu đã phân tích dưới dạng JSON |
| `--color {auto,always,never}` | `auto` | Bật / tắt màu sắc ANSI |
| `--stale SEC` | `900` | Ngưỡng cảnh báo dữ liệu cũ (giây, mặc định 15 phút) |
| `--timeout SEC` | `180` | Thời gian timeout tối đa khi gọi lệnh `omp usage` |
| `--version`, `-v` | `-` | Xem phiên bản hiện tại |

### Biến môi trường

Cả hai tiền tố `OMPAGY_*` và `OMP_MANAGER_*` đều được hỗ trợ; tiền tố khớp với tên lệnh bạn gõ sẽ được ưu tiên.

| Biến | Ý nghĩa |
|---|---|
| `OMPAGY_PROFILE` / `OMP_MANAGER_PROFILE` | Profile `omp` cần truy vấn |
| `OMPAGY_BY` / `OMP_MANAGER_BY` | Preset chấm điểm mặc định (`gemini`) |
| `OMPAGY_WEIGHTS` / `OMP_MANAGER_WEIGHTS` | 4 trọng số tuỳ chỉnh, cách nhau bởi dấu phẩy |
| `OMPAGY_NO_UPDATE` / `OMP_MANAGER_NO_UPDATE` | Đặt bất kỳ giá trị để tắt kiểm tra cập nhật nền |
| `OMP_DEFAULT_PROG` | Ép tên chương trình (`ompagy` hoặc `omp-manager`) |

---

## 🔄 Cơ chế Tự động Cập nhật (Auto-Update)

Khi bạn cập nhật code trên GitHub, **máy của người dùng khác cũng tự động được cập nhật** — không cần cài lại, không cần `git pull`.

1. **Khi chạy bình thường**: Chương trình kiểm tra `version.json` trên GitHub theo chu kỳ nền (mỗi **1 giờ** một lần, kết quả được cache tại `~/.cache/<tên lệnh>/update_check.json`). Nếu phát hiện phiên bản mới, nó sẽ tải script mới về, **kiểm tra cú pháp trước khi cài** (không bao giờ cài code hỏng), ghi đè file thực thi theo cách atomic (`os.replace`) rồi `execv` chạy lại với phiên bản mới.
2. **Không làm chậm CLI**: Kiểm tra nền bị bỏ qua hoàn toàn với `--mini`, `--json`, `--input` và `--no-update`, nên status bar của tmux hay cronjob luôn phản hồi tức thì.
3. **Cập nhật thủ công**: `ompagy --update` (hoặc `omp-manager --update`) kiểm tra và cài ngay lập tức.
4. **Nếu không có quyền ghi file**: Chương trình báo rõ và gợi ý `sudo ompagy --update`, thay vì im lặng bỏ qua.
5. **Bản cài trong thư mục git**: Nếu bạn cài bằng cách clone repo, chương trình ưu tiên `git pull --ff-only` trước khi tải từ mạng.

> Phiên bản được khai báo ở **hai** nơi: dòng `__version__` trong `omp-manager` và file `version.json`. Khi phát hành bản mới, hãy sửa cả hai (script `release.sh` hỗ trợ việc này).

---

## 🧮 Cơ chế tính điểm & Xếp loại

### 1. Các nhóm hạn mức (Buckets)
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

*Tùy biến trọng số qua biến môi trường `OMPAGY_WEIGHTS` hoặc `OMP_MANAGER_WEIGHTS`:*
```bash
export OMPAGY_WEIGHTS="0.4,0.4,0.1,0.1"
ompagy
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
set -g status-right '#(ompagy --mini)'
```

---

## 📂 Cấu trúc thư mục

```
omp-manager/
├── omp-manager              # Script chính (Python 3 thuần, executable)
├── ompagy                   # Wrapper alias tương thích (file thật, không phải symlink)
├── version.json             # File đánh dấu phiên bản phát hành (nguồn cho auto-update)
├── install.sh               # Script cài đặt tự động vào ~/.local/bin
├── release.sh               # Script phát hành phiên bản mới (bump version + push + tag)
├── .gitignore               # Cấu hình bỏ qua file tạm, cache
├── README.md                # Tài liệu hướng dẫn sử dụng chi tiết
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD kiểm thử tự động trên Python 3.9 - 3.13
├── examples/
│   ├── sample-usage.json    # Snapshot JSON mẫu để chạy thử offline
│   └── make_sample.py       # Script sinh snapshot mẫu thời gian thực
└── tests/
    ├── test_recoveries.py   # Test logic tính hồi phục hạn mức (recovery delta)
    ├── test_layouts.py      # Test các tầng hiển thị co dãn (responsive tiers)
    ├── test_tokens.py       # Test định dạng và tổng hợp token sử dụng
    └── test_updater.py      # Test so sánh phiên bản, config env và dual identity
```

---

## 📤 Phát hành phiên bản mới

Khi bạn muốn đẩy bản mới lên GitHub (để mọi máy người dùng tự cập nhật):

```bash
./release.sh 1.3.0 "Thêm bộ lọc theo profile"
```

Script sẽ bump `__version__` trong `omp-manager`, cập nhật `version.json`, chạy test, commit, push lên `main` và tạo tag `v1.3.0`.

> **Luôn phát hành từ `main`.** Client đọc `version.json` từ `main` để biết có bản mới. Nếu `version.json` nằm trên một nhánh khác thì không ai nhận được thông báo cập nhật — tính năng auto-update chết âm thầm. `release.sh` đã tự chuyển về `main` và pull trước khi phát hành để tránh lỗi này.

### Nhánh nào được bảo vệ?

Repo hiện **chưa** bật branch protection, nghĩa là collaborator có `push` quyền đẩy thẳng vào `main`. Bật protection cần quyền `admin` (owner của repo).

Để bật (Settings → Branches → Add rule hoặc Rulesets):

- Branch name pattern: `main`
- Require a pull request before merging → **1 approving review**
- Require status checks to pass → chọn job `CI / Quality Assurance`
- Block force pushes và branch deletion

Cách này giữ cho `main` luôn có `version.json` đúng, nên auto-update không bị hỏng do ai đó push thẳng.

---

## 🧪 Chạy bộ kiểm thử (Test Suite)

```bash
python3 -m unittest discover -s tests -v
```

---

## 📄 License

Dự án được phân phối dưới giấy phép [MIT License](LICENSE).
