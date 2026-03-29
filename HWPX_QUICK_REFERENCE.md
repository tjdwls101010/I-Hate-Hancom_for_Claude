# HWPX Format - Quick Reference Guide

## File Organization

```
HWPX Document (ZIP)
│
├─ mimetype (first file, uncompressed)
│  └─ "application/hwp+zip"
│
├─ Contents/
│  ├─ content.hpf ────────┐ (Manifest & metadata)
│  ├─ header.xml ─────────┼─ Defines all styles/fonts
│  ├─ section0.xml ───────┼─ Document content
│  ├─ section1.xml (opt)  │
│  └─ section2.xml (opt)  │
│
├─ BinData/ ─────────────┐ (Binary resources)
│  ├─ image1.jpg         │
│  ├─ image2.jpg         │
│  └─ ...                │
│
├─ Preview/
│  ├─ PrvImage.png (thumbnail)
│  └─ PrvText.txt (text preview)
│
├─ META-INF/
│  ├─ container.xml
│  ├─ container.rdf
│  └─ manifest.xml
│
├─ version.xml
└─ settings.xml
```

---

## Content Flow

```
content.hpf (manifest)
  └─ Lists: header.xml, section0.xml, section1.xml, imageN.jpg
  └─ Metadata: creator, dates, keywords
  └─ Spine order: determines reading sequence

header.xml (styles library)
  ├─ Fonts (23 Hangul, 24 Latin, etc.)
  ├─ Character Styles (id="0" to "159")
  ├─ Paragraph Styles
  ├─ Border Fills (32 patterns)
  └─ Tab Stops

section0.xml (actual content)
  └─ Paragraphs
     └─ Runs (text segments with formatting)
        └─ References: charPrIDRef="37" → looks up style 37 in header.xml
```

---

## Creating HWPX - Essential Steps

### 1. Set up package structure
```
1. Create ZIP archive
2. Add mimetype as first file (uncompressed): "application/hwp+zip"
3. Create directory structure: Contents/, BinData/, META-INF/, Preview/
```

### 2. Define styles (header.xml)
```
- List all fonts to be used
- Define character properties (styles) with IDs (0-159)
- Define paragraph properties
- Define border/fill patterns
- Define numbering/bullets
```

### 3. Create content (section0.xml)
```
- Create paragraphs with <hp:p> elements
- Each paragraph contains <hp:run> elements
- Each run references charPrIDRef (must exist in header.xml)
- Add text with <hp:t> tags
- Add tables with <hp:tbl> elements
- Add images with <hp:pic> elements
```

### 4. Add images (BinData/)
```
- Place image files (JPG, PNG) in BinData/ folder
- Reference in content.hpf manifest
- Reference in section*.xml with <hc:img binaryItemIDRef="imageN"/>
```

### 5. Create metadata (content.hpf)
```
- List all resources in <opf:manifest>
- Set reading order in <opf:spine>
- Add metadata: creator, dates, keywords
- Set language: "ko" for Korean
```

### 6. Create supporting files
```
- version.xml: Application version info
- settings.xml: Document settings
- META-INF/container.xml: ODF container info
- META-INF/container.rdf: Hancom metadata
- Preview/PrvText.txt: Text preview
- Preview/PrvImage.png: Thumbnail image
```

---

## Critical Rules

| Rule | Impact | Example |
|------|--------|---------|
| ID consistency | References break | Define charPr id="37" in header, use charPrIDRef="37" in content |
| Namespace prefixes | XML parse error | hp: for paragraph, hh: for head, hc: for core |
| UTF-8 encoding | Corruption | All XML and text must be UTF-8 |
| Well-formed XML | Parse error | All tags must close, attributes must be quoted |
| HWPUNIT values | Layout wrong | Use integers for dimensions (not decimals) |
| ZIP first file | Format invalid | mimetype must be first entry in ZIP (uncompressed) |
| Section references | Document broken | If section1.xml referenced in spine, it must exist |
| Image references | Display missing | If imageN referenced in manifest, must exist in BinData |

---

## Key Attributes Cheatsheet

### Paragraph (<hp:p>)
```xml
<hp:p id="0" paraPrIDRef="83" styleIDRef="0" pageBreak="0">
  ├─ id: unique identifier
  ├─ paraPrIDRef: paragraph style from header (ID 0-100+)
  ├─ styleIDRef: named style reference
  └─ pageBreak: "0" (none) or "NEXTPAGE"
```

### Run (<hp:run>)
```xml
<hp:run charPrIDRef="37">
  └─ charPrIDRef: character style from header (ID 0-159)
```

### Table (<hp:tbl>)
```xml
<hp:tbl id="1234" rowCnt="2" colCnt="3" borderFillIDRef="6">
  ├─ rowCnt: number of rows
  ├─ colCnt: number of columns
  └─ borderFillIDRef: border pattern from header
```

### Table Cell (<hp:tc>)
```xml
<hp:tc borderFillIDRef="7" header="1">
  ├─ header: "1" for header row, "0" for data
  └─ borderFillIDRef: optional cell-specific border override
```

### Image (<hp:pic>)
```xml
<hp:pic id="img1" zOrder="5">
  <hp:curSz width="5000" height="3000"/>
  <hc:img binaryItemIDRef="image1" effect="REAL_PIC"/>
  └─ binaryItemIDRef: must match filename in BinData/
```

---

## Common Dimension Values (HWPUNIT)

| Description | HWPUNIT Value | Notes |
|---|---|---|
| Page width (A4) | 59528 | Default width |
| Page height (A4) | 84188 | Default height |
| Left margin | 5669 | Standard |
| Right margin | 5669 | Standard |
| Top margin | 4251 | Standard |
| Bottom margin | 4251 | Standard |
| Small font size | 900 | 9pt |
| Normal font size | 1000 | 10pt |
| Large font size | 1200 | 12pt |
| Header margin | 2834 | Space from top |
| Footer margin | 2834 | Space from bottom |

---

## Document Metadata in content.hpf

```xml
<opf:meta name="creator" content="text">User Name</opf:meta>
<opf:meta name="lastsaveby" content="text">User Name</opf:meta>
<opf:meta name="CreatedDate" content="text">2026-03-29T12:00:00Z</opf:meta>
<opf:meta name="ModifiedDate" content="text">2026-03-29T12:00:00Z</opf:meta>
<opf:meta name="date" content="text">2026년 3월 29일 일요일</opf:meta>
<opf:meta name="keyword" content="text">keyword1, keyword2</opf:meta>
<opf:meta name="subject" content="text">Document subject</opf:meta>
<opf:meta name="description" content="text">Document description</opf:meta>
```

---

## Font Configuration Pattern

```xml
<!-- In header.xml -->
<hh:fontfaces itemCnt="7">
  <hh:fontface lang="HANGUL" fontCnt="23">
    <hh:font id="0" face="굴림" type="TTF" isEmbedded="0"/>
    <hh:font id="1" face="돋움" type="TTF" isEmbedded="0"/>
    <!-- ... more fonts ... -->
  </hh:fontface>
  <hh:fontface lang="LATIN" fontCnt="24">
    <hh:font id="0" face="Arial" type="TTF" isEmbedded="0"/>
    <!-- ... -->
  </hh:fontface>
  <!-- HANJA, JAPANESE, OTHER, SYMBOL, USER ... -->
</hh:fontfaces>

<!-- Then reference in character properties -->
<hh:charPr id="37" height="1000">
  <hh:fontRef hangul="0" latin="0" hanja="0" japanese="0" other="0"/>
</hh:charPr>
```

---

## Minimal Valid HWPX Document Structure

```
1. Minimal content.hpf
   - Package declaration
   - At least one metadata element
   - Manifest listing header.xml, section0.xml
   - Spine referencing both

2. Minimal header.xml
   - One fontface with one font
   - One charPr (character style)
   - One paraPr (paragraph style)
   - One borderFill
   - One section declaration (secCnt="1")

3. Minimal section0.xml
   - One section <hs:sec>
   - At least one paragraph <hp:p>
   - At least one run <hp:run> with text <hp:t>

4. Supporting files
   - version.xml (can be minimal)
   - settings.xml (can be minimal)
   - META-INF files (can be minimal)
```

---

## Testing Checklist

- [ ] All XML files are valid, well-formed
- [ ] All namespaces are correctly declared
- [ ] All character property IDs in section*.xml exist in header.xml
- [ ] All paragraph property IDs in section*.xml exist in header.xml
- [ ] All borderFill references exist
- [ ] All images referenced in content exist in BinData/
- [ ] All images in BinData/ are referenced in manifest
- [ ] ZIP structure is correct (mimetype first, uncompressed)
- [ ] UTF-8 encoding throughout
- [ ] Section count in header.xml matches number of section*.xml files
- [ ] Spine order in content.hpf is valid
- [ ] No ID conflicts or missing references

