# nimda_gui/visual_engine/transparency_manager.py

import tkinter as tk


class TransparencyManager:
    """
    Керує прозорістю вікон Tkinter.

    Примітка: Справжня прозорість віджетів у Tkinter складна.
    Цей клас керує прозорістю головного вікна.
    """

    def __init__(self, root_window):
        if not isinstance(root_window, tk.Tk):
            raise TypeError("TransparencyManager вимагає головне вікно tk.Tk.")
        self.root = root_window
        self._current_alpha = 1.0

    def set_transparency(self, alpha: float):
        """
        Встановлює прозорість головного вікна.

        :param alpha: Значення від 0.0 (повністю прозоре) до 1.0 (непрозоре).
        """
        if not (0.0 <= alpha <= 1.0):
            raise ValueError("Значення alpha має бути в діапазоні від 0.0 до 1.0")

        self._current_alpha = alpha
        try:
            # `set_alpha` - це стандартний спосіб для Windows
            # `attributes('-alpha', ...)` - для Unix-подібних систем (macOS, Linux)
            if self.root.tk.call("tk", "windowingsystem") == "win32":
                self.root.attributes("-alpha", self._current_alpha)
            else:
                # Для macOS та Linux
                self.root.attributes("-alpha", self._current_alpha)
        except tk.TclError as e:
            print(f"Помилка встановлення прозорості: {e}")
            print("Ваша система може не підтримувати прозорість вікон.")

    def get_transparency(self) -> float:
        """Повертає поточне значення прозорості."""
        return self._current_alpha

    def enable_blur(self):
        """
        Симулює ефект розмиття (blur).

        Примітка: Tkinter не має вбудованої підтримки розмиття фону.
        Ця функція є заглушкою для майбутньої реалізації з використанням
        специфічних для ОС API (наприклад, DWM для Windows, Core Animation для macOS).
        """
        print("Емуляція ефекту розмиття: Увімкнено (заглушка).")
        # Тут може бути код для виклику нативних функцій ОС
        # Наприклад, для Windows:
        # import ctypes
        # from ctypes import wintypes
        # ... (складний код для взаємодії з DWM)

    def disable_blur(self):
        """Вимикає ефект розмиття."""
        print("Емуляція ефекту розмиття: Вимкнено (заглушка).")


if __name__ == "__main__":
    # Демонстрація
    root = tk.Tk()
    root.title("TransparencyManager Demo")
    root.geometry("500x400")

    # Створюємо менеджер прозорості
    try:
        transparency_manager = TransparencyManager(root)

        label = tk.Label(
            root,
            text="Керуйте прозорістю вікна за допомогою слайдера.",
            font=("Arial", 12),
            pady=20,
        )
        label.pack()

        # Слайдер для керування прозорістю
        slider = tk.Scale(
            root,
            from_=0.0,
            to=1.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            label="Прозорість",
            command=lambda val: transparency_manager.set_transparency(float(val)),
        )
        slider.set(1.0)  # Початкове значення
        slider.pack(fill=tk.X, padx=20, pady=10)

        # Кнопки для "розмиття"
        blur_button = tk.Button(
            root,
            text="Увімкнути 'Blur' (емуляція)",
            command=transparency_manager.enable_blur,
        )
        blur_button.pack(pady=5)

        unblur_button = tk.Button(
            root,
            text="Вимкнути 'Blur' (емуляція)",
            command=transparency_manager.disable_blur,
        )
        unblur_button.pack(pady=5)

        print("TransparencyManager Demo: Використовуйте слайдер для зміни прозорості.")

    except Exception as e:
        error_label = tk.Label(root, text=f"Помилка ініціалізації: {e}", fg="red")
        error_label.pack(pady=20)
        print(f"Помилка: {e}")

    root.mainloop()
