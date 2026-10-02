# Trigger Eval Report — v3

## Cách làm và giới hạn thật của nó

Mỗi skill giờ có `evals/trigger-eval.json` — bộ query thật (6–14 should-trigger + 6–13 should-not-trigger mỗi skill, ~185 query tổng), theo đúng schema mà `skill-creator`'s `scripts/run_loop.py` nhận vào (`[{"query": ..., "should_trigger": true/false}]`).

**Việc đã làm trong session này:** tự đọc cả 15 description cạnh nhau (như thể chúng đang nằm chung trong `available_skills` thật), rồi tự phán đoán từng query nên/không nên trigger skill nào — một lần, bằng lý luận, không phải chạy lại nhiều lần qua model thật.

**Giới hạn cần biết:** đây **không phải** vòng lặp benchmark tự động thật của skill-creator. Vòng lặp thật (`scripts/run_loop.py`) cần CLI `claude -p`, chỉ có trên Claude Code — không gọi được từ môi trường chat này. Nó làm 3 việc mà bản thủ công này không làm được:
1. Chạy **nhiều lần lặp lại** (repeated sampling) để đo variance — model thật không phải lúc nào cũng quyết định giống nhau 2 lần liên tiếp với cùng 1 query.
2. Tách **train/test split** — tối ưu description trên một tập, xác nhận trên tập khác chưa từng thấy, tránh overfit description vào đúng bộ query mẫu.
3. Test với **toàn bộ 15 skill thật sự nằm trong context** của một model khác (không phải chính Claude đang viết ra description đó tự chấm nó).

Nói thẳng: bản phân tích thủ công này tốt để bắt các lỗi rõ ràng (từ ngữ trùng nhau giữa 2 description, thiếu ngữ cảnh phân biệt) — nhưng không thay được benchmark thật với variance thấp. Coi đây là "lint" cho description, không phải "test suite".

## Bổ sung ở v4: kiểm chứng offline lặp lại được (`scripts/`)

Bản rà soát dưới đây vẫn là thủ công. v4 thêm 2 script để phần "lint" không còn phụ thuộc trí nhớ người chấm:

- `python scripts/validate_skills.py` — kiểm cấu trúc (frontmatter, kebab-case khớp thư mục, description < 1024, mọi `references/...` phải tồn tại, eval đúng schema). Exit 1 khi lỗi.
- `python scripts/score_triggers.py` — baseline BM25: chấm mọi query eval với **cả 15 description cùng lúc**, in accuracy + bảng confusion. So sánh điểm trước/sau khi sửa một description để phát hiện hai description va nhau.

Hai script này **không** thay vòng lặp thật bên dưới (vẫn cần `claude -p` để đo variance và test split thật). Chúng chỉ biến bước lint thủ công thành bước chạy lại được. Xem `scripts/README.md`.

**Bổ sung ở v5:** thêm lớp eval chất lượng output (`evals/output-eval.md`) cho 4 skill có template — trước đó pack chỉ chấm *trigger*, chưa chấm *output*. `validate_skills.py` nay cảnh báo khi một skill có `references/*-template.md` mà thiếu rubric này.

**Kết quả chạy thật (2026-10-02, workspace_revision 15):**

- `validate_skills.py` → `15 skill(s): 0 error(s), 0 warning(s)`, exit 0.
- `score_triggers.py` → 83.3% (155/186), exit 0.
- Ca kiểm ngược (skill trỏ `references/khong-ton-tai.md`) → exit 1, đúng như thiết kế.

## Cách chạy vòng lặp thật sau này (trong Claude Code)

```bash
cd /path/to/skill-creator
python -m scripts.run_loop \
  --eval-set /path/to/.claude/skills/plan-mode/evals/trigger-eval.json \
  --skill-path /path/to/.claude/skills/plan-mode \
  --model claude-sonnet-4-6 \
  --max-iterations 5 \
  --verbose
```
Lặp lại cho từng skill. File eval đã có sẵn — chỉ cần trỏ đường dẫn.

## Phát hiện thật từ vòng rà soát thủ công

### 1. `write-prd` tự mâu thuẫn với `spec-driven-dev` (đã sửa — mức ưu tiên cao nhất)
Description gốc của `write-prd` liệt kê **"spec out this feature for me"** làm cụm trigger — nhưng đó gần như đúng y hệt cụm trigger của `spec-driven-dev` ("write a spec for X"). Đây không phải lỗi do query người dùng mơ hồ — chính bộ description tự giẫm lên nhau. Một câu như "spec out the referral program for me" trước đây có thể khớp cả hai.
**Sửa:** bỏ cụm đó khỏi `write-prd`, thay bằng "define this feature for me", và thêm câu chốt "Not for a technical given/when/then spec — that's spec-driven-dev" ngay trong description.

### 2. `debug-fast` ↔ `security-audit`: bug rò rỉ dữ liệu framed như "bug" thường
Query kiểu "users can see other people's orders by changing the id in the url" nằm đúng ranh giới: nghe như bug (debug-fast) nhưng thực chất là IDOR — nằm trong checklist của `security-audit`. Không có cách nào tách 100% chỉ bằng description vì phụ thuộc cách user diễn đạt.
**Sửa:** thêm cross-reference 2 chiều trong nội dung skill (không phải description, để tránh phình description) — `debug-fast` tự nhận diện và trỏ sang `security-audit` khi phát hiện đây là lỗi rò rỉ dữ liệu chứ không phải bug đơn lẻ; `security-audit` nhận diện khi user mô tả bằng ngôn ngữ "bug" nhưng bản chất là auth/IDOR.

### 3. `spec-driven-dev` ↔ `e2e-test`: cụm "given/when/then" dùng chung
`spec-driven-dev` dùng đúng thuật ngữ "given/when/then" trong description. Một query như "write given/when/then test cases for login, so QA can run them" vừa có tín hiệu spec ("given/when/then") vừa có tín hiệu test ("test cases", "QA can run"). Không giải quyết được 100% chỉ bằng description vì bản thân câu hỏi mơ hồ.
**Sửa:** thêm 1 dòng ở đầu mỗi skill: khác biệt cốt lõi là **tài liệu markdown** (spec-driven-dev) và **code chạy được** (e2e-test) — nếu chưa rõ, hỏi lại thay vì đoán.

### 4. `hooks-guardrails` vs git hook / React hook — nguy cơ thấp nhưng đáng vá
Từ "hook" bị dùng cho 3 khái niệm khác nhau hoàn toàn (Claude Code hooks, git hooks như husky, React hooks). Description gốc đã khá cụ thể (nêu tên PostToolUse/PreToolUse/Stop/Notification) nên rủi ro thực tế thấp, nhưng một query như "set up a pre-commit hook that runs lint with husky" không nhắc tên hook cụ thể nào của Claude Code — vẫn có thể bị model đọc lướt và match nhầm.
**Sửa:** thêm 1 câu tường minh phân biệt với git hooks và React hooks ngay trong body.

### Không tìm thấy vấn đề thật (đã kiểm tra kỹ vì nghi ngờ ban đầu)
- `plan-mode` ↔ `implementation-plan`: bản sửa ở v2 (điều kiện "đã có spec/PRD duyệt → dùng implementation-plan") đứng vững qua toàn bộ query test — không tìm thêm được ca nào gây nhầm lẫn mới.
- `wire-mcp-server` ↔ `connect-database`: từ "connect" trùng nhau về mặt chữ nhưng ngữ cảnh (database vs MCP/API) đủ khác biệt — không có ca nhầm lẫn thật.
- `wire-mcp-server` ↔ `mcp-builder` (nếu có trong môi trường): query "build a FastMCP server with 6 tools..." đúng ra VẪN nên trigger `wire-mcp-server` trước (nó là bước quyết định + wiring), rồi bên trong tự bàn giao phần scaffold cho `mcp-builder` — đây là thiết kế đúng từ v2, không phải lỗi.
- `task-to-skill` ↔ `skill-creator`, `task-to-skill` ↔ `create-claude-md`: description đủ tách biệt (skill workflow vs test/eval sâu vs file memory đơn), không tìm thấy ca nhầm.

## Tổng kết theo skill

| Skill | Số query | Vấn đề tìm thấy | Đã sửa |
|---|---|---|---|
| write-prd | 14 | Tự trùng trigger phrase với spec-driven-dev | ✅ |
| spec-driven-dev | 14 | Nhập nhằng "given/when/then" với e2e-test | ✅ |
| ui-ux-brief | 12 | Không | — |
| implementation-plan | 12 | Không (đã sạch từ v2) | — |
| plan-mode | 12 | Không (đã sạch từ v2) | — |
| wire-mcp-server | 12 | Không | — |
| connect-database | 12 | Không | — |
| security-audit | 13 | Nhập nhằng "bug" vs "vulnerability" với debug-fast | ✅ |
| debug-fast | 12 | (đối xứng với security-audit) | ✅ |
| cleanup-dead-code | 12 | Không | — |
| e2e-test | 13 | (đối xứng với spec-driven-dev) | ✅ |
| git-commit | 12 | Không | — |
| hooks-guardrails | 12 | Rủi ro thấp với từ "hook" dùng chung | ✅ |
| task-to-skill | 12 | Không | — |
| create-claude-md | 12 | Không | — |

**5/15 skill có sửa thật** dựa trên vòng rà soát này — 10 skill còn lại được xác nhận (ở mức độ "lint thủ công") là description đã đủ tách biệt.
