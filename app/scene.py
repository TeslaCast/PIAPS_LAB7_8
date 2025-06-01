from interfaces import Drawable, Clickable

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
    