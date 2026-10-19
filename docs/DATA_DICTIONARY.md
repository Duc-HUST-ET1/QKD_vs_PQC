# Từ điển cấu hình và dữ liệu

CSV là UTF-8, có header. Trường rỗng nghĩa là không áp dụng/không có dữ liệu, không phải số 0.
Dữ liệu chạy thực nằm ở `data/raw/`; bảng dẫn xuất ở `data/processed/`; ví dụ phải có nhãn và
nằm riêng trong `data/example/`.

## Cấu hình YAML

| Khóa | Kiểu | Mặc định | Quy tắc hiện tại |
|---|---|---:|---|
| `project.name` | chuỗi | `QKD vs PQC` | Không rỗng |
| `project.random_seed` | số nguyên | `42` | Không âm; dùng cho BB84 |
| `qkd.n_signals` | số nguyên | `100000` | Lớn hơn 0 |
| `qkd.channel_error_rate` | xác suất | `0.01` | [0, 1] |
| `qkd.eve_probability` | xác suất | `0.0` | [0, 1] |
| `qkd.qber_threshold` | xác suất | `0.11` | [0, 1], chỉ ngưỡng minh họa |
| `qkd.channel_loss_rate` | xác suất | `0.0` | [0, 1], tín hiệu mất trước khi tới Bob |
| `qkd_sweep.repetitions` | số nguyên | `10` | Số lần chạy độc lập mỗi điểm |
| `qkd_sweep.eve_probabilities` | danh sách xác suất | `[0, 0.1, 0.25, 0.5, 0.75, 1]` | Mỗi giá trị trong [0, 1] |
| `qkd_sweep.channel_error_rates` | danh sách xác suất | `[0, 0.01, 0.05, 0.1, 0.2]` | Mỗi giá trị trong [0, 1] |
| `qkd_sweep.channel_loss_rates` | danh sách xác suất | `[0, 0.1, 0.3, 0.5, 0.8]` | Mỗi giá trị trong [0, 1] |
| `pqc.algorithm` | chuỗi | `ML-KEM-768` | Bắt buộc đúng chuỗi này |
| `pqc.warmup_iterations` | số nguyên | `50` | Không âm |
| `pqc.measured_iterations` | số nguyên | `1000` | Lớn hơn 0 |
| `output.raw_data_dir` | đường dẫn tương đối | `data/raw` | Phân giải từ project root |
| `output.processed_data_dir` | đường dẫn tương đối | `data/processed` | Phân giải từ project root |
| `output.figures_dir` | đường dẫn tương đối | `figures` | Phân giải từ project root |

Config thay thế truyền vào `--config PATH`; path tương đối cũng phân giải từ gốc project, không
phải từ vị trí YAML.

## CSV kết quả BB84

Mỗi row là một lần chạy. Header theo đúng thứ tự code:

```text
run_id,timestamp_utc,seed,n_signals,channel_error_rate,eve_probability,qber_threshold,sifted_bits,error_bits,qber,sifted_fraction,illustrative_status,simulator_version,python_version,platform
```

Các cột tương thích được nối thêm sau header cũ:

```text
channel_loss_rate,received_signals,lost_signals,loss_fraction
```

| Cột | Kiểu/đơn vị | Ý nghĩa |
|---|---|---|
| `run_id` | chuỗi | ID duy nhất có tiền tố `qkd_` |
| `timestamp_utc` | ISO datetime | Thời điểm sinh run |
| `seed` | số nguyên | Seed của Python `random.Random` |
| `n_signals` | số nguyên | Tổng tín hiệu mô phỏng |
| `channel_error_rate` | xác suất [0,1] | Cấu hình lỗi lật bit độc lập |
| `eve_probability` | xác suất [0,1] | Xác suất intercept từng tín hiệu |
| `qber_threshold` | xác suất [0,1] | Ngưỡng dạy học cấu hình |
| `sifted_bits` | số nguyên | Số vị trí Alice/Bob có basis khớp |
| `error_bits` | số nguyên | Mismatch trong sifted positions |
| `qber` | tỷ lệ [0,1] | `error_bits / sifted_bits`; rỗng khi sifted bằng 0 |
| `sifted_fraction` | tỷ lệ [0,1] | `sifted_bits / n_signals` |
| `illustrative_status` | chuỗi enum | `illustrative_accept` hoặc `illustrative_reject`; không phải phán quyết an toàn |
| `simulator_version` | chuỗi | Phiên bản package mô phỏng |
| `python_version` | chuỗi | Phiên bản Python runtime |
| `platform` | chuỗi | Thông tin platform runtime |
| `channel_loss_rate` | xác suất [0,1] | Xác suất một tín hiệu mất trước khi tới Bob |
| `received_signals` | số nguyên | Số tín hiệu đến được Bob; Eve chỉ có thể chặn các tín hiệu này |
| `lost_signals` | số nguyên | `n_signals - received_signals`; mất tín hiệu không được tính là lỗi bit |
| `loss_fraction` | tỷ lệ [0,1] | `lost_signals / n_signals` |

CSV không lưu seed riêng cho từng signal hay bit khóa; seed và tham số cho phép chạy lại thống kê
với code version tương ứng. Các cột loss được nối thêm để giữ nguyên tên và thứ tự của các cột cũ;
consumer chỉ đọc header cũ vẫn có thể đọc file mới. File lịch sử thiếu các cột loss được xem như
không khai báo loss khi phân tích tương thích ngược.

## CSV benchmark ML-KEM-768

Mỗi row là một timed sample; ba operation tên chính xác là `key_generation`, `encapsulation`,
`decapsulation`. Header code:

```text
run_id,timestamp_utc,algorithm,operation,iteration,latency_us,median_latency_us,p95_latency_us,public_key_bytes,secret_key_bytes,ciphertext_bytes,shared_secret_bytes,warmup_iterations,measured_iterations,implementation,implementation_version,platform,python_version
```

| Cột | Kiểu/đơn vị | Ý nghĩa |
|---|---|---|
| `run_id` | chuỗi | ID duy nhất có tiền tố `mlkem_` |
| `timestamp_utc` | ISO datetime | Thời gian bắt đầu ghi kết quả |
| `algorithm` | chuỗi | Hiện chỉ `ML-KEM-768` |
| `operation` | chuỗi enum | Operation được đo |
| `iteration` | số nguyên | Sample đo, bắt đầu từ 1 cho từng operation |
| `latency_us` | microsecond | Thời gian một operation |
| `median_latency_us` | microsecond | Median của các mẫu cùng operation |
| `p95_latency_us` | microsecond | Nearest-rank p95, rank `ceil(0.95*n)` |
| `public_key_bytes` | byte | Chiều dài public key nếu có/áp dụng |
| `secret_key_bytes` | byte | Chiều dài secret key nếu có/áp dụng |
| `ciphertext_bytes` | byte | Chiều dài ciphertext nếu có/áp dụng |
| `shared_secret_bytes` | byte | Chiều dài shared secret, không phải nội dung |
| `warmup_iterations` | số nguyên | Số lần warm-up cho mỗi operation |
| `measured_iterations` | số nguyên | Số mẫu đo cho mỗi operation |
| `implementation` | chuỗi | Hiện `pqcrypto (pqcrypto.kem.ml_kem_768)` |
| `implementation_version` | chuỗi | Version phân phối `pqcrypto` |
| `platform` | chuỗi | Platform runtime |
| `python_version` | chuỗi | Phiên bản Python runtime |

Kích thước không liên quan để trống. Không xuất key, ciphertext hay shared-secret content. Timing
dùng `perf_counter_ns()` rồi chuyển thành microsecond; cài package, correctness verification và
file I/O không nằm trong vùng đo.

## Bảng comparison đã xử lý

Header: `dimension,qkd,pqc,evidence_type`.

`evidence_type` phân biệt `qualitative_reference_based`, `qualitative_assumption`,
`project_scope_limit`, `measured_project_data`. Từng measurement được truyền từ CSV vào bảng và
phải giữ provenance; “not applicable” không đồng nghĩa bằng 0. Với QKD CSV chỉ có một setting,
bảng có thể ghi các mean measurement; nếu có nhiều setting, chỉ ghi `valid_run_rows`,
`measurement_scope` và `setting_count`, không gộp các kịch bản thành một mean khó diễn giải.

## Tên file và ghi nhận không khả dụng

- Raw QKD: `qkd_<UTC timestamp>_<id>.csv`
- Raw ML-KEM: `mlkem_<UTC timestamp>_<id>.csv`
- Comparison: `comparison_<UTC timestamp>_<id>.csv`
- Figures: tên tĩnh theo chart trong `figures/` (có thể bị ghi đè)

Raw/processed CSV và hình sinh tự động bị `.gitignore` bỏ qua theo quy ước repository; không
commit chúng nếu chưa được nhóm duyệt ngoại lệ. Báo cáo có thể ghi số liệu quan sát được cùng
run ID/seed để người khác đối chiếu output local.

Writer raw mở exclusive, không ghi đè file cùng tên. Nếu ML-KEM không khả dụng, không tạo CSV số
đo; lưu thông tin lỗi trong issue/PR hoặc báo cáo theo dạng chữ và gắn trạng thái “unavailable”,
không tạo dòng CSV giả.
