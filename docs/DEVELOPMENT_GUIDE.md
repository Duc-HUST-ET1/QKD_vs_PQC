# Hướng dẫn phát triển

## Nguyên tắc Python

- Giữ cấu trúc hiện có và dùng tên hàm rõ nghĩa, type hint, docstring hữu ích.
- Tách config khỏi thuật toán; thêm validation gần nơi nhận dữ liệu không tin cậy.
- Tránh sao chép thuật toán vào script; script gọi API trong `src/qkd_pqc/`.
- Báo lỗi bằng exception/thông báo rõ; không biến lỗi thành kết quả trông hợp lệ.
- Dùng đường dẫn dựa trên `PROJECT_ROOT` hoặc đường dẫn output đã phân giải từ config; không ghi
  đường dẫn máy cá nhân vào source hoặc dữ liệu.
- Giữ seed cố định cho BB84 có thể tái lập. Không commit `.venv/`, cache, credential, private
  key, shared secret hay CSV raw.
- Đổi API/schema phải cập nhật docs và test của các consumer; không thay signature âm thầm.

Project khai báo Python `>=3.11`, package runtime `PyYAML`, `matplotlib`; extra `dev` có `pytest`,
extra `mlkem` có `pqcrypto`. Cài đặt editable theo README/USER_GUIDE.

## Giao diện và trách nhiệm module

| API | Input | Output / lỗi |
|---|---|---|
| `load_config(path=None) -> ExperimentConfig` | YAML (mặc định `configs/experiment_config.yaml`) | Dataclass đã xác thực; `ConfigurationError` nếu file/schema/giá trị sai |
| `simulate_bb84(config: QKDConfig, seed: int \| None = None) -> BB84Result` | Số tín hiệu, Eve/noise/loss/ngưỡng, seed bắt buộc | Run-level result; `ValueError` nếu tham số/seed sai |
| `write_bb84_result(result, output_dir) -> Path` | Result và thư mục | CSV duy nhất `qkd_*.csv`; báo lỗi nếu trùng tên/I/O |
| `run_qkd_experiment(config: ExperimentConfig) -> list[Path]` | Cấu hình BB84 cùng các sweep lặp | Ghi CSV per-run cho Eve, noise và loss sweeps |
| `detect_mlkem_implementation() -> MLKEMImplementation \| None` | Không tham số | Chỉ trả adapter nếu import, version, API và self-test shared secret đúng |
| `run_mlkem_benchmark(config: PQCConfig, output_dir) -> BenchmarkResults` | `ML-KEM-768`, warmup, repetitions | CSV per-sample `mlkem_*.csv`; `MLKEMUnavailableError` nếu backend vắng/sai |
| `analyze_tradeoffs(qkd_metrics=None, pqc_metrics=None) -> list[TradeoffItem]` | Mapping metric tùy chọn | Nhận định có nhãn evidence; `ValueError` với measurement không hợp lệ |
| `create_plots(qkd_csv=None, pqc_csv=None, figures_dir=None, processed_dir=None) -> list[Path]` | Một/nhiều đường dẫn CSV | Hình đã tạo; schema sai hoặc file thiếu gây exception rõ |
| `write_csv_exclusive(path, fieldnames, rows) -> Path` | Đường dẫn, header, mappings | Tạo cha directory và ghi CSV chế độ exclusive; không ghi đè |

`seed=None` được giữ trong type signature để biểu thị tham số tùy chọn ở mức Python nhưng hàm
BB84 hiện **yêu cầu** seed, nếu bỏ sẽ báo lỗi. CLI dùng `project.random_seed`. Đây là chi tiết
quan trọng khi gọi API trực tiếp.

## Cấu hình hiện hành

| Nhóm | Field | Kiểu/điều kiện |
|---|---|---|
| `project` | `name`, `random_seed` | Tên không rỗng; seed số nguyên không âm |
| `qkd` | `n_signals` | Số nguyên dương |
| `qkd` | `channel_error_rate`, `eve_probability`, `channel_loss_rate`, `qber_threshold` | Số trong [0, 1] |
| `qkd_sweep` | `repetitions` | Số nguyên dương; mặc định 10 |
| `qkd_sweep` | `eve_probabilities`, `channel_error_rates`, `channel_loss_rates` | Danh sách không rỗng; từng xác suất trong [0, 1] |
| `pqc` | `algorithm` | Bắt buộc chính xác `ML-KEM-768` |
| `pqc` | `warmup_iterations` | Số nguyên không âm |
| `pqc` | `measured_iterations` | Số nguyên dương |
| `output` | `raw_data_dir`, `processed_data_dir`, `figures_dir` | Chuỗi đường dẫn tương đối, phân giải từ project root |

Không có `openssl_provider`, path backend hoặc config API ML-KEM khác. Backend hỗ trợ trong mã
hiện tại là package `pqcrypto` với module `pqcrypto.kem.ml_kem_768`; adapter cần có callable
`generate_keypair`, `encrypt`, `decrypt`.

## CSV thực tế

### BB84: một dòng cho mỗi lần chạy

Header bắt đầu bằng các cột ổn định: `run_id, timestamp_utc, seed, n_signals,
channel_error_rate, eve_probability, qber_threshold, sifted_bits, error_bits, qber,
sifted_fraction, illustrative_status, simulator_version, python_version, platform`; bản hiện tại
nối thêm `channel_loss_rate, received_signals, lost_signals, loss_fraction`.

`qber` là tỷ lệ [0, 1], để trống nếu không có sifted bit; các xác suất/fraction nằm trong [0, 1].
`sifted_fraction=sifted_bits/n_signals`; `loss_fraction=lost_signals/n_signals`. Kết quả không
chứa bit khóa. Status `illustrative_accept`/`illustrative_reject` chỉ minh họa. Consumer cũ không
đọc các cột mới vẫn đọc được phần schema cũ; CSV lịch sử thiếu loss được xử lý như loss 0 trong
plotting.

### ML-KEM: một dòng cho mỗi mẫu timed operation

Header theo đúng thứ tự: `run_id, timestamp_utc, algorithm, operation, iteration, latency_us,
median_latency_us, p95_latency_us, public_key_bytes, secret_key_bytes, ciphertext_bytes,
shared_secret_bytes, warmup_iterations, measured_iterations, implementation,
implementation_version, platform, python_version`.

`operation` là `key_generation`, `encapsulation`, `decapsulation`; latency là microseconds. Median
là median mẫu (trung bình hai giá trị giữa nếu cỡ mẫu chẵn); p95 dùng nearest rank
`ceil(0.95*n)`. Kích thước không áp dụng để trống; nội dung key/ciphertext/secret không được ghi.

Chi tiết từng cột và provenance ở [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

## Quy ước khoa học

- QBER không phải thời gian thực thi; không vẽ chung như cùng metric.
- BB84 là mô hình bit/basis cổ điển đơn giản, không phải QKD production.
- Ngưỡng 0.11 chỉ là assumption minh họa; không chứng minh bảo mật.
- Không suy ra PQC nhanh hơn/tốt hơn mọi QKD từ benchmark primitive trên một máy.
- Gắn nhãn rõ `measured_project_data`, `qualitative_reference_based`,
  `qualitative_assumption` hoặc giới hạn phạm vi. Không dùng kết quả minh họa như số đo.
- Không bao gồm phần cứng quang học, error correction, privacy amplification, finite-key
  analysis/proof hoặc xác thực QKD hoàn chỉnh.

## Checklist trước khi gửi PR

1. Chạy `python -m pytest` trong environment dự án; ghi rõ pass/skip/fail.
2. Với docs-only: kiểm tra link và lệnh; không cần chạy benchmark.
3. Nếu sửa schema/API, cập nhật data dictionary và mọi caller/test liên quan.
4. Kiểm tra `git diff --check`, `git status`; không đưa output sinh ra hoặc `.venv` vào commit.
5. Ghi input, seed, platform/backend, phiên bản, giới hạn và nguồn tham khảo.
