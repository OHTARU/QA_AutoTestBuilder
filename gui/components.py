import tkinter as tk
from tkinter import ttk

class StepListManager:
    def __init__(self, parent_frame, steps_data, on_update_callback, on_highlight_callback):
        self.parent = parent_frame
        self.steps = steps_data
        self.on_update = on_update_callback
        self.on_highlight = on_highlight_callback

    def refresh(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        for idx, step in enumerate(self.steps):
            self._create_row(idx, step)

    def _create_row(self, idx, step):
        row = tk.Frame(self.parent, bg="white", pady=2, bd=1, relief="solid")
        row.pack(fill="x", pady=2, padx=5)

        tk.Label(row, text=f"{idx+1}", width=2, bg="white").pack(side="left")

        # 주석이면 배경색 변경
        entry_bg = "#F0F0F0"
        if step["action"] == "comment": entry_bg = "#FFF9C4"

        name_var = tk.StringVar(value=step["name"])
        name_var.trace("w", lambda *a: self._update_step_data(idx, "name", name_var.get()))
        tk.Entry(row, textvariable=name_var, width=18, bg=entry_bg).pack(side="left", padx=5)

        # [Level 4.5] 액션 목록 추가 (press_key, hover)
        action_var = tk.StringVar(value=step["action"])
        action_options = [
            "click", "input", "input_password", "check_text", "check_url",
            "press_key", "hover", # [New]
            "switch_frame", "switch_default",
            "accept_alert", "dismiss_alert",
            "drag_source", "drop_target",
            "comment"
        ]
        cb = ttk.Combobox(row, textvariable=action_var, values=action_options, width=12, state="readonly")
        cb.pack(side="left", padx=2)
        cb.bind("<<ComboboxSelected>>", lambda e: self._update_step_data(idx, "action", action_var.get(), refresh=True))

        # 입력값 표시 로직 (press_key도 값이 필요함 - 예: ENTER)
        if step["action"] in ["input", "input_password", "check_text", "check_url", "press_key"]:
            val_var = tk.StringVar(value=step["value"])
            val_var.trace("w", lambda *a: self._update_step_data(idx, "value", val_var.get()))
            
            bg_color = "#E3F2FD"
            show_char = ""
            if step["action"] == "check_text": bg_color = "#FFF3E0"
            elif step["action"] == "check_url": bg_color = "#E8F5E9"
            elif step["action"] == "press_key": bg_color = "#D1C4E9" # 보라색 (키 입력)
            elif step["action"] == "input_password": 
                bg_color = "#FFEBEE"
                show_char = "*"
            
            tk.Entry(row, textvariable=val_var, width=15, bg=bg_color, show=show_char).pack(side="left", padx=5)

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