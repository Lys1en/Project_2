import arcade
import json
import os
from game.constants import *


class SettingsView(arcade.View):
    """Экран настроек разрешения"""

    def __init__(self):
        super().__init__()

        # Загружаем настройки
        self.settings = self.load_settings()
        self.current_resolution = self.settings.get("resolution_index", DEFAULT_RESOLUTION_INDEX)
        self.fullscreen = self.settings.get("fullscreen", False)

        # Текущий выбранный пункт
        self.selected_item = 0  # 0=разрешение, 1=полноэкранный, 2=применить, 3=назад

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
            self.settings["resolution_index"] = self.current_resolution
            self.settings["fullscreen"] = self.fullscreen
            width, height, _ = RESOLUTIONS[self.current_resolution]
            self.settings["width"] = width
            self.settings["height"] = height

            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        center_x = self.window.width // 2
        center_y = self.window.height // 2

        # Заголовок
        arcade.draw_text(
            "НАСТРОЙКИ",
            center_x,
            self.window.height - 100,
            arcade.color.WHITE,
            min(40, self.window.width // 25),
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # Текущее разрешение для информации
        current_width, current_height, _ = RESOLUTIONS[self.current_resolution]
        resolution_text = f"{current_width}x{current_height}"

        # Позиции элементов (все по центру)
        item_height = 60
        start_y = center_y + 40

        # 1. Разрешение экрана
        color = arcade.color.YELLOW if self.selected_item == 0 else arcade.color.WHITE
        arcade.draw_text(
            f"Разрешение: {resolution_text}",
            center_x, start_y,
            color, min(28, self.window.width // 36),
            anchor_x="center", anchor_y="center"
        )

        # 2. Полноэкранный режим
        fs_text = "ВКЛ" if self.fullscreen else "ВЫКЛ"
        color = arcade.color.YELLOW if self.selected_item == 1 else arcade.color.WHITE
        arcade.draw_text(
            f"Полноэкранный: {fs_text}",
            center_x, start_y - item_height,
            color, min(28, self.window.width // 36),
            anchor_x="center", anchor_y="center"
        )

        # 3. Применить настройки
        color = arcade.color.YELLOW if self.selected_item == 2 else arcade.color.WHITE
        arcade.draw_text(
            "ПРИМЕНИТЬ НАСТРОЙКИ",
            center_x, start_y - item_height * 2,
            color, min(28, self.window.width // 36),
            anchor_x="center", anchor_y="center"
        )

        # 4. Назад в меню
        color = arcade.color.YELLOW if self.selected_item == 3 else arcade.color.WHITE
        arcade.draw_text(
            "НАЗАД В МЕНЮ",
            center_x, start_y - item_height * 3,
            color, min(28, self.window.width // 36),
            anchor_x="center", anchor_y="center"
        )

        # Информация о настройках
        arcade.draw_text(
            f"Текущие настройки: {current_width}x{current_height}, Полноэкранный: {fs_text}",
            center_x, 100,
            arcade.color.LIGHT_GRAY, min(18, self.window.width // 55),
            anchor_x="center", anchor_y="center"
        )

        # Управление
        arcade.draw_text(
            "↑↓: Выбор  ←→: Изменить  ENTER: Подтвердить  ESC: Назад",
            center_x, 50,
            arcade.color.LIGHT_GRAY, min(14, self.window.width // 71),
            anchor_x="center", anchor_y="center"
        )

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш"""
        if key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            self.window.show_view(MenuView())

        elif key == arcade.key.UP:
            self.selected_item = (self.selected_item - 1) % 4

        elif key == arcade.key.DOWN:
            self.selected_item = (self.selected_item + 1) % 4

        elif key == arcade.key.LEFT:
            if self.selected_item == 0:
                self.current_resolution = (self.current_resolution - 1) % len(RESOLUTIONS)
            elif self.selected_item == 1:
                self.fullscreen = not self.fullscreen

        elif key == arcade.key.RIGHT:
            if self.selected_item == 0:
                self.current_resolution = (self.current_resolution + 1) % len(RESOLUTIONS)
            elif self.selected_item == 1:
                self.fullscreen = not self.fullscreen

        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            if self.selected_item == 2:  # Применить настройки
                self.apply_settings()
            elif self.selected_item == 3:  # Назад в меню
                from game.views.menu_view import MenuView
                self.window.show_view(MenuView())

    def apply_settings(self):
        """Применение новых настроек"""
        # Сохраняем настройки
        self.save_settings()

        # Получаем новое разрешение
        new_width, new_height, _ = RESOLUTIONS[self.current_resolution]

        try:
            # Если сейчас полноэкранный режим - сначала выходим из него
            if self.window.fullscreen:
                self.window.set_fullscreen(False)
                # Даем окну время на обработку
                import time
                time.sleep(0.1)

            # Меняем размер окна
            self.window.set_size(new_width, new_height)

            # Если нужно - включаем полноэкранный режим
            if self.fullscreen:
                # Небольшая задержка перед включением полноэкранного режима
                import time
                time.sleep(0.1)
                self.window.set_fullscreen(True)

            # Центрируем окно если не в полноэкранном режиме
            if not self.fullscreen:
                try:
                    self.window.center_window()
                except:
                    pass

            print(f"Настройки применены: {new_width}x{new_height}, полноэкранный: {self.fullscreen}")

        except Exception as e:
            print(f"Ошибка применения настроек: {e}")
            # В случае ошибки возвращаемся в меню
            from game.views.menu_view import MenuView
            self.window.show_view(MenuView())