# Báo cáo đối chiếu đầu ra cuối dự án QKD_vs_PQC

**Ngày lập:** 10/11/2026

**Commit hiện tại:** `main` / `origin/main` tại `024669e65d8b72b9f05cff491550d83a28077e16`

**Mốc so sánh:** `main` tại `b3db306` (03/11/2026; sau PR #8)
**Đồng bộ:** `HEAD` trùng `origin/main`. Từ mốc `b3db306` có 2 commit: commit nội dung `036601b` và merge commit `024669e` (PR #9).

## Tóm tắt

- **Đã hoàn thành trước tuần này:** PR #8 (`13a3e66`, merge tại `b3db306`) cập nhật simulator BB84, thêm runtime/throughput của vòng lặp mô phỏng, kiểm soát tổng hợp theo cấu hình/runtime, bổ sung test và đồng bộ tài liệu API ML-KEM.
- **Đầu ra mới nhất đã merge:** PR #9 chỉ thay đổi bốn PNG trong `figures/`: ba đồ thị QKD và `mlkem_latency_cdf.png`. So sánh Git cho thấy không đổi mã, test hay CSV dữ liệu trong PR này.
- **Kiểm thử tại `HEAD` trước phần sửa cục bộ:** 70 passed, 2 skipped do môi trường workspace thiếu `pqcrypto.kem.ml_kem_768`. Sau các thay đổi code/test được ghi ở mục “Rà soát mã nguồn”, suite đạt 74 passed, 2 skipped.
- **Đối chiếu đầu ra với dữ liệu nguồn:** workspace có 145 CSV QKD cũ, nhưng không CSV nào chứa hai cột runtime mới; không có raw CSV ML-KEM. Vì vậy PNG cuối và các số ML-KEM trong comparison CSV không thể được tái tạo độc lập từ raw data hiện có.
- **Còn mở:** lưu hoặc dẫn nguồn dữ liệu cho artifact định lượng, xử lý comparison CSV có QBER gộp nhiều setting, xác nhận chính sách artifact tracked và hoàn tất review độc lập báo cáo BB84.

## Thay đổi kể từ báo cáo 03/11

| Thành phần | Trạng thái tại `b3db306` | Cập nhật tới `024669e` |
|---|---|---|
| BB84 simulator và metric runtime | Đã có code/test từ PR #8; runtime là thời gian Python của simulator, không phải QKD key rate. | Không đổi trong PR #9. |
| Phân tích và trade-off | Đã ngăn tổng hợp QBER/sifting/loss qua nhiều setting; runtime chỉ tổng hợp khi metadata điều kiện và môi trường đồng nhất. | Không đổi mã trong PR #9. Test của PR #8 bao phủ trường hợp mixed settings và runtime. |
| Tài liệu/API ML-KEM | README, protocol và development guide đã phân biệt API backend `keygen/encaps/decaps` với wrapper nội bộ `generate_keypair/encrypt/decrypt`. | Không đổi trong PR #9. |
| CSV comparison | Các CSV trước đó vẫn là artifact tracked, gồm bảng ngày 25/10 có số ML-KEM và `mean_qber` gộp. | PR #9 không cập nhật CSV nào; số liệu cũ vẫn còn trong Git. |
| Hình | Bốn PNG được theo dõi ở `figures/`. | Commit `036601b` cập nhật binary của cả bốn hình; không kèm CSV/raw data mới. |

`git diff --stat b3db306..024669e` xác nhận **4 file ảnh thay đổi, không có dòng mã/CSV thay đổi**. Không tính thay đổi tính năng BB84 hoặc sửa tài liệu API của PR #8 là công việc mới trong tuần này.

## Kiểm thử tại checkout hiện tại

Đã chạy:

```powershell
$env:MPLBACKEND='Agg'
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider --basetemp "$env:TEMP\qkd-pqc-final-20261110" -q
```

**Kết quả trên `HEAD` trước phần sửa cục bộ: 70 passed, 2 skipped trong 6,12 giây.** Hai test skip tại `tests/test_mlkem_benchmark.py` do optional implementation `pqcrypto.kem.ml_kem_768` không được cài. Lệnh không in warning hoặc failure. Kết quả này xác minh test trong dependency hiện có, không xác minh benchmark thật.

`reports/INTEGRATION_REPORT.md` ghi một lần tích hợp khác trên `main` @ `568bc4e`, Python 3.11.3 và `pqcrypto 1.0.0`: 69 passed/0 skipped, `run_all.py --sweep` hoàn tất, 140 CSV sweep và benchmark ML-KEM hoàn tất. Đây là bằng chứng đã được ghi trong báo cáo tích hợp, nhưng không phải kết quả chạy tại checkout/môi trường hiện tại.

## Đối chiếu với đầu ra và dữ liệu

### BB84

- `data/raw/` hiện có 145 file CSV QKD. Có 143 file theo schema đã thêm loss, hai file theo schema cũ; **0/145 file có** `simulation_elapsed_us` hoặc `simulation_signals_per_second`.
- 140 file thuộc cohort `qkd_20261019T1509*.csv` trong báo cáo BB84; đây là cohort tháng 10, không phải dữ liệu mới được sinh cho PR #8/#9.
- Do không có raw run CSV chứa runtime mới, chưa thể xác minh số runtime/throughput được dùng để cập nhật các hình hoặc bảng trên `main`. Đây là tốc độ vòng lặp Python của simulator, không phải tốc độ tạo khóa QKD vật lý.
- Mã hiện tại xử lý đúng trường hợp trộn setting bằng cách phát `measurement_scope`/`setting_count` thay vì mean QBER chung. Tuy nhiên `data/processed/comparison_20261025T022915_ef778c5c.csv` vẫn chứa `mean_qber=0.08980496` và `mean_sifted_fraction=0.49765167` trên 6 run khác cấu hình. File CSV này không được cập nhật bởi PR #9; không nên dùng các mean đó như kết quả một setting.

### ML-KEM-768

- Báo cáo tích hợp ghi benchmark trên `main` với raw file `mlkem_20261027T143913_1061f4a1.csv`, 50 warm-up và 1.000 mẫu mỗi operation. Median/p95 báo cáo: key generation **43,0/47,4 µs**, encapsulation **49,8/54,3 µs**, decapsulation **65,0/70,5 µs**. Báo cáo nói raw CSV bị ignore và được giữ ở máy kiểm tra.
- Workspace hiện có **0** file `data/raw/mlkem_*.csv`; vì thế các số trên là **được báo cáo trong integration report, chưa tái xác minh từ raw CSV tại checkout này**.
- Comparison CSV tracked ngày 25/10 vẫn ghi key generation **651,1/3852,0 µs**, encapsulation **636,35/2955,8 µs**, decapsulation **168,25/590,8 µs** và có nhãn `measured_project_data`. Không có raw nguồn để xác định môi trường/cohort hoặc giải thích chênh lệch với benchmark được báo cáo tích hợp.
- Hình CDF ML-KEM được cập nhật ở `036601b`, nhưng commit chỉ chứa ảnh. Không có raw CSV hay bảng nguồn đi kèm để tái kiểm tra đường cong.

## Rà soát mã nguồn và hoàn tất phần có thể kiểm chứng

Đối chiếu với đầu ra cuối cho thấy một lỗi còn tồn tại trong code: nếu lượt phân tích hiện tại không có dữ liệu cho một đồ thị cố định tên, file PNG cũ vẫn nằm đó; đặc biệt, chạy phân tích QKD khi không có CSV ML-KEM có thể để lại CDF từ lần benchmark trước. Ngoài ra, code trước đó gộp mẫu ML-KEM từ các implementation/runtime khác nhau vào một median/p95 và một CDF, dù metadata đã có trong CSV.

Các sửa đổi cục bộ, chưa commit trong worktree:

- `src/qkd_pqc/analysis/plotting.py`: dọn PNG cũ cùng tên khi lượt phân tích có đầu vào nhưng không có dữ liệu hiện tại hỗ trợ đồ thị đó; khi không truyền CSV thì giữ nguyên outputs. ML-KEM CDF được chia theo implementation/version, Python/platform và số vòng warm-up/đo. Comparison chỉ gộp median/p95 khi provenance đồng nhất; dữ liệu từ nhiều nhóm nhận `measurement_scope`/`measurement_group_count`, không có median gộp. CSV cũ thiếu provenance được giữ tách theo file nguồn. Bảng một nhóm ghi kèm provenance.
- `src/qkd_pqc/system/tradeoff_analysis.py`: phân biệt metric định lượng `measured_project_data` với scope/count/provenance gắn nhãn mới `measurement_metadata`, để số nhóm và metadata không bị đọc như phép đo.
- `tests/test_plotting.py`: thêm kiểm chứng rằng ảnh lỗi thời được dọn, ML-KEM khác runtime hoặc CSV legacy thiếu provenance không bị gộp, và bảng lưu metadata nguồn.
- `tests/test_tradeoff_analysis.py`: kiểm chứng nhãn evidence riêng cho scope/count/provenance.
- `README.md`, `docs/USER_GUIDE.md`, `docs/EXPERIMENT_PROTOCOL.md`: mô tả chính sách dọn ảnh và cách tách/tổng hợp ML-KEM theo provenance.
- `docs/DATA_DICTIONARY.md`, `docs/REFERENCES.md`, `docs/THREAT_MODEL.md`, `docs/DEVELOPMENT_GUIDE.md`: ghi rõ `measurement_metadata` và ranh giới với metric đo.

Đã chạy lại sau sửa code:

```powershell
$env:MPLBACKEND='Agg'
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider --basetemp "$env:TEMP\qkd-pqc-source-audit-final4-20261110" -q
```

**Kết quả: 74 passed, 2 skipped trong 5,79 giây, không warning.** Hai skip vẫn là test tùy chọn ML-KEM vì thiếu `pqcrypto`. Những thay đổi này đang ở worktree và chưa thuộc commit `024669e`.

### Trạng thái provenance/artifact

- `git ls-files` cho thấy 4 comparison CSV và 4 PNG được theo dõi. `.gitignore` vẫn bỏ qua `data/processed/*` và `figures/*`, nhưng ignore không gỡ các artifact đã tracked.
- Có 21 path `.pytest-tmp/` tracked; worktree hiện báo cả 21 bị xóa cục bộ. `.gitignore` có `.pytest-tmp/`, nhưng thay đổi ignore không tự untrack file cũ.
- Báo cáo 03/11 đang có chỉnh sửa cục bộ chưa commit; file này được giữ nguyên. Ngoài ra worktree còn 21 mục `.pytest-tmp/` báo xóa và hai báo cáo trước đây chưa tracked. Những trạng thái này không thuộc commit `024669e`.

## Việc còn mở

| Ưu tiên | Việc | Điều kiện hoàn tất có thể kiểm tra |
|---|---|---|
| Cao | Cung cấp provenance cho các hình và số ML-KEM được công bố. | Lưu/đính kèm raw CSV có run ID, config, backend/version, platform; tạo lại CDF và median/p95 từ CSV đó. Nếu raw không còn, ghi rõ artifact không thể tái xác minh và bỏ nhãn đo đã xác minh. |
| Cao | Sửa comparison CSV có thống kê QKD trộn setting. | Tạo bảng từ run CSV theo đúng cohort; với nhiều setting chỉ lưu `measurement_scope`/`setting_count` và kết quả theo setting, hoặc giới hạn mean vào một cấu hình thống nhất. Không giữ `mean_qber` gộp 6 setting như metric một setting. |
| Cao | Chạy benchmark ML-KEM trong môi trường có dependency tương thích. | Capability check và test ML-KEM pass; benchmark tạo raw CSV cho 3 operation với 1.000 mẫu/operation, metadata đầy đủ; tính lại và đối chiếu kết quả. |
| Vừa | Chốt chính sách generated artifacts và 21 fixture tracked. | Nhóm quyết định file nào giữ trong Git; sau đó thay đổi index có chủ đích và kiểm tra `git ls-files`. Không xem `.gitignore` là thao tác gỡ file tracked. |
| Vừa | Review độc lập báo cáo BB84. | Reviewer khác ghi kết quả trong `reports/QKD_BB84_EXPERIMENT.md`; trạng thái hiện vẫn chờ review. |

## Kết luận

Đầu ra mới nhất đã merge trên `main` có bốn hình được cập nhật, nhưng không kèm CSV nguồn. Rà soát mã đã xử lý các lỗi có thể tái lập: PNG cũ tồn tại khi dữ liệu hiện tại không hỗ trợ hình; gộp median/CDF ML-KEM qua nhiều provenance; gộp CSV legacy không có provenance; và nhãn metadata scope/count bị đánh đồng với metric đo. Suite sau sửa đạt 74/2. Các số ML-KEM vẫn chưa thể tái xác minh do không có raw CSV trong workspace và backend không có trong môi trường hiện tại; review BB84 và chính sách file tracked còn cần quyết định ngoài code.

**Căn cứ:** Git `b3db306..024669e`; `reports/PROGRESS_REPORT_2026-11-03.md`; `reports/INTEGRATION_REPORT.md`; `reports/QKD_BB84_EXPERIMENT.md`; bốn CSV/PNG tracked; `src/qkd_pqc/analysis/plotting.py`; `src/qkd_pqc/qkd/bb84_simulator.py`; `src/qkd_pqc/pqc/mlkem_benchmark.py`; `tests/test_plotting.py`, `tests/test_pipeline.py`, `tests/test_tradeoff_analysis.py`.
