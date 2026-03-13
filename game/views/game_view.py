import arcade
import os
from arcade import Camera2D
from game.constants import *
from game.player import Player
from game.utils.level_loader import LevelLoader
from game.views.message_view import MessageView


class GameView(arcade.View):
    """Игровой экран с камерой, следующей за игроком"""

    def __init__(self):
        super().__init__()

        # Объекты игры
        self.player = None
        self.player_sprite = None
        self.wall_list = None
        self.coin_list = None

        # Игровые данные
        self.score = 0
        self.level_name = ""
        self.finished = False

        # Физический движок
        self.physics_engine = None

        # Управление
        self.left_pressed = False
        self.right_pressed = False

        # Масштабирование
        self.world_width = 3000  # расширенный размер уровня по горизонтали
        self.world_height = 900  # чуть больше места по вертикали
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.camera = None
        self.gui_camera = None
        self.finish_sprite = None

    def setup(self, level_name):
        """Настройка уровня с масштабированием"""
        self.level_name = level_name
        self.score = 0
        self.finished = False

        screen_width = self.window.width
        screen_height = self.window.height
        # Масштаб больше не зависит от разрешения: объекты остаются одного размера,
        # а большее окно просто показывает больший участок мира
        self.scale_x = 1.0
        self.scale_y = 1.0

        # Камеры
        self.camera = Camera2D(window=self.window)
        self.gui_camera = Camera2D(window=self.window)

        # Создаем игрока
        self.player = Player()

        # Масштаб объектов
        game_scale = 1.0

        # Физический спрайт игрока
        try:
            self.player_sprite = arcade.SpriteSolidColor(
                int(self.player.width * game_scale),
                int(self.player.height * game_scale),
                self.player.color
            )
        except Exception:
            self.player_sprite = arcade.Sprite()
            self.player_sprite.color = self.player.color
            self.player_sprite.width = int(self.player.width * game_scale)
            self.player_sprite.height = int(self.player.height * game_scale)

        # Стартовая позиция
        self.player_sprite.center_x = int(150 * self.scale_x)
        self.player_sprite.center_y = int(200 * self.scale_y)
        self.player.center_x = self.player_sprite.center_x
        self.player.center_y = self.player_sprite.center_y

        # Списки спрайтов
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.finish_sprite = None
        self.finish_list = arcade.SpriteList()
        # Пытаемся загрузить уровень из файла, иначе строим стандартный
        level_path = os.path.join(LEVELS_DIR, f"{level_name}.json")
        level_data = LevelLoader.load_level(level_path)

        if level_data:
            self._build_from_level(level_data)
        else:
            self._build_fallback_level(game_scale)

        # Физический движок
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player_sprite,
            platforms=self.wall_list,
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        """Отрисовка игры"""
        self.clear()
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        if self.camera:
            self.camera.use()

        # Объекты
        self.wall_list.draw()
        self.coin_list.draw()
        if self.finish_list:
            self.finish_list.draw()

        # Игрок
        if self.player:
            self.player.draw()

        if self.gui_camera:
            self.gui_camera.use()

        # Интерфейс
        screen_width = self.window.width
        screen_height = self.window.height
        center_x = screen_width // 2

        base_font_size = max(16, min(24, screen_width // 50))

        arcade.draw_text(
            f"Уровень: {self.level_name}",
            center_x,
            screen_height - 40,
            arcade.color.WHITE,
            base_font_size,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            f"Очки: {self.score}",
            center_x,
            screen_height - 80,
            arcade.color.WHITE,
            base_font_size,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "WASD/Стрелки: движение | Пробел: прыжок",
            center_x,
            40,
            arcade.color.WHITE,
            base_font_size - 4,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "[ESC] Меню",
            20,
            screen_height - 40,
            arcade.color.WHITE,
            base_font_size - 4
        )

        arcade.draw_text(
            "[R] Рестарт",
            screen_width - 120,
            screen_height - 40,
            arcade.color.WHITE,
            base_font_size - 4
        )

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if key in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            if self.physics_engine and self.physics_engine.can_jump():
                jump_speed = PLAYER_JUMP_SPEED * self.scale_y
                self.player_sprite.change_y = jump_speed
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
            self.update_player_movement()
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
            self.update_player_movement()
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            self.window.show_view(MenuView())
        elif key == arcade.key.R:
            self.setup(self.level_name)

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
            self.update_player_movement()
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False
            self.update_player_movement()

    def update_player_movement(self):
        """Обновление движения игрока"""
        if self.player_sprite:
            speed = 0
            if self.left_pressed and not self.right_pressed:
                speed = -PLAYER_MOVEMENT_SPEED * self.scale_x
            elif self.right_pressed and not self.left_pressed:
                speed = PLAYER_MOVEMENT_SPEED * self.scale_x
            self.player_sprite.change_x = speed

    def on_update(self, delta_time):
        """Обновление игровой логики"""
        if self.physics_engine:
            self.physics_engine.update()

            if self.player and self.player_sprite:
                self.player.center_x = self.player_sprite.center_x
                self.player.center_y = self.player_sprite.center_y

            if self.player_sprite and self.coin_list:
                coins_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
                for coin in coins_hit:
                    coin.remove_from_sprite_lists()
                    self.score += 10

            # Финиш
            if not self.finished and self.finish_sprite and arcade.check_for_collision(self.player_sprite, self.finish_sprite):
                self.finished = True
                self.on_level_complete()

            # Проверяем падение
            if self.player and self.player.center_y < -100:
                self.setup(self.level_name)

            # Ограничиваем игрока по горизонтали
            if self.player_sprite:
                if self.player_sprite.center_x < 0:
                    self.player_sprite.center_x = 0
                    self.player_sprite.change_x = 0
                elif self.player_sprite.center_x > self.world_width:
                    self.player_sprite.center_x = self.world_width
                    self.player_sprite.change_x = 0

            # Камера за игроком
            self.center_camera_to_player()

    def on_level_complete(self):
        """Возврат в главное меню после окончания уровня"""
        from game.views.menu_view import MenuView
        self.window.show_view(MenuView())

    def center_camera_to_player(self):
        """Перемещает камеру за игроком с ограничениями уровня"""
        if not self.camera or not self.player_sprite:
            return

        # Центрировать камеру строго на игроке
        target_x = self.player_sprite.center_x
        target_y = self.player_sprite.center_y

        half_w = self.window.width / 2
        half_h = self.window.height / 2

        target_x = max(half_w, min(target_x, self.world_width - half_w))
        target_y = max(half_h, min(target_y, self.world_height - half_h))

        # Без инерции — мгновенно фиксируем на игроке
        self.camera.position = (target_x, target_y)

    # -----------------------
    # Вспомогательные методы
    # -----------------------
    def _build_from_level(self, data):
        """Строит уровень из JSON (поддержка относительных и абсолютных координат)"""
        platforms = data.get("platforms", [])
        coins = data.get("coins", [])
        player_start = data.get("player_start", {})
        finish_data = data.get("finish", {})
        grid_size = data.get("grid_size", 64)

        rel = any("x_rel" in p for p in platforms) or "x_rel" in player_start

        # Определяем размеры мира
        if rel:
            base_w = data.get("world_width", data.get("screen_width", self.world_width))
            base_h = data.get("world_height", data.get("screen_height", self.world_height))
            self.world_width = max(base_w, self.window.width)
            self.world_height = max(base_h, self.window.height)
        else:
            max_x = max((p.get("x", 0) + p.get("width", grid_size) // 2) for p in platforms) if platforms else self.world_width
            max_y = max((p.get("y", 0) + p.get("height", grid_size) // 2) for p in platforms) if platforms else self.world_height
            max_coin_x = max((c.get("x", 0)) for c in coins) if coins else 0
            max_coin_y = max((c.get("y", 0)) for c in coins) if coins else 0
            self.world_width = max(self.world_width, max_x + 200, max_coin_x + 200)
            self.world_height = max(self.world_height, max_y + 200, max_coin_y + 200)

        # Платформы
        for p in platforms:
            if rel:
                x = p["x_rel"] * self.world_width
                y = p["y_rel"] * self.world_height
                w = p.get("width_rel", grid_size / self.world_width) * self.world_width
                h = p.get("height_rel", grid_size / self.world_height) * self.world_height
            else:
                x = p.get("x", 0)
                y = p.get("y", 0)
                w = p.get("width", grid_size)
                h = p.get("height", grid_size)

            plat = arcade.SpriteSolidColor(int(w), int(h), arcade.color.DARK_GREEN)
            plat.center_x = x
            plat.center_y = y
            self.wall_list.append(plat)

        # Земля, если платформ нет
        if not platforms:
            for x in range(-100, int(self.world_width + 100), grid_size):
                ground = arcade.SpriteSolidColor(grid_size, grid_size, arcade.color.GREEN)
                ground.center_x = x
                ground.center_y = grid_size // 2
                self.wall_list.append(ground)

        # Монеты
        for c in coins:
            if rel:
                x = c["x_rel"] * self.world_width
                y = c["y_rel"] * self.world_height
            else:
                x = c.get("x", 0)
                y = c.get("y", 0)
            coin = arcade.SpriteSolidColor(grid_size // 2, grid_size // 2, arcade.color.YELLOW)
            coin.center_x = x
            coin.center_y = y
            self.coin_list.append(coin)

        # Старт игрока
        if rel:
            sx = player_start.get("x_rel", 0.1) * self.world_width
            sy = player_start.get("y_rel", 0.2) * self.world_height
        else:
            sx = player_start.get("x", 150)
            sy = player_start.get("y", 200)

        self.player_sprite.center_x = sx
        self.player_sprite.center_y = sy
        self.player.center_x = sx
        self.player.center_y = sy

        # Финиш
        if rel:
            fx = finish_data.get("x_rel", 0.9) * self.world_width if finish_data else self.world_width - 120
            fy = finish_data.get("y_rel", 0.15) * self.world_height if finish_data else grid_size * 2
        else:
            fx = finish_data.get("x", self.world_width - 120) if finish_data else self.world_width - 120
            fy = finish_data.get("y", grid_size * 2) if finish_data else grid_size * 2
        self._create_finish_sprite(fx, fy, grid_size)

    def _build_fallback_level(self, game_scale):
        """Стандартный уровень на случай отсутствия файла"""
        wall_width = 64
        wall_height = 64
        platform_width = 96
        platform_height = 32
        coin_size = 25

        for x in range(-100, int(self.world_width + 100), wall_width):
            wall = arcade.SpriteSolidColor(wall_width, wall_height, arcade.color.GREEN)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        platforms = [
            (int(self.world_width * 0.15), 200),
            (int(self.world_width * 0.30), 280),
            (int(self.world_width * 0.45), 220),
            (int(self.world_width * 0.60), 320),
            (int(self.world_width * 0.75), 260),
            (int(self.world_width * 0.90), 180),
        ]

        for x, y in platforms:
            plat = arcade.SpriteSolidColor(platform_width, platform_height, arcade.color.DARK_GREEN)
            plat.center_x = x
            plat.center_y = y
            self.wall_list.append(plat)

        coin_positions = [
            (int(self.world_width * 0.10), 150),
            (int(self.world_width * 0.18), 210),
            (int(self.world_width * 0.26), 150),
            (int(self.world_width * 0.34), 250),
            (int(self.world_width * 0.42), 300),
            (int(self.world_width * 0.50), 230),
            (int(self.world_width * 0.58), 320),
            (int(self.world_width * 0.66), 230),
            (int(self.world_width * 0.74), 200),
            (int(self.world_width * 0.82), 260),
            (int(self.world_width * 0.90), 180),
        ]

        for x, y in coin_positions:
            coin = arcade.SpriteSolidColor(coin_size, coin_size, arcade.color.YELLOW)
            coin.center_x = x
            coin.center_y = y
            self.coin_list.append(coin)

        # Финиш в конце уровня
        self._create_finish_sprite(self.world_width - 120, int(96 * game_scale), wall_width)

    def _create_finish_sprite(self, x, y, size):
        """Создает спрайт финиша (красный столб)"""
        width = int(size * 0.6)
        height = int(size * 1.0)
        finish = arcade.SpriteSolidColor(width, height, arcade.color.RED)
        finish.color = arcade.color.RED  # гарантируем красный тинт
        finish.center_x = x
        finish.center_y = y
        self.finish_sprite = finish
        self.finish_list = arcade.SpriteList()
        self.finish_list.append(finish)
