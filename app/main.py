import pygame
from button import Button
from interface import Game
        
if __name__ == "__main__":
    game = Game("Простая игра")
    # def func(obj:Button, screen:pygame.surface):
    #     obj.color = (255,255,0)
    #     obj.x = obj.x+10
    #     print("Функция вызвалась")


    button = Button(100,100, 100, 100, (255, 0, 0))
    game.add_obj(button)
    button = Button(100,200, 100, 100, (0, 0, 0))
    game.add_obj(button)
    game.Run()
    