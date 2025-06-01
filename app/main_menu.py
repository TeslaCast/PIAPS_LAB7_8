import pygame
from button import Button
from scene import Scene
from mainbox import MainBox  # Импортируем MainBox
from interface import Drawable, Clickable
from typing import List


class MainMenu(Drawable, Clickable):
    def __init__(self,game, x: int = 50, y: int = 100, button_width: int = 200, button_height: int = 50, spacing: int = 20):
        self.game = game
        self.x = x
        self.y = y
        self.button_width = button_width
        self.button_height = button_height
        self.spacing = spacing
        self.buttons: List[Button] = []
        self._init_buttons()

    def _init_buttons(self):
        labels = ["Новая игра", "Загрузить", "Выйти", "Продолжить"]
        funcs = [self.start_new_game, self.load_game, self.exit_game, self.continue_game]

        for i, (label, func) in enumerate(zip(labels, funcs)):
            color = (70, 70, 70)
            if label == "Выйти":
                color = (200, 50, 50)  # Красная кнопка

            btn = Button(
                x=self.x,
                y=self.y + i * (self.button_height + self.spacing),
                width=self.button_width,
                height=self.button_height,
                color=color,
                func=func,
                text=label
            )
            self.buttons.append(btn)

    def draw(self, screen: pygame.Surface):
        for btn in self.buttons:
            btn.draw(screen)

    def collidepoint(self, point) -> bool:
        return any(btn.collidepoint(point) for btn in self.buttons)

    def click(self, screen: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            if btn.collidepoint(mouse_pos):
                btn.click(screen)

    # --- Placeholder handlers ---
    def start_new_game(self, btn, screen):
        # print("Запуск новой игры...")
        # new_scene = Scene()

        # # Создаём MainBox и добавляем в сцену
        # dialogue_box = MainBox(x=100, y=500, width=1080, height=200)
        # dialogue_box.load_from_text("""
        # name(Система): Добро пожаловать в игру!
        # ch: Начать приключение
        # ---
        # name(Система): Вы выбрали начать!
        # ch: Продолжить
        # """)
        # new_scene.add_obj(dialogue_box)

        # self.game.set_scene(new_scene)
        self.game.SetActiveScene(1)  # Set to the new scene (ID 1)
    def load_game(self, btn, screen):
        print("Загрузка — ещё не реализовано")

    def exit_game(self, btn, screen):
        print("Выход из игры...")
        pygame.quit()
        exit()

    def continue_game(self, btn, screen):
        print("Продолжить — ещё не реализовано")
