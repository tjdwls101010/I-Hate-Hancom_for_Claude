# Style ID Catalog

This catalog documents the style IDs available in `templates/base/Contents/header.xml`. The converter (`md_to_hwpx.py`) references these IDs via its `CHAR`, `PARA`, and `BF` constants. This file is primarily for maintenance and debugging — you shouldn't need to look up IDs during normal document generation.

---

## 1. Character Styles (charPr)

### Titles and Headers

| ID | Size | Font | Bold | Color | Use For |
|----|------|------|------|-------|---------|
| 19 | 26pt | 바탕체 | **Yes** | black | **Main document title** |
| 1 | 16pt | HY울릉도M | No | black | **Section header number** |
| 14 | 15pt | HY울릉도M | **Yes** | black | **Section header title** |
| 9 | 16pt | 바탕체 | No | **#2E74B5 blue** | Blue accent text |

### Body Text

| ID | Size | Font | Bold | Color | Use For |
|----|------|------|------|-------|---------|
| 12 | 14pt | 함초롬돋움 | No | black | **Standard body text** |
| 20 | 14pt | 함초롬돋움 | **Yes** | black | **Body bold** (same size as 12, no spacing gap) |
| 15 | 15pt | 함초롬바탕 | **Yes** | black | **Large bold** (15pt, used for ▢ keyword emphasis) |
| 4 | 15pt | 함초롬바탕 | **Yes** | black, **shade=#FFD700** | **▢ heading with gold shade** |
| 21 | 14pt | 함초롬돋움 | **Yes** | black, **shade=#87CEEB** | **○ heading with sky blue shade** |
| 17 | 15pt | 맑은 고딕 | No | black | **Underline emphasis** (underline=BOTTOM) |

### Tables and Metadata

| ID | Size | Font | Bold | Color | Use For |
|----|------|------|------|-------|---------|
| 18 | 12pt | 바탕 | No | black | **Table body cells** |
| 13 | 12pt | 돋움체 | **Yes** | black | **Table header cells, row labels** |
| 16 | 12pt | 맑은 고딕 | **Yes** | black | **Caption text** |
| 5 | 10pt | 바탕체 | No | black | Table alternative text |

### Special Purpose

| ID | Size | Font | Bold | Color | Use For |
|----|------|------|------|-------|---------|
| 10 | 11pt | 바탕체 | No | black | **Spacer line** (empty paragraph) |
| 0 | 10pt | 함초롬돋움 | No | black | Default small text |
| 6 | 9pt | 바탕체 | No | black | Small compact text |

---

## 2. Paragraph Styles (paraPr)

| ID | Alignment | Use For |
|----|-----------|---------|
| 0 | JUSTIFY | **Default body paragraphs** |
| 1 | JUSTIFY (indented) | **▢/○ bullet items** |
| 15 | LEFT (deep indent) | **▷ sub-items** |
| 19 | CENTER | **Centered text** (titles, captions) |
| 21 | RIGHT | **Right-aligned text** (dates, signatures) |
| 22 | CENTER | **Table cell content** |

paraPr **2-8** are connected to outline headings and trigger automatic numbering — they should not be used for body text.

---

## 3. Border/Fill Styles (borderFill)

| ID | Fill | Borders | Use For |
|----|------|---------|---------|
| 1 | none | NONE | Invisible (page border) |
| 2 | **#E3F4E3 (light green)** | SOLID | **Section header cell** |
| 9 | none | SOLID all sides | **Standard table cell** |
| 11 | **#D9D9D9 (gray)** | SOLID all | **Gray data table header** |
| 12 | **#C5D4F0 (blue)** | SOLID all | **Blue comparison table header** |
| 13 | **#F5F5F5 (light gray)** | SOLID 0.4mm | **Note/warning box** |
| 14 | **#ECF2FA (light blue)** | DASH all | **Info/guide box** |

---

## 4. Common Style Combinations

These are the patterns used by `md_to_hwpx.py`:

| Pattern | charPr | paraPr | borderFill |
|---------|--------|--------|------------|
| Body paragraph | 12 | 0 | — |
| Body bold (`**text**`) | 20 + 12 | 0 | — |
| Spacer line | 10 | 0 | — |
| Main title | 19 | 19 | — |
| ▢ heading (gold shade) | 4 | 1 | — |
| ○ heading (sky blue shade) | 21 | 1 | — |
| ▷ bullet item | 12 (+ 20 for bold) | 1 | — |
| ▷ indented sub-item | 12 | 15 | — |
| ① numbered item | 12 (+ 20 for bold) | 1 | — |
| Section header # cell | 1 | 22 | **2** (green) |
| Section header title | 14 | 22 | 9 |
| Table header cell | 13 | 22 | 11 or 12 |
| Table body cell | 18 | 22 | 9 |
| Note box | 0 | 0 | 13 |
| Info box | 18 | 0 | 14 |

---

## 5. Safety Checklist

- [ ] All charPrIDRef values ≤ 21
- [ ] All paraPrIDRef values ≤ 22
- [ ] All borderFillIDRef values ≤ 14
- [ ] No paraPrIDRef in range 2-8
- [ ] Table rowCnt/colCnt match actual rows/columns
