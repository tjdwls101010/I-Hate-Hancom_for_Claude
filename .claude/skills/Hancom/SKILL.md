---
name: Hancom
description: HWPX 한컴문서를 읽고 작성하는 스킬. 한컴문서(HWPX) 파일을 분석하거나, 사용자가 제공한 내용을 바탕으로 한국 정부 공문서 수준의 문서를 생성한다. "한컴", "한글문서", "hwpx", "hwp", "보도자료 작성", "공문서 작성", "한컴으로 만들어줘", "hwpx로 저장", "이 hwpx 파일 읽어줘" 등의 요청이나 .hwpx 파일이 언급될 때 이 스킬을 사용한다. 한컴문서 관련 작업이라면 명시적으로 스킬을 요청하지 않아도 적극적으로 사용할 것.
---

# HWPX Document Skill

HWPX is Korea's standard document format — a ZIP archive containing XML files. The core idea: `header.xml` defines all styles by ID (like CSS), and `section0.xml` references those IDs to format content (like HTML).

## Design Catalog — The Primary Reference

The file `templates/design-catalog/section0.xml` is a complete, valid HWPX document containing every design pattern you need. **This is your primary design source.** When generating documents, copy XML patterns from the catalog and replace the text content.

Each pattern in the catalog is marked with XML comments explaining:
- What the pattern is for
- Which style IDs it uses (charPr, paraPr, borderFill)
- When to use it

## Reference Docs

Read these only when you need deeper understanding beyond what the catalog shows:

| When | Read |
|------|------|
| Normalizing markdown before conversion | `references/normalization-guide.md` |
| Deciding which visual pattern fits your content | `references/document-design.md` |
| Looking up what a specific style ID does | `references/style-catalog.md` |
| Understanding XML structure rules (esp. tables) | `references/hwpx-format.md` |

## Writing Workflow

### Step 0: Normalize the markdown (if needed)

Read `references/normalization-guide.md`. Assess whether the input markdown needs structural normalization (bullet→table conversions, Obsidian syntax cleanup, repetitive content condensing). If yes, create a normalized copy using Edit() and work from that. If the document is prose/editorial with no structured data, skip to Step 1.

### Step 1: Analyze the markdown

Identify the structural elements in the user's content:
- **Title** → Main Title pattern
- **# Heading** → Section Header pattern (with page break)
- **Bold keywords** → □ Major Topic or ○ Sub-Topic patterns
- **Bullet lists** → - Sub-Item or * Deep Sub-Item patterns
- **Tables** → Data Table (gray header) or Comparison Table (blue header)
- **Blockquotes / notes** → Note Box (※) or Info Box patterns
- **Date / signature** → Right-Aligned Text pattern

### Step 2: Read the design catalog

```bash
# Always read the catalog before generating
cat templates/design-catalog/section0.xml
```

### Step 3: Assemble section0.xml

For each element in the markdown:
1. Find the matching pattern in the catalog (identified by XML comments)
2. Copy the pattern's XML structure exactly
3. Replace only the text content inside `<hp:t>` tags
4. Keep all style IDs (charPrIDRef, paraPrIDRef, borderFillIDRef) unchanged
5. For repeated elements (multiple □ items, multiple table rows), duplicate the pattern

**Key assembly rules:**
- Do NOT write secPr — `build_hwpx.py` auto-injects it
- Each `# Heading` starts a new page: set `pageBreak="1"` on the paragraph
- The first page has no section header table — it starts with the title
- Spacer lines (`charPr 1`, 9pt) go between every major element

### Step 4: Validate

```bash
python3 scripts/validate_hwpx.py --section section0.xml --header templates/base/Contents/header.xml
```

Fix any failures before proceeding. Common issues: wrong ID references, mismatched rowCnt/colCnt.

### Step 5: Build HWPX

```bash
python3 scripts/build_hwpx.py --section section0.xml --output output.hwpx --title "문서 제목"
```

With images:
```bash
python3 scripts/build_hwpx.py --section section0.xml --output output.hwpx --images logo.png chart.jpg
```

### Step 6: Fix tables if needed

```bash
python3 scripts/table_fixer.py output.hwpx --output fixed.hwpx
```

## Reading Workflow

```bash
python3 scripts/read_hwpx.py input.hwpx           # text only
python3 scripts/read_hwpx.py input.hwpx --verbose  # with style info
```

## Critical Constraints

These are hard technical requirements. Violating them crashes Hancom Office:

1. **Never hand-write header.xml** — always use `templates/base/Contents/header.xml`
2. **Don't write secPr** — `build_hwpx.py` injects it from the template automatically
3. **Tables go directly inside `<hp:run>`** — never wrap in `<hp:ctrl>`
4. **`<hp:tc>` needs all attributes**: `name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="N"`
5. **paraPr 2-8 are DANGEROUS** — they trigger auto-numbering. Use 0, 1, 15 for indentation
6. **Table rowCnt/colCnt must match actual rows/columns**
7. **cellAddr must be sequential** per row, accounting for colSpan
8. **Section header is a complex 2x4 table** — copy from catalog exactly, don't simplify

## Script Paths

All scripts are in `scripts/` within this skill directory:
- `scripts/build_hwpx.py` — XML → HWPX ZIP assembly
- `scripts/validate_hwpx.py` — structural validation
- `scripts/read_hwpx.py` — HWPX → structured text extraction
- `scripts/table_fixer.py` — auto-fix table structure issues

Templates are in `templates/`:
- `templates/base/` — header.xml, secPr template, base ZIP structure
- `templates/design-catalog/` — model document with all design patterns
