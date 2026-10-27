# Báo cáo tiến độ dự án QKD_vs_PQC

**Ngày lập:** 20-10-2026  
**Mốc đánh giá:** `main` tại `2b690aa5371de94d444fe2ec23f00e1a1c3d2164` (trùng `origin/main`)  
**Baseline:** `0d8b5e5591a0c939da5078ef13439438361bb895` (`initial commit`)  
**Worktree khi kiểm tra:** nhánh `main`; có các mục `.pytest-tmp/` đang báo xóa. Đây là trạng thái cục bộ chưa commit và không được tính là nội dung của commit đánh giá.

## 1. Tóm tắt điều hành

**Trạng thái tổng thể: phần mềm và quy trình mô phỏng BB84 đã được mở rộng, có thể kiểm thử và có cohort lặp truy nguyên được; benchmark ML-KEM-768 chưa thực hiện thành công trong môi trường hiện tại.** Từ baseline, dự án bổ sung repeated sweeps BB84, phân tích tổng hợp mean/SD, báo cáo thí nghiệm, tài liệu tiếng Việt và hướng dẫn quy trình. Cohort BB84 được báo cáo gồm 140 trial trên 14 setting, và các số liệu chính được đối chiếu lại với 140 CSV cục bộ. Báo cáo BB84 vẫn **đang chờ review độc lập**.

Mã adapter ML-KEM-768 có kiểm tra API và shared secret, nhưng package `pqcrypto` tương thích không khả dụng: hai test benchmark bị skip và không có dữ liệu ML-KEM để kết luận về latency. Ảnh CDF ML-KEM đang được Git theo dõi nhưng không có CSV ML-KEM tương ứng để xác minh nguồn; không dùng ảnh đó làm bằng chứng benchmark. Worktree có xóa cục bộ các fixture trong `.pytest-tmp/`; các fixture này vốn được thêm vào lịch sử Git dù chính sách trong tài liệu nói output/test artifact sinh tự động không commit mặc định.

## 2. Baseline và phần bổ sung

`git log --oneline --reverse 0d8b5e5..2b690aa` cho thấy 8 commit sau baseline, gồm hai merge commit. So sánh toàn bộ lịch sử có 59 đường dẫn thay đổi (+2114/-517 dòng), nhưng số liệu này bao gồm file test artifact và dữ liệu/ảnh được theo dõi; không nên đọc như khối lượng mã sản phẩm thuần.

| Đã có tại baseline `0d8b5e5` | Được bổ sung sau baseline đến `2b690aa` |
|---|---|
| Cấu trúc package, config, một lần mô phỏng BB84 cổ điển, adapter ML-KEM, scripts chạy đơn/pipeline, phân tích trade-off, các test cơ sở và tài liệu phạm vi/giao thức/dữ liệu. | Thêm repeated sweep BB84 và trường channel loss; kiểm tra config/test mở rộng; lọc dữ liệu và tổng hợp biểu đồ/bảng; báo cáo BB84; tài liệu hướng dẫn sử dụng, workflow, code map, development, troubleshooting và đóng góp; Việt hóa/mở rộng tài liệu và cập nhật README/config. |

Các commit nội dung chính: `10cea18` (Việt hóa và tài liệu quy trình), `ab14865`/`8a642ba` (tham số mô phỏng và kiểm tra BB84), `45f564c`/`82a59dd` (đồ thị/phân tích), `c218e15` (sweep và đầu ra BB84), sau đó merge vào `main` tại `2b690aa`. Những thành phần nền như BB84 đơn, adapter ML-KEM và pipeline cơ sở không được tính nhầm là mới tạo trong giai đoạn này.

## 3. Tiến độ theo workstream

| Workstream | Trạng thái | Bằng chứng và giới hạn |
|---|---|---|
| BB84/QKD simulator | **Đã hoàn thành ở mức mô hình giáo dục** | `src/qkd_pqc/qkd/bb84_simulator.py` mô phỏng bit/basis, Eve intercept-resend, bit flip và loss Bernoulli. `src/qkd_pqc/qkd/experiment.py` chạy sweep độc lập và ghi seed từng trial; `scripts/run_qkd_experiment.py` cung cấp CLI. Đây không phải mô phỏng trạng thái lượng tử hay hệ thống QKD triển khai. |
| Repeated sweeps và cohort | **Đã hoàn thành; dữ liệu cục bộ xác minh được** | `configs/experiment_config.yaml`: 100.000 tín hiệu/trial, 10 repetition, 6 setting Eve, 5 noise, 5 loss; baseline chung nên là 14 setting/140 trial. Báo cáo ghi cohort ở `data/raw/qkd_20261019T1509*.csv`. 140 file tồn tại cục bộ và được kiểm tra seed/nhóm setting; raw CSV bị ignore, không được commit. |
| ML-KEM-768/PQC | **Có adapter; benchmark chưa thực hiện/không khả dụng** | `src/qkd_pqc/pqc/mlkem_benchmark.py` kiểm tra đúng module `pqcrypto.kem.ml_kem_768`, API và tính bằng nhau của shared secret trước khi đo; không thay bằng thuật toán khác. Hai test benchmark skip do dependency không có. Không tìm thấy `data/raw/mlkem_*.csv`; vì vậy không có latency đã xác minh. |
| Phân tích và biểu đồ | **Mã và test hoàn thành; một artifact chưa rõ provenance** | `src/qkd_pqc/analysis/plotting.py` tổng hợp theo setting, tránh trộn cấu hình và tính mean/sample SD. Ba CSV so sánh được commit (`data/processed/`), nội dung là so sánh định tính có nhãn `qualitative_reference_based`. Ba PNG QKD (Eve, channel error và sifted fraction theo channel error) được Git theo dõi dù raw nguồn bị ignore; PNG loss hiện có trong workspace nhưng không được theo dõi. Báo cáo BB84 mô tả cách tạo lại từ cohort. `figures/mlkem_latency_cdf.png` không có CSV ML-KEM đi kèm trong workspace nên provenance chưa xác minh. |
| Kiểm thử/tái lập | **Đã kiểm tra; có giới hạn môi trường** | Với Python trong `.venv`, pytest chạy thành công ở chế độ Agg: 50 passed, 2 skipped. Skip chỉ ở hai test ML-KEM vì thiếu `pqcrypto`. Lệnh pytest mặc định không đặt backend có 3 lỗi test đồ thị vì Matplotlib chọn Tk nhưng Tcl/Tk thiếu; chi tiết tại mục 6. |
| Tài liệu/quy trình | **Đã hoàn thành phần tài liệu; báo cáo BB84 chờ review** | README, scope, protocol, dictionary, team assignments, workflow, user guide, config và reports README được cập nhật/thêm. `reports/QKD_BB84_EXPERIMENT.md` ghi rõ giới hạn giáo dục, cohort, nguồn và trạng thái chờ review. |

## 4. Kết quả định lượng BB84 đã xác minh

Đối chiếu được thực hiện trên đúng 140 file `data/raw/qkd_20261019T1509*.csv` tại workspace, không gộp các setting. Mỗi CSV có một dòng; có 140 seed duy nhất từ 42 đến 201. `mean ± SD` là trung bình và độ lệch chuẩn mẫu trên 10 trial tại mỗi setting. Các giá trị sau khớp `reports/QKD_BB84_EXPERIMENT.md` và phép tính lại từ CSV:

| Sweep / setting | Chỉ số | Mean ± SD (10 trial) | Kỳ vọng mô hình |
|---|---|---:|---:|
| Eve `p=1.00`, noise/loss `=0` | QBER | 0,250174 ± 0,001481 | 0,250000 |
| Eve `p=0,75`, noise/loss `=0` | QBER | 0,188014 ± 0,000906 | 0,187500 |
| Eve `p=0,50`, noise/loss `=0` | QBER | 0,124582 ± 0,001083 | 0,125000 |
| Eve `p=0,25`, noise/loss `=0` | QBER | 0,062529 ± 0,000914 | 0,062500 |
| Eve `p=0,10`, noise/loss `=0` | QBER | 0,024797 ± 0,000563 | 0,025000 |
| Eve `p=0`, noise/loss `=0` | QBER | 0,000000 ± 0,000000 | 0 |
| Noise `e=0,01/0,05/0,10/0,20`, Eve/loss `=0` | QBER lần lượt | 0,010178 ± 0,000472; 0,050358 ± 0,000660; 0,099328 ± 0,001994; 0,200168 ± 0,001228 | Lần lượt 0,01; 0,05; 0,10; 0,20 |
| Loss `l=0,80`, Eve/noise `=0` | Tín hiệu Bob nhận / gửi | 0,199682 | 0,200000 |
| Loss `l=0,80`, Eve/noise `=0` | Sifted fraction | 0,099929 ± 0,000577 | 0,100000 |

Các tỷ lệ không có đơn vị. Với loss sweep QBER bằng 0 vì Eve và noise bằng 0. Không diễn giải các số trên thành tỷ lệ khóa bí mật cuối cùng hay chứng nhận an toàn; `qber_threshold=0,11` và `illustrative_accept` chỉ là nhãn minh họa của mô hình.

## 5. Kiểm thử và tích hợp

Lệnh chạy kiểm chứng thành công:

```powershell
$env:MPLBACKEND='Agg'
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider --basetemp "$env:TEMP\qkd-pqc-report-pytest-agg" -q
```

Kết quả: **50 passed, 2 skipped**. Hai skip là `tests/test_mlkem_benchmark.py:27` và `:52`, do không có implementation `pqcrypto` ML-KEM-768 được xác minh. `MPLBACKEND=Agg` chọn backend không giao diện để test sinh hình trên môi trường thiếu Tcl/Tk.

Chạy cùng pytest nhưng không đặt backend đồ họa cho kết quả **47 passed, 3 failed, 2 skipped**: cả ba lỗi tại các test vẽ hình (`test_plotting_creates_only_data_supported_figures`, `test_plotting_does_not_count_duplicate_seeded_runs_as_repetitions`, `test_plotting_omits_averages_across_mixed_qkd_settings`) xuất phát từ Matplotlib chọn Tk và Python không tìm thấy `init.tcl`. Đây là giới hạn môi trường hiện tại; không phải lỗi khẳng định của phép tính, nhưng test mặc định cần backend phù hợp hoặc cài Tcl/Tk. Không thấy PytestCacheWarning trong các lệnh trên vì đã tắt cache provider; báo cáo cũ ghi cảnh báo Windows cache từ một lần chạy khác.

## 6. Giới hạn và rủi ro diễn giải

- BB84 là mô hình xác suất bit/basis cổ điển. Không có trạng thái lượng tử, phần cứng quang, detector/side channel, xác thực kênh cổ điển, error correction, privacy amplification, finite-key analysis hay security proof.
- Benchmark ML-KEM có mã nhưng chưa có lần đo hợp lệ trong workspace. Không đưa ra latency, throughput hay kết luận nhanh/chậm. QBER và latency là đại lượng khác loại, không so sánh trực tiếp.
- Các ảnh QKD đang được theo dõi trong Git trong khi CSV raw/processed và PNG lại bị `.gitignore` bỏ qua theo tài liệu/README. `figures/mlkem_latency_cdf.png` và các fixture dưới `.pytest-tmp/` cũng được theo dõi; fixture hiện báo xóa ở worktree. Đây là **điểm cần xác minh chính sách có chủ ý hay không**. Ảnh không thay thế dữ liệu nguồn.
- Ba CSV `data/processed/comparison_*.csv` được theo dõi là nội dung so sánh định tính; không phải bảng latency. Cohort raw QKD hiện xác minh được ở workspace nhưng không được Git bảo toàn mặc định, nên khả năng tái lập độc lập từ clone sạch bị hạn chế nếu không lưu trữ cohort hoặc tạo lại.
- Các ghi nhận số lượng/thống kê commit ở trên bao gồm tài liệu, test và artifact; không phải chỉ số phần trăm hoàn thành.

## 7. Công việc tiếp theo ưu tiên

| Ưu tiên | Việc cần làm | Tiêu chí hoàn thành kiểm chứng được | Phụ thuộc/trạng thái |
|---|---|---|---|
| Cao | Review độc lập `reports/QKD_BB84_EXPERIMENT.md` | Review được ghi nhận; xác minh lại 140 trial, cohort, công thức mean/sample SD, giới hạn và provenance; xử lý nhận xét trước khi đổi trạng thái báo cáo. | Đang chờ reviewer; chưa có bằng chứng review hoàn tất. |
| Cao | Xác minh/chốt chính sách output sinh tự động | Đối chiếu `.gitignore` với `git ls-files`; quyết định rõ artifact nào cần commit để tái lập và artifact nào chỉ sinh cục bộ. Xử lý ảnh ML-KEM và fixture `.pytest-tmp` theo chính sách đã thống nhất. | Hiện trạng Git không nhất quán với mô tả mặc định bỏ qua output. |
| Cao | Chạy benchmark ML-KEM-768 trên backend tương thích | Cài/khóa implementation phù hợp; test capability pass, shared secret khớp; chạy benchmark và lưu CSV có version/platform, warmup và số lần đo; chỉ khi đó mới báo cáo median/p95 từ CSV. | Bị chặn hiện tại do `pqcrypto` tương thích chưa cài/khả dụng. |
| Vừa | Làm ổn định test biểu đồ trên Windows | Thiết lập backend Agg cho CI/test hoặc cung cấp Tcl/Tk; lệnh test chuẩn kết thúc 0 lỗi trên môi trường hỗ trợ và báo cáo rõ cấu hình. | Đã qua với `MPLBACKEND=Agg`; pytest mặc định vẫn lỗi môi trường. |
| Vừa | Cải thiện lưu provenance của cohort | Quy định cách lưu cohort được review (artifact phát hành hoặc kho dữ liệu có version/hash) và ghi hash/danh sách file trong báo cáo; đảm bảo có thể tái tạo bảng từ dữ liệu gốc. | CSV hiện có cục bộ, bị ignore; cần quyết định chính sách dữ liệu. |

## 8. Kết luận

Đến `2b690aa`, dự án đã có mô phỏng BB84 giáo dục, sweep lặp tái lập, phân tích theo setting, kiểm thử mở rộng và hướng dẫn sử dụng/tái lập. Cohort BB84 trong workspace có thể truy nguyên và các số liệu tóm tắt chính đã được xác minh. Chưa thể kết luận hiệu năng ML-KEM-768 vì chưa có benchmark thành công; báo cáo BB84 cần review độc lập; provenance của ảnh/fixture đang theo dõi Git cần được làm rõ. Không có căn cứ từ trạng thái này để đưa ra kết luận an toàn triển khai hoặc so sánh trực tiếp QKD/PQC bằng một thước đo chung.

## 9. Căn cứ đã đối chiếu

- Git: `0d8b5e5` (baseline), lịch sử `0d8b5e5..2b690aa`, `HEAD`/`origin/main` tại `2b690aa`; trạng thái worktree trên `main`.
- Tài liệu: `README.md`; `docs/PROJECT_SCOPE.md`; `docs/EXPERIMENT_PROTOCOL.md`; `docs/DATA_DICTIONARY.md`; `docs/TEAM_ASSIGNMENTS.md`; `docs/WORKFLOW.md`; `docs/USER_GUIDE.md`; `reports/README.md`; `reports/QKD_BB84_EXPERIMENT.md`.
- Cấu hình/mã: `configs/experiment_config.yaml`; `src/qkd_pqc/qkd/bb84_simulator.py`; `src/qkd_pqc/qkd/experiment.py`; `src/qkd_pqc/pqc/mlkem_benchmark.py`; `src/qkd_pqc/analysis/plotting.py`; `scripts/run_qkd_experiment.py`; `scripts/run_pqc_benchmark.py`.
- Kiểm thử: `tests/` toàn bộ; chạy tại workspace bằng Python trong `.venv` như lệnh mục 5.
- Dữ liệu/artefact: 140 CSV cục bộ `data/raw/qkd_20261019T1509*.csv`; `data/processed/comparison_20261019T152019_57ca8cb3.csv`; các CSV so sánh định tính tracked; PNG trong `figures/`. Không có CSV benchmark `mlkem_*.csv` để xác minh ảnh latency.
