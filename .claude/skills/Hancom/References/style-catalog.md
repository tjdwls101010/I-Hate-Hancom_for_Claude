# Style ID Catalog

This catalog documents the style IDs available in `templates/base/Contents/header.xml`. When writing section0.xml, every `charPrIDRef`, `paraPrIDRef`, and `borderFillIDRef` must reference an ID that exists here.

For working XML examples of each pattern, see the design catalog: `templates/design-catalog/section0.xml`.

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
| 15 | 15pt | 함초롬바탕 | **Yes** | black | **Bold keyword emphasis** (□ items) |
| 4 | 15pt | 함초롬바탕 | **Yes** | black, **shade=#FFD700** | **○-level heading with gold shade** |
| 17 | 15pt | 맑은 고딕 | No | black | **Underline emphasis** (underline=BOTTOM) |

### Tables and Metadata

| ID | Size | Font | Bold | Color | Use For |
|----|------|------|------|-------|---------|
| 18 | 12pt | 바탕 | No | black | **Table body cells** |
| 13 | 12pt | 돋움체 | **Yes** | black | **Table header cells, row labels** |
| 16 | 12pt | 맑은 고딕 | **Yes** | black | **< Caption > text** |
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
| 1 | JUSTIFY (indented) | **□/○ bullet items** |
| 15 | LEFT (deep indent) | **- sub-items, * deep sub-items** |
| 19 | CENTER | **Centered text** (titles, captions) |
| 20 | CENTER | Table cell center |
| 21 | RIGHT | **Right-aligned text** (dates, signatures) |
| 22 | CENTER | **Table cell content** |

### DANGEROUS IDs (never use for body text)

paraPr **2-8** are connected to outline headings and trigger automatic numbering.

---

## 3. Border/Fill Styles (borderFill)

| ID | Fill | Borders | Use For |
|----|------|---------|---------|
| 1 | none | NONE | Invisible (page border) |
| 2 | **#E3F4E3 (light green)** | SOLID | **Section header cell** |
| 3 | none | partial (L+R top) | Section header bracket piece |
| 4 | none | partial (L+Top+Bottom) | Cell border combo |
| 5 | none | partial (L only) | Cell border combo |
| 6 | none | partial (R+Bottom+L) | Cell border combo |
| 9 | none | SOLID all sides | **Standard table cell** |
| 11 | **#D9D9D9 (gray)** | SOLID all | **Gray table header** |
| 12 | **#C5D4F0 (blue)** | SOLID all | **Blue comparison table header** |
| 13 | **#F5F5F5 (light gray)** | SOLID 0.4mm | **※ Note/warning box** |
| 14 | **#ECF2FA (light blue)** | DASH all | **Info/guide box** |

---

## 4. Common Style Combinations

| Pattern | charPr | paraPr | borderFill |
|---------|--------|--------|------------|
| Body paragraph | 12 | 0 | — |
| Spacer line | 10 | 0 | — |
| Main title | 19 | 19 | — |
| Right-aligned date | 12 | 21 | — |
| □ major topic | 12 + 15 | 1 | — |
| ○ sub-topic (gold shade) | 12 + **4** | 1 | — |
| - sub-item | 12 | **15** | — |
| Bold emphasis | 15 + 12 | 0 | — |
| Underline emphasis | 17 + 12 | 1 | — |
| < Caption > | 16 | 19 | — |
| Section header # cell | 1 | 22 | **2** (green) |
| Section header title | 14 | 22 | 9 |
| Table header cell | 13 | 22 | 11 or 12 |
| Table body cell | 18 | 22 or 0 | 9 |
| Note box (※) | 0 | 0 | 13 |
| Info box | 18 | 0 | 14 |

---

## 5. Safety Checklist

- [ ] All charPrIDRef values ≤ 19
- [ ] All paraPrIDRef values ≤ 22
- [ ] All borderFillIDRef values ≤ 14
- [ ] No paraPrIDRef in range 2-8
- [ ] Table rowCnt/colCnt match actual rows/columns
- [ ] Section header uses 2x4 table structure (copy from catalog exactly)
