# Markdown Normalization Guide

## Why Normalize

Markdown is optimized for **fast authoring** — bullet points are the default tool. Hancom government documents are optimized for **structured reading** — tables are the default tool. Normalization bridges this gap by restructuring content where the nature of the information calls for it.

Not all markdown needs normalization. Prose, editorials, and narrative text are already in their ideal form. Normalization targets **structured data trapped in bullet format**.

## The Core Decision: Table or Bullets?

### Convert to table when the data has repeating structure

**Principle**: If the same set of fields appears multiple times across separate items, a table compresses the information and makes comparison effortless.

**Example 1 — Repeating item fields (10 topics × 4 attributes)**

Before (60+ lines):
```markdown
#### 토픽 0: 데이터 저장 및 관리
- **문서 수**: 3,636개 (81.4%)
- **설명 분산**: 0.0040
- **대표 키워드**: based, intelligence, artificial...
- **주요 K-means 군집**: Cluster 2

#### 토픽 1: 스마트 팩토리 자동화
- **문서 수**: 661개 (14.8%)
- **설명 분산**: 0.0206
...
(×10 topics)
```

After (12 lines):
```markdown
| 토픽 | 토픽명 | 문서 수 | 설명 분산 | 주요 군집 | 대표 키워드 |
|:---:|--------|--------:|:--------:|:--------:|------------|
| 0 | 데이터 저장 및 관리 | 3,636개 (81.4%) | 0.0040 | Cluster 2 | based, intelligence, artificial |
| 1 | 스마트 팩토리 자동화 | 661개 (14.8%) | 0.0206 | Cluster 3 | automation, water, production |
...
```

**Example 2 — Comparison data (4 entities × 3 ranked items)**

Before:
```markdown
**US**:
  - 토픽 0 (데이터 저장 및 관리): 93.1%
  - 토픽 9 (자율주행 시스템): 2.2%
  - 토픽 4 (토픽 4): 1.9%

**CN**:
  - 토픽 0 (데이터 저장 및 관리): 78.3%
  ...
```

After:
```markdown
| 국가 | 1순위 토픽 | 2순위 토픽 | 3순위 토픽 |
|:---:|-----------|-----------|-----------|
| US | 데이터 저장 (93.1%) | 자율주행 (2.2%) | 토픽 4 (1.9%) |
| CN | 데이터 저장 (78.3%) | 스마트 팩토리 (18.9%) | 토픽 4 (1.6%) |
...
```

### Keep as bullets when the content is not tabular

**Principle**: If the information is narrative, explanatory, sequential, or has only 2-3 key-value pairs, bullets are more natural than a table.

**Example 1 — Few key-value pairs (keep as bullets)**
```markdown
## 1. 개요
- **분석 일시**: 2025-11-13
- **데이터**: 4,469개 특허 문서
- **최종 토픽 수**: 10개
```
Only 3-4 items. A 2-column table with "항목 | 내용" headers adds overhead without improving readability. These map naturally to □ items in Hancom.

**Example 2 — Narrative explanation (keep as bullets)**
```markdown
- **선택 근거**:
  1. K-means 4개 군집의 2~3배 고려
  2. Cluster 2 (43%)의 과도한 크기 세분화 필요
  3. 비즈니스 해석 가능성
```
This is sequential reasoning. A table would flatten the logical flow.

**Example 3 — Editorial/argumentative text (keep as-is)**
```markdown
- 경향신문은 **"시한부 훈풍"** 이라고 평가했다.
- 이상민 연구위원은 "화석 연료 의존도를 줄이는 에너지 효율화 사업이 추경에 반영돼야 한다"고 지적했다.
```
Quotes, analysis, opinions — inherently non-tabular.

## What to Remove

- **Obsidian image embeds**: `![[image.jpg]]` → delete the entire line. Hancom cannot render Obsidian-specific syntax.
- **Inline URLs**: `[link text](https://very-long-url...)` → keep only `link text`. URLs clutter printed documents and are not clickable in Hancom.
- **Decorative emoji in headings**: `## 🔥프로젝트 메이븐` → `## 프로젝트 메이븐`. Formal documents don't use emoji.

## What to Condense

When every item in a list says essentially the same thing, condense into a meaningful insight.

Before (repetitive, no information gain):
```markdown
- **US**: 데이터 저장 및 관리 중심 (93.1%)
- **CN**: 데이터 저장 및 관리 중심 (78.3%)
- **JP**: 데이터 저장 및 관리 중심 (86.7%)
- **KR**: 데이터 저장 및 관리 중심 (91.2%)
```

After (highlights actual differences):
```markdown
- 전체 국가에서 **데이터 저장 및 관리**가 압도적 1순위 (78~93%)
- **CN**은 스마트 팩토리 자동화 비중(18.9%)이 타국 대비 현저히 높음
- **KR**은 유일하게 멀티 에이전트 협업이 2순위 (7.0%)
```

## Document Types and Expected Effort

| Document Type | Normalization | Typical Actions |
|--------------|:---:|----------------|
| Technical report / analysis | **HIGH** | Bullet→table conversions, image removal, condensing |
| News digest | **LOW** | Remove Obsidian syntax and URLs only |
| Column / editorial | **MINIMAL** | Remove emoji at most |
| Long-form article | **MINIMAL** | Heading structure already clean |

Assess the document type first. If it's prose-heavy with few structured data sections, skip normalization entirely.

## Heading Conventions

```
#   = Document title (one per document, maps to main title)
##  = Section headings (maps to □ section-level or section header with page break)
### = Subsection headings (maps to ○ sub-topic level)
```

Note: `#` is always the top-level document title. `##` is where sections begin. Do not use `#` for numbered sections — that is a `##` role.

## Workflow

1. **Read** the entire markdown
2. **Assess** the document type and normalization level needed
3. **Copy** to a `_normalized.md` file (preserve original)
4. **Edit()** to apply transformations — only touch sections that need change
5. Proceed to annotation and HWPX conversion with the normalized file
