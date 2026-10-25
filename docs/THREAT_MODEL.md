# Mô hình đe dọa và giả định bảo mật

Tài liệu này xác định ranh giới so sánh của repository; không phải chứng nhận bảo mật, đánh giá
implementation mật mã, hay khuyến nghị triển khai. Các nhận định về giao thức được gắn nguồn trong
[REFERENCES.md](REFERENCES.md); các kết quả đo của repository phải được ghi riêng là
`measured_project_data`.

## Ranh giới hệ thống và giả định tin cậy

Repository chỉ bao gồm simulator BB84 dạng cổ điển, adapter gọi implementation ML-KEM-768 tùy chọn,
và phân tích CSV/biểu đồ. Thiết bị QKD, protocol truyền thông hoàn chỉnh, xác thực danh tính,
phân phối/quản lý khóa trong ứng dụng, môi trường build và vận hành nằm ngoài ranh giới. Vì vậy,
thành công của simulator, capability check hay benchmark không phải bằng chứng rằng hệ thống đầu
cuối được bảo vệ.

Một triển khai thực tế phải tin cậy endpoint, nguồn ngẫu nhiên, implementation và cấu hình, quy
trình xác thực, cũng như bảo vệ và vòng đời khóa. Với QKD, giả định có quantum channel không thay
thế authenticated classical channel. Với ML-KEM, việc hai phía thu được cùng shared secret không
xác minh danh tính peer hoặc toàn vẹn transcript.

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

Attacker có thể quan sát hoặc sửa thông điệp công khai, giả danh peer khi protocol không xác thực,
hoặc khai thác endpoint/backend yếu nếu có quyền truy cập hay điều kiện tấn công phù hợp. Không
giả định attacker phá được các giả định mật mã của ML-KEM; rủi ro lượng tử ở đây là bối cảnh đe
dọa cho các thuật toán public-key cổ điển, không phải bằng chứng về an toàn của một implementation
cụ thể.

## BB84/QKD: giả định và ranh giới

Trực giác BB84 dựa trên các quy tắc đo trạng thái lượng tử; các tuyên bố bảo mật thực tế phụ thuộc
protocol, chứng minh, thiết bị và giả định triển khai [1, 2]. QKD thực tế cần một quantum channel
và một classical channel được xác thực. Nếu thiếu xác thực, active attacker có thể giả mạo hai
đầu và thực hiện tấn công trung gian; do đó xác thực phải được thiết lập bằng credential/secret
đáng tin cậy có trước hoặc cơ chế xác thực phù hợp [2, 5]. QKD không tự bootstrap trust cho kênh
cổ điển, bảo vệ endpoint hay quản lý khóa sau khi tạo [4, 5].

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
transcript, đồng thời chống MITM [3, 8]. Benchmark của repository chỉ đo các operation của
primitive ML-KEM-768 (khi backend tương thích đã qua capability/correctness check); không đo
handshake, mạng, xác thực, key management hay độ an toàn của ứng dụng.

## Tóm tắt threat/controls

| Tình huống / attacker | Điều kiện và tác động tiềm tàng | Control cần có ngoài đời | Coverage và bằng chứng trong repository |
|---|---|---|---|
| Nghe lén thụ động; attacker có năng lực lượng tử | Có quyền quan sát kênh; có thể làm lộ thông tin nếu giả định/protocol/implementation không phù hợp | Chọn protocol và primitive theo mô hình attacker, proof và implementation đã thẩm định [1–3] | BB84 chỉ mô phỏng bit/basis cổ điển; ML-KEM chỉ benchmark primitive, không chứng minh bảo mật triển khai |
| MITM, giả danh hoặc sửa transcript | Có thể can thiệp trao đổi công khai; kênh cổ điển QKD không xác thực hoặc protocol dùng KEM thiếu authentication | QKD cần authenticated classical channel và trust bootstrap; ML-KEM cần protocol xác thực/ràng buộc peer, khóa và transcript [2, 5, 8] | Không triển khai authentication hay protocol handshake |
| Endpoint compromise, RNG yếu, mất cắp khóa | Cần chiếm endpoint, nguồn entropy hoặc đường lưu trữ/xử lý khóa; có thể lộ khóa và phá confidentiality/integrity | Bảo vệ endpoint/entropy, phân quyền, lưu trữ, rotation, revocation và xử lý vòng đời khóa [4, 8] | Không mô phỏng hoặc kiểm tra các kiểm soát này; CSV không được chứa nội dung bí mật |
| Lỗi implementation, side-channel, cấu hình hoặc supply chain | Backend/thư viện/build bị lỗi hoặc bị thay thế; có thể làm sai primitive hay rò rỉ bí mật | Thẩm định implementation, dependency, build, cấu hình và môi trường vận hành [3, 8] | ML-KEM capability check chỉ kiểm tra API, version và round-trip secret; không phải security audit |
| Từ chối dịch vụ hoặc hỏng kênh | Attacker làm gián đoạn kênh, thiết bị hoặc endpoint; trao đổi khóa có thể không khả dụng | Thiết kế resilience, giám sát và xử lý lỗi ở tầng hệ thống [5, 6] | Không đo/đánh giá availability hoặc khả năng phục hồi |
| Diễn giải sai hoặc giả mạo bằng chứng | Người phân tích trộn điều kiện, dùng dữ liệu không có provenance hoặc coi metric khác loại là tương đương | Giữ nguồn CSV/run/config/runtime, nhãn evidence và giới hạn; reviewer độc lập kiểm tra | Analysis đọc CSV và gắn nhãn; hàm trade-off không tự xác minh provenance do caller cung cấp |

## Quy tắc diễn giải và evidence

- `qualitative_reference_based`: nhận định định tính gắn nguồn cụ thể trong
  [REFERENCES.md](REFERENCES.md); phạm vi nguồn phải phù hợp với claim.
- `qualitative_assumption`: giả định vận hành/triển khai chưa được đo trong repository.
- `project_scope_limit`: điều repository hiện không mô phỏng hoặc không chứng minh.
- `measured_project_data`: chỉ metric được tính từ CSV đầu vào thật; caller chịu trách nhiệm chỉ
  truyền số liệu đã validate và giữ run/provenance, đơn vị, cấu hình cùng điều kiện đo. Hàm
  `analyze_tradeoffs()` không thể xác minh nguồn gốc mapping metric.

QBER là tỷ lệ lỗi trong mô hình BB84, không phải latency. Latency ML-KEM là thời gian operation
phần mềm, không đại diện throughput hay hiệu năng mạng. Không so sánh trực tiếp hai đại lượng,
không suy ra bên nào luôn an toàn/nhanh/rẻ hơn, và không công bố cost, range, throughput thực địa
khi chưa có nguồn hoặc phép đo phù hợp. Xem [PROJECT_SCOPE.md](PROJECT_SCOPE.md) và
[EXPERIMENT_PROTOCOL.md](EXPERIMENT_PROTOCOL.md) để biết thêm phạm vi.
