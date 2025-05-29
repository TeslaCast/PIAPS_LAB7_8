import pygame
from typing import Protocol, Callable, runtime_checkable
import random

def passFunc(obj, screen):
    pass

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, color, func=passFunc, text=""):
        self.button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.func = func
        ##########
        self.font = pygame.font.SysFont("arial", 24)
        self.text_surface = self.font.render(text, True, (255, 255, 255))  # Белый текст
        self.text_rect = self.text_surface.get_rect(center=(self.x+self.width//2, self.y+self.height//2))  # Центр кнопки
        self.button_surface.blit(self.text_surface, self.text_rect)

    def draw(self, screen):
        self.button_surface.fill(self.color)
        # пересчитываем позицию текста (на случай перемещений, не строго обязательно)
        self.text_rect = self.text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.button_surface.blit(self.text_surface, self.text_rect)
        screen.blit(self.button_surface, (self.x, self.y))
        #pygame.draw.rect(surface=screen, color=self.color, rect=self.button_rect)
    def click(self, screen) -> None:
        self.func(self,screen)
    def collidepoint(self, point) -> bool:
        (x, y) = point
        # print(point)
        # print((self.x, self.y))ы
        return (y >= self.y and y <= self.y + self.height) and (x >= self.x and x <= self.x + self.width)

@runtime_checkable
class Drawable(Protocol):
    def draw(self, screen) -> None: ...

@runtime_checkable
class Clickable(Protocol):
    def click(self, screen: pygame.Surface) -> None: ...
    def collidepoint(self, point) -> bool: ...

class Scene:
    def __init__(self):
        self.__objects: list[Drawable] = []
        self.IsObjectVisible: list[bool] = []
        self.__clickable_objects: list[Clickable] = [] 
    def _getClickableObjects(self) -> list[Clickable]:
        return self.__clickable_objects
    def render(self, screen):
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
        
class Game:
    def __init__(self, gameName: str):
        pygame.init()
        self.__screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption(gameName)
        self.__running = False
        self.__clock = pygame.time.Clock()
        self.__scenes: list[Scene] = [Scene()]
        self.ActiveSceneID = 0 
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
                    for clicked in self.__scenes[self.ActiveSceneID]._getClickableObjects():
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
        self.__scenes[self.ActiveSceneID].render(screen)
        # for obj in self.__objects:
        #     obj.draw(screen)
    def add_obj(self, obj: Drawable):
        Id = self.__scenes[self.ActiveSceneID].add_obj(obj)
        return Id, self.ActiveSceneID
    def SetActiveScene(self, Id) -> int:
        if Id > len(self.__scenes):
            self.ActiveSceneID = len(self.__scenes)
            self.__scenes.append(Scene())
            return self.ActiveSceneID
        self.ActiveSceneID = Id
        return Id
    def AddScene(self, scene: Scene):
        self.__scenes.append(scene)
        
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
    