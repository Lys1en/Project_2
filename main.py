import arcade
import os
import json
from game.constants import *


class GameWindow(arcade.Window):
    """Главное окно игры"""

    def __init__(self):
        # Загружаем настройки
        self.settings = self.load_settings()

        # Получаем разрешение из настроек
        width = self.settings.get("width", SCREEN_WIDTH)
        height = self.settings.get("height", SCREEN_HEIGHT)
        fullscreen = self.settings.get("fullscreen", False)

        # Инициализируем окно
        super().__init__(width, height, SCREEN_TITLE, fullscreen=fullscreen)

        # Сохраняем настройки
        self.settings["width"] = width
        self.settings["height"] = height
        self.settings["fullscreen"] = fullscreen
        self.save_settings()

        # Создаем необходимые директории
        for directory in ["levels", "saves"]:
            os.makedirs(directory, exist_ok=True)

    def load_settings(self):
        """Загрузка настроек из файла"""
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except:
            pass
        return {}

    def save_settings(self):
        """Сохранение настроек в файл"""
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def setup(self):
        """Настройка игры"""
        from game.views.menu_view import MenuView
        menu_view = MenuView()
        self.show_view(menu_view)


def main():
    """Точка входа в игру"""
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()