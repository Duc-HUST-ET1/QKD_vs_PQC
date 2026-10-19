# Giao thức thí nghiệm

## Cấu hình, provenance và output

Config mặc định là `configs/experiment_config.yaml`; CLI nhận `--config PATH` (đường dẫn tương
đối tính từ project root). Chạy từ root sau khi cài package editable. Giá trị mặc định:

- `project.random_seed=42`
- BB84 một lần: `n_signals=100000`, `channel_error_rate=0.01`, `eve_probability=0.0`,
  `channel_loss_rate=0.0`, `qber_threshold=0.11`
- BB84 sweeps: 10 independent repetitions per setting; Eve `[0, 0.1, 0.25, 0.5, 0.75, 1]`,
  channel noise `[0, 0.01, 0.05, 0.1, 0.2]`, loss `[0, 0.1, 0.3, 0.5, 0.8]`
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
2. Với xác suất `channel_loss_rate`, tín hiệu bị mất và không tới Bob; tín hiệu mất không được
   tính là lỗi. Đây là loss Bernoulli độc lập, không phải mô hình optical channel.
3. Với xác suất `eve_probability`, Eve chặn từng tín hiệu còn lại, chọn basis ngẫu nhiên độc lập,
   đo: basis trùng Alice thì bit đo bằng bit Alice; basis khác thì kết quả bit là ngẫu nhiên. Eve
   gửi trạng thái bit/basis vừa đo lại.
4. Với xác suất `channel_error_rate`, channel lật bit logic được truyền một lần, độc lập với
   loss và Eve.
5. Bob chọn basis ngẫu nhiên; nếu trùng basis truyền, nhận bit truyền; nếu khác, kết quả đo là
   ngẫu nhiên.
6. Chỉ các tín hiệu đã đến Bob có basis Bob trùng basis Alice mới được sift. Mã đếm số đã nhận,
   sifted bits và mismatch.

`qber = error_bits / sifted_bits`; `sifted_fraction = sifted_bits / n_signals`. Nếu không có bit
được sift, QBER là `None`, CSV để rỗng, và status là `illustrative_reject`. Các status còn lại
dựa vào `qber > qber_threshold`; nhãn `illustrative_accept` không phải kết luận an toàn.

`loss_fraction = lost_signals / n_signals`. Khi loss độc lập với basis/bit, giá trị kỳ vọng của
sifted fraction là xấp xỉ `(1 - channel_loss_rate) / 2`. Trong mô hình độc lập hiện tại, kỳ vọng
QBER trên sifted bits là `e + (1 - 2e) * p_eve / 4`, với `e=channel_error_rate`; riêng noise
không Eve có QBER kỳ vọng `e`, và Eve intercept-resend toàn phần không noise có QBER kỳ vọng 25%.
Đây là kỳ vọng lý thuyết, không phải giá trị áp đặt lên dữ liệu.

Đây là mô hình cổ điển của lựa chọn bit/basis, không phải trạng thái lượng tử. `channel_loss_rate`
chỉ là phép thử Bernoulli ở mức logic, không mô phỏng suy hao quang học hoặc detector. Mô hình
không có phần cứng, device side-channel, error correction, privacy amplification hay finite-key proof.
Ngưỡng 11% là giá trị dạy học tùy cấu hình, không phải ngưỡng bảo đảm bảo mật tổng quát. Thí
nghiệm cần QKD thực tế phải có authenticated classical channel và quy trình hậu xử lý phù hợp.

Lệnh: `python scripts/run_qkd.py [--config PATH]`. Đầu ra là một row trong
`data/raw/qkd_*.csv`; output không bao gồm các bit khóa. Mỗi file ghi thêm loss rate, số tín hiệu
đã nhận/mất và loss fraction sau các cột BB84 cũ.

## Experiment A2 — BB84 repeated sweeps

Lệnh `python scripts/run_qkd_experiment.py [--config PATH]` chạy ba sweep độc lập: Eve (noise/loss
đặt 0), channel noise (Eve/loss đặt 0), và channel loss (Eve/noise đặt 0). Mỗi setting nhận số lần
lặp tại `qkd_sweep.repetitions`. Seed bắt đầu từ `project.random_seed`, sau đó được tăng duy nhất
cho từng trial; mọi seed và tham số được ghi trong CSV per-run. Những tổ hợp trùng nhau như
baseline `[0,0,0]` chỉ chạy một lần cho mỗi repetition. Do đó cùng config và code tạo lại cùng các
thống kê, nhưng run ID/timestamp mới.

`python scripts/run_analysis.py` tổng hợp các run CSV thành mean và sample standard deviation
(error bar ±1 SD) tại từng xác suất, lọc để các yếu tố khác ngoài sweep bằng 0. Nó tạo QBER theo
Eve, QBER theo channel noise, sifted fraction theo noise và sifted fraction theo loss. Các output
sinh tự động ở `data/raw/`, `data/processed/`, `figures/` bị `.gitignore` bỏ qua theo policy nhóm;
không commit nếu chưa được nhóm duyệt. Nhiều file có cùng seed, cấu hình và phiên bản mô phỏng chỉ
được tính một lần; chạy lại cùng seed không tạo thêm một mẫu thống kê độc lập.
Comparison CSV không gộp mean QBER/sifting/loss qua các cấu hình khác nhau; với dữ liệu nhiều setting,
nó ghi `measurement_scope` và `setting_count`, còn số liệu theo điều kiện được xem trong từng biểu đồ
và run CSV.
Kết quả batch đã quan sát được và các giới hạn được ghi tại
[reports/QKD_BB84_EXPERIMENT.md](../reports/QKD_BB84_EXPERIMENT.md); báo cáo đang chờ review.

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
  thư mục raw được cấu hình; `--qkd-run-prefix PREFIX` chỉ giới hạn CSV QKD theo prefix run ID
  nhưng vẫn giữ cách phân tích tương thích.
- `python scripts/run_all.py [--config PATH]` chạy BB84, thử PQC tùy chọn, sau đó chỉ phân tích
  CSV từ chính lượt chạy hiện tại.
- Figures được ghi trong `figures/` với tên cố định; chạy lại có thể ghi đè PNG.
- Bảng comparison được lưu tên mới trong `data/processed/`.
- Không có CSV: script analysis thông báo skip, không tạo dữ liệu giả. Lỗi schema/file được báo.

Muốn tái lập hình, giữ nguyên CSV raw cùng config và chạy lại `run_analysis.py`. Xem
[DATA_DICTIONARY.md](DATA_DICTIONARY.md) về columns, missing values và đơn vị.
