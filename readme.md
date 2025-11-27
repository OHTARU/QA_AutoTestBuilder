# No-Code Test Automation Builder

**Selenium 테스트 스크립트를 생성하고 실행하는 GUI 자동화 솔루션**

![Project Status](https://img.shields.io/badge/Status-Active-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.x-yellow)
![Allure](https://img.shields.io/badge/Report-Allure-orange)

## 프로젝트 소개 (Overview)
QA 엔지니어들이 반복적인 UI 테스트 코드를 작성하는 데 들이는 시간을 단축하기 위해 개발된 **No-Code 자동화 도구**입니다.
사용자는 브라우저에서 요소를 클릭하거나 드래그하는 직관적인 동작만으로 **식별자(ID/XPath/CSS)를 자동 추출**할 수 있으며, 이를 기반으로 **Pytest 기반의 견고한 테스트 코드**를 자동 생성합니다.

### 개발 배경 (Motivation)
- **반복 업무 제거:** `F12`를 눌러 ID를 복사하고 코드로 옮기는 단순 반복 작업을 자동화하고자 했습니다.
- **유지보수성:** 하드코딩된 `time.sleep` 대신 `WebDriverWait`를 적용한 표준화된 코드를 생성하여 테스트 안정성을 높였습니다.
- **접근성:** 코딩을 모르는 기획자나 매뉴얼 QA도 자동화 테스트를 수행할 수 있는 환경을 제공합니다.

---

## 핵심 기능 (Key Features)

### 1. 스마트 요소 스캔 (Smart Scanning)
- **클릭 투 스캔 (Click-to-Scan):** 브라우저에서 요소를 클릭하고 `F2` 키를 누르면 자동으로 리스트에 추가됩니다.
- **드래그 텍스트 검증:** 텍스트를 드래그하고 스캔하면 자동으로 `Assertion`(검증) 단계가 생성됩니다.
- **최적 로케이터 추천:** `Data-TestID` > `ID` > `Name` > `CSS` > `XPath` 순으로 가장 안정적인 식별자를 자동 선택합니다.

### 2. ⚡ 강력한 테스트 실행 (Robust Execution)
- **Smart Wait:** 네트워크 지연을 고려하여 요소가 나타날 때까지 기다리는 `Explicit Wait` 로직이 자동 적용됩니다.
- **Assertion:** 텍스트 유무, 요소 존재 여부 등 테스트 성공/실패를 판별하는 검증 로직을 지원합니다.
- **Allure Reporting:** 테스트 종료 후 상세한 시각화 리포트(성공/실패/로그)를 자동으로 띄워줍니다.

### 3. 🛡️ 보안 및 편의성
- **Password Masking:** 비밀번호 입력 시 화면에 노출되지 않도록 마스킹(`******`) 처리합니다.
- **JSON 관리:** 작성된 시나리오를 JSON 파일로 저장하고 불러와 재사용할 수 있습니다.

---

## 기술 스택 (Tech Stack)

| 구분 | 기술 | 설명 |
| :--- | :--- | :--- |
| **Language** | Python 3.14 | 핵심 로직 구현 |
| **GUI** | Tkinter | 사용자 인터페이스(UI) 구성 |
| **Core** | Selenium WebDriver | 브라우저 제어 및 요소 스캔 |
| **Testing** | Pytest | 테스트 실행 및 관리 |
| **Reporting** | Allure | 테스트 결과 시각화 리포트 |
| **Architecture** | Modular Pattern | Core/GUI/Utils 로직 분리 설계 |

---

## 프로젝트 구조 (Architecture)

유지보수와 확장성을 고려하여 **기능별로 모듈화(Modularization)** 된 구조를 갖추고 있습니다.

```text
AutoTestBuilder/
├── main.py                  # 프로그램 진입점 (Entry Point)
├── config.py                # 전역 설정 (Timeout, URL 등)
├── core/                    # [핵심 로직]
│   ├── browser.py           # Selenium Driver 및 JS Tracker 관리
│   ├── scanner.py           # DOM 분석 및 로케이터 추출 알고리즘
│   ├── generator.py         # Pytest 코드 자동 생성기 (Template Engine)
│   └── runner.py            # Subprocess 기반 테스트 실행기
├── gui/                     # [사용자 화면]
│   ├── app.py               # 메인 윈도우 및 이벤트 핸들링
│   └── components.py        # 리스트 아이템, 콤보박스 등 UI 컴포넌트
└── utils/                   # [유틸리티]
    └── file_manager.py      # JSON 직렬화/역직렬화 처리
```

---

## 실행 방법 (Getting Started)

### 1. 필수 요구사항 (Prerequisites)
- Python 3.x 설치
- Chrome Browser 설치
- (선택) [Allure Commandline](https://docs.qameta.io/allure/) 설치 (리포트 확인용)

### 2. 설치 (Installation)
```bash
# 저장소 클론
git clone https://github.com/[본인아이디]/AutoTestBuilder.git

# 프로젝트 폴더로 이동
cd AutoTestBuilder

# 의존성 패키지 설치
pip install -r requirements.txt
```

### 3. 실행 (Usage)
```bash
python main.py
```

### 4. 사용 가이드
1.  **[🌐 열기]** 버튼을 눌러 테스트 브라우저를 실행합니다.
2.  테스트할 요소를 **클릭**하거나 텍스트를 **드래그**합니다.
3.  프로그램에서 **`F2` 키** (또는 스캔 버튼)를 누릅니다.
4.  리스트에서 **Action**(`click`, `input`, `check_text`)을 설정합니다.
5.  **[▶ 테스트 시작]** 버튼을 눌러 자동화 테스트를 수행합니다.

---
## 로드맵 (Roadmap)

- [x] **v1.0:** 모듈화 구조 설계 및 기본 스캔/실행 기능
- [x] **v2.0:** Smart Wait 및 Assertion(검증) 기능 탑재
- [x] **v2.5:** 드래그 텍스트 검증, 단축키, 보안 마스킹 적용
- [ ] **v3.0:** Iframe 자동 감지 및 Alert 처리 (개발 중)
- [ ] **v4.0:** 엑셀 기반 데이터 주도 테스트(DDT) 지원 예정

---

## 라이선스 (License)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.