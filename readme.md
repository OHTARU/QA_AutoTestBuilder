현재까지 개발된 **모든 기능(Level 4.5 완료 시점)**을 반영하여, **기능 명세**와 **사용 가이드**를 대폭 보강한 `README.md` 템플릿입니다.

**"개발 중"**으로 되어 있던 로드맵을 **"완료"**로 수정하고, 사용자가 이 툴을 처음 접했을 때 **"어떻게 엑셀을 연동하고 검증하는지"** 쉽게 알 수 있도록 가이드 섹션을 강화했습니다.

그대로 복사해서 사용하시면 됩니다.

---

# 🚀 No-Code Test Automation Builder

**코딩 없이 클릭만으로 Selenium 테스트 스크립트를 생성하고, 엑셀 데이터를 연동하여 대량 반복 테스트를 수행하는 올인원 솔루션**

![Project Status](https://img.shields.io/badge/Status-Active-green)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.x-yellow)
![Allure](https://img.shields.io/badge/Report-Allure-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📖 프로젝트 소개 (Overview)

QA 엔지니어 및 기획자가 반복적인 UI 테스트 코드를 작성하는 시간을 단축하기 위해 개발된 **No-Code 자동화 도구**입니다.
브라우저에서 요소를 클릭하거나 드래그하는 직관적인 동작만으로 **최적의 식별자(ID/XPath/CSS)를 자동 추출**하며, 이를 기반으로 **Pytest 기반의 견고한 테스트 코드**를 자동 생성 및 실행합니다.

### 💡 개발 배경 (Motivation)
- **반복 업무 제거:** 개발자 도구(F12)를 열어 ID를 복사하고 코드로 옮기는 단순 반복 작업을 자동화했습니다.
- **안정성 확보:** 하드코딩된 `time.sleep` 대신 `WebDriverWait`와 `Smart Locator` 전략을 적용하여 깨지지 않는 테스트를 구현했습니다.
- **데이터 주도 테스트(DDT):** 엑셀 파일 하나로 수백 개의 테스트 케이스를 자동으로 수행할 수 있는 환경을 제공합니다.

---

## ✨ 핵심 기능 (Key Features)

### 1. 🕵️ 스마트 요소 스캔 (Smart Scanning)
*   **지능형 로케이터:** `Data-TestID` > `ID` > `Name` > `Title` > `Alt` > `CSS` > `XPath` 순서로 가장 안정적인 식별자를 자동 선택합니다.
*   **동적 클래스 필터링:** React/Vue 등에서 생성되는 난수 형태의 클래스(`btn__xyz123`)를 자동으로 감지하고 무시합니다.
*   **드래그 텍스트 검증:** 화면의 글자를 드래그하고 `F2`를 누르면 `Text Assertion`(글자 검증) 단계가 생성됩니다.
*   **단축키 지원:** 마우스 이동 없이 `F2` 키 하나로 즉시 스캔이 가능합니다.

### 2. 🎮 다양한 액션 지원 (Advanced Actions)
*   **기본 제어:** 클릭, 텍스트 입력, 비밀번호 입력(마스킹/암호화).
*   **고급 제어:** 키보드 입력(Enter/Tab), 마우스 호버(Hover), 드래그 앤 드롭(Drag & Drop).
*   **프레임/팝업:** Iframe 내부 요소 제어 (`switch_frame`) 및 브라우저 경고창 처리 (`Alert`).
*   **검증(Assertion):** 텍스트 일치 여부 및 URL 변경 여부 검증.

### 3. 📊 데이터 주도 테스트 (Excel DDT)
*   **엑셀 연동:** `.xlsx` 파일을 로드하여 테스트 데이터로 사용합니다.
*   **변수 치환:** 시나리오 입력값에 `{ID}`, `{PW}` 등의 변수를 사용하면 엑셀 데이터로 자동 매핑됩니다.
*   **자동 반복:** 엑셀 행(Row) 개수만큼 브라우저를 띄워 반복 테스트를 수행합니다.

### 4. 🛡️ 실행 안정성 및 보안
*   **크롬 보안 우회:** 시크릿 모드(`--incognito`)와 특수 플래그를 사용하여 "비밀번호 유출 경고" 팝업을 원천 차단했습니다.
*   **스마트 대기:** 요소가 나타날 때까지 기다리는 `Explicit Wait`가 자동 적용됩니다.
*   **방해 요소 감지:** 투명 팝업이 버튼을 가릴 경우, 이를 감지하고 JS 강제 클릭을 시도합니다.
*   **Headless 모드:** 브라우저 화면 없이 백그라운드에서 고속으로 테스트를 수행할 수 있습니다.

---

## 🛠️ 기술 스택 (Tech Stack)

| 구분 | 기술 | 설명 |
| :--- | :--- | :--- |
| **Language** | Python 3.14 | 핵심 로직 구현 |
| **GUI** | Tkinter | 사용자 인터페이스(UI) 구성 |
| **Core** | Selenium WebDriver | 브라우저 제어 및 요소 스캔 |
| **Testing** | Pytest | 테스트 실행 및 관리 |
| **Data** | Pandas, OpenPyxl | 엑셀 데이터 처리 |
| **Security** | Cryptography | 비밀번호 암호화 저장 |
| **Reporting** | Allure | 테스트 결과 시각화 리포트 |

---

## 🚀 실행 방법 (Getting Started)

### 1. 필수 요구사항 (Prerequisites)
- Python 3.x 설치
- Chrome Browser 설치
- (선택) [Allure Commandline](https://docs.qameta.io/allure/) 설치 (리포트 확인용)

### 2. 설치 (Installation)
```bash
# 저장소 클론
git clone https://github.com/OHTARU/AutoTestBuilder.git

# 프로젝트 폴더로 이동
cd AutoTestBuilder

# 의존성 패키지 설치
pip install -r requirements.txt
```

### 3. 실행 (Usage)
```bash
python main.py
```

---

## 📖 사용 가이드 (User Guide)

### 🟢 기본 테스트 시나리오 만들기
1.  **[🌐 열기]** 버튼을 눌러 브라우저를 실행합니다.
2.  원하는 요소를 **클릭**하거나 텍스트를 **드래그**합니다.
3.  프로그램에서 **[🎯 요소 추가]** 버튼을 누르거나 키보드 **`F2`**를 누릅니다.
4.  리스트에서 **Action**을 선택하고 필요한 값을 입력합니다.
5.  **[▶ 테스트 시작]** 버튼을 눌러 자동화를 실행합니다.

### 🟡 엑셀 데이터 연동하기 (DDT)
1.  **엑셀 준비:** 첫 줄에 변수명(헤더)을 적고 데이터를 채웁니다. (예: `ID`, `PW`, `EXPECTED`)
2.  **[📊 엑셀 데이터 연동]** 버튼을 눌러 파일을 불러옵니다.
3.  시나리오 입력칸에 변수를 중괄호와 함께 적습니다. (예: `{ID}`, `{PW}`)
4.  실행하면 엑셀 데이터 줄 수만큼 테스트가 반복됩니다.

### 🔵 액션(Action) 종류 설명

| 액션명 | 설명 | 비고 |
| :--- | :--- | :--- |
| **click** | 요소를 클릭합니다. | JS 강제 클릭 지원 |
| **input** | 텍스트를 입력합니다. | |
| **input_password** | 비밀번호를 입력합니다. | 화면 마스킹(`***`) 처리 |
| **press_key** | 특수키를 입력합니다. | `ENTER`, `TAB` 등 |
| **check_text** | 화면에 특정 글자가 있는지 검증합니다. | 실패 시 스크린샷 |
| **check_url** | 페이지 URL이 변경되었는지 검증합니다. | |
| **switch_frame** | Iframe 내부로 진입합니다. | |
| **accept_alert** | 브라우저 경고창을 '확인'합니다. | |
| **drag_source** | 드래그할 요소를 잡습니다. | |
| **drop_target** | 잡은 요소를 이곳에 놓습니다. | |

---

## 🗺️ 개발 로드맵 (Roadmap)

- [x] **v1.0 (Core):** 모듈화 구조 설계 및 기본 스캔/실행 기능
- [x] **v2.0 (Smart):** Smart Wait, Assertion(검증), 텍스트 드래그 스캔
- [x] **v2.5 (UX/Security):** 단축키(F2), 비밀번호 암호화, 드래그 앤 드롭
- [x] **v3.0 (Stability):** Iframe/Alert 처리, 크롬 보안 팝업 완벽 차단
- [x] **v4.0 (Data):** 엑셀 기반 데이터 주도 테스트(DDT) 및 변수 치환
- [ ] **v5.0 (AI):** Self-Healing (요소 변경 시 자동 복구) 예정
- [ ] **v6.0 (Dist):** 실행 파일(.exe) 배포 예정

---

## 📄 라이선스 (License)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.