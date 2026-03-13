import arcade
from game.constants import *
from game.utils.level_loader import LevelLoader


class LevelSelectorView(arcade.View):
    """Выбор уровня с центрированием"""

    def __init__(self):
        super().__init__()
        self.levels = LevelLoader.get_available_levels() or ["test_level", "level1", "level2"]
        self.selected_index = 0

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        center_x = self.window.width // 2
        center_y = self.window.height // 2

        # Заголовок - вверху по центру
        arcade.draw_text(
            "ВЫБЕРИТЕ УРОВЕНЬ",
            center_x,
            self.window.height - 100,
            arcade.color.WHITE,
            min(40, self.window.width // 25),
            anchor_x="center",
            anchor_y="center"
        )

        if not self.levels:
            # Сообщение если нет уровней - по центру
            arcade.draw_text(
                "Уровни не найдены!",
                center_x,
                center_y + 50,
                arcade.color.RED,
                min(30, self.window.width // 33),
                anchor_x="center",
                anchor_y="center"
            )

            arcade.draw_text(
                "Создайте уровни в редакторе",
                center_x,
                center_y - 50,
                arcade.color.WHITE,
                min(20, self.window.width // 50),
                anchor_x="center",
                anchor_y="center"
            )
        else:
            # Список уровней - по центру экрана
            total_items = len(self.levels)
            item_height = 50
            total_height = total_items * item_height
            start_y = center_y + (total_height // 2)

            for i, level in enumerate(self.levels):
                y_pos = start_y - (i * item_height)
                color = arcade.color.YELLOW if i == self.selected_index else arcade.color.WHITE

                # Префикс выбора
                prefix = "> " if i == self.selected_index else "  "

                arcade.draw_text(
                    f"{prefix}{level}",
                    center_x,
                    y_pos,
                    color,
                    min(28, self.window.width // 36),
                    anchor_x="center",
                    anchor_y="center"
                )

        # Управление - внизу по центру
        arcade.draw_text(
            "[↑↓] Выбор | [ENTER] Играть | [ESC] Назад",
            center_x,
            60,
            arcade.color.WHITE,
            min(18, self.window.width // 55),
            anchor_x="center",
            anchor_y="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            self.window.show_view(MenuView())

        elif key == arcade.key.UP and self.levels:
            self.selected_index = (self.selected_index - 1) % len(self.levels)

        elif key == arcade.key.DOWN and self.levels:
            self.selected_index = (self.selected_index + 1) % len(self.levels)

        elif key == arcade.key.ENTER and self.levels:
            self.start_level()

    def start_level(self):
        """Запуск выбранного уровня"""
        if self.levels:
            level_name = self.levels[self.selected_index]
            from game.views.game_view import GameView
            game_view = GameView()
            game_view.setup(level_name)
            self.window.show_view(game_view)