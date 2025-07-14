#!/usr/bin/env python3
import tkinter as tk
from pathlib import Path
from tkinter import PanedWindow, Text, ttk


class NimdaGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Core Window Setup ---
        self.title("NIMDA Agent v5.0 - Interactive Command Center")
        self.geometry("1200x800")

        # --- Hacker Theme Configuration ---
        self.background_color = "#0a0a0a"
        self.foreground_color = "#00ff00"
        self.widget_bg_color = "#1a1a1a"
        self.widget_fg_color = self.foreground_color
        self.border_color = "#00ff00"
        self.accent_color = "#333333"

        self.configure(bg=self.background_color)

        # --- Transparency (Alpha Channel) ---
        self.attributes("-alpha", 0.97)

        # --- Style Configuration ---
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self._configure_styles()

        # --- Main Layout ---
        self.paned_window = PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=8)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.control_panel = self._create_control_panel(self.paned_window)
        self.main_panel = self._create_main_panel(self.paned_window)

        self.paned_window.add(self.control_panel)
        self.paned_window.add(self.main_panel)

    def _configure_styles(self):
        """Configure all custom ttk styles."""
        self.style.configure("TFrame", background=self.background_color)
        self.style.configure(
            "TLabel",
            background=self.background_color,
            foreground=self.widget_fg_color,
            font=("Courier", 12),
        )
        self.style.configure(
            "TButton",
            background=self.accent_color,
            foreground=self.widget_fg_color,
            font=("Courier", 11, "bold"),
            borderwidth=1,
            focusthickness=0,
        )
        self.style.map(
            "TButton",
            background=[("active", self.border_color)],
            foreground=[("active", self.widget_bg_color)],
        )
        self.style.configure(
            "TEntry",
            fieldbackground=self.widget_bg_color,
            foreground=self.widget_fg_color,
            insertcolor=self.widget_fg_color,
            font=("Courier", 12),
        )
        self.style.configure("TPanedWindow", background=self.border_color)
        self.style.configure("Control.TButton", padding=10, width=20)
        self.style.configure(
            "Header.TLabel", font=("Courier", 14, "bold"), foreground=self.border_color
        )

    def _create_control_panel(self, parent):
        """Creates the left-side control panel."""
        panel = ttk.Frame(parent, padding="10 20")

        # --- Dev Plan Section ---
        dev_plan_header = ttk.Label(panel, text="== DEV PLAN ==", style="Header.TLabel")
        dev_plan_header.pack(fill=tk.X, pady=10)

        load_plan_btn = ttk.Button(
            panel, text="Load Plan", command=self.load_dev_plan, style="Control.TButton"
        )
        load_plan_btn.pack(fill=tk.X, pady=5)

        save_plan_btn = ttk.Button(
            panel, text="Save Plan", command=self.save_dev_plan, style="Control.TButton"
        )
        save_plan_btn.pack(fill=tk.X, pady=5)

        # --- Modes Section ---
        modes_header = ttk.Label(panel, text="== MODES ==", style="Header.TLabel")
        modes_header.pack(fill=tk.X, pady=(20, 10))

        mode_btn_1 = ttk.Button(
            panel,
            text="Deep Creation",
            command=lambda: self.set_mode("Deep Creation"),
            style="Control.TButton",
        )
        mode_btn_1.pack(fill=tk.X, pady=5)

        mode_btn_2 = ttk.Button(
            panel,
            text="Correction",
            command=lambda: self.set_mode("Correction"),
            style="Control.TButton",
        )
        mode_btn_2.pack(fill=tk.X, pady=5)

        mode_btn_3 = ttk.Button(
            panel,
            text="Formatting",
            command=lambda: self.set_mode("Formatting"),
            style="Control.TButton",
        )
        mode_btn_3.pack(fill=tk.X, pady=5)

        # --- Execution Section ---
        exec_header = ttk.Label(panel, text="== EXECUTION ==", style="Header.TLabel")
        exec_header.pack(fill=tk.X, pady=(20, 10))

        run_workflow_btn = ttk.Button(
            panel,
            text="Run Full Workflow",
            command=lambda: self.set_mode("Run Workflow"),
            style="Control.TButton",
        )
        run_workflow_btn.pack(fill=tk.X, pady=5)

        return panel

    def _create_main_panel(self, parent):
        """Creates the right-side main content panel."""
        panel = ttk.Frame(parent, padding="10")

        # --- Title Label ---
        title_label = ttk.Label(
            panel,
            text="█▓▒░ NIMDA AGENT :: ENHANCED INTERFACE ░▒▓█",
            font=("Courier", 18, "bold"),
            foreground=self.border_color,
        )
        title_label.pack(pady=10, fill=tk.X)

        # --- Main Text Area (Console/Editor) ---
        self.main_text = Text(
            panel,
            wrap=tk.WORD,
            bg=self.widget_bg_color,
            fg=self.widget_fg_color,
            font=("Courier", 11),
            bd=1,
            relief=tk.SOLID,
            insertbackground=self.foreground_color,
            selectbackground=self.border_color,
            selectforeground=self.widget_bg_color,
        )
        self.main_text.pack(pady=10, fill=tk.BOTH, expand=True)
        self.log_message("Initializing NIMDA v5.0...")
        self.log_message("Status: All systems operational.")
        self.log_message("Awaiting commands or user action from control panel...\n")
        self.main_text.configure(state="disabled")

        # --- Command Input Area ---
        input_frame = ttk.Frame(panel)
        input_frame.pack(fill=tk.X, pady=5)

        prompt_label = ttk.Label(input_frame, text="CMD>", font=("Courier", 12, "bold"))
        prompt_label.pack(side=tk.LEFT, padx=(0, 5))

        self.command_entry = ttk.Entry(input_frame)
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.command_entry.bind("<Return>", self.process_command)

        # --- Status Bar ---
        status_bar = ttk.Frame(self, relief=tk.SUNKEN, padding="2 5")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label = ttk.Label(
            status_bar,
            text="[Core: OK] [AI: OK] [Network: OK] | Mode: Standby | Ready",
            font=("Courier", 10),
        )
        self.status_label.pack(side=tk.LEFT)

        return panel

    def log_message(self, message):
        """Appends a message to the main text area."""
        self.main_text.configure(state="normal")
        self.main_text.insert(tk.END, message + "\n")
        self.main_text.see(tk.END)
        self.main_text.configure(state="disabled")

    def load_dev_plan(self):
        """Loads DEV_PLAN_v5.md into the main text area for editing."""
        try:
            dev_plan_path = Path(__file__).parent.parent / "DEV_PLAN_v5.md"
            if dev_plan_path.exists():
                with open(dev_plan_path, "r", encoding="utf-8") as f:
                    plan_content = f.read()

                self.main_text.configure(state="normal")
                self.main_text.delete("1.0", tk.END)
                self.main_text.insert("1.0", plan_content)
                self.status_label.config(
                    text=f"Mode: Editing Dev Plan | Loaded {dev_plan_path.name}"
                )
                self.log_message("--- DEV_PLAN_v5.md loaded for editing ---")
            else:
                self.log_message(f"ERROR: DEV_PLAN_v5.md not found at {dev_plan_path}")
        except Exception as e:
            self.log_message(f"ERROR loading dev plan: {e}")

    def save_dev_plan(self):
        """Saves the content of the main text area back to DEV_PLAN_v5.md."""
        try:
            dev_plan_path = Path(__file__).parent.parent / "DEV_PLAN_v5.md"
            content_to_save = self.main_text.get("1.0", tk.END)

            with open(dev_plan_path, "w", encoding="utf-8") as f:
                f.write(content_to_save)

            self.status_label.config(
                text="Mode: Standby | Dev Plan saved successfully."
            )
            self.log_message("--- DEV_PLAN_v5.md saved successfully ---")
            self.main_text.configure(state="disabled")
        except Exception as e:
            self.log_message(f"ERROR saving dev plan: {e}")

    def set_mode(self, mode_name):
        """Sets the agent's operational mode."""
        self.status_label.config(text=f"Mode: {mode_name} | Ready")
        self.log_message(f"--- Mode changed to: {mode_name} ---")
        # Placeholder for actual mode change logic
        if mode_name == "Run Workflow":
            self.log_message("Executing main workflow... (simulation)")
            # In a real scenario, this would trigger a complex background task.

    def process_command(self, event=None):
        command = self.command_entry.get()
        if command:
            self.main_text.configure(state="normal")
            self.main_text.insert(tk.END, f"> {command}\n")

            # Mock response
            response = f"Executing '{command}'... Done.\n"
            self.main_text.insert(tk.END, response)

            self.main_text.see(tk.END)  # Scroll to the end
            self.main_text.configure(state="disabled")
            self.command_entry.delete(0, tk.END)


if __name__ == "__main__":
    app = NimdaGUI()
    app.mainloop()
