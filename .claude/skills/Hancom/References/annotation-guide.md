# Annotation Guide

## How Annotations Work

After normalizing the markdown, Claude adds HTML comments as design instructions. Python's converter reads these annotations and applies the corresponding HWPX styles.

**Key principle: annotations specify MEANING, not APPEARANCE.** Write `<!-- table:compare -->` (semantic role), never `<!-- table:blue-header -->` (visual style). This separates design intent from implementation — if the color scheme changes later, only the converter needs updating, not every annotated document.

Most markdown elements need NO annotation. Python auto-detects headings, bullets, tables, and paragraphs from standard markdown syntax. Annotations are only for decisions that require Claude's judgment about the content's purpose.

## Annotation Reference

### `<!-- pagebreak -->`

Forces a new page before the next element. Place on its own line immediately before the `##` heading.

**When to use**: Major thematic transitions where a reader would expect a new chapter or section to start on a fresh page. Not every `##` needs one — only the significant shifts.

**Example**: A 12-section analysis report might get 3 pagebreaks:

```markdown
## 1. 개요          ← no pagebreak (right after title)
## 2. 방법론        ← no pagebreak (still setup)

<!-- pagebreak -->
## 3. 분석 결과     ← YES: transition from setup to results

## 4. 비교 분석     ← no pagebreak (continuation of results)

<!-- pagebreak -->
## 5. 국가별 분포   ← YES: new analysis dimension

## 6. 연도별 변화   ← no pagebreak (same dimension, different axis)
## 7. 토픽 간 관계  ← no pagebreak (still analysis)

<!-- pagebreak -->
## 8. 핵심 발견사항  ← YES: conclusions deserve their own page
```

**Decision principle**: Imagine printing this document. Where would you naturally start a new chapter?

### `<!-- table:data -->`

Place on the line immediately before the table's header row.

**When to use**: Tables that list items, catalog entries, time-series data, or file inventories. The reader is looking up facts — "what exists?" or "what happened when?"

**Examples**:
- 토픽 목록 (10 topics with attributes)
- 연도별 상위 토픽 (year × top topics)
- 생성 파일 목록 (file name + description)
- 유사도 순위 (ranked pairs with scores)

### `<!-- table:compare -->`

Place on the line immediately before the table's header row.

**When to use**: Tables comparing entities across the same dimensions. The reader is asking "how do they differ?" — countries vs countries, methods vs methods, growth vs decline.

**Examples**:
- 국가별 상위 토픽 (US vs CN vs JP vs KR)
- 군집별 주요 토픽 (Cluster 0 vs 1 vs 2 vs 3)
- 성장률 비교 (성장 토픽 vs 하락 토픽)
- 경쟁 환경 (국가 × 강점 분야)

**Distinguishing data from compare**: Ask yourself — is the first column a label for looking something up (data), or an entity being compared against others (compare)?

```markdown
<!-- table:data -->
| 연도 | 1순위 | 비율 |        ← 연도 = lookup key, not an entity being compared

<!-- table:compare -->
| 국가 | 1순위 토픽 | 2순위 토픽 |  ← 국가 = entities being compared
```

### `<!-- box:note -->` ... `<!-- /box -->`

Wraps content in a warning/caution box.

**When to use**: Content the reader must not miss — warnings, prerequisites, important caveats. The content says "watch out" or "be aware."

```markdown
<!-- box:note -->
※ 이 분석은 2025년 11월 기준 데이터를 사용하였으며, 이후 변동이 있을 수 있습니다.
<!-- /box -->
```

### `<!-- box:info -->` ... `<!-- /box -->`

Wraps content in an informational reference box.

**When to use**: Reference material, criteria lists, supplementary context that readers scan rather than deep-read. The content says "here's useful context."

```markdown
<!-- box:info -->
- **정량적**: Reconstruction Error, Topic Coherence, Sparsity
- **정성적**: 토픽 레이블 명확성, 키워드 해석 가능성, 비즈니스 의미 도출 용이성
<!-- /box -->
```

### `<!-- box:wrapper -->` ... `<!-- /box -->`

Groups related elements into a single bordered unit.

**When to use**: An introductory paragraph and its table belong together, or a description and its accompanying list form one logical unit.

```markdown
<!-- box:wrapper -->
『모두의 창업 프로젝트』는 일반/기술트랙과 로컬트랙으로 구분하여 운영됩니다.

| 구분 | 일반/기술트랙 | 로컬트랙 |
|------|-------------|---------|
| 모집규모 | 4,000명 | 1,000명 |
<!-- /box -->
```

## What NOT to Annotate

Python auto-detects these from markdown syntax. Adding annotations would be redundant:

| Markdown | Auto-Detection | Result |
|----------|---------------|--------|
| `# Title` | First `#` in document | Main title |
| `## Heading` | Any `##` | Section header (□ level) |
| `### Heading` | Any `###` | Subsection (○ level) |
| `- **key**: value` | Bold-colon pattern | □ bullet item with bold keyword |
| `- text` | Plain bullet | Body bullet item |
| `  - text` | Indented bullet | Sub-item with deeper indent |
| `| table |` (no annotation) | Default | Data table with gray header |
| Plain paragraph | No prefix | Body text with full-width indent |

**Note**: A table without any annotation defaults to `<!-- table:data -->`. Only add `<!-- table:compare -->` when the table is explicitly comparative.

## Decision Flowchart

**Table style?**
→ "Is the reader comparing entities?" → Yes → `compare` / No → `data`

**Pagebreak?**
→ "Would I start a new chapter here if this were a book?" → Yes → add / No → skip

**Box?**
→ "Does this content need visual separation from the surrounding flow?" → Yes → which type? / No → no box
→ "Is it a warning?" → `note`
→ "Is it reference material?" → `info`
→ "Is it a group of related elements?" → `wrapper`
