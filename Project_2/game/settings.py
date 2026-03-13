"""
Настройки игры: разрешение и полноэкранный режим
"""

import json
import os


class GameSettings:
    """Класс для управления настройками игры"""

    # Доступные разрешения
    AVAILABLE_RESOLUTIONS = [
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1366, 768),
        (1600, 900),
        (1920, 1080),
    ]

    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 768
        self.fullscreen = False
        self.current_resolution_index = 1  # 1024x768 по умолчанию
        self.load_settings()

    def load_settings(self):
        """Загрузка настроек из файла"""
        try:
            if os.path.exists("saves/settings.json"):
                with open("saves/settings.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.screen_width = data.get("screen_width", 1024)
                    self.screen_height = data.get("screen_height", 768)
                    self.fullscreen = data.get("fullscreen", False)

                    # Находим индекс текущего разрешения
                    for i, (w, h) in enumerate(self.AVAILABLE_RESOLUTIONS):
                        if w == self.screen_width and h == self.screen_height:
                            self.current_resolution_index = i
                            break
        except:
            pass

    def save_settings(self):
        """Сохранение настроек в файл"""
        try:
            os.makedirs("saves", exist_ok=True)
            data = {
                "screen_width": self.screen_width,
                "screen_height": self.screen_height,
                "fullscreen": self.fullscreen
            }
            with open("saves/settings.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def next_resolution(self):
        """Следующее разрешение"""
        self.current_resolution_index = (self.current_resolution_index + 1) % len(self.AVAILABLE_RESOLUTIONS)
        self.screen_width, self.screen_height = self.AVAILABLE_RESOLUTIONS[self.current_resolution_index]
        return self.screen_width, self.screen_height

    def previous_resolution(self):
        """Предыдущее разрешение"""
        self.current_resolution_index = (self.current_resolution_index - 1) % len(self.AVAILABLE_RESOLUTIONS)
        self.screen_width, self.screen_height = self.AVAILABLE_RESOLUTIONS[self.current_resolution_index]
        return self.screen_width, self.screen_height

    def toggle_fullscreen(self):
        """Переключение полноэкранного режима"""
        self.fullscreen = not self.fullscreen
        return self.fullscreen

    def get_resolution_text(self):
        """Текст текущего разрешения"""
        return f"{self.screen_width} × {self.screen_height}"

    def get_fullscreen_text(self):
        """Текст полноэкранного режима"""
        return "ВКЛ" if self.fullscreen else "ВЫКЛ"


# Глобальный объект настроек
game_settings = GameSettings()