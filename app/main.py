import pygame
from game import Game
from button import Button
from scene import Scene
import random


  
if __name__ == "__main__":
    game = Game("Простая игра")
    def func(obj:Button, screen:pygame.surface):
        obj.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        obj.x = random.randint(0, 640)
        obj.y = random.randint(0, 480)
        print("Функция вызвалась")
    button = Button(100,100, 100, 100, (255, 0, 0), func, "Нажми")
    game.add_obj(button)
    def func2(obj:Button, screen:pygame.surface):
        if game.ActiveSceneID == 0:
            game.SetActiveScene(1)
        else:
            game.SetActiveScene(0)
        print("Функция вызвалась")
    button = Button(100,200, 100, 100, (0, 0, 0), func2)
    game.add_obj(button)
    scene = Scene()
    scene.add_obj(button)
    game.AddScene(scene)
    game.Run()
    