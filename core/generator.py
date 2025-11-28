import config
import os

class ScriptGenerator:
    def generate(self, url, steps, is_headless=False, excel_path=None):
        """Pytest 스크립트 생성 (들여쓰기 오류 수정)"""
        
        # [수정] 들여쓰기(Indentation)를 안전하게 처리
        setup_lines = []
        if is_headless:
            setup_lines.append('options.add_argument("--headless=new")')
            setup_lines.append('options.add_argument("--window-size=1920,1080")')
        else:
            setup_lines.append('options.add_argument("--start-maximized")')
        
        # 리스트의 각 줄 앞에 공백 4칸을 붙여서 합침
        headless_setup = "\n".join(["    " + line for line in setup_lines])

        # [Excel] 데이터 로딩 코드
        data_loader_code = ""
        decorator_code = ""
        test_args = "driver"
        
        if excel_path:
            safe_excel_path = excel_path.replace("\\", "/")
            data_loader_code = f"""
import pandas as pd
import sys
import os

def get_excel_data():
    file_path = r"{safe_excel_path}"
    print(f"\\n[INFO] 엑셀 로드 경로: {{file_path}}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"엑셀 파일이 없습니다: {{file_path}}")

    try:
        df = pd.read_excel(file_path, engine='openpyxl').fillna("")
        df.columns = [str(c).strip() for c in df.columns]
        data = df.to_dict(orient='records')
        print(f"[INFO] 데이터 {{len(data)}}건 로드됨")
        if not data:
            raise ValueError("데이터가 비어있습니다.")
        return data
    except Exception as e:
        raise ValueError(f"엑셀 로드 실패: {{e}}")
"""
            decorator_code = '@pytest.mark.parametrize("row_data", get_excel_data())'
            test_args = "driver, row_data"

        # --- 스크립트 시작 ---
        # 주의: {headless_setup}은 이미 공백 4칸을 포함하므로, f-string 내에서는 맨 앞에 붙여야 함
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

{data_loader_code}

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
{headless_setup}
    
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    prefs = {{
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
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

{decorator_code}
@allure.feature("자동 생성된 테스트 시나리오")
def test_scenario({test_args}):
    wait = WebDriverWait(driver, {config.EXPLICIT_WAIT})
    actions = ActionChains(driver)
    drag_source_el = None

    try:
"""

        for i, step in enumerate(steps):
            safe_name = step['name'].replace('"', "'")
            locator_val = step["locator"]
            action = step["action"]
            value = step["value"]
            
            if step["type"] == "ID": locator_type = "By.ID"
            elif step["type"] == "CSS": locator_type = "By.CSS_SELECTOR"
            elif step["type"] == "NAME": locator_type = "By.NAME"
            else: locator_type = "By.XPATH"

            if action == "comment":
                script += f"""
        with allure.step("💬 {safe_name}"):
            pass
"""
                continue

            value_expr = repr(value)
            if excel_path and "{" in value and "}" in value:
                value_expr = f"'{value}'.format(**row_data)"

            if action in ["accept_alert", "dismiss_alert", "switch_default", "check_url"]:
                 script += f"""
        with allure.step("Step {i+1}: {action.upper()}"):
"""
            else:
                script += f"""
        with allure.step("Step {i+1}: {action.upper()} - {safe_name}"):
"""
                condition = "element_to_be_clickable" if action == "click" else "visibility_of_element_located"
                
                script += f"""            try:
                el = wait.until(EC.{condition}(({locator_type}, "{locator_val}")))
            except TimeoutException:
                print("\\n[WARN] Timeout! 요소를 찾지 못했습니다.")
                raise
"""

            if action == "click":
                script += """            try:
                el.click()
            except Exception:
                driver.execute_script("arguments[0].click();", el)
"""
            elif action in ["input", "input_password"]:
                script += f"            el.clear(); el.send_keys({value_expr})\n"

            elif action == "check_text":
                script += f"""            actual = el.text
            expected = {value_expr}
            assert expected in actual, f"텍스트 불일치! (기대: {{expected}}, 실제: {{actual}})"
"""
            elif action == "check_url":
                script += f"""            wait.until(EC.url_contains({value_expr}))
            assert {value_expr} in driver.current_url
"""
            elif action == "switch_frame":
                script += "            driver.switch_to.frame(el)\n"
            elif action == "switch_default":
                script += "            driver.switch_to.default_content()\n"
            elif action == "accept_alert":
                script += "            driver.switch_to.alert.accept()\n"
            elif action == "dismiss_alert":
                script += "            driver.switch_to.alert.dismiss()\n"
            elif action == "drag_source":
                script += "            drag_source_el = el\n"
            elif action == "drop_target":
                script += """            if drag_source_el:
                actions.drag_and_drop(drag_source_el, el).perform()
            else:
                raise Exception("드래그 시작점 미설정")
"""

        script += """
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=allure.attachment_type.PNG)
        raise e
"""

        return script