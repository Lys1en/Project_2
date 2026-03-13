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
        # Размер уровня (для сохранения/загрузки)
        self.world_width = 3000
        self.world_height = 900
        # Смещение камеры редактора (панорамирование)
        self.view_offset_x = 0
        self.view_offset_y = 0
        # Флаги для плавного панорамирования при удержании клавиш
        self.pan_left = False
        self.pan_right = False
        self.pan_up = False
        self.pan_down = False
        # Точка финиша
        self.finish_pos = None

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
        start_x = - (self.view_offset_x % self.grid_size)
        start_y = - (self.view_offset_y % self.grid_size)
        for x in range(int(start_x), self.window.width, self.grid_size):
            arcade.draw_line(x, 0, x, self.window.height, arcade.color.GRAY, 1)
        for y in range(int(start_y), self.window.height, self.grid_size):
            arcade.draw_line(0, y, self.window.width, y, arcade.color.GRAY, 1)

        # Платформы
        for x, y in self.tiles:
            sx = x - self.view_offset_x
            sy = y - self.view_offset_y
            self.draw_rectangle_filled(sx, sy, self.grid_size, self.grid_size, arcade.color.GREEN)
            self.draw_rectangle_outline(sx, sy, self.grid_size, self.grid_size, arcade.color.DARK_GREEN, 2)

        # Монеты
        for x, y in self.coins:
            coin_size = self.grid_size * 0.6
            sx = x - self.view_offset_x
            sy = y - self.view_offset_y
            arcade.draw_circle_filled(sx, sy, coin_size / 2, arcade.color.YELLOW)
            arcade.draw_circle_outline(sx, sy, coin_size / 2, arcade.color.GOLD, 2)

        # Старт игрока
        player_size = self.grid_size * 0.8
        psx = self.player_start[0] - self.view_offset_x
        psy = self.player_start[1] - self.view_offset_y
        arcade.draw_circle_filled(psx, psy, player_size / 2, arcade.color.RED)
        arcade.draw_circle_outline(psx, psy, player_size / 2, arcade.color.WHITE, 2)

        # Финиш
        if self.finish_pos:
            fx = self.finish_pos[0] - self.view_offset_x
            fy = self.finish_pos[1] - self.view_offset_y
            width = self.grid_size
            height = int(self.grid_size * 1.5)
            self.draw_rectangle_filled(fx, fy, width, height, arcade.color.RED)
            self.draw_rectangle_outline(fx, fy, width, height, arcade.color.WHITE, 2)

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
            "[P] Платформа  [C] Монета  [S] Старт  [F] Финиш",
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

        # Размер уровня
        arcade.draw_text(
            f"Размер уровня: {self.world_width} x {self.world_height}  [- / + ширина | < / > высота]",
            center_x,
            170,
            arcade.color.ORANGE,
            small_size,
            anchor_x="center",
            anchor_y="center"
        )

        # Смещение камеры
        arcade.draw_text(
            f"Смещение: ({self.view_offset_x}, {self.view_offset_y})  Стрелки/WASD — панорамирование",
            center_x,
            200,
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
        # Переводим экранные координаты в мировые с учетом смещения камеры
        world_x = x + self.view_offset_x
        world_y = y + self.view_offset_y
        grid_x, grid_y = self.snap_to_grid(world_x, world_y)

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.selected_tile == "platform":
                if (grid_x, grid_y) not in self.tiles:
                    self.tiles.append((grid_x, grid_y))
            elif self.selected_tile == "coin":
                if (grid_x, grid_y) not in self.coins:
                    self.coins.append((grid_x, grid_y))
            elif self.selected_tile == "start":
                self.player_start = (grid_x, grid_y)
            elif self.selected_tile == "finish":
                self.finish_pos = (grid_x, grid_y)

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if self.selected_tile == "platform":
                self.tiles = [pos for pos in self.tiles if pos != (grid_x, grid_y)]
            elif self.selected_tile == "coin":
                self.coins = [pos for pos in self.coins if pos != (grid_x, grid_y)]
            elif self.selected_tile == "finish":
                self.finish_pos = None

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self.selected_tile = "platform"
        elif key == arcade.key.C:
            self.selected_tile = "coin"
        elif key == arcade.key.S:
            self.selected_tile = "start"
        elif key == arcade.key.F:
            self.selected_tile = "finish"

        elif key == arcade.key.DELETE:
            if self.selected_tile == "platform":
                self.tiles.clear()
            elif self.selected_tile == "coin":
                self.coins.clear()

        # Изменение размеров уровня
        elif key == arcade.key.MINUS:        # -
            self.world_width = max(500, self.world_width - 200)
        elif key == arcade.key.EQUAL:        # +
            self.world_width += 200
        elif key == arcade.key.COMMA:         # <
            self.world_height = max(400, self.world_height - 100)
        elif key == arcade.key.PERIOD:        # >
            self.world_height += 100

        # Панорамирование камеры (удержание клавиш)
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.pan_left = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.pan_right = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.pan_up = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.pan_down = True

        elif key == arcade.key.F1:
            self.save_level()

        elif key == arcade.key.F2:
            self.load_level_dialog()

        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            self.window.show_view(MenuView())

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.pan_left = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.pan_right = False
        elif key in (arcade.key.UP, arcade.key.W):
            self.pan_up = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.pan_down = False

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
            "world_width": self.world_width,
            "world_height": self.world_height,
            "finish": (
                {
                    "x_rel": self.finish_pos[0] / self.world_width,
                    "y_rel": self.finish_pos[1] / self.world_height
                } if self.finish_pos else None
            ),
            "platforms": [
                {
                    "x_rel": x / self.world_width,   # Относительная позиция по X
                    "y_rel": y / self.world_height,  # Относительная позиция по Y
                    "width_rel": self.grid_size / self.world_width,
                    "height_rel": self.grid_size / self.world_height
                }
                for x, y in self.tiles
            ],
            "coins": [
                {
                    "x_rel": x / self.world_width,
                    "y_rel": y / self.world_height
                }
                for x, y in self.coins
            ],
            "player_start": {
                "x_rel": self.player_start[0] / self.world_width,
                "y_rel": self.player_start[1] / self.world_height
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

            # Размер уровня
            if "world_width" in data:
                self.world_width = data["world_width"]
            if "world_height" in data:
                self.world_height = data["world_height"]

            # Финиш
            finish = data.get("finish")
            if finish and "x_rel" in finish:
                x = int(finish["x_rel"] * self.world_width)
                y = int(finish["y_rel"] * self.world_height)
                self.finish_pos = (x, y)
            else:
                self.finish_pos = None

        except Exception as e:
            print(f"Ошибка загрузки: {e}")

    def on_update(self, delta_time):
        """Плавное панорамирование камеры при удержании клавиш"""
        speed = self.grid_size * 10 * delta_time  # пикс/сек, привязка к сетке

        if self.pan_left:
            self.view_offset_x = max(0, self.view_offset_x - speed)
        if self.pan_right:
            self.view_offset_x = min(max(0, self.world_width - self.window.width), self.view_offset_x + speed)
        if self.pan_up:
            self.view_offset_y = max(0, self.view_offset_y - speed)
        if self.pan_down:
            self.view_offset_y = min(max(0, self.world_height - self.window.height), self.view_offset_y + speed)
