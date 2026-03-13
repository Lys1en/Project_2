"""
Исправления для совместимости функций рисования в Arcade
"""

import arcade


def apply_draw_compatibility():
    """Применяет исправления для функций рисования"""

    # Проверяем, есть ли модуль arcade.draw
    if hasattr(arcade, 'draw'):
        print("Используется Arcade с модулем arcade.draw - создаем алиасы")

        # Создаем алиасы для обратной совместимости
        arcade.draw_rectangle_filled = arcade.draw.rectangle_filled
        arcade.draw_rectangle_outline = arcade.draw.rectangle_outline
        arcade.draw_circle_filled = arcade.draw.circle_filled
        arcade.draw_circle_outline = arcade.draw.circle_outline
        arcade.draw_line = arcade.draw.line
        arcade.draw_text = arcade.draw.text
        arcade.draw_lrwh_rectangle_textured = arcade.draw.lrwh_rectangle_textured
        arcade.draw_texture_rectangle = arcade.draw.texture_rectangle
        arcade.draw_triangle_filled = arcade.draw.triangle_filled
    else:
        print("Используется старая версия Arcade, функции уже на месте")


# Применяем исправления при импорте
apply_draw_compatibility()