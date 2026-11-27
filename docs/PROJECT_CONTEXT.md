# Ngữ cảnh tiếp quản QKD_vs_PQC

**Cập nhật ngày 27/11/2026 cho Nhóm 12, học phần Lý thuyết mật mã, Đại học Bách khoa Hà Nội.** Đề tài *Quantum Key Distribution versus Post-Quantum Cryptography: Security Models and System Trade-offs* xem xét ba câu hỏi liên quan đến giả định bảo mật, hiệu năng có thể đo khi thiết lập khóa và yêu cầu hạ tầng triển khai. Repository cung cấp một mô phỏng BB84 cổ điển và một benchmark primitive ML-KEM-768. Đọc [quy tắc làm việc](../AGENTS.md), [phạm vi](PROJECT_SCOPE.md) và [mốc tuần 11](PROGRESS_LOG.md) trước khi tiếp tục.

## Nhóm và phân công

Trang bìa báo cáo tuần 1 của Nhóm 12 ghi Trần Anh Đức, Đỗ Phương Điệp, Vũ Việt Thiện, Đào Ngọc Tuấn Linh và Trần Xuân Kiên. Tài liệu phân công trong repository dùng số thành viên. Chưa có bảng ghép tên với số thành viên được xác nhận trong các nguồn trên. Dùng vai trò dưới đây để bàn giao. [Phân công và phạm vi sở hữu file](TEAM_ASSIGNMENTS.md)

| Thành viên | Đầu việc | Đầu ra chịu trách nhiệm |
|---|---|---|
| 1 | BB84 và sweep | Mô hình Eve, noise, loss, seed, QBER, sifting và CSV mỗi trial |
| 2 | ML-KEM-768 | Adapter, kiểm tra shared secret và mẫu latency cho ba thao tác |
| 3 | Phân tích dữ liệu | Chọn đúng tập run, vẽ hình, lập bảng, đối chiếu số liệu |
| 4 | Threat model và trade-offs | Kiểm tra giả định, nguồn học thuật và giới hạn của từng kết luận |
| 5 | Tích hợp và tái lập | Config, schema dùng chung, pipeline, test và bằng chứng bàn giao |

## Luồng thực thi và dữ liệu

| Thành phần | Vai trò trong một lần chạy |
|---|---|
| `configs/experiment_config.yaml`, `src/qkd_pqc/config.py`, `paths.py` | Nạp và kiểm tra cấu hình, giải đường dẫn trong repo |
| `scripts/run_qkd.py`, `run_qkd_experiment.py` → `src/qkd_pqc/qkd/` | Chạy đơn hoặc sweep theo từng trục. Mặc định seed 42, 100.000 tín hiệu, noise 0,01, Eve/loss 0, ngưỡng 0,11. Sweep mặc định có 14 setting riêng biệt × 10 lần |
| `scripts/run_pqc_benchmark.py` → `src/qkd_pqc/pqc/mlkem_benchmark.py` | Kiểm tra backend, đo riêng key generation, encapsulation và decapsulation. Mặc định 50 vòng warm-up, 1.000 mẫu/thao tác |
| `src/qkd_pqc/common/`, `data/raw/` | Ghi CSV mới, run ID và metadata UTC. BB84 có một dòng/run, ML-KEM có một dòng/mẫu |
| `scripts/run_all.py`, `scripts/run_analysis.py` | Pipeline phân tích danh sách CSV của lượt chạy, có cờ `--sweep`. Script phân tích độc lập quét các CSV hiện có, cờ `--qkd-run-prefix` chỉ lọc BB84 |
| `src/qkd_pqc/analysis/plotting.py`, `system/tradeoff_analysis.py` | Đọc CSV, tổng hợp số liệu và ghép nhận định định tính vào `data/processed/`. Xuất PNG tên cố định vào `figures/` |
| `tests/`, `docs/`, `reports/` | Test đơn vị và tích hợp, giao thức thí nghiệm và báo cáo theo thời điểm. Xem [từ điển dữ liệu](DATA_DICTIONARY.md) và [giao thức](EXPERIMENT_PROTOCOL.md) |

**Môi trường.** Package yêu cầu Python ≥3.11, PyYAML và Matplotlib. Extras `dev` và `mlkem` khai báo pytest và pqcrypto. Checkout ngày 27/11 có venv Python 3.13.14 trên Windows, PyYAML 6.0.3, Matplotlib 3.11.2, pytest 9.1.1 và pqcrypto 0.4.0. Tests dùng Agg. Adapter tại HEAD yêu cầu `keygen/encaps/decaps`, còn module 0.4.0 cài ở đây xuất `generate_keypair/encrypt/decrypt`. Việc có package trên đĩa chưa đủ để xác nhận backend chạy với HEAD. [Khai báo môi trường](../pyproject.toml)

## Git và trạng thái tích hợp tại ngày 27/11

- Checkout và ref cục bộ `origin/feature/system-tradeoffs` cùng ở `66e687c`. Local `main` và `origin/main` vẫn ở `024669e` (PR #9). Khi bắt đầu rà soát, worktree đã có thay đổi ở `figures/mlkem_latency_cdf.png`.
- GitHub ghi PR #1–#10 đã merge, danh sách không có PR mở khi kiểm tra. Remote `main` ở `c8166f7`, merge PR #10 ngày 24/11 với head `0b2eff5`. Commit nội dung của PR thay ba PNG. Các tuyên bố về sửa mã trong mô tả PR cần đối chiếu với diff. [PR #10](https://github.com/Duc-HUST-ET1/QKD_vs_PQC/pull/10)
- Remote `feature/qkd` ở `146687f`, đi trước remote main một commit. Nhánh này lưu báo cáo 24/11, mã tách timing BB84 theo run ID, phân nhóm ML-KEM theo môi trường, khử trùng mẫu, đổi nhãn BB84 và test hồi quy. Checkout hiện tại chưa chứa các sửa đổi đó. [Diff so với main](https://github.com/Duc-HUST-ET1/QKD_vs_PQC/compare/c8166f7...146687f)
- Remote `feature/system-tradeoffs` ở `66e687c`. Commit này gỡ 21 đường dẫn `.pytest-tmp/` khỏi Git trên nhánh ngày 27/11, sau head của PR #10. Trên checkout hiện tại Git theo dõi 4 comparison CSV và 4 PNG. Raw CSV, bảng mới và hình sinh thêm mặc định bị ignore. Clone mới cần nguồn dữ liệu riêng để kiểm lại các số dưới đây.

## Kết quả đã xác minh trong checkout

**BB84.** Có 10 raw CSV. Đối chiếu từng dòng theo `error_bits / sifted_bits` và `sifted_bits / n_signals` khớp QBER và sifted fraction đã lưu. Hai run dưới đây dùng cùng seed 42, 100.000 tín hiệu, noise 0,01, Eve/loss 0, simulator 0.1.0, Python 3.13.14, Windows build 26200. Mỗi run nhận 100.000 tín hiệu, giữ 49.990 bit và có 484 bit lỗi. QBER bằng 0,009681936387277455, sifted fraction bằng 0,4999. Đây là một kết quả mô phỏng xác định và hai quan sát thời gian vòng lặp.

| Run ID trong `data/raw/` | Thời gian vòng lặp (µs) | Tín hiệu mô phỏng/giây |
|---|---:|---:|
| `qkd_20261117T153737_f85e2488` | 520.126,1 | 192.261,07 |
| `qkd_20261127T150032_8e76e66e` | 220.778,3 | 452.943,07 |

**ML-KEM-768.** Đọc ba CSV trong `data/raw/`, mỗi file có 1.000 iteration riêng cho từng thao tác, warm-up 50. Metadata cùng ghi pqcrypto 0.4.0, Python 3.13.14, Windows build 26200. Các kích thước public key, secret key, ciphertext, shared secret lần lượt là 1.184, 2.400, 1.088, 32 byte. Tính lại median và p95 nearest-rank từ `latency_us` cho từng nhóm thao tác. Mỗi ô dưới đây ghi **median / p95, đơn vị µs**. Các timestamp là UTC.

| Run ID hoặc tập mẫu | Key generation | Encapsulation | Decapsulation |
|---|---:|---:|---:|
| `mlkem_20261019T085230_11c2a248` | 651,10 / 3.852,0 | 636,35 / 2.955,8 | 168,25 / 590,8 |
| `mlkem_20261107T154257_948b90ae` | 401,35 / 1.544,6 | 401,25 / 1.462,5 | 102,25 / 339,3 |
| `mlkem_20261107T154351_3af4a310` | 703,45 / 5.999,1 | 667,15 / 4.252,5 | 171,50 / 936,4 |
| Ba file trên, 3.000 mẫu/thao tác | 588,90 / 3.732,8 | 584,55 / 2.883,8 | 163,15 / 514,9 |

Các số gộp khớp `comparison_20261127T150039_832243fe.csv`. Ngày lập bảng là ngày phân tích. Lần đo ML-KEM gần nhất có raw ở đây là 07/11. CSV xác minh được phép tính, nhưng không chứa SHA của mã đã tạo chúng và không cho phép kiểm tra lại shared secret của từng mẫu.

**Kiểm thử.** Ngày 27/11 trên `66e687c`, lệnh `.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider` đạt **70 passed, 2 skipped trong 27,63 giây**. Hai skip thuộc test round trip và test xuất mẫu ML-KEM bằng backend thật. Xem [test ML-KEM](../tests/test_mlkem_benchmark.py) và [kết quả tuần 10 để đối chiếu](PROGRESS_LOG.md).

## Các kết quả nhóm đã báo cáo trước đây

- Báo cáo BB84 ghi 140 trial thuộc 14 setting, 10 trial/setting. Ví dụ ở Eve = 1, noise/loss = 0, QBER trung bình ± SD mẫu là 0,250174 ± 0,001481. Checkout này thiếu tập 140 CSV tương ứng để tính lại. Review độc lập còn mở. [Báo cáo BB84](../reports/QKD_BB84_EXPERIMENT.md)
- Đợt tích hợp 27/10 ghi 69 passed, 0 skipped trên Python 3.11.3, pqcrypto 1.0.0. Median/p95 (µs) của keygen, encaps và decaps lần lượt là 43,0/47,4, 49,8/54,3 và 65,0/70,5. Raw của chính lần đo đó vắng trong checkout này. [Báo cáo tích hợp](../reports/INTEGRATION_REPORT.md)
- Báo cáo 24/11 ghi 73 passed, 2 skipped trong 7,09 giây trên Python 3.14.2 và mô tả thay đổi ở worktree khi lập báo cáo. Bằng chứng Git sau đó xác nhận commit trên nhánh riêng. [Báo cáo ngày 24/11](https://github.com/Duc-HUST-ET1/QKD_vs_PQC/blob/146687f/reports/PROGRESS_REPORT_2026-11-24.md)

## Giới hạn khoa học và việc còn mở

BB84 ở đây mô phỏng bit, basis, intercept-resend, bit flip và loss. Ngưỡng QBER 0,11 chỉ phục vụ nhãn minh họa. QBER và sifted bits chưa tính xử lý lỗi, privacy amplification và độ dài khóa bí mật cuối cùng. Tốc độ vòng lặp Python chỉ mô tả phần mềm. ML-KEM dựa trên giả định tính toán và phép đo chỉ bao gồm ba primitive cục bộ. QKD cần kênh cổ điển xác thực. ML-KEM cần giao thức xác thực peer. Cả hai cần bảo vệ endpoint và quản lý vòng đời khóa. So sánh chi phí, cự ly, hiệu năng đầu-cuối hay mức phù hợp cho một địa điểm cần dữ liệu cùng phạm vi, hiện còn thiếu. [Threat model](THREAT_MODEL.md) · [Tài liệu tham khảo](REFERENCES.md)

Các đầu việc tiếp quản là đối chiếu và review hai nhánh với main, xác minh backend thật cho mã hiện hành, liên kết từng hình/bảng với tập raw có thể chia sẻ, review báo cáo BB84 và chốt chính sách artifact. Điều kiện nghiệm thu và trạng thái so với cam kết 24/11 nằm trong [nhật ký tuần 11](PROGRESS_LOG.md).
