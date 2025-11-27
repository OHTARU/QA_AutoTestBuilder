from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import config
import time

class BrowserManager:
    def __init__(self):
        self.driver = None

    def open_browser(self, url):
        """브라우저 실행 및 Click Tracker 주입"""
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)
            self.driver.maximize_window()
            self.driver.get(url)
            
            # [Level 2.5] 클릭 추적기(JS) 주입
            self._inject_click_tracker()
            
            return True, "브라우저 실행 중 (클릭 및 드래그 추적 활성화)"
        except Exception as e:
            return False, f"실행 실패: {e}"

    def _inject_click_tracker(self):
        """자바스크립트로 클릭 이벤트 리스너를 심음"""
        if not self.driver: return
        try:
            # 마우스가 눌리는 순간(mousedown) 그 요소를 변수에 저장
            js_code = """
            document.addEventListener('mousedown', function(event) {
                window.lastClickedElement = event.target;
            }, true);
            """
            self.driver.execute_script(js_code)
        except Exception as e:
            print(f"Tracker Injection Failed: {e}")

    def get_selected_element(self):
        """마지막으로 클릭된 요소를 가져옴 (없으면 Active Element)"""
        if not self.driver: return None

        try:
            # 1. JS로 기록된 '마지막 클릭 요소'를 가져와 봄
            last_el = self.driver.execute_script("return window.lastClickedElement;")
            
            if last_el:
                return last_el
            
            # 2. 기록된 게 없으면 기존 방식(Focus) 시도
            return self.driver.switch_to.active_element
            
        except Exception:
            return self.driver.switch_to.active_element

    def get_selected_text(self):
        """[NEW] 현재 드래그(Highlight)된 텍스트를 가져옴"""
        if not self.driver: return ""
        try:
            # 자바스크립트로 선택 영역의 텍스트 추출
            text = self.driver.execute_script("return window.getSelection().toString();")
            return text.strip() if text else ""
        except Exception:
            return ""

    def highlight_element(self, element=None, locator_type=None, locator_value=None):
        """요소 하이라이트 (CSS Selector 지원)"""
        if not self.driver: return

        try:
            target = element
            if not target and locator_type and locator_value:
                if locator_type == "ID": by = By.ID
                elif locator_type == "CSS": by = By.CSS_SELECTOR
                else: by = By.XPATH
                target = self.driver.find_element(by, locator_value)
            
            if target:
                self.driver.execute_script(
                    f"arguments[0].style.border='{config.HIGHLIGHT_BORDER} solid {config.HIGHLIGHT_COLOR}';", 
                    target
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target)
        except Exception as e:
            print(f"Highlight Error: {e}")

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None