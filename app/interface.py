from typing import Protocol, Callable, runtime_checkable
import pygame

@runtime_checkable
class Drawable(Protocol):
    def draw(self, screen) -> None: ...

@runtime_checkable
class Clickable(Protocol):
    def click(self, screen: pygame.Surface) -> None: ...
    def collidepoint(self, point) -> bool: ...

