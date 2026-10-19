# QKD và PQC: mô hình bảo mật và đánh đổi hệ thống

Kho mã nghiên cứu này so sánh mô phỏng BB84 ở mức giáo dục với benchmark ML-KEM-768 theo
NIST FIPS 203, đồng thời mô tả giả định bảo mật và yêu cầu triển khai của hai hướng tiếp cận.

**Câu hỏi nghiên cứu:** “QKD và PQC khác nhau như thế nào về giả định bảo mật và hiệu năng thiết
lập khóa, và yêu cầu hạ tầng ảnh hưởng ra sao đến tính phù hợp khi triển khai?”

## Dự án làm gì?

- **QKD/BB84:** mô phỏng cổ điển các bit, cơ sở đo, Eve intercept-resend, lỗi lật bit, mất tín
  hiệu Bernoulli, sifting, QBER và tỷ lệ bit được giữ lại. Đây **không phải** mô phỏng trạng thái
  lượng tử hoặc hệ thống QKD an toàn để triển khai.
- **PQC/ML-KEM-768:** nếu có đúng implementation tương thích, đo riêng key generation,
  encapsulation và decapsulation; kiểm tra hai shared secret trùng nhau. Không tự thay bằng
  thuật toán khác.
- **Phân tích:** tạo biểu đồ từ CSV thực tế và bảng so sánh ghi rõ dữ liệu đo, nhận định định tính
  và giả định. QBER và độ trễ thuật toán là hai đại lượng khác nhau, không được so sánh trực tiếp.

Không kết luận rằng QBER dưới 11% chứng minh khóa an toàn, hoặc benchmark phần mềm chứng minh PQC
luôn nhanh hơn QKD. Hệ thống QKD thực tế cần kênh cổ điển được xác thực và các bước xử lý bảo mật
khác; phạm vi hiện tại không gồm error correction, privacy amplification, finite-key proof hay
phần cứng quang học.

## Bắt đầu nhanh

Chạy từ thư mục gốc repository, với Python 3.11 trở lên.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest
python scripts/run_qkd.py
python scripts/run_qkd_experiment.py
python scripts/run_all.py
```

### Linux/macOS

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest
python scripts/run_qkd.py
python scripts/run_qkd_experiment.py
python scripts/run_all.py
```

Benchmark ML-KEM là tùy chọn. Cài thêm dependency bằng
`python -m pip install -e ".[mlkem,dev]"`, rồi chạy `python scripts/run_pqc_benchmark.py`.
Chi tiết setup, đầu vào/đầu ra và xử lý lỗi nằm trong [docs/USER_GUIDE.md](docs/USER_GUIDE.md).
Các lệnh trên chưa được xác minh trên mọi hệ điều hành hoặc mọi backend mật mã.

## Cấu trúc repository

```text
configs/                  Cấu hình thí nghiệm YAML
data/raw/                 CSV đầu ra trực tiếp (bị Git bỏ qua)
data/processed/           Bảng so sánh dẫn xuất
data/example/             Tài liệu dành cho dữ liệu minh họa có nhãn rõ ràng
docs/                     Hướng dẫn, giao thức, sơ đồ mã và quy trình nhóm
figures/                  Biểu đồ được tạo từ CSV (bị Git bỏ qua)
reports/                  Tài liệu báo cáo
scripts/                  CLI cho từng thí nghiệm, phân tích và pipeline
src/qkd_pqc/              Logic Python có thể tái sử dụng
tests/                    Unit test
```

Xem [docs/CODE_MAP.md](docs/CODE_MAP.md) để biết mỗi module thuộc workstream nào và giao diện
nào cần giữ ổn định.

## Chạy các thành phần

Mọi script cần chạy từ thư mục gốc sau khi cài package editable. Có thể thêm
`--config configs/experiment_config.yaml` cho mỗi lệnh; mặc định, code cũng dùng cấu hình đó.

| Lệnh | Mục đích | Đầu ra hiện tại |
|---|---|---|
| `python scripts/run_qkd.py` | Chạy BB84 với seed trong config | Một CSV duy nhất `data/raw/qkd_*.csv` |
| `python scripts/run_qkd_experiment.py` | Chạy repeated sweeps cho Eve, noise và loss theo config | CSV riêng cho mỗi trial trong `data/raw/` |
| `python scripts/run_pqc_benchmark.py` | Chạy đúng ML-KEM-768 nếu adapter xác minh được implementation | Một CSV `data/raw/mlkem_*.csv`; mã thoát 2 nếu không hỗ trợ |
| `python scripts/run_analysis.py` | Đọc mọi CSV `qkd_*.csv` và `mlkem_*.csv` trong thư mục raw | PNG trong `figures/`, bảng trong `data/processed/`; không có CSV thì thông báo bỏ qua |
| `python scripts/run_all.py` | Chạy BB84, thử benchmark PQC tùy chọn, phân tích đầu ra của lần chạy này | Trạng thái từng bước; mã thoát khác 0 khi bước bắt buộc hoặc phân tích lỗi |
| `python -m pytest` | Chạy unit tests | Kết quả test trong terminal |

Các script chỉ hỗ trợ cờ `--config`; hiện không có cờ CLI để thay riêng số lần lặp, seed hoặc
đường dẫn output. Hãy thay đổi file YAML (hoặc cung cấp file cấu hình khác). Đường dẫn cấu hình
tương đối được phân giải từ thư mục gốc dự án. Xem [docs/DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md)
để biết chi tiết giao diện Python và CSV.

`run_qkd.py` tạo một run cho cấu hình đơn. `run_qkd_experiment.py` chạy các sweep nhiều lần để
đánh giá QBER theo xác suất Eve/noise và tỷ lệ sifting theo loss; chỉnh số lần lặp và các danh sách
xác suất trong `qkd_sweep` của YAML. Chạy `python scripts/run_analysis.py` sau đó để vẽ trung bình
và độ lệch chuẩn từ các CSV thật. Theo policy nhóm, CSV raw/processed và PNG tự sinh bị Git bỏ qua;
chỉ đưa chúng lên GitHub khi nhóm duyệt ngoại lệ.

## Đầu ra và trạng thái

- CSV kết quả từng lần chạy được tạo với tên có run ID trong `data/raw/`; writer mở file ở chế độ
  không ghi đè. Git bỏ qua CSV tại đây.
- Phân tích tạo tên PNG cố định trong `figures/`, vì vậy lần chạy sau có thể ghi đè hình trước.
- Bảng so sánh dùng tên run ID trong `data/processed/`.
- Log hiện chỉ ghi ra terminal (stdout/stderr); không có file log được tạo.
- `run_all.py` chỉ phân tích CSV vừa tạo trong lần chạy đó; `run_analysis.py` quét mọi file khớp
  tiền tố `qkd_`/`mlkem_` trong thư mục raw.

Các chức năng đã có trong source nhưng chưa có benchmark ML-KEM thực tế đi kèm. Adapter hiện thử
API `pqcrypto.kem.ml_kem_768`; tương thích thực tế phụ thuộc phiên bản package. Trong môi trường
đã khảo sát trước đây, OpenSSL 3.4.0 không quảng bá ML-KEM trong danh sách KEM, và `pqcrypto`
không được cài. Hãy kiểm tra lại backend trên máy của bạn; không suy diễn hỗ trợ chỉ từ phiên bản
OpenSSL.

## Tài liệu

- [Hướng dẫn sử dụng từng bước](docs/USER_GUIDE.md)
- [Phân công năm thành viên](docs/TEAM_ASSIGNMENTS.md)
- [Hướng dẫn phát triển và giao diện chung](docs/DEVELOPMENT_GUIDE.md)
- [Bản đồ mã nguồn](docs/CODE_MAP.md)
- [Quy trình phối hợp bất đồng bộ](docs/WORKFLOW.md)
- [Giao thức thí nghiệm](docs/EXPERIMENT_PROTOCOL.md)
- [Từ điển dữ liệu và CSV](docs/DATA_DICTIONARY.md)
- [Khắc phục sự cố](docs/TROUBLESHOOTING.md)
- [Đóng góp vào dự án](docs/CONTRIBUTING.md) (hướng dẫn gốc: [CONTRIBUTING.md](CONTRIBUTING.md))
- [Phạm vi dự án](docs/PROJECT_SCOPE.md)
- [Mô hình đe dọa](docs/THREAT_MODEL.md)
- [Tài liệu tham khảo](docs/REFERENCES.md)
- [Báo cáo thí nghiệm BB84](reports/QKD_BB84_EXPERIMENT.md) (đang chờ review)

## Thứ tự đọc đề xuất

Thành viên mới nên bắt đầu với README này, tiếp tục [USER_GUIDE](docs/USER_GUIDE.md), sau đó đọc
[PROJECT_SCOPE](docs/PROJECT_SCOPE.md), [CODE_MAP](docs/CODE_MAP.md),
[DEVELOPMENT_GUIDE](docs/DEVELOPMENT_GUIDE.md), và
[WORKFLOW](docs/WORKFLOW.md). Đọc giao thức, từ điển dữ liệu và mô hình đe dọa trước khi phân tích
kết quả.
