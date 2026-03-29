# HWPX Format Technical Guide

A principle-based guide to the HWPX document format, derived from analysis of 6 Korean government documents.

---

## 1. Architecture: HWPX as a ZIP Package

HWPX follows the same philosophy as OOXML (.docx) and ODF (.odt): a document is a ZIP archive of XML files. This design separates concerns -- styles live apart from content, metadata apart from both -- enabling partial reads and parallel processing.

### Why ZIP?

ZIP provides random access to individual entries. A renderer can read `header.xml` once to build a style lookup table, then stream through `section0.xml` without holding the entire document in memory. Embedded images stay in `BinData/` without bloating the XML.

### ZIP Structure

```
document.hwpx (ZIP archive)
+-- mimetype                        # MUST be first entry, STORED (uncompressed)
+-- version.xml                     # App version info, STORED
+-- settings.xml                    # Application settings
+-- META-INF/
|   +-- container.xml               # ODF-style container pointer
|   +-- manifest.xml                # Package manifest (often empty)
|   +-- container.rdf               # Lists header.xml + all section files
+-- Contents/
|   +-- header.xml                  # Style definitions (the "stylesheet")
|   +-- section0.xml                # Document content (first section)
|   +-- section1.xml                # Additional sections if present
|   +-- content.hpf                 # Package manifest with metadata
+-- BinData/                        # Embedded images (PNG, JPG, etc.)
+-- Preview/                        # Thumbnail image + text preview
```

### Boilerplate vs. Dynamic Files

Most of the ZIP structure is boilerplate -- identical across every document:

- **mimetype**: Always `application/hwp+zip`
- **META-INF/container.xml**: Fixed ODF container pointing to `content.hpf`
- **META-INF/manifest.xml**: Typically an empty manifest `<odf:manifest .../>`
- **settings.xml**: Nearly identical across documents (only `CaretPosition` varies)

The files that actually differ per document:

- **Contents/header.xml**: All style definitions (fonts, charPr, paraPr, borderFill)
- **Contents/section*.xml**: The actual document content
- **Contents/content.hpf**: Package manifest, metadata, image references
- **META-INF/container.rdf**: Enumerates header.xml + section files

---

## 2. The ID Reference System: Separation of Style and Content

This is the single most important concept in HWPX. Understanding it unlocks everything else.

### The Principle

HWPX separates *what text says* from *how it looks*. All visual formatting is defined once in `header.xml` and assigned numeric IDs. Content in `section*.xml` references those IDs. This is conceptually identical to CSS classes in HTML.

```
header.xml                          section0.xml
+--------------------------+        +---------------------------+
| charPr id="7"            |  <---  | <hp:run charPrIDRef="7">  |
|   height="1600" (16pt)   |        |   <hp:t>Title</hp:t>     |
|   <hh:bold/>             |        | </hp:run>                 |
+--------------------------+        +---------------------------+
| paraPr id="3"            |  <---  | <hp:p paraPrIDRef="3">    |
|   align="CENTER"         |        |   ...                     |
+--------------------------+        +---------------------------+
| borderFill id="13"       |  <---  | <hp:tc borderFillIDRef="13">
|   bgColor="#D9D9D9"      |        |   ...                     |
+--------------------------+        +---------------------------+
```

### Why This Design?

1. **Consistency**: Change a style once in `header.xml`, every reference updates.
2. **Compactness**: A 50-page document might use only 30 unique character styles.
3. **Validation**: A renderer can pre-build lookup tables before processing content.

### The Four ID-Referenced Systems

| System | Defined in header.xml | Referenced by | Controls |
|--------|----------------------|---------------|----------|
| `charPr` | `<hh:charPr id="N">` | `charPrIDRef="N"` on `<hp:run>` | Font, size, bold, color, underline |
| `paraPr` | `<hh:paraPr id="N">` | `paraPrIDRef="N"` on `<hp:p>` | Alignment, spacing, margins, indent |
| `borderFill` | `<hh:borderFill id="N">` | `borderFillIDRef="N"` on `<hp:tc>`, `<hp:tbl>`, etc. | Borders, background colors |
| `fontface` | `<hh:font id="N">` | `fontRef` attributes inside `charPr` | Font family per language group |

Font references add a second level of indirection: `section0.xml` -> `charPr` -> `fontRef` -> `fontface`.

---

## 3. Namespaces

HWPX uses XML namespaces to partition elements by functional area. Each namespace prefix maps to a specific concern:

```xml
<!-- Header file (style definitions) -->
hh:  http://www.hancom.co.kr/hwpml/2011/head
hc:  http://www.hancom.co.kr/hwpml/2011/core

<!-- Section files (document content) -->
hp:  http://www.hancom.co.kr/hwpml/2011/paragraph
hs:  http://www.hancom.co.kr/hwpml/2011/section
hp10: http://www.hancom.co.kr/hwpml/2016/paragraph

<!-- Other -->
hm:  http://www.hancom.co.kr/hwpml/2011/master-page
hv:  http://www.hancom.co.kr/hwpml/2011/version
ha:  http://www.hancom.co.kr/hwpml/2011/app
hwpunitchar: http://www.hancom.co.kr/hwpml/2016/HwpUnitChar

<!-- Package metadata (ODF-based) -->
opf: http://www.idpf.org/2007/opf/
ocf: urn:oasis:names:tc:opendocument:xmlns:container
odf: urn:oasis:names:tc:opendocument:xmlns:manifest:1.0
```

The split between `hh:` (header) and `hp:` (paragraph) reinforces the style/content separation. You will never see `hh:charPr` inside a section file or `hp:run` inside `header.xml`.

---

## 4. Header.xml: The Style Definitions

### Font Faces

Fonts are organized by language group because Korean documents routinely mix Hangul, Latin, Hanja, and symbol characters -- each potentially needing a different typeface.

```xml
<hh:fontfaces itemCnt="7">
  <hh:fontface lang="HANGUL" fontCnt="5">
    <hh:font id="0" face="함초롬돋움" type="TTF" isEmbedded="0"/>
    <hh:font id="1" face="함초롬바탕" type="TTF" isEmbedded="0"/>
    <hh:font id="2" face="맑은 고딕" type="TTF" isEmbedded="0"/>
    <hh:font id="3" face="바탕" type="TTF" isEmbedded="0"/>
    <hh:font id="4" face="HY헤드라인M" type="TTF" isEmbedded="0"/>
  </hh:fontface>
  <hh:fontface lang="LATIN" fontCnt="3">
    <hh:font id="0" face="함초롬돋움" type="TTF" isEmbedded="0"/>
    <hh:font id="1" face="Times New Roman" type="TTF" isEmbedded="0"/>
    <!-- IDs are per-language-group, not global -->
  </hh:fontface>
  <hh:fontface lang="HANJA" fontCnt="2">...</hh:fontface>
  <hh:fontface lang="JAPANESE" fontCnt="2">...</hh:fontface>
  <hh:fontface lang="OTHER" fontCnt="2">...</hh:fontface>
  <hh:fontface lang="SYMBOL" fontCnt="2">...</hh:fontface>
  <hh:fontface lang="USER" fontCnt="2">...</hh:fontface>
</hh:fontfaces>
```

Font IDs are scoped per language group. `hangul="7"` in a `fontRef` means the 8th font (0-indexed) in the `HANGUL` fontface list, while `latin="16"` means the 17th font in the `LATIN` list.

### Character Properties (charPr)

Each `charPr` defines a complete character style. The `height` attribute is in **hundredths of a point** (1/100 pt).

```xml
<hh:charPr id="7" height="1600" textColor="#000000" shadeColor="none"
           useFontSpace="0" useKerning="0" symMark="NONE" borderFillIDRef="1">
  <hh:fontRef hangul="7" latin="16" hanja="11" japanese="11"
              other="10" symbol="12" user="9"/>
  <hh:ratio hangul="100" latin="100" hanja="100" japanese="100"
            other="100" symbol="100" user="100"/>
  <hh:spacing hangul="0" latin="0" hanja="0" japanese="0"
              other="0" symbol="0" user="0"/>
  <hh:relSz hangul="100" latin="100" hanja="100" japanese="100"
            other="100" symbol="100" user="100"/>
  <hh:offset hangul="0" latin="0" hanja="0" japanese="0"
             other="0" symbol="0" user="0"/>
  <hh:bold/>
  <hh:underline type="NONE" shape="SOLID" color="#000000"/>
  <hh:strikeout shape="NONE" color="#000000"/>
  <hh:outline type="NONE"/>
  <hh:shadow type="NONE" color="#C0C0C0" offsetX="10" offsetY="10"/>
</hh:charPr>
```

Key points:
- **height="1600"** = 16pt. The formula: `pt = height / 100`.
- **`<hh:bold/>`**: Presence means bold is ON. Absence means normal weight. Same pattern for italic.
- **fontRef**: Each attribute references a font ID within its language group's fontface list.
- **textColor**: Standard hex color. Almost all government docs use `#000000`.

Common font sizes in government documents:

| height value | Point size | Typical use |
|-------------|-----------|-------------|
| 1000 | 10pt | Body text |
| 1200 | 12pt | Sub-body, emphasized body |
| 1400 | 14pt | Sub-headers |
| 1600 | 16pt | Section headers |
| 2000-2600 | 20-26pt | Document titles |

### Paragraph Properties (paraPr)

```xml
<hh:paraPr id="0" tabPrIDRef="0" condense="0" fontLineHeight="0" snapToGrid="1">
  <hh:align horizontal="JUSTIFY" vertical="BASELINE"/>
  <hh:lineSpacing type="PERCENT" value="160" unit="HWPUNIT"/>
  <hh:margin>
    <hc:intent value="0" unit="HWPUNIT"/>
    <hc:left value="0" unit="HWPUNIT"/>
    <hc:right value="0" unit="HWPUNIT"/>
    <hc:prev value="0" unit="HWPUNIT"/>
    <hc:next value="0" unit="HWPUNIT"/>
  </hh:margin>
  <hh:border borderFillIDRef="1" offsetLeft="0" offsetRight="0"
             offsetTop="0" offsetBottom="0"/>
</hh:paraPr>
```

- **JUSTIFY/BASELINE** is the dominant alignment in government documents.
- **Line spacing 160%** is the overwhelming standard (408 occurrences across 6 docs vs 98 for 130%).
- `<hc:prev>` and `<hc:next>` are paragraph spacing (before/after), not page margins.
- `<hc:intent>` is the first-line indent.

**The hp:switch pattern**: In practice, `paraPr` often uses an `hp:switch`/`hp:case`/`hp:default` wrapper to provide values in both HWPUNIT and legacy units for backward compatibility. When generating HWPX, you can use the direct form shown above.

### BorderFill

```xml
<hh:borderFill id="13">
  <hh:slash type="NONE" crooked="0" isCounter="0"/>
  <hh:border>
    <hh:left type="SOLID" width="0.12mm" color="#000000"/>
    <hh:right type="SOLID" width="0.12mm" color="#000000"/>
    <hh:top type="SOLID" width="0.12mm" color="#000000"/>
    <hh:bottom type="SOLID" width="0.12mm" color="#000000"/>
  </hh:border>
  <hh:fill>
    <hh:brushColor>
      <hh:windowBrush faceColor="#D9D9D9" hatchColor="none" alpha="0"/>
    </hh:brushColor>
  </hh:fill>
</hh:borderFill>
```

Common table header backgrounds in government documents:
- `#D9D9D9` -- light gray (most common)
- `#E0F4F6` -- light cyan
- `#DFE6F7` -- light blue

### Named Styles

Every government document includes these standard named styles (mapping a human-readable name to paraPr + charPr combinations):

| Style name | Korean | Purpose |
|-----------|--------|---------|
| Normal | 바탕글 | Default paragraph style |
| Body | 본문 | Body text |
| Outline 1-7 | 개요 1-7 | Heading levels |
| Page Number | 쪽번호 | Page numbering |
| Header | 머리말 | Page header |
| Footnote | 각주 | Footnote text |

---

## 5. Section XML: Document Content

### Paragraph Structure

A paragraph (`hp:p`) contains one or more runs (`hp:run`). Each run has its own character style, allowing mixed formatting within a single paragraph.

```xml
<hp:p id="2147483648" paraPrIDRef="0" styleIDRef="0"
      pageBreak="0" columnBreak="0" merged="0">
  <hp:run charPrIDRef="17">
    <hp:secPr>...</hp:secPr>  <!-- section properties, only in first paragraph -->
  </hp:run>
  <hp:run charPrIDRef="42">
    <hp:t>본문 텍스트입니다.</hp:t>
  </hp:run>
</hp:p>
```

Why multiple runs? Consider a paragraph where one word is bold: "This is **important** text." That requires three runs: normal, bold, normal -- each referencing a different `charPrIDRef`.

The first paragraph in a section typically contains an `hp:run` with `hp:secPr` (section properties) and no text. This defines page layout for the section.

### Section Properties (secPr)

Section properties define page geometry and appear inside the first run of the first paragraph:

```xml
<hp:secPr>
  <hp:pagePr landscape="WIDELY" width="59528" height="84188"
             gutterType="LEFT_ONLY">
    <hp:margin header="4252" footer="4252" left="8504" right="8504"
              top="5668" bottom="4252" gutter="0"/>
  </hp:pagePr>
  <hp:footNotePr>...</hp:footNotePr>
  <hp:endNotePr>...</hp:endNotePr>
  <hp:pageBorderFill type="BOTH" borderFillIDRef="1"
                     offsetLeft="1417" offsetRight="1417"
                     offsetTop="1417" offsetBottom="1417"/>
</hp:secPr>
```

**Units**: All dimensions use HWPUNIT where **7200 HWPUNIT = 1 inch**.

Standard A4 page: `width="59528" height="84188"` (approximately 210mm x 297mm).

Typical government document margins: ~20mm left/right, ~15mm top/bottom.

### Tables

Tables are the most structurally complex element. They follow a grid model similar to HTML tables.

```xml
<hp:tbl id="1234" numberingType="TABLE" textWrap="TOP_AND_BOTTOM"
        textFlow="BOTH_SIDES" rowCnt="3" colCnt="2" cellSpacing="0"
        borderFillIDRef="4" repeatHeader="1">
  <!-- Column width definitions (MUST match colCnt) -->
  <hp:gridCol>
    <hp:gridColItem width="14000"/>
    <hp:gridColItem width="14000"/>
  </hp:gridCol>

  <!-- Row 0 -->
  <hp:tr>
    <hp:tc borderFillIDRef="13" width="14000" header="0">
      <hp:cellAddr colAddr="0" rowAddr="0"/>
      <hp:cellSpan colSpan="1" rowSpan="1"/>
      <hp:cellSz width="14000" height="1000"/>
      <hp:cellMargin left="510" right="510" top="141" bottom="141"/>
      <hp:subList>
        <hp:p paraPrIDRef="0" styleIDRef="0">
          <hp:run charPrIDRef="5">
            <hp:t>Header Cell 1</hp:t>
          </hp:run>
        </hp:p>
      </hp:subList>
    </hp:tc>
    <hp:tc borderFillIDRef="13" width="14000" header="0">
      <hp:cellAddr colAddr="1" rowAddr="0"/>
      <hp:cellSpan colSpan="1" rowSpan="1"/>
      <hp:cellSz width="14000" height="1000"/>
      <hp:cellMargin left="510" right="510" top="141" bottom="141"/>
      <hp:subList>
        <hp:p paraPrIDRef="0" styleIDRef="0">
          <hp:run charPrIDRef="5">
            <hp:t>Header Cell 2</hp:t>
          </hp:run>
        </hp:p>
      </hp:subList>
    </hp:tc>
  </hp:tr>

  <!-- Row 1 -->
  <hp:tr>
    <hp:tc borderFillIDRef="4" width="14000" header="0">
      <hp:cellAddr colAddr="0" rowAddr="1"/>
      <hp:cellSpan colSpan="1" rowSpan="1"/>
      <hp:cellSz width="14000" height="1000"/>
      <hp:cellMargin left="510" right="510" top="141" bottom="141"/>
      <hp:subList>
        <hp:p paraPrIDRef="0" styleIDRef="0">
          <hp:run charPrIDRef="3">
            <hp:t>Data Cell</hp:t>
          </hp:run>
        </hp:p>
      </hp:subList>
    </hp:tc>
    <!-- ... more cells ... -->
  </hp:tr>
</hp:tbl>
```

**How tables embed in paragraphs**: A table is always a child of a `<hp:run>` inside a `<hp:p>`:

```xml
<hp:p paraPrIDRef="0" styleIDRef="0">
  <hp:run charPrIDRef="0">
    <hp:tbl ...>
      <!-- table content -->
    </hp:tbl>
  </hp:run>
</hp:p>
```

**Cell addressing**: `cellAddr` uses zero-based coordinates. In a 3-row, 2-column table:
- Row 0: `(colAddr=0, rowAddr=0)`, `(colAddr=1, rowAddr=0)`
- Row 1: `(colAddr=0, rowAddr=1)`, `(colAddr=1, rowAddr=1)`
- Row 2: `(colAddr=0, rowAddr=2)`, `(colAddr=1, rowAddr=2)`

**Cell content**: Each `<hp:tc>` contains a `<hp:subList>` which holds one or more `<hp:p>` paragraphs. This is recursive -- cells contain paragraphs, which can contain tables.

**repeatHeader="1"**: When set, the first row repeats on each page if the table spans multiple pages.

### Cell Merging

Merged cells use `colSpan` and `rowSpan` just like HTML. A cell spanning 2 columns and 3 rows:

```xml
<hp:cellSpan colSpan="2" rowSpan="3"/>
```

When cells are merged, the spanned positions are simply absent from the XML -- only the anchor cell (top-left of the merge region) appears.

---

## 6. Units and Measurements

HWPX uses a consistent unit system throughout:

| Unit | Conversion | Example |
|------|-----------|---------|
| HWPUNIT (dimensions) | 7200 = 1 inch | width="59528" (A4 width ~210mm) |
| Font height | 100 = 1pt | height="1600" = 16pt |
| Cell margins | HWPUNIT | left="510" (~1.8mm) |
| Border width | millimeters (string) | width="0.12mm" |

**Why HWPUNIT?** It provides sub-pixel precision without floating point. 7200 units per inch gives ~283 units per mm, enough for precise typographic layout with integer arithmetic.

---

## 7. Hard Technical Constraints

These are not design guidelines -- they are requirements that cause document corruption if violated.

1. **mimetype MUST be the first ZIP entry**, stored with STORED method (no compression). Many ZIP libraries default to DEFLATE; you must explicitly override this for the mimetype entry.

2. **All ID references must be valid.** Every `charPrIDRef`, `paraPrIDRef`, and `borderFillIDRef` in section files must correspond to an existing `id` attribute in `header.xml`. An invalid reference will cause rendering failures.

3. **Table dimensions must be consistent.** `rowCnt` must equal the actual number of `<hp:tr>` elements. `colCnt` must equal the number of `<hp:gridColItem>` elements and (for non-merged rows) the number of `<hp:tc>` per row.

4. **Cell addresses must be sequential.** `colAddr` increments from 0 within each row. `rowAddr` matches the row's position (0-indexed).

5. **Font IDs must be valid per language group.** Each `fontRef` attribute (hangul, latin, hanja, etc.) must reference a valid font ID within the corresponding language group in `fontfaces`.

6. **XML encoding must be UTF-8.**

7. **Namespace prefixes must be consistent** throughout each file.

---

## 8. Quick Reference

### Minimal Paragraph (body text, 10pt, justified)

```xml
<hp:p paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
  <hp:run charPrIDRef="3">
    <hp:t>본문 내용입니다.</hp:t>
  </hp:run>
</hp:p>
```

### Bold + Colored Run Within a Paragraph

```xml
<hp:p paraPrIDRef="0" styleIDRef="0">
  <hp:run charPrIDRef="3">
    <hp:t>일반 텍스트 </hp:t>
  </hp:run>
  <hp:run charPrIDRef="12">  <!-- charPr 12 has bold + textColor="#FF0000" -->
    <hp:t>강조 텍스트</hp:t>
  </hp:run>
  <hp:run charPrIDRef="3">
    <hp:t> 일반 텍스트</hp:t>
  </hp:run>
</hp:p>
```

### Government Document Defaults

```
Page:        A4 (59528 x 84188 HWPUNIT)
Margins:     ~20mm left/right, ~15mm top/bottom
Body font:   함초롬돋움 or 맑은 고딕, 10pt, black
Line spacing: 160%
Alignment:   JUSTIFY / BASELINE
Header bg:   #D9D9D9 (gray), #E0F4F6 (cyan), or #DFE6F7 (blue)
Text color:  #000000 (black); #0000FF (blue) and #FF0000 (red) for emphasis
```

### Font Size Cheat Sheet

```
height="1000"  ->  10pt  (body)
height="1200"  ->  12pt  (sub-body)
height="1400"  ->  14pt  (sub-header)
height="1600"  ->  16pt  (header)
height="2000"  ->  20pt  (title)
height="2600"  ->  26pt  (large title)
```

### HWPUNIT Conversions

```
7200 HWPUNIT  =  1 inch  =  25.4 mm  =  72 pt
1 mm          ~  283 HWPUNIT
1 pt          =  100 font height units
```

### ZIP Entry Order

```
1. mimetype          (STORED, uncompressed, must be first)
2. version.xml       (STORED)
3. META-INF/*        (DEFLATE)
4. Contents/*        (DEFLATE)
5. settings.xml      (DEFLATE)
6. BinData/*         (DEFLATE, if images exist)
7. Preview/*         (DEFLATE, optional)
```
