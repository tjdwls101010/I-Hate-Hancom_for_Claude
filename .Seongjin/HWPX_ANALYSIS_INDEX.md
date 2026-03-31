# HWPX Format Analysis - Complete Index

## Overview

This directory contains comprehensive documentation of the HWPX file format internal structure, extracted from analyzing 3 real-world Korean government press release documents.

## Generated Documentation Files

### 1. **HWPX_INTERNAL_STRUCTURE_ANALYSIS.md** (14 KB)
**Comprehensive Technical Reference**

Complete deep-dive into the HWPX format covering:
- Archive structure with file organization diagram
- Detailed explanation of all core XML files (content.hpf, header.xml, section0.xml)
- Document metadata and version information
- Key design patterns and architecture
- Statistical data from sample documents
- Common element attributes and their purposes
- Important observations for programmatic creation
- Sample element references with code examples

**Best for:** Understanding the complete HWPX architecture, detailed reference during implementation

---

### 2. **HWPX_QUICK_REFERENCE.md** (7.7 KB)
**Developer Quick Reference Guide**

Practical quick-reference covering:
- Visual file organization diagram
- Content flow and relationship diagram
- Step-by-step creation process
- Critical rules table
- Key attributes cheatsheet
- Common dimension values
- Document metadata examples
- Font configuration patterns
- Minimal valid document structure
- Testing checklist

**Best for:** Quick lookups during implementation, checklist validation, troubleshooting

---

## Analysis Methodology

### Documents Analyzed

1. **Document 1** (237 KB)
   - File: `유럽 탄소국경조정제도 대응… 기후부 1대1 상담 방식 등으로 밀착 지원(보도자료)(기후경제 3.29).hwpx`
   - Type: Single-section press release
   - Content: 118 paragraphs, 7 tables, 3 images
   - Character styles: 159
   - Size: 237 KB

2. **Document 2** (482 KB)
   - File: `[3.30.월.조간] 국립보건연구원, 국내 인공혈액 세포 치료제 개발을 앞당기다.hwpx`
   - Type: Single-section press release
   - Content: 195 paragraphs, 9 tables, 6 images
   - Character styles: 106
   - Size: 482 KB

3. **Document 3** (1.3 MB)
   - File: `260330_상담_7천건_돌파__스타트업_원스톱_지원센터_온라인_개소.hwpx`
   - Type: Multi-section document (3 sections)
   - Content: ~250 paragraphs total, 6 tables, 2 images
   - Character styles: 143
   - Size: 1.3 MB

### Analysis Techniques Used

1. **ZIP Archive Extraction** - Examined directory structure and file organization
2. **XML Parsing & Analysis** - Mapped element hierarchy and attributes
3. **Schema Extraction** - Identified all element types and their properties
4. **Content Analysis** - Analyzed paragraph, table, and image structures
5. **Metadata Extraction** - Examined document metadata and settings
6. **Comparative Analysis** - Found common patterns across documents

### Tools Used

- Python XML parsing (xml.etree.ElementTree)
- ZIP archive extraction (unzip)
- Direct file examination (bash, grep, head/tail)

---

## Key Findings

### Architecture Summary

HWPX is a ZIP-based container using XML to store:
- **Styles** (header.xml) - 150-200 character properties per document
- **Content** (section*.xml) - Hierarchical paragraphs, runs, tables, images
- **Metadata** (content.hpf) - Document properties and resource manifest
- **Resources** (BinData/) - Embedded images and binary files

### Critical Design Principles

1. **ID Reference System** - All formatting defined once, referenced by ID
2. **Modular Sections** - Multi-section documents supported via section0.xml, section1.xml, etc.
3. **ODP/ODF Compliance** - Uses OpenDocument Format structure with Hancom extensions
4. **Character Set Support** - Separate font definitions for Hangul, Latin, Hanja, Japanese, Other
5. **HWPUNIT System** - Internal unit system (1/7200 inch) for all dimensions

### Document Statistics

```
Document Type          Files    Size    Paragraphs  Tables  Images
Single-section PR      1        237 KB  118         7       3 JPG
Single-section PR      1        482 KB  195         9       6 mixed
Multi-section Doc      3        1.3 MB  ~250        6       2 mixed
```

---

## Implementation Guide

### For Reading HWPX Files:
1. Extract ZIP archive
2. Parse content.hpf to understand structure
3. Load header.xml to map all style IDs
4. Parse section*.xml referencing the style map
5. Load BinData/ images as needed

### For Creating HWPX Files:
1. Define all styles in header.xml with consistent IDs
2. Create document content in section0.xml (and section1.xml, etc. if multi-section)
3. All references MUST match defined IDs
4. Add images to BinData/ and reference in section*.xml
5. Create content.hpf manifest and metadata
6. Create supporting files (version.xml, settings.xml, META-INF files)
7. Package as ZIP with mimetype first (uncompressed)

### Common Gotchas:
- Character property ID mismatch (reference non-existent style)
- Missing image files (reference in XML but not in BinData/)
- Incorrect namespace prefixes (hp: vs hs: vs hh:)
- Non-UTF-8 encoding
- Missing section*.xml files referenced in spine
- Incorrect ZIP structure (mimetype not first)

---

## Technical Specifications

### Required Namespaces

```
hp:  http://www.hancom.co.kr/hwpml/2011/paragraph
hs:  http://www.hancom.co.kr/hwpml/2011/section
hh:  http://www.hancom.co.kr/hwpml/2011/head
hc:  http://www.hancom.co.kr/hwpml/2011/core
ha:  http://www.hancom.co.kr/hwpml/2011/app
hm:  http://www.hancom.co.kr/hwpml/2011/master-page
opf: http://www.idpf.org/2007/opf/
```

### Supported Image Formats
- JPG (most common)
- PNG
- Embedded in BinData/ folder

### Standard Page Dimensions (HWPUNIT)
- Width: 59528 (A4)
- Height: 84188 (A4)
- Margins: 5669 left/right, 4251 top/bottom

### Font Groups
- **HANGUL** (23 fonts typically) - Korean text
- **LATIN** (24 fonts typically) - English/European
- **HANJA** (19 fonts) - Chinese characters
- **JAPANESE** (19 fonts) - Japanese characters
- **OTHER** (16 fonts) - Other writing systems
- **SYMBOL** (19 fonts) - Symbols
- **USER** (16 fonts) - Custom fonts

### Typical Style Counts
- Character properties: 100-160 per document
- Paragraph properties: 20-50 per document
- Border/fill patterns: 30-35 per document
- Named styles: 10-20 per document

---

## File Format Checklist

### Before Final Delivery:
- [ ] All XML well-formed and valid
- [ ] UTF-8 encoding throughout
- [ ] All ID references match definitions
- [ ] Section count matches section0.xml, section1.xml, etc.
- [ ] All images in BinData/ are referenced
- [ ] All references in manifest are real files
- [ ] Correct namespace prefixes used
- [ ] ZIP structure correct (mimetype first, uncompressed)
- [ ] All required metadata present
- [ ] Version and settings files present

---

## Useful Commands for Inspection

```bash
# Extract HWPX
unzip -q document.hwpx -d extracted/

# List contents
ls -la extracted/

# View XML structure
head -c 1000 extracted/Contents/header.xml

# Count elements
grep -o '<hp:p\|<hp:tbl\|<hp:pic' extracted/Contents/section0.xml | wc -l

# Check for specific IDs
grep 'charPrIDRef="37"' extracted/Contents/section0.xml
```

---

## References

- **Format Specification**: HWPML 2011, 2016 versions
- **Base Standard**: OpenDocument Format (ODF)
- **Application**: Hancom Office Hangul (한글)
- **Tested Version**: 1.4 (from samples)

---

## Document Version

- **Created**: 2026-03-29
- **Analysis Date**: 2026-03-29
- **Sample Documents**: 3 Korean government press releases
- **Total Analysis Time**: Comprehensive deep-dive
- **Completeness**: Covers core structure, attributes, patterns, and examples

---

## Next Steps

To use this documentation for programmatic HWPX creation:

1. Start with HWPX_QUICK_REFERENCE.md for overview and checklist
2. Reference HWPX_INTERNAL_STRUCTURE_ANALYSIS.md for specific element details
3. Use the sample code patterns provided for table, image, and text handling
4. Follow the critical rules section for validation
5. Use the testing checklist before delivery

---

**Note**: This analysis is based on real-world Korean government documents. The format is stable and supports complex documents with tables, images, multiple sections, and advanced styling. Standard Korean character encoding is well-supported throughout.

