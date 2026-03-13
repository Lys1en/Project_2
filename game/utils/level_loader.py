import json
import os
from game.constants import LEVELS_DIR


class LevelLoader:
    """Загрузчик уровней"""

    @staticmethod
    def load_level(filename):
        """Загрузка уровня из файла"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None

    @staticmethod
    def get_available_levels():
        """Получение списка доступных уровней"""
        if not os.path.exists(LEVELS_DIR):
            return []

        levels = []
        for file in os.listdir(LEVELS_DIR):
            if file.endswith(".json"):
                levels.append(file[:-5])

        return sorted(levels)