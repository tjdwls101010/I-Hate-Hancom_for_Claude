# Content Preparation Guide

## What this step does

One-pass semantic preparation: restructure content for formal documents and add design annotations. By this point, `md_lint.py` has already handled mechanical cleanup (heading levels, spacing, trailing whitespace), so this step focuses on decisions that require understanding the content's meaning.

Work from a copy of the original file (`cleaned_*.md`). Read the entire document first, assess the document type, then Edit() to apply all changes in one pass.

## The core judgment: table or bullets?

Markdown is optimized for fast authoring — bullets are the default tool. Formal Korean documents are optimized for structured reading — tables are the default tool. The question is always: does the **nature of the information** call for restructuring?

### Convert to table when the data has repeating structure

If the same set of fields appears multiple times across separate items, a table compresses the information and makes comparison effortless.

**Example — 10 topics with the same 4 attributes each (60+ lines → 12 lines)**

Before:
```markdown
#### Topic 0: Data Storage
- **Documents**: 3,636 (81.4%)
- **Variance**: 0.0040
- **Keywords**: based, intelligence, artificial
- **Cluster**: Cluster 2

#### Topic 1: Smart Factory
- **Documents**: 661 (14.8%)
- **Variance**: 0.0206
...
(repeated 10 times)
```

After:
```markdown
| Topic | Name | Documents | Variance | Cluster | Keywords |
|:---:|--------|--------:|:--------:|:--------:|------------|
| 0 | Data Storage | 3,636 (81.4%) | 0.0040 | Cluster 2 | based, intelligence, artificial |
| 1 | Smart Factory | 661 (14.8%) | 0.0206 | Cluster 3 | automation, water, production |
...
```

The principle at work: 10 items sharing 4 fields is tabular data wearing a bullet-list costume. The table reveals the structure that was always there.

### Keep as bullets when the content is not tabular

**Few key-value pairs (3-4 items)** — A 2-column table with "항목 | 내용" headers adds overhead without improving readability. These map naturally to bullet items in the final document.

```markdown
## 1. Overview
- **Analysis date**: 2025-11-13
- **Data**: 4,469 patent documents
- **Final topics**: 10
```

**Sequential reasoning** — Numbered logic steps have flow. A table would flatten it.

```markdown
- **Selection rationale**:
  1. Considered 2-3x the K-means 4 clusters
  2. Cluster 2 (43%) too large, needs segmentation
  3. Business interpretability
```

**Editorial/argumentative text** — Quotes, analysis, opinions are inherently non-tabular. Don't touch them.

```markdown
- Kyunghyang Shinmun called it a "temporary warm wind."
- Researcher Lee said "energy efficiency projects should be reflected in the supplementary budget."
```

## What to condense

When every item in a list says essentially the same thing, distill the actual insight.

Before (repetitive — no information gain):
```markdown
- **US**: Data storage dominant (93.1%)
- **CN**: Data storage dominant (78.3%)
- **JP**: Data storage dominant (86.7%)
- **KR**: Data storage dominant (91.2%)
```

After (highlights what actually differs):
```markdown
- All countries dominated by **data storage** (78-93%)
- **CN** uniquely high in smart factory automation (18.9%)
- **KR** uniquely has multi-agent collaboration as #2 (7.0%)
```

The principle: if you can summarize N items in one sentence, the list isn't earning its space. Condense the common pattern, then call out the exceptions.

## What to clean up

These are content-level cleanups that require understanding context (unlike lint, which is purely mechanical):

- **Obsidian image embeds**: `![[image.jpg]]` → `![](image.jpg)` — convert to standard markdown syntax so the converter can find the file
- **Inline URLs in formal documents**: `[link text](https://very-long-url...)` → keep only `link text` — URLs clutter printed documents and aren't clickable in Hancom
- **Decorative emoji in headings**: `## 🔥Project Maven` → `## Project Maven` — formal documents don't use emoji

## Heading hierarchy

The converter maps markdown headings to specific visual patterns:

```
#    → Document title (one per document, centered, 26pt)
##   → Section header (green table with number, page break)
       Numbered: "## 1. Analysis Results" → section header table
       Unnumbered: "## Key Findings" → ▢ gold shade heading
###  → ▢ Major topic (gold shade, bold)
#### → ○ Sub-topic (sky blue shade, bold)
```

Numbering matters: `## 3. Section Name` produces a formal section header table (green background, page number cell). `## Section Name` without a number produces a simpler ▢-style heading.

## Annotations

Annotations are HTML comments that tell the converter about design intent. The principle: **annotations specify MEANING, not APPEARANCE**. Write `<!-- table:compare -->` (semantic role), not `<!-- table:blue-header -->` (visual style).

Most elements need no annotation — the converter auto-detects headings, bullets, tables, and paragraphs from standard markdown syntax. Only add annotations where your judgment about the content's purpose is needed.

### Pagebreaks

`<!-- pagebreak -->` forces a new page before the next element. Place on its own line before a `##` heading.

Not every `##` needs one — only the significant thematic transitions. Imagine printing the document: where would you naturally start a new chapter?

**Example** — a 12-section analysis report gets 3 pagebreaks:
```markdown
## 1. Overview          ← no pagebreak (right after title)
## 2. Methodology       ← no pagebreak (still setup)

<!-- pagebreak -->
## 3. Analysis Results  ← YES: transition from setup to results

## 4. Comparison        ← no pagebreak (continuation of results)

<!-- pagebreak -->
## 5. Country Analysis  ← YES: new analysis dimension

## 6. Yearly Trends     ← no pagebreak (same dimension, different axis)

<!-- pagebreak -->
## 8. Key Findings      ← YES: conclusions deserve their own page
```

Note: `##` sections already get automatic page breaks from the converter. Use `<!-- pagebreak -->` only when you want to override the default behavior or add breaks at non-heading positions.

### Table styles

Place on the line immediately before the table's header row.

**`<!-- table:data -->`** — Tables listing items, catalogs, time-series data. The reader is looking up facts. This is the default — tables without annotation get this style.

**`<!-- table:compare -->`** — Tables comparing entities across the same dimensions. The reader is asking "how do they differ?"

How to tell them apart: is the first column a lookup key (data), or an entity being compared against others (compare)?

```markdown
<!-- table:data -->
| Year | Top Topic | Share |       ← year = lookup key

<!-- table:compare -->
| Country | #1 Topic | #2 Topic |  ← country = entity being compared
```

### Boxes

Wrap content that needs visual separation from the surrounding flow.

**`<!-- box:note -->`** ... `<!-- /box -->` — Warnings, prerequisites, caveats. Content says "watch out."
```markdown
<!-- box:note -->
※ This analysis uses data as of November 2025 and may not reflect subsequent changes.
<!-- /box -->
```

**`<!-- box:info -->`** ... `<!-- /box -->` — Reference material, criteria lists, supplementary context.
```markdown
<!-- box:info -->
- **Quantitative**: Reconstruction Error, Topic Coherence, Sparsity
- **Qualitative**: Label clarity, keyword interpretability, business relevance
<!-- /box -->
```

**`<!-- box:wrapper -->`** ... `<!-- /box -->` — Groups related elements into one visual unit (e.g., intro paragraph + its table).
```markdown
<!-- box:wrapper -->
The program operates in General/Technical and Local tracks.

| Category | General/Technical | Local |
|----------|------------------|-------|
| Capacity | 4,000 | 1,000 |
<!-- /box -->
```

### What needs NO annotation (auto-detected)

| Markdown | Converter auto-detects as |
|----------|--------------------------|
| `# Title` | Main title (centered, 26pt) |
| `## N. Heading` | Numbered section header (green table) |
| `## Heading` | ▢ heading (gold shade) |
| `### Heading` | ▢ major topic (gold shade) |
| `#### Heading` | ○ sub-topic (sky blue shade) |
| `- **key**: value` | Bold-keyword bullet |
| `- text` | Body bullet (▷) |
| `  - text` | Indented sub-bullet (▷ with indent) |
| `1. text` | Numbered item (①②③) |
| `| table |` (no annotation) | Data table (gray header) |
| Plain paragraph | Body text (full-width indent) |

## Document types and expected effort

| Type | Effort | Typical actions |
|------|:------:|-----------------|
| Technical report / analysis | **HIGH** | Bullet→table conversions, condensing, multiple annotations |
| News digest | **LOW** | Obsidian cleanup, maybe pagebreaks between articles |
| Column / editorial | **MINIMAL** | Emoji removal at most, keep prose intact |
| Long-form article with images | **LOW** | Heading check, image syntax conversion |

Assess the document type first. If it's prose-heavy with no structured data sections, most of this guide doesn't apply — just clean up syntax and move on.
