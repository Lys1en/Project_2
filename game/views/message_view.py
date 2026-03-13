import arcade
from game.constants import *


class MessageView(arcade.View):
    """Вид для отображения сообщений"""

    def __init__(self, message, parent_window=None):
        super().__init__()
        self.message = message
        self.parent_window = parent_window
        self.timer = 2.0  # 2 секунды

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        # Фон сообщения
        arcade.draw_rectangle_filled(
            center_x, center_y,
            500, 200,
            arcade.color.DARK_BLUE_GRAY
        )

        arcade.draw_rectangle_outline(
            center_x, center_y,
            500, 200,
            arcade.color.YELLOW, 3
        )

        # Разделяем сообщение на строки
        lines = self.message.split('\n')

        # Рисуем каждую строку
        for i, line in enumerate(lines):
            y_offset = (len(lines) - 1) * 20 - i * 40
            arcade.draw_text(
                line,
                center_x,
                center_y + y_offset,
                arcade.color.WHITE,
                24,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

    def on_update(self, delta_time):
        self.timer -= delta_time
        if self.timer <= 0:
            from game.views.menu_view import MenuView
            self.window.show_view(MenuView())