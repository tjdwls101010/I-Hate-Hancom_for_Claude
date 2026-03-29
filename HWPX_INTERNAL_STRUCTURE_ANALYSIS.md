# HWPX File Format - Internal Structure Analysis

## Executive Summary

HWPX files are ZIP archives containing XML-based documents compliant with the Hancom Office Hangul word processor format. The format is structurally similar to ODF (OpenDocument Format) but with Hancom-specific extensions.

---

## 1. ARCHIVE STRUCTURE

HWPX files are ZIP containers with the following directory structure:

```
document.hwpx (ZIP Archive)
├── mimetype                  (Plain text, MIME type declaration)
├── version.xml               (XML, Version information)
├── settings.xml              (XML, Application settings)
├── Contents/
│   ├── content.hpf           (XML, Package manifest - root package file)
│   ├── header.xml            (XML, Styles, fonts, formatting definitions)
│   ├── section0.xml          (XML, Document content - main text/tables/images)
│   ├── section1.xml          (Optional, for multi-section documents)
│   ├── section2.xml          (Optional, for multi-section documents)
│   └── ...
├── BinData/
│   ├── image1.jpg            (Binary image files)
│   ├── image2.jpg
│   ├── image3.png
│   └── ...
├── Preview/
│   ├── PrvImage.png          (Preview thumbnail)
│   └── PrvText.txt           (Plain text preview)
└── META-INF/
    ├── container.xml         (XML, ODF container metadata)
    ├── container.rdf         (RDF, Hancom-specific metadata)
    └── manifest.xml          (XML, File manifest)
```

### Key Points:
- **mimetype**: Must be first file in ZIP, contains `application/hwp+zip`
- **No line breaks in XML**: All XML files are single-line or very long lines (minified)
- **Section files**: Documents can have multiple sections (section0.xml, section1.xml, etc.)
- **Multi-language support**: Korean, Latin, Hanja, Japanese, Other character sets

---

## 2. CORE XML FILES

### 2.1 content.hpf (Package Manifest)
**Location**: `Contents/content.hpf`
**Purpose**: Root package file defining document structure and resources

**Structure**:
```xml
<opf:package> (Root element - ODF Package Format)
  ├── <opf:metadata>          (Document metadata)
  │   ├── <opf:title>
  │   ├── <opf:language>      (e.g., "ko" for Korean)
  │   └── <opf:meta>          (Creator, subject, description, dates, keywords)
  ├── <opf:manifest>          (References all resources)
  │   └── <opf:item>          (Points to header.xml, section*.xml, images)
  │       ├── id              (Unique identifier)
  │       ├── href            (File path within ZIP)
  │       ├── media-type      (MIME type)
  │       └── isEmbeded       (Whether binary is embedded)
  └── <opf:spine>             (Reading order)
      └── <opf:itemref>       (References manifest items in order)
```

**Key Metadata**:
- `creator`: Document creator name
- `lastsaveby`: Last editor name
- `CreatedDate`: ISO 8601 format (e.g., 2025-03-27T06:35:04Z)
- `ModifiedDate`: Last modification date
- `keyword`: Document keywords

---

### 2.2 header.xml (Styles & Formatting)
**Location**: `Contents/header.xml`
**Purpose**: Defines all styles, fonts, character properties, paragraph properties, tables

**Structure**:
```xml
<hh:head version="1.4" secCnt="1">  (secCnt = number of sections)
  ├── <hh:beginNum>               (Starting numbers for pages, footnotes, etc.)
  ├── <hh:refList>                (Definition lists)
  │   ├── <hh:fontfaces>          (All fonts used)
  │   │   └── <hh:fontface lang="HANGUL|LATIN|HANJA|JAPANESE|OTHER|SYMBOL|USER">
  │   │       └── <hh:font>       (Individual font definitions)
  │   ├── <hh:charProperties>     (Character styles - ~100-150 styles per document)
  │   │   └── <hh:charPr>
  │   │       ├── <hh:fontRef>    (Font references by language)
  │   │       ├── <hh:bold>, <hh:underline>, <hh:strikeout>
  │   │       ├── <hh:shadow>     (Drop shadow effects)
  │   │       ├── <hh:offset>     (Superscript/subscript offset)
  │   │       └── <hh:spacing>    (Character spacing)
  │   ├── <hh:paraProperties>     (Paragraph styles)
  │   │   └── <hh:paraPr>
  │   │       ├── alignment, indentation, spacing
  │   │       ├── border, shading, numbering
  │   │       └── tab stops
  │   ├── <hh:borderFills>        (Border and fill patterns ~32 per document)
  │   │   └── <hh:borderFill>
  │   │       ├── <hh:topBorder>, <hh:bottomBorder>, etc.
  │   │       └── <hh:fillBrush>  (Background fill with colors)
  │   ├── <hh:tabProperties>      (Tab stop definitions)
  │   ├── <hh:numberings>         (Bullet/numbering styles)
  │   └── <hh:styles>             (Named paragraph styles)
  └── <hh:docOption>              (Document-level options)
      └── <hh:linkinfo>
```

**Important Notes**:
- Each character property has ID and is referenced throughout document
- Fonts defined separately for different languages (Hangul, Latin, Hanja, etc.)
- ~150-200 character property definitions typical per document
- Border and fill patterns reused via ID references

---

### 2.3 section0.xml (Main Document Content)
**Location**: `Contents/section0.xml` (and section1.xml, section2.xml for multi-section docs)
**Purpose**: Actual document content - paragraphs, tables, images, formatting

**Structure**:
```xml
<hs:sec>  (Section - one per section*.xml file)
  └── <hp:p>  (Paragraph - collection of runs)
      ├── id              (Paragraph ID)
      ├── paraPrIDRef     (Reference to paragraph style in header)
      ├── styleIDRef      (Reference to named style)
      ├── pageBreak       (Whether starts new page)
      ├── columnBreak     (Whether starts new column)
      ├── merged          (Merged cell indicator)
      │
      ├── <hp:run>        (Text run with consistent formatting)
      │   ├── charPrIDRef (Character property ID from header)
      │   ├── <hp:t>      (Actual text content)
      │   ├── <hp:tbl>    (Embedded table)
      │   ├── <hp:pic>    (Embedded picture/image)
      │   ├── <hp:rect>   (Shape)
      │   └── <hp:ctrl>   (Control elements - field, column breaks)
      │
      ├── <hp:ctrl>       (Control elements)
      │   ├── <hp:fieldBegin/End>  (Hyperlinks, bookmarks, fields)
      │   ├── <hp:colPr>           (Column properties)
      │   └── <hp:secPr>           (Section properties)
      │
      └── <hp:linesegarray>  (Layout line segments)
          └── <hp:lineseg>   (Vertical position and size info)
```

**Table Structure** (within paragraph run):
```xml
<hp:tbl>  (Table element)
  ├── id, zOrder, numberingType
  ├── rowCnt, colCnt            (Row and column count)
  ├── textWrap, textFlow        (Text wrapping)
  ├── repeatHeader              (Repeat header rows)
  ├── borderFillIDRef           (Reference to border/fill from header)
  ├── <hp:sz>                   (Size: width, height)
  ├── <hp:pos>                  (Position relative to text)
  ├── <hp:tr>                   (Table row)
  │   └── <hp:tc>               (Table cell)
  │       ├── name, header, protect
  │       ├── borderFillIDRef   (Cell-specific border)
  │       ├── <hp:cellSz>       (Cell dimensions)
  │       ├── <hp:cellMargin>   (Cell padding)
  │       └── <hp:subList>      (Cell content - paragraphs)
  │           └── <hp:p>        (Cells contain paragraphs)
  └── <hp:tr> ... (More rows)
```

**Image/Picture Structure** (within run):
```xml
<hp:pic>  (Picture element)
  ├── id, zOrder
  ├── href                      (URL if external)
  ├── <hp:offset>               (X, Y position)
  ├── <hp:orgSz>                (Original size)
  ├── <hp:curSz>                (Current/displayed size)
  ├── <hp:flip>                 (Horizontal/vertical flip)
  ├── <hp:rotationInfo>         (Rotation angle and center)
  ├── <hp:renderingInfo>        (Transformation matrices)
  │   ├── <hc:transMatrix>      (Translation)
  │   ├── <hc:scaMatrix>        (Scale)
  │   └── <hc:rotMatrix>        (Rotation)
  ├── <hp:imgRect>              (Image bounds)
  ├── <hp:imgClip>              (Clipping region)
  ├── <hp:imgDim>               (Image dimensions)
  ├── <hc:img>                  (Image data reference)
  │   ├── binaryItemIDRef       (Points to file in BinData/)
  │   ├── bright, contrast      (Effects)
  │   └── effect="REAL_PIC"     (Picture type)
  └── <hp:pos>                  (Position in document)
```

---

## 3. METADATA FILES

### 3.1 version.xml
Contains version information about the document creator.

Example:
```xml
<hv:HCFVersion 
  tagetApplication="WORDPROCESSOR" 
  major="5" minor="1" micro="0" 
  buildNumber="1" os="1" 
  xmlVersion="1.4" 
  application="Hancom Office Hangul" 
  appVersion="10, 0, 0, 14515 WIN32LEWindows_8"/>
```

### 3.2 settings.xml
Document-level settings: caret position, print settings, zoom level, etc.

### 3.3 container.rdf
Hancom-specific metadata describing document structure relationships.

Example:
```xml
<rdf:Description>
  <ns0:hasPart rdf:resource="Contents/header.xml"/>
  <rdf:type rdf:resource="...#HeaderFile"/>
</rdf:Description>
```

---

## 4. KEY DESIGN PATTERNS

### 4.1 ID Reference System
- All formatting is defined once in `header.xml` with unique IDs
- Content in `section*.xml` references these IDs
- Example: `<hp:p paraPrIDRef="83" charPrIDRef="37">` references paragraph style 83 and char style 37

### 4.2 Hierarchical Content
```
Document
  └── Section (section0.xml, section1.xml, etc.)
      └── Paragraph
          └── Run (text with consistent formatting)
              ├── Text
              ├── Table
              ├── Picture
              └── Controls
```

### 4.3 Unit System
- HWPUNIT: Hancom's internal unit (1/7200 inch typical)
- All dimensions use integer HWPUNIT values
- Conversion: pixels/points are stored as scaled integers

### 4.4 Namespace Usage
```
hp: http://www.hancom.co.kr/hwpml/2011/paragraph
hs: http://www.hancom.co.kr/hwpml/2011/section
hh: http://www.hancom.co.kr/hwpml/2011/head
hc: http://www.hancom.co.kr/hwpml/2011/core
ha: http://www.hancom.co.kr/hwpml/2011/app
opf: http://www.idpf.org/2007/opf/
```

---

## 5. DOCUMENT STATISTICS FROM SAMPLES

| Aspect | Doc 1 (Press Release 1) | Doc 2 (Press Release 2) | Doc 3 (Multi-section) |
|--------|----------------------|----------------------|----------------------|
| File Size | 237 KB | 482 KB | 1.3 MB |
| Sections | 1 | 1 | 3 |
| Paragraphs | 118 | 195 | ~250 (across 3 sections) |
| Tables | 7 | 9 | 6 |
| Images | 3 JPG | 6 (3 JPG + 3 PNG) | 2 (1 JPG, 1 PNG) |
| Character Styles | 159 | 106 | 143 |
| Paragraph Styles | Multiple | Multiple | Multiple |
| Border/Fill Patterns | 32 | 32+ | 32+ |
| Font Groups | 7 (Hangul, Latin, Hanja, Japanese, Other, Symbol, User) | Same | Same |

---

## 6. COMMON ELEMENT ATTRIBUTES

### Paragraph (<hp:p>)
- `id`: Unique identifier
- `paraPrIDRef`: Reference to paragraph properties in header
- `styleIDRef`: Reference to named style
- `pageBreak`: "0" (no break) or "NEXTPAGE" (page break)
- `columnBreak`: Column break indicator
- `merged`: Used in tables

### Run (<hp:run>)
- `charPrIDRef`: Reference to character properties in header

### Table (<hp:tbl>)
- `rowCnt`, `colCnt`: Dimensions
- `borderFillIDRef`: Border/fill style reference
- `repeatHeader`: Repeat header rows on each page
- `pageBreak`: "CELL" (default) - how to break across pages

### Table Cell (<hp:tc>)
- `header`: "1" if header cell, "0" if data
- `protect`: Whether cell is locked
- `editable`: Whether cell can be edited
- `borderFillIDRef`: Cell-specific border/fill override

### Picture (<hp:pic>)
- `zOrder`: Z-index for layering
- `href`: URL if external image (usually empty for embedded)
- Various size/position attributes

---

## 7. IMPORTANT OBSERVATIONS FOR PROGRAMMATIC CREATION

1. **XML Format**: All XML must be well-formed and UTF-8 encoded
2. **ID References**: Must match - if you reference charPrIDRef="37", that ID must exist in header.xml
3. **Units**: All dimensions in HWPUNIT (integer values)
4. **Section Order**: Referenced in content.hpf spine element
5. **Binary Images**: Images must be ZIP-compressed with correct references
6. **ZIP Ordering**: mimetype must be first, uncompressed in ZIP
7. **Namespace Prefixes**: Must match expected prefixes (hp:, hs:, hh:, hc:, etc.)
8. **Metadata**: Creator, dates, and other metadata in content.hpf
9. **Character Encoding**: Must support Korean characters (UTF-8)
10. **Single Line XML**: While not required, Hancom creates single-line XML files

---

## 8. SAMPLE ELEMENT REFERENCES

### Referencing a character property:
1. Define in header.xml: `<hh:charPr id="37" height="1000">...</hh:charPr>`
2. Reference in section*.xml: `<hp:run charPrIDRef="37"><hp:t>Text</hp:t></hp:run>`

### Creating a table:
1. Define border style in header.xml: `<hh:borderFill id="6">...</hh:borderFill>`
2. Create table in section*.xml:
   ```xml
   <hp:tbl borderFillIDRef="6" rowCnt="2" colCnt="3">
     <hp:tr>
       <hp:tc borderFillIDRef="7"><hp:subList><hp:p>...</hp:p></hp:subList></hp:tc>
     </hp:tr>
   </hp:tbl>
   ```

### Embedding an image:
1. Add to content.hpf manifest: `<opf:item id="image1" href="BinData/image1.jpg" media-type="image/jpg" isEmbeded="1"/>`
2. Reference in section*.xml:
   ```xml
   <hp:pic>
     <hc:img binaryItemIDRef="image1" effect="REAL_PIC"/>
   </hp:pic>
   ```

---

## CONCLUSION

The HWPX format is a well-structured, XML-based container format that allows programmatic document creation. Understanding the hierarchy and ID reference system is critical for generating valid HWPX files. The format supports complex documents with multiple sections, advanced styling, tables, and embedded images while maintaining human-readable XML structure (when properly formatted).

