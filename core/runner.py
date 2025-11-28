import subprocess
import sys
import os
import config

class TestRunner:
    def __init__(self):
        self.process = None

    def run_pytest(self):
        """Subprocess로 Pytest 실행 (인코딩 및 출력 설정 강화)"""
        # 기존 결과 삭제
        if os.path.exists(config.ALLURE_RESULTS_DIR):
            try:
                for f in os.listdir(config.ALLURE_RESULTS_DIR):
                    os.remove(os.path.join(config.ALLURE_RESULTS_DIR, f))
            except:
                pass

        cmd = [sys.executable, "-m", "pytest", config.TEMP_TEST_FILE, f"--alluredir={config.ALLURE_RESULTS_DIR}"]
        
        # [수정] encoding='utf-8' 추가 (한글 깨짐 방지)
        # errors='replace' 추가 (인코딩 에러 무시)
        self.process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            encoding='utf-8',
            errors='replace' 
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