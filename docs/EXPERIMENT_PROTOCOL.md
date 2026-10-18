# Giao thức thí nghiệm

## Cấu hình, provenance và output

Config mặc định là `configs/experiment_config.yaml`; CLI nhận `--config PATH` (đường dẫn tương
đối tính từ project root). Chạy từ root sau khi cài package editable. Giá trị mặc định:

- `project.random_seed=42`
- BB84: `n_signals=100000`, `channel_error_rate=0.01`, `eve_probability=0.0`,
  `qber_threshold=0.11`
- PQC: `algorithm=ML-KEM-768`, `warmup_iterations=50`, `measured_iterations=1000`
- Output: `data/raw`, `data/processed`, `figures`

Config được kiểm tra bởi `load_config()`. BB84 dùng `random.Random(seed)`; cùng config và seed sẽ
cho cùng thống kê nhưng run ID/timestamp mới. Seed benchmark ML-KEM không được cấu hình/ghi trong
project; không tuyên bố rằng nó tái lập giống nhau qua môi trường.

Writer tạo run ID có timestamp UTC và phần ngẫu nhiên; file CSV mới được mở exclusive nên không
ghi đè. Metadata ghi Python và platform; CSV PQC ghi implementation/version. File raw là dữ liệu
gốc; bảng `data/processed/` và hình là dẫn xuất. `.gitignore` bỏ qua CSV raw/processed và ảnh.
Pipeline không tạo log file; stdout/stderr là nơi xem trạng thái.

## Experiment A — BB84 đơn giản hóa

Hàm thực thi: `simulate_bb84(config: QKDConfig, seed: int | None = None) -> BB84Result`. Dù type
ghi `seed` có thể None, hàm hiện yêu cầu seed không âm; CLI truyền `project.random_seed`.

Với từng tín hiệu, code thực hiện theo thứ tự:

1. Alice sinh bit ngẫu nhiên và basis nhị phân ngẫu nhiên.
2. Với xác suất `eve_probability`, Eve chặn tín hiệu, chọn basis ngẫu nhiên. Nếu basis khớp,
   measurement bit bằng Alice; nếu lệch, bit là ngẫu nhiên. Eve gửi lại bit và basis vừa đo.
3. Với xác suất `channel_error_rate`, channel lật transmitted bit.
4. Bob chọn basis ngẫu nhiên; nếu trùng transmitted basis, kết quả bằng bit truyền, ngược lại
   code sinh bit đo ngẫu nhiên.
5. Chỉ vị trí Bob basis trùng Alice basis được sift. Mã đếm sifted bits và mismatch.

`qber = error_bits / sifted_bits`; `sifted_fraction = sifted_bits / n_signals`. Nếu không có bit
được sift, QBER là `None`, CSV để rỗng, và status là `illustrative_reject`. Các status còn lại
dựa vào `qber > qber_threshold`; nhãn `illustrative_accept` không phải kết luận an toàn.

Đây là mô hình cổ điển của lựa chọn bit/basis, không phải trạng thái lượng tử. Không có phần cứng,
optical loss, device side-channel, error correction, privacy amplification hay finite-key proof.
Ngưỡng 11% là giá trị dạy học tùy cấu hình, không phải ngưỡng bảo đảm bảo mật tổng quát. Thí
nghiệm cần QKD thực tế phải có authenticated classical channel và quy trình hậu xử lý phù hợp.

Lệnh: `python scripts/run_qkd.py [--config PATH]`. Đầu ra là một row trong
`data/raw/qkd_*.csv`; output không bao gồm các bit khóa.

## Experiment B — ML-KEM-768

Implementation được adapter hiện hỗ trợ là module `pqcrypto.kem.ml_kem_768` với các hàm
`generate_keypair`, `encrypt`, `decrypt`. Capability check xác minh package version, các hàm
callable, chạy round-trip, và xác nhận shared secret đúng. Nếu bất kỳ bước nào không đạt, adapter
không báo sẵn sàng; không tự dùng algorithm khác.

Mỗi warm-up iteration gọi keygen, encapsulation và decapsulation một lần, rồi kiểm tra shared
secret; warm-up không được ghi vào CSV. Mỗi measured iteration:

1. Đo riêng `generate_keypair()`.
2. Đo riêng `encrypt(public_key)` để tạo ciphertext/shared secret.
3. Đo riêng `decrypt(secret_key, ciphertext)` rồi kiểm tra equality sau khi timer dừng.

Timer là `time.perf_counter_ns()`, chia 1,000 để báo microseconds. Timing không bao gồm ghi file.
Key/ciphertext được tạo trong measured iteration; keygen cũng là operation timed riêng trong
cùng vòng iteration. Không benchmark subprocess OpenSSL. Median lấy theo mẫu; p95 dùng nearest
rank `ceil(0.95*n)`. Mã lưu từng latency sample; không chỉ lưu một row trung bình.

Output `data/raw/mlkem_*.csv` có `run_id`, timestamp UTC, operation/sample, median/p95, kích thước
byte áp dụng, warmup/repetition count, implementation/version, platform và Python version. Dữ
liệu bí mật không được xuất. Nếu thư viện vắng hoặc không tương thích, `run_pqc_benchmark.py` trả
mã 2 và không tạo benchmark CSV; ghi nhận trạng thái đó là “unavailable/skipped”, không phải số
đo.

## Experiment C — so sánh hệ thống định tính

`analyze_tradeoffs()` tạo các chiều security basis, key establishment, quantum adversary,
authentication, infrastructure, deployment và limits. Claim định tính gắn nhãn
`qualitative_reference_based`, `qualitative_assumption` hoặc `project_scope_limit`; metric chỉ
được thêm khi caller đưa vào và gắn `measured_project_data`.

Không có số cost, range, throughput thực địa của repository. Không diễn giải QBER như latency và
không kết luận benchmark primitive chứng minh PQC nói chung nhanh hơn QKD.

## Phân tích và tái lập hình

- `python scripts/run_analysis.py [--config PATH]` tìm tất cả `qkd_*.csv`, `mlkem_*.csv` trong
  thư mục raw được cấu hình.
- `python scripts/run_all.py [--config PATH]` chạy BB84, thử PQC tùy chọn, sau đó chỉ phân tích
  CSV từ chính lượt chạy hiện tại.
- Figures được ghi trong `figures/` với tên cố định; chạy lại có thể ghi đè PNG.
- Bảng comparison được lưu tên mới trong `data/processed/`.
- Không có CSV: script analysis thông báo skip, không tạo dữ liệu giả. Lỗi schema/file được báo.

Muốn tái lập hình, giữ nguyên CSV raw cùng config và chạy lại `run_analysis.py`. Xem
[DATA_DICTIONARY.md](DATA_DICTIONARY.md) về columns, missing values và đơn vị.
