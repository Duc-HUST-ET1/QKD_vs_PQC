# Quy trình làm việc song song, không phụ thuộc họp trực tiếp

## Vòng đời công việc

`Planned → In Progress → Ready for Review → Tested → Integrated → Done`

| Trạng thái | Ý nghĩa | Bằng chứng để chuyển bước |
|---|---|---|
| **Planned** | Đã mô tả việc cần làm, phạm vi và tiêu chí hoàn tất | Issue/task có owner, files dự kiến, interface/dependency |
| **In Progress** | Owner đang thực hiện trên nhánh riêng | Có cập nhật tiến độ và blocker; chưa yêu cầu người khác dùng output |
| **Ready for Review** | Thay đổi đã commit/push, cần review | PR có mục tiêu, files, ảnh hưởng interface, assumptions và lệnh kiểm tra |
| **Tested** | Reviewer/owner xác nhận các kiểm tra cần thiết đã chạy | Kết quả test thực, bao gồm skip; docs có thể ghi “docs-only, không chạy test” |
| **Integrated** | PR được merge vào nhánh tích hợp mặc định của nhóm | Merge commit/PR hợp lệ, các consumer đã được kiểm tra |
| **Done** | Deliverable đạt acceptance criteria và tài liệu cập nhật | Checklist hoàn tất, không còn blocker hoặc câu hỏi chưa ghi nhận |

Không đánh dấu Tested chỉ vì lệnh “có vẻ đúng”; ghi đầu ra đã quan sát. Với tính năng phụ thuộc
ML-KEM vắng mặt, ghi test nào skip và lý do thay vì tính skip là pass.

## Branch và PR

Mỗi thành viên làm trên một branch ngắn hạn, ví dụ:

- `feature/bb84-simulation`
- `feature/mlkem-benchmark`
- `feature/analysis-plots`
- `docs/threat-model`
- `integration/pipeline`

Quy trình an toàn từ repository đã được clone:

```sh
git status --short --branch
git switch -c feature/ten-cong-viec
# sửa file, chạy kiểm tra
git diff --check
git status --short
git add path/to/file-you-reviewed
git commit -m "feat: describe focused change"
git push -u origin feature/ten-cong-viec
```

Thay placeholder branch và đường dẫn trước khi chạy. Kiểm tra `git remote -v` trước khi push.
Mở PR vào nhánh mặc định thực tế của nhóm, không đoán tên nhánh. Không dùng `git add .` khi chưa
review `git status`; dữ liệu raw thường bị ignore nhưng vẫn phải kiểm tra.

## Phối hợp không họp

- Mỗi task/PR ghi ngắn gọn mục tiêu, trạng thái lifecycle, owner, files, interface, lệnh test,
  kết quả, assumptions và blocker.
- Thảo luận câu hỏi mở trong Issue/PR; nêu lựa chọn cần quyết định thay vì chờ buổi họp.
- Chốt giao diện trong tài liệu/API trước khi mỗi workstream phụ thuộc vào nó.
- Nếu file dùng chung cần thay đổi, tạo PR riêng hoặc yêu cầu owner cùng review; không force-push
  thay đổi của người khác.
- Nếu phụ thuộc bị chặn, tiếp tục phần độc lập, ghi rõ dữ liệu/interface tạm dùng và không tạo số
  đo giả.

## Ranh giới quyền sở hữu

Xem [TEAM_ASSIGNMENTS.md](TEAM_ASSIGNMENTS.md) và [CODE_MAP.md](CODE_MAP.md). Năm workstream có
thể khởi đầu song song:

1. BB84 / QKD — `src/qkd_pqc/qkd/`, `scripts/run_qkd.py`, tests BB84.
2. ML-KEM — `src/qkd_pqc/pqc/`, `scripts/run_pqc_benchmark.py`, tests optional.
3. Phân tích — `src/qkd_pqc/analysis/`, `scripts/run_analysis.py`, tests plotting.
4. Security/threat model — `docs/THREAT_MODEL.md`, `docs/REFERENCES.md`,
   `src/qkd_pqc/system/`.
5. Integration — config, common, paths, pipeline, tests tích hợp và README.

Đây là quyền sở hữu ban đầu. Không thành viên nào được đơn phương thay đổi API, schema CSV,
config dùng chung hoặc hướng dẫn chung mà không thông báo các consumer.

## Điểm kiểm tra trước khi tích hợp (Thành viên 5 điều phối)

- [ ] Package/module import được trong virtual environment đã cài project.
- [ ] Public function/class signature, config và exception được ghi trong DEVELOPMENT_GUIDE.
- [ ] Test liên quan chạy; output và skip/failure được ghi trung thực.
- [ ] CSV header, đơn vị, trường rỗng và version metadata nhất quán.
- [ ] Có thể chạy một thí nghiệm nhỏ nếu thay đổi đường đi runtime.
- [ ] Seed/input/runtime metadata đủ để tái lập khi liên quan.
- [ ] Biểu đồ và bảng chỉ được tạo từ input CSV thật.
- [ ] Không có benchmark giả, secret, cache, file `.venv`, hoặc dữ liệu lớn ngoài ý muốn.
- [ ] Docs nội bộ và commands phản ánh mã vừa merge.

## Safe Git commands

Các lệnh đọc trạng thái trước khi thay đổi:

```sh
git status --short --branch
git diff --check
git diff --stat
git remote -v
```

Không chạy lệnh xóa history, force push hoặc xóa nhánh có người dùng nếu chưa có xác nhận và chưa
hiểu tác động. Repository workspace đã kiểm tra trước đây chưa có `.git`; hãy dùng quy trình clone
của nhóm hoặc hỏi người quản lý Git, không tự `git init` khi chưa quyết định nơi lưu lịch sử.
