# Báo cáo tiến độ tuần dự án QKD_vs_PQC

**Kỳ báo cáo:** 17–24/11/2026 (cập nhật đến ngày 24/11/2026)  
**Mốc trước:** báo cáo tiến độ ngày 03/11/2026, `main` tại `f34f68d`  
**Commit hiện tại:** `c8166f7` — merge PR #10; `HEAD`, `main` và `origin/main` cùng trỏ tới commit này.  
**Nhánh checkout:** `feature/qkd`, cùng commit với `main`.  
**Trạng thái thay đổi tại thời điểm lập báo cáo:** các sửa đổi rà soát ngày 24/11 đang ở worktree, chưa commit.

## 1. Tóm tắt điều hành

Trong kỳ báo cáo, các hình phân tích trade-off và kết quả BB84/ML-KEM tiếp tục được cập nhật và
PR #10 đã được merge vào `main`. Rà soát mã nguồn theo câu hỏi nghiên cứu phát hiện một số nguy cơ
diễn giải sai: thời gian simulator BB84 có thể bị gộp hoặc bị loại khi các lần chạy dùng cùng seed;
latency ML-KEM từ các runtime khác nhau có thể bị gộp thành một phân phối; và số liệu mô phỏng BB84
được gắn nhãn “Measured QKD”.

Đã sửa các điểm trên trong worktree: tách số liệu mô phỏng khỏi timing simulator, khử trùng lặp
mẫu ML-KEM theo ID mẫu, phân chia biểu đồ theo cohort runtime/cấu hình đo và đổi nhãn số liệu BB84
thành “Measured BB84 simulator”. Bộ kiểm thử hiện đạt **73 passed, 2 skipped**. Hai test bị skip
do môi trường kiểm tra chưa có package tùy chọn `pqcrypto`; do đó chưa có benchmark ML-KEM mới được
xác minh trong kỳ.

**Kết luận chung:** phần mềm hiện hỗ trợ mô tả có căn cứ về giả định bảo mật, một số phép đo ở mức
simulator/primitive và yêu cầu hạ tầng ở mức định tính. Chưa có cơ sở để kết luận hiệu năng thiết
lập khóa đầu-cuối hoặc xếp hạng mức phù hợp cho một địa điểm triển khai cụ thể.

## 2. Tiến triển so với báo cáo trước

| Thời điểm/commit | Tiến triển | Ý nghĩa đối với đề tài |
|---|---|---|
| 03/11 — `13a3e66` | Bổ sung thời gian vòng lặp và số tín hiệu simulator BB84 xử lý mỗi giây; cập nhật phân tích, giao thức và phạm vi. | Có số đo hiệu năng phần mềm mô phỏng, nhưng không phải tốc độ tạo khóa bí mật QKD vật lý. |
| 07/11 — `036601b` | Cập nhật các ảnh biểu đồ phân tích. | Cải thiện đầu ra hình ảnh; ảnh không thay thế dữ liệu CSV nguồn. |
| 17/11 — `0b2eff5` | Tiếp tục cập nhật các hình biểu đồ trade-off/ML-KEM. | Có thay đổi artifact hình; không xác nhận được số liệu ML-KEM từ CSV raw trong workspace hiện tại. |
| 24/11 — `c8166f7` | Merge PR #10; `main` và `origin/main` cùng ở commit này. | Mốc code hiện hành để đánh giá. |
| 24/11 — worktree hiện tại | Sửa cách phân nhóm/khử trùng lặp số liệu hiệu năng, nhãn nguồn BB84, test và tài liệu. | Tăng độ tin cậy của phân tích; thay đổi chưa commit. |

Từ báo cáo ngày 03/11, commit bổ sung chính trong mã nguồn là `13a3e66`, liên quan đo hiệu năng
simulator BB84. Các commit ngày 07/11 và 17/11 chủ yếu thay đổi PNG được theo dõi trong Git; không
được xem là bằng chứng có thêm benchmark raw nếu không có CSV và provenance đi kèm.

## 3. Công việc thực hiện trong kỳ

### 3.1. Tách hiệu năng simulator BB84 khỏi kết quả mô phỏng

Trước sửa đổi, pipeline loại các run trùng seed/cấu hình để tránh đếm lặp kết quả BB84 xác định.
Do thời gian chạy cũng được lưu trong cùng CSV, bước khử trùng lặp này có thể làm mất những lần
đo timing độc lập có `run_id` khác nhau. Sau sửa đổi:

- Kết quả QBER/sifting tiếp tục khử trùng lặp theo seed và cấu hình để không coi việc chạy lại cùng
  mô phỏng xác định là một kết quả độc lập.
- Timing simulator được xử lý riêng theo `run_id`; các lần thực thi khác nhau vẫn có thể đóng góp
  vào thống kê runtime.
- Bản xuất lặp của cùng `run_id` không bị tính lại.
- Nếu điều kiện hoặc runtime khác nhau, bảng không tạo một giá trị trung bình chung gây hiểu nhầm.

### 3.2. Phân tích ML-KEM theo cohort

Latency ML-KEM có ý nghĩa khi xét cùng thuật toán, implementation, phiên bản thư viện, nền tảng,
phiên bản Python và cấu hình warm-up/số lần đo. Phân tích hiện:

- Khử trùng lặp mẫu có cùng `(run_id, operation, iteration)`.
- Chia cohort theo metadata runtime và cấu hình benchmark.
- Hiển thị các cohort riêng trên CDF khi đầu vào có nhiều môi trường/cấu hình.
- Không gộp median/p95 qua nhiều cohort; bảng comparison ghi phạm vi và số cohort để người đọc
  tra cứu CDF/CSV nguồn.

### 3.3. Làm rõ nhãn bằng chứng

Các metric truyền vào bảng comparison từ CSV BB84 đều là kết quả của simulator giáo dục. Nhãn
“Measured QKD” được đổi thành **“Measured BB84 simulator”** để không bị hiểu thành số đo từ thiết
bị hoặc hệ thống QKD vật lý.

### 3.4. Kiểm thử hồi quy và tài liệu

Bổ sung các test kiểm tra:

1. Hai lần chạy BB84 có cùng seed nhưng `run_id` riêng vẫn được tính như hai lần đo runtime, trong
   khi chỉ tính một kết quả mô phỏng xác định.
2. Latency ML-KEM từ các runtime cohort khác nhau không bị gộp trong bảng.
3. Mẫu ML-KEM bị lặp do đọc lại cùng file không làm sai thống kê.

Cập nhật README, từ điển dữ liệu và giao thức thí nghiệm để mô tả cách phân nhóm, khử trùng lặp và
giới hạn diễn giải.

## 4. Trạng thái theo workstream

| Workstream | Trạng thái | Bằng chứng và giới hạn |
|---|---|---|
| BB84/QKD | **Mô hình giáo dục và sweep đã có; giới hạn được làm rõ** | Mô phỏng bit/basis, Eve intercept-resend, bit flip và mất tín hiệu; có QBER/sifting và timing vòng lặp Python. Không mô phỏng trạng thái lượng tử, thiết bị quang hoặc tạo khóa QKD triển khai. |
| Hiệu năng BB84 | **Đo được hiệu năng simulator, không phải hiệu năng QKD vật lý** | CSV ghi thời gian vòng lặp và tín hiệu mô phỏng/giây. Phân tích mới giữ riêng timing của các lần chạy và không gộp qua runtime/điều kiện không đồng nhất. |
| ML-KEM-768 | **Adapter có; benchmark chưa xác minh trong môi trường hiện tại** | Mã adapter và test có sẵn; package `pqcrypto` không cài trong `.venv`, nên hai test tùy chọn bị skip. Không có `data/raw/mlkem_*.csv` trong workspace hiện tại để tái kiểm tra latency. |
| Phân tích và biểu đồ | **Đã tăng độ an toàn khi tổng hợp; provenance artifact cũ còn mở** | CDF ML-KEM giờ có thể phân biệt cohort. Một số PNG/CSV comparison được Git theo dõi nhưng không có raw ML-KEM CSV tương ứng trong workspace; không dùng chúng làm số đo mới đã xác minh. |
| Giả định bảo mật/threat model | **Có mô tả và giới hạn; cần review học thuật độc lập** | Tài liệu phân biệt giả định QKD và ML-KEM, nhấn mạnh xác thực, endpoint và key lifecycle. Mô phỏng/benchmark không phải security audit hoặc chứng minh an toàn triển khai. |
| Hạ tầng và khả năng phù hợp triển khai | **So sánh định tính; chưa đánh giá site cụ thể** | QKD cần thiết bị/kênh lượng tử và kênh cổ điển xác thực; ML-KEM dùng hạ tầng tính toán/truyền thông cổ điển nhưng vẫn cần implementation, tích hợp protocol và quản lý khóa. Chưa có dữ liệu site, chi phí, khoảng cách hoặc vận hành để xếp hạng deployment. |
| Kiểm thử/tích hợp | **Đạt trong môi trường hiện tại, có skip tùy chọn** | 73 passed, 2 skipped; `git diff --check` đạt. Pylance không báo lỗi mới ở các file đã sửa; còn một số cảnh báo unused-variable ở file không thuộc thay đổi. |

## 5. Kiểm thử và xác minh

Môi trường: Windows, Python **3.14.2**, môi trường ảo `.venv`; dùng backend Matplotlib `Agg`.

Lệnh kiểm thử:

```powershell
$env:MPLBACKEND='Agg'
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider --basetemp "$env:TEMP\qkd-pqc-final2-20261124" -q
```

Kết quả: **73 passed, 2 skipped trong 7,09 giây**.

Hai test bị skip thuộc benchmark ML-KEM vì không tìm thấy package `pqcrypto` trong môi trường này.
Đây là trạng thái “chưa kiểm chứng backend/benchmark ở môi trường hiện tại”, không phải kết quả
benchmark bằng 0. `git diff --check` không phát hiện lỗi định dạng whitespace. Pylance workspace
không báo lỗi mới trong các file vừa sửa; các cảnh báo hiện có nằm ở import/tham số chưa dùng trong
các file khác.

## 6. Mức độ đáp ứng câu hỏi nghiên cứu

### Giả định bảo mật

Tài liệu và phần trade-off phân biệt trực giác/protocol QKD với giả định tính toán của ML-KEM, đồng
thời nêu yêu cầu xác thực kênh cổ điển, xác thực peer, bảo vệ endpoint và quản lý khóa. BB84 trong
repository là mô hình bit/basis giáo dục; `qber_threshold=0.11` và nhãn
`illustrative_accept` không phải chứng nhận an toàn. ML-KEM benchmark chỉ xác nhận hoạt động primitive
và không xác thực danh tính peer hay đánh giá an toàn của toàn hệ thống.

### Hiệu năng thiết lập khóa

ML-KEM được thiết kế để đo riêng key generation, encapsulation và decapsulation. Tuy nhiên, do
backend không được cài và không có raw CSV trong workspace, kỳ này **không tạo số latency ML-KEM
mới**. Thời gian BB84 chỉ là tốc độ xử lý simulator Python; không thể so sánh trực tiếp với latency
primitive ML-KEM hoặc diễn giải thành key rate QKD vật lý. Repository hiện cũng chưa đo handshake,
mạng, authentication hay hiệu năng đầu-cuối.

### Hạ tầng và tính phù hợp triển khai

So sánh hiện nêu điều kiện hạ tầng theo hướng định tính: QKD cần thiết bị/kênh lượng tử và authenticated
classical channel; ML-KEM có thể chạy trên hạ tầng tính toán/truyền thông cổ điển nhưng cần backend
được hỗ trợ, giao thức xác thực và key lifecycle phù hợp. Chưa có dữ liệu deployment cụ thể để kết
luận giải pháp nào phù hợp hơn cho một tổ chức, tuyến truyền hoặc ngân sách nhất định.

## 7. Việc còn mở và rủi ro

| Ưu tiên | Việc còn mở | Tiêu chí hoàn thành |
|---|---|---|
| Cao | Chạy kiểm thử và benchmark ML-KEM trên backend tương thích. | Capability check và round-trip shared secret đạt; test ML-KEM không bị skip; lưu raw CSV cùng implementation/version, platform, Python, warm-up và số lần đo; đối chiếu median/p95 từ CSV. |
| Cao | Xác minh provenance các bảng/ảnh ML-KEM đang được theo dõi trong Git. | Truy xuất được raw CSV và cấu hình tương ứng; nếu không có nguồn thì ghi rõ trạng thái/không dùng làm kết quả đo sau khi nhóm thống nhất cách xử lý. |
| Cao | Review độc lập báo cáo thí nghiệm BB84 và các claim bảo mật. | Có ghi nhận của reviewer khác về dữ liệu, công thức, nguồn tham khảo và giới hạn diễn giải. Chưa có bằng chứng review hoàn tất trong lần kiểm tra này. |
| Vừa | Quyết định chính sách artifact sinh tự động. | Nhóm quyết định giữ hay gỡ PNG/CSV comparison và 21 file `.pytest-tmp/` đang tracked; thực hiện thay đổi qua PR, không xóa dữ liệu khi chưa thống nhất. |
| Vừa | Quyết định phạm vi phát biểu về hiệu năng thiết lập khóa. | Hoặc giới hạn kết luận ở simulator/primitive và ghi rõ không phải end-to-end; hoặc bổ sung thiết kế đo có thể so sánh, dữ liệu nguồn và điều kiện môi trường phù hợp. |
| Vừa | Đánh giá tính phù hợp hạ tầng theo kịch bản cụ thể. | Xác định site/use case, thiết bị và kênh sẵn có, yêu cầu xác thực, endpoint, vận hành và chi phí; chỉ đưa ra kết luận khi có nguồn hoặc phép đo tương ứng. |

## 8. Kết luận

Trong kỳ 17–24/11, tiến độ đáng kể về độ tin cậy là làm cho pipeline phân tích không gộp nhầm các
phép đo hiệu năng khác runtime, không đếm lại export trùng và không gắn nhãn số liệu mô phỏng BB84
như kết quả QKD vật lý. Các thay đổi đã được kiểm thử với **73 passed, 2 skipped**, nhưng hiện vẫn
chưa commit.

Đề tài đã có cấu trúc để thảo luận ba trục chính — giả định bảo mật, hiệu năng simulator/primitive
và yêu cầu hạ tầng — nhưng bằng chứng hiệu năng ML-KEM cần được chạy lại trong môi trường có backend
và lưu raw CSV. Không có dữ liệu QKD phần cứng, benchmark đầu-cuối hoặc thông tin deployment site;
vì vậy báo cáo hiện không khẳng định QKD hay PQC nhanh hơn/an toàn hơn/phù hợp hơn một cách tổng quát.

## 9. Căn cứ

- Git: baseline báo cáo trước `f34f68d`; commit hiện tại `c8166f7`; các commit liên quan `13a3e66`,
  `036601b`, `0b2eff5`.
- Báo cáo trước: [PROGRESS_REPORT_2026-11-03.md](PROGRESS_REPORT_2026-11-03.md).
- Tích hợp và benchmark được báo cáo trước: [INTEGRATION_REPORT.md](INTEGRATION_REPORT.md).
- Phạm vi đề tài: [PROJECT_SCOPE.md](../docs/PROJECT_SCOPE.md).
- Giao thức thí nghiệm: [EXPERIMENT_PROTOCOL.md](../docs/EXPERIMENT_PROTOCOL.md).
- Từ điển dữ liệu: [DATA_DICTIONARY.md](../docs/DATA_DICTIONARY.md).
- Mã phân tích: [plotting.py](../src/qkd_pqc/analysis/plotting.py) và
  [tradeoff_analysis.py](../src/qkd_pqc/system/tradeoff_analysis.py).
- Kiểm thử: `tests/test_plotting.py`, `tests/test_tradeoff_analysis.py` và
  `tests/test_pipeline.py`; kết quả chạy tại workspace nêu ở Mục 5.
