# Báo cáo tiến độ tuần QKD_vs_PQC

**Kỳ báo cáo:** 28/10–03/11/2026
**Mốc đánh giá:** `main` @ `b3db306` (03/11/2026, sau khi merge PR #8)
**Mốc tuần trước:** `main` @ `4274ecf` (27/10/2026)
**Trạng thái tại lần rà soát:** `main` đồng bộ `origin/main`; worktree sạch.

## 1. Tóm tắt điều hành

Trong kỳ có **hai PR được merge vào `main`**:

- PR #7 hoàn thiện báo cáo tích hợp sau khi merge PR #3–#6.
- PR #8 merge thay đổi của nhánh `feature/complete`, gồm **cả cập nhật mã nguồn, tests và tài
  liệu**. Vì vậy, báo cáo cũ ghi “không có thay đổi code tính năng/test trong tuần” là không còn
  đúng với mốc `main` mới; câu đó chỉ mô tả `main` tại `f34f68d`, trước PR #8.

Sau PR #8, BB84 có mô hình mất tín hiệu và số đo thời gian xử lý của simulator; phân tích hỗ trợ
thêm sweep theo loss, thống kê mean ± SD theo setting và tránh gộp các cấu hình/runtime khác nhau.
Các số thời gian mới là **hiệu năng vòng lặp Python**, không phải tốc độ tạo khóa của phần cứng
QKD. Không có benchmark ML-KEM mới hoặc số đo QKD phần cứng được tạo trong kỳ.

Đã chạy lại test suite trên checkout hiện tại: **70 passed, 2 skipped**. Hai test ML-KEM bị skip
do môi trường chưa có `pqcrypto.kem.ml_kem_768`; do đó adapter có trong code nhưng chưa được
benchmark lại tại môi trường này.

## 2. Thay đổi đã merge trong kỳ

| PR / mốc | Thay đổi |
|---|---|
| PR #7 — `f34f68d` | Merge báo cáo tích hợp sau PR #3–#6. |
| PR #8 — `b3db306` | Merge commit `13a3e66` từ `feature/complete`: cập nhật simulator BB84, CLI hiển thị metric, phân tích/biểu đồ, trade-off, tests và tài liệu. |

### Nội dung mã nguồn trong PR #8

- **BB84:** thêm `channel_loss_rate`; đếm `received_signals`, `lost_signals`, `loss_fraction`;
  đo `simulation_elapsed_us` và `simulation_signals_per_second`; kiểm tra xác suất hữu hạn trong
  [bb84_simulator.py](../src/qkd_pqc/qkd/bb84_simulator.py).
- **CLI:** `run_qkd.py` in thêm số tín hiệu nhận/mất và metric thời gian simulator.
- **Phân tích:** thêm biểu đồ sifted fraction theo channel loss; nhóm repeated runs theo setting,
  biểu diễn mean ± 1 sample SD; bỏ duplicate run BB84 cùng seed/cấu hình; tránh tổng hợp metric
  qua cấu hình hoặc runtime khác nhau; giới hạn tổng hợp timing theo metadata đồng nhất trong
  [plotting.py](../src/qkd_pqc/analysis/plotting.py).
- **Trade-off:** làm rõ ranh giới giữa latency primitive ML-KEM, throughput simulator BB84 và
  hiệu năng/key rate QKD thực tế trong
  [tradeoff_analysis.py](../src/qkd_pqc/system/tradeoff_analysis.py).
- **Kiểm thử/tài liệu:** thêm test cho metric simulator, channel loss, xử lý duplicate/mixed
  settings và cập nhật mô tả schema, protocol, scope, README.

Adapter ML-KEM dùng API backend `pqcrypto` `keygen`/`encaps`/`decaps`, bọc thành API nội bộ
`generate_keypair`/`encrypt`/`decrypt`; cần phân biệt hai lớp API này. Tài liệu đã được đồng bộ
với adapter trong PR #8.

## 3. Kiểm thử tại checkout hiện tại

Lệnh đã chạy trên Windows với Python 3.14.2, backend Matplotlib `Agg`; pytest cache tắt và thư
mục tạm đặt ngoài repository:

```powershell
$env:MPLBACKEND='Agg'
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider --basetemp "$env:TEMP\qkd-pqc-report-review-20261103" -q
```

**Kết quả quan sát:** **70 passed, 2 skipped trong 7,31 giây**. Hai skip ở
`tests/test_mlkem_benchmark.py` (dòng 27 và 52) do optional implementation
`pqcrypto.kem.ml_kem_768` không được cài. Lệnh này xác nhận test suite trên dependency hiện có;
nó không xác nhận benchmark ML-KEM.

Đây là kết quả chạy lại sau khi PR #8 đã vào `main`. Con số 67 passed/2 skipped trong bản báo cáo
cũ thuộc lần chạy trước phần test bổ sung, không phải kết quả cuối của checkout hiện tại.

## 4. Trạng thái theo workstream

| Workstream | Trạng thái tại `b3db306` | Bằng chứng và phần còn mở |
|---|---|---|
| Thành viên 1 — BB84/QKD | **Mô phỏng, sweep, loss và metric simulator đã có code/test; review báo cáo còn mở.** | Simulator hỗ trợ loss/noise/Eve; `run_all.py --sweep` chạy repeated sweeps; test kiểm tra các hành vi. [Báo cáo thí nghiệm BB84](QKD_BB84_EXPERIMENT.md) ghi cohort 140 trial và vẫn yêu cầu review độc lập. |
| Thành viên 2 — ML-KEM-768/PQC | **Adapter đã merge; benchmark chưa chạy lại ở môi trường hiện tại.** | Adapter kiểm tra đúng API backend và shared-secret round-trip. Capability check hiện trả unavailable vì thiếu `pqcrypto`; hai test optional bị skip. Báo cáo tích hợp ghi phép benchmark từ môi trường khác, nhưng checkout này không có raw ML-KEM CSV để xác minh lại. |
| Thành viên 3 — Phân tích/biểu đồ | **Code và test được mở rộng; provenance một số artifact cũ còn mở.** | Có thống kê repeated runs, biểu đồ loss, xử lý duplicate/mixed settings và metric simulator. Comparison CSV/ảnh ML-KEM đã tracked không thay thế raw measurements/version/provenance còn thiếu. |
| Thành viên 4 — Threat model/trade-offs | **Code/tài liệu được cập nhật; cần tiếp tục review nguồn và claim.** | Trade-off nêu riêng hiệu năng simulator, primitive ML-KEM và giới hạn triển khai; cần review độc lập trước khi dùng làm kết luận nghiên cứu. |
| Thành viên 5 — Tích hợp/config/test | **Pipeline/test có; quyết định artifact còn chờ nhóm.** | `run_all.py --sweep` và test tích hợp đã có từ các thay đổi trước; PR #8 bổ sung tests. Lần chạy hiện tại đạt 70/2. Có 21 đường dẫn `.pytest-tmp/` còn được Git theo dõi; `.gitignore` không tự gỡ các file đã tracked. |

## 5. Dữ liệu và ranh giới diễn giải

- Trong workspace hiện tại có **145 CSV BB84** ở `data/raw/`; trong đó **140 file** khớp cohort
  `qkd_20261019T1509*.csv` được mô tả trong báo cáo BB84. Đây là dữ liệu cũ, không phải cohort
  mới được tạo trong kỳ rà soát này.
- Không có file `mlkem_*.csv` trong `data/raw/` của checkout này. Một số comparison CSV và PNG
  được Git theo dõi, nhưng không có raw ML-KEM CSV tương ứng trong thư mục đó để tái xác minh số
  liệu ML-KEM.
- `simulation_elapsed_us` và `simulation_signals_per_second` đo vòng lặp Python xử lý tín hiệu
  mô phỏng. Chúng không đo optical hardware, kênh lượng tử, tốc độ trao đổi khóa QKD hoặc key
  generation rate của QKD thực tế.
- Latency keygen/encaps/decaps ML-KEM là số đo primitive phần mềm; không phải network handshake
  hay end-to-end protocol latency.
- QBER không cùng đơn vị/ý nghĩa với latency; QBER dưới 11% không chứng minh khóa an toàn.
- Mất tín hiệu trong simulator là xác suất Bernoulli độc lập, không phải mô hình suy hao quang học.
- Các CSV/PNG được tạo trong test có thể nằm dưới `.pytest-tmp/`; 21 đường dẫn như vậy hiện đã
  tracked. Nhóm cần quyết định chính sách giữ hay gỡ bằng PR riêng.

## 6. Việc còn mở

| Ưu tiên | Việc | Owner | Tiêu chí hoàn tất |
|---|---|---|---|
| Cao | Chạy lại test ML-KEM và benchmark với implementation tương thích. | Thành viên 2 + Thành viên 5 (cần xác nhận) | Cài extra `.[mlkem,dev]`; capability self-test thành công; chạy test và benchmark thật; lưu raw CSV cùng cấu hình, version và platform. Không thay bằng thuật toán khác. |
| Cao | Xác minh provenance các số ML-KEM trong artifact đã commit. | Thành viên 2 + Thành viên 3 (cần xác nhận) | Cung cấp raw CSV, máy/backend, cohort/config và nguồn; hoặc đánh dấu rõ artifact không tái xác minh được. |
| Cao | Review độc lập báo cáo thí nghiệm BB84. | Reviewer độc lập (chưa xác định) | Reviewer khác ghi kết quả và chỉnh sửa cần thiết trong báo cáo; không tự đánh dấu review hoàn tất. |
| Vừa | Quyết định chính sách `.pytest-tmp/`, PNG và CSV processed đã tracked. | Cả nhóm | Nhóm thống nhất giữ/gỡ và lý do; thực hiện thay đổi index bằng PR riêng, không xóa dữ liệu khi chưa thống nhất. |
| Vừa | Hoàn tất checklist nghiệm thu từng workstream. | Từng owner; Thành viên 5 điều phối | Owner xác nhận bằng chứng, test và tài liệu sau review; checklist giao việc không tự chứng minh review đã xong. |

## 7. Kế hoạch đề xuất cho tuần tới

1. **Thành viên 2 + Thành viên 5 (owner cần xác nhận):** cài backend tương thích, chạy test
   ML-KEM và pipeline; lưu, đối chiếu raw output trước khi trích số liệu.
2. **Reviewer độc lập (chưa xác định):** đọc và ghi nhận review báo cáo BB84.
3. **Cả nhóm:** quyết định chính sách với `.pytest-tmp/` và generated artifacts tracked; nếu đổi,
   thực hiện qua PR riêng.
4. **Thành viên 3 + Thành viên 4 (owner cần xác nhận):** rà provenance và wording của comparison
   CSV/figures trước khi dùng trong báo cáo nghiên cứu.
5. **Từng owner:** cập nhật checklist workstream với trạng thái đã review, test và blocker thực
   tế.
