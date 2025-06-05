import pygame
from typing import Tuple, Dict, List, Protocol, Callable
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

# Паттерн Состояние для персонажа
class CharacterState(ABC):
    @abstractmethod
    def handle(self, character):
        pass

class ActiveState(CharacterState):
    def handle(self, character):
        character.is_active = True
        character.is_visible = True
        character.set_display(DefaultDisplayStrategy())

class InactiveState(CharacterState):
    def handle(self, character):
        character.is_active = False
        character.is_visible = True
        character.set_display(DarkenedDisplayStrategy())

class HiddenState(CharacterState):
    def handle(self, character):
        character.is_active = False
        character.is_visible = False
        character.set_display(HiddenDisplayStrategy())

# Паттерн Наблюдатель для персонажа
class CharacterObserver(Protocol):
    def on_state_change(self, character): ...

class Character:
    def __init__(self, x: int, y: int, name: str = "", name_color: Tuple[int, int, int] = (200, 200, 0)):
        self.x = x
        self.y = y
        self.name = name
        self.name_color = name_color
        self.emotions: Dict[str, pygame.Surface] = {}
        self.current_emotion = None
        self._display_strategy: CharacterDisplayStrategy = DefaultDisplayStrategy()
        self.rect = None
        self.state: CharacterState = ActiveState()
        self.is_active = False
        self.is_visible = True
        self._observers: List[CharacterObserver] = []

    def add_observer(self, observer: CharacterObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: CharacterObserver):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.on_state_change(self)

    def set_state(self, state: CharacterState):
        self.state = state
        self.state.handle(self)
        self.notify_observers()

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

    def set_emotion(self, emotion_name: str):
        if emotion_name in self.emotions:
            self.current_emotion = self.emotions[emotion_name]
            self.rect = self.current_emotion.get_rect(topleft=(self.x, self.y))
            self.update_display()

    def set_display(self, strategy: CharacterDisplayStrategy):
        self._display_strategy = strategy

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y
        if self.current_emotion:
            self.rect = self.current_emotion.get_rect(topleft=(self.x, self.y))

    def toggle_visibility(self):
        self.is_visible = not self.is_visible
        self.update_display()

    def update_display(self):
        if not self.is_visible:
            self.set_display(HiddenDisplayStrategy())
        elif self.is_active:
            self.set_display(DefaultDisplayStrategy())
        else:
            self.set_display(DarkenedDisplayStrategy())

    def draw(self, screen):
        if self.current_emotion and self.is_visible:
            self._display_strategy.display(self, screen)
