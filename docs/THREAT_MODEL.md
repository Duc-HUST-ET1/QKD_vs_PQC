# Mô hình đe dọa và giả định bảo mật

Tài liệu này xác định ranh giới so sánh, không phải chứng nhận bảo mật.

## Tài sản và tác nhân

Hai cách tiếp cận hướng tới thiết lập vật liệu khóa dùng tiếp trong ứng dụng. Các tác nhân liên
quan: hai endpoint hợp lệ, người nghe lén thụ động, attacker chủ động trên mạng, attacker có năng
lực lượng tử trong tương lai, và Eve intercept-resend trong mô hình BB84 dạy học. Compromise
endpoint, lỗi implementation, supply-chain compromise và denial of service không được chứng minh
hay bao phủ bởi simulator này.

## BB84/QKD

Trực giác bảo mật BB84 dựa vào ảnh hưởng của phép đo trạng thái lượng tử và no-cloning principle,
trong phạm vi giả định của giao thức. Hệ QKD thực tế còn phải bảo đảm thiết bị/implementation,
quản lý khóa, xử lý hậu kỳ và trao đổi cổ điển được xác thực. Xác thực ngăn active attacker giả
danh khi hai bên trao đổi reconciliation data; bản thân xác thực phải được bootstrapped bằng
credential đáng tin cậy hoặc secret có trước.

Code dự án dùng mô hình bit/basis cổ điển có seed, mô phỏng Eve và lỗi lật bit độc lập. Code không
mô phỏng trạng thái lượng tử, detector, optical loss, side channel, finite-key proof, error
correction hoặc privacy amplification. QBER <= 0.11 **không** chứng minh khóa an toàn; accept/reject
chỉ là nhãn minh họa.

## ML-KEM-768/PQC

ML-KEM-768 là key-encapsulation mechanism cổ điển được chuẩn hóa ở NIST FIPS 203. Cơ sở an toàn
tính toán dựa trên cấu trúc Module Learning With Errors theo tiêu chuẩn. Thuật toán hướng tới
kháng tấn công cổ điển/lượng tử đã biết dưới giả định đó, không phải bảo đảm vô điều kiện. Cần
implementation đúng, random generation phù hợp, protocol composition, authentication và key
handling.

ML-KEM tự nó không xác thực danh tính endpoint. Ứng dụng vẫn cần identity authentication và
protocol có xác thực để chống man-in-the-middle. Benchmark dự án đo primitive, không phải handshake
hoàn chỉnh hoặc application.

## So sánh và giới hạn

QKD cần quantum channel cùng classical channel được xác thực và hạ tầng phù hợp tại hai đầu.
ML-KEM chạy trên tính toán/giao tiếp cổ điển; vẫn phải tích hợp vào protocol đã xác thực. Chi phí,
khoảng cách, throughput và vận hành cần evidence triển khai cụ thể; repository chưa đo các giá
trị này.

Không khẳng định phương án nào luôn nhanh, rẻ hay an toàn hơn. Giữ QBER tách biệt khỏi software
operation latency. Gắn nguồn/nhãn cho nhận định trong [REFERENCES.md](REFERENCES.md).
