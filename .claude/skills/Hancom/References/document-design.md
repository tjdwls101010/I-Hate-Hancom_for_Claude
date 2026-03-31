# Document Design Guide

This guide explains the *principles* behind Korean government document design — the WHY behind each visual choice. For the actual XML patterns, see the design catalog at `templates/design-catalog/section0.xml`.

## Core Values

Korean government documents optimize for three things simultaneously:

1. **Authority** — The document must look official. Color restraint (only navy/gray accents), justified text, serif body fonts, and structured headers all signal institutional credibility.

2. **Scannability** — Readers (legislators, executives, journalists) need to extract key info in 30 seconds. The □/○/- hierarchy, bold keyword markers, and table-based section headers exist for rapid visual scanning.

3. **Information density** — Government announcements pack enormous detail into few pages. Micro-spacing (9pt spacers instead of 14pt blank lines), compact tables, and indentation hierarchy compress information without sacrificing readability.

## Page Structure

A typical government document follows this flow:

```
Page 1 (Cover/Summary):
  Title (26pt, centered, bold)
  Spacer
  Introductory paragraph (with full-width indent)
  Spacer
  Date + Authority (right-aligned)
  Spacer
  Note box (※ prerequisites or key notices)
  Spacer
  Summary table (key facts at a glance)

Page 2+ (Sections):
  Section Header (table: navy number + title)
  Spacer
  □ Major topic (bold keyword label)
    ○ Sub-topic explanation
      - Detail item
      * Exception or footnote
  Spacer
  < Table Caption >
  Data table
  Spacer
  Info box (numbered steps or criteria)
```

## Decision Guide: Markdown → Design Pattern

Use this mapping to translate markdown elements into catalog patterns:

| Markdown Element | Design Pattern | Key Style IDs |
|-----------------|----------------|---------------|
| `# Heading` | Section Header (1x2 table, new page) | bf14 + bf4, charPr 26 + 29 |
| `## Heading` | □ Major Topic (NOT a section header) | charPr 34 (bold) + 9, paraPr 1 |
| `**bold text**` | Bold Emphasis (keyword bold) | charPr 34 (bold) + 9 (normal) |
| `- **keyword** text` | □ / ○ topic with bold label | charPr 9 + 34 + 9, paraPr 1 |
| `- list item` | ○ sub-topic or - sub-item | paraPr 1, 14, 15 |
| Indented `- item` | - sub-item (deeper indent) | paraPr 14 or 15 |
| `> blockquote` | Note Box (※) | bf25 (gray dashed) |
| Tables | Data Table or Comparison Table | bf22 (gray) or bf23 (blue) header |
| `code block` | Info Box | bf26 (blue dashed) |
| Paragraph text | Body Paragraph | charPr 9, paraPr 0 |
| Date/signature | Right-Aligned Text | paraPr 29 |

## The Symbol Hierarchy: □ ○ - *

Korean government documents use a strict visual hierarchy instead of numbered lists:

- **□ (네모)** — Major topics. Always followed by a bold keyword in parentheses: `□ (사업목적) 설명 텍스트`
- **○ (동그라미)** — Sub-topics under □. Same keyword+explanation format.
- **- (대시)** — Details under ○. Plain text, deeper indent.
- **\* (별표)** — Exceptions, footnotes, additional notes. Deepest indent.

This hierarchy is NOT decorative — it's a standardized information architecture that Korean civil servants and journalists are trained to scan.

## Professional Polish: What Separates Amateur from Expert

These subtle techniques are what make a document look professionally crafted:

### Full-width space indent
Every body paragraph starts with two ideographic spaces (U+3000 `　`). This creates a visual indent without relying on paragraph-level indentation. Do NOT apply to: table cells, titles, captions, or note box content.

### Micro-spacing (11pt spacers)
Between sections, use a spacer paragraph with charPr 5 (11pt) containing a single space. This creates ~80% of a full line's height — enough breathing room without wasting space. Never use a full-size (14pt) empty paragraph as a spacer.

### ○-level underline emphasis
Use charPr 99 (15pt 맑은고딕, underline BOTTOM) for ○-level keyword labels. This distinguishes ○ items from □ items and surrounding body text with a visible underline decoration.

### Bold keyword technique
In body text, bold only the key noun phrase, not the entire sentence. Critically, verb endings (-했다, -됩니다, -을 추진) must stay in normal weight. This creates a "journalist's highlight" effect.

**Example (split into runs):**
- Run 1 (charPr 9, normal): `　　정부는 `
- Run 2 (charPr 34, bold): `창업 생태계 혁신 방안`
- Run 3 (charPr 9, normal): `을 발표하였다.`

### Parenthetical reduction
Names, titles, and supplementary info in parentheses use a smaller font (charPr 5, 11pt) than the body text (charPr 9, 14pt). This prevents parenthetical info from visually competing with the main content.

### Font hierarchy
- **Serif fonts** (함초롬바탕, 휴먼명조) → body text, emphasis
- **Sans-serif fonts** (돋움체, 맑은 고딕) → tables, captions, metadata, notes

Never use sans-serif for body paragraphs or serif for table cells.

## Table Design

### Header rows need backgrounds
Every table header row must have a colored background. Without it, headers are indistinguishable from data rows.
- **Gray (bf22)** — Default for most data tables
- **Blue (bf23)** — For comparison, process, or highlight tables
- **Gray+double bottom (bf24)** — For separator-style headers

### Section headers are tables
Major section dividers (corresponding to `# Heading` in markdown) are 1x2 tables with green bracket borders:
- Left cell: Green top-left bracket (bf19), bold number (charPr 10), centered
- Right cell: Green right+top+bottom bracket (bf20), bold title (charPr 29)
- Not full-width — approximately 20000 HWPUNIT (~40% of content area)
- The paragraph containing this table has `pageBreak="1"` to start a new page

### Box patterns
- **Note box (bf25)**: Solid gray border + very light gray fill. For ※ warnings, prerequisites.
- **Info box (bf26)**: Dashed blue border + light blue fill. For guides, step lists, criteria.
- Both are 1x1 tables with full content width (48000 HWPUNIT).

### Content wrapper box
The original government documents wrap related content blocks inside a 1x1 table with bf4 (thin solid border, no fill). This creates visual grouping — e.g., on page 1, the track comparison introduction + summary table are wrapped together in one bordered box.

Use this pattern when:
- Page 1 has an introductory explanation followed by a summary table
- Code blocks in the markdown contain both text and a table
- Multiple related items should appear as a cohesive visual unit

### Table cell height
Use `height="1200"` (not 800) for table cell heights. This provides comfortable padding that matches real government documents. Cells auto-expand if content is longer, but the minimum height prevents cramped-looking tables.

## What NOT to Do

- Don't use paraPr 2-8 for body text (they trigger auto-numbering outlines)
- Don't put black text on navy backgrounds (use white charPr: 8, 26, or 55)
- Don't use 14pt empty lines as spacers (use 9pt charPr 1)
- Don't mix serif and sans-serif within the same text role
- Don't skip the spacer between elements — the document needs breathing room
- Don't generate header.xml from scratch — always use the base template
