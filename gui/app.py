import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import sys
import config
from core.browser import BrowserManager
from core.scanner import PageScanner
from core.generator import ScriptGenerator
from core.runner import TestRunner
from gui.components import StepListManager
from utils.file_manager import save_to_json, load_from_json

class AutoTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("No-Code Test Builder v5.4 (Restored)")
        self.geometry("620x800")
        
        self.browser = BrowserManager()
        self.scanner = PageScanner()
        self.generator = ScriptGenerator()
        self.runner = TestRunner()
        self.steps_data = []

        self._setup_ui()
        
        self.bind("<F2>", lambda event: self.cmd_scan_element())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _setup_ui(self):
        top = tk.Frame(self, pady=5)
        top.pack(fill="x")
        tk.Label(top, text="URL:").pack(side="left")
        self.url_entry = tk.Entry(top, width=30)
        self.url_entry.pack(side="left", padx=5)
        self.url_entry.insert(0, config.DEFAULT_URL)
        tk.Button(top, text="🌐 열기", command=self.cmd_open_browser, bg="#E1F5FE").pack(side="left")
        tk.Button(top, text="💾 저장", command=self.cmd_save).pack(side="right", padx=5)
        tk.Button(top, text="📂 로드", command=self.cmd_load).pack(side="right")

        ctrl = tk.Frame(self, pady=10, bg="#F5F5F5")
        ctrl.pack(fill="x")
        tk.Button(ctrl, text="🎯 요소/텍스트 스캔 (F2)", command=self.cmd_scan_element, 
                  bg="#FFCCBC", width=25, height=2).pack(side="left", padx=10)
        tk.Button(ctrl, text="🔗 URL 검증 추가", command=self.cmd_add_url_check,
                  bg="#C8E6C9", width=20, height=2).pack(side="left", padx=5)

        list_frame = tk.LabelFrame(self, text="테스트 시나리오", padx=5, pady=5)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        canvas = tk.Canvas(list_frame, bg="white")
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="white")
        
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.list_manager = StepListManager(
            self.scrollable_frame, 
            self.steps_data, 
            None, 
            self.cmd_highlight
        )

        btm = tk.Frame(self, pady=10, bg="#E8EAF6")
        btm.pack(fill="x")
        tk.Button(btm, text="▶ 테스트 시작", command=self.cmd_run_test, 
                  bg="#4CAF50", fg="white", width=20).pack(side="left", padx=20)
        tk.Button(btm, text="⏹ 정지", command=self.cmd_stop_test, 
                  bg="#F44336", fg="white").pack(side="right", padx=20)
        
        self.status_label = tk.Label(self, text="상태: 대기 중", fg="blue")
        self.status_label.pack()

    def cmd_open_browser(self):
        success, msg = self.browser.open_browser(self.url_entry.get())
        if not success: messagebox.showerror("에러", msg)
        else: self.status_label.config(text=msg, fg="green")

    def cmd_scan_element(self):
        selected_text = self.browser.get_selected_text()
        if selected_text:
            step = self.scanner.create_text_validation_step(selected_text)
            self.steps_data.append(step)
            self.list_manager.refresh()
            self.status_label.config(text=f"텍스트 검증 추가됨: {selected_text[:10]}...", fg="green")
            return

        if hasattr(self.browser, "get_selected_element"):
             el = self.browser.get_selected_element()
        else:
             el = self.browser.get_active_element()

        if not el or el.tag_name == 'html':
            messagebox.showwarning("경고", "요소를 클릭하거나 텍스트를 드래그 후 시도하세요.")
            return
        
        if hasattr(self.browser, "_inject_click_tracker"):
            self.browser._inject_click_tracker()

        step = self.scanner.create_step_data(el)
        self.steps_data.append(step)
        self.list_manager.refresh()
        self.browser.highlight_element(element=el)

    def cmd_add_url_check(self):
        if not self.browser.driver:
            messagebox.showwarning("경고", "브라우저가 열려있지 않습니다.")
            return
        current_url = self.browser.driver.current_url
        step = self.scanner.create_url_validation_step(current_url)
        self.steps_data.append(step)
        self.list_manager.refresh()
        self.status_label.config(text=f"URL 검증 추가됨: {current_url}", fg="green")

    def cmd_highlight(self, step):
        if step['action'] == "check_url":
            messagebox.showinfo("알림", "URL 검증은 요소를 하이라이트할 수 없습니다.")
            return
        self.browser.highlight_element(locator_type=step['type'], locator_value=step['locator'])

    def cmd_save(self):
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if f: save_to_json(f, self.url_entry.get(), self.steps_data)

    def cmd_load(self):
        f = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if f:
            url, steps = load_from_json(f)
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
            self.steps_data.clear()
            self.steps_data.extend(steps)
            self.list_manager.refresh()

    def cmd_run_test(self):
        if not self.steps_data: return
        script = self.generator.generate(self.url_entry.get(), self.steps_data)
        with open(config.TEMP_TEST_FILE, "w", encoding="utf-8") as f:
            f.write(script)
        threading.Thread(target=self._run_process).start()

    def _run_process(self):
        self.status_label.config(text="테스트 실행 중...", fg="blue")
        proc = self.runner.run_pytest()
        stdout, stderr = proc.communicate()
        self.status_label.config(text="테스트 완료. 리포트 생성.", fg="purple")
        self.runner.open_report()

    def cmd_stop_test(self):
        self.runner.stop()
        self.status_label.config(text="테스트 중지됨", fg="red")

    def on_close(self):
        if messagebox.askokcancel("종료", "프로그램을 종료하시겠습니까?"):
            if self.browser: self.browser.close()
            self.destroy()
            sys.exit(0)