from ursina import *

class Scene():
    def __init__(self, is_current_scene) -> None:
        self.entities = []
        self.is_current_scene = is_current_scene

        if self.is_current_scene:
            for entity in self.entities:
                entity.enabled = False

    def transition(self,scene):
        for entity in self.entities:
            destroy(entity)
        
        for entity in scene.entities:
            entity.enabled = True
        
        self.is_current_scene = False
        scene.is_current_scene = True
    
    def update(self):
        pass

    
