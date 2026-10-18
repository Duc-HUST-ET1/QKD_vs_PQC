# Hướng dẫn đóng góp

## Branch và commit

Tạo branch ngắn, gắn với một deliverable:

- `feature/bb84-simulation`
- `feature/mlkem-benchmark`
- `feature/analysis-plots`
- `docs/threat-model`
- `integration/pipeline`

Commit message nên ngắn, nêu hành động; ví dụ `feat: add BB84 CSV export`,
`test: cover zero sifted bits`, `docs: clarify ML-KEM setup`. Không viết như thể benchmark đã
chạy nếu chỉ mới thêm adapter.

Trước commit:

```sh
git status --short --branch
git diff --check
git diff --stat
```

Stage từng file đã xem lại bằng `git add path/to/file`; không mặc định `git add .`. Chỉ push lên
remote đã được xác nhận bằng `git remote -v`.

## Kiểm tra

- Thay đổi Python: chạy `python -m pytest` hoặc test file liên quan, ghi đúng số pass/skip/fail.
- Thay đổi interface/schema: chạy test consumer và cập nhật docs.
- Thay đổi tài liệu thuần túy: kiểm tra liên kết, file path và lệnh; không cần benchmark.
- Không coi optional ML-KEM test bị skip là pass. Đọc lý do skip trong pytest summary.

## Pull request và review

Mỗi PR nêu:

1. Vấn đề và phạm vi thay đổi.
2. File/module/interface hoặc header CSV bị ảnh hưởng.
3. Giả định, nguồn và giới hạn khoa học.
4. Lệnh đã chạy cùng kết quả thực tế (kể cả skip).
5. Hướng dẫn tái hiện hoặc lý do không cần chạy test.

Owner của module review thay đổi trong workstream đó. Thành viên 5 xem tính tương thích pipeline,
config, paths, CSV và tests. Thành viên 4 xem nhận định hệ thống; thành viên 4 phối hợp với các
owner khi sửa threat-model chung. Nội dung QKD/PQC không được kết luận chính xác chỉ bằng review
của người viết; cần nguồn và người review khác.

## Thay đổi API

Trước khi sửa signature, config keys, CSV headers hoặc output naming:

1. Mô tả lý do, consumer hiện tại và hướng di trú trong Issue/PR.
2. Thông báo owner các module gọi interface.
3. Đề xuất cập nhật code, tests và `DEVELOPMENT_GUIDE.md`/`DATA_DICTIONARY.md` trong cùng PR.
4. Không xóa trường/đổi ý nghĩa âm thầm; không dùng giá trị mặc định giả để che lỗi.

## Báo bug và blocker

Tạo GitHub Issue dùng template trong `.github/ISSUE_TEMPLATE/bug_report.md` hoặc
`task.md`. Đưa steps tái hiện, OS/Python/package versions và traceback cần thiết; xóa credentials,
private keys, shared secrets và dữ liệu nhạy cảm trước khi gửi. Ghi blocker sớm để các workstream
khác có thể tiếp tục phần độc lập.

## Dữ liệu và thông tin nhạy cảm

Không commit `.venv/`, cache, `.env`, credentials, private keys, shared-secret bytes, CSV raw, ảnh
được sinh tự động hoặc file lớn. Git hiện ignore raw CSV, processed outputs, PNG; vẫn cần kiểm tra
`git status` vì ignore không thay thế review. Actual run lưu ở `data/raw/`, ví dụ có nhãn ở
`data/example/`. Không chỉnh tay số đo trong CSV.

Hướng dẫn tổng quát tại [WORKFLOW.md](WORKFLOW.md); cấu trúc và ownership ở
[TEAM_ASSIGNMENTS.md](TEAM_ASSIGNMENTS.md).
