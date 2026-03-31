# Style ID Catalog

This catalog documents the style IDs available in `templates/base/Contents/header.xml`. When writing section0.xml, every `charPrIDRef`, `paraPrIDRef`, and `borderFillIDRef` must reference an ID that exists here.

For working XML examples of each pattern, see the design catalog: `templates/design-catalog/section0.xml`.

---

## 1. Font Faces

| ID | Font Name | Type | Role |
|----|-----------|------|------|
| 0 | 돋움체 | Sans-serif | Tables, metadata, small text |
| 1 | 맑은 고딕 | Sans-serif | Captions, UI-style text |
| 2 | 바탕 | Serif | Legacy body text |
| 3 | 바탕체 | Serif | Legacy fixed-width |
| 4 | 함초롬돋움 | Sans-serif | Title, headings |
| 5 | 함초롬바탕 | Serif | **Primary body text** |
| 6 | HY울릉도M | Display | Decorative (rare) |
| 7 | HY헤드라인M | Display | **Section header titles** |
| 8 | 휴먼명조 | Serif | **Bold body emphasis** |

---

## 2. Character Styles (charPr)

### Body Text

| ID | Size | Font | Bold | Color | Use For |
|----|------|------|------|-------|---------|
| 9 | 14pt | 함초롬바탕 (5) | No | black | **Standard body text** |
| 34 | 15pt | 휴먼명조 (8) | **Yes** | black | **Bold keyword emphasis** |
| 7 | 15pt | 함초롬바탕 (5) | No | black | Large body (rare) |
| 5 | 11pt | — | No | black | Parenthetical reduction |

### Titles and Headers

| ID | Size | Font | Bold | Color | Use For |
|----|------|------|------|-------|---------|
| 128 | 26pt | 함초롬돋움 (4) | **Yes** | black | **Main document title** |
| 26 | 17pt | HY헤드라인M (7) | No | **white** | **Section number on navy bg** |
| 29 | 15pt | HY헤드라인M (7) | **Yes** | black | **Section header title** |

### Tables and Metadata

| ID | Size | Font | Bold | Color | Use For |
|----|------|------|------|-------|---------|
| 109 | 12pt | 바탕 (2) | No | black | **Table body cells** |
| 10 | 12pt | 돋움체 (0) | **Yes** | black | **Table header cells, row labels** |
| 51 | 12pt | 맑은 고딕 (1) | **Yes** | black | **< Caption > text** |
| 10 | 12pt | 돋움체 (0) | **Yes** | black | Small bold keywords |

### Special Purpose

| ID | Size | Font | Bold | Color | Use For |
|----|------|------|------|-------|---------|
| 5 | 11pt | 함초롬돋움 (4) | No | black | **Spacer line** (small empty paragraph) |
| 99 | 15pt | 맑은 고딕 (1) | No | black | **○-level underline emphasis** (underline=BOTTOM) |
| 8 | 10pt | 돋움체 (0) | No | **white** | Text on dark background (small) |
| 55 | 16pt | — | No | **white** | Text on dark background (large) |

---

## 3. Paragraph Styles (paraPr)

### Safe IDs (use freely)

| ID | Alignment | Left Indent | Use For |
|----|-----------|-------------|---------|
| 0 | JUSTIFY | 0 | **Default body paragraphs** |
| 1 | JUSTIFY | 1500 | **□/○ bullet items** (first indent level) |
| 14 | JUSTIFY | 1100 | **- sub-items** (second indent level) |
| 15 | JUSTIFY | 2200 | **\* deep sub-items** (third indent level) |
| 9 | JUSTIFY | 0 | English text (150% line spacing) |
| 19 | CENTER | 0 | **Centered text** (titles, captions in body) |
| 22 | CENTER | 0 | **Table cell content** (centered) |
| 29 | RIGHT | 0 | **Right-aligned text** (dates, signatures) |
| 33 | CENTER | 0 | **Section header title cell** |

### DANGEROUS IDs (never use for body text)

| ID Range | Why Dangerous |
|----------|---------------|
| **2 - 8** | Connected to `heading type="OUTLINE"`. Triggers automatic numbering (1., 가., 3)) that you cannot control. The document will show unexpected numbers. |

---

## 4. Border/Fill Styles (borderFill)

### Basic Borders

| ID | Borders | Fill | Use For |
|----|---------|------|---------|
| 1 | NONE | none | Invisible (page border) |
| 4 | SOLID 0.12mm all sides | none | **Standard table cell** |
| 13 | SOLID 0.12mm all sides | none | Simple box (no diagonal) |

### Colored Backgrounds (for table headers and boxes)

| ID | Borders | Fill Color | Use For |
|----|---------|------------|---------|
| 14 | SOLID 0.3mm all sides | **#000066 (navy)** | **Section header number cell** — requires white text! |
| 22 | SOLID 0.12mm all sides | **#D9D9D9 (medium gray)** | **Standard table header row** |
| 23 | SOLID 0.12mm all sides | **#C5D4F0 (medium blue)** | **Comparison/process table header** |
| 24 | SOLID 0.12mm top/L/R, DOUBLE_SLIM 0.5mm bottom | **#E5E5E5 (gray)** | Separator-style table header |
| 25 | **SOLID 0.4mm** all sides, **#AAAAAA** | **#F5F5F5 (very light gray)** | **※ Note/warning box** |
| 26 | **DASH** 0.12mm all sides | **#ECF2FA (light blue)** | **Info/guide box** |

### Cell Border Combinations (for complex tables)

| ID | Top | Right | Bottom | Left | Use For |
|----|-----|-------|--------|------|---------|
| 5 | SOLID | NONE | SOLID | SOLID | Left+Top+Bottom edge cell |
| 6 | SOLID | SOLID | SOLID | NONE | Right+Top+Bottom edge cell |
| 7 | SOLID | NONE | SOLID | NONE | Top+Bottom only (interior) |
| 8 | NONE | NONE | SOLID | SOLID | Left+Bottom edge cell |
| 9 | NONE | SOLID | SOLID | NONE | Right+Bottom edge cell |
| 10 | NONE | NONE | SOLID | NONE | Bottom only (interior) |

---

## 5. Common Style Combinations

These are the most frequently used combinations. The design catalog contains working XML for each.

| Pattern | charPr | paraPr | borderFill | Notes |
|---------|--------|--------|------------|-------|
| Body paragraph | 9 | 0 | — | Add 2× full-width space indent |
| Spacer line | 5 | 0 | — | 11pt, content: single space " " |
| Main title | 128 | 19 | — | Centered, 26pt bold |
| Right-aligned date | 9 | 29 | — | |
| □ major topic | 9 + 34 | 1 | — | Bold keyword in separate run |
| ○ sub-topic | 9 + 34 | 1 | — | Same as □ with ○ symbol |
| - sub-item | 9 | 14 | — | |
| * deep sub-item | 9 | 15 | — | |
| < Caption > | 51 | 19 | — | Escape < > as &amp;lt; &amp;gt; |
| Table header cell | 10 | 22 | 22 or 23 | 12pt bold, gray or blue background |
| Table body cell | 109 | 19 or 0 | 4 | 12pt, center or justify |
| Section # cell | 10 | 22 | 19 | 12pt bold, green L+T bracket |
| Section title cell | 29 | 33 | 20 | Bold heading, green R+T+B bracket |
| Section title cell | 29 | 33 | 4 | Bold heading font |
| Note box | 1 | 0 | 25 | 1x1 table, dashed gray |
| Info box | 0 | 0 | 26 | 1x1 table, dashed blue |

---

## 6. Safety Checklist

Before finalizing section0.xml, verify:

- [ ] No paraPrIDRef in range 2-8 used outside of intentional outline headings
- [ ] All charPrIDRef values ≤ 136 (max ID in header.xml)
- [ ] All paraPrIDRef values ≤ 62 (max ID in header.xml)
- [ ] All borderFillIDRef values ≤ 26 (max ID in header.xml)
- [ ] Navy background cells (bf14) use white text charPr (26, 8, or 55)
- [ ] Table rowCnt/colCnt match actual `<hp:tr>` and `<hp:tc>` counts
- [ ] Each `<hp:tc>` has all required attributes: name, header, hasMargin, protect, editable, dirty, borderFillIDRef
- [ ] Each `<hp:tc>` has children in order: cellAddr, cellSpan, cellSz, cellMargin, subList
