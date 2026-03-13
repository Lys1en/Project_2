import arcade


class Player:
    """Класс игрока с поддержкой масштабирования"""

    def __init__(self, scale=1.0):
        # Фиксированный цвет игрока (синий)
        self.color = arcade.color.BLUE

        # Базовые размеры (при масштабе 1.0)
        self.base_width = 40
        self.base_height = 40

        # Масштабированные размеры
        self.scale = scale
        self.width = int(self.base_width * scale)
        self.height = int(self.base_height * scale)

        # Позиция (будет установлена позже)
        self.center_x = 0
        self.center_y = 0

        # Физика
        self.change_x = 0
        self.change_y = 0

        # Статистика
        self.score = 0
        self.health = 100

    def set_position(self, x, y):
        """Установка позиции игрока"""
        self.center_x = x
        self.center_y = y

    def draw(self):
        """Рисование игрока"""
        # Используем универсальную функцию
        self.draw_rectangle(
            self.center_x, self.center_y,
            self.width, self.height,
            self.color, arcade.color.WHITE, max(2, int(2 * self.scale))
        )

    @staticmethod
    def draw_rectangle(center_x, center_y, width, height, fill_color, border_color=None, border_width=2):
        """Универсальная функция рисования прямоугольника"""
        # Вычисляем левый нижний угол для lbwh
        left = center_x - width / 2
        bottom = center_y - height / 2

        try:
            # Рисуем заливку
            arcade.draw_lbwh_rectangle_filled(left, bottom, width, height, fill_color)

            # Рисуем обводку если нужно
            if border_color:
                arcade.draw_lbwh_rectangle_outline(left, bottom, width, height, border_color, border_width)
        except:
            # Запасной вариант
            try:
                arcade.draw_rectangle_filled(center_x, center_y, width, height, fill_color)
                if border_color:
                    arcade.draw_rectangle_outline(center_x, center_y, width, height, border_color, border_width)
            except:
                # Рисуем как полигон
                half_w = width / 2
                half_h = height / 2
                points = [
                    (center_x - half_w, center_y - half_h),
                    (center_x + half_w, center_y - half_h),
                    (center_x + half_w, center_y + half_h),
                    (center_x - half_w, center_y + half_h)
                ]
                arcade.draw_polygon_filled(points, fill_color)
                if border_color:
                    arcade.draw_polygon_outline(points, border_color, border_width)
