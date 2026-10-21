# Tài liệu tham khảo

Các số tham chiếu trong tài liệu threat model và trade-off analysis trỏ tới nguồn dưới đây. Ưu tiên
đặc tả/nguồn sơ cấp; kiểm tra đúng phiên bản, phạm vi và errata hiện hành trước khi trích dẫn trong
báo cáo.

1. C. H. Bennett và G. Brassard, “Quantum cryptography: Public key distribution and coin
   tossing,” *Proceedings of IEEE International Conference on Computers, Systems and Signal
   Processing*, 1984, tr. 175–179. Công bố giao thức BB84.
   <https://research.ibm.com/publications/quantum-cryptography-public-key-distribution-and-coin-tossing>
2. P. W. Shor và J. Preskill, “Simple Proof of Security of the BB84 Quantum Key Distribution
   Protocol,” *Physical Review Letters*, 85, 441–444, 2000.
   DOI: <https://doi.org/10.1103/PhysRevLett.85.441>. Nguồn về chứng minh bảo mật BB84; không
   chứng nhận simulator hay thiết bị của repository.
3. National Institute of Standards and Technology (NIST), *Module-Lattice-Based Key-Encapsulation
   Mechanism Standard*, FIPS 203, August 2024.
   DOI: <https://doi.org/10.6028/NIST.FIPS.203>. Đặc tả ML-KEM; xem tài liệu và errata chính thức
   khi trích dẫn.
4. NIST, *Recommendation for Key Management: Part 1 – General*, SP 800-57 Part 1 Revision 5,
   May 2020. DOI: <https://doi.org/10.6028/NIST.SP.800-57pt1r5>. Bối cảnh key management; cần xác
   nhận hướng dẫn hiện hành áp dụng cho từng hệ thống.
5. European Telecommunications Standards Institute (ETSI), *Quantum Key Distribution (QKD);
   Use Cases*, ETSI GS QKD 002 V1.1.1, June 2010.
   <https://www.etsi.org/deliver/etsi_gs/QKD/001_099/002/01.01.01_60/gs_QKD002v010101p.pdf>.
6. ETSI, *Quantum Key Distribution (QKD); Protocol and data format of REST-based key delivery
   API*, ETSI GS QKD 014 V1.1.1, February 2019.
   <https://www.etsi.org/deliver/etsi_gs/QKD/001_099/014/01.01.01_60/gs_QKD014v010101p.pdf>.
7. P. W. Shor, “Algorithms for quantum computation: discrete logarithms and factoring,”
   *Proceedings of the 35th Annual Symposium on Foundations of Computer Science*, 1994,
   tr. 124–134. DOI: <https://doi.org/10.1109/SFCS.1994.365700>. Bối cảnh tác động của máy tính
   lượng tử đến một số giả định public-key cổ điển; không phải phân tích ML-KEM.

## Kỷ luật bằng chứng

- `qualitative_reference_based`: claim định tính cần chỉ rõ nguồn [n] hỗ trợ nội dung đó.
- `qualitative_assumption`: giả định triển khai cần được ghi là giả định, không trình bày như kết
  quả đo hoặc quy định chuẩn.
- `project_scope_limit`: giới hạn của simulator/benchmark hiện tại.
- `measured_project_data`: chỉ số được tính từ dữ liệu CSV thực tế của project; nêu run ID, seed
  (nếu có), môi trường, version và cấu hình liên quan.

Tiêu chuẩn quy định thuật toán/giao diện, không đo hiệu năng trên máy dự án. Bài BB84 gốc và chứng
minh giao thức không xác nhận simulator đơn giản là implementation QKD an toàn. Chuẩn ML-KEM
không chứng minh backend cụ thể đã được kiểm định hoặc tích hợp ứng dụng an toàn. Không dùng
reference để suy ra cost, distance, throughput hay ưu thế tổng quát nếu nguồn không đo trực tiếp
điều đó.
