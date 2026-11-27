# Bàn giao giữa các phiên Codex và ChatGPT

## Khi bắt đầu

Đọc [ngữ cảnh dự án](docs/PROJECT_CONTEXT.md) để biết câu hỏi nghiên cứu, người phụ trách và nguồn số liệu. Đọc mục mới nhất trong [nhật ký tiến độ](docs/PROGRESS_LOG.md) để tiếp tục đúng việc đang mở. Kiểm tra `git status --short --branch`, HEAD và trạng thái PR trước khi dùng lại một nhận định về nhánh. Giữ các chỉnh sửa sẵn có của người dùng. Phạm vi và quy trình review nằm trong [phân công](docs/TEAM_ASSIGNMENTS.md) và [hướng dẫn đóng góp](docs/CONTRIBUTING.md).

## Khi làm việc với dữ liệu

- Ghi rõ đâu là kết quả đã đối chiếu, đâu là kết quả nhóm từng báo cáo và đâu là việc còn mở. Gắn số đo với run ID, cấu hình, môi trường, đơn vị, cỡ mẫu và cách tổng hợp. Khi thiếu raw CSV, ghi nguồn lịch sử và phần chưa kiểm tra được.
- Với BB84, đối chiếu số bit lỗi, bit sifted, tín hiệu gửi/nhận và seed. Tách các setting, nhận diện CSV đời cũ thiếu trường và loại bản xuất trùng seed/cấu hình khi đếm trial. Giới hạn diễn giải QBER, ngưỡng minh họa và thời gian vòng lặp trong phạm vi mô hình cổ điển.
- Với ML-KEM-768, kiểm tra backend và shared-secret round trip trước khi công nhận một lần benchmark mới. Tính median và p95 nearest-rank từ mẫu latency theo từng thao tác, tách các môi trường khác nhau. Phân biệt thời gian primitive với handshake mạng. Ghi riêng test pass, skip và nguyên nhân.
- Các nhận định về xác thực, hạ tầng và triển khai phải ghi giả định, nguồn và giới hạn. Giữ nguyên dữ liệu gốc. Ưu tiên tính lại từ CSV bằng thao tác chỉ đọc khi mục tiêu là kiểm chứng. Các lệnh phân tích có thể ghi lại hình có tên cố định.
- Tài liệu chỉ chứa metadata cần thiết. Loại bỏ thông tin xác thực, đường dẫn cá nhân, mã sinh viên, bit khóa, khóa bí mật và nội dung shared secret.

## Khi kết thúc một đợt thay đổi quan trọng

Cập nhật **cả** [PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) và [PROGRESS_LOG.md](docs/PROGRESS_LOG.md) khi mã, schema, cấu hình, kết quả thực nghiệm, kết quả kiểm thử, trạng thái tích hợp hoặc kế hoạch khoa học thay đổi đáng kể. Ngữ cảnh phản ánh trạng thái hiện hành. Nhật ký giữ các mốc cũ và thêm ngày, thay đổi so với mốc trước, bằng chứng, giới hạn và việc tiếp theo. Nếu sửa một kết luận cũ, ghi căn cứ và ngày đính chính.

Kiểm tra diff, kể cả tài liệu mới chưa tracked. Đối với bàn giao tài liệu, giữ benchmark, dữ liệu và PR nguyên trạng. Chỉ commit hoặc push khi người dùng đồng ý.
