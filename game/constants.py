import arcade

# Доступные разрешения
RESOLUTIONS = [
    (800, 600, "800x600"),
    (1024, 768, "1024x768"),
    (1280, 720, "1280x720 (HD)"),
    (1366, 768, "1366x768"),
    (1600, 900, "1600x900"),
    (1920, 1080, "1920x1080 (Full HD)"),
    (2560, 1440, "2560x1440 (2K)"),
    (3840, 2160, "3840x2160 (4K)"),
]

# Текущее разрешение по умолчанию
DEFAULT_RESOLUTION_INDEX = 2  # 1280x720
SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE = RESOLUTIONS[DEFAULT_RESOLUTION_INDEX]
SCREEN_TITLE = "Платформер"

# Игровые константы
CHARACTER_SCALING = 1.0
TILE_SCALING = 0.5
COIN_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 7  # было 5
GRAVITY = 1.0
PLAYER_JUMP_SPEED = 19  # было 15

# Пути
LEVELS_DIR = "levels"
SAVES_DIR = "saves"
SETTINGS_FILE = "saves/settings.json"

# Цвета
BACKGROUND_COLOR = arcade.color.DARK_BLUE
UI_COLOR = arcade.color.WHITE
HIGHLIGHT_COLOR = arcade.color.YELLOW
