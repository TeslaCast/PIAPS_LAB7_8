from interface import Drawable, Clickable
from mainbox import MainBox
from Character import Character
from typing import Optional
import pygame

class Scene:
    def __init__(self):
        self.__objects: list[Drawable] = []
        self.IsObjectVisible: list[bool] = []
        self.__clickable_objects: list[Clickable] = []
        self.characters: list[Character] = []
        self.current_dialogue: Optional[MainBox] = None
        self.background: Optional[pygame.Surface] = None  # Background attribute

    def _getClickableObjects(self) -> list[Clickable]:
        return self.__clickable_objects

    def render(self, screen):
        # Draw the scene-specific background if it exists
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((176, 224, 230))  # Default background color
        for i in range(len(self.__objects)):
            if self.IsObjectVisible[i]:
                self.__objects[i].draw(screen)

    def add_obj(self, obj: Drawable):
        addedObjId = -1
        if isinstance(obj, Drawable):
            addedObjId = len(self.__objects)
            self.__objects.append(obj)
            self.IsObjectVisible.append(True)
        if isinstance(obj, Clickable):
            self.__clickable_objects.append(obj)
        return addedObjId

    def set_background(self, image_path: str):
        """Set the background for this scene."""
        try:
            self.background = pygame.image.load(image_path).convert()
            self.background = pygame.transform.scale(self.background, (1280, 720))
        except Exception as e:
            print(f"Ошибка загрузки фона: {image_path}, {e}")
            self.background = None