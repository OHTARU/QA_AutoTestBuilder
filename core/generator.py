import config

class ScriptGenerator:
    def generate(self, url, steps):
        """Pytest 스크립트 생성 (보안 강화: repr 사용)"""
        
        script = f"""
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito") 
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    
    prefs = {{
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("{url}")
    yield driver
    try:
        driver.quit()
    except:
        pass

@allure.feature("자동 생성된 테스트 시나리오")
def test_scenario(driver):
    wait = WebDriverWait(driver, {config.EXPLICIT_WAIT})
    actions = ActionChains(driver)
    drag_source_el = None
"""

        for i, step in enumerate(steps):
            safe_name = step['name'].replace('"', "'")
            
            if step["type"] == "ID": locator_type = "By.ID"
            elif step["type"] == "CSS": locator_type = "By.CSS_SELECTOR"
            elif step["type"] == "NAME": locator_type = "By.NAME"
            else: locator_type = "By.XPATH"

            locator_val = step["locator"]
            action = step["action"]
            value = step["value"]

            # [보안 패치] 값(Value)을 안전하게 변환 (repr 사용)
            # repr("abc") -> "'abc'", repr('a"b') -> "'a\"b'" 처럼 자동으로 따옴표 처리해줌
            safe_value = repr(value)

            if action in ["accept_alert", "dismiss_alert", "switch_default", "check_url"]:
                 script += f"""
    with allure.step("Step {i+1}: {action.upper()}"):
"""
            else:
                script += f"""
    with allure.step("Step {i+1}: {action.upper()} - {safe_name}"):
"""
                condition = "element_to_be_clickable" if action == "click" else "visibility_of_element_located"
                
                script += f"""        try:
            el = wait.until(EC.{condition}(({locator_type}, "{locator_val}")))
        except TimeoutException:
            print("\\n[WARN] Timeout! 요소를 찾지 못했습니다.")
            raise
"""

            if action == "click":
                script += """        try:
            el.click()
        except Exception:
            driver.execute_script("arguments[0].click();", el)
"""

            elif action in ["input", "input_password"]:
                # [수정] safe_value 사용 (이미 따옴표가 포함되어 있으므로 f-string에서 따옴표 제거)
                script += f"        el.clear()\n        el.send_keys({safe_value})\n"

            elif action == "check_text":
                script += f"""        actual_text = el.text
        expected = {safe_value}
        assert expected in actual_text, f"텍스트 불일치! 기대: {{expected}}, 실제: {{actual_text}}"
"""
            elif action == "check_url":
                script += f"""        wait.until(EC.url_contains({safe_value}))
        assert {safe_value} in driver.current_url
"""
            elif action == "switch_frame":
                script += "        driver.switch_to.frame(el)\n"
            elif action == "switch_default":
                script += "        driver.switch_to.default_content()\n"
            elif action == "accept_alert":
                script += "        driver.switch_to.alert.accept()\n"
            elif action == "dismiss_alert":
                script += "        driver.switch_to.alert.dismiss()\n"
            elif action == "drag_source":
                script += "        drag_source_el = el\n"
            elif action == "drop_target":
                script += """        if drag_source_el:
            actions.drag_and_drop(drag_source_el, el).perform()
        else:
            raise Exception("드래그 시작점 미설정")
"""

        return script