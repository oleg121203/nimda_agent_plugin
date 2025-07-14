# nimda_gui/visual_engine/dark_theme_engine.py

import tkinter as tk
from tkinter import ttk


class DarkThemeEngine:
    """
    Застосовує професійну темну тему до віджетів Tkinter.
    """

    def __init__(self, root):
        self.root = root
        self.style = ttk.Style(self.root)
        self.themes = {
            "HackerNeon": {
                "bg": "#0a0a0a",
                "fg": "#00ff7f",  # SpringGreen
                "select_bg": "#008080",  # Teal
                "select_fg": "#ffffff",
                "button_bg": "#2a2a2a",
                "button_fg": "#00ff7f",
                "button_active_bg": "#3a3a3a",
                "entry_bg": "#1c1c1c",
                "entry_fg": "#e0e0e0",
                "font": ("Consolas", 10),
            },
            "CyberPunk": {
                "bg": "#0d0221",
                "fg": "#ff00ff",  # Magenta
                "select_bg": "#f9f871",  # Yellow
                "select_fg": "#0d0221",
                "button_bg": "#261a3b",
                "button_fg": "#ff00ff",
                "button_active_bg": "#3c2c5c",
                "entry_bg": "#1a112a",
                "entry_fg": "#f0f0f0",
                "font": ("Cyber", 11),  # Потрібно встановити шрифт
            },
        }

    def apply_theme(self, theme_name="HackerNeon"):
        """
        Застосовує вибрану тему.

        :param theme_name: Назва теми ("HackerNeon" або "CyberPunk").
        """
        if theme_name not in self.themes:
            raise ValueError(f"Тема '{theme_name}' не знайдена.")

        theme = self.themes[theme_name]

        # Налаштування стилю ttk
        self.style.theme_use("clam")  # 'clam', 'alt', 'default', 'classic'

        # Загальні налаштування
        self.root.configure(bg=theme["bg"])
        self.style.configure(
            ".",
            background=theme["bg"],
            foreground=theme["fg"],
            font=theme["font"],
            fieldbackground=theme["entry_bg"],
            troughcolor=theme["button_bg"],
        )

        # Налаштування для кнопок
        self.style.configure(
            "TButton",
            background=theme["button_bg"],
            foreground=theme["button_fg"],
            font=theme["font"],
            borderwidth=0,
            focuscolor=theme["select_bg"],
        )
        self.style.map(
            "TButton",
            background=[("active", theme["button_active_bg"])],
            foreground=[("active", theme["fg"])],
        )

        # Налаштування для міток
        self.style.configure(
            "TLabel", background=theme["bg"], foreground=theme["fg"], font=theme["font"]
        )

        # Налаштування для полів вводу
        self.style.configure(
            "TEntry",
            fieldbackground=theme["entry_bg"],
            foreground=theme["entry_fg"],
            insertcolor=theme["fg"],
            font=theme["font"],
        )

        # Налаштування для рамок
        self.style.configure("TFrame", background=theme["bg"])

        # Налаштування для Checkbutton
        self.style.configure(
            "TCheckbutton",
            background=theme["bg"],
            foreground=theme["fg"],
            indicatorcolor=theme["button_bg"],
            font=theme["font"],
        )
        self.style.map(
            "TCheckbutton", indicatorcolor=[("selected", theme["select_bg"])]
        )

        print(f"Тема '{theme_name}' успішно застосована.")


if __name__ == "__main__":
    # Демонстрація
    root = tk.Tk()
    root.title("DarkThemeEngine Demo")
    root.geometry("500x400")

    theme_engine = DarkThemeEngine(root)

    # --- Панель керування темою ---
    control_frame = ttk.Frame(root, padding=10)
    control_frame.pack(side="top", fill="x")

    theme_var = tk.StringVar(value="HackerNeon")

    def on_theme_change(*args):
        try:
            theme_engine.apply_theme(theme_var.get())
        except ValueError as e:
            print(e)

    theme_var.trace_add("write", on_theme_change)

    ttk.Label(control_frame, text="Виберіть тему:").pack(side="left", padx=5)

    hacker_radio = ttk.Radiobutton(
        control_frame, text="HackerNeon", variable=theme_var, value="HackerNeon"
    )
    hacker_radio.pack(side="left")

    cyber_radio = ttk.Radiobutton(
        control_frame, text="CyberPunk", variable=theme_var, value="CyberPunk"
    )
    cyber_radio.pack(side="left")

    # --- Демонстраційні віджети ---
    demo_frame = ttk.Frame(root, padding=20)
    demo_frame.pack(expand=True, fill="both")

    ttk.Label(demo_frame, text="Це мітка (Label)").pack(pady=5)

    ttk.Entry(demo_frame).pack(pady=5, fill="x", padx=20)

    ttk.Button(demo_frame, text="Це кнопка (Button)").pack(pady=10)

    ttk.Checkbutton(demo_frame, text="Це Checkbox").pack(pady=5)

    # Застосовуємо початкову тему
    theme_engine.apply_theme("HackerNeon")

    root.mainloop()
