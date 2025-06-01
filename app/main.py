import pygame
from button import Button
from interface import Game
from mainbox import MainBox
from scene import Scene

if __name__ == "__main__":
    game = Game("Простая игра")
    width, height = 1280, 720

    # Создаём сцену
    scene = Scene()

    # Создаём и добавляем MainBox в сцену
    box = MainBox(40, height - 240, width - 80, 200)
    scene.add_obj(box)

   # Загрузка текста из файла
    file_path = "app/h1.txt"
    box.load_from_file(file_path)

    # Устанавливаем сцену в Game
    game.set_scene(scene)

    game.Run()