import subprocess
import sys
import os
import config

class TestRunner:
    def __init__(self):
        self.process = None

    def run_pytest(self):
        """Subprocess로 Pytest 실행"""
        # 기존 결과 삭제
        if os.path.exists(config.ALLURE_RESULTS_DIR):
            for f in os.listdir(config.ALLURE_RESULTS_DIR):
                os.remove(os.path.join(config.ALLURE_RESULTS_DIR, f))

        cmd = [sys.executable, "-m", "pytest", config.TEMP_TEST_FILE, f"--alluredir={config.ALLURE_RESULTS_DIR}"]
        
        # 실행 (Blocking 방지를 위해 Popen 사용)
        self.process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        return self.process

    def open_report(self):
        """Allure 리포트 열기"""
        subprocess.Popen(["allure", "serve", config.ALLURE_RESULTS_DIR], shell=True)

    def stop(self):
        """테스트 강제 종료"""
        if self.process:
            self.process.terminate()
            self.process = None