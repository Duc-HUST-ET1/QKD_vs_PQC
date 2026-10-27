# Báo cáo tích hợp và tái lập (Thành viên 5)

**Ngày kiểm tra:** 2026-10-27 · **Nhánh:** `integration/pipeline` (tách từ `main` @ `2b690aa`)
**Trạng thái:** Ready for Review. Mọi số đo dưới đây được quan sát trực tiếp trên máy kiểm tra.

## Môi trường

| Thành phần | Giá trị |
|---|---|
| Hệ điều hành | Windows 11 Pro (`Windows-10-10.0.26200-SP0`), Intel64 Family 6 Model 186 |
| Python | 3.11.3, venv `.venv`, `pip install -e ".[mlkem,dev]"` |
| Package | PyYAML 6.0.3, matplotlib 3.11.2, pytest 9.1.1, pqcrypto 1.0.0 |

## Kết quả kiểm tra

| Phép kiểm tra | Kết quả quan sát |
|---|---|
| `pytest` trên `main` gốc | 49 passed, 1 failed, 2 skipped. Lỗi `test_plotting_omits_averages_across_mixed_qkd_settings` xuất hiện ngẫu nhiên (`TclError: invalid command name "tcl_findLibrary"`) vì matplotlib tự chọn backend `tkagg`. Chạy riêng `tests/test_plotting.py` 3 lần: pass, pass, fail. |
| `pytest` trên nhánh này | 57 passed, 2 skipped, ổn định 5/5 lần chạy liên tiếp. 2 skip là test ML-KEM vì adapter trên `main` không khớp API `pqcrypto` 1.0.0. |
| Gộp thử `main` + `feature/model` + `feature/mlkem-benchmark` (nhánh tạm local, không push) | Gộp không xung đột; `pytest` (với `MPLBACKEND=Agg`): **62 passed, 0 skipped**. Test ML-KEM lần đầu chạy với backend thật. |
| `run_all.py` trên bản gộp thử, config mặc định với `eve_probability: 0.0` | BB84 completed; ML-KEM-768 completed; Analysis completed (3 hình). Mã thoát 0. |
| `run_qkd_experiment.py` trên bản gộp thử | 140 CSV trong 28 giây; `run_analysis.py --qkd-run-prefix` tạo đủ 5 hình. |

### Tái lập BB84

Run đơn với seed 42 cho `sifted=49990/100000`, `QBER=0.009681936387277455`, trùng khớp từng chữ số
với smoke test trong [QKD_BB84_EXPERIMENT.md](QKD_BB84_EXPERIMENT.md). Điều này xác nhận tái lập
theo seed trên một máy thứ hai.

### Benchmark ML-KEM-768 thật đầu tiên

Nguồn: `mlkem_20261027T135504_ea032902.csv`, 50 warm-up và 1000 lần đo cho mỗi thao tác, chạy từ
nhánh `feature/mlkem-benchmark`. CSV raw bị Git bỏ qua theo quy ước và được giữ ở máy kiểm tra.

| Thao tác | Median (µs) | p95 (µs) |
|---|---:|---:|
| key_generation | 43.1 | 47.9 |
| encapsulation | 49.8 | 55.4 |
| decapsulation | 64.9 | 71.3 |

Kích thước khóa trong CSV đúng với FIPS 203 cho ML-KEM-768: public key 1184 byte, secret key 2400
byte. Đây là độ trễ của primitive phần mềm trên một máy, không phải handshake, network hay so sánh
tổng quát với QKD.

## Vấn đề phát hiện và cách xử lý

| # | Vấn đề | Owner | Xử lý |
|---|---|---|---|
| 1 | `configs/experiment_config.yaml` có `eve_probability: 1.0` (commit `ab14865`), trái với docs (`0.0`) và với smoke test của báo cáo BB84. Với giá trị này, `run_all.py` mặc định cho QBER khoảng 25% và trạng thái reject. | Thành viên 5 (config dùng chung), commit của Thành viên 3 | Khôi phục `0.0` trong PR này. Thêm test `test_shipped_config_matches_documented_defaults`. **Cần Thành viên 3 xác nhận.** |
| 2 | Thư mục `.pytest-tmp/` (CSV, PNG, symlink tạm của pytest) đã bị commit lên `main`. | Thành viên 5 | Thêm vào `.gitignore` để không bị commit lại. 21 file đã có **được giữ nguyên**; đề xuất gỡ trong một PR riêng (`chore/remove-pytest-tmp`) sau khi Thành viên 1 đồng ý. |
| 3 | Test plotting lỗi ngẫu nhiên do backend Tk. | Thành viên 5 (tests), Thành viên 3 (plotting) | Thêm `tests/conftest.py` dùng `Agg`. `run_all.py` mặc định `MPLBACKEND=Agg`. **Đề xuất Thành viên 3** gọi `matplotlib.use("Agg")` trong `plotting.py` để `run_analysis.py` cũng an toàn. |
| 4 | `run_all.py` chạy capability self-test ML-KEM hai lần (một lần trực tiếp, một lần trong `run_mlkem_benchmark`). | Thành viên 5 | Chỉ gọi `run_mlkem_benchmark` và bắt `MLKEMUnavailableError` để báo skip. |
| 5 | `run_all.py` không chạy được sweep của Thành viên 1. | Thành viên 5 | Thêm `--sweep`. Phân tích nhận đúng danh sách CSV của sweep vừa chạy. |
| 6 | `--qkd-run-prefix` chỉ chính xác tới phút: prefix `qkd_20261027T1355` lẫn thêm 1 CSV của lần `run_all` cùng phút (141 thay vì 140 dòng). | Thành viên 1/3 | Ghi chú trong README. `run_all.py --sweep` không bị ảnh hưởng. Đề xuất in prefix đầy đủ hơn hoặc ghi manifest danh sách file. |
| 7 | Adapter trên `main` không nhận `pqcrypto` 1.0.0 (API `keygen`/`encaps`/`decaps`), nên ML-KEM luôn bị skip. | Thành viên 2 | PR #5 (`feature/mlkem-benchmark`) đã sửa và chạy được (xem trên); đề xuất approve. Docs `DEVELOPMENT_GUIDE.md` và `EXPERIMENT_PROTOCOL.md` vẫn ghi API cũ. |
| 8 | Bảng `data/processed/comparison_20261019T085604_0a1ec043.csv` và `figures/mlkem_latency_cdf.png` trên `main` có số ML-KEM (ví dụ keygen median 651.1 µs) nhưng không có CSV raw `mlkem_*.csv` đi kèm. Lần đo ở đây cho 43.1 µs. | Thành viên 3 | Chưa xác minh được nguồn. PR #4 thêm `comparison_20261025T022915_ef778c5c.csv` với **cùng các số này**, vẫn không có CSV raw, và có `mean_qber` gộp 6 run khác cấu hình. **Đề xuất request changes cho PR #4**: tạo lại bảng/hình từ CSV thật sau khi merge PR #5. |
| 9 | `figures/` và `data/processed/` bị `.gitignore` chặn nhưng vẫn có file được ép commit. | Cả nhóm | Chưa thay đổi. Cần nhóm quyết định: gỡ các file này, hoặc tạo ngoại lệ cho assets báo cáo. |

## Thay đổi trong PR này

- `scripts/run_all.py`: thêm `--sweep`, phân tích đúng CSV của lượt chạy, một lần self-test ML-KEM,
  backend `Agg` mặc định, `main(argv)` để test được.
- `tests/test_pipeline.py` (mới): 7 test tích hợp: skip ML-KEM trung thực, chỉ phân tích CSV của lượt
  hiện tại, raw không bị ghi đè, sweep, ML-KEM lỗi trả mã 1, config sai trả mã 1, config mặc định
  khớp docs.
- `tests/conftest.py` (mới): backend `Agg` cho test.
- `configs/experiment_config.yaml`: `eve_probability` từ `1.0` về `0.0`.
- `.gitignore`: thêm `.pytest-tmp/` (không xóa file nào đã được commit).
- `README.md`: cập nhật cờ CLI, `--sweep`, trạng thái ML-KEM.

## Thứ tự merge đề xuất

1. PR #3 (`feature/model`, Thành viên 4): không xung đột.
2. PR #5 (`feature/mlkem-benchmark`, Thành viên 2): docs API cập nhật sau.
3. PR này (`integration/pipeline`), sau khi Thành viên 3 xác nhận mục 1.
4. PR #4 (Thành viên 3): làm lại từ CSV thật hoặc đóng.
5. Chạy lại `pytest` và `run_all.py --sweep` trên `main` sau khi merge, cập nhật báo cáo này.

## Checklist Thành viên 5

- [x] Config validation: config mặc định có test, đường dẫn output tương đối
- [x] CLI/status: `completed`/`skipped`/`failed` cho từng bước, mã thoát đúng
- [x] CSV interfaces: phân tích dùng đúng file của lượt chạy, raw không bị ghi đè
- [x] Suite: 57 passed / 2 skipped trên nhánh; 62 passed trên bản gộp thử
- [x] Docs: README, báo cáo này
- [ ] Không có output/secret vô tình commit: đã chặn `.pytest-tmp/` mới; gỡ file cũ (mục 2) và mục 9 chờ nhóm quyết định
- [ ] Merge hai nhánh còn lại và kiểm tra lại trên `main`
