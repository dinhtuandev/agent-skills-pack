# scripts/ — kiểm tra pack (offline)

Hai script chạy được **không cần mạng, không cần `claude` CLI** — bù cho phần
v3 vốn chỉ rà soát bằng tay (xem `../EVAL-REPORT.md`).

| Script | Trả lời câu hỏi | Exit code |
|---|---|---|
| `validate_skills.py` | "Cấu trúc skill còn đúng chuẩn không?" | 1 nếu có lỗi |
| `score_triggers.py` | "Sau khi sửa description, trigger có bị lệch không?" | luôn 0 |

## Chạy

Từ gốc pack:

```bash
python scripts/validate_skills.py            # cả 15 skill
python scripts/validate_skills.py write-prd  # 1 skill
python scripts/score_triggers.py             # điểm baseline + confusion
python scripts/score_triggers.py --verbose   # in từng ca dự đoán sai
```

Không cần cài thêm gì — thuần thư viện chuẩn Python 3.9+.

## validate_skills.py kiểm gì

Lỗi (làm fail):
- thiếu `SKILL.md`, hoặc không mở đầu bằng frontmatter `---`
- thiếu `name` / `description`
- `name` không phải kebab-case, hoặc khác tên thư mục
- `description` dài quá 1024 ký tự (giới hạn Claude Code)
- body trỏ tới `references/...`, `scripts/...`, `assets/...` không tồn tại
- thiếu `evals/trigger-eval.json`, sai schema, hoặc thiếu hẳn nhánh
  `should_trigger` true / false

Cảnh báo (không fail): description ngắn dưới 120 ký tự, không có cụm trigger
("use when / wants / asks / says..."), body mỏng, thư mục rỗng, và **skill có
`references/*-template.md` nhưng thiếu `evals/output-eval.md`** (tức chưa có
tiêu chí chấm chất lượng output).

Kiểm ngược để tin script: tạo tạm một thư mục skill trỏ tới file không tồn tại
rồi chạy — phải exit 1:

```bash
mkdir -p _tmp/references
printf '%s\n' \
  '---' \
  'name: tmp' \
  'description: A deliberately long enough description for the validator to accept this as a real skill description string here.' \
  '---' '' \
  'See `references/khong-ton-tai.md` for the missing thing.' > _tmp/SKILL.md
python scripts/validate_skills.py _tmp; echo "exit=$?"   # kỳ vọng exit=1
rm -rf _tmp
```

## score_triggers.py đo gì

Với **mỗi query trong mọi file eval**, nó chấm điểm query đó với **cả 15
description cùng lúc** bằng BM25, lấy description điểm cao nhất, rồi so với
skill được kỳ vọng. Kết quả: độ chính xác tổng, recall theo từng skill, và
bảng "confusion" (skill nào cướp query của skill nào).

Đây là **baseline từ vựng**, không phải model thật. Giá trị của nó là tính
**lặp lại được**: sửa một description, chạy lại, nếu điểm tụt hoặc xuất hiện
confusion mới → hai description vừa đụng nhau. Đó chính là loại lỗi v3 phải
phát hiện bằng mắt.

## Giới hạn (đọc trước khi tin số)

- Cả hai script chỉ đọc file trên đĩa — không chứng minh Claude Code sẽ load
  đúng, chỉ chứng minh file đúng chuẩn và description không đụng nhau về mặt
  từ vựng.
- Vòng benchmark thật (đo variance, train/test split, model khác chấm) vẫn cần
  `claude -p` trong Claude Code — lệnh có trong `../EVAL-REPORT.md`.
- Các script này chưa được chạy trong phiên tạo ra chúng (sandbox shell của môi
  trường soạn thảo không khởi động được). Lần đầu bạn chạy, hãy đọc kỹ output
  thay vì coi là đã xanh.
