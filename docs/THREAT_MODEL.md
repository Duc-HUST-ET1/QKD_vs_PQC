# Mô hình đe dọa và giả định bảo mật

Tài liệu này xác định ranh giới so sánh của repository; không phải chứng nhận bảo mật, đánh giá
implementation mật mã, hay khuyến nghị triển khai. Các nhận định về giao thức được gắn nguồn trong
[REFERENCES.md](REFERENCES.md); các kết quả đo của repository phải được ghi riêng là
`measured_project_data`.

## Mục tiêu và tài sản

BB84/QKD và ML-KEM là hai cách tạo hoặc thiết lập vật liệu khóa để một protocol/application khác
sử dụng. Chúng không tự mã hóa dữ liệu ứng dụng hay tự xác minh danh tính peer. Tài sản cần bảo vệ
trong một hệ thống thực tế gồm:

- bí mật và tính toàn vẹn của shared key sau khi thiết lập;
- danh tính endpoint, thông điệp điều khiển và tính toàn vẹn của transcript giao thức;
- private/authentication keys, entropy và trạng thái nội bộ của endpoint;
- tính đúng đắn của implementation, cấu hình, thư viện và quá trình build/phân phối;
- độ sẵn sàng của dịch vụ, kênh truyền và cơ chế cấp phát khóa.

CSV của dự án chỉ được giữ số đo/provenance; không được ghi bit khóa, private key, ciphertext
payload nhạy cảm hoặc shared-secret bytes.

## Tác nhân và năng lực

Mô hình xem xét endpoint hợp lệ, người nghe lén thụ động, attacker chủ động trên mạng (bao gồm
man-in-the-middle), attacker có máy tính lượng tử liên quan tới các giả định khóa công khai cổ
điển, và Eve intercept-resend trong mô hình BB84 dạy học. Rủi ro endpoint bị chiếm quyền, lỗi
implementation, lỗi/suy giảm random generation, supply-chain compromise, rò rỉ side-channel và
denial of service cần được xem xét riêng; simulator/benchmark này không xác minh hoặc loại trừ
chúng.

## BB84/QKD: giả định và ranh giới

Trực giác BB84 dựa trên các quy tắc đo trạng thái lượng tử; các tuyên bố bảo mật thực tế phụ thuộc
protocol, chứng minh, thiết bị và giả định triển khai [1, 2]. QKD thực tế cần một quantum channel
và một classical channel được xác thực. Nếu thiếu xác thực, active attacker có thể giả mạo hai
đầu và thực hiện tấn công trung gian; do đó xác thực phải được thiết lập bằng credential/secret
đáng tin cậy có trước hoặc cơ chế xác thực phù hợp [2, 5]. QKD không giải quyết tự thân việc
bootstrap xác thực, bảo vệ endpoint hay quản lý khóa sau khi tạo [4, 5].

Mô hình trong repository chỉ sinh bit/basis cổ điển có seed, rồi mô phỏng Eve intercept-resend,
bit flip độc lập và loss Bernoulli. Nó **không** mô phỏng trạng thái lượng tử, optical channel hay
detector; cũng không triển khai authentication, error correction/reconciliation, privacy
amplification, finite-key analysis, composable security proof, thiết bị chống side-channel hoặc
quản lý khóa. `qber_threshold` mặc định 0.11 và `illustrative_accept`/`illustrative_reject` là
nhãn mô phỏng, tuyệt đối không phải ngưỡng chứng minh an toàn hoặc kết luận khóa có thể dùng.

## ML-KEM-768/PQC: giả định và ranh giới

ML-KEM-768 là KEM cổ điển được định nghĩa trong NIST FIPS 203; cơ sở an toàn là tính toán trên
cấu trúc module-lattice, với phân tích liên quan đến Module Learning With Errors theo tiêu chuẩn
[3]. Đây là bảo mật tính toán dưới giả định và phạm vi của tiêu chuẩn, không phải bảo đảm vô điều
kiện. Cần đúng thuật toán, implementation, random generation, xử lý khóa và tích hợp protocol.

KEM encapsulation/decapsulation thiết lập shared secret; bản thân primitive không xác thực danh
tính peer. Ứng dụng phải dùng protocol có xác thực thích hợp để ràng buộc danh tính, khóa và
transcript, đồng thời chống MITM [3, 4]. Benchmark của repository chỉ đo các operation của
primitive ML-KEM-768 (khi backend tương thích đã qua capability/correctness check); không đo
handshake, mạng, xác thực, key management hay độ an toàn của ứng dụng.

## Tóm tắt threat/controls

| Mối đe dọa | Yêu cầu/biện pháp trong hệ thống thực | Trạng thái trong repository |
|---|---|---|
| MITM hoặc giả danh endpoint | QKD cần authenticated classical channel; ML-KEM cần protocol authentication | Không triển khai; nêu như giới hạn |
| Nghe lén, kể cả attacker có năng lực lượng tử | Chọn protocol/primitive theo giả định, proof và triển khai phù hợp | BB84 chỉ là mô phỏng cổ điển; ML-KEM chỉ benchmark primitive |
| Endpoint compromise, key theft, RNG lỗi | Bảo vệ endpoint, entropy, key lifecycle và secret storage | Không mô phỏng/kiểm tra |
| Sai implementation, side-channel hoặc supply-chain | Thẩm định implementation, cấu hình, build và vận hành | Capability check ML-KEM chỉ xác minh API/round-trip cơ bản, không phải security audit |
| Từ chối dịch vụ hoặc hỏng kênh | Resilience, monitoring và xử lý lỗi ở tầng hệ thống | Không đo/đánh giá |
| Diễn giải sai kết quả | Gắn evidence label, provenance và giới hạn; không gộp khác loại metric | Có CSV/analysis; reviewer vẫn phải xác minh dữ liệu và diễn giải |

## Quy tắc diễn giải và evidence

- `qualitative_reference_based`: nhận định định tính gắn nguồn cụ thể trong
  [REFERENCES.md](REFERENCES.md).
- `qualitative_assumption`: giả định vận hành/triển khai chưa được đo trong repository.
- `project_scope_limit`: điều repository hiện không mô phỏng hoặc không chứng minh.
- `measured_project_data`: chỉ metric được tính từ CSV đầu vào thật; phải giữ run/provenance và
  điều kiện đo.

QBER là tỷ lệ lỗi trong mô hình BB84, không phải latency. Latency ML-KEM là thời gian operation
phần mềm, không đại diện throughput hay hiệu năng mạng. Không so sánh trực tiếp hai đại lượng,
không suy ra bên nào luôn an toàn/nhanh/rẻ hơn, và không công bố cost, range, throughput thực địa
khi chưa có nguồn hoặc phép đo phù hợp. Xem [PROJECT_SCOPE.md](PROJECT_SCOPE.md) và
[EXPERIMENT_PROTOCOL.md](EXPERIMENT_PROTOCOL.md) để biết thêm phạm vi.
