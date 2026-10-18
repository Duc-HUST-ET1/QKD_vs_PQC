# Phạm vi dự án

## Câu hỏi nghiên cứu

QKD và PQC khác nhau như thế nào về giả định bảo mật và hiệu năng thiết lập khóa, và yêu cầu hạ
tầng ảnh hưởng ra sao đến tính phù hợp khi triển khai?

## Nội dung bao gồm

1. Mô phỏng cổ điển mang tính giáo dục về BB84 bits/bases, channel bit flips, intercept-resend Eve.
2. Adapter benchmark ML-KEM-768 chuẩn hóa theo NIST FIPS 203, chỉ chạy khi implementation thật
   tương thích và được kiểm tra.
3. So sánh định tính, có nguồn, về mô hình bảo mật và ràng buộc triển khai.
4. CSV có provenance, tái lập, tests và biểu đồ được tạo từ CSV thực tế.

## Ngoài phạm vi và giới hạn diễn giải

BB84 ở đây không phải mô phỏng lượng tử hoặc stack QKD an toàn. Không mô hình hóa phần cứng,
optical effects/losses, side channel, error correction, privacy amplification, finite-key proof
hay quy trình xác thực. Ngưỡng QBER 0.11 là tham số dạy học; vượt qua ngưỡng không chứng minh khóa
an toàn.

ML-KEM-768 là thuật toán NIST FIPS 203. Benchmark phụ thuộc implementation tương thích; không đo
network, cài đặt, integration protocol hay key management. Không chứng minh PQC luôn nhanh hơn hay
phù hợp hơn QKD.

Không tạo số liệu cost, distance, throughput hoặc deployment chưa đo. Phân biệt kết quả đo với
nhận định định tính và assumption.

## Workstream độc lập

Cả năm thành viên có thể bắt đầu song song trên API và CSV contract đã ghi. Thay đổi giao diện
chung cần phối hợp qua PR; xem [TEAM_ASSIGNMENTS.md](TEAM_ASSIGNMENTS.md) và
[WORKFLOW.md](WORKFLOW.md).
