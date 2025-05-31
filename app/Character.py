import pygame
from typing import Tuple, Dict
from abc import ABC, abstractmethod

class CharacterDisplayStrategy(ABC):
    @abstractmethod
    def display(self, character, screen):
        pass


class DefaultDisplayStrategy(CharacterDisplayStrategy):
    def display(self, character, screen):
        screen.blit(character.current_emotion, character.rect)


class DarkenedDisplayStrategy(CharacterDisplayStrategy):
    def display(self, character, screen):
        darkened = character.current_emotion.copy()
        darken = pygame.Surface(darkened.get_size(), pygame.SRCALPHA)
        darken.fill((80, 80, 80, 0))
        darkened.blit(darken, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        screen.blit(darkened, character.rect)


class HiddenDisplayStrategy(CharacterDisplayStrategy):
    def display(self, character, screen):
        pass


class Character:
    def __init__(self, x: int, y: int, name: str = "", name_color: Tuple[int, int, int] = (200, 200, 0)):
        self.x = x
        self.y = y
        self.name = name
        self.name_color = name_color  # Цвет имени персонажа
        self.emotions: Dict[str, pygame.Surface] = {}
        self.current_emotion = None
        self._display_strategy: CharacterDisplayStrategy = DefaultDisplayStrategy()
        self.rect = None
        self.is_active = False
        self.is_visible = True

    #Добавление эмоций(png) персонажа
    def add_emotion(self, emotion_name: str, image_path: str):
    try:
        image = pygame.image.load(image_path).convert_alpha()
        self.emotions[emotion_name] = image
        if len(self.emotions) == 1:
            self.set_emotion(emotion_name)
    except:
        print(f"Error loading image: {image_path}")
        image = pygame.Surface((200, 400), pygame.SRCALPHA)
        pygame.draw.rect(image, (100, 100, 100), (0, 0, 200, 400))
        self.emotions[emotion_name] = image
        if len(self.emotions) == 1:
            self.set_emotion(emotion_name)
            
    #Изменение эмоций(png) персонажа
    def set_emotion(self, emotion_name: str):
        if emotion_name in self.emotions:
            self.current_emotion = self.emotions[emotion_name]
            self.rect = self.current_emotion.get_rect(topleft=(self.x, self.y))
            self.update_display_strategy()

    #Изменение отображение персонажа
    def set_display(self, strategy: CharacterDisplayStrategy):
        self._display_strategy = strategy

    #Изменение позиции персонажа
    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y
        if self.current_emotion:
            self.rect = self.current_emotion.get_rect(topleft=(self.x, self.y))

    #Изменение видимости/невидимости персонажа
    def toggle_visibility(self):
        """Переключает видимость персонажа"""
        self.is_visible = not self.is_visible
        self.update_display()

    #Обновление отображение персонажа
    def update_display(self):
        """Обновляет стратегию отображения в зависимости от состояния"""
        if not self.is_visible:
            self.set_display(HiddenDisplayStrategy())
        elif self.is_active:
            self.set_display(DefaultDisplayStrategy())
        else:
            self.set_display(DarkenedDisplayStrategy())

    #Отрисовка персонажа
    def draw(self, screen):
        if self.current_emotion and self.is_visible:
            self._display_strategy.display(self, screen)