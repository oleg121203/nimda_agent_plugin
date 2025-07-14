# nimda_gui/visual_engine/neon_effect_engine.py

import math
import time
import tkinter as tk
from tkinter import ttk


class NeonEffectEngine:
    """
    Реалізує динамічні неонові ефекти для віджетів Tkinter.
    """

    def __init__(self, widget, color="cyan"):
        self.widget = widget
        self.color = color
        self.canvas = self.widget.master
        self.glow_items = []
        self.is_glowing = False
        self.animation_job = None

        self.widget.bind("<Enter>", self.start_glow)
        self.widget.bind("<Leave>", self.stop_glow)

    def _get_widget_bbox(self):
        """Отримує bounding box віджета."""
        x, y = self.widget.winfo_x(), self.widget.winfo_y()
        width, height = self.widget.winfo_width(), self.widget.winfo_height()
        return x, y, x + width, y + height

    def _create_glow(self, bbox, step, max_steps):
        """Створює один шар світіння."""
        x1, y1, x2, y2 = bbox

        # Розрахунок прозорості
        alpha = 1.0 - (step / max_steps)
        hex_alpha = f"{int(alpha * 255):02x}"

        # Створення кольору з прозорістю (не працює нативно в Tkinter, але для логіки)
        glow_color = f"#{hex_alpha}{self.color[1:]}"  # Fake transparency

        # Для реального ефекту, ми створюємо декілька прямокутників
        # зі злегка зміненими кольорами для імітації світіння.
        r, g, b = self.canvas.winfo_rgb(self.color)

        # Зменшуємо інтенсивність кольору для зовнішніх шарів
        intensity_factor = 1.0 - (step / (max_steps * 1.5))
        r = int(r / 65535 * 255 * intensity_factor)
        g = int(g / 65535 * 255 * intensity_factor)
        b = int(b / 65535 * 255 * intensity_factor)

        glow_color = f"#{r:02x}{g:02x}{b:02x}"

        # Розширюємо прямокутник для кожного шару світіння
        glow_x1 = x1 - step * 2
        glow_y1 = y1 - step * 2
        glow_x2 = x2 + step * 2
        glow_y2 = y2 + step * 2

        glow_item = self.canvas.create_rectangle(
            glow_x1,
            glow_y1,
            glow_x2,
            glow_y2,
            outline=glow_color,
            width=2,
            tags="neon_glow",
        )
        return glow_item

    def start_glow(self, event=None):
        """Починає анімацію світіння."""
        if self.is_glowing:
            return
        self.is_glowing = True
        self._animate_glow()

    def stop_glow(self, event=None):
        """Зупиняє анімацію світіння."""
        if not self.is_glowing:
            return
        self.is_glowing = False
        if self.animation_job:
            self.canvas.after_cancel(self.animation_job)
            self.animation_job = None
        self.clear_glow()

    def clear_glow(self):
        """Видаляє всі елементи світіння."""
        self.canvas.delete("neon_glow")
        self.glow_items.clear()

    def _animate_glow(self):
        """Цикл анімації для пульсуючого ефекту."""
        if not self.is_glowing:
            return

        self.clear_glow()

        bbox = self._get_widget_bbox()
        if (
            bbox[2] - bbox[0] <= 1 or bbox[3] - bbox[1] <= 1
        ):  # віджет ще не намальований
            self.animation_job = self.canvas.after(50, self._animate_glow)
            return

        # Використовуємо синусоїду для пульсації
        t = time.time() * 3
        max_steps = 5 + int(2 * math.sin(t))  # Пульсація від 3 до 7 шарів

        for step in range(1, max_steps):
            glow_item = self._create_glow(bbox, step, max_steps)
            self.glow_items.append(glow_item)

        # Піднімаємо віджет на передній план
        self.canvas.tag_raise(self.widget)

        self.animation_job = self.canvas.after(50, self._animate_glow)


if __name__ == "__main__":
    # Демонстрація
    root = tk.Tk()
    root.title("NeonEffectEngine Demo")
    root.geometry("400x300")
    root.configure(bg="black")

    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Створюємо кнопку, яку будемо підсвічувати
    style = ttk.Style()
    style.configure(
        "TButton", padding=6, relief="flat", background="#333", foreground="cyan"
    )

    # Важливо: для того, щоб розмістити кнопку на Canvas,
    # ми створюємо її як дочірній елемент Canvas
    button = ttk.Button(canvas, text="Наведи на мене!")

    # Розміщуємо кнопку на Canvas
    canvas.create_window(200, 150, window=button)

    # Ініціалізуємо рушій неонового ефекту
    neon_engine = NeonEffectEngine(button, color="cyan")

    print("NeonEffectEngine Demo: Наведіть курсор на кнопку, щоб побачити ефект.")

    root.mainloop()
