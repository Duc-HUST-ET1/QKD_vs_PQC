# Nhật ký tiến độ QKD_vs_PQC

## Tuần 11 · cập nhật đến 27/11/2026

**Từ mốc 24/11, nhóm đã lưu các sửa đổi phân tích của tuần 10 trên nhánh riêng, gỡ fixture pytest khỏi Git trên nhánh trade-offs và có thêm một raw CSV BB84 ngày 27/11.** Việc đối chiếu tuần này xác nhận các số latency ML-KEM từ ba CSV tháng 10 và đầu tháng 11. Chưa có raw của một benchmark ML-KEM mới trong kỳ 25–27/11. Các số liệu và run ID đầy đủ nằm trong [ngữ cảnh dự án](PROJECT_CONTEXT.md).

### Mốc đối chiếu ngày 24/11

Nguồn chính là bản PDF *Nhóm 12_Tuần 10_Báo cáo.docx.pdf* do nhóm cung cấp, kỳ 17–24/11, mục 1, 3, 5 và 7. Bản này mô tả checkout `feature/qkd` tại `c8166f7`, cùng commit với main khi đó. PR #10 đã merge. Tại thời điểm viết, nhóm báo cáo đã sửa cách đếm timing BB84 theo run ID, khử trùng mẫu ML-KEM theo bộ ba (run ID, thao tác, iteration), tách cohort runtime và đổi nhãn số đo BB84. Các thay đổi lúc ấy chưa commit. Nhóm báo cáo **73 passed, 2 skipped** trên Windows, Python 3.14.2, thiếu pqcrypto và thiếu raw ML-KEM tại máy lập báo cáo. [Bản Markdown trên nhánh của nhóm](https://github.com/Duc-HUST-ET1/QKD_vs_PQC/blob/146687f/reports/PROGRESS_REPORT_2026-11-24.md)

### Những thay đổi có bằng chứng sau mốc báo cáo

| Mốc | Đã xác minh | Ý nghĩa cho tuần 11 |
|---|---|---|
| 24/11, sau khi lập báo cáo | GitHub ghi commit `146687f` trên `feature/qkd` lúc 14:51 UTC. Diff với main có mã phân tích, nhãn trade-off, ba test hồi quy mô tả trong PDF, tài liệu và báo cáo 24/11. | Công việc tuần 10 đã có commit để review. Ngày 27/11 nhánh này đi trước main một commit. Chưa có bằng chứng đã tích hợp các sửa đó vào main hoặc checkout dùng để kiểm tra tuần 11. |
| 27/11, Git | `66e687c` gỡ 21 đường dẫn fixture khỏi Git trên `feature/system-tradeoffs`. `git ls-files -- .pytest-tmp` rỗng trên nhánh này. | Đã xử lý phần fixture trên một nhánh. PR #10 chỉ merge đến head `0b2eff5`. Quyết định chung về các PNG và CSV được theo dõi vẫn mở. |
| 27/11, BB84 | Raw `qkd_20261127T150032_8e76e66e.csv` cho 484/49.990 bit lỗi sau sifting, QBER ≈ 0,9682%. Cấu hình và số đếm trùng raw ngày 17/11. Vòng lặp mới mất 220.778,3 µs cho 100.000 tín hiệu. | Có thêm một quan sát timing trên máy chạy. Cùng seed/cấu hình chỉ đóng góp một kết quả QBER xác định. Hai lần timing chưa đủ để kết luận có cải thiện hiệu năng. |
| 27/11, bảng tổng hợp | SHA-256 của hai file `data/processed/comparison_20261117T153823_a1175778.csv` và `comparison_20261127T150039_832243fe.csv` trùng nhau. Bảng ghi 7 dòng QKD sau khử trùng, 7 setting theo mã hiện tại và 1 dòng timing, 520.126,1 µs của ngày 17/11. | `run_analysis.py` sắp xếp đường dẫn, `_unique_qkd_runs` giữ dòng đầu theo seed/cấu hình trước khi tính timing. Điều này giải thích vì sao bảng ngày 27/11 thiếu timing mới dù raw còn nguyên. Các CSV cũ thiếu trường loss, nên cần xét cả schema khi diễn giải số setting. |
| 27/11, ML-KEM | Tính lại median và p95 từ 9.000 dòng raw. Mỗi thao tác có 3.000 mẫu gộp thuộc ba run cùng metadata đã ghi. Median/p95 gộp (µs) lần lượt là 588,90/3.732,8 cho keygen, 584,55/2.883,8 cho encaps, 163,15/514,9 cho decaps. | Khớp bảng mới. Các số riêng trong bảng 25/10 cũng khớp raw 19/10. Việc khớp số chỉ xác nhận phần thống kê ML-KEM. Giá trị `mean_qber` gộp 6 cấu hình trong bảng 25/10 không phù hợp để báo cáo cho một cấu hình. |
| 27/11, kiểm thử | Chạy suite tại `66e687c` bằng Python 3.13.14, đạt **70 passed, 2 skipped**. Hai test ML-KEM thật bị skip. Module pqcrypto 0.4.0 cài tại đây có API khác các callable adapter yêu cầu. | Suite lịch sử 73/2 và suite 70/2 ứng với hai cây mã và môi trường khác nhau. Ba test hồi quy của `146687f` vắng trên nhánh này. Chưa xác minh chạy backend thật trên HEAD hiện hành. |
| 27/11, bàn giao | Bổ sung `AGENTS.md`, bản ngữ cảnh hiện hành và nhật ký theo mốc có đường dẫn nguồn. | Phiên sau có thể tra cứu quy tắc, kiểm thử, dữ liệu và việc mở ngay trong repository khi các tài liệu được chia sẻ. |

**Phạm vi của bằng chứng.** Raw và các bảng tháng 11 có mặt tại workspace rà soát, mặc định bị Git bỏ qua. Tệp CDF đã có thay đổi cục bộ trước đợt bàn giao. Chưa có manifest ánh xạ từng PNG đến danh sách CSV, cấu hình và phiên bản mã đã dùng để vẽ. Các nhận định định tính về hạ tầng và xác thực được giữ riêng với kết quả đo. [Mã phân tích ở checkout](../src/qkd_pqc/analysis/plotting.py) · [PR #10](https://github.com/Duc-HUST-ET1/QKD_vs_PQC/pull/10)

### Việc tiếp theo từ danh sách tuần 10

Các vai trò dưới đây theo [phân công repository](TEAM_ASSIGNMENTS.md). Việc phê duyệt tích hợp và chính sách dữ liệu thuộc về nhóm.

| Việc còn mở | Vai trò phối hợp | Dấu hiệu hoàn tất |
|---|---|---|
| Review thay đổi phân tích trên `146687f` và fixture trên `66e687c` | TV3, TV4, TV5 | Có quyết định cho từng nhánh và bằng chứng test trên commit đích. Phép thử hai timing khác run ID/cùng seed giữ đủ timing và chỉ đếm một kết quả QBER. |
| Xác minh backend ML-KEM với mã cần công bố | TV2, TV5 | Capability check và test round trip/export thực sự chạy. Nếu nhóm thực hiện benchmark mới, lưu run ID, metadata và CSV theo từng thao tác. |
| Hoàn thiện provenance của bảng và hình, thống nhất artifact chia sẻ | TV2, TV3, TV5 | Mỗi artifact công bố truy được đúng tập raw, cấu hình, phiên bản mã và lệnh phân tích. Clone mới truy cập được bằng chứng đã duyệt. |
| Review độc lập BB84 và claim bảo mật | TV1, TV4 và reviewer khác người lập | Có ghi nhận kiểm tra cohort 140 trial, công thức, nguồn và giới hạn bằng văn bản. |
| Chốt phạm vi kết luận hệ thống | TV4, TV5 | Báo cáo giới hạn số đo ở simulator/primitive. Kết luận về handshake, site, cự ly hoặc chi phí chỉ bổ sung khi có thiết kế đo và dữ liệu phù hợp. |
