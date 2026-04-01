---
name: Hancom
description: HWPX 한컴문서를 읽고 작성하는 스킬. 한컴문서(HWPX) 파일을 분석하거나, 사용자가 제공한 내용을 바탕으로 한국 정부 공문서 수준의 문서를 생성한다. "한컴", "한글문서", "hwpx", "hwp", "보도자료 작성", "공문서 작성", "한컴으로 만들어줘", "hwpx로 저장", "이 hwpx 파일 읽어줘" 등의 요청이나 .hwpx 파일이 언급될 때 이 스킬을 사용한다. 한컴문서 관련 작업이라면 명시적으로 스킬을 요청하지 않아도 적극적으로 사용할 것.
---

# HWPX Document Skill

HWPX is Korea's standard document format — a ZIP archive containing XML files. The core idea: `header.xml` defines all styles by ID (like CSS), and `section0.xml` references those IDs to format content (like HTML).

## Reference Docs

| When | Read |
|------|------|
| Normalizing markdown before conversion | `references/normalization-guide.md` |
| Adding design annotations to markdown | `references/annotation-guide.md` |
| Deciding which visual pattern fits your content | `references/document-design.md` |
| Looking up what a specific style ID does | `references/style-catalog.md` |
| Understanding XML structure rules (esp. tables) | `references/hwpx-format.md` |

## Writing Workflow

### Step 1: Normalize the markdown (if needed)

Read `references/normalization-guide.md`. Assess whether the input markdown needs structural normalization (bullet→table conversions, Obsidian syntax cleanup, repetitive content condensing). If yes, create a normalized copy using Edit() and work from that. If the document is prose/editorial with no structured data, skip to Step 2.

### Step 2: Annotate the markdown

Read `references/annotation-guide.md`. Add HTML comment annotations for pagebreaks, table styles, and box types where design judgment is needed. Use Edit() to insert annotations into the normalized markdown. Most elements need no annotation — `md_to_hwpx.py` auto-detects from markdown syntax.

### Step 3: Convert to HWPX

```bash
python3 scripts/md_to_hwpx.py input.md --output output.hwpx --build --title "문서 제목"
```

With images (auto-detected from `![](file)` in markdown):
```bash
python3 scripts/md_to_hwpx.py input.md --output output.hwpx --build --title "문서 제목"
```

The converter handles all XML generation: headings, bullets, tables, boxes, images, spacing. No manual XML assembly needed.

### Step 4: Validate (optional)

```bash
python3 scripts/validate_hwpx.py --section section0.xml --header templates/base/Contents/header.xml
```

## Reading Workflow

```bash
python3 scripts/read_hwpx.py input.hwpx           # text only
python3 scripts/read_hwpx.py input.hwpx --verbose  # with style info
```

## Critical Constraints

These are hard technical requirements. Violating them crashes Hancom Office:

1. **Never hand-write header.xml** — always use `templates/base/Contents/header.xml`
2. **Never use Python ElementTree to write header.xml** — it rewrites `hh:`/`hc:` prefixes to `ns0:`/`ns1:`, breaking Hancom rendering
3. **Don't write secPr** — `build_hwpx.py` injects it from the template automatically
4. **paraPr 2-8 are DANGEROUS** — they trigger auto-numbering. Use 0, 1, 15 for indentation

## Script Paths

All scripts are in `scripts/` within this skill directory:
- `scripts/md_to_hwpx.py` — annotated markdown → HWPX (main converter)
- `scripts/build_hwpx.py` — section0.xml → HWPX ZIP assembly
- `scripts/validate_hwpx.py` — structural validation
- `scripts/read_hwpx.py` — HWPX → structured text extraction

Templates are in `templates/`:
- `templates/base/` — header.xml, secPr template, base ZIP structure
- `templates/xml-parts/` — XML fragment templates used by md_to_hwpx.py
