# agent-skills-pack — Agent Skills pack (15 skill)

> Đây là bản tiếng Việt, giữ đầy đủ lịch sử thay đổi. Bản chính (tiếng Anh): [README.md](README.md).

Bộ 15 skill chuyển thể từ 15 prompt card gốc (write PRD → turn task into skill),
đóng gói theo chuẩn mở **Agent Skills**: mỗi skill là một thư mục có `SKILL.md`
(frontmatter `name` + `description`, rồi tới nội dung hướng dẫn), kèm `references/`
và `evals/` tuỳ skill.

Vì bám chuẩn mở, pack dùng được cho nhiều coding agent, không riêng Claude Code.
Khác với prompt gốc (điền chỗ trống rồi copy-paste mỗi lần), agent tự đọc
`description` để biết khi nào nên dùng, và tự áp dụng luôn — không cần gõ lại prompt.

## Cài đặt

Mọi client hỗ trợ Agent Skills đều nạp skill cùng một cách: đặt thư mục skill
(chứa `SKILL.md`) vào thư mục skills mà client đó quét.

1. Tải repo về.
2. Copy các thư mục skill vào thư mục skills của client.
3. Mở lại session — client tự load, không cần config thêm.

Đường dẫn cụ thể khác nhau theo từng client; xem danh sách client và hướng dẫn tại
<https://agentskills.io/clients> thay vì đoán.

### Claude Code

- Copy các thư mục skill vào `.claude/skills/` ở gốc project
  (hoặc `~/.claude/skills/` nếu muốn dùng chung cho mọi project).
- Claude Code theo chuẩn Agent Skills và bổ sung frontmatter mở rộng; pack này chỉ
  dùng `name` + `description` nên tương thích với mọi client.

## Danh sách 15 skill

| # | Thư mục | Dùng khi nào |
|---|---------|--------------|
| 1 | `write-prd` | Viết PRD đầy đủ cho 1 feature trước khi làm |
| 2 | `create-claude-md` | Scan repo, generate/refresh CLAUDE.md (chỉ Claude Code) |
| 3 | `plan-mode` | Bắt Claude lên plan trước, không đụng code |
| 4 | `spec-driven-dev` | Viết spec given/when/then trước khi code |
| 5 | `ui-ux-brief` | Viết brief UI/UX đầy đủ cho 1 screen/flow |
| 6 | `implementation-plan` | Từ spec/PRD đã duyệt ra build sequence từng bước |
| 7 | `wire-mcp-server` | Setup MCP server cho 1 service/API |
| 8 | `connect-database` | Kết nối DB, schema, migration, query helper |
| 9 | `security-audit` | Audit bảo mật kiểu tấn công thật, xếp theo severity |
| 10 | `debug-fast` | Debug theo bằng chứng, không đoán mò |
| 11 | `e2e-test` | Viết Playwright E2E test cho 1 flow |
| 12 | `cleanup-dead-code` | Tìm & xoá dead code an toàn |
| 13 | `git-commit` | Chia commit sạch theo conventional commits |
| 14 | `hooks-guardrails` | Setup Claude Code hooks làm guardrail (chỉ Claude Code) |
| 15 | `task-to-skill` | Biến 1 task lặp lại thành skill mới (meta) |

## Thay đổi ở bản v5 (output eval + template báo cáo)

**Thêm eval chất lượng output.** v4 mới kiểm *có trigger hay không*; nó chưa kiểm *skill tạo ra cái gì*. v5 thêm `evals/output-eval.md` — rubric từng mục kèm ví dụ input, để phần "body" của skill cũng có tiêu chí chấm:

- `write-prd/evals/output-eval.md` — PRD phải đủ mọi mục của template, metric đo được, acceptance criteria tick được, có non-goals và failure states.
- `spec-driven-dev/evals/output-eval.md` — given/when/then cho từng case, API contract có status code cụ thể, UI states đủ 4 trạng thái.
- `ui-ux-brief/evals/output-eval.md` — component inventory đủ mọi state, token là giá trị cụ thể, motion có duration/easing.
- `implementation-plan/evals/output-eval.md` — mỗi bước đủ 5 field, verify là lệnh thật, rollback cụ thể.

`validate_skills.py` nay cảnh báo khi một skill có `references/*-template.md` nhưng thiếu rubric output.

**Thêm 2 template báo cáo:** `cleanup-dead-code/references/cleanup-report.md` và `connect-database/references/migration-checklist.md`; đã nối vào SKILL.md tương ứng.

**Khả chuyển hook:** `hooks-guardrails/references/portability.md` — hook `.sh` cần Git Bash/WSL trên Windows, `jq` bắt buộc, kèm biến thể kiểm path không cần `jq` (nhắc lại: chỉ exit code 2 mới chặn PreToolUse).

**Kiểm chứng đã chạy (2026-10-02):**

- `python scripts/validate_skills.py` → `15 skill(s): 0 error(s), 0 warning(s)`, exit 0.
- `python scripts/score_triggers.py` → baseline 83.3% (155/186), exit 0.

## Thay đổi ở bản v4 (kiểm chứng lặp lại + template)

**Thêm bộ kiểm tra offline chạy được (`scripts/`).** v3 tự nhận là "lint thủ công", không lặp lại được. Giờ có 2 script thuần thư viện chuẩn Python, không cần mạng hay `claude` CLI:

- `scripts/validate_skills.py` — kiểm cấu trúc từng skill: frontmatter hợp lệ, `name` kebab-case khớp tên thư mục, `description` dưới 1024 ký tự, mọi đường dẫn `references/…` được nhắc trong body phải tồn tại thật, và `evals/trigger-eval.json` đúng schema. Exit code 1 khi có lỗi.
- `scripts/score_triggers.py` — chấm **mọi query trong mọi file eval với cả 15 description cùng lúc** bằng BM25, in ra độ chính xác, recall từng skill, và bảng confusion (skill nào cướp query của skill nào). Đây là con số lặp lại được để phát hiện hai description vừa đụng nhau sau một lần sửa — đúng loại lỗi mà v3 phải tìm bằng mắt.

Chi tiết cách chạy và giới hạn: `scripts/README.md`.

**Bổ sung 4 template còn thiếu.** v2 đã thêm template cho `write-prd`, `spec-driven-dev`, `ui-ux-brief` với lý do "mỗi lần chạy Claude tự bịa lại cấu trúc Markdown". Lý do đó áp dụng y hệt cho 4 skill còn lại, nay đã có và đã được nối vào SKILL.md:

- `implementation-plan/references/plan-template.md`
- `debug-fast/references/hypothesis-ledger.md`
- `security-audit/references/findings-report.md`
- `e2e-test/references/test-skeleton.md`

**Sửa lỗi nhỏ:** comment đầu `hooks-guardrails/scripts/protect-paths.sh` ghi "exits non-zero to block the edit" — sai cơ chế (chỉ **exit code 2** mới chặn PreToolUse), nay đã sửa khớp với phần thân script, và ghi rõ script cần `jq` trên PATH.

**Chưa chạy được trong phiên soạn:** sandbox shell của môi trường soạn thảo không khởi động được (lỗi ACL NTFS của host), nên 2 script trên chưa được execute tại chỗ. Lần đầu chạy trong Claude Code hoặc trên máy bạn, hãy đọc output thật thay vì coi là đã xanh.

## Thay đổi ở bản v3 (trigger eval)

Đã tạo `evals/trigger-eval.json` cho cả 15 skill (~185 query, should-trigger + should-not-trigger, tập trung vào các cặp near-miss) và làm một vòng rà soát thủ công (đọc 15 description cạnh nhau, tự phán đoán từng query) — **không phải** vòng benchmark tự động thật (`run_loop.py` cần CLI `claude -p`, chỉ chạy được trong Claude Code, không gọi được từ đây). Chi tiết phương pháp, giới hạn, và toàn bộ phát hiện: xem `EVAL-REPORT.md`.

Tóm tắt 5 sửa thật tìm được: `write-prd` từng tự liệt kê trigger phrase trùng với `spec-driven-dev` ngay trong description của chính nó (lỗi tự gây ra, không phải do query mơ hồ) — đã bỏ. Ba cặp còn lại (`debug-fast`↔`security-audit`, `spec-driven-dev`↔`e2e-test`, `hooks-guardrails` vs git/React hook) được thêm cross-reference ngay trong nội dung skill để tự nhận diện và trỏ đúng hướng khi câu hỏi người dùng vốn dĩ mơ hồ.

File eval đã sẵn sàng để chạy vòng lặp tối ưu description thật trong Claude Code — lệnh cụ thể có trong `EVAL-REPORT.md`.

## Thay đổi ở bản v2 (review lại)

**Sửa lỗi chuỗi liên kết PRD → spec → implementation plan:** `spec-driven-dev` trước đây đọc PRD từ `docs/prd-*.md` nhưng không tự lưu output theo quy ước nào cả — nghĩa là `implementation-plan` không có cách nào chắc chắn tìm ra spec đã duyệt. Giờ `spec-driven-dev` lưu về `docs/spec-[feature-slug].md`, và `implementation-plan` chủ động tìm cả hai file theo quy ước trước khi hỏi lại user.

**Thêm template thật** cho `write-prd`, `spec-driven-dev`, `ui-ux-brief` (`references/*.md`) — trước đây 3 skill này chỉ liệt kê tên section, mỗi lần chạy Claude tự bịa lại cấu trúc Markdown, không đảm bảo nhất quán giữa các lần chạy hay giữa các session khác nhau.

**`hooks-guardrails`**: bỏ luật cứng "mỗi script dưới 20 dòng" (không có lý do rõ ràng, dễ trở thành giới hạn giả tạo) và sửa lỗi thực tế — hook `PreToolUse` của Claude Code cần thoát bằng **exit code 2** để thực sự chặn hành động, exit code khác chỉ báo lỗi chứ không chặn. Bản gốc chỉ nói "exit non-zero" là chưa đúng cơ chế. Thêm `scripts/protect-paths.sh`, `scripts/lint-and-typecheck.sh`, `references/settings-example.json` chạy được thật, và ghi rõ skill này **chỉ hoạt động trên Claude Code** (hooks không tồn tại trên claude.ai/Cowork).

**`plan-mode` vs `implementation-plan`**: hai skill này có mô tả trigger khá gần nhau ("plan trước khi code" có thể khớp cả hai). Thêm một dòng phân định rõ: đã có spec/PRD duyệt rồi → dùng `implementation-plan`; chưa có gì chính thức, chỉ là task rủi ro → dùng `plan-mode`.

**`connect-database`**: nới lỏng luật "mỗi bảng một typed query helper" — đây là một lựa chọn kiến trúc cụ thể, không phù hợp mọi stack (GraphQL resolver, repository pattern, ORM method có sẵn). Giữ tinh thần "đừng rải raw SQL khắp nơi" nhưng không ép khuôn cụ thể.

**`security-audit`**: thêm phần Scope rõ ràng (chỉ audit code do user sở hữu, không phải hệ thống live của bên thứ ba) và giới hạn mức độ chi tiết của proof-of-concept — đủ để chứng minh và sửa lỗi, không phải một exploit script dùng được ngay. Đây vốn là tinh thần bản gốc đã có ("defensive exercise") nhưng viết rõ hơn để không mơ hồ khi audit chạm tới các lỗ hổng nghiêm trọng.

**`wire-mcp-server`**: bước 3 (tự scaffold MCP server bằng SDK) trùng lặp với skill `mcp-builder` có sẵn trong nhiều môi trường Claude Code (chi tiết hơn nhiều — FastMCP, Node SDK, auth, error handling). Sửa lại để `wire-mcp-server` lo phần quyết định "có nên tự build không + wiring vào project", còn phần scaffold chi tiết nhường cho `mcp-builder` nếu có, tránh hai skill đưa ra hướng dẫn xung đột nhau. Thêm `assets/mcp-config-template.json` mẫu.

**`task-to-skill`**: tương tự, đây là bản "capture nhanh" — nếu có `skill-creator` (bộ công cụ test/eval/tối ưu description bài bản hơn), skill này nên bàn giao cho nó thay vì tự làm lại vòng lặp iterate.

**Giữ nguyên không đổi**: `write-prd` (phần còn lại), `debug-fast`, `e2e-test`, `git-commit`, `cleanup-dead-code`, `create-claude-md` — 5 skill này đã đủ chặt: có lý do rõ ràng cho từng luật, tránh tính từ mơ hồ, có "done when"/proof cụ thể, và không đụng vấn đề gì cần sửa.

## Ghi chú

- Mỗi `SKILL.md` đã pass `quick_validate.py` (frontmatter hợp lệ, tên kebab-case,
  description dưới 1024 ký tự).
- Nội dung giữ nguyên tinh thần checklist trong ảnh gốc, nhưng viết lại theo
  hướng "hướng dẫn cho Claude" thay vì "prompt điền chỗ trống", vì đó là cách
  skill hoạt động.
- Nếu muốn dùng riêng lẻ trên claude.ai (không phải Claude Code) — mỗi skill
  cần đóng gói thành file `.skill` riêng, nói mình pack cho.
- `connect-database` có thêm 1 dòng theo hướng bạn hay tự viết DDL/trigger tay
  thay vì để ORM tự generate — sửa lại trong file nếu không cần.
