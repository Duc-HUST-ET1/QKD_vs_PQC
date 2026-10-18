# Tài liệu tham khảo

Các nguồn dưới đây dùng để định nghĩa phạm vi và thuật ngữ tiêu chuẩn. Trước khi trích dẫn kết
luận, cần kiểm tra phiên bản tài liệu và nội dung chính xác liên quan.

1. C. H. Bennett và G. Brassard, “Quantum cryptography: Public key distribution and coin
   tossing,” *Proceedings of IEEE International Conference on Computers, Systems and Signal
   Processing*, 1984, tr. 175–179. Nguồn nền tảng cho giao thức BB84.
2. National Institute of Standards and Technology (NIST), *Module-Lattice-Based Key-Encapsulation
   Mechanism Standard*, FIPS 203, August 2024. DOI:
   <https://doi.org/10.6028/NIST.FIPS.203>. Đặc tả chuẩn ML-KEM.
3. NIST, *Recommendation for Key Management: Part 1 – General*, SP 800-57 Part 1 Revision 5,
   May 2020. DOI: <https://doi.org/10.6028/NIST.SP.800-57pt1r5>. Bối cảnh quản lý khóa; tra cứu
   hướng dẫn hiện hành áp dụng cho nghiên cứu.
4. European Telecommunications Standards Institute (ETSI), *Quantum Key Distribution (QKD);
   Use Cases*, ETSI GS QKD 002 V1.1.1, June 2010. Tra cứu:
   <https://www.etsi.org/standards-search>.
5. ETSI, *Quantum Key Distribution (QKD); Protocol and data format of REST-based key delivery
   API*, ETSI GS QKD 014 V1.1.1, February 2019. Tra cứu:
   <https://www.etsi.org/standards-search>.
6. P. W. Shor, “Algorithms for quantum computation: discrete logarithms and factoring,”
   *Proceedings of the 35th Annual Symposium on Foundations of Computer Science*, 1994,
   tr. 124–134. DOI: <https://doi.org/10.1109/SFCS.1994.365700>. Bối cảnh mối đe dọa lượng tử đối
   với một số giả định public-key cổ điển.

## Kỷ luật bằng chứng

Tiêu chuẩn quy định thuật toán/interface, không đo hiệu năng trên máy của dự án. Bài BB84 gốc
không xác nhận simulator đơn giản là implementation an toàn. So sánh triển khai cần nguồn sơ cấp
hiện hành và nhãn loại bằng chứng. Thành viên phụ trách threat model cần kiểm tra mọi claim trước
khi đưa vào báo cáo cuối.
