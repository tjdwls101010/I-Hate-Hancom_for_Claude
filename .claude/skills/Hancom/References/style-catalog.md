# Doc4 (국립보건연구원 보도자료) 스타일 카탈로그

> 이 문서는 **doc4 (국립보건연구원 보도자료)** 의 실제 `header.xml`에서 추출한 스타일 ID를 정리한 것이다.
> section0.xml을 생성할 때 `charPrIDRef`, `paraPrIDRef`, `borderFillIDRef` 값을 이 카탈로그에서 참조한다.
>
> **원칙**: 이 카탈로그에 없는 ID를 사용하지 않는다. header.xml에 정의되지 않은 ID를 참조하면 문서가 깨진다.

---

## 1. 한글 서체 목록 (hangulFont)

| fontID | 서체명 | 계열 |
|--------|--------|------|
| 0 | 돋움체 | 고딕 (sans-serif) |
| 1 | 맑은 고딕 | 고딕 (sans-serif) |
| 2 | 바탕 | 명조 (serif) |
| 3 | 바탕체 | 명조 (serif, mono) |
| 4 | 함초롬돋움 | 고딕 (sans-serif) |
| 5 | 함초롬바탕 | 명조 (serif) |
| 6 | HY울릉도M | 디자인 |
| 7 | HY헤드라인M | 제목 전용 (headline) |
| 8 | 휴먼명조 | 명조 (serif) |

> charPr의 `<hh:fontRef hangul="N">` 에서 위 fontID를 참조한다.

---

## 2. 글자 스타일 (charPr) — 용도별 분류

section XML에서 `<hp:run charPrIDRef="N">`으로 참조한다.

### 2-1. 제목 계열

| ID | 크기 | 서체 (fontID) | 굵기 | 색상 | 용도 |
|----|------|---------------|------|------|------|
| **128** | 26pt | 함초롬돋움 (4) | **BOLD** | black | **문서 메인 제목** (가장 큰 텍스트) |
| 29 | 15pt | HY헤드라인M (7) | **BOLD** | black | **□ 소제목 (헤딩)** — 본문 구분용 |
| 4 | 16pt | 함초롬돋움 (4) | 일반 | #2E74B5 | **파란색 부제목** |
| 51 | 12pt | 맑은 고딕 (1) | **BOLD** | black | 중간 강조 제목 |

### 2-2. 본문 계열

| ID | 크기 | 서체 (fontID) | 굵기 | 색상 | 용도 |
|----|------|---------------|------|------|------|
| **9** | 14pt | 함초롬바탕 (5) | 일반 | black | **기본 본문** (가장 많이 사용) |
| 13–19 | 14pt | 바탕 (2) | 일반 | black | 본문 변형 (거의 동일, 호환 가능) |
| 10 | 12pt | 돋움체 (0) | **BOLD** | black | **본문 내 강조** 단어/구절 |

### 2-3. 표 계열

| ID | 크기 | 서체 (fontID) | 굵기 | 색상 | 용도 |
|----|------|---------------|------|------|------|
| **0** | 10pt | 함초롬돋움 (4) | 일반 | black | **표 본문 셀** (기본 작은 텍스트) |
| **136** | 10pt | 돋움체 (0) | **BOLD** | black | **표 헤더 셀** 텍스트 |

### 2-4. 주석/캡션 계열

| ID | 크기 | 서체 (fontID) | 굵기 | 색상 | 용도 |
|----|------|---------------|------|------|------|
| 1 | 9pt | 함초롬돋움 (4) | 일반 | black | 각주, 작은 주석 |
| 23 | 13pt | 휴먼명조 (8) | 일반 | black | 캡션 |
| 42 | 13pt | 맑은 고딕 (1) | 일반 | black | 라벨 |
| 132–133 | 13pt | 휴먼명조 (8) | 일반 | black | 중간 텍스트 (캡션 변형) |

### 2-5. 색상 계열 (어두운 배경 전용)

| ID | 크기 | 서체 (fontID) | 굵기 | 색상 | 용도 |
|----|------|---------------|------|------|------|
| **8** | 10pt | 돋움체 (0) | 일반 | **#FFFFFF** | 흰색 텍스트 — 어두운 배경 표 셀 |
| **26** | 17pt | HY헤드라인M (7) | 일반 | **#FFFFFF** | 흰색 큰 제목 — 어두운 배경 |
| **55** | 16pt | HY헤드라인M (7) | 일반 | **#FFFFFF** | 흰색 중제목 — 어두운 배경 |

> **주의**: 흰색 charPr(8, 26, 55)은 반드시 어두운 배경의 borderFill(예: id=14)과 함께 사용해야 한다.
> 밝은 배경에 흰색 텍스트를 넣으면 보이지 않는다.

---

## 3. 문단 스타일 (paraPr) — 안전도별 분류

section XML에서 `<hp:p paraPrIDRef="N">`으로 참조한다.

### !! 중요: heading 속성의 함정 !!

paraPr에는 `heading` 속성이 있다. 이 값에 따라 문단의 동작이 완전히 달라진다:

| heading 값 | 동작 | 위험도 |
|------------|------|--------|
| **NONE** | 일반 텍스트 문단 | 안전 — 자유롭게 사용 |
| **OUTLINE** | **자동 번호 매기기** (1., 가., 나. 등) | **위험** — 일반 텍스트에 사용하면 원치 않는 번호 삽입 |
| **BULLET** | **자동 불릿 삽입** | 주의 — 불릿 기호가 자동 삽입됨 |

### 3-1. 안전한 일반 문단 (heading=NONE)

| ID | 정렬 | 줄간격 | 들여쓰기 | 용도 |
|----|------|--------|----------|------|
| **0** | JUSTIFY | 160% | 없음 | **기본 본문** — 가장 안전, 가장 범용 |
| 1 | JUSTIFY | 160% | left=1500 | ㅇ 레벨 들여쓰기 |
| 9 | JUSTIFY | 150% | 없음 | 약간 빽빽한 본문 |
| 14 | LEFT | 160% | left=1100 | - 레벨 들여쓰기 |
| 15 | LEFT | 160% | left=2200 | * 레벨 들여쓰기 (이중) |
| 28 | JUSTIFY | 155% | 없음 | 중간 간격 본문 |
| 35 | JUSTIFY | 170% | 없음 | 넓은 간격 본문 |

### 3-2. 정렬 특수 문단 (heading=NONE)

| ID | 정렬 | 줄간격 | 들여쓰기 | 용도 |
|----|------|--------|----------|------|
| **19** | CENTER | 160% | 없음 | **제목 (가운데 정렬)** |
| 29 | RIGHT | 160% | 없음 | 날짜, 오른쪽 정렬 텍스트 |
| 30 | LEFT | 160% | 없음 | 왼쪽 정렬 텍스트 |
| 43 | CENTER | 180% | 없음 | 넓은 가운데 정렬 |
| 50 | CENTER | 150% | 없음 | 중간 가운데 |

### 3-3. 표 셀 전용 문단 (heading=NONE)

| ID | 정렬 | 줄간격 | 들여쓰기 | 용도 |
|----|------|--------|----------|------|
| **22** | CENTER | 130% | 없음 | **표 헤더 셀** (가운데 정렬, 빽빽) |
| **33** | CENTER | 160% | 없음 | 표 본문 셀 (가운데 정렬) |
| 34 | LEFT | 100% | left=400 | 표 셀 (왼쪽, 타이트) |

### 3-4. 위험 — 개요 자동번호 (heading=OUTLINE)

> **경고**: 아래 ID를 일반 텍스트에 사용하면 "1.", "가." 같은 번호가 자동 삽입된다.
> 반드시 개요(outline) 구조가 필요한 경우에만 사용할 것.

| ID | 개요 레벨 | 들여쓰기 left | 자동번호 예시 |
|----|-----------|--------------|--------------|
| 2 | 0 (최상위) | 1000 | 1. |
| 3 | 1 | 2000 | 가. |
| 4 | 2 | 3000 | (1) |
| 5 | 3 | 4000 | (가) |
| 6 | 4 | 5000 | ① |
| 7 | 5 | 6000 | ㉮ |
| 8 | 6 | 7000 | (최하위) |

### 3-5. 주의 — 불릿 자동삽입 (heading=BULLET)

| ID | 비고 |
|----|------|
| 26, 27, 46, 55 | 불릿 문자가 자동으로 삽입됨 — 직접 기호를 쓸 필요 없음 |

---

## 4. 테두리/배경 스타일 (borderFill)

표 셀에서 `<hp:tc borderFillIDRef="N">`으로, 문단에서 참조한다.

### 4-1. 일반 스타일

| ID | 테두리 | 배경색 | 용도 |
|----|--------|--------|------|
| **1** | 없음 | 없음 | **기본값** — 일반 문단, 배경 없는 곳 |
| **4** | SOLID 0.12mm 사방 | 없음 | **기본 표 셀** — 가장 범용 |

### 4-2. 표 셀 변형 (테두리 조합)

| ID | 테두리 | 배경색 | 용도 |
|----|--------|--------|------|
| 5 | 좌+상+하 (우 없음) | 없음 | 표 좌측 경계 셀 |
| 7 | 상+하 (좌우 없음) | 없음 | 수평 구분선 셀 |
| 8 | 우+상+하 (좌 없음) | 없음 | 표 우측 경계 셀 |
| 10 | 좌+우+상 (하 없음) | 없음 | **연결 셀(상단)** — 아래 셀과 시각적으로 연결 |
| 11 | 좌+우+하 (상 없음) | 없음 | **연결 셀(하단)** — 위 셀과 시각적으로 연결 |
| 12 | 좌+우 (상하 없음) | 없음 | **연결 셀(중간)** — 위아래 셀과 연결 |
| 13 | SOLID 0.12mm 사방 | 없음 | 기본 표 셀 (bf4와 동일) |

> **연결 셀 기법**: bf10(상단) + bf12(중간) + bf11(하단)을 사용하면 여러 행이 하나의 영역으로 보인다. 제목과 부제목을 하나의 박스로 묶을 때 유용.

### 4-3. 배경색 있는 셀 (표 헤더/강조/박스)

| ID | 테두리 | 배경색 | 용도 |
|----|--------|--------|------|
| **22** | SOLID 0.12mm 사방 | **#F2F2F2** (연회색) | **표 헤더 배경** — 가장 범용적. 표의 첫 행에 사용 |
| **23** | SOLID 0.12mm 사방 | **#DFE6F7** (연파랑) | **강조 헤더** — 플로차트 단계, 섹션 구분 |
| **24** | SOLID 0.12mm + 하단 DOUBLE_SLIM 0.5mm | **#E5E5E5** (중회색) | **구분선 헤더** — 헤더와 데이터 사이 이중선 구분 |
| **25** | DASH 0.12mm 사방 | **#EDEDED** (옅은회색) | **주의/정보 박스** — ※ 참고사항, 조건 박스 |
| **26** | DASH 0.12mm 사방 | **#ECF2FA** (옅은파랑) | **안내 박스** — 참고 안내, 신청 방법 등 |

> **표 헤더 기본 조합**: borderFill=**22** + charPr=**136**(10pt 돋움체 BOLD) + paraPr=**22**(가운데 130%)
> 실제 정부 문서의 표 헤더는 거의 예외 없이 배경색이 있다. 배경 없는 표 헤더는 아마추어 인상.

### 4-4. 어두운 배경 (흰색 텍스트 필수)

| ID | 테두리 | 배경색 | 용도 |
|----|--------|--------|------|
| **14** | SOLID 0.3mm | **#000066** (짙은 남색) | **어두운 헤더** — 반드시 흰색 charPr 사용! |

> **필수 조합**: borderFill=14 → charPr=8(10pt 흰색), 26(17pt 흰색), 또는 55(16pt 흰색)
> 어두운 배경에 검정 텍스트를 넣으면 보이지 않는다.

---

## 5. doc4에서 실제 사용된 표 셀 조합

### 헤더 영역 (정보 셀)
```
borderFillIDRef = 5, 7, 8, 9  (헤더 영역 전용 borderFill)
charPrIDRef     = 8(흰색), 9, 10, 128, 129, 136
```

### 본문 영역
```
borderFillIDRef = 4  (기본 표 셀)
charPrIDRef     = 다양 (내용에 따라 선택)
```

---

## 6. 일반적인 조합 패턴 (copy-paste용)

### 패턴 A: 문서 메인 제목

```xml
<hp:p paraPrIDRef="19" styleIDRef="0">
  <hp:run charPrIDRef="128"><hp:t>국립보건연구원 주요 연구 성과</hp:t></hp:run>
</hp:p>
```
> paraPr 19 (CENTER, 160%) + charPr 128 (26pt 함초롬돋움 BOLD)
> **이유**: 메인 제목은 가운데 정렬 + 가장 큰 글씨 + 굵게로 시각적 위계의 최상위를 표현한다.

### 패턴 B: 파란색 부제목

```xml
<hp:p paraPrIDRef="0" styleIDRef="0">
  <hp:run charPrIDRef="4"><hp:t>연구 배경 및 목적</hp:t></hp:run>
</hp:p>
```
> paraPr 0 (JUSTIFY, 160%) + charPr 4 (16pt 함초롬돋움 #2E74B5)
> **이유**: 색상으로 구분되는 부제목. 본문과 같은 정렬이지만 파란색과 큰 글씨로 구분한다.

### 패턴 C: □ 소제목

```xml
<hp:p paraPrIDRef="0" styleIDRef="0">
  <hp:run charPrIDRef="29"><hp:t>□ 주요 추진 내용</hp:t></hp:run>
</hp:p>
```
> paraPr 0 (JUSTIFY, 160%) + charPr 29 (15pt HY헤드라인M BOLD)
> **이유**: □ 기호와 헤드라인 서체로 소제목 역할. paraPr 0은 heading=NONE이므로 자동번호 없이 안전.

### 패턴 D: 기본 본문

```xml
<hp:p paraPrIDRef="0" styleIDRef="0">
  <hp:run charPrIDRef="9"><hp:t>국립보건연구원은 감염병 대응 연구를 강화한다.</hp:t></hp:run>
</hp:p>
```
> paraPr 0 (JUSTIFY, 160%) + charPr 9 (14pt 함초롬바탕)
> **이유**: 가장 기본적인 조합. 양쪽 정렬 + 적당한 크기의 명조체가 공문서 본문의 표준이다.

### 패턴 E: ㅇ 들여쓰기 설명

```xml
<hp:p paraPrIDRef="1" styleIDRef="0">
  <hp:run charPrIDRef="9"><hp:t>ㅇ 감염병 예방을 위한 백신 개발 연구를 추진한다.</hp:t></hp:run>
</hp:p>
```
> paraPr 1 (JUSTIFY, 160%, left=1500) + charPr 9 (14pt 함초롬바탕)
> **이유**: ㅇ 기호 앞에 들여쓰기를 넣어 본문과의 위계를 표현한다.

### 패턴 F: - 세부항목

```xml
<hp:p paraPrIDRef="14" styleIDRef="0">
  <hp:run charPrIDRef="9"><hp:t>- 대상: 만 65세 이상 고령자</hp:t></hp:run>
</hp:p>
```
> paraPr 14 (LEFT, 160%, left=1100) + charPr 9 (14pt 함초롬바탕)
> **이유**: ㅇ보다 한 단계 안쪽으로 들여쓰기하여 하위 항목임을 나타낸다.

### 패턴 G: 표 헤더 셀 (배경색 있음 — 권장)

```xml
<hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="22">
  <hp:subList>
    <hp:p paraPrIDRef="22" styleIDRef="0">
      <hp:run charPrIDRef="136"><hp:t>구분</hp:t></hp:run>
    </hp:p>
  </hp:subList>
</hp:tc>
```
> borderFill **22** (#F2F2F2 연회색 배경) + paraPr 22 (CENTER, 130%) + charPr 136 (10pt 돋움체 BOLD)
> **이유**: 실제 정부 문서의 표 헤더는 거의 예외 없이 연회색/연파랑 배경을 갖는다. 배경 없는 표 헤더는 데이터 행과 구분이 안 되어 아마추어 인상을 준다.
> **변형**: borderFill 23(연파랑)은 플로차트/프로세스 표에, 24(중회색+이중선)는 복잡한 표의 최상단에 사용.

### 패턴 H: 표 본문 셀

```xml
<hp:tc borderFillIDRef="4">
  <hp:subList>
    <hp:p paraPrIDRef="33" styleIDRef="0">
      <hp:run charPrIDRef="0"><hp:t>500억 원</hp:t></hp:run>
    </hp:p>
  </hp:subList>
</hp:tc>
```
> borderFill 4 (SOLID 테두리) + paraPr 33 (CENTER, 160%) + charPr 0 (10pt 함초롬돋움)
> **이유**: 본문 셀도 가운데 정렬이 일반적. 굵기 없이 일반 서체로 데이터를 표시.

### 패턴 I: 어두운 배경 + 흰색 제목

```xml
<hp:tc borderFillIDRef="14">
  <hp:subList>
    <hp:p paraPrIDRef="22" styleIDRef="0">
      <hp:run charPrIDRef="26"><hp:t>연구 성과 요약</hp:t></hp:run>
    </hp:p>
  </hp:subList>
</hp:tc>
```
> borderFill 14 (#000066 짙은 남색) + paraPr 22 (CENTER) + charPr 26 (17pt HY헤드라인M #FFFFFF)
> **이유**: 어두운 배경에는 반드시 흰색 텍스트를 사용. charPr 8(10pt), 26(17pt), 55(16pt) 중 크기에 맞게 선택.

### 패턴 J: 날짜/오른쪽 정렬

```xml
<hp:p paraPrIDRef="29" styleIDRef="0">
  <hp:run charPrIDRef="9"><hp:t>2026. 3. 29.(토)</hp:t></hp:run>
</hp:p>
```
> paraPr 29 (RIGHT, 160%) + charPr 9 (14pt 함초롬바탕)
> **이유**: 날짜나 발행 정보는 오른쪽 정렬이 공문서 관행.

### 패턴 K: 각주/출처

```xml
<hp:p paraPrIDRef="0" styleIDRef="0">
  <hp:run charPrIDRef="1"><hp:t>※ 출처: 국립보건연구원 내부자료</hp:t></hp:run>
</hp:p>
```
> paraPr 0 (JUSTIFY, 160%) + charPr 1 (9pt 함초롬돋움)
> **이유**: 작은 크기(9pt)로 본문과 시각적으로 구분하되, 정렬은 기본 양쪽맞춤 유지.

### 패턴 L: 번호 섹션 헤더 (표 기반)

마크다운의 `# 1 제목` 형식을 만나면 반드시 이 표 패턴을 사용한다.

```xml
<hp:p paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
  <hp:run charPrIDRef="0">
    <hp:tbl rowCnt="1" colCnt="2" cellSpacing="0" borderFillIDRef="4"
            pageBreak="CELL" repeatHeader="0" id="0">
      <hp:tr>
        <hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="14">
          <hp:cellAddr colAddr="0" rowAddr="0"/>
          <hp:cellSpan colSpan="1" rowSpan="1"/>
          <hp:cellSz width="3500" height="1200"/>
          <hp:cellMargin left="283" right="283" top="141" bottom="141"/>
          <hp:subList>
            <hp:p paraPrIDRef="22" styleIDRef="0">
              <hp:run charPrIDRef="26"><hp:t>1</hp:t></hp:run>
            </hp:p>
          </hp:subList>
        </hp:tc>
        <hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="4">
          <hp:cellAddr colAddr="1" rowAddr="0"/>
          <hp:cellSpan colSpan="1" rowSpan="1"/>
          <hp:cellSz width="38500" height="1200"/>
          <hp:cellMargin left="283" right="283" top="141" bottom="141"/>
          <hp:subList>
            <hp:p paraPrIDRef="33" styleIDRef="0">
              <hp:run charPrIDRef="29"><hp:t> 사업 개요</hp:t></hp:run>
            </hp:p>
          </hp:subList>
        </hp:tc>
      </hp:tr>
    </hp:tbl>
  </hp:run>
</hp:p>
```
> 열 1: bf14(남색) + charPr 26(17pt 흰색 HY헤드라인M) — 번호 셀
> 열 2: bf4(일반) + charPr 29(15pt HY헤드라인M BOLD) — 제목 셀
> **핵심**: 마크다운의 `# N 제목`은 항상 이 표로. `## 소제목`은 기존 □ 텍스트 스타일.

### 패턴 M: ※ 주의/정보 박스

마크다운의 `> blockquote`나 `※` 참고사항은 1x1 표로 감싸면 시각적으로 돋보인다.

```xml
<hp:p paraPrIDRef="0" styleIDRef="0">
  <hp:run charPrIDRef="0">
    <hp:tbl rowCnt="1" colCnt="1" cellSpacing="0" borderFillIDRef="4"
            pageBreak="CELL" repeatHeader="0" id="0">
      <hp:tr>
        <hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="25">
          <hp:cellAddr colAddr="0" rowAddr="0"/>
          <hp:cellSpan colSpan="1" rowSpan="1"/>
          <hp:cellSz width="42000" height="1000"/>
          <hp:cellMargin left="283" right="283" top="141" bottom="141"/>
          <hp:subList>
            <hp:p paraPrIDRef="0" styleIDRef="0">
              <hp:run charPrIDRef="1"><hp:t>※ 참고사항 텍스트</hp:t></hp:run>
            </hp:p>
          </hp:subList>
        </hp:tc>
      </hp:tr>
    </hp:tbl>
  </hp:run>
</hp:p>
```
> borderFill **25** (#EDEDED 옅은회색, DASH 테두리) + charPr 1 (9pt) 또는 0 (10pt)
> **이유**: 점선 테두리 + 옅은 배경이 "참고" 성격을 시각적으로 전달한다.
> **변형**: borderFill 26(옅은파랑)은 신청 안내, 절차 설명 등 안내성 박스에.

### 패턴 M: < 캡션 > 스타일 (표 위 설명)

표 바로 위에 오는 `< 제목 >` 형식의 캡션:
```xml
<hp:p paraPrIDRef="19" styleIDRef="0">
  <hp:run charPrIDRef="51"><hp:t>< 지역기반 아이디어 선정규모(안) ></hp:t></hp:run>
</hp:p>
```
> paraPr 19 (CENTER) + charPr 51 (12pt 맑은고딕 BOLD)
> **이유**: 본문보다 작고 고딕체이며 가운데 정렬 — 표의 "라벨" 역할. 꺾쇠 < >로 감싸는 것이 정부 문서 관행.

---

## 7. 흔한 실수 방지 체크리스트

1. **paraPr 2~8을 일반 텍스트에 사용하지 말 것** → heading=OUTLINE이므로 자동번호가 삽입된다.
2. **borderFill 14에 검정 텍스트를 넣지 말 것** → 배경이 #000066이라 보이지 않는다. charPr 8/26/55 사용.
3. **charPr 8/26/55를 밝은 배경에 사용하지 말 것** → 흰색(#FFFFFF) 텍스트라 보이지 않는다.
4. **header.xml에 없는 ID를 사용하지 말 것** → 문서가 깨진다.
5. **paraPr 26/27/46/55는 heading=BULLET** → 불릿 기호가 자동 삽입되므로 직접 기호를 쓰면 중복된다.
6. **charPr 128은 26pt** → 메인 제목 전용. 본문에 사용하면 지나치게 크다.
7. **표 셀에서는 paraPr 22(헤더), 33(본문 가운데), 34(본문 왼쪽)를 사용** → 일반 본문용 paraPr 0을 표에 넣으면 줄간격이 불필요하게 넓다.
