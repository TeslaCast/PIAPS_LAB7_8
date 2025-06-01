import pygame
from typing import Protocol, Callable, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    def draw(self, screen) -> None: ...

@runtime_checkable
class Clickable(Protocol):
    def collidepoint(self, point) -> bool: ...
    def click(self, screen: pygame.Surface) -> None: ...
from scene import Scene
class Game:
    def __init__(self, gameName: str):
        pygame.init()
        self.__screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption(gameName)
        self.__running = False
        self.__clock = pygame.time.Clock()
        self.__current_scene: Scene | None = None  # Текущая сцена

    def set_scene(self, scene: Scene):
        """Устанавливает текущую сцену."""
        self.__current_scene = scene

    def get_screen_size(self) -> tuple[int, int]:
        """Возвращает текущее разрешение окна."""
        screen = pygame.display.get_surface()
        return screen.get_width(), screen.get_height()

    def Run(self):
        self.__running = True
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__running = False
                    elif event.key == pygame.K_SPACE:
                        print("Пробел нажат!")
                if event.type == pygame.MOUSEBUTTONDOWN and self.__current_scene:
                    for clicked in self.__current_scene._getClickableObjects():
                        if clicked.collidepoint(event.pos):
                            clicked.click(self.__screen)
                            print("Кнопка нажата!")

            self.__screen.fill((176, 224, 230))  # Фон

            # Отрисовка текущей сцены
            if self.__current_scene:
                self.__current_scene.render(self.__screen)

            pygame.display.flip()
            self.__clock.tick(60)

        pygame.quit()