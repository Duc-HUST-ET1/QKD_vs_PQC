# Báo cáo thí nghiệm BB84 (QKD)

**Trạng thái:** kết quả được sinh từ mô phỏng; chờ thành viên khác review.
**Phạm vi:** mô phỏng BB84 giáo dục dạng bit/basis; không phải triển khai QKD hoặc khóa bí mật an toàn.

## Mục tiêu và phương pháp

Đo ảnh hưởng riêng của xác suất Eve intercept-resend, lỗi lật bit trên kênh và mất tín hiệu lên
QBER/tỷ lệ sifting. Cấu hình dùng `configs/experiment_config.yaml`: 100.000 tín hiệu mỗi lần
chạy, seed gốc 42, 10 repetitions mỗi setting. Có 6 setting Eve, 5 setting noise và 5 setting
loss; baseline `[Eve=0, noise=0, loss=0]` dùng chung, nên tổng cộng 14 setting độc lập và 140
trial. Mỗi trial có seed duy nhất được ghi trong CSV; cohort này có seed từ 42 đến 201.

Run CSV cohort: `data/raw/qkd_20261019T1509*.csv` (140 file, mỗi file có header và một dòng dữ liệu).
Comparison CSV: `data/processed/comparison_20261019T152019_57ca8cb3.csv` (10 data rows và header;
ghi `setting_count=14`, `valid_run_rows=140`, không gộp mean qua nhiều kịch bản).
Để tạo lại các hình chỉ từ cohort này, tránh trộn dữ liệu raw cũ:

```powershell
.\.venv\Scripts\python.exe scripts\run_qkd_experiment.py --config configs\experiment_config.yaml
.\.venv\Scripts\python.exe scripts\run_analysis.py --config configs\experiment_config.yaml --qkd-run-prefix qkd_<UTC-run-prefix>
```

Thay `<UTC-run-prefix>` bằng prefix `qkd_...` được CLI sweep in ra. Đầu ra hình:

- `figures/qber_vs_eve_probability.png`
- `figures/qber_vs_channel_error_rate.png`
- `figures/sifted_fraction_vs_channel_error_rate.png`
- `figures/sifted_fraction_vs_channel_loss_rate.png`

Đường trung bình và error bar thể hiện mean ±1 sample standard deviation của 10 trial tại mỗi
setting. Run có cùng seed, cấu hình và phiên bản mô phỏng được tính một lần, không coi các lần
xuất lặp của cùng deterministic run là quan sát độc lập.

## Mô hình và định nghĩa

Alice chọn bit/basis ngẫu nhiên. Tín hiệu bị loại theo channel loss trước khi tới Bob; Eve chỉ
chặn tín hiệu còn lại, chọn basis ngẫu nhiên, đo và gửi lại trạng thái theo kết quả đo. Channel
bit flip được áp dụng độc lập một lần sau Eve. Bob chọn basis ngẫu nhiên; chỉ tín hiệu đến Bob mà
basis Alice/Bob khớp mới được sift.

- `QBER = error_bits / sifted_bits`; không có sifted bit thì QBER không xác định (CSV rỗng).
- `sifted_fraction = sifted_bits / n_signals`.
- `loss_fraction = lost_signals / n_signals`.
- Với noise `e` và xác suất intercept `p`, QBER kỳ vọng theo mô hình độc lập là
  `e + (1 - 2e) * p / 4`.
- Với loss `l` độc lập, tỷ lệ tín hiệu đến Bob kỳ vọng `1-l`; sifted fraction kỳ vọng `(1-l)/2`.

Đây là xác suất bit/basis cổ điển, không mô phỏng state vector, phần cứng, kênh quang, detector,
side channel hay mọi tấn công lượng tử. Không có xác thực kênh cổ điển, error correction,
information reconciliation, privacy amplification, finite-key analysis hoặc composable security
proof. `illustrative_accept` không phải khẳng định an toàn; số bit sifted không phải khóa bí mật
cuối cùng. Mất tín hiệu được mô hình hóa bằng Bernoulli độc lập, không phải optical attenuation.

## Kết quả quan sát

Các giá trị dưới đây được tính từ đúng 140 CSV cohort, không gồm CSV khác trong `data/raw/`.
`mean ± SD` là tỷ lệ thực đo qua 10 trial; giá trị kỳ vọng là đối chiếu lý thuyết, không phải dữ
liệu được nhập vào simulator.

### QBER theo Eve

| Eve probability | QBER mean ± SD | Kỳ vọng `p/4` |
|---:|---:|---:|
| 0.00 | 0.000000 ± 0.000000 | 0.000000 |
| 0.10 | 0.024797 ± 0.000563 | 0.025000 |
| 0.25 | 0.062529 ± 0.000914 | 0.062500 |
| 0.50 | 0.124582 ± 0.001083 | 0.125000 |
| 0.75 | 0.188014 ± 0.000906 | 0.187500 |
| 1.00 | 0.250174 ± 0.001481 | 0.250000 |

QBER quan sát tăng theo xác suất Eve; intercept-resend toàn phần đạt xấp xỉ 25% như kỳ vọng.

### QBER theo channel noise

| Bit-flip probability | QBER mean ± SD | Kỳ vọng `e` |
|---:|---:|---:|
| 0.00 | 0.000000 ± 0.000000 | 0.000000 |
| 0.01 | 0.010178 ± 0.000472 | 0.010000 |
| 0.05 | 0.050358 ± 0.000660 | 0.050000 |
| 0.10 | 0.099328 ± 0.001994 | 0.100000 |
| 0.20 | 0.200168 ± 0.001228 | 0.200000 |

QBER quan sát theo sát xác suất bit flip cấu hình.

### Channel loss và sifted fraction

| Loss probability | Bob received / sent mean | Sifted fraction mean ± SD | Kỳ vọng sifted fraction |
|---:|---:|---:|---:|
| 0.00 | 1.000000 | 0.499788 ± 0.001510 | 0.500000 |
| 0.10 | 0.899831 | 0.449430 ± 0.001335 | 0.450000 |
| 0.30 | 0.699848 | 0.349431 ± 0.001172 | 0.350000 |
| 0.50 | 0.499447 | 0.249090 ± 0.001092 | 0.250000 |
| 0.80 | 0.199682 | 0.099929 ± 0.000577 | 0.100000 |

Mất tín hiệu làm giảm số tín hiệu nhận và sifted fraction; không làm tăng lỗi bit. Mọi trial
trong loss sweep có QBER 0 do Eve và channel noise bằng 0.

### Smoke test single-run

`python scripts/run_qkd.py` sinh `qkd_20261019T151402_a53cba6b.csv`: seed 42, 100.000 tín hiệu,
100.000 tín hiệu nhận, 49.990 bit sifted, 484 bit lỗi, QBER `0.0096819364` (xấp xỉ channel noise
0.01). Đây là một run đơn, không dùng thay cho các mean/SD của repeated sweep.

## Kiểm thử và tích hợp

- `.\.venv\Scripts\python.exe -m pytest`: 50 passed, 2 skipped; 2 skip là test benchmark ML-KEM vì optional
  `pqcrypto` chưa cài. Có một `PytestCacheWarning` của cache trên Windows (`WinError 183`), không
  làm test thất bại.
- `.\.venv\Scripts\python.exe scripts\run_qkd_experiment.py`: tạo 140 run CSV trong cohort.
- `.\.venv\Scripts\python.exe scripts\run_analysis.py --qkd-run-prefix qkd_20261019T1509`: tạo 4 hình từ đúng cohort.
- `.\.venv\Scripts\python.exe scripts\run_all.py`: BB84 hoàn thành; ML-KEM được skip trung thực do thiếu `pqcrypto`;
  analysis của một run riêng chỉ tạo 2 hình khả dụng.
- Kiểm tra CSV: 140 run ID và seed duy nhất; mỗi row có `received + lost = n_signals`,
  `error_bits <= sifted_bits <= received_signals`, các fraction/QBER khớp công thức.

## Schema, provenance và lưu trữ

CSV giữ toàn bộ các cột BB84 cũ theo đúng thứ tự, sau đó nối thêm
`channel_loss_rate, received_signals, lost_signals, loss_fraction`. Các cột bổ sung không làm
consumer cũ thiếu cột bắt buộc bị lỗi. Metadata per-row ghi seed, run ID, UTC timestamp,
simulator/Python version và platform.

Raw CSV, PNG và CSV processed đang bị `.gitignore` bỏ qua theo quy ước chung (generated data
không commit mặc định). Chúng còn trong workspace local để kiểm tra/tái lập, nhưng chưa được
đưa lên GitHub. Báo cáo này chỉ ghi lại kết quả đã quan sát; không chứa khóa hoặc bí mật.
