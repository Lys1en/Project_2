import arcade
from arcade import Camera2D
from game.constants import *


class PhysicsEngine:
    """Физический движок игры"""

    def __init__(self, player, walls, gravity=GRAVITY):
        self.player = player
        self.walls = walls
        self.gravity = gravity

        # Создаем физический движок
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=player,
            platforms=walls,
            gravity_constant=gravity
        )

    def update(self):
        """Обновление физики"""
        self.physics_engine.update()

    def can_jump(self):
        """Проверка возможности прыжка"""
        return self.physics_engine.can_jump()

    def jump(self, jump_speed=PLAYER_JUMP_SPEED):
        """Прыжок игрока"""
        if self.can_jump():
            self.player.change_y = jump_speed
            return True
        return False


class Camera:
    """Система камеры"""

    def __init__(self, viewport_width=SCREEN_WIDTH, viewport_height=SCREEN_HEIGHT):
        self.camera = Camera2D()
        self.gui_camera = Camera2D()

    def center_on_player(self, player, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Центрирование камеры на игроке"""
        half_w = screen_width / 2
        half_h = screen_height / 2

        target_x = max(half_w, player.center_x)
        target_y = max(half_h, player.center_y)

        self.camera.position = (target_x, target_y)

    def use_game_camera(self):
        """Активировать игровую камеру"""
        self.camera.use()

    def use_gui_camera(self):
        """Активировать GUI камеру"""
        self.gui_camera.use()


class SceneManager:
    """Менеджер сцены для упрощенной версии"""

    def __init__(self):
        self.scene = None
        self.walls = []
        self.coins = []
        self.enemies = []

    def create_scene(self):
        """Создание новой сцены"""
        self.scene = arcade.Scene()

        # Создаем спрайт-листы
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls")
        self.scene.add_sprite_list("Coins")
        self.scene.add_sprite_list("Enemies")

        # Очищаем списки
        self.walls = []
        self.coins = []
        self.enemies = []

    def add_wall(self, x, y, width=64, height=64):
        """Добавление стены как простого прямоугольника"""
        # Создаем спрайт для стены
        wall = arcade.Sprite()
        wall.center_x = x
        wall.center_y = y
        wall.width = width
        wall.height = height
        wall.color = arcade.color.GREEN  # Цвет для отрисовки

        self.scene.add_sprite("Walls", wall)
        self.walls.append(wall)
        return wall

    def add_coin(self, x, y):
        """Добавление монеты как простого круга"""
        # Создаем спрайт для монеты
        coin = arcade.Sprite()
        coin.center_x = x
        coin.center_y = y
        coin.width = 30
        coin.height = 30
        coin.color = arcade.color.YELLOW  # Цвет для отрисовки

        self.scene.add_sprite("Coins", coin)
        self.coins.append(coin)
        return coin

    def check_collisions(self, player):
        """Проверка столкновений"""
        return arcade.check_for_collision_with_list(player, self.scene["Coins"])

    def remove_coin(self, coin):
        """Удаление монеты"""
        coin.remove_from_sprite_lists()
        if coin in self.coins:
            self.coins.remove(coin)
