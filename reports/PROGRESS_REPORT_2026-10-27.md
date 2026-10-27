# Báo cáo tiến độ tuần QKD_vs_PQC

**Kỳ báo cáo:** 21–27/10/2026

**Commit được đánh giá:** `main` / `origin/main` tại `568bc4e85017e10d99107f03a527a12b134493c6`

**Mốc so sánh:** báo cáo ngày 20/10/2026, commit `2b690aa5371de94d444fe2ec23f00e1a1c3d2164`

**Đồng bộ:** `HEAD` trùng `origin/main`; 13 commit sau mốc, gồm 9 commit không phải merge và 4 merge commit.
**Worktree:** có 21 mục `.pytest-tmp/` được Git theo dõi nhưng đang báo xóa cục bộ; `reports/PROGRESS_REPORT.md` là file chưa được Git theo dõi. Không tính các trạng thái cục bộ này là thay đổi đã merge.

## Tóm tắt điều hành

- **Đã merge:** adapter ML-KEM-768 được sửa để gọi API `pqcrypto` hiện hành; pipeline thêm `--sweep`, dùng backend đồ họa Agg mặc định và có test tích hợp. Cấu hình mặc định BB84 cũng trở lại `eve_probability: 0.0`.
- **Đã kiểm tra trong môi trường hiện tại:** pytest đạt **67 passed, 2 skipped**. Hai test ML-KEM skip vì môi trường hiện tại không có implementation `pqcrypto` tương thích; do đó mã adapter đã merge nhưng benchmark chưa xác minh được tại máy này.
- **Đã được báo cáo từ môi trường tích hợp khác:** `reports/INTEGRATION_REPORT.md` ghi benchmark với `pqcrypto 1.0.0`, 50 warm-up và 1.000 mẫu mỗi operation. CSV raw được báo là nằm trên máy kiểm tra ngoài workspace, nên các số latency chưa thể tái xác minh độc lập ở đây.
- **Cần xử lý:** README, `docs/EXPERIMENT_PROTOCOL.md` và `docs/DEVELOPMENT_GUIDE.md` còn mô tả API ML-KEM cũ. Comparison CSV mới được merge có số ML-KEM không kèm raw CSV; đồng thời gộp QKD từ 6 run khác cấu hình thành `mean_qber`/`mean_sifted_fraction`, nên các con số này không nên được hiểu là thống kê của một setting thuần nhất.
- **Không thay đổi phạm vi BB84:** đây vẫn là mô hình giáo dục cổ điển bit/basis; ngưỡng QBER 0,11 không phải chứng nhận an toàn.

## So sánh theo workstream

| Workstream | Trạng thái tại báo cáo 20/10 (`2b690aa`) | Cập nhật đã merge trong tuần | Trạng thái tại `568bc4e` |
|---|---|---|---|
| BB84 | Simulator và sweep lặp đã có; cohort 140 trial trong báo cáo BB84 đã đối chiếu ở workspace; báo cáo chờ review. | Sửa mặc định `eve_probability` từ 1.0 về 0.0 tại `568bc4e`; thêm test cấu hình mặc định. Pipeline có thể chạy sweep qua `--sweep`. | **Đã hoàn thành** ở mức mô hình giáo dục và pipeline. Báo cáo thí nghiệm vẫn **chờ review**; không có bằng chứng tuần này về lần chạy cohort mới hoặc review đã hoàn tất. |
| ML-KEM-768 | Adapter có nhưng không tương thích dependency có trong môi trường trước đó; chưa có benchmark xác minh tại workspace. | Commit tính năng `5c751e5` đổi adapter sang API `keygen/encaps/decaps`; được merge qua `36e91da`. Self-test xác nhận round-trip shared secret trước khi benchmark. | **Đã merge nhưng chưa xác minh ở môi trường hiện tại.** Test skip vì dependency không có. Báo cáo tích hợp khác ghi benchmark thành công; raw CSV không có trong workspace. |
| Pipeline và phân tích | Có pipeline cơ bản; chưa có sweep trong `run_all.py`; test plotting có thể lỗi do Tk/Tcl. | `cff086e` thêm `--sweep`, phân tích chỉ đầu ra của invocation hiện tại, Agg mặc định và refactor có thể test; thêm test pipeline. Merge cuối tại `568bc4e`. Trade-off analysis được kiểm tra metric hữu hạn/định dạng hợp lệ. | **Đã hoàn thành** theo test hiện tại. README cảnh báo prefix theo phút có thể bắt thêm run; đường `run_all.py --sweep` truyền danh sách file chính xác. |
| Tests | Báo cáo 20/10 ghi 50 passed/2 skipped với Agg; thiếu `pqcrypto`. | Thêm `tests/test_pipeline.py`, `tests/conftest.py`, mở rộng `tests/test_tradeoff_analysis.py`; báo cáo tích hợp ghi 57/2 trên nhánh pipeline và 62/0 trên một bản gộp thử. | **Đã kiểm tra:** 67 passed/2 skipped trong môi trường hiện tại; không có warning trong lệnh bên dưới. Hai skip vẫn do thiếu `pqcrypto`. |
| Tài liệu và provenance | Báo cáo BB84 ghi provenance cohort, đồng thời nêu ảnh/output tracked chưa nhất quán với `.gitignore`. | Thêm `reports/INTEGRATION_REPORT.md`, README CLI notes, cập nhật threat model/references; thêm `.pytest-tmp/` vào `.gitignore`. PR phân tích thêm comparison CSV có số liệu ML-KEM nhưng không raw CSV. | Tài liệu tích hợp ghi nhận benchmark môi trường khác và các điểm còn mở. **Cần xử lý:** README, experiment protocol và development guide vẫn mô tả API cũ; provenance của CSV/ảnh tracked chưa được giải quyết. |

## Thay đổi đã merge kể từ mốc tuần trước

`git diff --stat 2b690aa..568bc4e` xác nhận **15 đường dẫn, 691 dòng thêm và 187 dòng xóa**. Số này gồm tài liệu, test, PNG và comparison CSV, không đại diện riêng cho mã tính năng.

| Commit | Loại | Nội dung liên quan |
|---|---|---|
| `1185a5d`, `32cee80` → merge `0307c4d` | Hai commit nội dung + merge | Mở rộng threat model/references; cải thiện kiểm tra metric và test trade-off. |
| `5c751e5` → merge `36e91da` | Commit tính năng + merge | Sửa adapter benchmark ML-KEM để tương thích API backend và kiểm tra capability. |
| `be9369b` → merge `63a0f2d` | Commit phân tích + merge | Cập nhật latency CDF và comparison CSV. CSV mới cần đánh giá provenance/aggregation bên dưới. |
| `dee90e7`, `cff086e`, `e20b613`, `85bfeef`, `a539f19` → merge `568bc4e` | Chore/tính năng/tài liệu + merge | Ignore output pytest mới, thêm `--sweep`/Agg/test pipeline, báo cáo tích hợp và cập nhật README. |

Tổng cộng sau mốc là 13 commit trong lịch sử: 9 commit thường và 4 merge (`0307c4d`, `63a0f2d`, `36e91da`, `568bc4e`). Tính năng BB84 simulator và repeated sweep được mô tả trong báo cáo 20/10 là trạng thái có từ trước; không tính lại là tiến độ mới tuần này.

## Test và benchmark

### Test đã chạy trong workspace hiện tại

Lệnh thực tế:

```powershell
$env:MPLBACKEND='Agg'
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider --basetemp "$env:TEMP\qkd-pqc-weekly-20261027" -q
```

**Kết quả: 67 passed, 2 skipped trong 9,23 giây.** Skip tại `tests/test_mlkem_benchmark.py:27` và `:52`: optional verified `pqcrypto` ML-KEM-768 implementation không được cài. Lệnh tắt pytest cache và dùng thư mục tạm ngoài repository; không có warning/failure được in. Test này xác nhận suite hiện hành với dependency sẵn có, không xác nhận benchmark thật.

### ML-KEM: tách bằng chứng theo nguồn

**Mã đã merge:** `src/qkd_pqc/pqc/mlkem_benchmark.py` hiện yêu cầu các callable `keygen`, `encaps`, `decaps`, bọc lại thành giao diện nội bộ ổn định `generate_keypair`/`encrypt`/`decrypt`, rồi chạy round-trip và so sánh shared secret. Đây là thay đổi so với `2b690aa`; không đồng nghĩa benchmark đã chạy trong môi trường hiện tại.

**Số liệu được báo cáo ở máy tích hợp khác, chưa tái xác minh từ raw CSV:** `reports/INTEGRATION_REPORT.md` nêu nguồn `mlkem_20261027T135504_ea032902.csv`, 50 warm-up và 1.000 lần đo mỗi operation; median/p95 lần lượt là key generation **43,1/47,9 µs**, encapsulation **49,8/55,4 µs**, decapsulation **64,9/71,3 µs**. Báo cáo nói CSV được giữ ở máy kiểm tra và bị Git ignore. Không thấy file `data/raw/mlkem_*.csv` trong workspace hiện tại, vì vậy các số này là kết quả được báo cáo trong tài liệu, chưa phải dữ liệu có thể kiểm tra lại tại checkout này.

## CSV, hình và provenance

- Git theo dõi 4 comparison CSV trong `data/processed/`, gồm `comparison_20261025T022915_ef778c5c.csv`, cùng 4 PNG trong `figures/` (1 ML-KEM CDF, 3 hình QKD). Hiện workspace có thêm các comparison CSV raw/processed bị ignore, nhưng không có CSV ML-KEM raw.
- Comparison CSV ngày 25/10 gắn nhãn `measured_project_data` cho ML-KEM, với key generation median/p95 **651,1/3852,0 µs**, encapsulation **636,35/2955,8 µs**, decapsulation **168,25/590,8 µs**. Không có raw CSV tương ứng trong workspace để xác nhận nguồn, máy, version hoặc cohort. Các số này khác đáng kể với số trong báo cáo tích hợp (43,1/47,9; 49,8/55,4; 64,9/71,3 µs); hiện **chưa có dữ liệu để kết luận** số nào đại diện cho lần đo nào. Không dùng các số trong comparison CSV như phép đo đã tái kiểm chứng.
- Cùng comparison CSV ghi `valid_run_rows=6`, `mean_qber=0.08980496` và `mean_sifted_fraction=0.49765167`. Báo cáo tích hợp ghi nhận 6 run QKD khác cấu hình bị gộp. Vì QBER phụ thuộc setting, mean trên các setting không tương đương mean lặp của một setting; cần tính lại theo cohort/setting hoặc đổi nhãn thành phép gộp mô tả có cảnh báo.
- `.gitignore` nay có `.pytest-tmp/` và pattern cho raw CSV, processed output, figures; tuy nhiên các file đã được Git theo dõi vẫn tiếp tục được theo dõi. `git ls-files '.pytest-tmp/**'` đếm **21 fixture tracked**. Trong worktree hiện cả 21 đều báo xóa cục bộ; `reports/INTEGRATION_REPORT.md` nói PR thêm ignore có chủ ý giữ chúng. Ignore chỉ ngăn file chưa được theo dõi mới, không gỡ file tracked và không tự khôi phục những file đang thiếu.
- **Chính sách output cần xử lý:** các processed CSV/PNG bị ignore theo quy tắc nhưng một số vẫn được commit; `reports/QKD_BB84_EXPERIMENT.md` nói raw/processed/PNG không commit mặc định. Cần xác định artifact nào được duyệt để commit và artifact nào cần raw data/hash kèm theo. Không xóa hoặc khôi phục 21 fixture trong phạm vi báo cáo này.

## Tài liệu đối chiếu và trạng thái đúng/sai thời điểm

- `README.md` còn ghi adapter trên main gọi `generate_keypair`/`encrypt`/`decrypt` và chỉ nhánh `feature/mlkem-benchmark` sửa API; nội dung đó đã lỗi thời sau khi `5c751e5` được merge qua `36e91da`.
- `docs/EXPERIMENT_PROTOCOL.md` và `docs/DEVELOPMENT_GUIDE.md` cũng mô tả backend có callable `generate_keypair`, `encrypt`, `decrypt`. Adapter hiện tại dùng API upstream `keygen`, `encaps`, `decaps` rồi bọc thành API nội bộ; hai tài liệu cần cập nhật và nêu rõ sự khác nhau giữa API backend và adapter.
- `docs/PROJECT_SCOPE.md` và `docs/THREAT_MODEL.md` xác định giới hạn mô hình BB84/PQC và không cho phép kết luận bảo mật quá phạm vi. `docs/REFERENCES.md` yêu cầu `measured_project_data` có provenance; hàm `analyze_tradeoffs()` chỉ kiểm tra kiểu/giá trị hữu hạn, không thể xác thực nguồn CSV. Caller phải chịu trách nhiệm provenance.
- `configs/experiment_config.yaml` hiện có `eve_probability: 0.0`, khớp default được test trong `tests/test_pipeline.py`; đây là sửa thật so với cấu hình ở mốc 20/10.
- `reports/QKD_BB84_EXPERIMENT.md` vẫn gắn trạng thái chờ review độc lập. Không có bằng chứng trong các commit/tài liệu hiện tại rằng review đã hoàn tất.

## Công việc còn mở

| Ưu tiên | Công việc và trạng thái | Tiêu chí hoàn thành kiểm chứng được |
|---|---|---|
| Cao | **Cần xử lý:** cập nhật API docs ở README, `docs/EXPERIMENT_PROTOCOL.md`, `docs/DEVELOPMENT_GUIDE.md`. | Tài liệu phân biệt rõ API `keygen/encaps/decaps` của `pqcrypto` với wrapper nội bộ; tìm kiếm repo không còn khẳng định adapter hiện tại gọi API cũ. |
| Cao | **Chưa có dữ liệu tại checkout:** tái xác minh benchmark ML-KEM. | Chạy adapter với backend/version ghi rõ; giữ CSV raw có đủ 3 operation, 1.000 mẫu mỗi operation, metadata, kích thước key; tính lại median/p95 và đối chiếu với báo cáo tích hợp/comparison CSV. |
| Cao | **Cần xử lý:** provenance và QKD aggregation của `comparison_20261025T022915_ef778c5c.csv` cùng ảnh CDF. | Cung cấp raw CSV và cohort/version/config hoặc thay lại artifacts từ dữ liệu kiểm chứng; phân nhóm QKD theo từng cấu hình, không báo mean gộp 6 run khác setting như thống kê một setting. |
| Vừa | Chốt chính sách fixture/output tracked. | Quyết định có giữ hay gỡ 21 fixture tracked; sửa Git index/commit tương ứng theo quyết định. Kiểm tra `git ls-files` sau thay đổi; chỉ thêm `.gitignore` là chưa đủ. |
| Vừa | Chạy lại pipeline tích hợp trên main với backend ML-KEM thật. | Trên môi trường có `pqcrypto` tương thích, `run_all.py` và `run_all.py --sweep` kết thúc mã 0; lưu log/trạng thái và raw CSV; xác minh analysis chỉ nhận cohort được tạo trong lần chạy. |
| Vừa | Review BB84 độc lập. | Ghi nhận reviewer và kết quả/điểm sửa trong báo cáo; hiện vẫn **chờ review**. |
| Thấp | Chuẩn hóa lưu trữ generated artifacts. | README, reports và `.gitignore` thống nhất file nào được commit, file nào lưu ngoài Git và cách truy xuất provenance. |

## Kết luận

So với 20/10, thay đổi thực chất đã merge gồm adapter ML-KEM tương thích API, pipeline sweep/Agg với integration tests, sửa cấu hình Eve mặc định và cải thiện kiểm tra trade-off/threat model. Suite tại checkout hiện đạt 67/2; pipeline/test có tiến triển rõ. Tuy nhiên môi trường hiện tại chưa chạy benchmark ML-KEM, raw CSV của các số benchmark trong báo cáo tích hợp không có ở đây, các artifact comparison mới chưa có provenance đủ để xác minh, và tài liệu API còn lỗi thời. Chưa thể dùng các CSV/ảnh tracked này để đưa ra kết luận latency độc lập hoặc kết luận so sánh QKD/PQC. BB84 vẫn là mô hình giáo dục; báo cáo BB84 còn chờ review và không đưa ra chứng nhận an toàn.

## Căn cứ

- Git: `2b690aa..568bc4e`; commit nội dung `1185a5d`, `32cee80`, `5c751e5`, `be9369b`, `dee90e7`, `cff086e`, `e20b613`, `85bfeef`, `a539f19`; merge `0307c4d`, `63a0f2d`, `36e91da`, `568bc4e`.
- Báo cáo: `reports/PROGRESS_REPORT.md` (20/10), `reports/INTEGRATION_REPORT.md`, `reports/QKD_BB84_EXPERIMENT.md`.
- Tài liệu/cấu hình: `README.md`, `docs/PROJECT_SCOPE.md`, `docs/EXPERIMENT_PROTOCOL.md`, `docs/THREAT_MODEL.md`, `docs/REFERENCES.md`, `docs/DEVELOPMENT_GUIDE.md`, `configs/experiment_config.yaml`, `.gitignore`.
- Mã/test: `scripts/run_all.py`, `src/qkd_pqc/pqc/mlkem_benchmark.py`, `src/qkd_pqc/system/tradeoff_analysis.py`, `tests/test_pipeline.py`, `tests/test_tradeoff_analysis.py`, toàn bộ test suite.
- Artifact tracked: 4 `data/processed/comparison_*.csv`, 4 `figures/*.png`, 21 đường dẫn `.pytest-tmp/`. Không tìm thấy raw `data/raw/mlkem_*.csv` trong workspace.
