# Hướng dẫn sử dụng cho thành viên mới

Tài liệu này hướng dẫn thao tác trên code hiện có. Chạy mọi lệnh từ thư mục gốc
`QKD_vs_PQC/`; cài project bằng editable install trước khi gọi các script. Đường dẫn config và
thư mục output trong YAML tương đối với gốc dự án.

## 1. Mở hoặc clone repository

Nếu đã được cấp thư mục dự án, mở chính thư mục đó bằng VS Code; không clone đè lên thư mục có
dữ liệu. Khi clone từ GitHub và tài khoản có quyền truy cập:

```powershell
git clone https://github.com/Duc-HUST-ET1/QKD_vs_PQC.git
Set-Location QKD_vs_PQC
```

```sh
git clone https://github.com/Duc-HUST-ET1/QKD_vs_PQC.git
cd QKD_vs_PQC
```

Lệnh đọc remote GitHub và tạo bản sao local; clone cần mạng và quyền truy cập. URL/khả năng truy
cập remote chưa được xác minh trong tác vụ tài liệu này. Nếu lệnh clone thất bại, dùng thư mục
đã được cấp và hỏi người quản lý repository về URL/quyền truy cập; không khởi tạo Git mới lên một
repository có lịch sử.

## 2. Kiểm tra Python và công cụ

```powershell
python --version
git --version
openssl version
openssl list -kem-algorithms
```

```sh
python3 --version
git --version
openssl version
openssl list -kem-algorithms
```

Dự án yêu cầu Python 3.11 trở lên. OpenSSL chỉ được kiểm tra để tham khảo khả năng backend; script
benchmark hiện không dùng OpenSSL CLI. Kết quả `openssl list` không quảng bá ML-KEM không được
thay bằng phỏng đoán hoặc thuật toán khác.

## 3. Tạo và kích hoạt virtual environment

Tại repository root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Virtual environment cô lập dependency khỏi Python toàn hệ thống. Sau khi kích hoạt, dấu nhắc
thường hiển thị `(.venv)`. Nếu PowerShell chặn activation, không cần thay đổi execution policy:
dùng trực tiếp `.venv\Scripts\python.exe` cho các lệnh thay vì activation.

## 4. Cài dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

```sh
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Các lệnh cài package hiện tại và pytest phục vụ phát triển; cần mạng/package index khi tải lần
đầu. Benchmark ML-KEM là optional:

```powershell
python -m pip install -e ".[mlkem,dev]"
```

```sh
python -m pip install -e ".[mlkem,dev]"
```

Nếu cài optional dependency thất bại, vẫn có thể chạy BB84 và unit tests; không tự cài thuật toán
khác thay thế ML-KEM-768.

## 5. Kiểm tra và sửa cấu hình

Đọc [experiment_config.yaml](../configs/experiment_config.yaml). Giá trị mặc định hiện có:

- seed `42`; số tín hiệu BB84 `100000`;
- `channel_error_rate=0.01`, `eve_probability=0.0`, ngưỡng minh họa `0.11`;
- ML-KEM `warmup_iterations=50`, `measured_iterations=1000`;
- output `data/raw`, `data/processed`, `figures`.

`load_config()` xác thực section, số nguyên, xác suất [0, 1], thuật toán phải chính xác
`ML-KEM-768`, output directory phải là đường dẫn tương đối. Sửa bản sao YAML hoặc tạo YAML khác;
script hỗ trợ `--config <đường-dẫn>`, đường dẫn tương đối tính từ project root. Không có cờ CLI
riêng cho từng thông số.

## 6. Chạy mô phỏng BB84

```powershell
python scripts/run_qkd.py
# Hoặc: python scripts/run_qkd.py --config configs/experiment_config.yaml
```

```sh
python scripts/run_qkd.py
# Hoặc: python scripts/run_qkd.py --config configs/experiment_config.yaml
```

Script đọc YAML, dùng `project.random_seed`, gọi `simulate_bb84`, sau đó tạo một file mới
`data/raw/qkd_<timestamp>_<id>.csv`. Terminal hiển thị số sifted/error bits, QBER, sifted
fraction và nhãn minh họa. QBER không phải bằng chứng kết luận an toàn; xem
[EXPERIMENT_PROTOCOL.md](EXPERIMENT_PROTOCOL.md).

Nếu import lỗi, kiểm tra đã chạy `pip install -e ".[dev]"` trong environment đang hoạt động và
đang ở project root. Nếu config sai, đọc thông báo validation; file raw đã tồn tại không bị ghi
đè.

## 7. Kiểm tra/chạy benchmark ML-KEM-768

Kiểm tra adapter mà không bắt đầu toàn bộ benchmark:

```powershell
python -c "from qkd_pqc.pqc.mlkem_benchmark import detect_mlkem_implementation; print(detect_mlkem_implementation())"
```

```sh
python -c 'from qkd_pqc.pqc.mlkem_benchmark import detect_mlkem_implementation; print(detect_mlkem_implementation())'
```

Đối tượng được trả về biểu thị adapter đã import được API chính xác và tự kiểm tra thành công;
`None` nghĩa là không có API tương thích/đã xác minh. Benchmark đầy đủ:

```powershell
python scripts/run_pqc_benchmark.py
```

```sh
python scripts/run_pqc_benchmark.py
```

Script đọc cùng YAML và ghi `data/raw/mlkem_<timestamp>_<id>.csv` nếu thành công. Nó đo riêng
key generation, encapsulation, decapsulation bằng `perf_counter_ns`, lưu từng mẫu (microsecond)
cùng median/p95. Khi không có implementation, script báo lỗi rõ ràng và trả mã thoát 2; đó không
phải một benchmark đã chạy. Cài optional dependency như bước 4, rồi chạy kiểm tra capability lại.
Tương thích cụ thể của phiên bản package/API chưa được bảo đảm trên mọi môi trường.

## 8. Chạy phân tích và tạo biểu đồ

```powershell
python scripts/run_analysis.py
```

```sh
python scripts/run_analysis.py
```

Script tìm mọi `qkd_*.csv` và `mlkem_*.csv` trong thư mục raw theo cấu hình. Nó kiểm tra cột bắt
buộc, bỏ qua hàng có giá trị rỗng/không hữu hạn/không hợp lệ, và tạo ảnh chỉ khi có dữ liệu thật
hợp lệ. PNG được lưu trong `figures/`; tên hình là cố định nên có thể bị ghi đè khi chạy lại.
Bảng định tính và các metric tổng hợp (nếu có) được ghi thành CSV mới trong
`data/processed/`. Nếu không có file raw nào, chương trình thông báo bỏ qua và kết thúc thành
công; không sinh dữ liệu giả.

## 9. Chạy pipeline tích hợp

```powershell
python scripts/run_all.py
```

```sh
python scripts/run_all.py
```

Pipeline đọc config, chạy BB84 bắt buộc, thử benchmark ML-KEM tùy chọn nếu capability check
thành công, sau đó phân tích **các file vừa tạo trong lần chạy này**. Terminal in trạng thái
từng bước. Benchmark không khả dụng được ghi là skipped; lỗi BB84 hoặc phân tích làm pipeline
trả mã khác 0. `run_all.py` không quét dữ liệu cũ; dùng `run_analysis.py` nếu muốn tổng hợp mọi
CSV raw hiện có.

## 10. Kiểm tra đầu ra

```powershell
Get-ChildItem data\raw
Get-ChildItem data\processed
Get-ChildItem figures
```

```sh
ls -la data/raw data/processed figures
```

CSV raw có tên run ID và chính sách không ghi đè; `.gitignore` bỏ qua CSV raw/processed và ảnh.
Thư mục `data/example/` dành cho ví dụ có nhãn minh họa, không phải kết quả thực nghiệm. Log chỉ
ra terminal, không có log file riêng. Không đưa private key/shared secret vào tài liệu hay output.

## 11. Chạy tests

```powershell
python -m pytest
```

```sh
python -m pytest
```

Pytest dùng `tests/` và import package từ `src/` theo `pyproject.toml`. Hai test ML-KEM có thể
skip nếu adapter không sẵn có; đọc phần summary để phân biệt pass/skip/fail. Khi test fail, giữ
lại traceback và báo giao diện/cấu hình liên quan; không ghi nhận test skip thành pass.

## 12. Nhánh, commit và push

Kiểm tra trạng thái trước khi thay đổi và trước khi commit:

```powershell
git status --short --branch
git switch -c feature/ten-cong-viec
git add docs/README.md
git commit -m "docs: add Vietnamese contributor guide"
git push -u origin feature/ten-cong-viec
```

```sh
git status --short --branch
git switch -c feature/ten-cong-viec
git add docs/README.md
git commit -m "docs: add Vietnamese contributor guide"
git push -u origin feature/ten-cong-viec
```

Thay `feature/ten-cong-viec` bằng nhánh của bạn và danh sách trong `git add` bằng đúng file đã
review; không copy lệnh mẫu để vô tình commit file ngoài phạm vi. Chỉ push nếu `git remote -v`
hiển thị remote đúng và bạn có quyền. Tạo pull request từ nhánh đó, ghi mục tiêu, files, tests,
giả định và người cần review. Repository được khảo sát hiện **chưa khởi tạo Git**, vì vậy các lệnh
branch/commit/push chỉ dùng sau khi repository nhóm có lịch sử và remote hợp lệ; xem
[WORKFLOW.md](WORKFLOW.md).
