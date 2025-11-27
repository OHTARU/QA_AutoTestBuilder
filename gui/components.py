import tkinter as tk
from tkinter import ttk

class StepListManager:
    def __init__(self, parent_frame, steps_data, on_update_callback, on_highlight_callback):
        self.parent = parent_frame
        self.steps = steps_data
        self.on_update = on_update_callback
        self.on_highlight = on_highlight_callback

    def refresh(self):
        """리스트 UI 새로고침"""
        for widget in self.parent.winfo_children():
            widget.destroy()

        for idx, step in enumerate(self.steps):
            self._create_row(idx, step)

    def _create_row(self, idx, step):
        row = tk.Frame(self.parent, bg="white", pady=2, bd=1, relief="solid")
        row.pack(fill="x", pady=2, padx=5)

        # 1. 순서
        tk.Label(row, text=f"{idx+1}", width=2, bg="white").pack(side="left")

        # 2. 이름 수정
        name_var = tk.StringVar(value=step["name"])
        name_var.trace("w", lambda *a: self._update_step_data(idx, "name", name_var.get()))
        tk.Entry(row, textvariable=name_var, width=18, bg="#F0F0F0").pack(side="left", padx=5)

        # 3. 액션 선택 (input_password 추가됨)
        action_var = tk.StringVar(value=step["action"])
        cb = ttk.Combobox(row, textvariable=action_var, 
                          values=["click", "input", "input_password", "check_text"], 
                          width=10, state="readonly")
        cb.pack(side="left", padx=2)
        cb.bind("<<ComboboxSelected>>", lambda e: self._update_step_data(idx, "action", action_var.get(), refresh=True))

        # 4. 입력값 (Input 계열 또는 Check Text일 때 표시)
        if step["action"] in ["input", "input_password", "check_text"]:
            val_var = tk.StringVar(value=step["value"])
            val_var.trace("w", lambda *a: self._update_step_data(idx, "value", val_var.get()))
            
            # 색상 및 마스킹 설정
            bg_color = "#E3F2FD" # 기본 파랑 (input)
            show_char = ""       # 기본 보임

            if step["action"] == "check_text":
                bg_color = "#FFF3E0" # 주황 (검증)
            elif step["action"] == "input_password":
                bg_color = "#FFEBEE" # 분홍 (비번)
                show_char = "*"      # [Level 2.5] 마스킹 처리

            tk.Entry(row, textvariable=val_var, width=15, bg=bg_color, show=show_char).pack(side="left", padx=5)

        # 5. 버튼 영역
        btn_frame = tk.Frame(row, bg="white")
        btn_frame.pack(side="right", padx=5)
        
        tk.Button(btn_frame, text="👁️", width=2, command=lambda: self.on_highlight(step)).pack(side="left")
        tk.Button(btn_frame, text="▲", width=2, command=lambda: self._move_step(idx, -1)).pack(side="left")
        tk.Button(btn_frame, text="▼", width=2, command=lambda: self._move_step(idx, 1)).pack(side="left")
        tk.Button(btn_frame, text="X", width=2, fg="red", command=lambda: self._delete_step(idx)).pack(side="left")

    def _update_step_data(self, idx, key, value, refresh=False):
        self.steps[idx][key] = value
        if refresh: self.refresh()

    def _move_step(self, idx, direction):
        new_idx = idx + direction
        if 0 <= new_idx < len(self.steps):
            self.steps[idx], self.steps[new_idx] = self.steps[new_idx], self.steps[idx]
            self.refresh()

    def _delete_step(self, idx):
        del self.steps[idx]
        self.refresh()