import config

class ScriptGenerator:
    def generate(self, url, steps):
        """Pytest 스크립트 문자열 생성 (Smart Wait & Assertion & Password Support)"""
        
        script = f"""
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # 필요시 주석 해제
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.get("{url}")
    yield driver
    driver.quit()

@allure.feature("자동 생성된 테스트 시나리오")
def test_scenario(driver):
    # [Level 2] 스마트 대기 객체 생성
    wait = WebDriverWait(driver, {config.EXPLICIT_WAIT})
"""

        for i, step in enumerate(steps):
            safe_name = step['name'].replace('"', "'")
            
            # 로케이터 타입 결정
            if step["type"] == "ID":
                locator_type = "By.ID"
            elif step["type"] == "CSS":
                locator_type = "By.CSS_SELECTOR"
            else:
                locator_type = "By.XPATH"

            locator_val = step["locator"]
            action = step["action"]
            value = step["value"]

            # 단계별 Allure 로그 시작
            script += f"""
    with allure.step("Step {i+1}: {action.upper()} - {safe_name}"):
"""
            
            # --- [스마트 대기 로직] ---
            condition = "element_to_be_clickable" if action == "click" else "visibility_of_element_located"
            
            script += f"""        # Smart Wait 적용
        el = wait.until(EC.{condition}(({locator_type}, "{locator_val}")))
"""

            # --- [액션별 실행 로직] ---
            if action == "click":
                script += "        el.click()\n"
            
            # [Level 2.5] input과 input_password는 동일하게 처리
            elif action in ["input", "input_password"]:
                script += f"        el.clear()\n        el.send_keys('{value}')\n"
            
            elif action == "check_text":
                script += f"""        # Assertion (텍스트 검증)
        actual_text = el.text
        expected_text = '{value}'
        assert expected_text in actual_text, f"검증 실패! 기대값 포함 여부 확인 불가. (기대: '{{expected_text}}', 실제: '{{actual_text}}')"
"""

        return script