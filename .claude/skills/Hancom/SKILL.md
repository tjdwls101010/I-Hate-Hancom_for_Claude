---
name: Hancom
description: HWPX 한컴문서를 읽고 작성하는 스킬. 한컴문서(HWPX) 파일을 분석하거나, 사용자가 제공한 내용을 바탕으로 한국 정부 공문서 수준의 문서를 생성한다. "한컴", "한글문서", "hwpx", "hwp", "보도자료 작성", "공문서 작성", "한컴으로 만들어줘", "hwpx로 저장", "이 hwpx 파일 읽어줘" 등의 요청이나 .hwpx 파일이 언급될 때 이 스킬을 사용한다. 한컴문서 관련 작업이라면 명시적으로 스킬을 요청하지 않아도 적극적으로 사용할 것.
---

# HWPX 한컴문서 스킬

HWPX는 한국의 표준 문서 포맷으로, 내부적으로 ZIP 안에 XML 파일들로 구성된다. 이 스킬은 Claude가 HWPX 포맷을 이해하고, 읽고, 생성할 수 있도록 지식과 도구를 제공한다.

## 핵심 개념

HWPX 문서의 핵심 구조는 **ID 참조 시스템**이다:
- `header.xml`: 모든 스타일(글꼴, 크기, 색상, 정렬, 테두리 등)을 ID로 정의
- `section0.xml`: 실제 문서 내용. 각 문단과 텍스트 런에서 header의 스타일 ID를 참조

이는 CSS와 HTML의 관계와 유사하다. header.xml이 스타일시트이고, section0.xml이 마크업이다.

## 레퍼런스 문서 안내

이 스킬에는 세 개의 상세 참조 문서가 있다. 작업 유형에 따라 필요한 문서를 읽는다:

| 상황 | 읽어야 할 문서 |
|------|---------------|
| HWPX 포맷 구조를 이해해야 할 때 | `references/hwpx-format.md` |
| 문서의 시각적 디자인을 결정해야 할 때 | `references/document-design.md` |
| 어떤 스타일 ID를 사용할지 정해야 할 때 | `references/style-catalog.md` |

## 쓰기 워크플로우

사용자가 한컴문서 생성을 요청하면 다음 흐름을 따른다.

### 1단계: 요구사항 파악

사용자의 요청에서 다음을 파악한다:
- **문서 유형**: 보도자료, 업무보고서, 공문, 회의록 등
- **핵심 내용**: 제목, 본문 텍스트, 표 데이터 등
- **특별 요구**: 특정 서식, 이미지 포함 여부 등

### 2단계: 문서 구조 설계

`references/document-design.md`를 참조하여 문서의 전체 구조를 설계한다.
한국 공문서의 표준 구성을 따르되, 문서 유형에 맞게 조정한다.

### 3단계: section0.xml 생성

`references/style-catalog.md`를 참조하여 적절한 스타일 ID를 선정하고,
`references/hwpx-format.md`의 XML 구조 예시를 참조하여 section0.xml을 작성한다.

section0.xml의 기본 골격:
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<hs:sec xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section"
  xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph"
  xmlns:hp10="http://www.hancom.co.kr/hwpml/2016/paragraph"
  xmlns:hc="http://www.hancom.co.kr/hwpml/2011/core"
  xmlns:hh="http://www.hancom.co.kr/hwpml/2011/head"
  xmlns:hwpunitchar="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar">

  <!-- 첫 번째 문단: secPr(페이지 설정)을 포함 -->
  <hp:p id="0" paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
    <hp:run charPrIDRef="1">
      <hp:secPr textDirection="HORIZONTAL" spaceColumns="1134" tabStop="8000" outlineShapeIDRef="1" memoShapeIDRef="0" textVerticalWidthHead="0" masterPageCnt="0">
        <hp:pagePr landscape="WIDELY" width="59528" height="84188" gutterType="LEFT_ONLY">
          <hp:margin header="2834" footer="2834" gutter="0" left="5669" right="5669" top="4251" bottom="4251"/>
        </hp:pagePr>
        <hp:footNotePr>
          <hp:autoNumFormat type="DIGIT" suffixChar=")" supscript="0"/>
          <hp:noteLine length="-1" type="SOLID" width="0.12 mm" color="#000000"/>
          <hp:noteSpacing betweenNotes="283" belowLine="567" aboveLine="850"/>
          <hp:numbering type="CONTINUOUS" newNum="1"/>
          <hp:placement place="EACH_COLUMN" beneathText="0"/>
        </hp:footNotePr>
        <hp:endNotePr>
          <hp:autoNumFormat type="DIGIT" suffixChar=")" supscript="0"/>
          <hp:noteLine length="14692" type="SOLID" width="0.12 mm" color="#000000"/>
          <hp:noteSpacing betweenNotes="0" belowLine="567" aboveLine="850"/>
          <hp:numbering type="CONTINUOUS" newNum="1"/>
          <hp:placement place="END_OF_DOCUMENT" beneathText="0"/>
        </hp:endNotePr>
      </hp:secPr>
    </hp:run>
    <hp:run charPrIDRef="1">
      <hp:t>본문 첫 줄 텍스트</hp:t>
    </hp:run>
  </hp:p>

  <!-- 이후 문단들 -->
  <hp:p id="0" paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
    <hp:run charPrIDRef="1">
      <hp:t>다음 문단 텍스트</hp:t>
    </hp:run>
  </hp:p>

</hs:sec>
```

### 4단계: 검증

생성한 section0.xml의 구조적 정합성을 확인한다:
```bash
python3 scripts/validate_hwpx.py --section section0.xml --header templates/base/Contents/header.xml
```

### 5단계: HWPX 조립

section0.xml과 기반 템플릿을 결합하여 HWPX 파일을 생성한다:
```bash
python3 scripts/build_hwpx.py --section section0.xml --output output.hwpx --title "문서 제목"
```

이미지를 포함할 경우:
```bash
python3 scripts/build_hwpx.py --section section0.xml --output output.hwpx --images logo.png chart.jpg
```

### 6단계: 테이블 수정 (필요시)

표 구조에 문제가 있으면 자동 수정한다:
```bash
python3 scripts/table_fixer.py output.hwpx --output fixed.hwpx
```

## 읽기 워크플로우

사용자가 HWPX 파일 분석을 요청하면:

### 1단계: 내용 추출
```bash
python3 scripts/read_hwpx.py input.hwpx
```

### 2단계: 상세 분석 (필요시)
```bash
python3 scripts/read_hwpx.py input.hwpx --verbose
```
`--verbose` 옵션은 각 문단의 스타일 정보(글꼴, 크기, 정렬 등)도 함께 표시한다.

### 3단계: 사용자에게 결과 제공

추출된 내용을 요약하거나, 사용자가 요청한 특정 정보를 제공한다.
필요하면 문서의 구조적 특성(표 개수, 이미지, 스타일 패턴 등)도 분석한다.

## 기술적 제약 사항

HWPX 포맷에는 원칙이 아닌 **기술적 필수 요건**이 있다. 이를 어기면 Hancom Office에서 파일이 열리지 않는다:

1. **mimetype은 ZIP의 첫 번째 엔트리이고 비압축(STORED)이어야 한다** — ODF 기반 포맷의 표준 요구사항
2. **ID 참조 정합성** — section XML의 모든 charPrIDRef, paraPrIDRef, borderFillIDRef가 header.xml에 존재해야 한다
3. **테이블 rowCnt/colCnt** — 실제 행/열 수와 일치해야 한다
4. **테이블 cellAddr** — 각 행의 셀 주소가 colSpan을 고려해 순차적이어야 한다
5. **XML 인코딩** — UTF-8만 사용
6. **네임스페이스 접두사** — 파일 전체에서 일관되어야 한다

## 스크립트 경로 참조

모든 스크립트는 이 스킬 디렉토리 내 `scripts/`에 위치한다:
- `scripts/build_hwpx.py` — XML → HWPX ZIP 조립
- `scripts/validate_hwpx.py` — 구조 정합성 검증
- `scripts/read_hwpx.py` — HWPX → 구조화된 텍스트 추출
- `scripts/table_fixer.py` — 테이블 구조 자동 수정

기반 템플릿은 `templates/base/`에 위치한다.
