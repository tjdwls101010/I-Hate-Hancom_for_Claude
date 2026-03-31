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

### 2.5단계: 암묵지 적용 (프로 수준 품질의 핵심)

`references/document-design.md`의 암묵지 섹션을 반드시 읽고, 다음 원칙을 section0.xml 생성에 적용한다:

1. **본문 들여쓰기**: 모든 본문 단락의 `<hp:t>` 텍스트 앞에 전각 공백 2개("  ")를 삽입한다. 표 셀, 제목, 주석에는 넣지 않는다.
2. **소형 빈 줄**: 단락 사이 빈 줄은 본문 크기(14pt)가 아니라 반으로 줄인 크기(3-8pt)의 charPr을 사용한다. 이것이 "프로가 만든 문서" 느낌의 핵심.
3. **Bold는 기자용 마커**: 본문에서 핵심 정책/성과 구절만 bold charPr run으로 분리한다. 동사 어미(-했다, -한다)는 bold에서 반드시 제외한다.
4. **괄호 부가정보 축소**: "(장관 김성환)" 같은 괄호 안 직함은 본문보다 2pt 작은 charPr run으로 분리한다.
5. **서체 위계**: 명조(바탕)=본문, 고딕(돋움/맑은고딕)=표/주석/메타데이터. 이 위계를 깨지 않는다.

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

## 함정 방지 (반드시 읽을 것)

Hancom 뷰어는 XML 구조에 매우 민감하다. 아래 사항을 어기면 크래시, 빈 페이지, 또는 시각적 결함이 발생한다. 이 내용은 실제 테스트에서 확인된 것이다.

### header.xml은 직접 생성하지 말 것
Hancom 뷰어는 header.xml의 내부 구조에 문서화되지 않은 요구사항이 있다. XML로서 유효하더라도 뷰어가 크래시할 수 있다. 반드시 `templates/base/Contents/header.xml`(실제 정부 문서에서 추출)을 사용한다.

### secPr은 템플릿을 사용할 것
section0.xml의 첫 번째 문단 첫 번째 run에 secPr(페이지 설정)이 필요하다. secPr이 불완전하면 빈 페이지가 된다. `build_hwpx.py`는 secPr이 없으면 `templates/base/secpr_template.xml`을 자동 삽입한다. secPr을 직접 작성할 필요가 없다.

### 표는 `<hp:run>` 안에 직접 넣을 것
```xml
<!-- 올바름 -->
<hp:run charPrIDRef="0"><hp:tbl ...>...</hp:tbl></hp:run>

<!-- 잘못됨 — 크래시 발생 -->
<hp:run charPrIDRef="0"><hp:ctrl><hp:tbl ...>...</hp:tbl></hp:ctrl></hp:run>
```
`<hp:ctrl>`은 컬럼 설정(colPr) 등에만 사용되며, 표를 감싸면 안 된다.

### `<hp:tc>` 태그에 필수 속성을 모두 포함할 것
```xml
<!-- 올바른 형식 (실제 문서에서 추출) -->
<hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="4">

<!-- 잘못된 형식 — 속성 누락 -->
<hp:tc borderFillIDRef="4" width="10000" header="0">
```
`width`는 tc 속성이 아니라 `<hp:cellSz>`에서 지정한다.

### paraPr 2~8은 일반 본문에 사용 금지
이 ID들은 `heading type="OUTLINE"`이 연결되어 있어 자동 번호 매기기(1., 가., 3) 등)가 활성화된다. 들여쓰기가 필요하면 paraPr 0(기본), 1(left=1500), 14(left=1100), 15(left=2200)를 사용한다. 상세한 안전/위험 ID 목록은 `references/style-catalog.md` 참조.

### 표 헤더에는 배경색 borderFill을 사용할 것
실제 정부 문서의 표 헤더는 거의 예외 없이 배경색이 있다. borderFill 22(#F2F2F2 연회색), 23(#DFE6F7 연파랑), 24(#E5E5E5 중회색+이중선) 중 선택. 배경 없는 표 헤더(borderFill 4)는 데이터 행과 구분이 안 되어 아마추어 인상을 준다.

### ※ 주의사항은 1x1 표 박스로 감쌀 것
마크다운의 blockquote(`>`)나 `※` 참고사항은 1행 1열 표(borderFill 25 또는 26)로 감싸면 시각적으로 돋보인다.

### 어두운 배경의 표 셀에는 흰색 글자를 사용할 것
borderFill 14(#000066 진한 파랑) 같은 어두운 배경에 검정 글자를 넣으면 보이지 않는다. 흰색 textColor를 가진 charPr(id=8, 26, 55)을 사용한다.

## 스크립트 경로 참조

모든 스크립트는 이 스킬 디렉토리 내 `scripts/`에 위치한다:
- `scripts/build_hwpx.py` — XML → HWPX ZIP 조립
- `scripts/validate_hwpx.py` — 구조 정합성 검증
- `scripts/read_hwpx.py` — HWPX → 구조화된 텍스트 추출
- `scripts/table_fixer.py` — 테이블 구조 자동 수정

기반 템플릿은 `templates/base/`에 위치한다.
