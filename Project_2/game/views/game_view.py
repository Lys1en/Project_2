import arcade
from game.constants import *
from game.player import Player


class GameView(arcade.View):
    """Игровой экран с масштабированием под разрешение"""

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

        # Физический движок
        self.physics_engine = None

        # Управление
        self.left_pressed = False
        self.right_pressed = False

        # Масштабирование
        self.world_width = 1500  # Фиксированная ширина игрового мира
        self.world_height = 800  # Фиксированная высота игрового мира
        self.scale_x = 1.0
        self.scale_y = 1.0

    def setup(self, level_name):
        """Настройка уровня с масштабированием"""
        self.level_name = level_name
        self.score = 0

        # Вычисляем масштаб для текущего разрешения
        screen_width = self.window.width
        screen_height = self.window.height
        self.scale_x = screen_width / self.world_width
        self.scale_y = screen_height / self.world_height

        # Масштаб для игровых объектов (берем минимальный масштаб чтобы сохранить пропорции)
        game_scale = min(self.scale_x, self.scale_y) * 0.8  # 80% от экрана

        # Создаем игрока
        self.player = Player()

        # Создаем физический спрайт
        try:
            self.player_sprite = arcade.SpriteSolidColor(
                int(self.player.width * game_scale),
                int(self.player.height * game_scale),
                self.player.color
            )
        except:
            self.player_sprite = arcade.Sprite()
            self.player_sprite.color = self.player.color
            self.player_sprite.width = int(self.player.width * game_scale)
            self.player_sprite.height = int(self.player.height * game_scale)

        # Стартовая позиция по центру внизу
        self.player_sprite.center_x = screen_width // 2
        self.player_sprite.center_y = int(200 * self.scale_y)
        self.player.center_x = self.player_sprite.center_x
        self.player.center_y = self.player_sprite.center_y

        # Создаем списки спрайтов
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Масштабируем размеры объектов
        wall_width = int(64 * game_scale)
        wall_height = int(64 * game_scale)
        platform_width = int(96 * game_scale)
        platform_height = int(32 * game_scale)
        coin_size = int(25 * game_scale)

        # Создаем землю по ширине экрана
        for x in range(-100, screen_width + 100, wall_width):
            try:
                wall = arcade.SpriteSolidColor(wall_width, wall_height, arcade.color.GREEN)
            except:
                wall = arcade.Sprite()
                wall.color = arcade.color.GREEN
                wall.width = wall_width
                wall.height = wall_height

            wall.center_x = x
            wall.center_y = int(32 * self.scale_y)
            self.wall_list.append(wall)

        # Добавляем платформы (масштабируем позиции)
        platforms = [
            (int(screen_width * 0.2), int(200 * self.scale_y)),  # 20% ширины
            (int(screen_width * 0.5), int(300 * self.scale_y)),  # 50% ширины
            (int(screen_width * 0.8), int(250 * self.scale_y)),  # 80% ширины
            (int(screen_width * 0.35), int(180 * self.scale_y)),  # 35% ширины
            (int(screen_width * 0.65), int(180 * self.scale_y)),  # 65% ширины
        ]

        for x, y in platforms:
            try:
                wall = arcade.SpriteSolidColor(platform_width, platform_height, arcade.color.DARK_GREEN)
            except:
                wall = arcade.Sprite()
                wall.color = arcade.color.DARK_GREEN
                wall.width = platform_width
                wall.height = platform_height

            wall.center_x = x
            wall.center_y = y
            self.wall_list.append(wall)

        # Добавляем монеты (масштабируем позиции)
        coin_positions = [
            (int(screen_width * 0.15), int(150 * self.scale_y)),
            (int(screen_width * 0.3), int(150 * self.scale_y)),
            (int(screen_width * 0.45), int(150 * self.scale_y)),
            (int(screen_width * 0.2), int(250 * self.scale_y)),
            (int(screen_width * 0.5), int(280 * self.scale_y)),
            (int(screen_width * 0.8), int(230 * self.scale_y)),
            (int(screen_width * 0.35), int(230 * self.scale_y)),
            (int(screen_width * 0.65), int(230 * self.scale_y)),
        ]

        for x, y in coin_positions:
            try:
                coin = arcade.SpriteSolidColor(coin_size, coin_size, arcade.color.YELLOW)
            except:
                coin = arcade.Sprite()
                coin.color = arcade.color.YELLOW
                coin.width = coin_size
                coin.height = coin_size

            coin.center_x = x
            coin.center_y = y
            self.coin_list.append(coin)

        # Физический движок
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player_sprite,
            platforms=self.wall_list,
            gravity_constant=GRAVITY * self.scale_y  # Масштабируем гравитацию
        )

    def on_draw(self):
        """Отрисовка игры"""
        self.clear()
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Рисуем объекты (они уже масштабированы)
        self.wall_list.draw()
        self.coin_list.draw()

        # Рисуем игрока с масштабированием
        if self.player:
            self.player.draw()

        # Интерфейс (адаптивный)
        screen_width = self.window.width
        screen_height = self.window.height
        center_x = screen_width // 2

        # Размер шрифта в зависимости от разрешения
        base_font_size = max(16, min(24, screen_width // 50))

        # Уровень - вверху по центру
        arcade.draw_text(
            f"Уровень: {self.level_name}",
            center_x,
            screen_height - 40,
            arcade.color.WHITE,
            base_font_size,
            anchor_x="center",
            anchor_y="center"
        )

        # Очки - под уровнем
        arcade.draw_text(
            f"Очки: {self.score}",
            center_x,
            screen_height - 80,
            arcade.color.WHITE,
            base_font_size,
            anchor_x="center",
            anchor_y="center"
        )

        # Управление - внизу по центру
        arcade.draw_text(
            "WASD/Стрелки: движение | Пробел: прыжок",
            center_x,
            40,
            arcade.color.WHITE,
            base_font_size - 4,
            anchor_x="center",
            anchor_y="center"
        )

        # Меню и рестарт - по углам
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
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine and self.physics_engine.can_jump():
                # Масштабируем скорость прыжка
                jump_speed = PLAYER_JUMP_SPEED * self.scale_y
                self.player_sprite.change_y = jump_speed

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.update_player_movement()

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.update_player_movement()

        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            self.window.show_view(MenuView())

        elif key == arcade.key.R:
            self.setup(self.level_name)

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
            self.update_player_movement()

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            self.update_player_movement()

    def update_player_movement(self):
        """Обновление движения игрока"""
        if self.player_sprite:
            # Масштабируем скорость движения
            speed = 0
            if self.left_pressed and not self.right_pressed:
                speed = -PLAYER_MOVEMENT_SPEED * self.scale_x
            elif self.right_pressed and not self.left_pressed:
                speed = PLAYER_MOVEMENT_SPEED * self.scale_x

            self.player_sprite.change_x = speed

    def on_update(self, delta_time):
        """Обновление игровой логики"""
        if self.physics_engine:
            # Обновляем физику
            self.physics_engine.update()

            # Синхронизируем позицию
            if self.player and self.player_sprite:
                self.player.center_x = self.player_sprite.center_x
                self.player.center_y = self.player_sprite.center_y

            # Проверяем сбор монет
            if self.player_sprite and self.coin_list:
                coins_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
                for coin in coins_hit:
                    coin.remove_from_sprite_lists()
                    self.score += 10

            # Проверяем падение
            screen_height = self.window.height
            if self.player and self.player.center_y < -100:
                self.setup(self.level_name)

            # Ограничиваем игрока по горизонтали
            if self.player_sprite:
                if self.player_sprite.center_x < 0:
                    self.player_sprite.center_x = 0
                    self.player_sprite.change_x = 0
                elif self.player_sprite.center_x > self.window.width:
                    self.player_sprite.center_x = self.window.width
                    self.player_sprite.change_x = 0