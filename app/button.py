import pygame
from typing import Callable

def passFunc(obj, screen):
    pass

# Декоратор для кнопок, добавляющий функционал (например, логирование)
class ButtonDecorator:
    def __init__(self, button):
        self._button = button

    def draw(self, screen):
        self._button.draw(screen)

    def click(self, screen):
        print(f"Button '{self._button.text}' clicked")
        self._button.click(screen)

    def collidepoint(self, point):
        return self._button.collidepoint(point)

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, color, func=passFunc, text=""): 
        self.button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.func = func
        self.text = text  # Add text attribute to store the button's text
        ##########
        self.font = pygame.font.SysFont("arial", 24)
        self.text_surface = self.font.render(text, True, (255, 255, 255))  # Белый текст
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))  # Центр кнопки
        self.button_surface.blit(self.text_surface, self.text_rect)

    def draw(self, screen):
        self.button_surface.fill(self.color)
        # пересчитываем позицию текста (на случай перемещений, не строго обязательно)
        self.text_rect = self.text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.button_surface.blit(self.text_surface, self.text_rect)
        screen.blit(self.button_surface, (self.x, self.y))

    def click(self, screen) -> None:
        self.func(self, screen)

    def collidepoint(self, point) -> bool:
        (x, y) = point
        return (y >= self.y and y <= self.y + self.height) and (x >= self.x and x <= self.x + self.width)

# Фабрика для создания кнопок
class ButtonFactory:
    @staticmethod
    def create_button(x: int, y: int, width: int, height: int, color, func=passFunc, text=""):
        button = Button(x, y, width, height, color, func, text)
        # Оборачиваем кнопку в декоратор для расширения функционала
        decorated_button = ButtonDecorator(button)
        return decorated_button
