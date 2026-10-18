# Phân công năm thành viên

Đây là ranh giới sở hữu ban đầu để mọi người có thể làm song song trong khoảng một tuần, không
phải quyền thay đổi giao diện chung mà không hỏi. Các giao diện hiện có và cách kiểm tra đặt tại
[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md). Thống nhất thay đổi qua issue/PR; không có thành
viên nào phải chờ họp trực tiếp để bắt đầu phần việc độc lập.

## Thành viên 1 — Mô phỏng BB84 / QKD

1. **Trách nhiệm chính:** Alice bits/bases, Eve intercept-resend, channel noise, Bob measurement,
   basis sifting, QBER, sifted fraction và CSV tái lập.
2. **File sở hữu:** `src/qkd_pqc/qkd/bb84_simulator.py`,
   `scripts/run_qkd.py`, `tests/test_bb84.py`; đề xuất thay đổi schema phải phối hợp Thành viên 5.
3. **Có thể đọc; không sửa nếu chưa trao đổi:** `config.py`, `common/`, `paths.py`,
   `scripts/run_all.py`, `docs/DATA_DICTIONARY.md`.
4. **Đầu vào/phụ thuộc:** `QKDConfig`, `project.random_seed`, helper CSV/metadata dùng chung.
5. **Đầu ra:** `BB84Result`; một `data/raw/qkd_*.csv` mới, không có nội dung bit khóa.
6. **Cách chạy:** `python scripts/run_qkd.py`; config khác dùng `--config PATH`.
7. **Cách kiểm tra:** `python -m pytest tests/test_bb84.py tests/test_csv_utils.py`.
8. **Tiêu chí nghiệm thu:** Seed cố định tái lập; zero sift xử lý an toàn; operation order và mô
   hình được ghi rõ; QBER/thống kê đúng; ngưỡng 0.11 chỉ là minh họa, không khẳng định an toàn.
9. **Phụ thuộc:** API `QKDConfig`, output `BB84Result` và CSV của Thành viên 5; API input CSV của
   Thành viên 3.
10. **Checklist:** [ ] Tái lập; [ ] noise/Eve; [ ] zero-sift; [ ] schema; [ ] test; [ ] docs.

## Thành viên 2 — Benchmark ML-KEM-768 / PQC

1. **Trách nhiệm chính:** Dùng implementation thật đúng ML-KEM-768; xác minh API, benchmark ba
   operation riêng, equality shared secret, kích thước, version/platform và CSV.
2. **File sở hữu:** `src/qkd_pqc/pqc/mlkem_benchmark.py`,
   `scripts/run_pqc_benchmark.py`, `tests/test_mlkem_benchmark.py`.
3. **Có thể đọc; không sửa nếu chưa trao đổi:** `config.py`, `common/`, `paths.py`,
   `run_all.py`, `plotting.py`, `DATA_DICTIONARY.md`.
4. **Đầu vào/phụ thuộc:** `PQCConfig`, optional `pqcrypto`; module đích hiện tại
   `pqcrypto.kem.ml_kem_768`.
5. **Đầu ra:** `BenchmarkResults`; CSV per-operation/per-iteration `data/raw/mlkem_*.csv`.
6. **Cách chạy:** `python scripts/run_pqc_benchmark.py`; capability check bằng lệnh trong
   [USER_GUIDE.md](USER_GUIDE.md).
7. **Cách kiểm tra:** `python -m pytest tests/test_mlkem_benchmark.py`; hai test có thể skip nếu
   backend vắng.
8. **Tiêu chí nghiệm thu:** Không tự thay algorithm; correctness được xác minh; đo riêng bằng
   timer monotonic; ghi median/p95/size/version/platform; timing không gồm install/I/O; unavailable
   có thông báo rõ.
9. **Phụ thuộc:** Config và output conventions của Thành viên 5; schema consumer của Thành viên 3.
10. **Checklist:** [ ] API đã xác minh; [ ] round-trip secret đúng; [ ] ba operation; [ ] đơn vị
   và metadata; [ ] test; [ ] không có số benchmark giả.

## Thành viên 3 — Phân tích và trực quan hóa

1. **Trách nhiệm chính:** Đọc CSV thật đã validate; xử lý missing/invalid; tạo biểu đồ, bảng tóm
   tắt, kiểm tra nhãn trục/đơn vị và đường dẫn.
2. **File sở hữu:** `src/qkd_pqc/analysis/plotting.py`,
   `scripts/run_analysis.py`, `tests/test_plotting.py`.
3. **Có thể đọc; không sửa nếu chưa trao đổi:** simulator/benchmark producers, schema config,
   `tradeoff_analysis.py`, `run_all.py`, `DATA_DICTIONARY.md`.
4. **Đầu vào/phụ thuộc:** CSV BB84/ML-KEM theo data dictionary; trade-off items từ Thành viên 4.
5. **Đầu ra:** PNG trong `figures/`, bảng CSV mới trong `data/processed/`; ảnh hiện có tên cố định,
   có thể ghi đè khi chạy lại.
6. **Cách chạy:** `python scripts/run_analysis.py`; script quét mọi `qkd_*.csv`/`mlkem_*.csv` trong
   raw; không có cờ input CSV hiện tại.
7. **Cách kiểm tra:** `python -m pytest tests/test_plotting.py tests/test_tradeoff_analysis.py`.
8. **Tiêu chí nghiệm thu:** Chỉ vẽ dữ liệu CSV thật; validate header/numeric/range/algorithm;
   nhãn trục và microsecond rõ; file thiếu/schema sai thông báo; không sinh điểm giả.
9. **Phụ thuộc:** Hai CSV producer của Thành viên 1/2; định dạng `TradeoffItem` Thành viên 4.
10. **Checklist:** [ ] schema đúng; [ ] missing/invalid rows; [ ] chart labels; [ ] output; [ ]
    không fake; [ ] tests.

## Thành viên 4 — Threat model, tài liệu và system trade-offs

1. **Trách nhiệm chính:** Mô tả giả định bảo mật, xác thực, QKD channels, ML-KEM computational
   basis, hạ tầng và giới hạn; gắn nguồn và nhãn evidence.
2. **File sở hữu:** `docs/THREAT_MODEL.md`, `docs/REFERENCES.md`,
   `src/qkd_pqc/system/tradeoff_analysis.py`, `tests/test_tradeoff_analysis.py`.
3. **Có thể đọc; không sửa nếu chưa trao đổi:** implementation của Thành viên 1/2, plotting,
   README, dữ liệu thí nghiệm.
4. **Đầu vào/phụ thuộc:** Tài liệu tiêu chuẩn/nguồn có thể truy xuất; metrics tùy chọn đã đo do
   producer cung cấp.
5. **Đầu ra:** `TradeoffItem` với `dimension`, `qkd`, `pqc`, `evidence_type`; threat model review.
6. **Cách chạy:** Module so sánh được gọi bởi phân tích; kiểm tra riêng bằng
   `python -m pytest tests/test_tradeoff_analysis.py`.
7. **Cách kiểm tra:** Tests validation; kiểm tra references và claim với nguồn gốc.
8. **Tiêu chí nghiệm thu:** Phân biệt qualitative/measured/assumption; nói rõ authenticated
   classical channel; không gọi ML-KEM là authentication; không bịa cost/distance/throughput.
9. **Phụ thuộc:** Hỏi Thành viên 1/2 về mô hình code; phối hợp Thành viên 3/5 về label summary.
10. **Checklist:** [ ] nguồn traceable; [ ] assumptions; [ ] giới hạn; [ ] interface typed; [ ]
    tests; [ ] review bởi thành viên khác.

## Thành viên 5 — Tích hợp, config, test và tái lập

1. **Trách nhiệm chính:** Giữ package, config, paths, CSV conventions, pipeline và điểm tích hợp
   nhất quán; review toàn hệ thống; chuẩn bị assets báo cáo.
2. **File sở hữu:** `src/qkd_pqc/config.py`, `paths.py`, `common/`,
   `scripts/run_all.py`, `pyproject.toml`, `configs/experiment_config.yaml`, test tích hợp,
   `README.md`. File được đồng sở hữu theo PR với nhóm.
3. **Có thể đọc; không sửa nếu chưa trao đổi:** Các module cốt lõi do Thành viên 1-4 sở hữu;
   không tự viết lại thuật toán để tích hợp.
4. **Đầu vào/phụ thuộc:** API producer BB84/PQC, trade-off items, interface phân tích của các
   thành viên; mọi thay đổi shared interface cần PR.
5. **Đầu ra:** Pipeline báo rõ completed/skipped/failed; config/runtime/test docs; báo cáo tái
   lập.
6. **Cách chạy:** `python scripts/run_all.py`; `python -m pytest`.
7. **Cách kiểm tra:** `python -m pytest`, import package và smoke-test nhỏ; ML-KEM có thể skipped.
8. **Tiêu chí nghiệm thu:** BB84 bắt buộc; PQC tùy chọn được skip trung thực; analysis dùng CSV
   vừa tạo trong pipeline; raw không bị overwrite; output path relative.
9. **Phụ thuộc:** Tất cả các workstream, nhưng từng thành viên có thể phát triển độc lập theo API
   đã ghi.
10. **Checklist:** [ ] config validation; [ ] CLI/status; [ ] CSV interfaces; [ ] suite; [ ]
    docs; [ ] không có output/secret vô tình commit.

## Thay đổi dùng chung và bàn giao

`config.py`, `paths.py`, `common/`, config YAML, `run_all.py`, README, CSV schemas và interface
package là shared surface. PR sửa các vùng này phải ghi rõ consumer bị tác động và được owner của
các consumer review. Khi task kết thúc, cập nhật checklist và lưu lệnh/result test thực tế; không
đánh dấu benchmark chưa chạy là hoàn tất.
