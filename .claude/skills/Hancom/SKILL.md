---
name: Hancom
description: HWPX 한컴문서를 읽고 작성하는 스킬. 한컴문서(HWPX) 파일을 분석하거나, 사용자가 제공한 내용을 바탕으로 한국 정부 공문서 수준의 문서를 생성한다. "한컴", "한글문서", "hwpx", "hwp", "보도자료 작성", "공문서 작성", "한컴으로 만들어줘", "hwpx로 저장", "이 hwpx 파일 읽어줘" 등의 요청이나 .hwpx 파일이 언급될 때 이 스킬을 사용한다. 한컴문서 관련 작업이라면 명시적으로 스킬을 요청하지 않아도 적극적으로 사용할 것.
---

# HWPX Document Skill

HWPX is Korea's standard document format — a ZIP archive containing XML files. The core idea: `header.xml` defines all styles by ID (like CSS), and `section0.xml` references those IDs to format content (like HTML). The converter (`md_to_hwpx.py`) handles all XML generation from annotated markdown.

## Reference Docs

| When | Read |
|------|------|
| Preparing content (normalize + annotate) | `references/content-prep-guide.md` |
| Understanding design principles | `references/document-design.md` |
| Looking up style IDs | `references/style-catalog.md` |
| Understanding HWPX XML structure | `references/hwpx-format.md` |

## Writing Workflow

### Step 1: Lint the markdown

Copy the original file and run mechanical cleanup:

```bash
cp original.md cleaned_original.md
python3 scripts/md_lint.py cleaned_original.md
```

This fixes heading level gaps, collapses consecutive blank lines, removes blank lines between list items, normalizes multiple spaces, and strips trailing whitespace. No semantic judgment — purely mechanical.

### Step 2: Prepare content (normalize + annotate)

Read `references/content-prep-guide.md`. Then Read() the linted file and Edit() in one pass:

- Restructure where needed (bullet→table conversions, condensing repetitive content)
- Add annotations where design judgment is needed (`<!-- table:compare -->`, `<!-- box:note -->`, etc.)
- Clean up Obsidian syntax, decorative emoji, inline URLs

Most elements need no annotation — the converter auto-detects headings, bullets, tables, and paragraphs from standard markdown syntax.

### Step 3: Convert to HWPX

```bash
python3 scripts/md_to_hwpx.py cleaned_original.md --output output.hwpx --build --title "문서 제목"
```

Images referenced in the markdown (`![](file.png)`) are automatically detected and embedded.

The converter handles all XML generation: headings, bullets, tables, boxes, images, spacing. No manual XML assembly needed.

## Reading Workflow

```bash
python3 scripts/read_hwpx.py input.hwpx           # text only
python3 scripts/read_hwpx.py input.hwpx --verbose  # with style info
```

## Critical Constraints

These are hard technical requirements — violating them crashes Hancom Office:

1. **Never hand-write header.xml** — always use `templates/base/Contents/header.xml`
2. **Never use Python ElementTree to write header.xml** — it rewrites `hh:`/`hc:` prefixes to `ns0:`/`ns1:`, breaking Hancom rendering
3. **Don't write secPr** — `build_hwpx.py` injects it from the template automatically
4. **paraPr 2-8 are dangerous** — they trigger auto-numbering. Use 0, 1, 15 for indentation

## Script Paths

All scripts are in `scripts/` within this skill directory:
- `scripts/md_lint.py` — mechanical markdown linter (pre-processing)
- `scripts/md_to_hwpx.py` — annotated markdown → HWPX (main converter)
- `scripts/build_hwpx.py` — section0.xml → HWPX ZIP assembly
- `scripts/validate_hwpx.py` — structural validation
- `scripts/read_hwpx.py` — HWPX → structured text extraction

Templates are in `templates/`:
- `templates/base/` — header.xml, secPr template, base ZIP structure
- `templates/xml-parts/` — XML fragment templates used by md_to_hwpx.py
