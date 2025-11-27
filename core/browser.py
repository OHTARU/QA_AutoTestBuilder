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
        """브라우저 실행 (시크릿 모드로 보안 팝업 원천 차단)"""
        try:
            service = Service(ChromeDriverManager().install())
            
            options = webdriver.ChromeOptions()
            
            # [핵심 해결책] 시크릿 모드 적용 (비밀번호 검사 안 함)
            options.add_argument("--incognito")
            
            # [안정성 옵션] 튕김 방지
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            
            # 비밀번호 저장 팝업 끄기 (Prefs)
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False, # 유출 감지 끄기
            }
            options.add_experimental_option("prefs", prefs)
            
            # 봇 탐지 방지
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.get(url)
            
            self._inject_click_tracker()
            
            return True, "브라우저 실행 중 (시크릿 모드)"
        except Exception as e:
            return False, f"실행 실패: {e}"

    def _inject_click_tracker(self):
        if not self.driver: return
        try:
            js_code = """
            document.addEventListener('mousedown', function(event) {
                window.lastClickedElement = event.target;
            }, true);
            """
            self.driver.execute_script(js_code)
        except Exception as e:
            print(f"Tracker Injection Failed: {e}")

    def get_selected_element(self):
        if not self.driver: return None
        try:
            last_el = self.driver.execute_script("return window.lastClickedElement;")
            if last_el: return last_el
            return self.driver.switch_to.active_element
        except Exception:
            return self.driver.switch_to.active_element

    def get_selected_text(self):
        if not self.driver: return ""
        try:
            text = self.driver.execute_script("return window.getSelection().toString();")
            return text.strip() if text else ""
        except Exception:
            return ""

    def highlight_element(self, element=None, locator_type=None, locator_value=None):
        if not self.driver: return
        try:
            target = element
            if not target and locator_type and locator_value:
                if locator_type == "ID": by = By.ID
                elif locator_type == "CSS": by = By.CSS_SELECTOR
                elif locator_type == "NAME": by = By.NAME
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
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None