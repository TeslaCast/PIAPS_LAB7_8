import pygame
from typing import Protocol, Callable, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self, screen) -> None: ...

@runtime_checkable
class Clickable(Protocol):
    def collidepoint(self, point) -> bool: ...
    def click(self, screen: pygame.Surface) -> None: ...

#singleton

class Game:
    def __init__(self, gameName: str):
        pygame.init()
        self.__screen = pygame.display.set_mode((640, 480)) #разрешение

        pygame.display.set_caption(gameName)
        self.__running = False
        self.__clock = pygame.time.Clock()
        self.__objects: list[Drawable] = []
        self.__clickable_objects: list[Clickable] = [] 

        
    def Run(self):
        self.__running = True
        #button_rect = pygame.Rect(100, 100, 200, 50)
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__running = False
                    elif event.key == pygame.K_SPACE:
                        print("Пробел нажат!")

                

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for clicked in self.__clickable_objects:
                        # sup = pygame.Rect(0, 0, 0, 0) 
                        # sup.collidepoint
                        if clicked.collidepoint(event.pos):
                            clicked.click(self.__screen)
                            print("Кнопка нажата!")  
                    # if button_rect.collidepoint(event.pos):
                    #     print("Кнопка нажата!")

            self.__screen.fill((176, 224, 230))  # фон
            

            self.render_all(self.__screen)
            # pygame.draw.circle(self.__screen, (255, 0, 0), (320, 240), 50)  # Красный круг
            # pygame.draw.rect(self.__screen, (0, 255, 0), button_rect)

            pygame.display.flip()
            self.__clock.tick(60)  # Ограничить до 60 кадров в секунду

        pygame.quit()
    def render_all(self, screen):
        for obj in self.__objects:
            obj.draw(screen)

    def add_obj(self, obj: Drawable):
        # print(type(obj))
        # self.__objects.append(obj)
        if isinstance(obj, Drawable):
            self.__objects.append(obj)   
        if isinstance(obj, Clickable):
            self.__clickable_objects.append(obj)   
