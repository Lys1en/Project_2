import arcade
from game.constants import *


class MenuView(arcade.View):
    """Главное меню с центрированием"""

    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()
        arcade.set_background_color(BACKGROUND_COLOR)

        # Получаем центр экрана
        center_x = self.window.width // 2
        center_y = self.window.height // 2

        # Заголовок - вверху по центру
        arcade.draw_text(
            "ПЛАТФОРМЕР",
            center_x,
            self.window.height - 150,
            arcade.color.WHITE,
            min(50, self.window.width // 20),
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # Пункты меню - по центру экрана
        menu_items = [
            ("[1] НАЧАТЬ ИГРУ", 50),
            ("[2] РЕДАКТОР УРОВНЕЙ", -30),
            ("[3] НАСТРОЙКИ", -110),
        ]

        for text, offset in menu_items:
            arcade.draw_text(
                text,
                center_x,
                center_y + offset,
                arcade.color.WHITE,
                min(30, self.window.width // 33),
                anchor_x="center",
                anchor_y="center"
            )

        # Выход - внизу по центру
        arcade.draw_text(
            "[ESC] ВЫХОД",
            center_x,
            80,
            arcade.color.WHITE,
            min(25, self.window.width // 40),
            anchor_x="center",
            anchor_y="center"
        )

        # Инструкция - в самом низу
        arcade.draw_text(
            "Используйте цифры 1-3 для выбора, ESC для выхода",
            center_x,
            30,
            arcade.color.LIGHT_GRAY,
            min(16, self.window.width // 62),
            anchor_x="center",
            anchor_y="center"
        )

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш"""
        if key == arcade.key.KEY_1 or key == arcade.key.NUM_1:
            from game.views.level_select_view import LevelSelectorView
            self.window.show_view(LevelSelectorView())

        elif key == arcade.key.KEY_2 or key == arcade.key.NUM_2:
            from game.views.editor_view import LevelEditor
            self.window.show_view(LevelEditor())

        elif key == arcade.key.KEY_3 or key == arcade.key.NUM_3:
            from game.views.settings_view import SettingsView
            self.window.show_view(SettingsView())

        elif key == arcade.key.ESCAPE:
            arcade.exit()