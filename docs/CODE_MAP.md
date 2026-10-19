# Bản đồ mã nguồn

## Cây thư mục hiện có

```text
configs/experiment_config.yaml
data/example/README.md
data/processed/.gitkeep
data/raw/.gitkeep
docs/
figures/.gitkeep
reports/README.md
scripts/run_all.py
scripts/run_analysis.py
scripts/run_pqc_benchmark.py
scripts/run_qkd.py
scripts/run_qkd_experiment.py
src/qkd_pqc/
  analysis/plotting.py
  common/csv_utils.py
  common/metadata.py
  config.py
  paths.py
  pqc/mlkem_benchmark.py
  qkd/bb84_simulator.py
  qkd/experiment.py
  system/tradeoff_analysis.py
tests/test_bb84.py
tests/test_qkd_experiment.py
tests/test_config.py
tests/test_csv_utils.py
tests/test_mlkem_benchmark.py
tests/test_plotting.py
tests/test_tradeoff_analysis.py
```

## Quy ước thư mục

| Đường dẫn | Mục đích | Không nên đặt ở đây |
|---|---|---|
| `src/` | Logic có thể import, tái sử dụng và kiểm thử; module gọi module qua API đã thống nhất | Mã điều phối CLI riêng, cấu hình máy cá nhân, dữ liệu kết quả |
| `scripts/` | Đọc tham số CLI, gọi hàm trong `src/`, báo trạng thái và mã thoát | Bản sao thuật toán đã có trong package |
| `configs/` | Giá trị thí nghiệm trong YAML, có validation ở `config.py` | Hằng số cấu hình rải rác trong mã |
| `data/raw/` | CSV ban đầu do thí nghiệm tạo; không chỉnh tay, tên run độc nhất | Ví dụ giả lập, file bí mật |
| `data/processed/` | Bảng phân tích/tổng hợp dẫn xuất từ raw | Dữ liệu gốc không biến đổi |
| `data/example/` | Ví dụ được đánh dấu rõ là minh họa | Kết quả được trình bày như số đo |
| `figures/` | PNG sinh từ CSV thực tế | Biểu đồ có điểm bịa hoặc nhập thủ công |
| `tests/` | Unit test cho validation, API và kết quả xác định | Benchmark nặng trong test mặc định |
| `docs/` | Hướng dẫn cho team, protocol, threat model, từ điển dữ liệu | Mã thực thi |
| `reports/` | Tài liệu báo cáo đã được team xem xét | CSV raw hoặc cache sinh tự động |

## Bản đồ file và quyền sở hữu ban đầu

Quyền sở hữu là ranh giới phối hợp, không phải quyền sửa đơn phương giao diện dùng chung. Người
phụ trách có thể đọc toàn bộ repository; hãy yêu cầu review/đồng ý trước khi đổi API hoặc schema
do workstream khác cung cấp.

| Thành phần | Vai trò, đầu vào/đầu ra và phụ thuộc | Owner / quyền sửa |
|---|---|---|
| `src/qkd_pqc/qkd/bb84_simulator.py` | Mô phỏng seeded BB84 rút gọn có Eve, noise, loss; vào `QKDConfig`, seed; ra `BB84Result` và CSV qua writer | Thành viên 1; người khác chỉ sửa khi phối hợp |
| `src/qkd_pqc/qkd/experiment.py`, `scripts/run_qkd_experiment.py` | Repeated Eve/noise/loss sweeps; mỗi trial ghi một CSV run-level | Thành viên 1; config sweep trong schema chung cần review Thành viên 5 |
| `tests/test_qkd_experiment.py` | Kiểm tra sweep tạo các trial có cấu hình/seed tách biệt | Thành viên 1 |
| `scripts/run_qkd.py` | CLI gọi config và BB84, ghi trạng thái | Thành viên 1; sửa pipeline chung cần báo Thành viên 5 |
| `src/qkd_pqc/pqc/mlkem_benchmark.py` | Capability detection `pqcrypto.kem.ml_kem_768`, correctness, timings, CSV | Thành viên 2; tuyệt đối không đổi thuật toán ngầm |
| `scripts/run_pqc_benchmark.py` | CLI tùy chọn benchmark, mã 2 khi không sẵn implementation | Thành viên 2 |
| `src/qkd_pqc/analysis/plotting.py` | Đọc và kiểm tra CSV, vẽ QKD/PQC, ghi bảng comparison | Thành viên 3 |
| `scripts/run_analysis.py` | Tìm các CSV theo tiền tố trong raw, gọi phân tích | Thành viên 3 |
| `src/qkd_pqc/system/tradeoff_analysis.py` | `TradeoffItem`, nhận định định tính và metric cung cấp | Thành viên 4 |
| `docs/THREAT_MODEL.md`, `docs/REFERENCES.md` | Giả định, giới hạn bảo mật và nguồn | Thành viên 4, phối hợp nội dung |
| `src/qkd_pqc/config.py` | Dataclass và validation YAML | Thành viên 5 quản lý; schema dùng chung, cần PR |
| `src/qkd_pqc/paths.py` | `PROJECT_ROOT`, phân giải đường dẫn tương đối | Thành viên 5 quản lý |
| `src/qkd_pqc/common/csv_utils.py` | Writer CSV exclusive, không ghi đè file đích | Thành viên 5 quản lý |
| `src/qkd_pqc/common/metadata.py` | Run ID/time UTC và metadata Python/platform | Thành viên 5 quản lý |
| `scripts/run_all.py` | Điều phối BB84, benchmark tùy chọn, phân tích kết quả của chính lượt đó | Thành viên 5 |
| `tests/`, `pyproject.toml`, `configs/` | Test chung, cài đặt, config dùng chung | Thành viên 5 điều phối; sửa chung qua PR |
| `README.md` | Điểm vào chung cho người dùng | Thành viên 5 điều phối; nội dung chuyên môn cần owner review |
| `docs/USER_GUIDE.md`, `CODE_MAP.md`, `WORKFLOW.md`, `DEVELOPMENT_GUIDE.md`, `TROUBLESHOOTING.md`, `CONTRIBUTING.md` | Hướng dẫn cộng tác và onboarding | Cả nhóm đóng góp qua PR |

Các file còn lại trong `docs/` mô tả dự án/protocol/schema; khi thay đổi giao thức hoặc schema,
owner code liên quan phải đề xuất cập nhật tài liệu cùng PR.

## Các giao diện quan trọng

- `load_config(path: str | Path | None = None) -> ExperimentConfig`
- `simulate_bb84(config: QKDConfig, seed: int | None = None) -> BB84Result`
- `write_bb84_result(result: BB84Result, output_dir: str | Path) -> Path`
- `detect_mlkem_implementation() -> MLKEMImplementation | None`
- `run_mlkem_benchmark(config: PQCConfig, output_dir: str | Path) -> BenchmarkResults`
- `analyze_tradeoffs(qkd_metrics: Mapping | None = None, pqc_metrics: Mapping | None = None) -> list[TradeoffItem]`
- `create_plots(qkd_csv=None, pqc_csv=None, figures_dir=None, processed_dir=None) -> list[Path]`
- `write_csv_exclusive(path, fieldnames, rows) -> Path`

Đây là signature hiện có; thay đổi cần cập nhật caller, tests và tài liệu trong cùng pull request.
Script là entry point; thuật toán chỉ nên nằm trong `src/` một lần.

## Phần dự kiến nhưng chưa có

Không có thư mục `src/qkd/` hoặc `src/pqc/` ở repository hiện tại; package thực tế là
`src/qkd_pqc/qkd/` và `src/qkd_pqc/pqc/`. Chưa có CLI riêng để chọn CSV input, thay seed trực tiếp,
hoặc chọn output directory; chưa có file log và chưa có benchmark ML-KEM đã thu thập trong repo.
