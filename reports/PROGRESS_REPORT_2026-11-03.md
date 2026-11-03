# Báo cáo tiến độ tuần QKD_vs_PQC

**Kỳ báo cáo:** 28/10–03/11/2026  
**Mốc đánh giá:** `main` @ `f34f68d` (03/11/2026)  
**Mốc tuần trước:** `main` @ `4274ecf` (27/10/2026)  
**Worktree trước khi lập báo cáo:** sạch; không có thay đổi mã nguồn chưa commit.

## 1. Tóm tắt điều hành

Trong kỳ này, thay đổi đã merge là hoàn thiện báo cáo tích hợp qua PR #7; không có commit tính năng
hoặc sửa mã nguồn trong khoảng 28/10–03/11. Khi rà soát lại, phát hiện README, giao thức thí nghiệm
và hướng dẫn phát triển vẫn mô tả sai API backend ML-KEM. Ba tài liệu đã được đồng bộ với adapter
hiện tại; báo cáo này ghi lại tình trạng code và các việc còn mở.

Toàn bộ test không phụ thuộc backend ML-KEM chạy thành công: **67 passed, 2 skipped**. Hai test
được skip do môi trường hiện tại không cài `pqcrypto`; do đó chưa tái chạy được benchmark ML-KEM
trên checkout/môi trường này. Không có số đo mới được tạo trong kỳ và không dùng số liệu cũ như
kết quả tái xác minh.

**Kết luận:** các thành phần lõi BB84, phân tích, trade-off và pipeline đã có code/test tương ứng.
Không tìm thấy TODO/FIXME triển khai còn bỏ ngỏ trong source; điều này không thay thế review độc lập.
Các điểm chưa thể tự hoàn tất là review báo cáo BB84, xác minh nguồn các artifact benchmark đã
được theo dõi trong Git, quyết định chính sách artifact/fixture, và chạy lại ML-KEM với dependency
tương thích.

## 2. Thay đổi và xác minh trong tuần

### Đã merge trong kỳ

Git history từ 28/10 đến 03/11 chỉ có PR #7, một thay đổi tài liệu:

- `reports/INTEGRATION_REPORT.md`: hoàn thiện báo cáo tích hợp sau khi merge PR #3–#6.
- Không có thay đổi code tính năng/test trong commit tuần này.

### Hoàn thành khi rà soát

- Cập nhật [README.md](../README.md), [EXPERIMENT_PROTOCOL.md](../docs/EXPERIMENT_PROTOCOL.md)
  và [DEVELOPMENT_GUIDE.md](../docs/DEVELOPMENT_GUIDE.md): phân biệt API backend
  `keygen`/`encaps`/`decaps` với API wrapper nội bộ `generate_keypair`/`encrypt`/`decrypt`.
- Kiểm tra source/test và xác nhận test suite hiện có chạy được trong môi trường hiện tại.
- Không sửa/xóa dữ liệu, fixture `.pytest-tmp`, hay artifacts tracked khi provenance/quyết định nhóm
  chưa được xác nhận.

### Kết quả kiểm thử tại checkout hiện tại

Lệnh đã chạy trên Windows với Python 3.14.2, backend Matplotlib `Agg`:

```powershell
$env:MPLBACKEND='Agg'
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider --basetemp "$env:TEMP\qkd-pqc-weekly-20261103" -q
```

Kết quả: **67 passed, 2 skipped trong 18,27 giây**. Hai test tại
`tests/test_mlkem_benchmark.py` skip vì optional implementation `pqcrypto.kem.ml_kem_768` không
được cài. Vì vậy test này xác nhận suite trong môi trường sẵn có, không xác nhận benchmark thật.

## 3. Trạng thái theo thành viên/workstream

| Workstream | Trạng thái tại 03/11 | Bằng chứng và phần còn mở |
|---|---|---|
| Thành viên 1 — BB84/QKD | **Code/test đã có; review báo cáo còn mở** | Simulator, repeated sweep, CSV và test hiện có. Báo cáo cohort 140 trial nằm tại `reports/QKD_BB84_EXPERIMENT.md`; báo cáo vẫn ghi chờ review độc lập. Không có bằng chứng review hoàn tất trong thay đổi tuần này. |
| Thành viên 2 — ML-KEM-768/PQC | **Adapter đã có; benchmark chưa tái xác minh tại môi trường này** | Adapter kiểm tra implementation cụ thể và shared-secret round-trip. Hai test tùy chọn skip vì thiếu `pqcrypto`. `reports/INTEGRATION_REPORT.md` ghi benchmark thành công ở môi trường khác, nhưng raw CSV đó không có trong checkout để tái kiểm tra. |
| Thành viên 3 — Phân tích/biểu đồ | **Code/test có; provenance artifact cũ cần giải quyết** | Phân tích hiện có test và hỗ trợ cohort. Một số CSV/PNG được theo dõi trong Git không có raw source đủ để tái xác minh; không thể xác nhận các số đo đó chỉ từ ảnh hoặc CSV tổng hợp. |
| Thành viên 4 — Threat model/trade-offs | **Code/tài liệu/test có; cần tiếp tục review nguồn và claim** | Trade-off gắn nhãn loại evidence và nêu giới hạn phạm vi. Cần reviewer xác nhận claim và provenance trước khi dùng làm kết luận nghiên cứu. |
| Thành viên 5 — Tích hợp/config/test | **Pipeline/test có; policy artifact còn mở** | Pipeline và test tích hợp có sẵn; suite hiện tại đạt 67/2. Có 21 đường dẫn `.pytest-tmp/` còn tracked; `.gitignore` không tự gỡ file đã tracked. Việc giữ/gỡ cần quyết định và PR riêng. |

## 4. Các việc còn mở cần chủ sở hữu/nhóm xác nhận

| Ưu tiên | Việc cần làm | Điều kiện hoàn tất |
|---|---|---|
| Cao | Chạy test ML-KEM và pipeline với backend thật tương thích. | Cài extra đã khai báo `.[mlkem,dev]` trong môi trường dự án; chạy test và benchmark; lưu raw CSV cùng version/platform/config; đối chiếu median/p95. Không thay bằng thuật toán khác. |
| Cao | Xác minh provenance các số ML-KEM và artifact đã commit. | Cung cấp raw CSV, thông tin máy/backend/cohort và nguồn; hoặc thay artifact bằng output có nguồn kiểm chứng được. Hiện không kết luận số liệu nào đại diện cho benchmark có thể tái lập. |
| Cao | Review độc lập báo cáo BB84. | Reviewer khác ghi kết quả và các chỉnh sửa (nếu có) trong báo cáo; không tự đánh dấu review hoàn tất. |
| Vừa | Quyết định chính sách `.pytest-tmp/`, PNG và CSV processed đã tracked. | Nhóm quyết định giữ hay gỡ; thực hiện thay đổi index qua PR riêng. Không xóa/khôi phục file trong kỳ rà soát này. |
| Vừa | Hoàn tất checklist nghiệm thu của từng workstream. | Owner xác nhận checklist và cập nhật trạng thái sau review; checklist trong `docs/TEAM_ASSIGNMENTS.md` hiện là ranh giới trách nhiệm, không phải bằng chứng mọi việc đã được review. |

## 5. Rủi ro và giới hạn diễn giải

- ML-KEM benchmark trong báo cáo tích hợp là kết quả từ một môi trường khác; chưa có raw CSV tại
  checkout để xác minh độc lập. Không đưa số latency đó ra như phép đo tuần này.
- QBER của mô phỏng BB84 không phải độ trễ ML-KEM; mô hình BB84 hiện tại là mô hình giáo dục cổ
  điển, không chứng minh tính an toàn của QKD thực tế.
- Ảnh hoặc comparison CSV không thay thế raw measurements, cấu hình, metadata và provenance.
- Không có thay đổi thuật toán/cấu hình thực nghiệm trong kỳ; không tạo cohort mới, không chạy lại
  benchmark ML-KEM và không có số liệu mới để kết luận hiệu năng.

## 6. Kế hoạch đề xuất cho tuần tới

1. **Thành viên 2 + Thành viên 5 (cần xác nhận owner):** trong môi trường có `pqcrypto`, chạy
   test ML-KEM và pipeline; lưu raw CSV cùng metadata và đối chiếu kết quả. Không đưa dữ liệu vào
   báo cáo cho tới khi kiểm tra được nguồn.
2. **Reviewer độc lập (chưa xác định):** đọc báo cáo BB84, ghi nhận kết quả và các chỉnh sửa cần
   thiết.
3. **Cả nhóm:** quyết định chính sách giữ/gỡ fixture `.pytest-tmp` và generated artifacts đã
   tracked; thực hiện bằng PR riêng sau khi thống nhất.
4. **Thành viên 3 + Thành viên 4 (cần xác nhận owner):** kiểm tra provenance và wording của
   comparison CSV/figures trước khi dùng làm bằng chứng trong báo cáo nghiên cứu.

## 7. Prompt dùng để tạo bản báo cáo DOC

> Hãy chuyển nội dung báo cáo Markdown này thành báo cáo tiến độ tuần bằng tiếng Việt, giữ nguyên
> kỳ báo cáo 28/10–03/11/2026, mốc `main` @ `f34f68d`, và mọi số liệu kiểm thử theo đúng ngữ cảnh:
> lần kiểm tra checkout ban đầu 67 passed/2 skipped, lần kiểm tra sau bổ sung scope 70 passed/2
> skipped. Dùng cấu trúc gồm:
> tóm tắt điều hành, thay đổi trong tuần, trạng thái theo 5 thành viên, kiểm thử, việc còn mở,
> rủi ro/giới hạn và kế hoạch tuần tới. Trình bày các bảng dễ đọc, giải thích skip là do thiếu
> `pqcrypto`; không biến kết quả benchmark từ môi trường khác thành kết quả mới. Giữ nguyên phân
> biệt giữa API backend và wrapper nội bộ, không tự bịa tên
> người review, số đo, ngày chạy, tiến độ hoặc quyết định của nhóm. Kết thúc bằng danh sách hành
> động, owner để trống nếu chưa có xác nhận, và tiêu chí nghiệm thu cho từng việc.

## Bổ sung sau khi đối chiếu trực tiếp với câu hỏi nghiên cứu

Sau mốc checkout ở đầu báo cáo, rà soát câu hỏi nghiên cứu cho thấy benchmark primitive ML-KEM và
các chỉ số QBER/sifting của BB84 chưa tạo thành phép so sánh hiệu năng thiết lập khóa đầu-cuối.
Code hiện ghi thêm thời gian vòng lặp Python và số tín hiệu mô phỏng mỗi giây, nhưng đây chỉ là
benchmark simulator, không phải physical QKD key rate. Bảng trade-off cũng nêu rõ yêu cầu hạ tầng
và điều kiện định tính; repository không có dữ liệu để kết luận deployment cụ thể phù hợp hơn.

Thay đổi bổ sung hiện ở worktree, chưa merge: `src/qkd_pqc/qkd/bb84_simulator.py`,
`src/qkd_pqc/analysis/plotting.py`, trade-off analysis, CSV schema/tests và tài liệu liên quan.
Kiểm thử lại sau các thay đổi này: **70 passed, 2 skipped**; hai skip vẫn do thiếu `pqcrypto`.
Không có benchmark ML-KEM mới hoặc số liệu QKD phần cứng được tạo.
