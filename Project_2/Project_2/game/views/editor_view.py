import arcade
import json
import os
from game.constants import *


class LevelEditor(arcade.View):
    """Редактор уровней с адаптивной сеткой"""

    def __init__(self):
        super().__init__()

        # Адаптивная сетка (зависит от разрешения)
        self.grid_size = self.calculate_grid_size()
        self.selected_tile = "platform"
        self.tiles = []
        self.coins = []

        # Стартовая позиция по центру
        self.player_start = (self.window.width // 2, 200) if hasattr(self, 'window') else (500, 200)

    def calculate_grid_size(self):
        """Рассчитываем размер сетки в зависимости от разрешения"""
        if hasattr(self, 'window'):
            # Базовый размер сетки, адаптируемый под разрешение
            base_size = 64
            min_size = 32
            max_size = 96

            # Масштабируем в зависимости от ширины экрана
            screen_width = self.window.width
            scale = screen_width / 1280  # 1280 - базовое разрешение

            grid_size = int(base_size * scale)
            grid_size = max(min_size, min(grid_size, max_size))

            # Округляем до ближайшего четного числа для ровной сетки
            grid_size = (grid_size // 2) * 2

            return grid_size
        return 64

    def draw_rectangle_filled(self, center_x, center_y, width, height, color):
        """Рисование прямоугольника по центру"""
        left = center_x - width / 2
        bottom = center_y - height / 2
        arcade.draw_lbwh_rectangle_filled(left, bottom, width, height, color)

    def draw_rectangle_outline(self, center_x, center_y, width, height, color, border_width=1):
        """Рисование контура прямоугольника по центру"""
        left = center_x - width / 2
        bottom = center_y - height / 2
        arcade.draw_lbwh_rectangle_outline(left, bottom, width, height, color, border_width)

    def on_show(self):
        """Вызывается при показе редактора"""
        # Пересчитываем размер сетки при каждом показе
        self.grid_size = self.calculate_grid_size()

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_GRAY)

        center_x = self.window.width // 2
        center_y = self.window.height // 2

        # Сетка по всему экрану
        for x in range(0, self.window.width, self.grid_size):
            arcade.draw_line(x, 0, x, self.window.height, arcade.color.GRAY, 1)
        for y in range(0, self.window.height, self.grid_size):
            arcade.draw_line(0, y, self.window.width, y, arcade.color.GRAY, 1)

        # Платформы
        for x, y in self.tiles:
            self.draw_rectangle_filled(x, y, self.grid_size, self.grid_size, arcade.color.GREEN)
            self.draw_rectangle_outline(x, y, self.grid_size, self.grid_size, arcade.color.DARK_GREEN, 2)

        # Монеты
        for x, y in self.coins:
            coin_size = self.grid_size * 0.6
            arcade.draw_circle_filled(x, y, coin_size / 2, arcade.color.YELLOW)
            arcade.draw_circle_outline(x, y, coin_size / 2, arcade.color.GOLD, 2)

        # Старт игрока
        player_size = self.grid_size * 0.8
        arcade.draw_circle_filled(self.player_start[0], self.player_start[1], player_size / 2, arcade.color.RED)
        arcade.draw_circle_outline(self.player_start[0], self.player_start[1], player_size / 2, arcade.color.WHITE, 2)

        # GUI - адаптивный интерфейс
        screen_width = self.window.width
        screen_height = self.window.height

        # Размер шрифта в зависимости от разрешения
        title_size = max(24, min(36, screen_width // 40))
        normal_size = max(16, min(24, screen_width // 60))
        small_size = max(12, min(18, screen_width // 80))

        # Заголовок
        arcade.draw_text(
            "РЕДАКТОР УРОВНЕЙ",
            center_x,
            screen_height - 50,
            arcade.color.WHITE,
            title_size,
            anchor_x="center",
            anchor_y="center"
        )

        # Инструменты
        arcade.draw_text(
            "[P] Платформа  [C] Монета  [S] Старт",
            center_x,
            screen_height - 100,
            arcade.color.WHITE,
            normal_size,
            anchor_x="center",
            anchor_y="center"
        )

        # Управление
        arcade.draw_text(
            "[LMB] Добавить  [RMB] Удалить  [DEL] Очистить",
            center_x,
            screen_height - 140,
            arcade.color.WHITE,
            small_size,
            anchor_x="center",
            anchor_y="center"
        )

        # Сохранение/загрузка
        arcade.draw_text(
            "[ESC] Меню  [F1] Сохранить  [F2] Загрузить",
            center_x,
            40,
            arcade.color.WHITE,
            normal_size,
            anchor_x="center",
            anchor_y="center"
        )

        # Статус
        arcade.draw_text(
            f"Инструмент: {self.selected_tile.upper()}",
            center_x,
            80,
            arcade.color.YELLOW,
            normal_size,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            f"Платформ: {len(self.tiles)}  Монет: {len(self.coins)}",
            center_x,
            110,
            arcade.color.WHITE,
            small_size,
            anchor_x="center",
            anchor_y="center"
        )

        # Размер сетки
        arcade.draw_text(
            f"Размер сетки: {self.grid_size}px",
            center_x,
            140,
            arcade.color.LIGHT_GRAY,
            small_size,
            anchor_x="center",
            anchor_y="center"
        )

    def snap_to_grid(self, x, y):
        """Привязка к сетке"""
        grid_x = (x // self.grid_size) * self.grid_size + self.grid_size // 2
        grid_y = (y // self.grid_size) * self.grid_size + self.grid_size // 2
        return grid_x, grid_y

    def on_mouse_press(self, x, y, button, modifiers):
        grid_x, grid_y = self.snap_to_grid(x, y)

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.selected_tile == "platform":
                if (grid_x, grid_y) not in self.tiles:
                    self.tiles.append((grid_x, grid_y))
            elif self.selected_tile == "coin":
                if (grid_x, grid_y) not in self.coins:
                    self.coins.append((grid_x, grid_y))
            elif self.selected_tile == "start":
                self.player_start = (grid_x, grid_y)

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if self.selected_tile == "platform":
                self.tiles = [pos for pos in self.tiles if pos != (grid_x, grid_y)]
            elif self.selected_tile == "coin":
                self.coins = [pos for pos in self.coins if pos != (grid_x, grid_y)]

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self.selected_tile = "platform"
        elif key == arcade.key.C:
            self.selected_tile = "coin"
        elif key == arcade.key.S:
            self.selected_tile = "start"

        elif key == arcade.key.DELETE:
            if self.selected_tile == "platform":
                self.tiles.clear()
            elif self.selected_tile == "coin":
                self.coins.clear()

        elif key == arcade.key.F1:
            self.save_level()

        elif key == arcade.key.F2:
            self.load_level_dialog()

        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            self.window.show_view(MenuView())

    def save_level(self):
        """Сохранение уровня"""
        if not (self.tiles or self.coins):
            print("Уровень пустой, нечего сохранять!")
            return

        print("\n" + "=" * 50)
        print("СОХРАНЕНИЕ УРОВНЯ")
        print("=" * 50)

        if os.path.exists(LEVELS_DIR):
            levels = [f[:-5] for f in os.listdir(LEVELS_DIR) if f.endswith(".json")]
            if levels:
                print("Существующие уровни:")
                for level in levels:
                    print(f"  - {level}")

        level_name = input("Введите название уровня: ").strip()

        if not level_name:
            print("Сохранение отменено")
            return

        # Сохраняем относительные координаты (в процентах от ширины/высоты)
        screen_width = self.window.width
        screen_height = self.window.height

        level_data = {
            "name": level_name,
            "screen_width": screen_width,
            "screen_height": screen_height,
            "grid_size": self.grid_size,
            "platforms": [
                {
                    "x_rel": x / screen_width,  # Относительная позиция по X
                    "y_rel": y / screen_height,  # Относительная позиция по Y
                    "width_rel": self.grid_size / screen_width,
                    "height_rel": self.grid_size / screen_height
                }
                for x, y in self.tiles
            ],
            "coins": [
                {
                    "x_rel": x / screen_width,
                    "y_rel": y / screen_height
                }
                for x, y in self.coins
            ],
            "player_start": {
                "x_rel": self.player_start[0] / screen_width,
                "y_rel": self.player_start[1] / screen_height
            }
        }

        os.makedirs(LEVELS_DIR, exist_ok=True)
        filename = os.path.join(LEVELS_DIR, f"{level_name}.json")

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(level_data, f, indent=2)
            print(f"Уровень сохранен: {filename}")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_level_dialog(self):
        """Загрузка уровня"""
        if not os.path.exists(LEVELS_DIR):
            print("Папка levels не существует!")
            return

        levels = [f[:-5] for f in os.listdir(LEVELS_DIR) if f.endswith(".json")]

        if not levels:
            print("Нет сохраненных уровней!")
            return

        print("\n" + "=" * 50)
        print("ЗАГРУЗКА УРОВНЯ")
        print("=" * 50)
        print("Доступные уровни:")

        for i, level in enumerate(levels, 1):
            print(f"{i}. {level}")

        try:
            choice = input("\nВведите номер уровня: ").strip()
            index = int(choice) - 1

            if 0 <= index < len(levels):
                self.load_level(levels[index])
                print(f"Уровень загружен: {levels[index]}")
            else:
                print("Неверный номер!")
        except (ValueError, EOFError):
            print("Загрузка отменена")

    def load_level(self, level_name):
        """Загрузка уровня из файла"""
        filename = os.path.join(LEVELS_DIR, f"{level_name}.json")

        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Получаем текущие размеры экрана
            screen_width = self.window.width
            screen_height = self.window.height

            # Конвертируем относительные координаты в абсолютные
            self.tiles = []
            for platform in data.get("platforms", []):
                x = int(platform["x_rel"] * screen_width)
                y = int(platform["y_rel"] * screen_height)
                self.tiles.append((x, y))

            self.coins = []
            for coin in data.get("coins", []):
                x = int(coin["x_rel"] * screen_width)
                y = int(coin["y_rel"] * screen_height)
                self.coins.append((x, y))

            if "player_start" in data:
                x = int(data["player_start"]["x_rel"] * screen_width)
                y = int(data["player_start"]["y_rel"] * screen_height)
                self.player_start = (x, y)

            # Обновляем размер сетки если есть в данных
            if "grid_size" in data:
                self.grid_size = data["grid_size"]

        except Exception as e:
            print(f"Ошибка загрузки: {e}")